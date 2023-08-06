import json
from datetime import datetime, timezone
from typing import Dict, List

import sqlalchemy
from sqlalchemy import Column, Connection, Inspector, Table, bindparam, inspect
from sqlalchemy.engine.interfaces import ReflectedColumn
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql.ddl import CreateSchema
from sqlalchemy.sql.type_api import TypeEngine
from strong_typing.core import JsonType, Schema
from strong_typing.serialization import json_dump_string, json_to_object

from ..dap_types import GetTableDataResult, VersionedSchema
from ..database.connection import DatabaseSession
from .ddl import column_name, execute_ddl, table_name, type_name, value_literal
from .metadata import create_table_definition


def _create_metatable_def(namespace: str) -> sqlalchemy.Table:
    metadata = sqlalchemy.MetaData(schema=namespace)
    metatable = sqlalchemy.Table(
        "dap_meta",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("namespace", sqlalchemy.String(64), nullable=False),
        sqlalchemy.Column("source_table", sqlalchemy.String(64), nullable=False),
        sqlalchemy.Column("timestamp", sqlalchemy.DateTime(), nullable=False),
        sqlalchemy.Column("schema_version", sqlalchemy.Integer, nullable=False),
        sqlalchemy.Column("target_schema", sqlalchemy.String(64), nullable=True),
        sqlalchemy.Column("target_table", sqlalchemy.String(64), nullable=False),
        sqlalchemy.Column(
            "schema_description_format", sqlalchemy.String(64), nullable=False
        ),
        sqlalchemy.Column("schema_description", sqlalchemy.Text(), nullable=False),
        sqlalchemy.UniqueConstraint(
            "namespace",
            "source_table",
            name="UQ__dap_meta__namespace__source_table",
        ),
    )
    return metatable


class _MetatableRecord:
    namespace: str
    table_name: str
    timestamp: datetime
    versioned_schema: VersionedSchema
    metadata: sqlalchemy.MetaData

    @staticmethod
    async def load(
        namespace: str,
        table_name: str,
        db_conn: DatabaseSession,
        metatable_def: sqlalchemy.Table,
    ) -> "_MetatableRecord":
        async with db_conn.context() as conn:
            result = await conn.execute(
                metatable_def.select()
                .where(metatable_def.c.namespace == namespace)
                .where(metatable_def.c.source_table == table_name)
            )
            metatable_record = result.first()

        if metatable_record is None:
            raise NoMetadataError(namespace, table_name)

        schema_description_format: str = metatable_record._mapping[
            "schema_description_format"
        ]
        if schema_description_format != "json":
            raise WrongSchemaDescriptionError(schema_description_format)

        schema_description: JsonType = json.loads(
            metatable_record._mapping["schema_description"]
        )

        schema_version: int = metatable_record._mapping["schema_version"]
        versioned_schema: VersionedSchema = VersionedSchema(
            json_to_object(Schema, schema_description), schema_version
        )

        record = _MetatableRecord(
            namespace, table_name, versioned_schema, metatable_def.metadata
        )
        record.timestamp = metatable_record._mapping["timestamp"]
        return record

    def __init__(
        self,
        namespace: str,
        table_name: str,
        versioned_schema: VersionedSchema,
        metadata: sqlalchemy.MetaData,
    ) -> None:
        self.namespace = namespace
        self.table_name = table_name
        self.versioned_schema = versioned_schema
        self.metadata = metadata


class MetaTableManager:
    _db_connection: DatabaseSession
    _namespace: str
    _table_name: str
    _metatable_def: sqlalchemy.Table

    def __init__(
        self, db_connection: DatabaseSession, namespace: str, table_name: str
    ) -> None:
        self._db_connection = db_connection
        self._namespace = namespace
        self._table_name = table_name
        self._metatable_def = _create_metatable_def(namespace)

    async def last_sync_datetime(self) -> datetime:
        """
        :returns: datetime of last updates on table
        """
        metatable_record = await _MetatableRecord.load(
            self._namespace, self._table_name, self._db_connection, self._metatable_def
        )
        return metatable_record.timestamp.replace(tzinfo=timezone.utc)

    async def initialize(
        self, table_schema: VersionedSchema, table_data: GetTableDataResult
    ) -> None:
        """
        Creates table in database schema and records an entry in it.
        """

        async with self._db_connection.context() as conn:
            await conn.run_sync(lambda c: self._create_tables(c))
            await conn.execute(
                self._metatable_def.insert(),
                [
                    {
                        "namespace": self._namespace,
                        "source_table": self._table_name,
                        "timestamp": table_data.timestamp.astimezone(
                            tz=timezone.utc
                        ).replace(tzinfo=None),
                        "schema_version": table_data.schema_version,
                        "target_schema": self._namespace,
                        "target_table": self._table_name,
                        "schema_description_format": "json",
                        "schema_description": json_dump_string(table_schema.schema),
                    }
                ],
            )

    async def synchronize(
        self, table_schema: VersionedSchema, table_data: GetTableDataResult
    ) -> None:
        """
        Updates related record of meta table with recent table data.
        """

        await self._update_table_schema(table_schema)
        async with self._db_connection.context() as conn:
            await conn.execute(
                (
                    self._metatable_def.update()
                    .where(self._metatable_def.c.namespace == self._namespace)
                    .where(self._metatable_def.c.source_table == self._table_name)
                    .values(
                        timestamp=bindparam("new_timestamp"),
                        schema_version=bindparam("new_schema_version"),
                        schema_description=bindparam("new_schema_description"),
                    )
                ),
                [
                    {
                        "new_timestamp": table_data.timestamp.astimezone(
                            timezone.utc
                        ).replace(tzinfo=None),
                        "new_schema_version": table_data.schema_version,
                        "new_schema_description": json_dump_string(table_schema.schema),
                    }
                ],
            )

            # New enum values must be committed before they can be used.
            # See: https://www.postgresql.org/docs/release/12.0/
            #   "Previously, ALTER TYPE ... ADD VALUE could not be called in a transaction block,
            #    unless it was part of the same transaction that created the enumerated type. Now
            #    it can be called in a later transaction, so long as the new enumerated value is
            #    not referenced until after it is committed."
            await conn.commit()

    async def _update_table_schema(self, table_schema: VersionedSchema) -> None:
        metatable_record = await _MetatableRecord.load(
            self._namespace, self._table_name, self._db_connection, self._metatable_def
        )

        previous_dap_schema: VersionedSchema = metatable_record.versioned_schema
        desired_dap_schema: VersionedSchema = table_schema
        if previous_dap_schema.version == desired_dap_schema.version:
            return

        async with self._db_connection.context() as conn:
            current_table_columns: List[ReflectedColumn] = await conn.run_sync(
                lambda c: self._get_table_columns(c)
            )

            await self._alter_table(
                conn,
                prev_table_def=create_table_definition(
                    self._namespace, self._table_name, previous_dap_schema
                ),
                desired_table_def=create_table_definition(
                    self._namespace, self._table_name, desired_dap_schema
                ),
                current_table_cols=current_table_columns,
            )

    def _get_table_columns(self, db_conn: Connection) -> List[ReflectedColumn]:
        inspector: Inspector = inspect(db_conn)
        return inspector.get_columns(self._table_name, self._namespace)

    async def drop(self) -> None:
        async with self._db_connection.context() as conn:
            await conn.execute(
                self._metatable_def.delete()
                .where(self._metatable_def.c.namespace == self._namespace)
                .where(self._metatable_def.c.source_table == self._table_name)
            )

    def _create_tables(self, db_conn: Connection) -> None:
        inspector: Inspector = inspect(db_conn)
        if self._metatable_def.schema is not None and not inspector.has_schema(
            self._metatable_def.schema
        ):
            db_conn.execute(CreateSchema(self._metatable_def.schema))  # type: ignore

        self._metatable_def.metadata.create_all(db_conn)

    async def _alter_table(
        self,
        db_conn: AsyncConnection,
        prev_table_def: Table,
        desired_table_def: Table,
        current_table_cols: List[ReflectedColumn],
    ) -> None:
        await self._drop_columns(
            db_conn, prev_table_def, desired_table_def, current_table_cols
        )
        await self._add_columns(
            db_conn, prev_table_def, desired_table_def, current_table_cols
        )
        await self._alter_columns(
            db_conn, prev_table_def, desired_table_def, current_table_cols
        )

    async def _drop_columns(
        self,
        db_conn: AsyncConnection,
        prev_table_def: Table,
        desired_table_def: Table,
        current_table_cols: List[ReflectedColumn],
    ) -> None:
        current_cols: Dict[str, ReflectedColumn] = {
            col["name"]: col for col in current_table_cols
        }
        desired_cols: Dict[str, Column] = {
            col.name: col for col in desired_table_def.columns
        }

        for col_name in current_cols:
            if desired_cols.get(col_name) is None:
                await execute_ddl(
                    db_conn,
                    f"ALTER TABLE {table_name(desired_table_def.name, desired_table_def.schema)} DROP COLUMN {column_name(col_name)}",
                )
                await self._drop_type(db_conn, current_cols[col_name]["type"])

    async def _add_columns(
        self,
        db_conn: AsyncConnection,
        prev_table_def: Table,
        desired_table_def: Table,
        current_table_cols: List[ReflectedColumn],
    ) -> None:
        current_cols: Dict[str, ReflectedColumn] = {
            col["name"]: col for col in current_table_cols
        }
        desired_cols: Dict[str, Column] = {
            col.name: col for col in desired_table_def.columns
        }

        for col_name in desired_cols:
            if current_cols.get(col_name) is None:
                col_def: Column = desired_cols[col_name]

                await self._create_type(db_conn, col_def.type)

                if col_def.nullable and not col_def.default:
                    await execute_ddl(
                        db_conn,
                        f"""ALTER TABLE {table_name(desired_table_def.name, desired_table_def.schema)}
                            ADD COLUMN {column_name(col_name)} {col_def.type.compile(db_conn.dialect)}""",
                    )
                elif col_def.nullable and col_def.default:
                    await execute_ddl(
                        db_conn,
                        f"""ALTER TABLE {table_name(desired_table_def.name, desired_table_def.schema)}
                            ADD COLUMN {column_name(col_name)} {col_def.type.compile(db_conn.dialect)}
                            DEFAULT {value_literal(col_def.default.arg)}""",  # type: ignore
                    )
                elif not col_def.nullable and not col_def.default:
                    await execute_ddl(
                        db_conn,
                        f"""ALTER TABLE {table_name(desired_table_def.name, desired_table_def.schema)}
                            ADD COLUMN {column_name(col_name)} {col_def.type.compile(db_conn.dialect)} NOT NULL""",
                    )
                else:
                    await execute_ddl(
                        db_conn,
                        f"""ALTER TABLE {table_name(desired_table_def.name, desired_table_def.schema)}
                            ADD COLUMN {column_name(col_name)} {col_def.type.compile(db_conn.dialect)} NOT NULL
                            DEFAULT {value_literal(col_def.default.arg)}""",  # type: ignore
                    )

    async def _alter_columns(
        self,
        db_conn: AsyncConnection,
        prev_table_def: Table,
        desired_table_def: Table,
        current_table_cols: List[ReflectedColumn],
    ) -> None:
        current_cols = {col["name"]: col for col in current_table_cols}
        desired_cols = {col.name: col for col in desired_table_def.columns}

        altered_cols = {
            col_name: desired_cols[col_name]
            for col_name in (set(desired_cols).intersection(set(current_cols)))
        }

        for col_name, col_def in altered_cols.items():
            await self._alter_type(db_conn, col_def)

    async def _create_type(
        self, db_conn: AsyncConnection, type_def: TypeEngine
    ) -> None:
        col_type = type(type_def)
        if not col_type is sqlalchemy.Enum:
            # Only dealing with enum types
            return

        enum_type_def: sqlalchemy.Enum = type_def  # type: ignore
        if not enum_type_def.name:
            # Only dealing with named enum types
            return

        enum_values = ", ".join(
            map(lambda val: f"{value_literal(val)}", enum_type_def.enums)
        )
        await execute_ddl(
            db_conn,
            f"CREATE TYPE {type_name(enum_type_def.name, enum_type_def.schema)} AS ENUM ({enum_values})",
        )

    async def _drop_type(self, db_conn: AsyncConnection, type_def: TypeEngine) -> None:
        col_type = type(type_def)
        if not col_type is sqlalchemy.Enum:
            # Only dealing with enum types
            return

        enum_type_def: sqlalchemy.Enum = type_def  # type: ignore
        if not enum_type_def.name:
            # Only dealing with named enum types
            return

        await execute_ddl(
            db_conn,
            f"DROP TYPE IF EXISTS {type_name(enum_type_def.name, enum_type_def.schema)}",
        )

    async def _alter_type(self, db_conn: AsyncConnection, col_def: Column) -> None:
        col_type = type(col_def.type)
        if not col_type is sqlalchemy.Enum:
            # Only dealing with enum types
            return

        enum_type_def: sqlalchemy.Enum = col_def.type  # type: ignore
        if not enum_type_def.name:
            # Only dealing with named enum types
            return

        for value in enum_type_def.enums:
            await execute_ddl(
                db_conn,
                f"ALTER TYPE {type_name(enum_type_def.name, enum_type_def.schema)} ADD VALUE IF NOT EXISTS {value_literal(value)}",
            )


class MetadataError(Exception):
    """
    Generic base class for specific meta-table related errors.
    """


class NoMetadataError(MetadataError):
    def __init__(self, namespace: str, table_name: str) -> None:
        super().__init__(
            f"metadata not found for table `{table_name}` in `{namespace}`"
        )


class WrongSchemaDescriptionError(MetadataError):
    def __init__(self, schema_description_format: str) -> None:
        super().__init__(
            f"wrong schema description format; expected: json, got: {schema_description_format}"
        )

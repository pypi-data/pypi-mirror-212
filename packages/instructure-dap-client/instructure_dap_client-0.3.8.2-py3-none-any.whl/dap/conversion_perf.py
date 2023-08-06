from typing import Tuple

from sqlalchemy import Table

from .conversion_common import ConverterDict, get_column_converter


def create_upsert_converters(table_def: Table) -> ConverterDict:
    # create a tuple of converter objects for each column for UPSERT records
    return {col.name: get_column_converter(col) for col in table_def.columns}


def create_delete_converters(table_def: Table) -> ConverterDict:
    # create a tuple of converter objects for each column for DELETE records
    return {col.name: get_column_converter(col) for col in table_def.primary_key}


def create_copy_converters(table_def: Table) -> Tuple:
    return tuple(get_column_converter(col) for col in table_def.columns)

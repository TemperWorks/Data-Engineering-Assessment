#!/usr/bin/env python

import csv
import json
import logging

import sqlalchemy
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.engine import Engine, Connection
from dataclasses import dataclass
from tables import TableObject


@dataclass
class DatabaseObject:
    engine: Engine
    connection: Connection
    metadata: MetaData


def fetch_conn() -> DatabaseObject:
    """
    Fetches Database connection
    """

    engine = sqlalchemy.create_engine(
        "mysql+mysqlconnector://temper_code_test:good_luck@127.0.0.1:3306/temper_code_test")
    connection = engine.connect()
    metadata = sqlalchemy.schema.MetaData(engine)
    return DatabaseObject(engine, connection, metadata)


def create_table_if_not_exists(db: DatabaseObject, table: TableObject):
    """
    Creates a database table if it does not exist
    """
    if not db.engine.dialect.has_table(db.connection, table.name):
        Table(
            table.name,
            db.metadata,
            *table.columns
        ).create()
    return sqlalchemy.schema.Table(table.name, db.metadata, autoload=True, autoload_with=db.engine)


def load_records(db: DatabaseObject, table: Table, csv_file: str, has_header=True, ignore_if_table_exists=True):
    """
    Loads records into a database table
    """
    if ignore_if_table_exists and db.engine.dialect.has_table(db.connection, table.name):
        logging.warning("The created table already exists and data is not inserted.")
        return None
    with open(csv_file) as csv_file:
        reader = csv.reader(csv_file)
        if has_header:
            column_names = next(reader)
        for row in reader:
            row_dict = dict(zip(column_names, row))
            db.connection.execute(table.insert().values(row_dict))
    return None


def return_rows_in_table(db: DatabaseObject, table: Table):
    """
    Return rows in a table.
    """
    for row in db.connection.execute(sqlalchemy.sql.select([table])).fetchall():
        yield {key: value for (key, value) in dict(row).items()}


def convert_row_to_json(row):
    """
    Converts a CSV row into JSON
    """
    return json.dumps(row, separators=(',', ':'), default=str)


def iterator_to_file(iterator_obj, output_file):
    """
    Writes the contents of an iterator object to a file.
    """
    with open(output_file, 'w+') as json_file:
        for row in iterator_obj:
            json_file.write(f"{row}\n")


def read_file(file_path: str):
    """
    Reads a file's contents from its path
    """
    with open(file_path) as f:
        contents = f.read()
    return contents


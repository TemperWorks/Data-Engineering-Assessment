#!/usr/bin/env python

import json
import sqlalchemy
from sqlalchemy.schema import MetaData
from sqlalchemy.engine import Engine, Connection
from dataclasses import dataclass


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


def convert_row_to_json(row):
    """
    Converts a csv row into a valid JSON
    """
    return json.dumps(row, separators=(',', ':'), default=str)


def iterator_to_file(iterator_obj, output_file):
    """
    Write the contents of an iterator object into a file
    """
    with open(output_file, 'w+') as json_file:
        for row in iterator_obj:
            json_file.write(f"{row}\n")


def execute_statement(db: DatabaseObject, sql_statement: str):
    """
    Executes a SQL statement
    """
    return db.engine.execute(
        sql_statement
    )


def combine_results_into_list(iterator_obj):
    """
    Combines the results of an iterator object into a list
    """

    json_out = []
    for item in iterator_obj:
        json_out.append(dict(item))
    yield convert_row_to_json(json_out)


def combine_results_into_separated_jsons(iterator_obj):
    """
    Combines the results of an iterator object into a line separated JSON
    """

    for item in iterator_obj:
        yield convert_row_to_json(dict(item))


def combine_results_into_one_json(iterator_obj):
    """
    Combines the results of an iterator object into one JSON item
    """

    json_out = {}
    for item in iterator_obj:
        json_out = {**json_out, **{item[0]: item[1]}}
    yield convert_row_to_json(json_out)


def read_file(file_path: str):
    """
    Reads a file's contents from its path
    """
    with open(file_path) as f:
        contents = f.read()
    return contents


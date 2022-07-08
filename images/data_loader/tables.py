#!/usr/bin/env python

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Date, VARCHAR
from typing import List
from dataclasses import dataclass


@dataclass
class TableObject:
    name: str
    columns: List[Column]
    source: str


ExampleTable = TableObject(
    name="examples",
    columns=[
        Column('id', Integer, primary_key=True, nullable=False),
        Column('name', VARCHAR(20))
    ],
    source="./data/example.csv"
)

PeopleTable = TableObject(
    name="people",
    columns=[
        Column('id', Integer, primary_key=True, nullable=False),
        Column('given_name', VARCHAR(80)),
        Column('family_name', VARCHAR(200)),
        Column('date_of_birth', Date),
        Column('place_of_birth', VARCHAR(200))
    ],
    source="./data/people.csv"
)

PlacesTable = TableObject(
    name="places",
    columns=[
        Column('id', Integer, primary_key=True, nullable=False),
        Column('city', VARCHAR(200)),
        Column('county', VARCHAR(200)),
        Column('country', VARCHAR(200))
    ],
    source="./data/places.csv"
)

tables_to_create = [
    ExampleTable,
    PeopleTable,
    PlacesTable
]

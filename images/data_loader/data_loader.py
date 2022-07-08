#!/usr/bin/env python

import functions
import tables
import logging

logging.basicConfig(
    filename="./logs/log.txt",
    level=logging.INFO,
    format='%(asctime)s:%(filename)s:%(funcName)s:%(levelname)s :%(message)s'
)
logging.info("Data Loader logging test...")


if __name__ == "__main__":

    DB: functions.DatabaseObject = functions.fetch_conn()
    for table in tables.tables_to_create:
        logging.info(f"Creating table '{table.name}'.")
        db_table = functions.create_table_if_not_exists(
            DB,
            table
        )

        logging.info(f"Loading records into table '{table.name}'.")
        functions.load_records(
            DB,
            db_table,
            table.source
        )

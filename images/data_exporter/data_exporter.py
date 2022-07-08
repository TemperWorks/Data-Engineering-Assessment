#!/usr/bin/env python

import functions
import logging

logging.basicConfig(
    filename="./logs/log.txt",
    level=logging.INFO,
    format='%(asctime)s:%(filename)s:%(funcName)s:%(levelname)s :%(message)s'
)
logging.info("Data Exporter logging test...")


if __name__ == "__main__":

    DB: functions.DatabaseObject = functions.fetch_conn()

    logging.info("Creating country summary table")
    functions.iterator_to_file(
        functions.combine_results_into_one_json(functions.execute_statement(
            DB,
            functions.read_file("sql/get_counts_per_country.sql")
        )),
        "./out/output_counts_per_country.json"
    )

    logging.info("Creating county summary table")
    functions.iterator_to_file(
        functions.combine_results_into_list(functions.execute_statement(
            DB,
            functions.read_file("sql/get_counts_per_county.sql")
        )),
        "./out/output_counts_per_county.json"
    )

    logging.info("Creating city summary table")
    functions.iterator_to_file(
        functions.combine_results_into_separated_jsons(functions.execute_statement(
            DB,
            functions.read_file("sql/get_counts_per_city.sql")
        )),
        "./out/output_counts_per_city.json"
    )

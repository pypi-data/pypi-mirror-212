import os
import sys
import shutil
import logging
import random
import json
from typing import Optional, List, Dict, Tuple
import sqlite3

import typer
from humanfriendly import format_size
from minlog import logger, Verbosity

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

APP_NAME = "sqbased"
app = typer.Typer(
    name=APP_NAME,
    help=f"{APP_NAME}: sqlite database optimization utility",
    no_args_is_help=True,
    context_settings=CONTEXT_SETTINGS,
)


def friendly_size(size):
    return format_size(size, binary=True)


@app.callback()
def app_callback(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Quiet output"),
):
    if verbose:
        logger.be_verbose()
    elif quiet:
        logger.be_quiet()


@app.command("info", help="show detailed information and statistics about a database")
def info(
    db_file: str = typer.Argument(..., help="Database file to use"),
):
    logger.info(f"opening database: {db_file}")

    conn = sqlite3.connect(db_file)

    # get statistics: number of tables, number of rows, size of database, etc.
    logger.info("database info:")

    # db file size
    db_file_size = os.path.getsize(db_file)
    logger.info(f"  file size: {friendly_size(db_file_size)}")

    # info on each table
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        logger.info(f"  table: {table[0]}")

        # show pretty print of schema
        cursor.execute(f"PRAGMA table_info({table[0]});")
        schema = cursor.fetchall()
        logger.info("    schema:")
        for column in schema:
            logger.info(f"      {column[1]}: {column[2]}")

        # row count
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
        row_count = cursor.fetchone()[0]
        logger.info(f"    rows: {row_count}")

        # get the size of just this table using dbstat
        cursor.execute(f"SELECT SUM(pgsize) FROM dbstat WHERE name='{table[0]}';")
        table_size = cursor.fetchone()[0]
        logger.info(f"    size: {friendly_size(table_size)}")


@app.command("vacuum", help="vacuum a database for optimal layout")
def vacuum(
    db_file_in: str = typer.Argument(..., help="Input database file to use"),
    db_file_out: str = typer.Argument(..., help="Output database file to use"),
):
    # copy the input database to the output database if they are different
    if db_file_in != db_file_out:
        logger.info(f"copying database: {db_file_in} -> {db_file_out}")
        shutil.copyfile(db_file_in, db_file_out)

    logger.info(f"opening database: {db_file_out}")
    conn = sqlite3.connect(db_file_out)

    # vacuum the database
    logger.info("vacuuming database")
    conn.execute("VACUUM;")
    conn.commit()


@app.command("autofts5", help="automatically create fts5 indexes on a database")
def autofts5(
    db_file_in: str = typer.Argument(..., help="Input database file to use"),
    db_file_out: str = typer.Argument(..., help="Output database file to use"),
    table_name: str = typer.Argument(..., help="Table to create fts5 index on"),
    fts_columns: str = typer.Option(
        None,
        "--columns",
        "-c",
        help="Columns to create fts5 index on. Defaults to all text columns.",
    ),
    drop_original: bool = typer.Option(
        False,
        "--drop-original",
        help="Drop the original table after creating the fts5 table.",
    ),
):
    if db_file_in != db_file_out:
        logger.info(f"copying database: {db_file_in} -> {db_file_out}")
        shutil.copyfile(db_file_in, db_file_out)

    logger.info(f"opening database: {db_file_out}")
    conn = sqlite3.connect(db_file_out)

    # auto fts5: for the input table
    # we will create <table_name>_fts5 with the specified columns
    # by default we will use all text/VARCHAR columns

    # get the schema for the input table
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    table_schema = cursor.fetchall()

    # ensure the input table exists
    if not table_schema:
        logger.error(f"table does not exist: {table_name}")
        raise typer.Exit(code=1)

    # get the column names for the input table
    table_columns = [column[1] for column in table_schema]

    # get the column types for the input table
    table_column_types = [column[2] for column in table_schema]

    logger.trace(f"opening table: {table_name}")
    logger.trace(f"  schema: {table_schema}")
    logger.trace(f"  columns: {table_columns}")
    logger.trace(f"  column types: {table_column_types}")

    fts_table_name = f"{table_name}_fts5"
    logger.info(
        f"creating fts5 table: {table_name} -> {fts_table_name} on columns: {fts_columns}"
    )

    # get the column names for the fts5 table
    if fts_columns:
        fts_columns = fts_columns.split(",")
        # ensure the specified columns exist
        for column in fts_columns:
            if column not in table_columns:
                logger.error(f"column does not exist: {column}")
                raise typer.Exit(code=1)
    else:
        fts_columns = [
            column
            for column, column_type in zip(table_columns, table_column_types)
            if (column_type == "text" or "VARCHAR" in column_type)
        ]

    logger.info(f"  fts columns: {fts_columns}")

    # create the fts5 table
    fts_columns_str = ", ".join(fts_columns)
    conn.execute(
        f"CREATE VIRTUAL TABLE {fts_table_name} USING fts5({fts_columns_str});"
    )
    conn.commit()

    # insert the data from the input table into the fts5 table
    logger.info(f"coping data from {table_name} -> {fts_table_name}")
    conn.execute(
        f"INSERT INTO {fts_table_name}({fts_columns_str}) SELECT {fts_columns_str} FROM {table_name};"
    )
    conn.commit()

    if drop_original:
        logger.warn(f"dropping original table: {table_name}")
        conn.execute(f"DROP TABLE {table_name};")
        conn.commit()

    # vacuum the database
    logger.info("vacuuming database")
    conn.execute("VACUUM;")
    conn.commit()


@app.command("copytables", help="copy tables from one database to another")
def copytables(
    db_file_in: str = typer.Argument(..., help="Input database file to use"),
    db_file_out: str = typer.Argument(..., help="Output database file to use"),
    tables: List[str] = typer.Argument(..., help="Tables to copy"),
):
    logger.info(f"opening database: {db_file_in}")
    conn_in = sqlite3.connect(db_file_in)
    cursor_in = conn_in.cursor()

    logger.info(f"opening database: {db_file_out}")
    conn_out = sqlite3.connect(db_file_out)
    cursor_out = conn_out.cursor()

    # ensure the input database has the specified tables
    cursor_in.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables_in = [table[0] for table in cursor_in.fetchall()]
    for table in tables:
        if table not in tables_in:
            logger.error(f"table does not exist: {table}")
            raise typer.Exit(code=1)

    # attach the input database to the output database
    logger.info(f"attaching database: {db_file_in} -> {db_file_out}")
    cursor_out.execute(f"ATTACH DATABASE '{db_file_in}' AS db_in;")

    # copy the tables
    logger.info(f"copying tables from {db_file_in} -> {db_file_out}")
    for table in tables:
        logger.info(f"  copying table: {table}")
        # get the schema for the input table
        cursor_in.execute(f"PRAGMA table_info({table});")
        table_schema = cursor_in.fetchall()
        logger.trace(f"    schema: {table_schema}")

        # create the output table
        table_schema_str = ", ".join(
            [f"{column[1]} {column[2]}" for column in table_schema]
        )
        cursor_out.execute(f"CREATE TABLE {table}({table_schema_str});")

        # copy all rows
        cursor_out.execute(f"INSERT INTO {table} SELECT * FROM db_in.{table};")

    conn_out.commit()


def main():
    app()


if __name__ == "__main__":
    main()

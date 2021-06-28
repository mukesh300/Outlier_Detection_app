import sqlite3
from sqlite3 import Error
import os
import yaml

CWD = os.path.dirname(os.path.abspath(__file__))
config_path = f"{CWD}//params.yaml"


def read_params(conf_path=config_path):
    with open(conf_path) as yaml_file:
        cfg = yaml.safe_load(yaml_file)
    return cfg


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def create_tables(conn, schema_path):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        cursor = conn.cursor()
        with open(schema_path, 'r') as sql_file:
            sql_as_string = sql_file.read()
            cursor.executescript(sql_as_string)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    config = read_params()
    db_path = CWD + config["DB"]["sqlite"]
    schema_path = CWD + config["DB"]["schema"]
    conn = create_connection(db_path)
    create_tables(conn, schema_path)

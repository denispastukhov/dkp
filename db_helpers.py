from loguru import logger
import psycopg2
from psycopg2.extras import DictCursor




class Database:
    """PostgreSQL Database class."""

    def __init__(self ): #config):
        self.host = 'localhost' #config.DATABASE_HOST
        #self.username = config.DATABASE_USERNAME
        #self.password = config.DATABASE_PASSWORD
        #self.port = config.DATABASE_PORT
        self.dbname = 'dkp' #config.DATABASE_NAME
        self.conn = None

    def connect(self):
        """Connect to a Postgres database."""
        LOGGER = logger
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    #user=self.username,
                    #password=self.password,
                    #port=self.port,
                    dbname=self.dbname
                )
            except psycopg2.DatabaseError as e:
                LOGGER.error(e)
                raise e
            finally:
                LOGGER.info('Connection opened successfully.')
    
    def select_rows_dict_cursor(self, query, *params):
        """Run SELECT query and return dictionaries."""
        self.connect()
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, (*params,))
            records = cur.fetchall()
        cur.close()
        return records

    def select_column_headers(self, table):
        self.connect()
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(f"Select * FROM {table} LIMIT 0")
            colnames = [desc[0] for desc in cur.description]
        return colnames

    def select_one_row_dict_cursor(self, query, *params):
        """Run SELECT query and return dictionaries."""
        self.connect()
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(query, (*params,))
            records = cur.fetchone()
        cur.close()
        return records

    def update_rows(self, query, *params):
        """Run a SQL query to update rows in table."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query, (*params,))
            self.conn.commit()
            cur.close()
            return f"{cur.rowcount} rows affected."
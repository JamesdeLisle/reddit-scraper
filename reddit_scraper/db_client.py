import sys
import logging
import psycopg2

from os import environ

from typing import List

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.errors import DuplicateDatabase
from psycopg2.errors import UniqueViolation 
from psycopg2.extras import execute_values
 
from .error import EnvironmentVariableNotSet
from .record import Record

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)


try:
    DATABASE_NAME = environ['POSTGRES_DB']
except KeyError:
    raise EnvironmentVariableNotSet(f"Environment variable POSTGRES_DB not set.")


try:
    RESET_DB = environ['RESET_DB']
except KeyError:
    raise EnvironmentVariableNotSet(f"Environment variable RESET_DB not set.")


class PostgresClient:
    def __init__(self):
        self.connection = psycopg2.connect()
        try:
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = self.connection.cursor()
            cur.execute(f"CREATE DATABASE {DATABASE_NAME}")
        except DuplicateDatabase:
            logger.info(f"DATABASE {DATABASE_NAME} already exists")
        finally:
            cur.close()
            self.connection.close()
        self.connection = psycopg2.connect(database=DATABASE_NAME)
        self.create_tables()

    
    def create_tables(self):
        logger.info("Creating tables...")
        cur = self.connection.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                username VARCHAR(128),
                subreddit VARCHAR(128),
                is_submitter BOOLEAN,
                created_at BIGINT,
                score BIGINT,
                guilded BOOLEAN,
                body TEXT,
                body_sha1 VARCHAR(160),
                post_url VARCHAR(540),
                PRIMARY KEY (username, subreddit, created_at, body_sha1)
            )
        """)
        cur.close()
        self.connection.commit()
    
    def insert_records(self, records: List[Record]):
        cur = self.connection.cursor()
        for record in records:
            try:
                cur.execute(
                    """INSERT INTO posts (
                            username,
                            subreddit,
                            is_submitter,
                            created_at,
                            score,
                            guilded,
                            body,
                            body_sha1,
                            post_url
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    record.post
                ) 
                self.connection.commit()
            except UniqueViolation:
                self.connection.rollback()
                logger.info(f"Duplicate record encountered: {record.author} | {record.subreddit} | {record.created_utc} | {record.body_sha1}")
        cur.close()
        

if __name__ == '__main__':
    pc = PostgresClient()

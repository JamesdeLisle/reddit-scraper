import sys
import logging
import json
from os import environ

from pmaw import PushshiftAPI
from pydantic import ValidationError 

from psycopg2 import OperationalError

from .db_client import PostgresClient
from .record import Record
from .error import DatabaseConnectionError


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class Scraper:

    def __init__(self, ):
        self.api = PushshiftAPI()
        logger.info("Connecting to database")
        try:
            self.db_client = PostgresClient()
        except OperationalError:
            logger.error("""
            Cannot connect to the postgres database.
            Ensure that the following environment variables have been set

                PGHOST
                PGPORT
                PGUSER
                PGPASSWORD
        """)
            raise DatabaseConnectionError
        pass
    
    def scrape(self, query: str, window: int):
        logger.info(f"Scraping reddit for posts containing [{query}] in the last [{window}] days.")
        comments = self.api.search_comments(
            q=query, 
            search_window=window,
            mem_safe=True,
            cache_dir='/cache',
            safe_exit=True
        )
        records = []
        for comment in comments:
            try:
                records.append(Record(**comment))
            except ValidationError as e:
                logger.info("Invalid record received.")
        
        logger.info(f"Found {len(records)} comments")

        self.db_client.insert_records(records)

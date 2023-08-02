import pyodbc
import os
from dotenv import load_dotenv
from scrapy.exceptions import NotConfigured

load_dotenv()

class AzureSqlPipeline:
    def __init__(self) -> None:
        try:
            self.server = os.getenv('AZURE_SERVER_HOST')
            self.database = os.getenv('AZURE_DB_NAME')
            self.username = os.getenv('AZURE_SERVER_USER')
            self.password = os.getenv('AZURE_SERVER_PASSWORD')

            self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+self.server +
                                       ';DATABASE='+self.database+';ENCRYPT=yes;UID='+self.username+';PWD=' + self.password)
            self.cursor = self.cnxn.cursor()

            self.cursor.execute("""
            DROP TABLE IF EXISTS main_upcoming_movies;

            CREATE TABLE main_upcoming_movies(
                id INT NOT NULL IDENTITY(1,1),
                title VARCHAR(255),
                release_date DATE,
                genres VARCHAR(255),
                director VARCHAR(255),
                cast VARCHAR(255),
                duration VARCHAR(255),
                views INTEGER,
                nationality VARCHAR(255),
                distributor VARCHAR(255),
                prediction FLOAT,
                PRIMARY KEY (id)
                )
            """)
            self.cnxn.commit()

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def process_item(self, item, spider):
        try:
            # Define insert statement
            self.cursor.execute(""" INSERT INTO main_upcoming_movies (
                title,
                release_date,
                genres,
                director,
                cast,
                duration,
                views,
                nationality,
                distributor,
                prediction
            ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                item["title"],
                item["release_date"],
                item["genres"],
                item["director"],
                item["cast"],
                item["duration"],
                item["views"],
                item["nationality"],
                item["distributor"],
                0.0
            ))

            # Execute insert of data into database
            self.cnxn.commit()

        except Exception as e:
            print(f"An error occurred when inserting data: {str(e)}")
        return item

    def close_spider(self, spider):
        try:
            # Close cursor & connection to database
            self.cursor.close()
            self.cnxn.close()

        except Exception as e:
            print(f"An error occurred when closing the connection: {str(e)}")
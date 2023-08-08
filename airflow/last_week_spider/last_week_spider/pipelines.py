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
            CREATE TABLE IF NOT EXISTS main_last_week_movies(
                id INT NOT NULL AUTO_INCREMENT,
                title VARCHAR(255),
                week VARCHAR(255),
                entrance INTEGER,
                country VARCHAR(255),
                PRIMARY KEY (id)
                )
            """)
            self.cnxn.commit()
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def process_item(self, item, spider):
        try:
            # Define insert statement
            self.cursor.execute(""" INSERT INTO main_last_week_movies (
                title,
                week,
                entrance,
                country
            ) values (?, ?, ?, ?)""", (
                item["title"],
                item["week"],
                item["entrance"],
                item["country"],
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
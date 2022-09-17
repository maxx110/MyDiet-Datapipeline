from ast import Return
from distutils.log import error
from io import StringIO
import psycopg2
import pymysql
from sqlalchemy import create_engine
import psycopg2.extras as extras


class Migration:
    def __init__(self):
        self.host = 'Localhost'
        self.port = '5432'
        self.user = 'postgres'
        self.passwd = 'xxxx'
        self.database = 'postgres'
        self.conn = psycopg2.connect(
            host=self.host, dbname=self.database, user=self.user, password=self.passwd, port=self.port)
        self.conn_string = "postgresql://postgres:xxxx@Localhost/postgres"

    def est_conn(self, data_frame):
        """
        loads data_frame into the postgres databse
        """
        try:
            db = create_engine(self.conn_string)
            conn = db.connect()
            conn1 = psycopg2.connect(
                database="postgres",
                user='postgres',
                password='xxxx',
                host='Localhost',
                port='5432'
            )
            conn1.autocommit = True
            cur = conn1.cursor()
            # converting data to sql
            data_frame.to_sql('mydiett_information', conn,
                              if_exists='replace', index=False)
            conn1.close()
        except:
            print('data not loaded to postgress')

    def create_schema(self):
        """
        creates a schema for the database
        """
        try:
            cur = self.conn.cursor()
            query = 'CREATE SCHEMA IF NOT EXISTS mydiett'
            #params = ('mydiett','postgres')
            cur.execute(query)
            self.conn.commit()
        except:
            print('schema not created')

    def create_table(self):
        """
        creates a table for the database if it exists
        """
        cur = self.conn.cursor()
        try:
            create_table_command = """
                        CREATE TABLE IF NOT EXISTS mydiett.mydiett_information(
                            Unique_Id VARCHAR(255) PRIMARY KEY,
                            Product_Id INT NOT NULL,
                            Product_Name VARCHAR(100),
                            Product_Price VARCHAR(255),
                            Product_Link VARCHAR(255),
                            Product_img VARCHAR(255),
                            Product_description VARCHAR(255)
                        )
            """
            cur.execute(create_table_command)
            self.conn.commit()
            # cur.close()

        except:
            print('table not created successfully')

    def query_schema(self):
        cur = self.conn.cursor()
        query = 'select * from my_diet_info'
        cur.execute(query)
        #result = cur.fetchall()

    def con_database(self):
        """
        establishes a connecction to the database
        """
        try:
            cur = self.conn.cursor()
            self.conn.commit()

        except Exception as error:
            print('not connected to database')

    def insert_into_database_noduplicate(self, Unique_Id, Product_Id, Product_Name, Product_Price, Product_Link, Product_img, Product_description):
        db = create_engine(self.conn_string)
        conn = db.connect()
        conn1 = psycopg2.connect(
            database="postgres",
            user='postgres',
            password='xxxx',
            host='Localhost',
            port='5432'

        )
        conn1.autocommit = True
        cur = conn1.cursor()
        cur.execute(
            # "SELECT \"Product_Id\" FROM mydiett.mydiett_information WHERE \"Product_Id\"=%s", [Product_Id])
            "SELECT 'Product_Id' FROM mydiett.mydiett_information WHERE 'Product_Id'=%s", [Product_Id])

        result = cur.fetchall()
        if result:
            print('Record already exist')
            # Record already exists
            # Do something that tells the user that email/user handle already exists

        else:
            cur.execute('INSERT INTO mydiett.mydiett_information ("unique_id","product_id", "product_name","product_price", "product_link", "product_img","product_description") VALUES (%s, %s, %s, %s, %s, %s, %s)', [
                        Unique_Id,Product_Id, Product_Name, Product_Price, Product_Link, Product_img ,Product_description])
            conn1.commit()
        cur.close()
        conn1.close()


conne = Migration()
conne.create_schema()
conne.create_table()

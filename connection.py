from ast import Return
from distutils.log import error
import psycopg2
import pymysql
from sqlalchemy import create_engine
import psycopg2.extras as extras


class Migration:
    def __init__(self):
        self.host = 'Localhost'
        self.port = 5432
        self.user = 'postgres'
        self.passwd = '@Job7mupps5'
        self.database = 'postgres'
        self.conn = psycopg2.connect(host=self.host, dbname=self.database, user=self.user, password=self.passwd, port=self.port)

    @staticmethod
    def insert_df(df,table='mydiett_information'):
        host = 'Localhost'
        port = 5432
        user = 'postgres'
        passwd = '@Job7mupps5'
        database = 'postgres'
        conn = psycopg2.connect(host=host, dbname=database, user=user, password=passwd, port=port)

        if len(df)>0:
            
            df_columns = list(df)
            #create (col1,col2...)
            columns = ','.join(df_columns)
            #create values per column
            values = 'VALUES({})'.format(','.join(['%s' for _ in df_columns]))
            #create insert into table column and values
            insert_statement = 'INSERT INTO {} ({}) {}'.format(table,columns,values)
            cur = conn.cursor()
            #cur.execute('truncate' + table + ';') #avoids duplicate           
            psycopg2.extras.execute_batch(cur,insert_statement,df.values)
            conn.commit()

    # def get_dataframe(self):
    #     dataframe = scrapper.data_frame
    #     print(dataframe)
    
    def print_inf(self,z,u):
        return print(z+u)

    def create_schema(self):
        cur = self.conn.cursor()
        query ='CREATE SCHEMA IF NOT EXISTS mydiett'
        #params = ('mydiett','postgres')
        cur.execute(query)
        #self.conn.commit()
    
    
    def create_table(self):
        cur =self.conn.cursor()
        try:
            create_table_command = """
                        CREATE TABLE IF NOT EXISTS mydiett.mydiett_information(
                            Unique_Id VARCHAR(255) PRIMARY KEY,
                            Product_Id INT NOT NULL,
                            Product_Name VARCHAR(100),
                            Product_Price INT,
                            Product_Link VARCHAR(255),
                            Product_img VARCHAR(255),
                            Product_description VARCHAR(255)
                        )
            """
            cur.execute(create_table_command)
            
        except:
            print('table not created successfully')
    

    def query_schema(self):
        cur =self.conn.cursor()
        query ='select * from my_diet_info'
        cur.execute(query)
        #result = cur.fetchall()
        


    def con_database(self):
        # self.conn = None
        # #cur = None
        try:
            cur = self.conn.cursor()
            self.create_schema()
            self.create_table()
            
            self.conn.commit()
            cur.close()
            #self.conn.close()
        except Exception as error:
            print(error)
        finally:
            # if cur is not None:
            #     cur.close()
            if self.conn is not None:
                self.conn.close()
        

conne= Migration()
conne.con_database()
    
    


import sqlalchemy
import pandas as pd


class DB:
   
    engine = sqlalchemy.create_engine('sqlite:///mydatabase.db')
    @staticmethod
    def pushDb(df):
        df.to_sql(name="mytable", con=DB.engine, if_exists='replace',index=False) 

    @staticmethod
    def execDB(sqlString):
        with DB.engine.connect() as conn:
            result = conn.execute(sqlalchemy.text(sqlString))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return df  
    
    @staticmethod
    def getColsDB():
        ''' Get Col names from table (assume single table)'''
        retString=None
        inspector = sqlalchemy.inspect(DB.engine)
        table_names = inspector.get_table_names()
        print(f'table_names:/t{table_names}')
        assert(len(table_names)==1)
        table_name=table_names[0]
        retString=f"Table = {table_name}, "
        columns = inspector.get_columns(table_name)
        retString+=f"Columns = ["
        for col in columns:
            retString+=f"{col['name']} {col['type']}, "
        retString+="]"
        return retString
    
    @staticmethod
    def read_data_from_database():
    # Establish a connection
        with DB.engine.connect() as connection:
            # Execute a SQL query and retrieve data
            query = sqlalchemy.text("SELECT * FROM mytable")
            result = connection.execute(query)

            # Convert the result to a Pandas DataFrame
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
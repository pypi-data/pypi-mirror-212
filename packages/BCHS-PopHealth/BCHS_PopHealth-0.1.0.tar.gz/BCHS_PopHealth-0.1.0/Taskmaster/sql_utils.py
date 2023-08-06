import pandas
from sqlalchemy.sql import text
import sqlparams

def run_sql_script(sqlfile, engine, parameters={}):
    # connection = pyodbc.connect('DRIVER={{SQL Server}};SERVER={};DATABASE={}'.format(IP_ADDRESS, DATABASE))
    dataframes = []

    connection = engine.raw_connection()
    connection.timeout = 60 * 5
    try:
        with open(sqlfile, encoding='utf-8-sig') as f:
            query = f.read()
        
        cursor = connection.cursor()

        if engine.name == "mssql":
            fmt = sqlparams.SQLParams('pyformat', 'qmark')
            query, parameters = fmt.format(query, parameters)
            cursor.execute(query, parameters)

            while True:
                results = cursor.fetchall()
                for i, result in enumerate(results):
                    results[i] = [value for value in results[i]]
                
                headers = [col[0] for col in cursor.description]
                df = pandas.DataFrame(data=results, columns=headers)

                dataframes.append(df)
                
                if not cursor.nextset():
                    break
        
        cursor.close()

    finally:
        connection.close()


    return dataframes
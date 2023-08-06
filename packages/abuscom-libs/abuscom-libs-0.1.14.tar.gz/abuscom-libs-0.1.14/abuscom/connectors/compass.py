from airflow.providers.jdbc.hooks.jdbc import JdbcHook
import datetime

#from java.sql import Timestamp

class Compass:

    def __init__(self, compass_conn_id):
        self.__compass_conn_id = compass_conn_id

    def __dataFrameToTuples(self, df, columns):
        tuples= []
        for i, row in df.iterrows():
            tuple = ()

            for idx, column in enumerate(columns):
                try:
                    timestamp = row[idx].getTime() / 1000
                    tuple = tuple + (datetime.datetime.fromtimestamp(timestamp).astimezone().isoformat(),)
                except AttributeError:
                    tuple = tuple + (row[idx],)
            tuples.append(tuple)

        return tuples


    def load_to_dataframe(self, tableName, columns, schema, where=[]):
        cpHook = JdbcHook(log_sql=True, jdbc_conn_id=self.__compass_conn_id)
        strColumns = ",".join('"' + columnName.upper() + '"' for columnName in columns)

        if len(where) > 0:
            whereConditions = map(lambda cond: '"' + cond['column'].upper() + '"' + ' ' + cond['symbol'] + ' ' + cond['value'], where)
            whereCondition = f'where {" and ".join(list(whereConditions))}'
        else:
            whereCondition = ""

        sql = f'select {strColumns} from {schema}.{tableName} {whereCondition}'

        print(sql)
        db = cpHook.get_pandas_df(sql=sql)
        # print(db)
        return db

    def load_to_tuples(self, tableName, columns, schema, where=[]):
        df = self.load_to_dataframe(tableName=tableName, columns=columns, schema=schema, where=where)
        tuples = self.__dataFrameToTuples(df=df, columns=columns)
        # print(tuples)
        return tuples
        # return list(df.itertuples(index=False, name=None))
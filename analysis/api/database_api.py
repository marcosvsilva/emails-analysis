from asyncio import new_event_loop
from re import X
import pymssql
import os
import time

from api.gmail_api import (Message)


class Connection:

    def __init__(self):
        try:
            server = os.getenv("SQL_SERVER", "127.0.0.1")
            port = os.getenv("SQL_PORT", "")
            database = os.getenv("SQL_DATABASE", "Master")
            user = os.getenv("SQL_USER", "sa")
            password = os.getenv("SQL_PASSWORD", "")

            self._max_insert = int(os.getenv("SQL_MAX_INSERT", 50))
            self._time_sleep = int(os.getenv("SQL_FAIL_TIME_SLEEP", 50))

            if port != '':
                self.__connection = pymssql.connect(host=server,
                                                    port=port,
                                                    database=database,
                                                    user=user,
                                                    password=password)
            else:
                self.__connection = pymssql.connect(host=server,
                                                    database=database,
                                                    user=user,
                                                    password=password)

        except pymssql.Error as fail:
            raise Exception('exception connection, fail : {}'.format(fail))

    def insert_information(self, informations):
        if not len(informations) > 0:
            exit

        sql_insert = '''
        INSERT INTO EMISSAO_DFE
        (EMDF_SISTEMA, EMDF_MODELO, EMDF_DATA_EMISSAO, EMDF_NUMERO,
        EMDF_SERIE, EMDF_CNPJ,EMDF_RAZAO_SOCIAL, EMDF_FANTASIA, EMDF_ENDERECO,
        EMDF_BAIRRO, EMDF_MUNICIPIO)
        VALUES(%s, %s, CONVERT(DATETIME, %s, 103),
        %d, %s, %s, %s, %s, %s, %s, %s)
        '''

        list_inserts = []
        for inf in informations:
            new_insert = [value for tag, value in dict(inf)['description'].items()]
            list_inserts.append(tuple(new_insert))

        self.sql_insert(sql_insert, list_inserts)

    def sql_query(self, sql_query, table_columns):
        try:
            cursor = self.__connection.cursor()
            cursor.execute(sql_query)
            row = cursor.fetchone()
            response = []
            while row:
                row_json = {}
                index_column = 0
                for column in table_columns:
                    row_json.update({column: row[index_column]})
                    index_column += 1
                response.append(row_json)
                row = cursor.fetchone()

            return response
        except Exception as fail:
            raise Exception('exception get sql, fail: {}'.format(fail))

    def sql_update(self, sql_update, list_update):
        self.sql_execut_emany(sql_update, list_update)

    def sql_insert(self, sql_insert, list_inserts):
        n = int(len(list_inserts) / self._max_insert) + 1
        init = 0

        for i in range(n):
            list_ins_part = list_inserts[init: init+self._max_insert]
            print(list_ins_part)
            self.sql_execut_emany(sql_insert, list_ins_part)

    def sql_execut_emany(self, sql_script, list_exec, n_errors=0):
        try:
            cursor = self.__connection.cursor()
            cursor.executemany(sql_script, list_exec)
            self.__connection.commit()
        except Exception as fail:
            if n_errors < 5:
                print('exception insert fail: {}; Try again soon!'.format(fail))
                time.sleep(self._time_sleep)
                self.sql_execut_emany(sql_script, list_exec, n_errors+1)
            else:
                self.__connection.rollback()
                raise Exception('exception update sql {}, fail: {}'.format(
                    sql_script, fail), True)


    def sql_execute(self, sql_script):
        try:
            cursor = self.__connection.cursor()
            cursor.execute(sql_script)
            self.__connection.commit()
        except Exception as fail:
            self.__connection.rollback()
            raise Exception('exception update sql {}, fail: {}'.format(
                sql_script, fail), True)

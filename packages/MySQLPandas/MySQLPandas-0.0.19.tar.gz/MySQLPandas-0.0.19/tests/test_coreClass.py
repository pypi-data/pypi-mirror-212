import pytest
import sys
import pandas as pd

sys.path.append("/home/nakashima/Lab/code/pandas_mysql")

from MySQLPandas.core import MySQLPandas
from MySQLPandas.lib.ErrorClass import PandasMySQLError
test_file_path = "/home/nakashima/Lab/2023_2_27/AESPA/dataframe.csv"
dammy_path = "dammy"

def test_TrueConstract(capfd):
    with MySQLPandas("nakashima","nakashima_db",initfile_path="docs/password.ini") as obj:
        obj.isConnectDB()
        out,err = capfd.readouterr()
        assert out == "Connected to the database\n"
        assert err == ""


def FalseConstract():
    PandasMySQL_obj = MySQLPandas("nakashma","nakashima_db",initfile_path="docs/password.ini")

def test_RaiseConectionError():
    with pytest.raises(PandasMySQLError):
        FalseConstract()

def test_raiseAlreadyExistTable():
    with pytest.raises(PandasMySQLError):
        with MySQLPandas("nakashima","nakashima_db",initfile_path="docs/password.ini") as obj:
            obj.makeTable(df_path=test_file_path,table_name="RNAcentral_bed")

def test_ExecutecatchCommand():
    with MySQLPandas("nakashima","nakashima_db",initfile_path="docs/password.ini") as obj:
        obj.showTableList()


def test_makeTable_from_csv():
    with MySQLPandas("nakashima","nakashima_db",initfile_path="docs/password.ini") as obj:
        obj.makeTable(df_path=test_file_path,table_name="test_table")
        obj.addPrimaryKey(table_name="test_table",primary_key="Run")
        obj.deletePrimaryKey(table_name="test_table")
        assert obj.isNullTableNameinTableList("test_table") == True
        obj.deleteTable("test_table")
        assert obj.isNullTableNameinTableList("test_table") == False

def test_makeTable_from_obj():
    with MySQLPandas("nakashima","nakashima_db",initfile_path="docs/password.ini") as obj:
        df =  pd.read_csv(test_file_path)
        obj.makeTable(df=df,table_name="test_table")
        obj.addPrimaryKey(table_name="test_table",primary_key="Run")
        assert obj.isNullTableNameinTableList("test_table") == True
        obj.deleteTable("test_table")
        assert obj.isNullTableNameinTableList("test_table") == False



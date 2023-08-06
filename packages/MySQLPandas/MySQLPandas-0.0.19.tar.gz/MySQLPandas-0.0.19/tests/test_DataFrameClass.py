import pytest
import sys
import pandas as pd

sys.path.append("/home/nakashima/Lab/code/pandas_mysql")

from MySQLPandas.lib.DataFrameClass import DataframeProcessing,ImportDataFrame,TwoDataframesProcessing
from MySQLPandas.lib.ErrorClass import PandasMySQLError,PandasMySQLError_dev

test_file_path = "/home/nakashima/Lab/2023_2_27/AESPA/single/Homo_sapiens/result/tsv/SRR649360.tsv"
dammy_path = "dammy"

@pytest.fixture
def DataFrameObject_from_obj():
    df = pd.read_csv(test_file_path,sep="\t",converters={2:str})
    pandas_mysql_obj = DataframeProcessing(table_name = "",df=df)
    return pandas_mysql_obj

@pytest.fixture
def DataFrameObject_from_csv():
    pandas_mysql_obj = DataframeProcessing(table_name = "",df_path=test_file_path,sep="\t",converters={2:str})
    return pandas_mysql_obj

def test_ImportDataFrameMethod():
    df_from_csv = ImportDataFrame(df_path=test_file_path,sep="\t",converters={2:str})
    assert type(df_from_csv) == pd.DataFrame
    df = pd.read_csv(test_file_path,sep="\t",converters={2:str})
    df_from_object = ImportDataFrame(df)
    assert type(df_from_object) == pd.DataFrame

def RaiseImportDataFrameMethodError():
    df = ImportDataFrame()

def test_RaiseImportDataFrameMethodError():
    with pytest.raises(PandasMySQLError):
        RaiseImportDataFrameMethodError()

def test_DataFrame_from_object(DataFrameObject_from_obj):
    assert DataFrameObject_from_obj.df_for_command == None
    assert DataFrameObject_from_obj.sql_command == None
    assert type(DataFrameObject_from_obj.df) == pd.DataFrame
    
def test_DataFrame_from_pcsv(DataFrameObject_from_csv):
    assert DataFrameObject_from_csv.df_for_command == None
    assert DataFrameObject_from_csv.sql_command == None
    assert type(DataFrameObject_from_csv.df) == pd.DataFrame

def RaiseDammyPathError():
    pandas_mysql_obj = DataframeProcessing(table_name = None,df_path=dammy_path)

def test_RaiseDammyPathError():
    with pytest.raises(PandasMySQLError):
        RaiseDammyPathError()

def test_makeDBFrame(DataFrameObject_from_obj):
    DataFrameObject_from_obj.makeDBFrame()
    assert type(DataFrameObject_from_obj.df_for_command) == pd.DataFrame

def test_makeSQLcommand(DataFrameObject_from_obj):
    DataFrameObject_from_obj.makeDBFrame()
    DataFrameObject_from_obj.makeTableSQLcommand()
    assert type(DataFrameObject_from_obj.sql_command) == str

@pytest.fixture
def df_continue():
    class df_EqualObject():
        df1 = pd.DataFrame(
            {0: [25, 12, 15, 14],1: [5, 7, 13, 12],2: [5, 7, 13, 12]}
            )
        df2 = pd.DataFrame(
            {0: [25, 12, 15, 14],1: [5, 7, 13, 12],2: [5, 7, 13, 12]}
            )
    return df_EqualObject

@pytest.fixture
def df_failed():
    class df_EqualObject():
        df1 = pd.DataFrame(
            {0: [25, 12, 15, 14],1: [5, 7, 13, 12],2: [5, 7, 13, 12]}
            )
        df2 = pd.DataFrame(
            {0: [5, 12, 15, 14],1: [5, 7, 13, 12],2: [5, 7, 13, 12]}
            )
    return df_EqualObject

@pytest.fixture
def df_modify_continue():
    class df_EqualObject():
        df1 = pd.DataFrame(
            {0: [25, 12, 15, 14],1: [5, 7, 13, 12],2: [5, 7, 13, 12]}
            )
        df2 = pd.DataFrame(
            {0: [25, 12, 15, 14],1: [5, 7, 13, 12],2: [5, 7, 13, 11]}
            )
    return df_EqualObject

@pytest.fixture
def df_modify_modify():
    class df_EqualObject():
        df1 = pd.DataFrame(
            {0: [25, 12, 15, 14],1: [5, 7, 13, 12],2: [5, 7, 13, 12]}
            )
        df2 = pd.DataFrame(
            {0: [25, 12, 15, 14],1: [5, 7, 13, 12],2: [5, 7, 13, 15]}
            )
    return df_EqualObject

def test_isContinueDataFrame(df_continue):
    dfs_obj = TwoDataframesProcessing(df_continue.df1,df_continue.df2)
    status_message = dfs_obj.isEqualDataFrames()
    assert status_message == "continue"

def test_isModifyDataFrame_continue(df_modify_continue):
    dfs_obj = TwoDataframesProcessing(df_modify_continue.df1,df_modify_continue.df2)
    status_message = dfs_obj.isEqualDataFrames(Strict_Mode=False)
    assert status_message == "continue"

def test_isModifyDataFrame_modify(df_modify_modify):
    dfs_obj = TwoDataframesProcessing(df_modify_modify.df1,df_modify_modify.df2)
    status_message = dfs_obj.isEqualDataFrames(Strict_Mode=False)
    assert status_message == "modify"

def test_isFailedDataFrame(df_failed):
    dfs_obj = TwoDataframesProcessing(df_failed.df1,df_failed.df2)
    status_message = dfs_obj.isEqualDataFrames()
    assert status_message == "failed"
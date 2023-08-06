import pandas as pd
import getpass
import os
import sys
import time
from tqdm import tqdm
from configparser import ConfigParser
from mysql.connector import MySQLConnection
from typing import Optional

from MySQLPandas.lib.DataFrameClass import DataframeProcessing,TwoDataframesProcessing
from MySQLPandas.lib.ErrorClass import PandasMySQLError
#mysql-python-connector=8.0.29


class MySQLPandas(MySQLConnection):
    def __init__(
            self,user:str,
            db_name:str,
            host:str = 'localhost',
            port:str = '3306',
            initfile_path:str = ''
            ) -> None:
        """
        Generate connector object

        Parameters
        ----------
        user : str
        db_name : str
        host : str, default '3306'
        initfile_path : str, default ''
            Specify password file.  
            If you don't do it, you're required password from console.

        Returns
        ----------
        None

        Raises
        ----------
        PandasMySQLError
            When you input wrong DB info.
        """
        super().__init__()
        self.DBList:list = []
        self.table_name:Optional[str] = None
        self.table_info:Optional[pd.DataFrame] = None

        #enter user info
        InitFile_path = initfile_path #specify password file (change before useing)
        if os.path.isfile(InitFile_path):
            config = ConfigParser()
            config.read(InitFile_path)
            password = config.get("development","password")
        else:
            try:
                password = getpass.getpass("enter password(hidden):")
            except KeyboardInterrupt:
                sys.exit(1)

        DB_config = {
            'user' : user,
            'port' : port,
            'password' : password,
            'host' : host,
            'database' : db_name
        } # convert dict
        self.__db_config = DB_config #private val
        #catch exception
        try:
            super().connect(**self.__db_config)
            super().ping(True)
        except Exception as error:
            raise PandasMySQLError(error)
    
    def __enter__(self):
        try:
            super().connect(**self.__db_config)
            super().ping(True)
        except Exception as e:
            raise PandasMySQLError(e)
        return super().__enter__()

    def isConnectDB(self) -> None:
        """
        Return whether object is connecting DB or Not

        parameters
        ----------
        None

        Returns
        ----------
        If it connects, it outputs "Connected to the database" 

        Raises
        ----------
        PandasMySQLError
            When it disconnects DB.
        """
        con = self
        if con.is_connected():
            print("Connected to the database")
        else:
            raise PandasMySQLError("something went wrong.")
        self.__catchwaringshow()

    def showTableList(self) -> None:
        """
        Display exist table name list.  

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        self.__catchTableList()
        for DBname in self.DBList:
            print(DBname)
        self.__catchwaringshow()
        
    
    def showTableinfo(self,table_name:str) -> None:
        """
        Display table column definition.

        Parameters
        ----------
        table_name:str

        Returns
        ----------
        None

        Raises
        ----------
        PandasMySQLError
            Input not existing table name.
        """
        self.__catchTableInfo(table_name=table_name)
        print(self.table_info)
        self.__catchwaringshow()
    
    def deleteTable(self,table_name:str) -> None:
        """
        Delete Table.

        Parameters
        ----------
        table_name:str

        Returns
        ----------
        None

        Raises
        ----------
        PandasMySQLError
            Input not existing table name.
        """        
        con = self
        cursor = con.cursor()
        cursor.execute(f"drop table {table_name};")
        self.__catchwaringshow()

    def makeTable(
            self,
            table_name: str,
            df_path: Optional[str] = None,
            df:Optional[pd.DataFrame] = None,
            converters:Optional[dict] = None,
            sep:str = ","
            ) -> None:
        """
        Make table frame from DataFrame object or csv,tsv file.  
        If a same table name exists, it raises Error.

        Parameters
        ----------
        table_name:str
        df_path:Optional[str]
            Please select either df_path or df option.
        df:Optional[pd.Dataframe]
            Please select either df_path or df option.
        converters:Optional[dict]
            Pass into pandas.read_csv() option.  
            Please see https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
        sep:str
            Pass into pandas.read_csv() option.  
            Please see https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html

        Returns
        ----------
        None

        Raises
        ----------
        PandasMySQLError
            Input already existing table name.
        """
        self.__catchTableList()
        if table_name in self.DBList:
            raise PandasMySQLError(f"It already exists table named {table_name}")        
        df_object = DataframeProcessing(
            table_name = table_name,
            df = df,
            df_path = df_path,
            sep=sep,
            converters = converters)
        df_object.makeDBFrame()
        df_object.makeTableSQLcommand()
        con = self
        cursor = con.cursor()
        cursor.execute(df_object.sql_command)
        self.__catchwaringshow()
    
    def insertRecord(
            self,
            table_name: str,
            df_path: Optional[str] = None,
            df:Optional[pd.DataFrame] = None,
            converters:Optional[dict] = None,
            sep:str = ",",
            Strict_Mode:bool=True
            ) -> None:
        """
        Insert Record into Table

        Parameters
        ----------
        table_name:str
        df_path:Optional[str]
            Please select either df_path or df option.
        df:Optional[pd.Dataframe]
            Please select either df_path or df option.
        converters:Optional[dict]
            Pass into pandas.read_csv() option.  
            Please see https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
        sep:str
            Pass into pandas.read_csv() option.  
            Please see https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
        Strict_Mode:bool (default:True)
            In default parameter, you can't insert string data over that length definition.  
            However,if you select Strict_mode = False, you can insert insert string data over that length definition automatically.

        Return
        ----------
        None

        Raises
        ----------
        PandasMySQLError
            Input not exist table name or quite differnt DataFrame.
        Notes
        ----------
        numeric data definition can't change! (Cannot change int type column into float one)
        """
        self.__catchTableList()
        if not table_name in self.DBList:
            raise PandasMySQLError(f"There is no table named {table_name}")
        
        #make columns list from DB
        self.__catchTableInfo(table_name=table_name)
        df_exist = DataframeProcessing(table_name = None,df = self.table_info)
        df_exist.makeDBFrameFromDB()

        #make columns list from df
        df_insert= DataframeProcessing(
            table_name = None,
            df = df,
            df_path = df_path,
            sep=sep,
            converters = converters
            )
        df_insert.makeDBFrame()
        
        #is match insert data and exist data
        dfs_obj = TwoDataframesProcessing(
            df_exist=df_exist.df_for_command,
            df_insert=df_insert.df_for_command)
        status_message = dfs_obj.isEqualDataFrames(Strict_Mode=Strict_Mode)
        match status_message:
            case "continue":
                _insertRecordBuffer(
                    self,
                    table_name = table_name,
                    df = df,
                    df_path = df_path,
                    sep=sep,
                    converters = converters
                    )
            case "modify":
                #modify table definition
                print("The length of varchar is differnt.Rewrite column definition.")
                modify_obj = DataframeProcessing(
                    table_name = table_name,
                    df=df_insert.df_for_command.iloc[dfs_obj.extract_number,:]
                    )
                modify_obj.makeRewriteSQLcommand()
                con = self
                con.autocommit = False
                cursor = con.cursor()
                for sql_command in modify_obj.sql_command_list:
                    try:
                        cursor.execute(sql_command)
                        con.commit()
                    except Exception as e:
                        con.rollback()
                        raise PandasMySQLError(e)
                
                _insertRecordBuffer(
                    self,
                    table_name = table_name,
                    df = df,
                    df_path = df_path,
                    sep=sep,
                    converters = converters
                    )
                
            case "failed":
                print("--exist--")
                print(df_exist.df_for_command)
                print("--insert--")
                print(df_insert.df_for_command)
                raise PandasMySQLError("Not match Table frame")

    def addPrimaryKey(self,table_name:str,primary_key:str) -> None:
        """
        Add PrimaryKey in table.  
        You can know the advantage of specifying primarykey from here.  
        https://dev.mysql.com/doc/refman/8.0/ja/partitioning-limitations-partitioning-keys-unique-keys.html

        Parameters
        ----------
        table_name:str
        primary_key:str
            Enter column name you want to add primarykey.

        Returns
        ----------
        None
        """ 
        con = self
        cursor = con.cursor()
        cursor.execute(f"alter table {table_name} add primary key ({primary_key});")
        self.__catchwaringshow()
    
    def deletePrimaryKey(self,table_name:str) -> None:
        """
        Delete PrimaryKey.

        Parameters
        ----------
        table_name:str

        Return
        ----------
        None
        """ 
        con = self
        cursor = con.cursor()
        cursor.execute(f"alter table {table_name} drop primary key;")
        self.__catchwaringshow()

    def __catchTableInfo(self,table_name:str) -> None:
        con = self
        cursor = con.cursor()
        cursor.execute(f"show columns from {table_name}")
        rows = cursor.fetchall()
        self.table_info = pd.DataFrame(
            rows,
            columns=["Field","Type","Null","Key","Default","Extra"]
            )

    def __catchTableList(self) -> None:
        self.DBList = [] #initialize
        con = self
        cursor = con.cursor()
        cursor.execute("show tables;")
        rows = cursor.fetchall()
        for row in rows:
            self.DBList.append(row[0])
    
    def __catchwaringshow(self) -> Optional[pd.DataFrame]:
        con = self
        cursor = con.cursor()
        cursor.execute('show warnings;')
        warn_state = pd.DataFrame(cursor.fetchall())
        if not warn_state.empty:
            print(warn_state)

    def executeSQLcommand(self,command:str) -> pd.DataFrame:
        """
        Execute SQL command and return DataFrame object

        Parameters
        ----------
        command:str

        Return
        ----------
        DataFrame
        """ 
        con = self
        cursor = con.cursor()
        try:
            cursor.execute(command)
        except Exception as e:
            raise PandasMySQLError(e)
        result = cursor.fetchall()
        self.__catchwaringshow()
        return pd.DataFrame(result)

    #debug
    def isNullTableNameinTableList(self,table_name:str) -> bool:
        """
        For debug. If self.DBList is None, it return True.
        """
        self.__catchTableList()
        if table_name in self.DBList:
            return True
        else:
            return False

    def __exit__(self, exc_type, exc_value, traceback):
        return super().__exit__(exc_type, exc_value, traceback)


#tools
def _insertRecordBuffer(
        self:MySQLPandas,
        table_name: str,
        df_path: Optional[str] = None,
        df:Optional[pd.DataFrame] = None,
        converters:Optional[dict] = None,
        sep:str = ","
        ):

    record_list = DataframeProcessing(
        table_name = table_name,
        df = df,
        df_path = df_path,
        sep=sep,
        converters = converters
        )
    record_list.makeRecordSQLcommand()

    con = self
    con.autocommit = False
    cursor = con.cursor()
    
    rep = 0
    #make progress bar object
    pbar = tqdm(total=((len(record_list.list_for_command)//1000)+1)*1000)

    while not rep >= len(record_list.list_for_command):   
        split_list_for_command = record_list.list_for_command[rep:rep+1000]
        rep += 1000
        pbar.update(1000)
        try:
            cursor.executemany(record_list.sql_command,split_list_for_command)
            con.commit()

            #print if MySQL output some error.
            cursor.execute('show warnings;')
            warn_state = pd.DataFrame(cursor.fetchall())
            if not warn_state.empty:
                print(warn_state)
            
            time.sleep(1.0)
        except Exception as e:
            con.rollback()
            raise PandasMySQLError(e)
    pbar.close()
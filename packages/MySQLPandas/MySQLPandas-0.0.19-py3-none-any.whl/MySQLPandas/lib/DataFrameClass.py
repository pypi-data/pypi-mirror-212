import pandas as pd
import os
from typing import Optional
from MySQLPandas.lib.ErrorClass import PandasMySQLError,PandasMySQLError_dev
import sys

def ImportDataFrame(df:Optional[pd.DataFrame] = None,df_path:Optional[str] = None,converters:Optional[dict] = None,sep = ",") -> pd.DataFrame:
    if type(df) != type(None) and type(df_path) == type(None):
        return df
    elif type(df) == type(None) and type(df_path) != type(None):
        #is exist df path
        if not os.path.isfile(df_path):
            raise PandasMySQLError("Not exist a path.")
        df = pd.read_csv(df_path,sep=sep,converters=converters)
        return df
    else:
        raise PandasMySQLError("Need argment df or df_path")

class DataframeProcessing():
    def __init__(self,table_name:Optional[str],df:Optional[pd.DataFrame] = None,df_path:Optional[str] = None,converters:Optional[dict] = None,sep = ",") -> None:
        #add option for avoiding Dtypewarnig
        self.df = ImportDataFrame(df=df,df_path=df_path,converters=converters,sep=sep)
        self.df_for_command = None
        self.list_for_command = None
        self.sql_command = None
        self.sql_command_list = None
        self.table_name = table_name
    
    def makeDBFrame(self) -> None:
        #create sql command
        column_name = list(map(lambda x:x.replace(" "," "),list(self.df.columns))) #column name list

        column_type = list(map(str,list(self.df.dtypes))) #column dtype list
        column_type = list(map(lambda x:x.replace("64",""),column_type)) #remove "64"
        column_type = list(map(lambda x:x.replace("object","varchar"),column_type)) #translate string column
        #append convert "float" to "double"?
        column_max_len = []
        count = 0
        for i in self.df.dtypes:
            if i == "object":
                column_max_len.append(int(self.df.iloc[:,count].str.len().max()))
            else:
                column_max_len.append(0)
            count += 1
        df_for_command = pd.DataFrame([column_name,column_type,column_max_len]).T
        self.df_for_command = df_for_command

    def makeTableSQLcommand(self) -> None:
        if self.df_for_command is None:
            raise PandasMySQLError_dev("executing makeSQLcommand method before makeDBFrame method.")
        #make list for set sql command for each row
        sql_command_list = []
        #output row data as tuple from dataframe
        for index,row in self.df_for_command.iterrows():
            if row[2] == 0: #devide string type and int float type
                #int,float
                sql_command_row = "`" + row[0] + "`" + " " + row[1]
                sql_command_list.append(sql_command_row)
            else:
                #string
                if row[2] > 255: 
                    print("The length of string is over 256. Data cannot be saved correctly.")
                    sql_command_row = "`" + str(row[0]) + "`" + " " + str(row[1]) + "(255)"
                    sql_command_list.append(sql_command_row)
                else:
                    sql_command_row = "`" + str(row[0]) + "`" + " " + str(row[1]) + "(" + str(row[2]) + ")"
                    sql_command_list.append(sql_command_row)
        #concat list and print string
        self.sql_command = "create table `" + self.table_name + "` (" + ",".join(sql_command_list) + ");"
    
    def makeRecordSQLcommand(self):
        self.list_for_command = tuple(map(tuple,self.df.values.tolist()))
        part_of_s = ','.join(["%s"]*len(self.df.columns))
        self.makeDBFrame()
        part_of_columns = '`' + '`, `'.join(list(self.df_for_command[0])) + '`'
        self.sql_command = f"insert into `{self.table_name}` (" + part_of_columns + ") values (" + part_of_s + ")"

    def makeRewriteSQLcommand(self):
        #make list for set sql command for each row
        sql_command_list = []
        #output row data as tuple from dataframe
        for index,row in self.df.iterrows():
            if row[2] == 0: #only rewrite string type column
                pass
                #raise PandasMySQLError_dev("unexpected error.")
            else:
                #string
                if row[2] > 255: 
                    print("The length of string is over 256. Data cannot be saved correctly.")
                    sql_command_row = "`" + str(row[0]) + "`" + " " + str(row[1]) + "(255)"
                    sql_command_list.append(sql_command_row)
                else:
                    sql_command_row = "`" + str(row[0]) + "`" + " " + str(row[1]) + "(" + str(row[2]) + ")"
                    sql_command_list.append(sql_command_row)
        self.sql_command_list = list(map(lambda x,y: "alter table " + y + " modify " + x + ";",sql_command_list,["`" + self.table_name + "`"] * len(sql_command_list)))
            
    
    def makeDBFrameFromDB(self):
        #split type column
        self.df_for_command = pd.concat([self.df["Field"],self.df["Type"].str.split("(",expand=True)],axis=1)
        #init column and remove "("
        self.df_for_command.columns = range(self.df_for_command.shape[1])
        self.df_for_command[2] = self.df_for_command[2].str.replace(")","",regex=False)
        #if column type is not varchar,return NA
        self.df_for_command[2] = self.df_for_command[2].where(self.df_for_command[1] == "varchar",0).astype("int")
    
class TwoDataframesProcessing():
    def __init__(self,df_exist:pd.DataFrame,df_insert:pd.DataFrame) -> None:
        self.df_exist = df_exist
        self.df_insert = df_insert
        self.extract_number = []
    
    def isEqualDataFrames(self,Strict_Mode:bool = True) -> str:
        try:
            if (self.df_exist == self.df_insert).all().all():
                return "continue"
            elif ((not (self.df_exist[2] == self.df_insert[2]).all()) and (Strict_Mode == False)):
                if self.isNeedModify():
                    return "modify"
                else:
                    return "continue"
            else:
                return "failed"
        except ValueError as e:
            return "failed"
    
    def isNeedModify(self) -> bool:
        self.extract_number = []
        for i in range(len(self.df_exist)):
            if self.df_exist.iloc[i,-1] >= self.df_insert.iloc[i,-1]:
                pass
            else:
                self.extract_number.append(i) #make modify index list
        if self.extract_number:
            return True
        else:
            return False 
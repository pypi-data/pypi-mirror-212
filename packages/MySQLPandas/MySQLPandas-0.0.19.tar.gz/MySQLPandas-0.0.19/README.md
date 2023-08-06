MySQLPandas
============
[![pages-build-deployment](https://github.com/Sota-Nakashima/MySQLPandas/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/Sota-Nakashima/MySQLPandas/actions/workflows/pages/pages-build-deployment)
[![Version](https://img.shields.io/badge/stable-main-gree)](https://github.com/Sota-Nakashima/MySQLPandas)
[![PyPI](https://img.shields.io/badge/PyPI-0.0.19-blue)](https://pypi.org/project/MySQLPandas/)
[![License: GPL v2](https://img.shields.io/badge/License-GPL_v2-blue.svg)](https://github.com/Sota-Nakashima/MySQLPandas/blob/main/LICENCE)
#  Overview
Simple connector between MySQL(MariaDB) and Pandas

## Description
This tool is primarily intended to help Python users easily handle databases.
It uses Pandas as its base, so it should be easy to use even for those who are not familiar with databases.
The tool supports MySQL or MariaDB as the database engine.
## Demo
* Make new table and install dataframe or csv
```python:tutoring.py
from MySQLPandas.core import MySQLPandas
with MySQLPandas("hoge","hoge_db",initfile_path="hoge.ini") as obj:
    obj.makeTable("sample_table",df_path="sample.csv")
    obj.showTableinfo("sample_table")
    obj.insertRecord("sample_table",df_path="sample.csv")
```

Regarding other functions, see [here](https://sota-nakashima.github.io/MySQLPandas/MySQLPandas.html).

## Note
In MySQLPandas function of insertRecord, it doesn't allow any difference on table denfinition.(If it has slightly differcence, MySQLPandas raise error.)  
```
raise PandasMySQLError("Not match Table frame")
MySQLPandas.lib.ErrorClass.PandasMySQLError: Not match Table frame
```
If you want to change table definition, please see below.  
* Change string type column  
  You can change table denfiniton automatically. Please rewrite  "Strict_Mode = False" in "insertRecord" method.
* Change int or float type column  
  Sorry, you can't change it in MySQLPandas. Please rewrite it by using "executeSQLcommand" method. 

0.0.19 ~
* Columns are no longer automatically assigned an underscore instead of a space when the database is created. However, it is recommended to replace them with underbars as much as possible, since spaces may cause unintended behavior.
## Setup password.ini
In default, you need to input DB password in your console every time.  
If you felt bothered, you avoid this by creating "password.ini" file.  
In GitHub page, it's put [sample file](https://github.com/Sota-Nakashima/MySQLPandas/blob/main/password_sample.ini).
## Requirement
* MySQL(MariaDB)  
The version of Auther's MariaDB is 5.5.68-MariaDB MariaDB Server.  
Don't try the newest version so please check your MariaDB version.
* Pandas <= 1.5.3
* Python 3.*
* mysql-connector-python <= 8.0.29
* tqdm <= 4.65.0

## Developer Guide
See [here](https://sota-nakashima.github.io/MySQLPandas/).
## Install
Install through pip.
```
pip install MySQLPandas
```

## Licence

[GNU GPLv2](https://github.com/Sota-Nakashima/MySQLPandas/blob/main/LICENSE)

## Author

[Sota Nakashima](https://github.com/Sota-Nakashima)

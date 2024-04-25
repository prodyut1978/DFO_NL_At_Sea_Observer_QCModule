from tkinter import*
from tkinter import messagebox
import sqlite3
import pandas as pd

DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
DB_SetCatch_Validation_Range = ("./BackEnd/Sqlite3_DB/QC_Check_RangeConsistency_DB/DFO_NL_ASOP_SetCatch_RangeValidation.db")

def SetCatch_Count_FailedQC_TowDistance():
        conn = sqlite3.connect(DB_SetCatch_Validation_Range)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_TowDistance;", conn)
        data = pd.DataFrame(Complete_df)
        ## QC FailCount
        QCFailCount = data[(data.TowDiffFlag) == 'Yes']
        QCFailCount  = QCFailCount.reset_index(drop=True)
        QCFailCount  = pd.DataFrame(QCFailCount)
        Length_QCFailedDF = len(QCFailCount)                  
        conn.commit()
        conn.close()
        return Length_QCFailedDF

def SetCatch_Count_FailedQC_TowSeparation():
        conn = sqlite3.connect(DB_SetCatch_Validation_Range)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_TowSeparation;", conn)
        data = pd.DataFrame(Complete_df)
        ## QC FailCount
        QCFailCount = data[(data.TowSepErrorFlag) == 'Yes']
        QCFailCount  = QCFailCount.reset_index(drop=True)
        QCFailCount  = pd.DataFrame(QCFailCount)
        Length_QCFailedDF = len(QCFailCount)                  
        conn.commit()
        conn.close()
        return Length_QCFailedDF

def SetCatch_NumberOf_Entries():
        conn = sqlite3.connect(DB_Set_Catch_Analysis)
        Complete_df= pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data[(data.RecordType) == 1]
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_Entries = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_Entries
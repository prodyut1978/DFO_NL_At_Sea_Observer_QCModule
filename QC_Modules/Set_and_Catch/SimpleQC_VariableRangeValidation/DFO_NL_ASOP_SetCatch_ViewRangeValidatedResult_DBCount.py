from tkinter import*
from tkinter import messagebox
import sqlite3
import pandas as pd

DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
DB_SetCatch_Validation_Range = ("./BackEnd/Sqlite3_DB/QC_Check_RangeConsistency_DB/DFO_NL_ASOP_SetCatch_RangeValidation.db")

def SetCatch_NumberOf_FailedQC_CalenderVariables():
        conn = sqlite3.connect(DB_SetCatch_Validation_Range)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_CalenderVariables ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_FailedQC_CalenderVariables = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_FailedQC_CalenderVariables

def SetCatch_NumberOf_FailedQC_PositionalVariables():
        conn = sqlite3.connect(DB_SetCatch_Validation_Range)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_PositionalVariables ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_FailedQC_PositionalVariables = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_FailedQC_PositionalVariables

def SetCatch_NumberOf_FailedQC_GearVariables():
        conn = sqlite3.connect(DB_SetCatch_Validation_Range)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_GearVariables ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_FailedQC_GearVariables = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_FailedQC_GearVariables

def SetCatch_NumberOf_FailedQC_CatchVariables():
        conn = sqlite3.connect(DB_SetCatch_Validation_Range)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_CatchVariables ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_FailedQC_CatchVariables = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_FailedQC_CatchVariables

def SetCatch_NumberOf_Entries():
        conn = sqlite3.connect(DB_Set_Catch_Analysis)
        Complete_df= pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_Entries = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_Entries
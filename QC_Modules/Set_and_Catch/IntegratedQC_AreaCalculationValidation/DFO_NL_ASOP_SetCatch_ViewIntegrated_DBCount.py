from tkinter import*
from tkinter import messagebox
import sqlite3
import pandas as pd

DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
DB_SetCatch_Val_Calculation = ("./BackEnd/Sqlite3_DB/QC_Check_CalculationConsistency_DB/DFO_NL_ASOP_SetCatch_Calculation.db")


def SetCatch_FailCount_NAFOAreaCalc():
        conn = sqlite3.connect(DB_SetCatch_Val_Calculation)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_NAFO_AreaQCAnalysis;", conn)
        data = pd.DataFrame(Complete_df)
        ## QC FailCount
        QCFailCount = data[
            ((data.NAFOValidityCheck_StartPoints) == 'NAFO-QC Failed')
            ]
        QCFailCount  = QCFailCount.reset_index(drop=True)
        QCFailCount  = pd.DataFrame(QCFailCount)
        Length_QCFailedDF = len(QCFailCount)                  
        conn.commit()
        conn.close()
        return Length_QCFailedDF

def SetCatch_FailCount_UnitAreaCalc():
        conn = sqlite3.connect(DB_SetCatch_Val_Calculation)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_UnitAreaQCAnalysis;", conn)
        data = pd.DataFrame(Complete_df)
        ## QC FailCount
        QCFailCount = data[
                ((data.UAValidityCheck_StartPoints) == 'UnitArea-QC Failed')
                ]
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
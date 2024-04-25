from tkinter import*
from tkinter import messagebox
import sqlite3
import pandas as pd

DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
DB_SetCatch_Validation_Consistency = ("./BackEnd/Sqlite3_DB/QC_Check_ConsistencyValidate_DB/DFO_NL_ASOP_SetCatch_ConsistencyValidation.db")


def SetCatch_NumberOf_ConsistncyFailedQC_YCQ():
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_YCQ_FailConsis_SummaryDF;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        FailedQC_YCQ = sum(data['QCFailCount'])                     
        conn.commit()
        conn.close()
        return FailedQC_YCQ

def SetCatch_NumberOf_ConsistncyFailedQC_Vessel():
        ListConsistency = ['FailCount_VesselSideNumber_Consistency',
                          'FailCount_VesselClass_Consistency',
                          'FailCount_VesselLength_Consistency',
                          'FailCount_VesselHorsepower_Consistency']
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_Vessel_FailConsis_SummaryDF;", conn)
        conn.commit()
        conn.close()
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        TotalFailedQC_Vessel = sum(data['QCFailCount'])
        FailedQC_VSN_STN =  data[((data.VariableName) == ListConsistency[0])]
        FailedQC_VSN_STN  = FailedQC_VSN_STN.reset_index(drop=True)
        FailedQC_VSN_STN = pd.DataFrame(FailedQC_VSN_STN)
        TotalFailedQC_VSN_STN = sum(FailedQC_VSN_STN['QCFailCount'])                  
        TotalFailedQC_VC_VL_VHP = TotalFailedQC_Vessel - TotalFailedQC_VSN_STN
        return TotalFailedQC_Vessel, TotalFailedQC_VSN_STN, TotalFailedQC_VC_VL_VHP 

def SetCatch_NumberOf_ConsistncyFailedQC_Calender():
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_Calender_FailConsis_SummaryDF;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        FailedQC_Calender = sum(data['QCFailCount'])                     
        conn.commit()
        conn.close()
        return FailedQC_Calender

def SetCatch_NumberOf_ConsistncyFailedQC_MG():
        conn = sqlite3.connect(DB_SetCatch_Validation_Consistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_MobileGear_FailConsis_SummaryDF;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        FailedQC_MG = sum(data['QCFailCount'])                     
        conn.commit()
        conn.close()
        return FailedQC_MG

def SetCatch_NumberOf_Entries():
        conn = sqlite3.connect(DB_Set_Catch_Analysis)
        Complete_df= pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_Entries = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_Entries
from tkinter import*
from tkinter import messagebox
import sqlite3
import pandas as pd

DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
DB_SetCatch_Validation_Presence = ("./BackEnd/Sqlite3_DB/QC_Check_PresenceConsistency_DB/DFO_NL_ASOP_SetCatch_PresenceValidation.db")

## 01: Presence must Count
def SetCatch_NumberOf_PresenceMust_Failed():
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MustVariables ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        NumbOf_PresenceMust_Failed = len(data)                    
        conn.commit()
        conn.close()
        return NumbOf_PresenceMust_Failed

## 02: Presence conditional Count
def SetCatch_NumberOf_PresenceConditional_Failed():
        FailedQC_AverageTowSpeed = SetCatch_NumberOf_FailedQC_AverageTowSpeed()
        FailedQC_CodendMeshSize = SetCatch_NumberOf_FailedQC_CodendMeshSize()
        FailedQC_MeshSizeMG = SetCatch_NumberOf_FailedQC_MeshSizeMG()
        FailedQC_NumberGillnets = SetCatch_NumberOf_FailedQC_NumberGillnets()
        FailedQC_AverageGillnetLength = SetCatch_NumberOf_FailedQC_AverageGillnetLength()
        FailedQC_NumberHooks = SetCatch_NumberOf_FailedQC_NumberHooks()
        FailedQC_NumberPots = SetCatch_NumberOf_FailedQC_NumberPots()
        FailedQC_NumberWindows = SetCatch_NumberOf_FailedQC_NumberWindows()
        NumbOf_PresenceConditional_Failed = (int(FailedQC_AverageTowSpeed) + \
                                             int(FailedQC_CodendMeshSize) + \
                                             int(FailedQC_MeshSizeMG) + \
                                             int(FailedQC_NumberGillnets) + \
                                             int(FailedQC_AverageGillnetLength) + \
                                             int(FailedQC_NumberHooks)+ \
                                             int(FailedQC_NumberPots)+ \
                                             int(FailedQC_NumberWindows))
        return NumbOf_PresenceConditional_Failed

def SetCatch_NumberOf_FailedQC_AverageTowSpeed():
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageTowSpeed ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        FailedQC_AverageTowSpeed = len(data)                    
        conn.commit()
        conn.close()
        return FailedQC_AverageTowSpeed

def SetCatch_NumberOf_FailedQC_CodendMeshSize():
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_CodendMeshSize ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        FailedQC_CodendMeshSize = len(data)                    
        conn.commit()
        conn.close()
        return FailedQC_CodendMeshSize

def SetCatch_NumberOf_FailedQC_MeshSizeMG():
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_MeshSizeMG ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        FailedQC_MeshSizeMG = len(data)                    
        conn.commit()
        conn.close()
        return  FailedQC_MeshSizeMG

def SetCatch_NumberOf_FailedQC_NumberGillnets():
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberGillnets ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        FailedQC_NumberGillnets = len(data)                    
        conn.commit()
        conn.close()
        return FailedQC_NumberGillnets

def SetCatch_NumberOf_FailedQC_AverageGillnetLength():
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_AverageGillnetLength ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        FailedQC_AverageGillnetLength = len(data)                    
        conn.commit()
        conn.close()
        return FailedQC_AverageGillnetLength

def SetCatch_NumberOf_FailedQC_NumberHooks():
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberHooks ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        FailedQC_NumberHooks = len(data)                    
        conn.commit()
        conn.close()
        return FailedQC_NumberHooks

def SetCatch_NumberOf_FailedQC_NumberWindows():
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberWindows ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        FailedQC_NumberWindows = len(data)                    
        conn.commit()
        conn.close()
        return FailedQC_NumberWindows

def SetCatch_NumberOf_FailedQC_NumberPots():
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedPresence_NumberPots ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        FailedQC_NumberPots = len(data)                    
        conn.commit()
        conn.close()
        return FailedQC_NumberPots



## 03: Presence Rectype-GearDamage Count
def SetCatch_NumOf_PreCondlMisc_Fail():
        conn = sqlite3.connect(DB_SetCatch_Validation_Presence)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedMiscPresence_RecTGearDamage;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        FailedNumOf_PreCondlMisc = len(data)                    
        conn.commit()
        conn.close()
        return FailedNumOf_PreCondlMisc

def SetCatch_NumberOf_Entries():
        conn = sqlite3.connect(DB_Set_Catch_Analysis)
        Complete_df= pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_Entries = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_Entries
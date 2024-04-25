from tkinter import*
from tkinter import messagebox
import sqlite3
import pandas as pd

DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
DB_SetCatch_Validation_Logical = ("./BackEnd/Sqlite3_DB/QC_Check_LogicalConsistency_DB/DFO_NL_ASOP_SetCatch_LogicalValidation.db")


def SetCatch_NumberOf_LogicalCatch_Failed():
        FailedQC_CodendMeshSize = SetCatch_NumberOf_FailedQC_CodendMeshSize()
        FailedQC_DirectedSpecies = SetCatch_NumberOf_FailedQC_DirectedSpecies()
        FailedQC_NumberPotReleasedCrab = SetCatch_NumberOf_FailedQC_NumberPotReleasedCrab()
        FailedQC_KeptWeight_DiscardWeight = SetCatch_NumberOf_FailedQC_KeptWeight_DiscardWeight()
        NumbOf_LogicalCatch_Failed = (int(FailedQC_CodendMeshSize) + \
                                             int(FailedQC_DirectedSpecies) + \
                                             int(FailedQC_NumberPotReleasedCrab) + \
                                             int(FailedQC_KeptWeight_DiscardWeight))
        return NumbOf_LogicalCatch_Failed

def SetCatch_NumberOf_FailedQC_CodendMeshSize():
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_CatchVariable_CodendMeshSize ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        FailedQC_CodendMeshSize = len(data)                    
        conn.commit()
        conn.close()
        return FailedQC_CodendMeshSize

def SetCatch_NumberOf_FailedQC_DirectedSpecies():
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_CatchVariable_DirectedSpecies ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        FailedQC_DirectedSpecies = len(data)                    
        conn.commit()
        conn.close()
        return  FailedQC_DirectedSpecies

def SetCatch_NumberOf_FailedQC_NumberPotReleasedCrab():
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_CatchVariable_NumberPotReleasedCrab ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        FailedQC_NumberPotReleasedCrab = len(data)                    
        conn.commit()
        conn.close()
        return FailedQC_NumberPotReleasedCrab

def SetCatch_NumberOf_FailedQC_KeptWeight_DiscardWeight():
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_CatchVariable_KeptWeight_DiscardWeight ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        FailedQC_KeptWeight_DiscardWeight = len(data)                    
        conn.commit()
        conn.close()
        return FailedQC_KeptWeight_DiscardWeight

def SetCatch_NumberOf_Entries():
        conn = sqlite3.connect(DB_Set_Catch_Analysis)
        Complete_df= pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_Entries = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_Entries

def SetCatch_NumberOf_LogicalRS_Failed():
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        Complete_df= pd.read_sql_query("SELECT * FROM Logical_RecordType_SetNumber_FailSummary;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        RecordType_SetNumber = len(data)                    
        conn.commit()
        conn.close()
        return RecordType_SetNumber

def SetCatch_NumberOf_LogicalRN_Failed():
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        Complete_df= pd.read_sql_query("SELECT * FROM Logical_RecordType_NumberSpecies_FailSummary;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        RecordType_NumberSpecies = sum(data['QCFailCount'])                     
        conn.commit()
        conn.close()
        return RecordType_NumberSpecies

def SetCatch_NumberOf_LogicalRT_SpCode_Failed():
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        Complete_df= pd.read_sql_query("SELECT * FROM Logical_RecType_SpecsCode_NumbSpecs_FailSummary;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        LengthRT_SpCode = sum(data['QCFailCount'])                       
        conn.commit()
        conn.close()
        return LengthRT_SpCode

def SetCatch_NumberOf_RecType_KW_DW_NI_Failed():
        conn = sqlite3.connect(DB_SetCatch_Validation_Logical)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLogical_RecType_KW_DW_NI;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        LenRecType_KW_DW_NI = len(data)                     
        conn.commit()
        conn.close()
        return LenRecType_KW_DW_NI
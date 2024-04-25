from tkinter import*
from tkinter import messagebox
import sqlite3
import pandas as pd


DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")
DB_SetCatch_Validation_LookUpConsistency = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")

def SetCatch_NumberOf_FailedQC_ASOCCode():
        conn = sqlite3.connect(DB_SetCatch_Validation_LookUpConsistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_ASOCCode ORDER BY `ASOCCode` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_FailedQC_ASOCCode = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_FailedQC_ASOCCode

def SetCatch_NumberOf_FailedQC_Country():
        conn = sqlite3.connect(DB_SetCatch_Validation_LookUpConsistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_Country ORDER BY `Country` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_FailedQC_Country = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_FailedQC_Country

def SetCatch_NumberOf_FailedQC_DataSource():
        conn = sqlite3.connect(DB_SetCatch_Validation_LookUpConsistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_DataSource ORDER BY `DataSource` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_FailedQC_DataSource = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_FailedQC_DataSource

def SetCatch_NumberOf_FailedQC_GearDamage():
        conn = sqlite3.connect(DB_SetCatch_Validation_LookUpConsistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_GearDamage ORDER BY `GearDamage` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_FailedQC_GearDamage = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_FailedQC_GearDamage

def SetCatch_NumberOf_FailedQC_GearType():
        conn = sqlite3.connect(DB_SetCatch_Validation_LookUpConsistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_GearType ORDER BY `GearType` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_FailedQC_GearType = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_FailedQC_GearType

def SetCatch_NumberOf_FailedQC_Quota():
        conn = sqlite3.connect(DB_SetCatch_Validation_LookUpConsistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_Quota ORDER BY `Quota` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_FailedQC_Quota = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_FailedQC_Quota

def SetCatch_NumberOf_FailedQC_SetType():
        conn = sqlite3.connect(DB_SetCatch_Validation_LookUpConsistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_SetType ORDER BY `SetType` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_FailedQC_SetType = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_FailedQC_SetType

def SetCatch_NumberOf_FailedQC_SpeciesCode():
        conn = sqlite3.connect(DB_SetCatch_Validation_LookUpConsistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_SpeciesCode ORDER BY `SpeciesCode` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_FailedQC_SpeciesCode = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_FailedQC_SpeciesCode

def SetCatch_NumberOf_FailedQC_DirectedSpecies():
        conn = sqlite3.connect(DB_SetCatch_Validation_LookUpConsistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_DirectedSpecies ORDER BY `DirectedSpecies` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_FailedQC_DirectedSpecies = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_FailedQC_DirectedSpecies

def SetCatch_NumberOf_FailedQC_VesselClass():
        conn = sqlite3.connect(DB_SetCatch_Validation_LookUpConsistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_VesselClass ORDER BY `VesselClass` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_FailedQC_VesselClass = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_FailedQC_VesselClass

def SetCatch_NumberOf_FailedQC_NAFODivision():
        conn = sqlite3.connect(DB_SetCatch_Validation_LookUpConsistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_NAFODivision ORDER BY `NAFODivision` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_FailedQC_NAFODivision = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_FailedQC_NAFODivision

def SetCatch_NumberOf_FailedQC_UnitArea():
        conn = sqlite3.connect(DB_SetCatch_Validation_LookUpConsistency)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_QCFailedLookUpTable_UnitArea ORDER BY `UnitArea` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_FailedQC_UnitArea = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_FailedQC_UnitArea

def SetCatch_NumberOf_Entries():
        conn = sqlite3.connect(DB_Set_Catch_Analysis)
        Complete_df= pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        SetCatch_NumberOf_Entries = len(data)                    
        conn.commit()
        conn.close()
        return SetCatch_NumberOf_Entries
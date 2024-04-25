from tkinter import*
from tkinter import messagebox
import sqlite3
import pandas as pd
from QC_Modules.Set_and_Catch.SimpleQC_LookUpTableValidation import DFO_NL_ASOP_SetCatch_RunLookUpTableValidation_BackEnd

DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")
DB_SetCatch_Validation_LookUpConsistency = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")

def SetCatch_RunLookUpTableValidation():
    FailedLookUpTableValidation_ASOCCode = DFO_NL_ASOP_SetCatch_RunLookUpTableValidation_BackEnd.RunLookUpTableValidation_BackEnd_ASOCCode()
    FailedLookUpTableValidation_Country = DFO_NL_ASOP_SetCatch_RunLookUpTableValidation_BackEnd.RunLookUpTableValidation_BackEnd_Country()
    FailedLookUpTableValidation_DataSource = DFO_NL_ASOP_SetCatch_RunLookUpTableValidation_BackEnd.RunLookUpTableValidation_BackEnd_DataSource()
    FailedLookUpTableValidation_GearDamage = DFO_NL_ASOP_SetCatch_RunLookUpTableValidation_BackEnd.RunLookUpTableValidation_BackEnd_GearDamage()
    FailedLookUpTableValidation_GearType = DFO_NL_ASOP_SetCatch_RunLookUpTableValidation_BackEnd.RunLookUpTableValidation_BackEnd_GearType()
    FailedLookUpTableValidation_Quota = DFO_NL_ASOP_SetCatch_RunLookUpTableValidation_BackEnd.RunLookUpTableValidation_BackEnd_Quota()
    FailedLookUpTableValidation_SetType = DFO_NL_ASOP_SetCatch_RunLookUpTableValidation_BackEnd.RunLookUpTableValidation_BackEnd_SetType()
    FailedLookUpTableValidation_SpeciesCode = DFO_NL_ASOP_SetCatch_RunLookUpTableValidation_BackEnd.RunLookUpTableValidation_BackEnd_SpeciesCode()
    FailedLookUpTableValidation_DirectedSpecies = DFO_NL_ASOP_SetCatch_RunLookUpTableValidation_BackEnd.RunLookUpTableValidation_BackEnd_DirectedSpecies()
    FailedLookUpTableValidation_VesselClass = DFO_NL_ASOP_SetCatch_RunLookUpTableValidation_BackEnd.RunLookUpTableValidation_BackEnd_VesselClass()
    FailedLookUpTableValidation_NAFODivision = DFO_NL_ASOP_SetCatch_RunLookUpTableValidation_BackEnd.RunLookUpTableValidation_BackEnd_NAFODivision()
    FailedLookUpTableValidation_UnitArea = DFO_NL_ASOP_SetCatch_RunLookUpTableValidation_BackEnd.RunLookUpTableValidation_BackEnd_UnitArea()
    
    TotalFailedQC_LookUpTable =  ((int(FailedLookUpTableValidation_ASOCCode) + \
                                       int(FailedLookUpTableValidation_Country) + \
                                       int(FailedLookUpTableValidation_DataSource) + \
                                       int(FailedLookUpTableValidation_GearDamage) + \
                                       int(FailedLookUpTableValidation_GearType) + \
                                       int(FailedLookUpTableValidation_Quota) + \
                                       int(FailedLookUpTableValidation_SetType) + \
                                       int(FailedLookUpTableValidation_SpeciesCode) + \
                                       int(FailedLookUpTableValidation_DirectedSpecies) + \
                                       int(FailedLookUpTableValidation_VesselClass)  + \
                                       int(FailedLookUpTableValidation_NAFODivision))  + \
                                       int(FailedLookUpTableValidation_UnitArea))
    
    ReturnFailedMessage = str(TotalFailedQC_LookUpTable) + " " + " Failed In QC"
    ReturnPassedMessage = "All Passed"
    if TotalFailedQC_LookUpTable > 0:
        ReturnMsg = ReturnFailedMessage
    else:
        ReturnMsg = ReturnPassedMessage
    return ReturnMsg, TotalFailedQC_LookUpTable

#Import Python Modules
from tkinter import*
import tkinter.messagebox
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, filedialog
import sqlite3
from datetime import datetime
import pandas as pd
import numpy as np
import pickle
import os

DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")
DB_SetCatch_Validation_LookUpTable = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")
Pickle_FileNameImport ="./Pickle_MetaData/ImportFileName.pickle"
DB_Set_Catch_Misc = ("./BackEnd/Sqlite3_DB/SetCatch_Misc_DB/DFO_NL_ASOP_Set_Catch_Misc.db")
DB_SetCatch_Val_Calculation = ("./BackEnd/Sqlite3_DB/QC_Check_CalculationConsistency_DB/DFO_NL_ASOP_SetCatch_Calculation.db")
DB_SetCatch_Validation_Range = ("./BackEnd/Sqlite3_DB/QC_Check_RangeConsistency_DB/DFO_NL_ASOP_SetCatch_RangeValidation.db")
DB_SetCatch_Validation_Presence = ("./BackEnd/Sqlite3_DB/QC_Check_PresenceConsistency_DB/DFO_NL_ASOP_SetCatch_PresenceValidation.db")
DB_SetCatch_Validation_Logical = ("./BackEnd/Sqlite3_DB/QC_Check_LogicalConsistency_DB/DFO_NL_ASOP_SetCatch_LogicalValidation.db")
DB_SetCatch_Validation_Consistency = ("./BackEnd/Sqlite3_DB/QC_Check_ConsistencyValidate_DB/DFO_NL_ASOP_SetCatch_ConsistencyValidation.db")

###### Import BackEnd Files 
# DB Create Set and Catch QC Database and Lookup table
from BackEnd.DB_Schema import DFO_NL_ASOP_Set_Catch_DB_BackEnd
from BackEnd.DB_Schema import DFO_NL_ASOP_Lookup_Table_DB_BackEnd
from BackEnd.DB_Schema import DFO_NL_ASOP_LookUpTableValidation_DB_BackEnd
from BackEnd.DB_Schema import DFO_NL_ASOP_RangeValidation_DB_BackEnd
from BackEnd.DB_Schema import DFO_NL_ASOP_PresenceValidation_DB_BackEnd
from BackEnd.DB_Schema import DFO_NL_ASOP_LogicalValidation_DB_BackEnd
from BackEnd.DB_Schema import DFO_NL_ASOP_ConsistencyValidation_DB_BackEnd
from BackEnd.DB_Schema import DFO_NL_ASOP_Set_Catch_Misc_BackEnd
from BackEnd.DB_Schema import DFO_NL_ASOP_CalculationValidation_DB_BackEnd

DFO_NL_ASOP_Set_Catch_DB_BackEnd.DFO_NL_ASOP_Set_Catch_Analysis()
DFO_NL_ASOP_Lookup_Table_DB_BackEnd.DFO_NL_ASOP_Lookup_Table_DB()
DFO_NL_ASOP_LookUpTableValidation_DB_BackEnd.DFO_NL_ASOP_LookUpTableValidation_DB()
DFO_NL_ASOP_RangeValidation_DB_BackEnd.DFO_NL_ASOP_RangeValidation_DB()
DFO_NL_ASOP_PresenceValidation_DB_BackEnd.DFO_NL_ASOP_PresenceValidation_DB()
DFO_NL_ASOP_LogicalValidation_DB_BackEnd.DFO_NL_ASOP_LogicalValidation_DB()
DFO_NL_ASOP_ConsistencyValidation_DB_BackEnd.DFO_NL_ASOP_ConsistencyValidation_DB()
DFO_NL_ASOP_Set_Catch_Misc_BackEnd.DFO_NL_ASOP_Set_Catch_Misc()
DFO_NL_ASOP_CalculationValidation_DB_BackEnd.DFO_NL_ASOP_CalculationValidation_DB()

###### Import External Import Files
# Import Observer Set and Catch CSV DataSheet Module
from External_Import.SetCatch_ImportCSV import DFO_NL_ASOP_Set_Catch_Import_CSV

# Import Observer Lookup Tables Module
from External_Import.LookUpTables_Import import DFO_NL_ASOP_GenAll_LookupTables
from External_Import.LookUpTables_Import import DFO_NL_ASOP_LookupTable_ASOCCode
from External_Import.LookUpTables_Import import DFO_NL_ASOP_LookupTable_Country
from External_Import.LookUpTables_Import import DFO_NL_ASOP_LookupTable_DataSource
from External_Import.LookUpTables_Import import DFO_NL_ASOP_LookupTable_GearDamage
from External_Import.LookUpTables_Import import DFO_NL_ASOP_LookupTable_GearType
from External_Import.LookUpTables_Import import DFO_NL_ASOP_LookupTable_Quota
from External_Import.LookUpTables_Import import DFO_NL_ASOP_LookupTable_SetType
from External_Import.LookUpTables_Import import DFO_NL_ASOP_LookupTable_SpeciesCode
from External_Import.LookUpTables_Import import DFO_NL_ASOP_LookupTable_VesselClass
from External_Import.LookUpTables_Import import DFO_NL_ASOP_LookupTable_NAFODivision

# Import Observer Variable Range Tables Module
from External_Import.VariablesRangeTable_Import import DFO_NL_ASOP_RangeVariables_ValidationTable

# Import Area Calculated Import Module
from External_Import.AreaCalculated_Import import DFO_NL_ASOP_NAFOAreaTable

###### View Imported Observer Set and Catch DB View and Export DB Module
from ViewDB_And_ExportDB.Set_and_Catch import DFO_NL_ASOP_TreeViewDatabaseQCAnalysis_SetCatch
from ViewDB_And_ExportDB.Set_and_Catch import DFO_NL_ASOP_ExcelViewDatabaseQCAnalysis_SetCatch 

###### Import QC Modules - Simple QC- Module - C
# Import Set& Catch - LookUp Tables QC Modules - C-1
from QC_Modules.Set_and_Catch.SimpleQC_LookUpTableValidation import DFO_NL_ASOP_SetCatch_RunLookUpTableValidation
from QC_Modules.Set_and_Catch.SimpleQC_LookUpTableValidation import DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult
# Import Set& Catch - Range Variables QC Modules - C-2
from QC_Modules.Set_and_Catch.SimpleQC_VariableRangeValidation import DFO_NL_ASOP_SetCatch_RunRangeValidation
from QC_Modules.Set_and_Catch.SimpleQC_VariableRangeValidation import DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult
# Import Set& Catch - Presence Variables QC Modules - C-3
from QC_Modules.Set_and_Catch.SimpleQC_VariablePresenceValidation import DFO_NL_ASOP_SetCatch_RunPresenceValidation
from QC_Modules.Set_and_Catch.SimpleQC_VariablePresenceValidation import DFO_NL_ASOP_SetCatch_ViewPresenceValidatedResult
# Import Set& Catch - Logical Variables QC Modules - C-4
from QC_Modules.Set_and_Catch.SimpleQC_VariableLogicalValidation import DFO_NL_ASOP_SetCatch_RunLogicalValidation
from QC_Modules.Set_and_Catch.SimpleQC_VariableLogicalValidation import DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult
# Import Set& Catch - Consistency Variables QC Modules - C-5
from QC_Modules.Set_and_Catch.SimpleQC_VariableConsistencyValidation import DFO_NL_ASOP_SetCatch_RunConsistencyValidation
from QC_Modules.Set_and_Catch.SimpleQC_VariableConsistencyValidation import DFO_NL_ASOP_SetCatch_ViewConsistencyValidatedResult

###### Import QC Modules - Integrated QC- Module - D
# Import Set& Catch - Range Variables QC Modules - D-2
from QC_Modules.Set_and_Catch.IntegratedQC_VariableRangeValidation import DFO_NL_ASOP_SetCatch_RunIntegratedRangeValidation
from QC_Modules.Set_and_Catch.IntegratedQC_VariableRangeValidation import DFO_NL_ASOP_SetCatch_ViewIntegratedRangeResult
# Import Set& Catch - Range Variables QC Modules - D-3
from QC_Modules.Set_and_Catch.IntegratedQC_AreaCalculationValidation import DFO_NL_ASOP_SetCatch_RunIntegratedAreaCalValidation
from QC_Modules.Set_and_Catch.IntegratedQC_AreaCalculationValidation import DFO_NL_ASOP_SetCatch_ViewIntegratedAreaCalcResult

###### Import QC Modules - Tombstone QC- Module - E
from QC_Modules.Set_and_Catch.TombstoneQC_SetDataValidation import DFO_NL_ASOP_SetCatch_RunTombstoneQCValidation
from QC_Modules.Set_and_Catch.TombstoneQC_SetDataValidation import DFO_NL_ASOP_SetCatch_ViewTombQCSetDataValResult

## Main 
class DFO_NL_ASOP_Module:    
    def __init__(self,root):
        Default_Date_today   = datetime.now()
        self.root =root
        self.root.title ("QC Main Version 0.1.0")
        self.root.geometry("830x580+100+50")
        self.root.config(bg="cadet blue")
        self.root.resizable(0, 0)

        ## DataFrame Main-Headers - SetCatch
        DataFrameMainSCHead = Frame(self.root)
        DataFrameMainSCHead.grid(row=0,column=0 ,columnspan=2, padx= 5, pady=10)
        lblDFO_NL_ASOP_Set_Catch = Label(DataFrameMainSCHead, bd= 4, font=('Helvetica', 12, 'bold', 'underline'), 
                                   width = 34, fg = 'blue',
                                   text="*** DFO-NL-ASO Set & Catch QC Modules *** ")
        lblDFO_NL_ASOP_Set_Catch.grid(row=0,column=0,padx= 1, pady= 0, ipady =4)   

        ## DataFrameLEFT -Headers
        DataFrameLEFT = Frame(self.root)
        DataFrameLEFT.grid(row=1,column=0 ,padx= 5, pady=1)     
        
        lblDFO_NL_ASOP_Set_Catch = Label(DataFrameLEFT, bd= 4, font=('Helvetica', 11, 'bold'), 
                    width = 28, fg = 'green',
                    bg = "orange", underline =-1, text="Import View & Update Module")
        lblDFO_NL_ASOP_Set_Catch.grid(row=0,column=0,padx= 1, pady= 1, ipady =1)

        lbl_DB_Display = Label(DataFrameLEFT, bd= 4, font=('Helvetica', 11, 'bold'), width = 12, fg = 'green',
                    bg = "orange", text="System Display ")
        lbl_DB_Display.grid(row=12,column=0, padx= 1, pady= 2, ipady =1)

        lbl_DB_Export = Label(DataFrameLEFT, bd= 4, font=('Helvetica', 11, 'bold'), width = 15, fg = 'green',
                    bg = "orange", text="Database Export ")
        lbl_DB_Export.grid(row=22,column=0, padx= 1, pady= 2, ipady =1)

        ## DataFrameRIGHT - Headers
        DataFrameRIGHT = Frame(self.root)
        DataFrameRIGHT.grid(row=1,column=1 ,padx= 10, pady= 1)        
       
        lblDFO_NL_ASOP_Set_Catch = Label(DataFrameRIGHT, bd= 6, font=('Helvetica', 12, 'bold'), width = 45, fg = 'green',
                    bg = "orange", text="**   Set & Catch QC & Validation Module   ** \n(Simple & Integrated Check)")
        lblDFO_NL_ASOP_Set_Catch.grid(row=0,column=0, padx= 1, pady= 1, ipady= 1)

        ## Define Functions For Run Simple QC Check On Module - C
        def RunSimpleQCValidationCheck():
            ListSimpleQCCheck = ['Select Simple QC & Validation SubType',
                    '1: Simple Table Lookup & Validation Check',
                    '2: Simple Range & Validation Check',
                    '3: Simple Presence & Validation Check',
                    '4: Simple Logical & Validation Check',
                    '5: Simple Consistency & Validation Check']
            
            getSimpleQCValidationCheck = entry_VarListSimpleQCCheck.get()
            
            if getSimpleQCValidationCheck == ListSimpleQCCheck[0]:
                tkinter.messagebox.showinfo("Run Simple QC Validation Message","Please Select Simple QC & Validation SubType To Run")
            
            if getSimpleQCValidationCheck == ListSimpleQCCheck[1]:
                print('Start TimeStamp : ' + str(Default_Date_today))
                print('Running QC Check : '+ getSimpleQCValidationCheck)
                RunSimpleLookupTableValidationCheck_C_1()
                print('Finish Running QC Check :'+ getSimpleQCValidationCheck)
                print('End TimeStamp : ' + str(Default_Date_today + pd.DateOffset(seconds=40)))
            
            if getSimpleQCValidationCheck == ListSimpleQCCheck[2]:
                print('Start TimeStamp : ' + str(Default_Date_today))
                print('Running QC Check :'+ getSimpleQCValidationCheck)
                RunSimpleRangeValidationCheck_C_2()
                print('Finish Running QC Check :'+ getSimpleQCValidationCheck)
                print('End TimeStamp : ' + str(Default_Date_today + pd.DateOffset(seconds=80)))
            
            if getSimpleQCValidationCheck == ListSimpleQCCheck[3]:
                print('Start TimeStamp : ' + str(Default_Date_today))
                print('Running QC Check :'+ getSimpleQCValidationCheck)
                RunSimplePresenceValidationCheck_C_3()
                print('Finish Running QC Check :'+ getSimpleQCValidationCheck)
                print('End TimeStamp : ' + str(Default_Date_today + pd.DateOffset(seconds=100)))
            
            if getSimpleQCValidationCheck == ListSimpleQCCheck[4]:
                print('Start TimeStamp : ' + str(Default_Date_today))
                print('Running QC Check :'+ getSimpleQCValidationCheck)
                RunSimpleLogicalValidationCheck_C_4()
                print('Finish Running QC Check :'+ getSimpleQCValidationCheck)
                print('End TimeStamp : ' + str(Default_Date_today + pd.DateOffset(seconds=60)))
            
            if getSimpleQCValidationCheck == ListSimpleQCCheck[5]:
                print('Start TimeStamp : ' + str(Default_Date_today))
                print('Running QC Check :'+ getSimpleQCValidationCheck)
                RunSimpleConsistencyValidationCheck_C_5()
                print('Finish Running QC Check :'+ getSimpleQCValidationCheck)
                print('End TimeStamp : ' + str(Default_Date_today + pd.DateOffset(seconds=80)))

        def ViewSimpleQCValidationCheck():
            ListSimpleQCCheck = ['Select Simple QC & Validation SubType',
                '1: Simple Table Lookup & Validation Check',
                '2: Simple Range & Validation Check',
                '3: Simple Presence & Validation Check',
                '4: Simple Logical & Validation Check',
                '5: Simple Consistency & Validation Check']
            getSimpleQCValidationCheck = entry_VarListSimpleQCCheck.get()
            if getSimpleQCValidationCheck == ListSimpleQCCheck[0]:
                tkinter.messagebox.showinfo("View Simple QC Validation Message","Please Select Simple QC & Validation SubType To View Results")
            if getSimpleQCValidationCheck == ListSimpleQCCheck[1]:
                ViewSimpleLookupTableValidationResult_C_1()
            if getSimpleQCValidationCheck == ListSimpleQCCheck[2]:
                ViewSimpleRangeValidationResult_C_2()
            if getSimpleQCValidationCheck == ListSimpleQCCheck[3]:
                ViewSimplePresenceValidationResult_C_3()
            if getSimpleQCValidationCheck == ListSimpleQCCheck[4]:
                ViewSimpleLogicalValidationResult_C_4()
            if getSimpleQCValidationCheck == ListSimpleQCCheck[5]:
                ViewSimpleConsistencyValidationResult_C_5()

        def ViewSimpleLookupTableValidationResult_C_1():
            DFO_NL_ASOP_SetCatch_ViewLookupTableValidatedResult.SetCatch_ViewLookupTableValidatedResult()

        def RunSimpleLookupTableValidationCheck_C_1():
            ReturnPassedMessage = "All Passed"
            DisplayvalidationMsg = DFO_NL_ASOP_SetCatch_RunLookUpTableValidation.SetCatch_RunLookUpTableValidation()
            DisplayvalidationMsg = DisplayvalidationMsg[0]
            if DisplayvalidationMsg == ReturnPassedMessage:
                txtSimpleDisplayvalidationMsg.delete(0,END)
                txtSimpleDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
                txtSimpleDisplayvalidationMsg.config(fg='green')
            else:
                txtSimpleDisplayvalidationMsg.delete(0,END)
                txtSimpleDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
                txtSimpleDisplayvalidationMsg.config(fg='red')

        def ViewSimpleRangeValidationResult_C_2():
            DFO_NL_ASOP_SetCatch_ViewRangeValidatedResult.SetCatch_ViewRangeVariablesValidatedResult()

        def RunSimpleRangeValidationCheck_C_2():
            ReturnPassedMessage = "All Passed"
            DisplayvalidationMsg = DFO_NL_ASOP_SetCatch_RunRangeValidation.SetCatch_VariableRangeValidation()
            DisplayvalidationMsg = DisplayvalidationMsg[0]
            if DisplayvalidationMsg == ReturnPassedMessage:
                txtSimpleDisplayvalidationMsg.delete(0,END)
                txtSimpleDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
                txtSimpleDisplayvalidationMsg.config(fg='green')
            else:
                txtSimpleDisplayvalidationMsg.delete(0,END)
                txtSimpleDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
                txtSimpleDisplayvalidationMsg.config(fg='red')
        
        def ViewSimplePresenceValidationResult_C_3():
            DFO_NL_ASOP_SetCatch_ViewPresenceValidatedResult.SetCatch_ViewPresenceValidatedResult()

        def RunSimplePresenceValidationCheck_C_3():
            ReturnPassedMessage = "All Passed"
            DisplayvalidationMsg = DFO_NL_ASOP_SetCatch_RunPresenceValidation.SetCatch_VariablePresenceValidation()
            DisplayvalidationMsg = DisplayvalidationMsg[0]
            if DisplayvalidationMsg == ReturnPassedMessage:
                txtSimpleDisplayvalidationMsg.delete(0,END)
                txtSimpleDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
                txtSimpleDisplayvalidationMsg.config(fg='green')
            else:
                txtSimpleDisplayvalidationMsg.delete(0,END)
                txtSimpleDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
                txtSimpleDisplayvalidationMsg.config(fg='red') 
        
        def ViewSimpleLogicalValidationResult_C_4():
            DFO_NL_ASOP_SetCatch_ViewLogicalValidatedResult.SetCatch_ViewLogicalValidatedResult()

        def RunSimpleLogicalValidationCheck_C_4():
            ReturnPassedMessage = "All Passed"
            DisplayvalidationMsg = DFO_NL_ASOP_SetCatch_RunLogicalValidation.SetCatch_VariableLogicalValidation()
            DisplayvalidationMsg = DisplayvalidationMsg[0]
            if DisplayvalidationMsg == ReturnPassedMessage:
                txtSimpleDisplayvalidationMsg.delete(0,END)
                txtSimpleDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
                txtSimpleDisplayvalidationMsg.config(fg='green')
            else:
                txtSimpleDisplayvalidationMsg.delete(0,END)
                txtSimpleDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
                txtSimpleDisplayvalidationMsg.config(fg='red')

        def ViewSimpleConsistencyValidationResult_C_5():
            DFO_NL_ASOP_SetCatch_ViewConsistencyValidatedResult.SetCatch_ViewConsistencyValidatedResult()

        def RunSimpleConsistencyValidationCheck_C_5():
            ReturnPassedMessage = "All Passed"
            DisplayvalidationMsg = DFO_NL_ASOP_SetCatch_RunConsistencyValidation.SetCatch_VariableConsistencyValidation()
            DisplayvalidationMsg = DisplayvalidationMsg[0]
            if DisplayvalidationMsg == ReturnPassedMessage:
                txtSimpleDisplayvalidationMsg.delete(0,END)
                txtSimpleDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
                txtSimpleDisplayvalidationMsg.config(fg='green')
            else:
                txtSimpleDisplayvalidationMsg.delete(0,END)
                txtSimpleDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
                txtSimpleDisplayvalidationMsg.config(fg='red')

        ## Define Functions For Run Integrated QC Check On Module - D
        def RunIntegratedQCValidationCheck():
            ListIntegratedQCCheck = ['Select Integrated QC & Validation SubType',
                '1: Integrated Table Lookup & Validation Check',
                '2: Integrated Range & Validation Check',
                '3: Integrated Calculation & Validation Check',
                '4: Integrated Logical & Validation Check',
                '5: Integrated Consistency & Validation Check']
            
            getIntegratedQCValidationCheck = entry_VarListIntegratedQCCheck.get()
            
            if getIntegratedQCValidationCheck == ListIntegratedQCCheck[0]:
                tkinter.messagebox.showinfo("Run Integrated QC Validation Message","Please Select Integrated QC & Validation SubType To Run")
            
            if getIntegratedQCValidationCheck == ListIntegratedQCCheck[1]:
                print('Start TimeStamp : ' + str(Default_Date_today))
                print('Running QC Check : '+ getIntegratedQCValidationCheck)
                #RunIntegratedLookupTableValidationCheck_C_1()
                print('Finish Running QC Check :'+ getIntegratedQCValidationCheck)
                print('End TimeStamp : ' + str(Default_Date_today + pd.DateOffset(seconds=40)))
            
            if getIntegratedQCValidationCheck == ListIntegratedQCCheck[2]:
                print('Start TimeStamp : ' + str(Default_Date_today))
                print('Running QC Check :'+ getIntegratedQCValidationCheck)
                RunIntegratedRangeValidationCheck_D_2()
                print('Finish Running QC Check :'+ getIntegratedQCValidationCheck)
                print('End TimeStamp : ' + str(Default_Date_today + pd.DateOffset(seconds=80)))
            
            if getIntegratedQCValidationCheck == ListIntegratedQCCheck[3]:
                print('Start TimeStamp : ' + str(Default_Date_today))
                print('Running QC Check :'+ getIntegratedQCValidationCheck)
                RunIntegratedCalculationValCheck_D_3()
                print('Finish Running QC Check :'+ getIntegratedQCValidationCheck)
                print('End TimeStamp : ' + str(Default_Date_today + pd.DateOffset(seconds=100)))
            
            if getIntegratedQCValidationCheck == ListIntegratedQCCheck[4]:
                print('Start TimeStamp : ' + str(Default_Date_today))
                print('Running QC Check :'+ getIntegratedQCValidationCheck)
                #RunIntegratedLogicalValidationCheck_C_4()
                print('Finish Running QC Check :'+ getIntegratedQCValidationCheck)
                print('End TimeStamp : ' + str(Default_Date_today + pd.DateOffset(seconds=60)))
            
            if getIntegratedQCValidationCheck == ListIntegratedQCCheck[5]:
                print('Start TimeStamp : ' + str(Default_Date_today))
                print('Running QC Check :'+ getIntegratedQCValidationCheck)
                #RunIntegratedConsistencyValidationCheck_C_5()
                print('Finish Running QC Check :'+ getIntegratedQCValidationCheck)
                print('End TimeStamp : ' + str(Default_Date_today + pd.DateOffset(seconds=80)))
        
        def ViewIntegratedQCValidationCheck():
            ListIntegratedQCCheck = ['Select Integrated QC & Validation SubType',
                '1: Integrated Table Lookup & Validation Check',
                '2: Integrated Range & Validation Check',
                '3: Integrated Calculation & Validation Check',
                '4: Integrated Logical & Validation Check',
                '5: Integrated Consistency & Validation Check']
            getIntegratedQCValidationCheck = entry_VarListIntegratedQCCheck.get()
            if getIntegratedQCValidationCheck == ListIntegratedQCCheck[0]:
                tkinter.messagebox.showinfo("View Integrated QC Validation Message","Please Select Integrated QC & Validation SubType To View Results")
            if getIntegratedQCValidationCheck == ListIntegratedQCCheck[1]:
                pass
            if getIntegratedQCValidationCheck == ListIntegratedQCCheck[2]:
                ViewIntegratedRangeValidationResult_D_2()
            if getIntegratedQCValidationCheck == ListIntegratedQCCheck[3]:
                ViewIntegratedCalculationValCheck_D_3()
            if getIntegratedQCValidationCheck == ListIntegratedQCCheck[4]:
                pass
            if getIntegratedQCValidationCheck == ListIntegratedQCCheck[5]:
                pass
        
        def ViewIntegratedRangeValidationResult_D_2():
            DFO_NL_ASOP_SetCatch_ViewIntegratedRangeResult.SetCatch_ViewIntegratedRangeResult()

        def RunIntegratedRangeValidationCheck_D_2():
            ReturnPassedMessage = "All Passed"
            DisplayvalidationMsg = DFO_NL_ASOP_SetCatch_RunIntegratedRangeValidation.SetCatch_IntegratedVariableRangeValidation()
            DisplayvalidationMsg = DisplayvalidationMsg[0]
            if DisplayvalidationMsg == ReturnPassedMessage:
                txtIntegratedDisplayvalidationMsg.delete(0,END)
                txtIntegratedDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
                txtIntegratedDisplayvalidationMsg.config(fg='green')
            else:
                txtIntegratedDisplayvalidationMsg.delete(0,END)
                txtIntegratedDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
                txtIntegratedDisplayvalidationMsg.config(fg='red')
        
        def ViewIntegratedCalculationValCheck_D_3():
            DFO_NL_ASOP_SetCatch_ViewIntegratedAreaCalcResult.SetCatch_ViewIntegratedCalcResult()

        def RunIntegratedCalculationValCheck_D_3():
            ReturnPassedMessage = "All Passed"
            DisplayvalidationMsg = DFO_NL_ASOP_SetCatch_RunIntegratedAreaCalValidation.SetCatch_IntegratedAreaCalcValidation()
            DisplayvalidationMsg = DisplayvalidationMsg[0]
            if DisplayvalidationMsg == ReturnPassedMessage:
                txtIntegratedDisplayvalidationMsg.delete(0,END)
                txtIntegratedDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
                txtIntegratedDisplayvalidationMsg.config(fg='green')
            else:
                txtIntegratedDisplayvalidationMsg.delete(0,END)
                txtIntegratedDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
                txtIntegratedDisplayvalidationMsg.config(fg='red')
        
        ## Define Functions For Run Tombstone QC Check On Module - E
        def RunTombStonQCValidationCheck():
            print('Start TimeStamp : ' + str(Default_Date_today))
            print('Running QC Check :'+ 'Set&Catch TombstoneQC Check')
            RunTombSetDataValidationCheck_E_1()
            print('Finish Running QC Check :'+ 'Set&Catch TombstoneQC Check')
            print('End TimeStamp : ' + str(Default_Date_today + pd.DateOffset(seconds=80)))
        
        def RunTombSetDataValidationCheck_E_1():
            ReturnPassedMessage = "All Passed"
            DisplayvalidationMsg = DFO_NL_ASOP_SetCatch_RunTombstoneQCValidation.SetCatch_TombSetDataValidation()
            DisplayvalidationMsg = DisplayvalidationMsg[0]
            if DisplayvalidationMsg == ReturnPassedMessage:
                txtTombDisplayvalidationMsg.delete(0,END)
                txtTombDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
                txtTombDisplayvalidationMsg.config(fg='green')
            else:
                txtTombDisplayvalidationMsg.delete(0,END)
                txtTombDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
                txtTombDisplayvalidationMsg.config(fg='red')
        
        def ViewTombStonQCValidationCheck():
            DFO_NL_ASOP_SetCatch_ViewTombQCSetDataValResult.ViewTombQCSetDataFailResult()
        
        ## Define Function For Clear Message
        def Clear_ValidationMsg():
            DisplayvalidationMsg = "Validated QC Message"
            txtSimpleDisplayvalidationMsg.delete(0,END)
            txtSimpleDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
            txtSimpleDisplayvalidationMsg.config(fg='grey')
            txtIntegratedDisplayvalidationMsg.delete(0,END)
            txtIntegratedDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
            txtIntegratedDisplayvalidationMsg.config(fg='grey')
            txtTombDisplayvalidationMsg.delete(0,END)
            txtTombDisplayvalidationMsg.insert(tk.END,DisplayvalidationMsg)
            txtTombDisplayvalidationMsg.config(fg='grey')
        
        ## Define File Menue Functions
        def Add_Filemenu():
            self.menu = Menu(self.root)
            self.root.config(menu=self.menu)
            filemenu  = Menu(self.menu, tearoff=0)
            LookupTables = Menu(self.menu, tearoff=0)
            VariablesRange = Menu(self.menu, tearoff=0)
            CordinateArea = Menu(self.menu, tearoff=0)
            UpdateDeploymentUID = Menu(self.menu, tearoff=0)
            self.menu.add_cascade(label="File", menu=filemenu)        
            filemenu.add_command(label="Exit", font=("arial", 10,'bold'), command=iExit)
            
            self.menu.add_cascade(label="LookupTable", menu=LookupTables)
            sub_menu = Menu(LookupTables, tearoff=0)
            sub_menu.add_command(label="ASOC Coded Table", font=("arial", 9,'bold'), 
                                    command=DFO_NL_ASOP_LookupTable_ASOCCode.DFO_NL_ASOP_ASOC_Profile_Table)
            sub_menu.add_command(label="Country Coded Table", font=("arial", 9,'bold'), 
                                    command=DFO_NL_ASOP_LookupTable_Country.DFO_NL_ASOP_Country_Profile_Table)
            sub_menu.add_command(label="DataSource Coded Table", font=("arial", 9,'bold'), 
                                    command=DFO_NL_ASOP_LookupTable_DataSource.DFO_NL_ASOP_DataSource_Profile_Table)
            sub_menu.add_command(label="GearDamage Coded Table", font=("arial", 9,'bold'), 
                                    command=DFO_NL_ASOP_LookupTable_GearDamage.DFO_NL_ASOP_GearDamage_Profile_Table)
            sub_menu.add_command(label="GearType Coded Table", font=("arial", 9,'bold'), 
                                    command=DFO_NL_ASOP_LookupTable_GearType.DFO_NL_ASOP_GearType_Profile_Table)
            sub_menu.add_command(label="Quota Coded Table", font=("arial", 9,'bold'), 
                                    command=DFO_NL_ASOP_LookupTable_Quota.DFO_NL_ASOP_Quota_Profile_Table)
            sub_menu.add_command(label="SetType Coded Table", font=("arial", 9,'bold'), 
                                    command=DFO_NL_ASOP_LookupTable_SetType.DFO_NL_ASOP_SetType_Profile_Table)
            sub_menu.add_command(label="SpeciesCode Coded Table", font=("arial", 9,'bold'), 
                                    command=DFO_NL_ASOP_LookupTable_SpeciesCode.DFO_NL_ASOP_SpeciesCode_Profile_Table)
            sub_menu.add_command(label="VesselClass Coded Table", font=("arial", 9,'bold'), 
                                    command=DFO_NL_ASOP_LookupTable_VesselClass.DFO_NL_ASOP_VesselClass_Profile_Table)
            sub_menu.add_command(label="NAFODivision Coded Table", font=("arial", 9,'bold'), 
                                    command=DFO_NL_ASOP_LookupTable_NAFODivision.DFO_NL_ASOP_NAFODivision_Profile_Table)
            
            LookupTables.add_cascade(label="All Lookup Table Modules",menu=sub_menu , font=("arial", 9,'bold'))
            LookupTables.add_command(label="Generate All LookUp Table Code Data", font=("arial", 9,'bold'), 
                                    command=DFO_NL_ASOP_GenAll_LookupTables.DFO_NL_ASOP_Generate_All_LookupTables)
            LookupTables.add_command(label="Clear All LookUp Table Code Data", font=("arial", 9,'bold'), 
                                    command=DFO_NL_ASOP_GenAll_LookupTables.DFO_NL_ASOP_Clear_All_LookupTables)
            
            self.menu.add_cascade(label="VariableRange", menu=VariablesRange)
            VariablesRange.add_command(label="View & Define QC Variables Range", font=("arial", 9,'bold'), 
                                    command=DFO_NL_ASOP_RangeVariables_ValidationTable.DFO_NL_ASOP_VariablesRangeProfile)
            
            self.menu.add_cascade(label="AreaRange", menu=CordinateArea)
            CordinateArea.add_command(label="View & Define NAFO Coordinated Area", font=("arial", 9,'bold'), 
                                    command=DFO_NL_ASOP_NAFOAreaTable.DFO_NL_ASOP_NAFOProfile)
            
            self.menu.add_cascade(label="Update", menu=UpdateDeploymentUID)
            UpdateDeploymentUID.add_command(label="Update DeploymentUID After Year/ASOCCode/DeploymentNumber/SetNumber Update", font=("arial", 9,'bold'), 
                                    command=UpdateDeploymentUIDAfterUpdate)

        ## Define Functions For System Display 
        def ConnectToSetCatchAnalysisDB():
            txtCurrentEntriesDB.delete(0,END)
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT")
                Len_Complete_df = len(cursor.fetchall())
                txtCurrentEntriesDB.insert(tk.END,Len_Complete_df)
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()
                    return Len_Complete_df
        
        def GetPickledImportedFileName():
            Len_Complete_df = ConnectToSetCatchAnalysisDB()
            if Len_Complete_df > 0:
                txtCurrentImportedFileName.delete(0,END)
                try:
                    with open(Pickle_FileNameImport, 'rb') as f:
                        FileNameImport = pickle.load(f)
                        txtCurrentImportedFileName.insert(tk.END,FileNameImport)
                except:
                    txtCurrentImportedFileName.insert(tk.END,'FileName.pickle Lost, Please Import CSV To Create Pickle File Name')
            else:
                txtCurrentImportedFileName.insert(tk.END,'Empty DB')

        def Refresh():
            ConnectToSetCatchAnalysisDB()
            GetPickledImportedFileName()

        def ExportSetAndCatch_QC_DB():
            ListExportOption = ['Overwrite','Append']
            get_ExportOption = (entry_ExportOptionList.get())
            if get_ExportOption == ListExportOption[0]:
                try:
                    conn = sqlite3.connect(DB_Set_Catch_Analysis)
                    cursor = conn.cursor()
                    Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", conn)
                    ListColumns = Complete_df.columns
                    Complete_df = Complete_df.iloc[:, 3:len(list(Complete_df.columns))]
                    Complete_df = Complete_df.replace('None', '')
                    Complete_df.sort_values(by=['Year', 'ASOCCode', 
                        'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
                    if len(Complete_df) >0:
                        Export_MasterTB_DF  = pd.DataFrame(Complete_df)
                        Export_MasterTB_DF  = Export_MasterTB_DF.reset_index(drop=True)
                        filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                                defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                        if len(filename) >0:
                            Export_MasterTB_DF.to_csv(filename,index=None)
                            tkinter.messagebox.showinfo("Set And Catch QC Database Profile Message",
                                "Set And Catch QC Database Profile Report Saved as CSV - Overwrite Mode")
                        else:
                            tkinter.messagebox.showinfo("Set And Catch QC Database Profile Message",
                                "Please Select File Name To Export")
                    else:
                        messagebox.showerror('Export Error : Set And Catch QC Database Profile Message', 
                                "Void File... Nothing to Export")
                except sqlite3.Error as error:
                    print('Error occured - ', error)
                finally:
                    if conn:
                        cursor.close()
                        conn.close()

            if get_ExportOption == ListExportOption[1]:
                try:
                    conn = sqlite3.connect(DB_Set_Catch_Analysis)
                    cursor = conn.cursor()
                    Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", conn)
                    ListColumns = Complete_df.columns
                    Complete_df = Complete_df.iloc[:, 3:len(list(Complete_df.columns))]
                    Complete_df = Complete_df.replace('None', '')
                    Complete_df.sort_values(by=['Year', 'ASOCCode', 
                        'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
                    if len(Complete_df) >0:
                        Export_MasterTB_DF  = pd.DataFrame(Complete_df)
                        Export_MasterTB_DF  = Export_MasterTB_DF.reset_index(drop=True)
                        filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                                defaultextension='.csv', confirmoverwrite=False,
                                filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                        if len(filename) >0:
                            output_path = filename
                            print(filename)
                            Export_MasterTB_DF.to_csv(output_path, index=None, mode='a', 
                                header=not os.path.exists(output_path))
                            # Export_MasterTB_DF.to_csv(filename,index=None)
                            tkinter.messagebox.showinfo("Set And Catch QC Database Profile Message",
                                "Set And Catch QC Database Profile Report Saved as CSV- Append Mode")
                        else:
                            tkinter.messagebox.showinfo("Set And Catch QC Database Profile Message",
                                "Please Select Appended File Name To Export")
                    else:
                        messagebox.showerror('Export Error : Set And Catch QC Database Profile Message', 
                                "Void File... Nothing to Export")
                except sqlite3.Error as error:
                    print('Error occured - ', error)
                finally:
                    if conn:
                        cursor.close()
                        conn.close()

        def iExit():
            iExit= tkinter.messagebox.askyesno("Exit DFO-NL ASOP Module", "Confirm If You Want To Exit")
            if iExit >0:
                self.root.destroy()
            return

        def UpdateDeploymentUIDAfterUpdate():
            DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
            def GetSetCatchProfileDB():
                try:
                    conn = sqlite3.connect(DB_Set_Catch_Analysis)
                    cursor = conn.cursor()
                    Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                    if len(Complete_df) >0:
                        SetCatchQCFailedDB_DF  = pd.DataFrame(Complete_df)
                        SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,['DataBase_ID','RecordIdentifier',
                                                                            'Year','ASOCCode','DeploymentNumber',
                                                                            'SetNumber']]
                        SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.replace(np.nan, 99999999)
                        SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.replace('', 99999999)
                        SetCatchQCFailedDB_DF[['DataBase_ID','RecordIdentifier',
                                                'Year','ASOCCode','DeploymentNumber',
                                                'SetNumber']] = SetCatchQCFailedDB_DF[
                                                ['DataBase_ID','RecordIdentifier',
                                                'Year','ASOCCode','DeploymentNumber',
                                                'SetNumber']].astype(int)
                        SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.replace(99999999, '')
                        SetCatchQCFailedDB_DF['DeploymentUID'] = SetCatchQCFailedDB_DF["Year"].map(str) + "-" + \
                                                                SetCatchQCFailedDB_DF["ASOCCode"].map(str)+ "-" +\
                                                                SetCatchQCFailedDB_DF["DeploymentNumber"].map(str)+"-"+ \
                                                                SetCatchQCFailedDB_DF["SetNumber"].map(str)
                        SetCatchQCFailedDB_DF = SetCatchQCFailedDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                                            'Year','ASOCCode','DeploymentNumber',
                                                                            'SetNumber']]
                    
                        SetCatchQCFailedDB_DF  = SetCatchQCFailedDB_DF.reset_index(drop=True)
                        SetCatchQCFailedDB_DF  = pd.DataFrame(SetCatchQCFailedDB_DF)
                        return SetCatchQCFailedDB_DF
                    else:
                        return Complete_df
                except sqlite3.Error as error:
                    print('Error occured - ', error)
                finally:
                    if conn:
                        cursor.close()
                        conn.close()
            ## Get Set And Catch DB Profile
            SetCatchQCFailedDB_DF = GetSetCatchProfileDB()
            UpdateRecordList_SetCatchDB =[]
            df_rows = SetCatchQCFailedDB_DF.to_numpy().tolist()
            for row in df_rows:
                rowValue = row
                list_item_DataBase_ID = int(rowValue[0])
                list_item_RecordIdentifier = int(rowValue[1])
                list_item_DeploymentUID = (rowValue[2])
                list_item_Year = (rowValue[3])
                list_item_ASOCCode = (rowValue[4])
                list_item_DeploymentNumber = (rowValue[5])
                list_item_SetNumber = (rowValue[6])
                UpdateRecordList_SetCatchDB.append((
                            list_item_DeploymentUID,
                            list_item_Year,
                            list_item_ASOCCode,
                            list_item_DeploymentNumber,
                            list_item_SetNumber,
                            list_item_DataBase_ID,
                            list_item_RecordIdentifier,
                            ))
            ## DB Update Executing
            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
            cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
            cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentUID =?, Year = ?, \
                                                ASOCCode = ?, DeploymentNumber = ?, SetNumber = ?\
                                                WHERE DataBase_ID =? AND RecordIdentifier =?", 
                                                UpdateRecordList_SetCatchDB)
            conn_DB_Set_Catch_Analysis.commit()
            conn_DB_Set_Catch_Analysis.close()
            tkinter.messagebox.showinfo("DeploymentUID Update","DeploymentUID Update Successfully")

        ## Define Functions For Import Set&Catch DB On Module - A
        def Import_SetCatch_CSV():
            DFO_NL_ASOP_Set_Catch_Import_CSV.Observer_Set_Catch_LogIMPORT()

        ## Define Functions For View Edit Update Search Set&Catch DB On Module - B
        def ViewEditUpdateExportDB_TreeViewModules():
            Len_Complete_df = ConnectToSetCatchAnalysisDB()
            if Len_Complete_df > 0:
                print("Application B-1 is Loading ..... Please Wait....")
                DFO_NL_ASOP_TreeViewDatabaseQCAnalysis_SetCatch.TreeViewDB_QCAnalysis_SetCatch()
            else:
                tkinter.messagebox.showinfo("Empty Set&Catch DB","Empty Set&Catch DB, Please Import Set&Catch CSV File To View")

        def ViewOnlyDB_ExcelViewModules():
            Len_Complete_df = ConnectToSetCatchAnalysisDB()
            if Len_Complete_df > 0:
                print("Application B-2 is Loading ..... Please Wait....")
                DFO_NL_ASOP_ExcelViewDatabaseQCAnalysis_SetCatch.ExcelViewDB_QCAnalysis_SetCatch()
            else:
                tkinter.messagebox.showinfo("Empty Set&Catch DB","Empty Set&Catch DB, Please Import Set&Catch CSV File To View")

        ## Adding File Menu 
        Add_Filemenu()

        ## Adding Callback function Event
        def callbackFuncSelectVariable1(event):
            ListSimpleQCCheck = ['Select Simple QC & Validation SubType',
                    '1: Simple Table Lookup & Validation Check',
                    '2: Simple Range & Validation Check',
                    '3: Simple Presence & Validation Check',
                    '4: Simple Logical & Validation Check',
                    '5: Simple Consistency & Validation Check']
            getSimpleQCValidationCheck = entry_VarListSimpleQCCheck.get()
            print('Selected QC Check :'+ getSimpleQCValidationCheck)
            
            if (getSimpleQCValidationCheck == ListSimpleQCCheck[0]):
                txtSimpleDisplayvalidationMsg.delete(0,END)
                txtSimpleDisplayvalidationMsg.insert(tk.END,'Select QC SubType & Run')
                txtSimpleDisplayvalidationMsg.config(fg='grey')
            
            if (getSimpleQCValidationCheck == ListSimpleQCCheck[1]):
                txtSimpleDisplayvalidationMsg.delete(0,END)
                txtSimpleDisplayvalidationMsg.insert(tk.END,'1: Run Table Lookup Check')
                txtSimpleDisplayvalidationMsg.config(fg='black')
            
            if (getSimpleQCValidationCheck == ListSimpleQCCheck[2]):
                txtSimpleDisplayvalidationMsg.delete(0,END)
                txtSimpleDisplayvalidationMsg.insert(tk.END,'2: Run Range Check')
                txtSimpleDisplayvalidationMsg.config(fg='black')
            
            if (getSimpleQCValidationCheck == ListSimpleQCCheck[3]):
                txtSimpleDisplayvalidationMsg.delete(0,END)
                txtSimpleDisplayvalidationMsg.insert(tk.END,'3: Run Presence Check')
                txtSimpleDisplayvalidationMsg.config(fg='black')
            
            if (getSimpleQCValidationCheck == ListSimpleQCCheck[4]):
                txtSimpleDisplayvalidationMsg.delete(0,END)
                txtSimpleDisplayvalidationMsg.insert(tk.END,'4: Run Logical Check')
                txtSimpleDisplayvalidationMsg.config(fg='black')
            
            if (getSimpleQCValidationCheck == ListSimpleQCCheck[5]):
                txtSimpleDisplayvalidationMsg.delete(0,END)
                txtSimpleDisplayvalidationMsg.insert(tk.END,'5: Run Consistency Check')
                txtSimpleDisplayvalidationMsg.config(fg='black')
        
        def callbackFuncSelectVariable2(event):
            ListIntegratedQCCheck = ['Select Integrated QC & Validation SubType',
                '1: Integrated Table Lookup & Validation Check',
                '2: Integrated Range & Validation Check',
                '3: Integrated Calculation & Validation Check',
                '4: Integrated Logical & Validation Check',
                '5: Integrated Consistency & Validation Check']
            getIntegratedQCValidationCheck = entry_VarListIntegratedQCCheck.get()
            print('Selected QC Check :'+ getIntegratedQCValidationCheck)
            
            if (getIntegratedQCValidationCheck == ListIntegratedQCCheck[0]):
                txtIntegratedDisplayvalidationMsg.delete(0,END)
                txtIntegratedDisplayvalidationMsg.insert(tk.END,'Select QC SubType & Run')
                txtIntegratedDisplayvalidationMsg.config(fg='grey')
            
            if (getIntegratedQCValidationCheck == ListIntegratedQCCheck[1]):
                txtIntegratedDisplayvalidationMsg.delete(0,END)
                txtIntegratedDisplayvalidationMsg.insert(tk.END,'Under Construction - 1: Run Table Lookup Check')
                txtIntegratedDisplayvalidationMsg.config(fg='Red')
            
            if (getIntegratedQCValidationCheck == ListIntegratedQCCheck[2]):
                txtIntegratedDisplayvalidationMsg.delete(0,END)
                txtIntegratedDisplayvalidationMsg.insert(tk.END,'2: Run Range Check')
                txtIntegratedDisplayvalidationMsg.config(fg='black')
            
            if (getIntegratedQCValidationCheck == ListIntegratedQCCheck[3]):
                txtIntegratedDisplayvalidationMsg.delete(0,END)
                txtIntegratedDisplayvalidationMsg.insert(tk.END,'3: Run Calculation Check')
                txtIntegratedDisplayvalidationMsg.config(fg='black')
            
            if (getIntegratedQCValidationCheck == ListIntegratedQCCheck[4]):
                txtIntegratedDisplayvalidationMsg.delete(0,END)
                txtIntegratedDisplayvalidationMsg.insert(tk.END,'Under Construction - 4: Run Logical Check')
                txtIntegratedDisplayvalidationMsg.config(fg='Red')
            
            if (getIntegratedQCValidationCheck == ListIntegratedQCCheck[5]):
                txtIntegratedDisplayvalidationMsg.delete(0,END)
                txtIntegratedDisplayvalidationMsg.insert(tk.END,'Under Construction - 5: Run Consistency Check')
                txtIntegratedDisplayvalidationMsg.config(fg='Red')
        
        
        ## ************ DFO_NL_ASOP_Set & Catch Module - Import ............... Sec : A ********************
        label_Set_Catch_Import = Label(DataFrameLEFT, text = "A: External Import Modules:", justify ="left",
                font=("arial", 12,'bold'), fg = 'blue', bg= "ghost white", padx= 1, pady= 2, underline =0)
        label_Set_Catch_Import.grid(row=2,column=0, sticky =W , padx= 2, pady= 2)
        ## Buttons
        btnImport_Set_Catch = Button(DataFrameLEFT, text="Import Set & Catch CSV File", font=('aerial', 10, 'bold'),
                bg= "ghost white" , height =1, width=26, bd=2, padx= 1, pady= 1, 
                command = Import_SetCatch_CSV)
        
        btnImport_Set_Catch.grid(row = 3, column=0, sticky =W , padx= 20, pady= 2, ipady =2)

        ##  ************ DFO_NL_ASOP_Set & Catch Module - View, Edit, Update Export ............... Sec : B  ************
        label_ViewEditUpdateExportDBModules = Label(DataFrameLEFT, text = "B: View Edit Update & Export DB Modules:", justify ="left",
                   font=("arial", 12,'bold'), fg = 'blue', bg= "ghost white", padx= 1, pady= 2, underline =0)
        label_ViewEditUpdateExportDBModules.grid(row=6,column=0, sticky =W , padx= 2, pady= 6, ipady =1)

        label_ViewEditUpdateExportDB_TreeViewModules = Label(DataFrameLEFT, text = "1: View/Edit/Update/Export Set & Catch DB:", justify ="left", 
                             font=("arial", 10,'bold'), fg = 'blue', bg= "ghost white", padx= 1, pady= 2, underline =0)
        label_ViewEditUpdateExportDB_TreeViewModules.grid(row=7,column=0, sticky =W , padx= 10, pady= 1)

        label_ViewOnlyDB_ExcelViewModules = Label(DataFrameLEFT, text = "2: View Only & Export Set & Catch DB:", justify ="left", 
                             font=("arial", 10,'bold'), fg = 'blue', bg= "ghost white", padx= 1, pady= 2, underline =0)
        label_ViewOnlyDB_ExcelViewModules.grid(row=9,column=0, sticky =W , padx= 10, pady= 2)

        label_CurrentImportedFileName = Label(DataFrameLEFT, text = " 1. Current Imported File Name :", justify ="left",
                    font=("arial", 10,'bold'), fg = 'blue', bg= "ghost white", padx= 1, pady= 2)
        label_CurrentImportedFileName.grid(row=14,column=0, sticky =W , padx= 10, pady= 1, ipady =1)

        CurrentImportedFileName = StringVar(DataFrameLEFT, value="")
        txtCurrentImportedFileName = Entry(DataFrameLEFT, font=('aerial', 10),
                    textvariable = CurrentImportedFileName, width = 30)
        txtCurrentImportedFileName.grid(row =16, column = 0, padx=40, pady =2, ipady=2, sticky =W)
        txtCurrentImportedFileName.config(fg='grey')

        btnUpdateRefresh = Button(DataFrameLEFT, text="Refresh", font=('aerial', 10),
                bg= "ghost white" , height =1, width=8, bd=1, padx= 1, pady= 5,
                command = Refresh)
        btnUpdateRefresh.grid(row = 16, column=0, sticky =E , padx= 2, pady= 1)

        label_NB = Label(DataFrameLEFT, text = "(N.B: Hit Refreash After Import To Update FileName)", justify ="left",
                   font=("arial", 8,'bold'), fg = 'blue', bg= "ghost white", padx= 1, pady= 2)
        label_NB.grid(row=17,column=0, sticky =W , padx= 10, pady= 1, ipady =1)

        label_CurrentEntriesDB = Label(DataFrameLEFT, text = " 2. Total Database Entries :", justify ="left",
                   font=("arial", 10,'bold'), fg = 'blue', bg= "ghost white", padx= 1, pady= 2)
        label_CurrentEntriesDB.grid(row=18,column=0, sticky =W , padx= 10, pady= 1, ipady =1)

        CurrentEntriesDB = IntVar(DataFrameLEFT, value="")
        txtCurrentEntriesDB = Entry(DataFrameLEFT, font=('aerial', 10),textvariable = CurrentEntriesDB, width = 9)
        txtCurrentEntriesDB.grid(row =18, column = 0, padx=80, pady =2, ipady=2, sticky =E)
        txtCurrentEntriesDB.config(fg='grey')

        btnUExportDB = Button(DataFrameLEFT, text="Export Set & Catch For Archive", font=('aerial', 10, 'bold'),
                              bg= "ghost white" , height =1, width=26, bd=2, padx= 1, pady= 5,
                              command = ExportSetAndCatch_QC_DB)
        btnUExportDB.grid(row = 24, column=0, sticky =W , padx= 20, pady= 4)

        ListExportOption = ['Overwrite','Append']
        entry_ExportOptionList  = ttk.Combobox(DataFrameLEFT, font=('aerial', 10, 'bold'), justify = tk.LEFT,
                                            textvariable =ListExportOption, width = 10, state='readonly')
        entry_ExportOptionList.grid(row =24, column = 0, padx=1, pady =4, ipady= 2, sticky =E)
        entry_ExportOptionList['values'] = ListExportOption
        entry_ExportOptionList.current(0)

        ## Buttons
        btnViewEditUpdateExportDB_TreeViewModules = Button(DataFrameLEFT, text="View Edit Update & Export DB", font=('aerial', 10, 'bold'),
                              bg= "ghost white" , height =1, width=26, bd=2, padx= 1, pady= 5,
                              command = ViewEditUpdateExportDB_TreeViewModules)
        btnViewEditUpdateExportDB_TreeViewModules.grid(row = 8, column=0, sticky =W , padx= 20, pady= 4)

        btnViewOnlyDB_ExcelViewModules = Button(DataFrameLEFT, text="Excel View Only & Export DB", font=('aerial', 10, 'bold'),
                              bg= "ghost white" , height =1, width=26, bd=2, padx= 1, pady= 5,
                              command = ViewOnlyDB_ExcelViewModules)
        btnViewOnlyDB_ExcelViewModules.grid(row = 10, column=0, sticky =W , padx= 20, pady= 4)

        ##  ************ DFO_NL_ASOP_Set & Catch Module - Simple QC & Validation (Level One)........... Sec : C  ************
        label_SimpleQCvalidationLevel_1 = Label(DataFrameRIGHT, text = "C: Simple QC & Data Validation (Level One):",
                                         justify ="left", font=("arial", 12,'bold'), fg = 'blue', 
                                         bg= "ghost white", padx= 1, pady= 2, underline =0)
        label_SimpleQCvalidationLevel_1.grid(row=2,column=0, sticky =W , padx= 2, pady= 5)

        ListSimpleQCCheck = ['Select Simple QC & Validation SubType',
                             '1: Simple Table Lookup & Validation Check',
                             '2: Simple Range & Validation Check',
                             '3: Simple Presence & Validation Check',
                             '4: Simple Logical & Validation Check',
                             '5: Simple Consistency & Validation Check']
        entry_VarListSimpleQCCheck  = ttk.Combobox(DataFrameRIGHT, font=('aerial', 10, 'bold'), 
                                                    width = 45, state='readonly')
        entry_VarListSimpleQCCheck['values'] = ListSimpleQCCheck
        entry_VarListSimpleQCCheck.current(0)
        entry_VarListSimpleQCCheck.grid(row =4, column = 0, padx=20, pady =2, ipady= 4, sticky =W)

        SimpleDisplayvalidationMsg = StringVar(DataFrameRIGHT, value=" Validated QC Message")
        txtSimpleDisplayvalidationMsg = Entry(DataFrameRIGHT, font=('aerial', 10, 'bold'),textvariable = SimpleDisplayvalidationMsg, width = 30)
        txtSimpleDisplayvalidationMsg.grid(row =6, column = 0, padx=4, pady =2, ipady=5, sticky =E)
        txtSimpleDisplayvalidationMsg.config(fg='grey')
        
        ## Buttons
        btnRunSimpleQCVal = Button(DataFrameRIGHT, text="Run Simple QC Validation", font=('aerial', 10, 'bold'),
                                  bg= "ghost white" , height =1, width=22, bd=2, padx= 1, pady= 5, 
                                  command = RunSimpleQCValidationCheck)
        btnRunSimpleQCVal.grid(row = 6, column=0, sticky =W , padx= 20, pady= 4)

        btnViewSimpleQCValResults = Button(DataFrameRIGHT, text="View Validated QC Results", font=('aerial', 10, 'bold'),
                                            bg= "ghost white" , height =1, width=22, bd=2, padx= 1, pady= 5, 
                                            command = ViewSimpleQCValidationCheck)
        btnViewSimpleQCValResults.grid(row = 8, column=0, sticky =W , padx= 20, pady= 4)

        btnRunAllSimpleQC = Button(DataFrameRIGHT, text="Run All Simple QC", font=('aerial', 10, 'bold'),
                                  bg= "ghost white" , height =1, width=20, bd=2, padx= 1, pady= 5, 
                                  command = '')
        btnRunAllSimpleQC.grid(row = 8, column=0, sticky =E , padx= 2, pady= 4)

        # ***DFO_NL_ASOP_Set & Catch Module - Integrated QC & Validation (Level Two)..Sec : D  *****
        label_D_IntQCDataValLev2 = Label(DataFrameRIGHT, text = "D: Integrated QC & Data Validation (Level Two):",
                                         justify ="left", font=("arial", 12,'bold'), fg = 'blue', 
                                         bg= "ghost white", padx= 1, pady= 2, underline =0)
        label_D_IntQCDataValLev2.grid(row=12,column=0, sticky =W , padx= 2, pady= 5)

        ListIntegratedQCCheck = ['Select Integrated QC & Validation SubType',
                             '1: Integrated Table Lookup & Validation Check',
                             '2: Integrated Range & Validation Check',
                             '3: Integrated Calculation & Validation Check',
                             '4: Integrated Logical & Validation Check',
                             '5: Integrated Consistency & Validation Check']
        entry_VarListIntegratedQCCheck  = ttk.Combobox(DataFrameRIGHT, font=('aerial', 10, 'bold'), 
                                                    width = 45, state='readonly')
        entry_VarListIntegratedQCCheck['values'] = ListIntegratedQCCheck
        entry_VarListIntegratedQCCheck.current(0)
        entry_VarListIntegratedQCCheck.grid(row =14, column = 0, padx=20, pady =2, ipady= 4, sticky =W)

        IntegratedDisplayvalidationMsg = StringVar(DataFrameRIGHT, value=" Validated QC Message")
        txtIntegratedDisplayvalidationMsg = Entry(DataFrameRIGHT, font=('aerial', 10, 'bold'),textvariable = IntegratedDisplayvalidationMsg, width = 30)
        txtIntegratedDisplayvalidationMsg.grid(row =16, column = 0, padx=4, pady =2, ipady=5, sticky =E)
        txtIntegratedDisplayvalidationMsg.config(fg='grey')
        
        ## Buttons
        btnRunIntQCValidation = Button(DataFrameRIGHT, text="Run Integrated QC Validation", font=('aerial', 10, 'bold'),
                                  bg= "ghost white" , height =1, width=25, bd=2, padx= 1, pady= 5, 
                                  command = RunIntegratedQCValidationCheck)
        btnRunIntQCValidation.grid(row = 16, column=0, sticky =W , padx= 20, pady= 4)

        btnIntViewQCValResult = Button(DataFrameRIGHT, text="View Validated QC Results", font=('aerial', 10, 'bold'),
                                            bg= "ghost white" , height =1, width=25, bd=2, padx= 1, pady= 5, 
                                            command = ViewIntegratedQCValidationCheck)
        btnIntViewQCValResult.grid(row = 18, column=0, sticky =W , padx= 20, pady= 4)

        btnRunAllIntegratedQC = Button(DataFrameRIGHT, text="Run All Integrated QC", font=('aerial', 10, 'bold'),
                                  bg= "ghost white" , height =1, width=20, bd=2, padx= 1, pady= 5, 
                                  command = '')
        btnRunAllIntegratedQC.grid(row = 18, column=0, sticky =E , padx= 2, pady= 4)

        # ***DFO_NL_ASOP_Set & Catch Module - Tombstone QC & Validation (Level Three)..Sec : E  *****
        labelE_TombstoneQCVal_3 = Label(DataFrameRIGHT, text = "E: Tombstone QC & Set Data Validation (Level Three):",
                                         justify ="left", font=("arial", 12,'bold'), fg = 'blue', 
                                         bg= "ghost white", padx= 1, pady= 2, underline =0)
        labelE_TombstoneQCVal_3.grid(row=22,column=0, sticky =W , padx= 2, pady= 5)

        TombDisplayvalidationMsg = StringVar(DataFrameRIGHT, value=" Validated QC Message")
        txtTombDisplayvalidationMsg = Entry(DataFrameRIGHT, font=('aerial', 10, 'bold'),textvariable = TombDisplayvalidationMsg, width = 30)
        txtTombDisplayvalidationMsg.grid(row =24, column = 0, padx=4, pady =2, ipady=5, sticky =E)
        txtTombDisplayvalidationMsg.config(fg='grey')
        
        ## Buttons
        btnRunTombstoneQCValidation = Button(DataFrameRIGHT, text="Run Tombstone QC Validation", font=('aerial', 10, 'bold'),
                                  bg= "ghost white" , height =1, width=25, bd=2, padx= 1, pady= 5, 
                                  command = RunTombStonQCValidationCheck)
        btnRunTombstoneQCValidation.grid(row = 24, column=0, sticky =W , padx= 20, pady= 4)

        btnTombViewQCValResult = Button(DataFrameRIGHT, text="View Validated QC Results", font=('aerial', 10, 'bold'),
                                            bg= "ghost white" , height =1, width=25, bd=2, padx= 1, pady= 5, 
                                            command = ViewTombStonQCValidationCheck)
        btnTombViewQCValResult.grid(row = 26, column=0, sticky =W , padx= 20, pady= 4)

        btnIntClear_ValMsg = Button(DataFrameRIGHT, text="Clear Message", font=('aerial', 10, 'bold'),
                                  bg= "ghost white" , height =1, width=12, bd=2, padx= 1, pady= 5, 
                                  command = Clear_ValidationMsg)
        btnIntClear_ValMsg.grid(row = 26, column = 0, padx=4, pady =2, ipady=5, sticky =E)


        ## Running System Display Modules
        ConnectToSetCatchAnalysisDB()
        GetPickledImportedFileName()

        ## Combobox Select Event
        entry_VarListSimpleQCCheck.bind('<<ComboboxSelected>>', callbackFuncSelectVariable1)
        entry_VarListIntegratedQCCheck.bind('<<ComboboxSelected>>', callbackFuncSelectVariable2)

## Running Main 
if __name__ == '__main__':
    print("QC Main Version 0.1.0 is Loading .....Please Wait")
    root = Tk()
    application  = DFO_NL_ASOP_Module (root)
    print("QC Main Version 0.1.0 Loaded Successfully")
    root.mainloop()

from tkinter import *
import tkinter.messagebox
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import messagebox
import numpy as np
import sqlite3
import pandas as pd
from pandastable import Table, config

DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
DB_SetCatch_Validation_Range  = ("./BackEnd/Sqlite3_DB/QC_Check_RangeConsistency_DB/DFO_NL_ASOP_SetCatch_RangeValidation.db")
from QC_Modules.Set_and_Catch.IntegratedQC_VariableRangeValidation \
import DFO_NL_ASOP_SetCatch_RunIntegratedRangeValidation

def ViewRangeValidatedResult_TowDistance():
    windows = tk.Toplevel()
    windows.title ("DFO-NL-ASOP Range Validator - ID-D-02-0")
    windows.geometry('1560x875+40+40')
    windows.config(bg="cadet blue")

    HeaderFrame = tk.Frame(windows, width = 40,  bd = 2,relief = RIDGE, bg= "cadet blue")
    HeaderFrame.pack(side = TOP, padx= 0, pady=0)

    lbl_SortLabel = Label(HeaderFrame, font=('aerial', 11, 'bold'),
            bg= "cadet blue", text="Tow Difference QC Table : ")
    lbl_SortLabel.grid(row =0, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)
    ListVariableListA = ['DataBase_ID','RecordIdentifier','DeploymentUID',
                        'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
                        'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
                        'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
                        'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
                        'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
                        'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
                        'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                        'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                        'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
                        'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
                        'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                        'NumberIndividuals', '']
    SelColIndex       = StringVar(HeaderFrame, value ='Sort By Column Name')
    entry_SelectedSortVar  = ttk.Combobox(HeaderFrame, font=('aerial', 10, 'bold'), 
                                        textvariable = SelColIndex, width = 20, state='readonly')
    entry_SelectedSortVar.grid(row =0, column = 1, padx=2, pady =2, ipady =1, sticky =E)
    entry_SelectedSortVar['values'] = (list(ListVariableListA))

    lbl_TotalDBEntries = Label(HeaderFrame, font=('aerial', 11, 'bold'),
            bg= "cadet blue", text="Total DB Entries : ")
    lbl_TotalDBEntries.grid(row =0, column = 4, columnspan=1 ,padx=1, pady =2, sticky =W)
    EntryDBEntries       = IntVar(HeaderFrame, value ='')
    entry_DBEntries = Entry(HeaderFrame, font=('aerial', 10), justify='center',
                                textvariable = EntryDBEntries, width = 6, bd=2)
    entry_DBEntries.grid(row =0, column = 5, padx=2, pady =2, ipady =1, sticky =E)

    EntryFlagged       = IntVar(HeaderFrame, value ='')
    entry_Flagged = Entry(HeaderFrame, font=('aerial', 10), justify='center',
                                textvariable = EntryFlagged, width = 6, bd=2)
    entry_Flagged.grid(row =0, column = 9, padx=1, pady =2, ipady =1, sticky =E)

    frame = tk.Frame(windows)
    frame.pack(fill=BOTH, expand=1)

    def DeleteTempStorage():
        sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Range)
        cursor = sqliteConnection.cursor()
        Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_TempTowDistance;", sqliteConnection)
        length_Complete_df = len(Complete_df)
        if length_Complete_df > 0:
            cursor.execute("DELETE FROM SetCatch_QCFailedRange_TempTowDistance")
            sqliteConnection.commit()
            cursor.close()
            sqliteConnection.close()

    def get_ObserverSetCatchDB():
        try:
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = sqliteConnection.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_TowDistance;", sqliteConnection)
            length_Complete_df = len(Complete_df)
            if length_Complete_df > 0:
                Complete_df = Complete_df.reset_index(drop=True)
                ObserverSetCatchDB = pd.DataFrame(Complete_df)
                lengthFlagged = len(Complete_df[(Complete_df.TowDiffFlag) == 'Yes'])
                sqliteConnection.commit()
                return ObserverSetCatchDB, length_Complete_df, lengthFlagged
            else:
                messagebox.showerror('Set & Catch Database Is Empty', "Please Import Set & Catch CSV File To View")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()
    
    Return_ObserverSetCatchDB = get_ObserverSetCatchDB()
    ObserverSetCatchDB = Return_ObserverSetCatchDB[0]
    entry_DBEntries.insert(tk.END,Return_ObserverSetCatchDB[1])
    entry_Flagged.insert(tk.END,Return_ObserverSetCatchDB[2])
    DeleteTempStorage()
    ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                ['TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag',
				'DataBase_ID','RecordIdentifier','DeploymentUID',
				'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
				'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
				'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
				'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
				'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
				'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
				'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
				'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
				'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
				'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
				'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
				'NumberIndividuals']]
    ObserverSetCatchDB.sort_values(by=['Year', 'ASOCCode', 
        'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
    ObserverSetCatchDB['ViewDepUID'] = ObserverSetCatchDB.loc[:, 'DeploymentUID']
    ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
    ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)
    pt = Table(frame, dataframe = ObserverSetCatchDB, showtoolbar=True, showstatusbar=True)
    pt.setRowColors(rows=range(1,len(ObserverSetCatchDB),2), clr='lightblue', cols='all')
    pt.cellbackgr = 'aliceblue'
    options = config.load_options()
    options = { 'align': 'center',
                'cellbackgr': '#F4F4F3',
                'cellwidth': 120,
                'floatprecision': 2,
                'thousandseparator': '',
                'font': 'Arial',
                'fontsize': 8,
                'fontstyle': '',
                'grid_color': '#ABB1AD',
                'linewidth': 1,
                'rowheight': 22,
                'rowselectedcolor': '#E4DED4',
                'textcolor': 'black'}
    config.apply_options(options, pt)
    pt.autoResizeColumns()
    pt.prodyutCustomsetindex2_1()
    pt.show()
    
    ## Define Functions
    def SubmitToUpdateDB():
        Complete_df = pd.DataFrame(ObserverSetCatchDB)
        if len(Complete_df) >0:
            Complete_df  = pd.DataFrame(pt.model.df)
            Complete_df= (Complete_df.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID',
				'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
				'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
				'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
				'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
				'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
				'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
				'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
				'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
				'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
				'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
				'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
				'NumberIndividuals']]).replace(['', None, np.nan, 
                'None', ' ', '  ', '   ', '    '], 99999999)

            Complete_df[['DataBase_ID', 'RecordIdentifier', 'GearDamage',
                        'ASOCCode', 'Year', 'DeploymentNumber', 
                        'SetNumber', 'Country', 'Quota', 'SetType',
                        'VesselClass','Day', 'Month','PositionPrecision',
                        'GearType','RecordType','DirectedSpecies','DataSource', 
                        'VesselHorsepower','HaulDay','HaulMonth', 'StartTime',
                        'StatisticalArea', 'InOut200MileLimit',  'CodendMeshSize',
                        'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 
                        'NumberGillnets', 'AverageGillnetLength', 'GrateBarSpacing', 
                        'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                        'NumberPotReleasedCrab','AverageDepth','NumberSpecies', 'LogbookIDNumber1', 
                        'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 
                        'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                        'NumberIndividuals']] = Complete_df[
                        ['DataBase_ID', 'RecordIdentifier', 'GearDamage',
                        'ASOCCode', 'Year', 'DeploymentNumber', 
                        'SetNumber', 'Country', 'Quota', 'SetType',
                        'VesselClass','Day', 'Month','PositionPrecision',
                        'GearType','RecordType','DirectedSpecies','DataSource', 
                        'VesselHorsepower','HaulDay','HaulMonth', 'StartTime',
                        'StatisticalArea', 'InOut200MileLimit',  'CodendMeshSize',
                        'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 
                        'NumberGillnets', 'AverageGillnetLength', 'GrateBarSpacing', 
                        'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                        'NumberPotReleasedCrab','AverageDepth','NumberSpecies', 'LogbookIDNumber1', 
                        'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 
                        'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                        'NumberIndividuals']].astype(int)
                    
            Complete_df[['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                        'EndLongitude','AverageTowSpeed', 'VesselLength']] = Complete_df[
                        ['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                        'EndLongitude','AverageTowSpeed', 'VesselLength']].astype(float)
            
            Complete_df['VesselSideNumber'] = pd.to_numeric(Complete_df[
                        'VesselSideNumber'], downcast='integer', errors='ignore')
            
            Complete_df['SubTripNumber'] = pd.to_numeric(Complete_df[
                        'SubTripNumber'], downcast='integer', errors='ignore')
                        
            Complete_df[['ObserverNumber', 'DeploymentUID', 
                        'SubTripNumber','NAFODivision', 'VesselSideNumber',
                        'UnitArea','DetailedCatchSpeciesCompCode']] = Complete_df[
                        ['ObserverNumber', 'DeploymentUID', 
                        'SubTripNumber','NAFODivision', 'VesselSideNumber',
                        'UnitArea','DetailedCatchSpeciesCompCode']].astype(str)

            Complete_df = Complete_df.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID',
                'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
                'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
                'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
                'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
                'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
                'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
                'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
                'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
                'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                'NumberIndividuals']]
                
            Complete_df = Complete_df.replace([99999999, 99999999.0, np.nan], '')
            Complete_df = Complete_df.replace(['99999999.0', '99999999', '.'], 'None')
            Complete_df  = Complete_df.reset_index(drop=True)
            Complete_df = pd.DataFrame(Complete_df)
            iSubmit = tkinter.messagebox.askyesno("Submit DFO-NL ASOP Set & Catch Edited Table",
                    "Confirm If You Want to Submit DFO-NL ASOP Set & Catch Edited Table To QC Database ?")
            if iSubmit >0:
                try:
                    Complete_df = pd.DataFrame(Complete_df)
                    BackendSubmitAndUpdateDB(Complete_df)
                except:
                    print('Error Occured In DataBase')
                finally:
                    pt.redraw()
                    ViewClearView()
                    tkinter.messagebox.showinfo("Submitted To Set&Catch DB","Successfully Submitted To Update DB")      
        else:
            tkinter.messagebox.showinfo("Empty Set&Catch DB","Empty Set&Catch DB, Please Import Set&Catch CSV File To Submit")

    def BackendSubmitAndUpdateDB(Complete_df):
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
        conn_DB_SetCatch_Validation_Range= sqlite3.connect(DB_SetCatch_Validation_Range)
        cur_DB_SetCatch_Validation_Range=conn_DB_SetCatch_Validation_Range.cursor()
        UpdateRecordList1_SetCatchDB =[]
        UpdateRecordList2_SetCatchDB =[]
        UpdateRecordList3_SetCatchDB =[]
        df_rows = Complete_df.to_numpy().tolist()
        for row in df_rows:
            rowValue = row
            list_item_DataBase_ID = int(rowValue[0])
            list_item_RecordIdentifier = int(rowValue[1])
            list_item_DeploymentUID = (rowValue[2])
            list_item_ASOCCode = (rowValue[3])
            list_item_ObserverNumber = (rowValue[4])
            list_item_Year = (rowValue[5])
            list_item_DeploymentNumber = (rowValue[6])
            list_item_SubTripNumber = (rowValue[7])
            list_item_SetNumber = (rowValue[8])
            list_item_Country = (rowValue[9])
            list_item_Quota = (rowValue[10])
            list_item_SetType = (rowValue[11])
            list_item_VesselSideNumber = (rowValue[12])
            list_item_VesselClass = (rowValue[13])
            list_item_VesselLength = (rowValue[14])
            list_item_VesselHorsepower = (rowValue[15])
            list_item_Day = (rowValue[16])
            list_item_Month = (rowValue[17])
            list_item_HaulDay = (rowValue[18])
            list_item_HaulMonth = (rowValue[19])
            list_item_StartTime = (rowValue[20])
            list_item_Duration = (rowValue[21])
            list_item_PositionPrecision = (rowValue[22])
            list_item_StartLatitude = (rowValue[23])
            list_item_StartLongitude = (rowValue[24])
            list_item_EndLatitude = (rowValue[25])
            list_item_EndLongitude = (rowValue[26])
            list_item_NAFODivision = (rowValue[27])
            list_item_UnitArea = (rowValue[28])
            list_item_StatisticalArea = (rowValue[29])
            list_item_InOut200MileLimit = (rowValue[30])
            list_item_GearType = (rowValue[31])
            list_item_CodendMeshSize = (rowValue[32])
            list_item_MeshSizeMG = (rowValue[33])
            list_item_MeshSizeFG = (rowValue[34])
            list_item_RollerBobbbinDiameter = (rowValue[35])
            list_item_NumberGillnets = (rowValue[36])
            list_item_AverageGillnetLength = (rowValue[37])
            list_item_GrateBarSpacing = (rowValue[38])
            list_item_FootropeLength = (rowValue[39])
            list_item_NumberWindows = (rowValue[40])
            list_item_NumberHooks = (rowValue[41])
            list_item_NumberPots = (rowValue[42])
            list_item_NumberPotReleasedCrab = (rowValue[43])
            list_item_GearDamage = (rowValue[44])
            list_item_AverageTowSpeed = (rowValue[45])
            list_item_AverageDepth = (rowValue[46])
            list_item_DataSource = (rowValue[47])
            list_item_DirectedSpecies = (rowValue[48])
            list_item_NumberSpecies = (rowValue[49])
            list_item_RecordType = (rowValue[50])
            list_item_DetailedCatchSpeciesCompCode = (rowValue[51])
            list_item_LogbookIDNumber1 = (rowValue[52])
            list_item_LogbookIDNumber2 = (rowValue[53])
            list_item_SpeciesCode = (rowValue[54])
            list_item_KeptWeight = (rowValue[55])
            list_item_DiscardWeight = (rowValue[56])
            list_item_EstimatedWeightReleasedCrab = (rowValue[57])
            list_item_NumberIndividuals = (rowValue[58])

            UpdateRecordList1_SetCatchDB.append((
                                list_item_ASOCCode,                     
                                list_item_ObserverNumber,               
                                list_item_Year,                        
                                list_item_DeploymentNumber,             
                                list_item_SubTripNumber,                
                                list_item_SetNumber,                    
                                list_item_Country,                      
                                list_item_Quota,                        
                                list_item_SetType,                     
                                list_item_VesselSideNumber,             
                                list_item_VesselClass,                  
                                list_item_VesselLength,                 
                                list_item_VesselHorsepower,             
                                list_item_Day,                          
                                list_item_Month,                        
                                list_item_HaulDay,                      
                                list_item_HaulMonth,                    
                                list_item_StartTime,                    
                                list_item_Duration,                     
                                list_item_PositionPrecision,            
                                list_item_StartLatitude,                
                                list_item_StartLongitude,               
                                list_item_EndLatitude,                  
                                list_item_EndLongitude,                 
                                list_item_NAFODivision,                 
                                list_item_UnitArea,                     
                                list_item_StatisticalArea,              
                                list_item_InOut200MileLimit,            
                                list_item_GearType,                     
                                list_item_CodendMeshSize,               
                                list_item_MeshSizeMG,                   
                                list_item_MeshSizeFG,                   
                                list_item_RollerBobbbinDiameter,        
                                list_item_NumberGillnets,               
                                list_item_AverageGillnetLength,         
                                list_item_GrateBarSpacing,              
                                list_item_FootropeLength,              
                                list_item_NumberWindows,                
                                list_item_NumberHooks,                  
                                list_item_NumberPots,                  
                                list_item_NumberPotReleasedCrab,       
                                list_item_GearDamage,                   
                                list_item_AverageTowSpeed,              
                                list_item_AverageDepth,                 
                                list_item_DataSource,                   
                                list_item_DirectedSpecies,              
                                list_item_NumberSpecies,                            
                                list_item_DetailedCatchSpeciesCompCode, 
                                list_item_LogbookIDNumber1,             
                                list_item_LogbookIDNumber2,             
                                list_item_DeploymentUID))
            
            UpdateRecordList2_SetCatchDB.append((
                                list_item_ASOCCode,                     
                                list_item_ObserverNumber,               
                                list_item_Year,                        
                                list_item_DeploymentNumber,             
                                list_item_SubTripNumber,                
                                list_item_SetNumber,                    
                                list_item_Country,                      
                                list_item_Quota,                        
                                list_item_SetType,                     
                                list_item_VesselSideNumber,             
                                list_item_VesselClass,                  
                                list_item_VesselLength,                 
                                list_item_VesselHorsepower,             
                                list_item_Day,                          
                                list_item_Month,                        
                                list_item_HaulDay,                      
                                list_item_HaulMonth,                    
                                list_item_StartTime,                    
                                list_item_Duration,                     
                                list_item_PositionPrecision,            
                                list_item_StartLatitude,                
                                list_item_StartLongitude,               
                                list_item_EndLatitude,                  
                                list_item_EndLongitude,                 
                                list_item_NAFODivision,                 
                                list_item_UnitArea,                     
                                list_item_StatisticalArea,              
                                list_item_InOut200MileLimit,            
                                list_item_GearType,                     
                                list_item_CodendMeshSize,               
                                list_item_MeshSizeMG,                   
                                list_item_MeshSizeFG,                   
                                list_item_RollerBobbbinDiameter,        
                                list_item_NumberGillnets,               
                                list_item_AverageGillnetLength,         
                                list_item_GrateBarSpacing,              
                                list_item_FootropeLength,              
                                list_item_NumberWindows,                
                                list_item_NumberHooks,                  
                                list_item_NumberPots,                  
                                list_item_NumberPotReleasedCrab,       
                                list_item_GearDamage,                   
                                list_item_AverageTowSpeed,              
                                list_item_AverageDepth,                 
                                list_item_DataSource,                   
                                list_item_DirectedSpecies,              
                                list_item_NumberSpecies,                            
                                list_item_DetailedCatchSpeciesCompCode, 
                                list_item_LogbookIDNumber1,             
                                list_item_LogbookIDNumber2,             
                                list_item_SpeciesCode,                  
                                list_item_KeptWeight,                   
                                list_item_DiscardWeight,                
                                list_item_EstimatedWeightReleasedCrab,  
                                list_item_NumberIndividuals,  
                                list_item_DeploymentUID))
            
            UpdateRecordList3_SetCatchDB.append((
                                list_item_SpeciesCode,                  
                                list_item_KeptWeight,                   
                                list_item_DiscardWeight,                
                                list_item_EstimatedWeightReleasedCrab,  
                                list_item_NumberIndividuals,
                                list_item_RecordType, 
                                list_item_DataBase_ID))    
                         
        ## DB Update Executing
        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET \
                ASOCCode =? , ObserverNumber = ?, Year =?, DeploymentNumber =?, SubTripNumber =?,\
                SetNumber =? , Country = ?, Quota =?, SetType =?, VesselSideNumber =?,\
                VesselClass =? , VesselLength = ?, VesselHorsepower =?, Day =?, Month =?,\
                HaulDay =? , HaulMonth = ?, StartTime =?, Duration =?, PositionPrecision =?,\
                StartLatitude =? , StartLongitude = ?, EndLatitude =?, EndLongitude =?, NAFODivision =?,\
                UnitArea =? , StatisticalArea = ?, InOut200MileLimit =?, GearType =?, CodendMeshSize =?,\
                MeshSizeMG =?, MeshSizeFG = ? , RollerBobbbinDiameter = ?, NumberGillnets = ?, AverageGillnetLength =?,\
                GrateBarSpacing =?, FootropeLength = ? , NumberWindows = ?, NumberHooks = ?, NumberPots =?,\
                NumberPotReleasedCrab =?, GearDamage = ? , AverageTowSpeed = ?, AverageDepth = ?, DataSource =?,\
                DirectedSpecies =?, NumberSpecies = ? , DetailedCatchSpeciesCompCode = ?, LogbookIDNumber1 =?, LogbookIDNumber2 =?\
				WHERE DeploymentUID =?", 
				UpdateRecordList1_SetCatchDB)
        
        cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET \
                ASOCCode =? , ObserverNumber = ?, Year =?, DeploymentNumber =?, SubTripNumber =?,\
                SetNumber =? , Country = ?, Quota =?, SetType =?, VesselSideNumber =?,\
                VesselClass =? , VesselLength = ?, VesselHorsepower =?, Day =?, Month =?,\
                HaulDay =? , HaulMonth = ?, StartTime =?, Duration =?, PositionPrecision =?,\
                StartLatitude =? , StartLongitude = ?, EndLatitude =?, EndLongitude =?, NAFODivision =?,\
                UnitArea =? , StatisticalArea = ?, InOut200MileLimit =?, GearType =?, CodendMeshSize =?,\
                MeshSizeMG =?, MeshSizeFG = ? , RollerBobbbinDiameter = ?, NumberGillnets = ?, AverageGillnetLength =?,\
                GrateBarSpacing =?, FootropeLength = ? , NumberWindows = ?, NumberHooks = ?, NumberPots =?,\
                NumberPotReleasedCrab =?, GearDamage = ? , AverageTowSpeed = ?, AverageDepth = ?, DataSource =?,\
                DirectedSpecies =?, NumberSpecies = ? , DetailedCatchSpeciesCompCode = ?, LogbookIDNumber1 =?, LogbookIDNumber2 =?, \
                SpeciesCode = ? , KeptWeight = ?, DiscardWeight = ?, EstimatedWeightReleasedCrab =?, NumberIndividuals =?\
				WHERE DeploymentUID =?", 
				UpdateRecordList2_SetCatchDB)
                                    
        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET \
                SpeciesCode = ? , KeptWeight = ?, DiscardWeight = ?,\
                EstimatedWeightReleasedCrab =?, NumberIndividuals =?\
				WHERE RecordType =? AND DataBase_ID = ? ", 
				UpdateRecordList3_SetCatchDB)
        
        conn_DB_Set_Catch_Analysis.commit()
        conn_DB_Set_Catch_Analysis.close()
        conn_DB_SetCatch_Validation_Range.commit()
        conn_DB_SetCatch_Validation_Range.close()
     
    def SetCatchColName():
        SetCatchColNameList =  ['TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag',
				'DataBase_ID','RecordIdentifier','DeploymentUID',
				'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
				'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
				'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
				'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
				'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
				'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
				'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
				'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
				'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
				'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
				'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
				'NumberIndividuals']
        return SetCatchColNameList

    def SetCatchDFQC(Complete_df):
        Complete_df  = pd.DataFrame(Complete_df)      
        Complete_df= (Complete_df.loc[:,
            ['TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag',
            'DataBase_ID','RecordIdentifier','DeploymentUID',
            'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
            'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
            'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
            'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
            'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
            'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
            'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
            'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
            'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
            'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
            'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
            'NumberIndividuals'
            ]]).replace(['', None, np.nan, 'None'], 99999999)

        Complete_df[['DataBase_ID', 'RecordIdentifier', 'GearDamage',
                    'ASOCCode', 'Year', 'DeploymentNumber', 
                    'SetNumber', 'Country', 'Quota', 'SetType',
                    'VesselClass','Day', 'Month','PositionPrecision',
                    'GearType','RecordType','DirectedSpecies','DataSource', 
                    'VesselHorsepower','HaulDay','HaulMonth', 'StartTime',
                    'StatisticalArea', 'InOut200MileLimit',  'CodendMeshSize',
                    'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 
                    'NumberGillnets', 'AverageGillnetLength', 'GrateBarSpacing', 
                    'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                    'NumberPotReleasedCrab','AverageDepth','NumberSpecies', 'LogbookIDNumber1', 
                    'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 
                    'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                    'NumberIndividuals']] = Complete_df[
                    ['DataBase_ID', 'RecordIdentifier', 'GearDamage',
                    'ASOCCode', 'Year', 'DeploymentNumber', 
                    'SetNumber', 'Country', 'Quota', 'SetType',
                    'VesselClass','Day', 'Month','PositionPrecision',
                    'GearType','RecordType','DirectedSpecies','DataSource', 
                    'VesselHorsepower','HaulDay','HaulMonth', 'StartTime',
                    'StatisticalArea', 'InOut200MileLimit',  'CodendMeshSize',
                    'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 
                    'NumberGillnets', 'AverageGillnetLength', 'GrateBarSpacing', 
                    'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                    'NumberPotReleasedCrab','AverageDepth','NumberSpecies', 'LogbookIDNumber1', 
                    'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 
                    'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                    'NumberIndividuals']].astype(int)
                    
        Complete_df[['TowDistance', 'SCDistance', 'TowDifference',
                     'Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                     'EndLongitude','AverageTowSpeed', 'VesselLength']] = Complete_df[
                    ['TowDistance', 'SCDistance', 'TowDifference',
                     'Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                     'EndLongitude','AverageTowSpeed', 'VesselLength']].astype(float)
        
        Complete_df['VesselSideNumber'] = pd.to_numeric(Complete_df[
                    'VesselSideNumber'], downcast='integer', errors='ignore')
        
        Complete_df['SubTripNumber'] = pd.to_numeric(Complete_df[
                    'SubTripNumber'], downcast='integer', errors='ignore')
                    
        Complete_df[['ObserverNumber', 'DeploymentUID', 'TowDiffFlag',
                    'SubTripNumber','NAFODivision', 'VesselSideNumber',
                    'UnitArea','DetailedCatchSpeciesCompCode']] = Complete_df[
                    ['ObserverNumber', 'DeploymentUID', 'TowDiffFlag',
                    'SubTripNumber','NAFODivision', 'VesselSideNumber',
                    'UnitArea','DetailedCatchSpeciesCompCode']].astype(str)
        
        Complete_df.sort_values(by=['Year', 'ASOCCode', 'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
        Complete_df  = Complete_df.reset_index(drop=True)
        Complete_df = pd.DataFrame(Complete_df, index=None)

        Complete_df = Complete_df.replace([99999999, 99999999.0, np.nan], '')
        Complete_df = Complete_df.replace(['99999999.0', '99999999', '.'], 'None')
        Complete_df  = Complete_df.reset_index(drop=True)
        return Complete_df

    ## CV - Set & Index Col - Section D
    def SetIndexDF():
        def findElements(lst1, lst2):
            return list(map(lst1.__getitem__, lst2))
        SetCatchColNameList = SetCatchColName()
        getColsSelectedID = pt.prodyutCustomgetSelColName()
        getColsSelectedCol = findElements(SetCatchColNameList, getColsSelectedID)
        if ((len(getColsSelectedCol)) > 0) & ((len(getColsSelectedCol))<6):
            pt.setindex()
            button_SubmitToUpdateDB_PF.config(state="disabled")

            button_SetUpAsIndexCols.config(state="disabled")
            button_SetUpDefaultIndexCols.config(state="disabled")
            button_ResetIndexCols.config(state="normal")

            button_SetUpColChooser.config(state="disabled")
            button_SetUpDefColchoser.config(state="disabled")
            button_ResetChooseCols.config(state="disabled")

            button_SetUuListCols.config(state="disabled")
            button_SetUpDefColList.config(state="disabled")
            button_ResetChooseColList.config(state="disabled")

            button_ViewAllFlagged.config(state="normal")
            button_ViewCleartable.config(state="disabled")
            button_ReloadViewFlagged.config(state="disabled")
        else:
            tkinter.messagebox.showinfo("Set-Up Index Selection Message","Length Of Index Selection Must Be Between 1 To 5")

    def DefaultSetIndexDF():
        button_SubmitToUpdateDB_PF.config(state="disabled")

        button_SetUpAsIndexCols.config(state="disabled")
        button_SetUpDefaultIndexCols.config(state="disabled")
        button_ResetIndexCols.config(state="normal")

        button_SetUpColChooser.config(state="disabled")
        button_SetUpDefColchoser.config(state="disabled")
        button_ResetChooseCols.config(state="disabled")

        button_SetUuListCols.config(state="disabled")
        button_SetUpDefColList.config(state="disabled")
        button_ResetChooseColList.config(state="disabled")

        button_ViewAllFlagged.config(state="normal")
        button_ViewCleartable.config(state="disabled")
        button_ReloadViewFlagged.config(state="disabled")
  
    def ReSetIndexDF_BackEnd():
        pt.resetIndex(ask=False, drop=False)
        Complete_df = pd.DataFrame(pt.model.df)
        Complete_df.reset_index(drop=True, inplace = True)
        Complete_df = SetCatchDFQC(Complete_df)
        Complete_df = Complete_df.loc[:,['TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag',
				'DataBase_ID','RecordIdentifier','DeploymentUID',
				'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
				'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
				'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
				'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
				'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
				'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
				'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
				'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
				'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
				'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
				'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
				'NumberIndividuals']]
        Complete_df.sort_values(by=['Year', 'ASOCCode', 'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
        Complete_df  = Complete_df.reset_index(drop=True)
        Complete_df = pd.DataFrame(Complete_df, index=None)
        pt.prodyutCustomclearTable()
        pt.model.df = Complete_df
        pt.model.df.reset_index(drop=True)
        pt.update()
        pt.redraw()
        pt.resetColors()
        pt.setRowColors(rows=range(1,len(Complete_df),2), clr='lightblue', cols='all')
        pt.cellbackgr = 'aliceblue'
        options = config.load_options()
        options = { 'align': 'center',
                    'cellbackgr': '#F4F4F3',
                    'cellwidth': 120,
                    'floatprecision': 2,
                    'thousandseparator': '',
                    'font': 'Arial',
                    'fontsize': 8,
                    'fontstyle': '',
                    'grid_color': '#ABB1AD',
                    'linewidth': 1,
                    'rowheight': 22,
                    'rowselectedcolor': '#E4DED4',
                    'textcolor': 'black'}
        config.apply_options(options, pt)
       
    def ReSetIndexDF():
        windows.after(100, ReSetIndexDF_BackEnd)
        pt.autoResizeColumns()
        button_SubmitToUpdateDB_PF.config(state="normal")

        button_SetUpAsIndexCols.config(state="disabled")
        button_SetUpDefaultIndexCols.config(state="disabled")
        button_ResetIndexCols.config(state="normal")

        button_SetUpColChooser.config(state="normal")
        button_SetUpDefColchoser.config(state="normal")
        button_ResetChooseCols.config(state="normal")

        button_SetUuListCols.config(state="normal")
        button_SetUpDefColList.config(state="normal")
        button_ResetChooseColList.config(state="normal")

        button_ViewAllFlagged.config(state="normal")
        button_ViewCleartable.config(state="normal")
        button_ReloadViewFlagged.config(state="normal")
    
    ## CV - Sel & Move Col - Section B
    def SetColumnChooser():
        def findElements(lst1, lst2):
            return list(map(lst1.__getitem__, lst2))
        SetCatchColNameList = SetCatchColName()
        getColsSelectedID = pt.prodyutCustomgetSelColName()
        getColsSelectedCol = findElements(SetCatchColNameList, getColsSelectedID)
        if (len(getColsSelectedCol))> 0:
            pt.moveColumns(names = getColsSelectedCol, pos='start')
            pt.redraw()
            button_SubmitToUpdateDB_PF.config(state="disabled")

            button_SetUpAsIndexCols.config(state="disabled")
            button_SetUpDefaultIndexCols.config(state="disabled")
            button_ResetIndexCols.config(state="disabled")

            button_SetUpColChooser.config(state="normal")
            button_SetUpDefColchoser.config(state="normal")
            button_ResetChooseCols.config(state="normal")

            button_SetUuListCols.config(state="disabled")
            button_SetUpDefColList.config(state="disabled")
            button_ResetChooseColList.config(state="disabled")

            button_ViewAllFlagged.config(state="normal")
            button_ViewCleartable.config(state="normal")
            button_ReloadViewFlagged.config(state="normal")
        else:
            tkinter.messagebox.showinfo("Set-Up Column Chooser Selection Message",
                                        "Length Of Column Chooser Selection Must Be Greater Than Zero")

    def ResetColumnChooser():
        Complete_df = pd.DataFrame(pt.model.df)
        Complete_df = SetCatchDFQC(Complete_df)
        Complete_df = Complete_df.loc[:,['TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag',
				'DataBase_ID','RecordIdentifier','DeploymentUID',
				'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
				'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
				'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
				'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
				'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
				'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
				'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
				'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
				'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
				'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
				'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
				'NumberIndividuals']]
        Complete_df.sort_values(by=['Year', 'ASOCCode', 'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
        Complete_df  = Complete_df.reset_index(drop=True)
        Complete_df = pd.DataFrame(Complete_df, index=None)
        pt.prodyutCustomclearTable()
        pt.model.df = Complete_df
        pt.model.df.reset_index(drop=True)
        pt.update()
        pt.resetColors()
        pt.setRowColors(rows=range(1,len(Complete_df),2), clr='lightblue', cols='all')
        pt.cellbackgr = 'aliceblue'
        options = config.load_options()
        options = { 'align': 'center',
                    'cellbackgr': '#F4F4F3',
                    'cellwidth': 120,
                    'floatprecision': 2,
                    'thousandseparator': '',
                    'font': 'Arial',
                    'fontsize': 8,
                    'fontstyle': '',
                    'grid_color': '#ABB1AD',
                    'linewidth': 1,
                    'rowheight': 22,
                    'rowselectedcolor': '#E4DED4',
                    'textcolor': 'black'}
        config.apply_options(options, pt)
        button_SubmitToUpdateDB_PF.config(state="normal")

        button_SetUpAsIndexCols.config(state="disabled")
        button_SetUpDefaultIndexCols.config(state="disabled")
        button_ResetIndexCols.config(state="disabled")

        button_SetUpColChooser.config(state="normal")
        button_SetUpDefColchoser.config(state="normal")
        button_ResetChooseCols.config(state="normal")

        button_SetUuListCols.config(state="normal")
        button_SetUpDefColList.config(state="normal")
        button_ResetChooseColList.config(state="normal")

        button_ViewAllFlagged.config(state="normal")
        button_ViewCleartable.config(state="normal")
        button_ReloadViewFlagged.config(state="normal")

    def DefaultColChooser():
        pt.prodyutCustomclearTable()
        Return_ObserverSetCatchDB = get_ObserverSetCatchDB()
        ObserverSetCatchDB = Return_ObserverSetCatchDB[0]
        ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                ['DeploymentUID','TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag',
                 'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'Day', 
                 'Month', 'StartTime', 'Duration', 'HaulDay','HaulMonth', 'GearType',
                 'RecordType', 'NAFODivision','UnitArea', 'StatisticalArea', 'InOut200MileLimit', 
                 'Country','ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
                 'SetNumber',  'Quota', 'SetType', 'VesselSideNumber', 'VesselClass', 
                 'VesselLength', 'VesselHorsepower',  'PositionPrecision','CodendMeshSize',
                 'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                 'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                 'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
                 'DirectedSpecies', 'NumberSpecies',  'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
                 'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                 'NumberIndividuals', 'DataBase_ID','RecordIdentifier']]
        ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)
        pt.model.df = ObserverSetCatchDB
        pt.model.df.reset_index(drop=True)
        #pt.redraw()
        pt.update()
        pt.resetColors()
        pt.setRowColors(rows=range(1,len(ObserverSetCatchDB),2), clr='lightblue', cols='all')
        pt.cellbackgr = 'aliceblue'
        options = config.load_options()
        options = { 'align': 'center',
                    'cellbackgr': '#F4F4F3',
                    'cellwidth': 120,
                    'floatprecision': 2,
                    'thousandseparator': '',
                    'font': 'Arial',
                    'fontsize': 8,
                    'fontstyle': '',
                    'grid_color': '#ABB1AD',
                    'linewidth': 1,
                    'rowheight': 22,
                    'rowselectedcolor': '#E4DED4',
                    'textcolor': 'black'}
        config.apply_options(options, pt)
        button_SubmitToUpdateDB_PF.config(state="disabled")

        button_SetUpAsIndexCols.config(state="disabled")
        button_SetUpDefaultIndexCols.config(state="disabled")
        button_ResetIndexCols.config(state="normal")

        button_SetUpColChooser.config(state="normal")
        button_SetUpDefColchoser.config(state="normal")
        button_ResetChooseCols.config(state="normal")

        button_SetUuListCols.config(state="disabled")
        button_SetUpDefColList.config(state="disabled")
        button_ResetChooseColList.config(state="disabled")

        button_ViewAllFlagged.config(state="normal")
        button_ViewCleartable.config(state="disabled")
        button_ReloadViewFlagged.config(state="disabled")

    ## Top Menu 
    def ReloadDBViewAllFlaggedEntries():
        Return_ObserverSetCatchDB = get_ObserverSetCatchDB()
        ObserverSetCatchDB = Return_ObserverSetCatchDB[0]
        entry_DBEntries.delete(0,END)
        entry_Flagged.delete(0,END)
        entry_DBEntries.insert(tk.END,Return_ObserverSetCatchDB[1])
        entry_Flagged.insert(tk.END,Return_ObserverSetCatchDB[2])
        ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                ['TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag',
				'DataBase_ID','RecordIdentifier','DeploymentUID',
				'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
				'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
				'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
				'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
				'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
				'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
				'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
				'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
				'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
				'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
				'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
				'NumberIndividuals']]
        ObserverSetCatchDB.sort_values(by=['Year', 'ASOCCode', 
        'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
        ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)
        
        UpdatedObserverSetCatchDB = pd.DataFrame(pt.model.df)
        if len(UpdatedObserverSetCatchDB) > 0:
            pt.resetIndex(ask=False, drop=False)
            UpdatedObserverSetCatchDB = pd.DataFrame(pt.model.df)
            UpdatedObserverSetCatchDB.reset_index(drop=True, inplace = True)
            UpdatedObserverSetCatchDB = pd.DataFrame(UpdatedObserverSetCatchDB, index=None)
            UpdatedObserverSetCatchDB = UpdatedObserverSetCatchDB.loc[:,
                ['TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag',
				'DataBase_ID','RecordIdentifier','DeploymentUID',
				'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
				'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
				'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
				'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
				'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
				'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
				'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
				'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
				'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
				'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
				'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
				'NumberIndividuals']]
            UpdatedObserverSetCatchDB.sort_values(by=['Year', 'ASOCCode', 
                'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
            UpdatedObserverSetCatchDB  = UpdatedObserverSetCatchDB.reset_index(drop=True)
            UpdatedObserverSetCatchDB = pd.DataFrame(UpdatedObserverSetCatchDB, index=None)
            ObserverSetCatchDB.update(UpdatedObserverSetCatchDB)
            ObserverSetCatchDB = SetCatchDFQC(ObserverSetCatchDB)

        ObserverSetCatchDB['ViewDepUID'] = ObserverSetCatchDB.loc[:, 'DeploymentUID']
        ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)
        pt.prodyutCustomclearTable()
        pt.model.df = ObserverSetCatchDB
        pt.model.df.reset_index(drop=True)
        pt.update()
        pt.resetColors()
        pt.setRowColors(rows=range(1,len(ObserverSetCatchDB),2), clr='lightblue', cols='all')
        pt.cellbackgr = 'aliceblue'
        options = config.load_options()
        options = { 'align': 'center',
                    'cellbackgr': '#F4F4F3',
                    'cellwidth': 120,
                    'floatprecision': 2,
                    'thousandseparator': '',
                    'font': 'Arial',
                    'fontsize': 8,
                    'fontstyle': '',
                    'grid_color': '#ABB1AD',
                    'linewidth': 1,
                    'rowheight': 22,
                    'rowselectedcolor': '#E4DED4',
                    'textcolor': 'black'}
        config.apply_options(options, pt)
        pt.autoResizeColumns()
        pt.prodyutCustomsetindex2_1()
        button_SubmitToUpdateDB_PF.config(state="normal")
        button_SetUpColChooser.config(state="normal")
        button_SetUpAsIndexCols.config(state="disabled")
        button_SetUpDefaultIndexCols.config(state="disabled")

    def get_QCfailFlaggedEntries():
        try:
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = sqliteConnection.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_TowDistance;", sqliteConnection)
            length_Complete_df = len(Complete_df)
            if length_Complete_df > 0:
                Complete_df = Complete_df[(Complete_df.TowDiffFlag) == 'Yes']
                Complete_df = Complete_df.reset_index(drop=True)
                ObserverSetCatchDB = pd.DataFrame(Complete_df)
                sqliteConnection.commit()
                return ObserverSetCatchDB, length_Complete_df
            else:
                messagebox.showerror('Set & Catch Database Is Empty', "Please Import Set & Catch CSV File To View")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()
    
    def ViewQCfailFlaggedEntries():
        root = tk.Toplevel(windows)
        root.title ("ExcelView All Set&Catch Entries")
        root.geometry('1515x855+40+40')
        root.config(bg="cadet blue")
        def on_close():
            tkinter.messagebox.ABORT = 'abort'
        frame1 = tk.Frame(root)
        frame1.pack(fill=BOTH, expand=1)
        Return_ObserverSetCatchDB = get_QCfailFlaggedEntries()
        ObserverSetCatchDB = Return_ObserverSetCatchDB[0]
        ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                ['TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag',
				'DataBase_ID','RecordIdentifier','DeploymentUID',
				'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
				'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
				'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
				'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
				'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
				'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
				'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
				'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
				'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
				'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
				'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
				'NumberIndividuals']]
        ObserverSetCatchDB.sort_values(by=['Year', 'ASOCCode', 
        'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
        ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)
        pt1 = Table(frame1, dataframe = ObserverSetCatchDB, showtoolbar=True, showstatusbar=True)
        pt1.setRowColors(rows=range(1,len(ObserverSetCatchDB),2), clr='lightblue', cols='all')
        pt1.cellbackgr = 'aliceblue'
        options = config.load_options()
        options = { 'align': 'center',
                    'cellbackgr': '#F4F4F3',
                    'cellwidth': 120,
                    'floatprecision': 2,
                    'thousandseparator': '',
                    'font': 'Arial',
                    'fontsize': 8,
                    'fontstyle': '',
                    'grid_color': '#ABB1AD',
                    'linewidth': 1,
                    'rowheight': 22,
                    'rowselectedcolor': '#E4DED4',
                    'textcolor': 'black'}
        config.apply_options(options, pt1)
        pt1.autoResizeColumns()
        pt1.show()
        root.protocol("WM_DELETE_WINDOW",  on_close)
        root.mainloop()
    
    def ViewClearView():
        pt.prodyutCustomclearTable()
        button_SetUpAsIndexCols.config(state="disabled")
        button_SetUpDefaultIndexCols.config(state="disabled")

    ## CV - Sel From List & View - Section C
    def RunSelCols_SetAndCatchDB():
        ViewClearView()
        win = tk.Tk()
        win.title ("Column Selection View")
        win.geometry("250x300")
        ListBoxDisplay = Listbox(win,selectmode="multiple", font=('aerial', 8, 'bold'),
                                height =6, width =20)
        GetSetCatchDB_VariableList = [
				'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
				'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
				'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
				'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
				'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
				'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
				'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
				'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
				'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
				'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
				'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
				'NumberIndividuals']

        for i in GetSetCatchDB_VariableList:
            ListBoxDisplay.insert(END,i)

        s = Scrollbar()
        scrollbar = ttk.Scrollbar(win, orient= 'vertical')
        scrollbar.pack(side= RIGHT, fill= BOTH)
        ListBoxDisplay.config(yscrollcommand= scrollbar.set)
        scrollbar.config(command= ListBoxDisplay.yview)
        ListBoxDisplay.pack(expand=YES,fill="both")
        def RunSeletView():
            SelectedColumns =[]
            for i in ListBoxDisplay.curselection():
                sel = (ListBoxDisplay.get(i))
                SelectedColumns.append(sel)
            viewSelCols_SetAndCatchDB(SelectedColumns)
            win.destroy()
        
        btn_SubmitSelection = Button(win, bd = 2, width = 15,
                    height=1, font=('aerial', 10, 'bold'), 
                    fg="blue", bg="cadet blue", 
                    text='Submit Selection', command=RunSeletView)
        btn_SubmitSelection.pack(side='bottom')
        win.mainloop()

    def viewSelCols_SetAndCatchDB(SelectedColumns):
        GetSetCatchDB_Columns = ['TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag',
				'DataBase_ID','RecordIdentifier','DeploymentUID',
				'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
				'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
				'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
				'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
				'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
				'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
				'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
				'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
				'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
				'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
				'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
				'NumberIndividuals'] 
        BaseColumns =['DeploymentUID','TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag']
        TreeViewSelectedCols = list(BaseColumns + list((SelectedColumns)))
        con= sqlite3.connect(DB_SetCatch_Validation_Range)
        cur=con.cursor()
        cur.execute("SELECT * FROM SetCatch_QCFailedRange_TowDistance")
        rows=cur.fetchall()
        rows = pd.DataFrame(rows)
        rows = rows.reset_index(drop=True)
        rows.columns = GetSetCatchDB_Columns
        cur.close()
        con.close()
        rows = pd.DataFrame(rows)
        rows = rows.reset_index(drop=True)
        rows = rows.loc[:,TreeViewSelectedCols]
        rows = rows.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(rows)
        ObserverSetCatchDB = ObserverSetCatchDB[(ObserverSetCatchDB.TowDiffFlag) == 'Yes']
        ObserverSetCatchDB[['Year_Sep', 'ASOC_Sep', 'DepN_Sep', 'SetN_Sep']] = \
        ObserverSetCatchDB['DeploymentUID'].str.split('-', expand=True)
        ObserverSetCatchDB[['Year_Sep', 'ASOC_Sep', 'DepN_Sep', 'SetN_Sep']] = ObserverSetCatchDB[
        ['Year_Sep', 'ASOC_Sep', 'DepN_Sep', 'SetN_Sep']].astype(int)
        ObserverSetCatchDB.sort_values(by=['Year_Sep', 'ASOC_Sep', 
                'DepN_Sep', 'SetN_Sep'], ascending=True, inplace=True)
        ObserverSetCatchDB = ObserverSetCatchDB.loc[:,TreeViewSelectedCols]
        ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)
        pt.model.df = ObserverSetCatchDB
        pt.model.df.reset_index(drop=True)
        pt.resetColors()
        pt.setRowColors(rows=range(1,len(ObserverSetCatchDB),2), clr='lightblue', cols='all')
        pt.cellbackgr = 'aliceblue'
        options = config.load_options()
        options = { 'align': 'center',
                    'cellbackgr': '#F4F4F3',
                    'cellwidth': 120,
                    'floatprecision': 2,
                    'thousandseparator': '',
                    'font': 'Arial',
                    'fontsize': 8,
                    'fontstyle': '',
                    'grid_color': '#ABB1AD',
                    'linewidth': 1,
                    'rowheight': 22,
                    'rowselectedcolor': '#E4DED4',
                    'textcolor': 'black'}
        config.apply_options(options, pt)
        button_SubmitToUpdateDB_PF.config(state="disabled")

        button_SetUpAsIndexCols.config(state="disabled")
        button_SetUpDefaultIndexCols.config(state="disabled")
        button_ResetIndexCols.config(state="disabled")

        button_SetUpColChooser.config(state="disabled")
        button_SetUpDefColchoser.config(state="disabled")
        button_ResetChooseCols.config(state="disabled")

        button_SetUuListCols.config(state="normal")
        button_SetUpDefColList.config(state="normal")
        button_ResetChooseColList.config(state="normal")

        button_ViewAllFlagged.config(state="normal")
        button_ViewCleartable.config(state="disabled")
        button_ReloadViewFlagged.config(state="disabled")

    def RunDefaultSelCols_SetAndCatchDB():
        ViewClearView()
        win = tk.Tk()
        win.title ("Column Selection View")
        win.geometry("250x300")
        ListBoxDisplay = Listbox(win,selectmode="multiple", font=('aerial', 8, 'bold'),
                                height =6, width =20)
        GetSetCatchDB_VariableList = [
                'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude',
                'Day', 'Month', 'StartTime', 'Duration', 'GearType', 'RecordType'
				]

        for i in GetSetCatchDB_VariableList:
            ListBoxDisplay.insert(END,i)
        
        ListBoxDisplay.selection_set(0, "end")
        s = Scrollbar()
        scrollbar = ttk.Scrollbar(win, orient= 'vertical')
        scrollbar.pack(side= RIGHT, fill= BOTH)
        ListBoxDisplay.config(yscrollcommand= scrollbar.set)
        scrollbar.config(command= ListBoxDisplay.yview)
        ListBoxDisplay.pack(expand=YES,fill="both")
        def RunSeletView():
            SelectedColumns =[]
            for i in ListBoxDisplay.curselection():
                sel = (ListBoxDisplay.get(i))
                SelectedColumns.append(sel)
            viewSelCols_SetAndCatchDB(SelectedColumns)
            win.destroy()
        
        btn_SubmitSelection = Button(win, bd = 2, width = 15,
                    height=1, font=('aerial', 10, 'bold'), 
                    fg="blue", bg="cadet blue", 
                    text='Submit Selection', command=RunSeletView)
        btn_SubmitSelection.pack(side='bottom')
        win.mainloop()

    def ResetListViewSelCol():
        Return_ObserverSetCatchDB = get_ObserverSetCatchDB()
        ObserverSetCatchDB = Return_ObserverSetCatchDB[0]
        ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                    ['TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag',
                    'DataBase_ID','RecordIdentifier','DeploymentUID',
                    'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
                    'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
                    'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
                    'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
                    'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
                    'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
                    'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                    'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                    'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
                    'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
                    'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                    'NumberIndividuals']]
        ObserverSetCatchDB.sort_values(by=['Year', 'ASOCCode', 
        'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
        ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)
        Complete_df  = pd.DataFrame(pt.model.df)
        Complete_df  = Complete_df.reset_index(drop=True)
        if (len(Complete_df) >0)&(len(ObserverSetCatchDB) >0):
            ObserverSetCatchDB.update(Complete_df)
            ObserverSetCatchDB.reset_index(inplace=True)
            ObserverSetCatchDB = SetCatchDFQC(ObserverSetCatchDB)
            ViewClearView()
            pt.model.df = ObserverSetCatchDB
            pt.model.df.reset_index(drop=True)
            pt.update()
            pt.resetColors()
            pt.setRowColors(rows=range(1,len(ObserverSetCatchDB),2), clr='lightblue', cols='all')
            pt.cellbackgr = 'aliceblue'
            options = config.load_options()
            options = { 'align': 'center',
                        'cellbackgr': '#F4F4F3',
                        'cellwidth': 120,
                        'floatprecision': 2,
                        'thousandseparator': '',
                        'font': 'Arial',
                        'fontsize': 8,
                        'fontstyle': '',
                        'grid_color': '#ABB1AD',
                        'linewidth': 1,
                        'rowheight': 22,
                        'rowselectedcolor': '#E4DED4',
                        'textcolor': 'black'}
            config.apply_options(options, pt)
            button_SubmitToUpdateDB_PF.config(state="normal")

            button_SetUpAsIndexCols.config(state="disabled")
            button_SetUpDefaultIndexCols.config(state="disabled")
            button_ResetIndexCols.config(state="normal")

            button_SetUpColChooser.config(state="normal")
            button_SetUpDefColchoser.config(state="normal")
            button_ResetChooseCols.config(state="normal")

            button_SetUuListCols.config(state="normal")
            button_SetUpDefColList.config(state="normal")
            button_ResetChooseColList.config(state="normal")

            button_ViewAllFlagged.config(state="normal")
            button_ViewCleartable.config(state="normal")
            button_ReloadViewFlagged.config(state="normal")

    ### Top File Menu : Misc
    def iExit():
        iExit= tkinter.messagebox.askyesno("DFO-NL-ASOP CalenderVariables Profile", "Confirm If You Want To Exit")
        if iExit >0:
            windows.destroy()
            return
    
    def ViewAssendingSortVariable():
        SetCatchColNameList = SetCatchColName()
        get_SortVarSelected  = entry_SelectedSortVar.get()
        if get_SortVarSelected in SetCatchColNameList:
            length_GetSetCatchDB = int(entry_DBEntries.get())
            Complete_df = pd.DataFrame(pt.model.df)
            length_Complete_df = len(Complete_df)
            if length_Complete_df == length_GetSetCatchDB:
                Complete_df = SetCatchDFQC(Complete_df)
                if get_SortVarSelected == 'DeploymentUID':
                    Complete_df[['Year_Sep', 'ASOC_Sep', 'DepN_Sep', 'SetN_Sep']] = \
                    Complete_df['DeploymentUID'].str.split('-', expand=True)
                    Complete_df[['Year_Sep', 'ASOC_Sep', 'DepN_Sep', 'SetN_Sep']] = Complete_df[
                    ['Year_Sep', 'ASOC_Sep', 'DepN_Sep', 'SetN_Sep']].astype(int)

                    Complete_df.sort_values(by=['Year_Sep', 'ASOC_Sep', 'DepN_Sep', 'SetN_Sep'], ascending=True, inplace=True)
                    SetCatchColNameList = SetCatchColName()
                    Complete_df= (Complete_df.loc[:,SetCatchColNameList])
                    Complete_df  = Complete_df.reset_index(drop=True)
                    Complete_df = pd.DataFrame(Complete_df)
                    Complete_df['ViewDepUID'] = Complete_df.loc[:, 'DeploymentUID']
                    Complete_df  = Complete_df.reset_index(drop=True)
                    Complete_df = pd.DataFrame(Complete_df, index=None)
                else:
                    Complete_df.sort_values(by=[get_SortVarSelected], ascending=True, inplace=True)
                    Complete_df  = Complete_df.reset_index(drop=True)
                    Complete_df = pd.DataFrame(Complete_df)
                    Complete_df['ViewDepUID'] = Complete_df.loc[:, 'DeploymentUID']
                    Complete_df  = Complete_df.reset_index(drop=True)
                    Complete_df = pd.DataFrame(Complete_df, index=None)
                pt.prodyutCustomclearTable()
                pt.model.df = Complete_df
                pt.model.df.reset_index(drop=True)
                pt.update()
                pt.resetColors()
                pt.setRowColors(rows=range(1,len(ObserverSetCatchDB),2), clr='lightblue', cols='all')
                pt.cellbackgr = 'aliceblue'
                options = config.load_options()
                options = { 'align': 'center',
                            'cellbackgr': '#F4F4F3',
                            'cellwidth': 120,
                            'floatprecision': 2,
                            'thousandseparator': '',
                            'font': 'Arial',
                            'fontsize': 8,
                            'fontstyle': '',
                            'grid_color': '#ABB1AD',
                            'linewidth': 1,
                            'rowheight': 22,
                            'rowselectedcolor': '#E4DED4',
                            'textcolor': 'black'}
                config.apply_options(options, pt)
                pt.autoResizeColumns()
                pt.prodyutCustomsetindex2_1()
                button_SubmitToUpdateDB_PF.config(state="normal")

                button_SetUpAsIndexCols.config(state="disabled")
                button_SetUpDefaultIndexCols.config(state="disabled")
                button_ResetIndexCols.config(state="disabled")

                button_SetUpColChooser.config(state="normal")
                button_ResetChooseCols.config(state="normal")

                button_SetUuListCols.config(state="normal")
                button_ResetChooseColList.config(state="normal")

                button_ViewCleartable.config(state="normal")
                button_ReloadViewFlagged.config(state="normal")

            else:
                tkinter.messagebox.showinfo("DB Sorting Message - Table Entries Must Be Same Total DB Entries",
                                            "Unable To Sort, Please Check If There is Row Filter Applied Or Not")
        else:
            tkinter.messagebox.showinfo("Sorting Table Message",
                                        "Please Select Sorting Variable From DropDown")
    
    def ViewDesendingSortVariable():
        SetCatchColNameList = SetCatchColName()
        get_SortVarSelected  = entry_SelectedSortVar.get()
        if get_SortVarSelected in SetCatchColNameList:
            length_GetSetCatchDB = int(entry_DBEntries.get())
            Complete_df = pd.DataFrame(pt.model.df)
            length_Complete_df = len(Complete_df)
            if length_Complete_df == length_GetSetCatchDB:
                Complete_df = SetCatchDFQC(Complete_df)
                if get_SortVarSelected == 'DeploymentUID':
                    Complete_df[['Year_Sep', 'ASOC_Sep', 'DepN_Sep', 'SetN_Sep']] = \
                    Complete_df['DeploymentUID'].str.split('-', expand=True)
                    Complete_df[['Year_Sep', 'ASOC_Sep', 'DepN_Sep', 'SetN_Sep']] = Complete_df[
                    ['Year_Sep', 'ASOC_Sep', 'DepN_Sep', 'SetN_Sep']].astype(int)
                    Complete_df.sort_values(by=['Year_Sep', 'ASOC_Sep', 
                        'DepN_Sep', 'SetN_Sep'], ascending=False, inplace=True)
                    SetCatchColNameList = SetCatchColName()
                    Complete_df= (Complete_df.loc[:,SetCatchColNameList])
                    Complete_df  = Complete_df.reset_index(drop=True)
                    Complete_df = pd.DataFrame(Complete_df)
                    Complete_df['ViewDepUID'] = Complete_df.loc[:, 'DeploymentUID']
                    Complete_df  = Complete_df.reset_index(drop=True)
                    Complete_df = pd.DataFrame(Complete_df, index=None)
                else:
                    Complete_df.sort_values(by=[get_SortVarSelected], ascending=False, inplace=True)
                    Complete_df  = Complete_df.reset_index(drop=True)
                    Complete_df = pd.DataFrame(Complete_df)
                    Complete_df['ViewDepUID'] = Complete_df.loc[:, 'DeploymentUID']
                    Complete_df  = Complete_df.reset_index(drop=True)
                    Complete_df = pd.DataFrame(Complete_df, index=None)
                pt.prodyutCustomclearTable()
                pt.model.df = Complete_df
                pt.model.df.reset_index(drop=True)
                pt.update()
                pt.resetColors()
                pt.setRowColors(rows=range(1,len(ObserverSetCatchDB),2), clr='lightblue', cols='all')
                pt.cellbackgr = 'aliceblue'
                options = config.load_options()
                options = { 'align': 'center',
                            'cellbackgr': '#F4F4F3',
                            'cellwidth': 120,
                            'floatprecision': 2,
                            'thousandseparator': '',
                            'font': 'Arial',
                            'fontsize': 8,
                            'fontstyle': '',
                            'grid_color': '#ABB1AD',
                            'linewidth': 1,
                            'rowheight': 22,
                            'rowselectedcolor': '#E4DED4',
                            'textcolor': 'black'}
                config.apply_options(options, pt)
                pt.autoResizeColumns()
                pt.prodyutCustomsetindex2_1()
                button_SubmitToUpdateDB_PF.config(state="normal")

                button_SetUpAsIndexCols.config(state="disabled")
                button_SetUpDefaultIndexCols.config(state="disabled")
                button_ResetIndexCols.config(state="disabled")

                button_SetUpColChooser.config(state="normal")
                button_ResetChooseCols.config(state="normal")

                button_SetUuListCols.config(state="normal")
                button_ResetChooseColList.config(state="normal")

                button_ViewCleartable.config(state="normal")
                button_ReloadViewFlagged.config(state="normal")

            else:
                tkinter.messagebox.showinfo("DB Sorting Message - Table Entries Must Be Same Total DB Entries",
                                            "Unable To Sort, Please Check If There is Row Filter Applied Or Not")
        else:
            tkinter.messagebox.showinfo("Sorting Table Message",
                                        "Please Select Sorting Variable From DropDown")
    
    ### Alternate Procedure-2
    def SelectForUpdateEntry():
        SetCatchColNameList =  ['TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag',
                'DataBase_ID','RecordIdentifier','DeploymentUID',
				'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
				'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
				'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
				'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
				'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
				'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
				'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
				'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
				'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
				'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
				'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
				'NumberIndividuals']
        ListVariableListA = ['ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
                        'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
                        'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
                        'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
                        'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
                        'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
                        'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                        'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                        'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
                        'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
                        'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                        'NumberIndividuals']
        rows = pt.getSelectedRowData()
        SelectedvalueDepUID_DF = rows['DeploymentUID']
        SelectedvalueDepUID = SelectedvalueDepUID_DF.iloc[0]
        cols = pt.getSelectedColumn()
        SelectedVariableDF = rows.iloc[:,cols]
        SelectedVariableValue = SelectedVariableDF.iloc[0]
        SelectedVariable = (pd.DataFrame(SelectedVariableDF).columns.tolist())
        SelectedVariable = SelectedVariable[0]
        def findElements(lst1, lst2):
            return list(map(lst1.__getitem__, lst2))
        getColsSelectedCol = findElements(SetCatchColNameList, [cols])
        getColsSelectedCol = getColsSelectedCol[0]
        if SelectedVariable == getColsSelectedCol :
            if SelectedVariable in ListVariableListA:
                entry_DepUIDSelected.delete(0,END)
                entry_VariableSelected.delete(0,END)
                entry_VariableValue.delete(0,END)
                indexSelCol = ListVariableListA.index(SelectedVariable)
                entry_VariableSelected.current(indexSelCol)
                entry_DepUIDSelected.insert(tk.END,SelectedvalueDepUID)
                entry_VariableValue.insert(tk.END,SelectedVariableValue)
            else:
                entry_DepUIDSelected.delete(0,END)
                entry_VariableSelected.delete(0,END)
                entry_VariableValue.delete(0,END)
                entry_VariableSelected.current(len(ListVariableListA))

    def SetcatchDB_VariableList():
        GetSetCatchDB_VariableList = ['ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
                            'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
                            'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
                            'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
                            'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
                            'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
                            'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                            'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                            'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
                            'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
                            'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                            'NumberIndividuals']
        return GetSetCatchDB_VariableList
    
    def Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList):
        SetNoUpdateList = ['SpeciesCode', 'KeptWeight', 'DiscardWeight', 
                           'EstimatedWeightReleasedCrab', 'NumberIndividuals']
        UpdateSetList = UpdateRecordList
        if get_Updated_Variable not in SetNoUpdateList:
            GetSetCatchDB_VariableList = SetcatchDB_VariableList()
            ## Updating SetCatch DB
            conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
            cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET ASOCCode = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET ObserverNumber = ? WHERE DeploymentUID =?", 
                    UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Year = ? WHERE DeploymentUID =?", 
                        UpdateSetList)

            if get_Updated_Variable == GetSetCatchDB_VariableList[3]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DeploymentNumber = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[4]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SubTripNumber = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[5]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SetNumber = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[6]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Country = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[7]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Quota = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[8]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET SetType = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[9]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselSideNumber = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[10]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselClass = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[11]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselLength = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))

            if get_Updated_Variable == GetSetCatchDB_VariableList[12]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET VesselHorsepower = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[13]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Day = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[14]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Month = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[15]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET HaulDay = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[16]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET HaulMonth = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[17]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StartTime = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[18]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET Duration = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[19]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET PositionPrecision = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[20]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StartLatitude = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[21]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StartLongitude = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[22]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET EndLatitude = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[23]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET EndLongitude = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[24]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NAFODivision = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[25]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET UnitArea = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[26]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET StatisticalArea = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[27]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET InOut200MileLimit = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[28]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET GearType = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[29]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET CodendMeshSize = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[30]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET MeshSizeMG = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[31]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET MeshSizeFG = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[32]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET RollerBobbbinDiameter = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[33]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberGillnets = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[34]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageGillnetLength = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[35]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET GrateBarSpacing = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[36]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET FootropeLength = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[37]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberWindows = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[38]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberHooks = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[39]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberPots = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[40]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberPotReleasedCrab = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[41]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET GearDamage = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[42]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageTowSpeed = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[43]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET AverageDepth = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[44]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DataSource = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[45]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DirectedSpecies = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[46]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET NumberSpecies = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[47]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET RecordType = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[48]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET DetailedCatchSpeciesCompCode = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[49]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET LogbookIDNumber1 = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[50]:
                cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET LogbookIDNumber2 = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                        
            conn_DB_Set_Catch_Analysis.commit()
            conn_DB_Set_Catch_Analysis.close()

            ## Updating TowDistance DB
            conn_DB_SetCatch_Validation_Range= sqlite3.connect(DB_SetCatch_Validation_Range)
            cur_DB_SetCatch_Validation_Range=conn_DB_SetCatch_Validation_Range.cursor()
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[0]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET ASOCCode = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[1]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET ObserverNumber = ? WHERE DeploymentUID =?", 
                    UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[2]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET Year = ? WHERE DeploymentUID =?", 
                        UpdateSetList)

            if get_Updated_Variable == GetSetCatchDB_VariableList[3]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET DeploymentNumber = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[4]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET SubTripNumber = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[5]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET SetNumber = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[6]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET Country = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[7]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET Quota = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[8]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET SetType = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[9]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET VesselSideNumber = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[10]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET VesselClass = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[11]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET VesselLength = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))

            if get_Updated_Variable == GetSetCatchDB_VariableList[12]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET VesselHorsepower = ? WHERE DeploymentUID =?", 
                        (UpdateSetList))
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[13]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET Day = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[14]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET Month = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[15]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET HaulDay = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[16]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET HaulMonth = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[17]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET StartTime = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[18]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET Duration = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[19]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET PositionPrecision = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[20]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET StartLatitude = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[21]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET StartLongitude = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[22]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET EndLatitude = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[23]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET EndLongitude = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[24]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET NAFODivision = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[25]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET UnitArea = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[26]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET StatisticalArea = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[27]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET InOut200MileLimit = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[28]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET GearType = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[29]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET CodendMeshSize = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[30]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET MeshSizeMG = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[31]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET MeshSizeFG = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[32]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET RollerBobbbinDiameter = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[33]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET NumberGillnets = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[34]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET AverageGillnetLength = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[35]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET GrateBarSpacing = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[36]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET FootropeLength = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[37]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET NumberWindows = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[38]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET NumberHooks = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[39]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET NumberPots = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[40]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET NumberPotReleasedCrab = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[41]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET GearDamage = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[42]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET AverageTowSpeed = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[43]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET AverageDepth = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[44]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET DataSource = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                
            if get_Updated_Variable == GetSetCatchDB_VariableList[45]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET DirectedSpecies = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[46]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET NumberSpecies = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[47]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET RecordType = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[48]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET DetailedCatchSpeciesCompCode = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
            
            if get_Updated_Variable == GetSetCatchDB_VariableList[49]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET LogbookIDNumber1 = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                    
            if get_Updated_Variable == GetSetCatchDB_VariableList[50]:
                cur_DB_SetCatch_Validation_Range.executemany("UPDATE SetCatch_QCFailedRange_TowDistance SET LogbookIDNumber2 = ? WHERE DeploymentUID =?", 
                        UpdateSetList)
                        
            conn_DB_SetCatch_Validation_Range.commit()
            conn_DB_SetCatch_Validation_Range.close()
        else:
            messagebox.showerror('Wrong Variable Selection For Set Update', 
            "Set Update For Last five Variable From Table Not Allowed")
            ReloadDBAfterEntryUpdate()

    def QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable):
        # Performing QC On Variables Value And DataType
        Var_Class_IntA18=['DataBase_ID', 'RecordIdentifier', 'GearDamage',
                        'ASOCCode', 'Year', 'DeploymentNumber', 
                        'SetNumber', 'Country', 'Quota', 'SetType',
                        'VesselClass','Day', 'Month','PositionPrecision',
                        'GearType','RecordType','DirectedSpecies','DataSource']
        
        Var_Class_FloatA7= ['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                            'EndLongitude','AverageTowSpeed', 'VesselLength']
        
        Var_Class_String7 =['ObserverNumber', 'DeploymentUID', 
                            'SubTripNumber','NAFODivision', 'VesselSideNumber',
                            'UnitArea','DetailedCatchSpeciesCompCode']
        
        Var_Class_IntB27  = ['VesselHorsepower','HaulDay','HaulMonth', 'StartTime',
                            'StatisticalArea', 'InOut200MileLimit',  'CodendMeshSize',
                            'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 
                            'NumberGillnets', 'AverageGillnetLength', 'GrateBarSpacing', 
                            'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                            'NumberPotReleasedCrab','AverageDepth','NumberSpecies', 'LogbookIDNumber1', 
                            'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 
                            'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                            'NumberIndividuals']

        ReturnFail ="ReturnFail"

        if get_Updated_Variable in Var_Class_IntA18:
            if(len(get_UpdateValue_UpdatedVariable)!=0):
                try:
                    get_UpdateValue_UpdatedVariable = int(get_UpdateValue_UpdatedVariable)
                    return get_UpdateValue_UpdatedVariable
                except:
                    messagebox.showerror('Update Variable Datatype Error Message', "Updated Value Must Be Integer Value")
                    return ReturnFail
            else:
                messagebox.showerror('Update Variable Error Message',
                                    "Updated Value Can Not Be Null")
                return ReturnFail
        
        if get_Updated_Variable in Var_Class_FloatA7:
            if(len(get_UpdateValue_UpdatedVariable)!=0):
                try:
                    get_UpdateValue_UpdatedVariable = float(get_UpdateValue_UpdatedVariable)
                    return get_UpdateValue_UpdatedVariable
                except:
                    messagebox.showerror('Update Variable Datatype Error Message', 
                                        "Updated Value Must Be Float Value")
                    return ReturnFail
            else:
                get_UpdateValue_UpdatedVariable = (get_UpdateValue_UpdatedVariable)
                return get_UpdateValue_UpdatedVariable

        if get_Updated_Variable in Var_Class_String7:
            if(len(get_UpdateValue_UpdatedVariable)!=0):
                try:
                    get_UpdateValue_UpdatedVariable = int(get_UpdateValue_UpdatedVariable)
                    return get_UpdateValue_UpdatedVariable
                except:
                    get_UpdateValue_UpdatedVariable = (get_UpdateValue_UpdatedVariable)
                    return get_UpdateValue_UpdatedVariable
            else:
                get_UpdateValue_UpdatedVariable = 'None'
                return get_UpdateValue_UpdatedVariable
        
        if get_Updated_Variable in Var_Class_IntB27:
            if(len(get_UpdateValue_UpdatedVariable)!=0):
                try:
                    get_UpdateValue_UpdatedVariable = int(get_UpdateValue_UpdatedVariable)
                    return get_UpdateValue_UpdatedVariable
                except:
                    messagebox.showerror('Update Variable Datatype Error Message', "Updated Value Must Be Integer Value")
                    return ReturnFail
            else:
                get_UpdateValue_UpdatedVariable = (get_UpdateValue_UpdatedVariable)
                return get_UpdateValue_UpdatedVariable

    def ReloadDBAfterEntryUpdate():
        Return_ObserverSetCatchDB = get_ObserverSetCatchDB()
        ObserverSetCatchDB = Return_ObserverSetCatchDB[0]
        entry_DBEntries.delete(0,END)
        entry_Flagged.delete(0,END)
        entry_DBEntries.insert(tk.END,Return_ObserverSetCatchDB[1])
        entry_Flagged.insert(tk.END,Return_ObserverSetCatchDB[2])
        ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                ['TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag',
				'DataBase_ID','RecordIdentifier','DeploymentUID',
				'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
				'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
				'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
				'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
				'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
				'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
				'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
				'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
				'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
				'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
				'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
				'NumberIndividuals']]
        ObserverSetCatchDB.sort_values(by=['Year', 'ASOCCode', 
        'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
        ObserverSetCatchDB['ViewDepUID'] = ObserverSetCatchDB.loc[:, 'DeploymentUID']
        ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)
        pt.prodyutCustomclearTable()
        pt.model.df = ObserverSetCatchDB
        pt.model.df.reset_index(drop=True)
        pt.update()
        pt.resetColors()
        pt.setRowColors(rows=range(1,len(ObserverSetCatchDB),2), clr='lightblue', cols='all')
        pt.cellbackgr = 'aliceblue'
        options = config.load_options()
        options = { 'align': 'center',
                    'cellbackgr': '#F4F4F3',
                    'cellwidth': 120,
                    'floatprecision': 2,
                    'thousandseparator': '',
                    'font': 'Arial',
                    'fontsize': 8,
                    'fontstyle': '',
                    'grid_color': '#ABB1AD',
                    'linewidth': 1,
                    'rowheight': 22,
                    'rowselectedcolor': '#E4DED4',
                    'textcolor': 'black'}
        config.apply_options(options, pt)
        pt.autoResizeColumns()
        pt.prodyutCustomsetindex2_1()
        button_SubmitToUpdateDB_PF.config(state="normal")
        button_SetUpColChooser.config(state="normal")
        button_SetUpAsIndexCols.config(state="disabled")
        button_SetUpDefaultIndexCols.config(state="disabled")
    
    def UpdateSelected_SetCatch_DBEntries():
        ReturnFail ="ReturnFail"
        DepUIDUpdateList = ['ASOCCode', 'Year', 'DeploymentNumber', 'SetNumber']
        get_Updated_Variable = entry_VariableSelected.get()
        get_UpdateValue_UpdatedVariable = entry_VariableValue.get()
        get_Selested_DepUID = entry_DepUIDSelected.get()
        get_UpdateValue_UpdatedVariable = QCOnVariableType(get_Updated_Variable, get_UpdateValue_UpdatedVariable)
        if (get_UpdateValue_UpdatedVariable != ReturnFail) & (len(get_Updated_Variable)!=0):
            ListBox_DF = pd.DataFrame(pt.model.df)
            ## Update SetCatch DB
            if (len(ListBox_DF)>0)& (len(ListBox_DF)<20001):          
                
                if(len(get_Updated_Variable)==0) & ((get_UpdateValue_UpdatedVariable)==''):
                    messagebox.showerror('Update Entries Missing',
                                    "Selection of Variable From List Entries Or Updated \
                                    Variable Value Entry Missing Or Both Entries Missing")
                    
                if(len(get_Updated_Variable)==0) & ((get_UpdateValue_UpdatedVariable)!=''):
                    messagebox.showerror('Update Entries Missing',
                                        "Selection of Variable From List Entries Or Updated \
                                        Variable Value Entry Missing Or Both Entries Missing")

                if(len(get_Updated_Variable)!=0) & ((get_UpdateValue_UpdatedVariable)!=''):
                    UpdateRecordList =[]
                    list_item_DeploymentUID = get_Selested_DepUID
                    UpdateRecordList.append((get_UpdateValue_UpdatedVariable, list_item_DeploymentUID))
                    Lookup_User_DB_Variable_UpdateDB(get_Updated_Variable, UpdateRecordList)
                    ReloadDBAfterEntryUpdate()
                    tkinter.messagebox.showinfo("Update Success","Successfully Updated The Selected Entries")

            # Empty Selection Case
            if (len(ListBox_DF)<=0):
                tkinter.messagebox.showinfo("Update Error",
                "Empty Set & Catch Table Selection Please Select At least One Entries In the Table To Update The Variable")
            
            # Max Limit Update Exceed Case Limiting Because Of Slow Performance 
            if (len(ListBox_DF)>20000):
                tkinter.messagebox.showinfo("Update Selection Max Case","Max Limit For Update Selection Is 20,000 \
                Please Select A Batch Of 20,000 Entries Each Time If You Need To Update More")  
        
        else:
            messagebox.showerror('Update Error',
                                "Please Check Variable DataType And Follow Proper Update Step") 

    ### Alternate Procedure-1
    def AddEntriesForUpdate():
        Entriesupdate = pt.prodyutcustomAddUpdate()
        ObserverSetCatchDB = pd.DataFrame(Entriesupdate, index=None)
        ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(Entriesupdate, index=None)
        AddForSubmitToUpdateDB(ObserverSetCatchDB)
    
    def AddForSubmitToUpdateDB(ObserverSetCatchDB):
        Complete_df = pd.DataFrame(ObserverSetCatchDB)
        if len(Complete_df) >0:
            Complete_df = SetCatchDFQC(Complete_df)
            Complete_df  = Complete_df.reset_index(drop=True)
            Complete_df = pd.DataFrame(Complete_df)
            iSubmit = tkinter.messagebox.askyesno("Submit DFO-NL ASOP Set & Catch Edited Table",
                    "Confirm If You Want to Submit?")
            if iSubmit >0:
                try:
                    Complete_df = pd.DataFrame(Complete_df)
                    BackendAddForSubmitToUpdateDB(Complete_df)
                except:
                    print('Error Occured In DataBase')
                finally:
                    pt.redraw()
                    tkinter.messagebox.showinfo("Submitted To Set&Catch DB","Successfully Submitted To Update DB")      
        else:
            tkinter.messagebox.showinfo("Empty Set&Catch DB","Empty Set&Catch DB, Please Import Set&Catch CSV File To Submit")

    def BackendAddForSubmitToUpdateDB(Complete_df):
        try:
            Submit_To_DBStorage = pd.DataFrame(Complete_df)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = sqliteConnection.cursor()
            Submit_To_DBStorage.to_sql('SetCatch_QCFailedRange_TempTowDistance', sqliteConnection, 
                                        if_exists="append", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()
        
    def get_AddedEntries():
        try:
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = sqliteConnection.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_QCFailedRange_TempTowDistance;", sqliteConnection)
            length_Complete_df = len(Complete_df)
            if length_Complete_df > 0:
                Complete_df = Complete_df.reset_index(drop=True)
                ObserverSetCatchDB = pd.DataFrame(Complete_df)
                lengthAdded = len(ObserverSetCatchDB)
                sqliteConnection.commit()
                return ObserverSetCatchDB, lengthAdded
            else:
                messagebox.showerror('Set & Catch Database Is Empty', "Empty Selected Entries")
                ObserverSetCatchDB = pd.DataFrame(Complete_df)
                return ObserverSetCatchDB, 0
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def ViewSubmitForUpdate():
        Return_ObserverSetCatchDB = get_AddedEntries()
        ObserverSetCatchDB = Return_ObserverSetCatchDB[0]
        if (len(ObserverSetCatchDB) > 0) :
            root1 = tk.Toplevel(windows)
            root1.title ("ExcelView Added Set&Catch Entries")
            root1.geometry('1100x855+40+40')
            root1.config(bg="cadet blue")
            def on_close():
                tkinter.messagebox.ABORT = 'abort'
            frame1 = tk.Frame(root1)
            frame1.pack(fill=BOTH, expand=1)
            ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                ['TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag',
				'DataBase_ID','RecordIdentifier','DeploymentUID',
				'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
				'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
				'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
				'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
				'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
				'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
				'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
				'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
				'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
				'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
				'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
				'NumberIndividuals']]
            ObserverSetCatchDB.sort_values(by=['Year', 'ASOCCode', 
                'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
            ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
            ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)
            pt1 = Table(frame1, dataframe = ObserverSetCatchDB, showtoolbar=True, showstatusbar=True)
            pt1.setRowColors(rows=range(1,len(ObserverSetCatchDB),2), clr='lavender', cols='all')
            pt1.cellbackgr = 'aliceblue'
            options = config.load_options()
            options = { 'align': 'center',
                        'cellbackgr': '#F4F4F3',
                        'cellwidth': 120,
                        'floatprecision': 2,
                        'thousandseparator': '',
                        'font': 'Arial',
                        'fontsize': 8,
                        'fontstyle': '',
                        'grid_color': '#ABB1AD',
                        'linewidth': 1,
                        'rowheight': 22,
                        'rowselectedcolor': '#E4DED4',
                        'textcolor': 'black'}
            config.apply_options(options, pt1)
            pt1.autoResizeColumns()
            pt1.show()
            button_AddSubmitdpdate.config(state="disabled")
            
            def SubmitToUpdateDB():
                Complete_df = pd.DataFrame(ObserverSetCatchDB)
                if len(Complete_df) >0:
                    Complete_df  = pd.DataFrame(pt1.model.df)
                    Complete_df= (Complete_df.loc[:,
                        ['DataBase_ID','RecordIdentifier','DeploymentUID',
                        'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
                        'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
                        'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
                        'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
                        'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
                        'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
                        'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                        'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                        'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
                        'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
                        'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                        'NumberIndividuals']]).replace(['', None, np.nan, 
                        'None', ' ', '  ', '   ', '    '], 99999999)

                    Complete_df[['DataBase_ID', 'RecordIdentifier', 'GearDamage',
                                'ASOCCode', 'Year', 'DeploymentNumber', 
                                'SetNumber', 'Country', 'Quota', 'SetType',
                                'VesselClass','Day', 'Month','PositionPrecision',
                                'GearType','RecordType','DirectedSpecies','DataSource', 
                                'VesselHorsepower','HaulDay','HaulMonth', 'StartTime',
                                'StatisticalArea', 'InOut200MileLimit',  'CodendMeshSize',
                                'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 
                                'NumberGillnets', 'AverageGillnetLength', 'GrateBarSpacing', 
                                'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                                'NumberPotReleasedCrab','AverageDepth','NumberSpecies', 'LogbookIDNumber1', 
                                'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 
                                'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                                'NumberIndividuals']] = Complete_df[
                                ['DataBase_ID', 'RecordIdentifier', 'GearDamage',
                                'ASOCCode', 'Year', 'DeploymentNumber', 
                                'SetNumber', 'Country', 'Quota', 'SetType',
                                'VesselClass','Day', 'Month','PositionPrecision',
                                'GearType','RecordType','DirectedSpecies','DataSource', 
                                'VesselHorsepower','HaulDay','HaulMonth', 'StartTime',
                                'StatisticalArea', 'InOut200MileLimit',  'CodendMeshSize',
                                'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 
                                'NumberGillnets', 'AverageGillnetLength', 'GrateBarSpacing', 
                                'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                                'NumberPotReleasedCrab','AverageDepth','NumberSpecies', 'LogbookIDNumber1', 
                                'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 
                                'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                                'NumberIndividuals']].astype(int)
                    
                    Complete_df[['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                        'EndLongitude','AverageTowSpeed', 'VesselLength']] = Complete_df[
                        ['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                        'EndLongitude','AverageTowSpeed', 'VesselLength']].astype(float)
                        
                    Complete_df['VesselSideNumber'] = pd.to_numeric(Complete_df[
                                'VesselSideNumber'], downcast='integer', errors='ignore')
                    
                    Complete_df['SubTripNumber'] = pd.to_numeric(Complete_df[
                                'SubTripNumber'], downcast='integer', errors='ignore')
                        
                    Complete_df[['ObserverNumber', 'DeploymentUID', 
                                'SubTripNumber','NAFODivision', 'VesselSideNumber',
                                'UnitArea','DetailedCatchSpeciesCompCode']] = Complete_df[
                                ['ObserverNumber', 'DeploymentUID', 
                                'SubTripNumber','NAFODivision', 'VesselSideNumber',
                                'UnitArea','DetailedCatchSpeciesCompCode']].astype(str)
                    
                    Complete_df = Complete_df.loc[:,
                        ['DataBase_ID','RecordIdentifier','DeploymentUID',
                        'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
                        'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
                        'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
                        'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
                        'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
                        'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
                        'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                        'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                        'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
                        'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
                        'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                        'NumberIndividuals']]

                    Complete_df = Complete_df.replace([99999999, 99999999.0, np.nan], '')
                    Complete_df = Complete_df.replace(['99999999.0', '99999999', '.'], 'None')
                    Complete_df  = Complete_df.reset_index(drop=True)
                    Complete_df = pd.DataFrame(Complete_df)
                    iSubmit = tkinter.messagebox.askyesno("Submit DFO-NL ASOP Set & Catch Edited Table",
                            "Confirm If You Want to Submit DFO-NL ASOP Set & Catch Edited Table To QC Database ?")
                    if iSubmit >0:
                        try:
                            Complete_df = pd.DataFrame(Complete_df)
                            BackendSubmitAndUpdateDB(Complete_df)
                        except:
                            print('Error Occured In DataBase')
                        finally:
                            pt.redraw()
                            tkinter.messagebox.showinfo("Submitted To Set&Catch DB","Successfully Submitted To Update DB")      
                else:
                    tkinter.messagebox.showinfo("Empty Set&Catch DB",
                    "Empty Set&Catch DB, Please Import Set&Catch CSV File To Submit")

            def ReloadAddEntries():
                pt1.prodyutCustomclearTable()
                Return_ObserverSetCatchDB = get_AddedEntries()
                ObserverSetCatchDB = Return_ObserverSetCatchDB[0]
                pt1.model.df = ObserverSetCatchDB
                pt1.model.df.reset_index(drop=True)
                pt1.update()
                pt1.resetColors()
                pt1.setRowColors(rows=range(1,len(ObserverSetCatchDB),2), clr='lightblue', cols='all')
                pt1.cellbackgr = 'aliceblue'
                options = config.load_options()
                options = { 'align': 'center',
                            'cellbackgr': '#F4F4F3',
                            'cellwidth': 120,
                            'floatprecision': 2,
                            'thousandseparator': '',
                            'font': 'Arial',
                            'fontsize': 8,
                            'fontstyle': '',
                            'grid_color': '#ABB1AD',
                            'linewidth': 1,
                            'rowheight': 22,
                            'rowselectedcolor': '#E4DED4',
                            'textcolor': 'black'}
                config.apply_options(options, pt1)

            ProcedureFrame = Frame(root1, width = 40,  bd = 2,relief = RIDGE, bg= "cadet blue")
            ProcedureFrame.pack(side = LEFT, padx= 15, pady=0)
            lbl_HeaderDefine_PF = Label(ProcedureFrame, font=('aerial', 11, 'bold'),
                                    bg= "cadet blue", text="A: Procedure To Edit & Update & Submit")
            lbl_HeaderDefine_PF.grid(row =0, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            lbl_Step_1Procedure_PF = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                                    bg= "cadet blue", text="1 : Double Click On TreeView Cell For Edit, Except")
            lbl_Step_1Procedure_PF.grid(row =1, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            lbl_Step_1_0Procedure_PF = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                                    bg= "cadet blue", text=" DataBase_ID And RecordIdentifier And RecordType ")
            lbl_Step_1_0Procedure_PF.grid(row =2, column = 0, columnspan=1 ,padx=12, pady =2, sticky =W)

            lbl_Step_1_1Procedure_PF = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                                    bg= "cadet blue", text="2 : Press Enter (Must) To Modify  Cell Value")
            lbl_Step_1_1Procedure_PF.grid(row =3, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            lbl_Step_2Procedure_PF = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                                    bg= "cadet blue", text="3 : Submit Edited Table To Update Set & Catch QC DB ")
            lbl_Step_2Procedure_PF.grid(row =6, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            button_SubmitToUpdateDB_PF = Button(ProcedureFrame, bd = 2, text ="Submit To Update DB", width =18,
                                        height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                        command =SubmitToUpdateDB)
            button_SubmitToUpdateDB_PF.grid(row =8, column = 0, padx=2, pady =1, ipady =1, sticky =W)

            lbl_CautionSteps_2_PF = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="NB : Edit/Modify DeplymentUID Columns Requires - ")
            lbl_CautionSteps_2_PF.grid(row =11, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            lbl_CautionSteps_3_PF = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text=" Modify Year/ASOC/DepN/SetN Accordingly")
            lbl_CautionSteps_3_PF.grid(row =12, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

            ReloadFrame = Frame(root1, width = 40,  bd = 2,relief = RIDGE, bg= "cadet blue")
            ReloadFrame.pack(side = LEFT, padx= 15, pady=0)
            

            button_ReloadDB = Button(ReloadFrame, bd = 2, text ="Reload Add Entries DataBase", width =24,
                                        height=2, font=('aerial', 14, 'bold'), fg="blue", bg="cadet blue", 
                                        command =ReloadAddEntries)
            button_ReloadDB.grid(row =1, column = 0, padx=2, pady =1, ipady =1, sticky =W)

            root1.protocol("WM_DELETE_WINDOW",  on_close)
            root1.mainloop()

    ## Bottom Left Frame- ProcedureFrame Define
    ProcedureFrame = Frame(windows, width = 40,  bd = 2,relief = RIDGE, bg= "cadet blue")
    ProcedureFrame.pack(side = LEFT, padx= 0, pady=0)
    lbl_HeaderDefine_PF = Label(ProcedureFrame, font=('aerial', 11, 'bold'),
                            bg= "cadet blue", text="A: QC Table Edit-Update & Submit")
    lbl_HeaderDefine_PF.grid(row =0, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_Step_1Procedure_PF = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="1 : Double Click On Cell For Edit, Except")
    lbl_Step_1Procedure_PF.grid(row =1, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_Step_1_0Procedure_PF = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text=" (DB_ID, RecId, RecType, DepUID) ")
    lbl_Step_1_0Procedure_PF.grid(row =2, column = 0, columnspan=1 ,padx=12, pady =2, sticky =W)

    lbl_Step_1_1Procedure_PF = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="2 : Press Enter (Must) To Modify  Cell Value")
    lbl_Step_1_1Procedure_PF.grid(row =3, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_Step_2Procedure_PF = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="3 : Submit QC Table To Update DB ")
    lbl_Step_2Procedure_PF.grid(row =6, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    button_SubmitToUpdateDB_PF = Button(ProcedureFrame, bd = 2, text ="Submit To Update DB", width =18,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =SubmitToUpdateDB)
    button_SubmitToUpdateDB_PF.grid(row =8, column = 0, padx=12, pady =1, ipady =1, sticky =W)

    lbl_CautionSteps_2_PF = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                    bg= "cadet blue", text="NB : Edit Year/ASOC/DepN/SetN Cols Requires")
    lbl_CautionSteps_2_PF.grid(row =11, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_CautionSteps_3_PF = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                    bg= "cadet blue", text="Modify DepUID (In B-1/2 Module) Accordingly")
    lbl_CautionSteps_3_PF.grid(row =12, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_CautionSteps_4_PF = Label(ProcedureFrame, font=('aerial', 9, 'bold'),
                    bg= "cadet blue", text="NB : Submit To DB : After All Table Edit ")
    lbl_CautionSteps_4_PF.grid(row =13, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    ## Frame Of Customized Column View -B : Column Chooser
    CuscolView_SetResetframe = tk.Frame(windows, bd = 2,relief = RIDGE, bg= "cadet blue")
    CuscolView_SetResetframe.pack(side =LEFT, padx=5, pady =2)

    lbl_AddStepProcess_CLV = Label(CuscolView_SetResetframe, font=('aerial', 11, 'bold'),
                            bg= "cadet blue", text="B: View - Select & Move Columns")
    lbl_AddStepProcess_CLV.grid(row =0, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_Step1_ColChooser_CLV = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="1 : Select Columns To Move First")
    lbl_Step1_ColChooser_CLV.grid(row =2, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_Step2_ColChooser_CLV = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="2 : Set-Up Column Chooser")
    lbl_Step2_ColChooser_CLV.grid(row =3, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    button_SetUpColChooser = Button(CuscolView_SetResetframe, bd = 2, text ="Set-Up Column Chooser", width =20,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =SetColumnChooser)
    button_SetUpColChooser.grid(row =4, column = 0, padx=2, pady =1, ipady =1, sticky =W)

    lbl_OrMsg_CS = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="OR Run Set-Up")
    lbl_OrMsg_CS.grid(row =5, column = 0, padx=30, pady =2, sticky =W)

    button_SetUpDefColchoser = Button(CuscolView_SetResetframe, bd = 2, text ="Default Column Chooser", width =20,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =DefaultColChooser)
    button_SetUpDefColchoser.grid(row =6, column = 0, padx=2, pady =1, ipady =1, sticky =W)

    lbl_Step3_SetResetColChooser = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="3 : Reset Column Chooser (Must)")
    lbl_Step3_SetResetColChooser.grid(row =7, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    button_ResetChooseCols = Button(CuscolView_SetResetframe, bd = 2, text ="Reset Column Chooser", width =20,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ResetColumnChooser)
    button_ResetChooseCols.grid(row =8, column = 0, padx=2, pady =1, ipady =1, sticky =W)

     ## Frame Of Customized Column View C : Column List view
    CuscolView_SetResetframe = tk.Frame(windows, bd = 2,relief = RIDGE, bg= "cadet blue")
    CuscolView_SetResetframe.pack(side =LEFT, padx=5, pady =2)

    lbl_AddStepProcess_List = Label(CuscolView_SetResetframe, font=('aerial', 11, 'bold'),
                            bg= "cadet blue", text="C: View - Select From List")
    lbl_AddStepProcess_List.grid(row =0, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_Step1_ColList_CLV = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="1 : Select From List & View Button Below")
    lbl_Step1_ColList_CLV.grid(row =1, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    button_SetUuListCols = Button(CuscolView_SetResetframe, bd = 2, text ="Set-Up Select From List & View", width =25,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =RunSelCols_SetAndCatchDB)
    button_SetUuListCols.grid(row =2, column = 0, padx=2, pady =1, ipady =1, sticky =W)

    lbl_Step2_ColList = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="2 : Select Columns from List OR")
    lbl_Step2_ColList.grid(row =3, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_OrMsg_CL = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="3 : Run Default Column List View")
    lbl_OrMsg_CL.grid(row =5, column = 0, padx=2, pady =2, sticky =W)

    button_SetUpDefColList = Button(CuscolView_SetResetframe, bd = 2, text ="Default Column List & View", width =25,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =RunDefaultSelCols_SetAndCatchDB)
    button_SetUpDefColList.grid(row =6, column = 0, padx=2, pady =1, ipady =1, sticky =W)

    lbl_Step3_SetResetColList = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="4 : Reset Column List View (Must)")
    lbl_Step3_SetResetColList.grid(row =7, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    button_ResetChooseColList = Button(CuscolView_SetResetframe, bd = 2, text ="Reset Column List & View", width =25,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ResetListViewSelCol)
    button_ResetChooseColList.grid(row =8, column = 0, padx=2, pady =1, ipady =1, sticky =W)

    ## Frame Of Customized Column View -D: Set/Reset Index 
    CuscolView_SetResetframe = tk.Frame(windows, bd = 2,relief = RIDGE, bg= "cadet blue")
    CuscolView_SetResetframe.pack(side =LEFT, padx=3, pady =2)

    lbl_AddStepProcess_CLV = Label(CuscolView_SetResetframe, font=('aerial', 11, 'bold'),
                            bg= "cadet blue", text="D: View - By Set/Reset Index")
    lbl_AddStepProcess_CLV.grid(row =0, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_Step1_SetResetIndex_CLV = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="1 : Choose Index Columns (Max 3)")
    lbl_Step1_SetResetIndex_CLV.grid(row =2, column = 0, columnspan=1 ,padx=12, pady =2, sticky =W)

    lbl_Step2_SetResetIndex_CLV = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="2 : Set-Up Index Columns")
    lbl_Step2_SetResetIndex_CLV.grid(row =3, column = 0, columnspan=1 ,padx=12, pady =2, sticky =W)

    button_SetUpAsIndexCols = Button(CuscolView_SetResetframe, bd = 2, text ="Set-Up Index Columns", width =20,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =SetIndexDF)
    button_SetUpAsIndexCols.grid(row =4, column = 0, padx=12, pady =1, ipady =1, sticky =W)

    lbl_OrMsg_CLV = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="OR Run Set-Up")
    lbl_OrMsg_CLV.grid(row =5, column = 0, padx=30, pady =2, sticky =W)

    button_SetUpDefaultIndexCols = Button(CuscolView_SetResetframe, bd = 2, text ="Default Index Columns", width =20,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =DefaultSetIndexDF)
    button_SetUpDefaultIndexCols.grid(row =6, column = 0, padx=12, pady =1, ipady =1, sticky =W)

    lbl_Step3_SetResetIndex_CLV = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="3 : Reset Index Columns (Must)")
    lbl_Step3_SetResetIndex_CLV.grid(row =7, column = 0, columnspan=1 ,padx=12, pady =2, sticky =W)

    button_ResetIndexCols = Button(CuscolView_SetResetframe, bd = 2, text ="Reset Index Columns", width =20,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ReSetIndexDF)
    button_ResetIndexCols.grid(row =8, column = 0, padx=12, pady =1, ipady =1, sticky =W)

    ## Frame Of Alternate Update-1 -E 
    SelectedEntriesframe = tk.Frame(windows, bd = 2,relief = RIDGE, bg= "cadet blue")
    SelectedEntriesframe.pack(side =LEFT, padx=5, pady =2)

    lbl_AddStepProcess_CLV = Label(SelectedEntriesframe, font=('aerial', 11, 'bold'),
                            bg= "cadet blue", text="E: Alternate Update Procedure -1")
    lbl_AddStepProcess_CLV.grid(row =0, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_Step0_AddEntries_CLV = Label(SelectedEntriesframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="1 : Select Row For Update ")
    lbl_Step0_AddEntries_CLV.grid(row =2, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_Step1_AddEntries_CLV = Label(SelectedEntriesframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="2 : Edit/Update Selected Row Cell ")
    lbl_Step1_AddEntries_CLV.grid(row =3, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_Step2_AddEntries_CLV = Label(SelectedEntriesframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="3 : Hit Add Entries For Update Button")
    lbl_Step2_AddEntries_CLV.grid(row =4, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    button_AddSelectedpdate = Button(SelectedEntriesframe, bd = 2, text ="Add Entries For Update", width =22,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =AddEntriesForUpdate)
    button_AddSelectedpdate.grid(row =5, column = 0, padx=2, pady =1, ipady =1, sticky =W)

    lbl_Step3_AddEntries_CLV = Label(SelectedEntriesframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="4 : Hit View & Submit Button Below")
    lbl_Step3_AddEntries_CLV.grid(row =6, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    button_AddSubmitdpdate = Button(SelectedEntriesframe, bd = 2, text ="View & Submit For Update", width =22,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ViewSubmitForUpdate)
    button_AddSubmitdpdate.grid(row =7, column = 0, padx=2, pady =1, ipady =1, sticky =W)

    button_ViewAfterUpdate = Button(SelectedEntriesframe, bd = 2, text ="View & Refreash Update", width =22,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ReloadDBAfterEntryUpdate)
    button_ViewAfterUpdate.grid(row =8, column = 0, padx=2, pady =1, ipady =1, sticky =W)

    ## Frame Of Alternate Update-2 -F
    QCEditDBEntry = tk.Frame(windows, bd = 2,relief = RIDGE, bg= "cadet blue")
    QCEditDBEntry.pack(side =LEFT, padx=3, pady =2)

    lbl_QCEditDBEntry = Label(QCEditDBEntry, font=('aerial', 11, 'bold'),
                            bg= "cadet blue", text="F: Alternate Update Procedure - 2")
    lbl_QCEditDBEntry.grid(row =0, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_Step1_QCEditDBEntry = Label(QCEditDBEntry, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="1 : Select Table Cell Entry")
    lbl_Step1_QCEditDBEntry.grid(row =2, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    button_Selforupdate = Button(QCEditDBEntry, bd = 2, text ="Select For Edit & Update", width =20,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command = SelectForUpdateEntry)
    button_Selforupdate.grid(row =3, column = 0, padx=2, pady =2, ipady =2, sticky =W)

    lbl_SelectedVar_A = Label(QCEditDBEntry, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text=" A. DeploymentUID :")
    lbl_SelectedVar_A.grid(row =5, column = 0, padx=4, pady =1, sticky =W)
    
    DepUIDSelected       = IntVar(QCEditDBEntry, value ='SelectedDeptUID')
    entry_DepUIDSelected = Entry(QCEditDBEntry, font=('aerial', 8, 'bold'), justify='left',
                                textvariable = DepUIDSelected, width = 22, bd=2)
    entry_DepUIDSelected.grid(row =5, column = 0, padx=140, pady =1, ipady =1, sticky =W)

    lbl_SelectedVar_B = Label(QCEditDBEntry, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text=" B. QCVariable :")
    lbl_SelectedVar_B.grid(row =6, column = 0, padx=4, pady =1, sticky =W)
    
    ListVariableListA = ['ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
                        'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
                        'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
                        'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
                        'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
                        'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
                        'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                        'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                        'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
                        'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
                        'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
                        'NumberIndividuals', '']
    VariableListA        = StringVar(QCEditDBEntry, value ='Selected Variable')
    entry_VariableSelected = ttk.Combobox(QCEditDBEntry, font=('aerial', 8, 'bold'), 
                                        textvariable = VariableListA, width = 19, state='readonly')
    entry_VariableSelected.grid(row =6, column = 0, padx=140, pady =1, ipady =1, sticky =W)
    entry_VariableSelected['values'] = (list(ListVariableListA))

    lbl_SelectedVar_C = Label(QCEditDBEntry, font=('aerial', 10, 'bold'),
                                    bg= "cadet blue", text=" C. QCVariale Value :")
    lbl_SelectedVar_C.grid(row =7, column = 0, padx=4, pady =1, sticky =W)
    
    VariableSelected       = IntVar(QCEditDBEntry, value ='UpdatedValue')
    entry_VariableValue = Entry(QCEditDBEntry, font=('aerial', 8, 'bold'), justify='left',
                                textvariable = VariableSelected, width = 18, bd=2)
    entry_VariableValue.grid(row =7, column = 0, padx=160, pady =1, ipady =1, sticky =W)

    lbl_Step3_QCEditDBEntry = Label(QCEditDBEntry, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="2 : Hit Submit & Update Selected Entry To DB ")
    lbl_Step3_QCEditDBEntry.grid(row =8, column = 0, columnspan=1 ,padx=2, pady =1, sticky =W)

    button_SubmitForUpdate = Button(QCEditDBEntry, bd = 2, text ="Submit Updated Entry", width =20,
                            height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                            command = UpdateSelected_SetCatch_DBEntries)
    button_SubmitForUpdate.grid(row =9, column = 0, padx=2, pady =1, ipady =1, sticky =W)

    ## Header Frame
    button_ReloadView = Button(HeaderFrame, bd = 2, text ="↓ Ascending Sort ↓ ", width =16,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ViewAssendingSortVariable)
    button_ReloadView.grid(row =0, column = 2, columnspan=1 ,padx=2, pady =2, sticky =W)

    button_SortHighToLow = Button(HeaderFrame, bd = 2, text ="↑ Descending Sort ↑ ", width =16,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ViewDesendingSortVariable)
    button_SortHighToLow.grid(row =0, column = 3, columnspan=1 ,padx=2, pady =2, sticky =W)

    button_ReloadViewFlagged = Button(HeaderFrame, bd = 2, text ="Reload DB & View All Flagged Entries", width =32,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ReloadDBViewAllFlaggedEntries)
    button_ReloadViewFlagged.grid(row =0, column = 6, padx=2, pady =1, ipady =1, sticky =W)

    button_ViewCleartable = Button(HeaderFrame, bd = 2, text ="Clear View", width =9,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ViewClearView)
    button_ViewCleartable.grid(row =0, column = 7, padx=2, pady =1, ipady =1, sticky =W)

    button_ViewAllFlagged = Button(HeaderFrame, bd = 2, text ="QC Fail Flagged Entries", width =20,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ViewQCfailFlaggedEntries)
    button_ViewAllFlagged.grid(row =0, column = 8, padx=12, pady =1, ipady =1, sticky =W)

    ## Adding File Menu 
    menu = Menu(windows)
    windows.config(menu=menu)
    
    filemenu  = Menu(menu, tearoff=0)
    View  = Menu(menu, tearoff=0)

    menu.add_cascade(label="File", menu=filemenu)
    menu.add_cascade(label="View", menu=View)
    
    filemenu.add_command(label="Exit", command=iExit)
    View.add_command(label="View Analysis On Set&Catch DB", command='')

    windows.mainloop()

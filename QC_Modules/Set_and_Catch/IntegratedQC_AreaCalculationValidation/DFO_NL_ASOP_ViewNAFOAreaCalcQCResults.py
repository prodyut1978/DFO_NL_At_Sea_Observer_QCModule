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
DB_SetCatch_Val_Calculation = ("./BackEnd/Sqlite3_DB/QC_Check_CalculationConsistency_DB/DFO_NL_ASOP_SetCatch_Calculation.db")

def ViewCalcValidatedResult_NAFOArea():
    windows = tk.Toplevel()
    windows.title ("DFO-NL-ASOP NAFO Area Validator - ID-D-03-0")
    windows.geometry('1520x855+40+40')
    windows.config(bg="cadet blue")

    HeaderFrame = tk.Frame(windows, width = 40,  bd = 2,relief = RIDGE, bg= "cadet blue")
    HeaderFrame.pack(side = TOP, padx= 0, pady=0)

    lbl_SortLabel = Label(HeaderFrame, font=('aerial', 11, 'bold'),
            bg= "cadet blue", text="NAFO Area QC Table: ")
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

    lbl_TotalFlagged = Label(HeaderFrame, font=('aerial', 11, 'bold'),
            bg= "cadet blue", text="Total Flagged Entries : ")
    lbl_TotalFlagged.grid(row =0, column = 8, columnspan=1 ,padx=1, pady =2, sticky =W)
    EntryFlagged       = IntVar(HeaderFrame, value ='')
    entry_Flagged = Entry(HeaderFrame, font=('aerial', 10), justify='center',
                                textvariable = EntryFlagged, width = 6, bd=2)
    entry_Flagged.grid(row =0, column = 9, padx=2, pady =2, ipady =1, sticky =E)
    
    frame = tk.Frame(windows)
    frame.pack(fill=BOTH, expand=1)

    def get_ObserverSetCatchDB():
        try:
            sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = sqliteConnection.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", sqliteConnection)
            length_Complete_df = len(Complete_df)
            if length_Complete_df > 0:
                Complete_df = Complete_df[(Complete_df.RecordType) == 1]
                Complete_df = Complete_df.reset_index(drop=True)
                ObserverSetCatchDB = pd.DataFrame(Complete_df)
                sqliteConnection.commit()
                return ObserverSetCatchDB
            else:
                messagebox.showerror('Set & Catch Database Is Empty', "Please Import Set & Catch CSV File To View")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()
    
    def get_NAFO_AreaQC_dfDB():
        Return_ObsSetCatchDB = get_ObserverSetCatchDB()
        try:
            sqliteConnection = sqlite3.connect(DB_SetCatch_Val_Calculation)
            cursor = sqliteConnection.cursor()
            NAFO_AreaQC_df = pd.read_sql_query("SELECT * FROM SetCatch_NAFO_AreaQCAnalysis;", sqliteConnection)
            length_NAFO_AreaQC_df = len(NAFO_AreaQC_df)
            if length_NAFO_AreaQC_df > 0:
                NAFO_AreaQC_df = NAFO_AreaQC_df[
                ((NAFO_AreaQC_df.NAFOValidityCheck_StartPoints) == 'NAFO-QC Failed')]
                NAFO_AreaQC_df = NAFO_AreaQC_df.loc[:,
                ['DeploymentUID', 'NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
                 'StartPoints','EndPoints', 'Assigned_NAFOPloygon', 'Calculated_NAFOPolygon', 'RecordType']]
                NAFO_AreaQC_df = NAFO_AreaQC_df.reset_index(drop=True)
                NAFO_AreaQC_dfDB = pd.DataFrame(NAFO_AreaQC_df)
                NAFO_AreaQC_dfDB=  NAFO_AreaQC_dfDB.merge(
                    Return_ObsSetCatchDB, 
                    on = ['DeploymentUID', 'RecordType'],
                    indicator=True, 
                    how='left').query('_merge == "both"')

                lengthFlagged = len(NAFO_AreaQC_dfDB)
                sqliteConnection.commit()
                return NAFO_AreaQC_dfDB, length_NAFO_AreaQC_df, lengthFlagged
            else:
                messagebox.showerror('Set & Catch Database Is Empty', "Please Import Set & Catch CSV File To View")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()
    
    get_NAFO_AreaQC_df = get_NAFO_AreaQC_dfDB()
    entry_Flagged.insert(tk.END,get_NAFO_AreaQC_df[2])
    ObserverSetCatchDB = get_NAFO_AreaQC_df[0]
    length_ObserverSetCatchDB = len(ObserverSetCatchDB)
    if length_ObserverSetCatchDB > 0:

        ObserverSetCatchDB = (ObserverSetCatchDB.loc[:,
            ['DeploymentUID', 'NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartPoints','EndPoints', 'Assigned_NAFOPloygon','Calculated_NAFOPolygon',
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
            'NumberIndividuals', 'DataBase_ID','RecordIdentifier']]).replace(['', None, np.nan, 
            'None', ' ', '  ', '   ', '    '], 99999999)
        
        ObserverSetCatchDB[['DataBase_ID', 'RecordIdentifier', 'GearDamage',
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
                            'NumberIndividuals']] = ObserverSetCatchDB[
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
                        
        ObserverSetCatchDB[['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                    'EndLongitude','AverageTowSpeed', 'VesselLength']] = ObserverSetCatchDB[
                    ['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                    'EndLongitude','AverageTowSpeed', 'VesselLength']].astype(float)
                
        ObserverSetCatchDB['VesselSideNumber'] = pd.to_numeric(ObserverSetCatchDB[
                    'VesselSideNumber'], downcast='integer', errors='ignore')
        
        ObserverSetCatchDB['SubTripNumber'] = pd.to_numeric(ObserverSetCatchDB[
                    'SubTripNumber'], downcast='integer', errors='ignore')
                    
        ObserverSetCatchDB[['NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartPoints','EndPoints', 'Assigned_NAFOPloygon', 'Calculated_NAFOPolygon', 
            'ObserverNumber', 'DeploymentUID', 
            'SubTripNumber','NAFODivision', 'VesselSideNumber',
            'UnitArea','DetailedCatchSpeciesCompCode']] = ObserverSetCatchDB[
            ['NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartPoints','EndPoints', 'Assigned_NAFOPloygon','Calculated_NAFOPolygon',
            'ObserverNumber', 'DeploymentUID', 
            'SubTripNumber','NAFODivision', 'VesselSideNumber',
            'UnitArea','DetailedCatchSpeciesCompCode']].astype(str)
        
        ObserverSetCatchDB = ObserverSetCatchDB.replace([99999999, 99999999.0, np.nan], '')
        ObserverSetCatchDB = ObserverSetCatchDB.replace(['99999999.0', '99999999', '.'], 'None')
        ObserverSetCatchDB = (ObserverSetCatchDB.loc[:,
            ['DeploymentUID', 'NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartPoints','EndPoints', 'Assigned_NAFOPloygon','Calculated_NAFOPolygon',
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
            'NumberIndividuals', 'DataBase_ID','RecordIdentifier']])
        ObserverSetCatchDB.sort_values(by=['Year', 'ASOCCode', 'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
        ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)
        pt = Table(frame, dataframe = ObserverSetCatchDB, showtoolbar=True, showstatusbar=True, maxcellwidth=1500)
        pt.setRowColors(rows=range(1,len(ObserverSetCatchDB),2), clr='lightblue', cols='all')
        pt.cellbackgr = 'aliceblue'
        options = config.load_options()
        options = { 'align': 'center',
                    'cellbackgr': '#F4F4F3',
                    'cellwidth': 150,
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
        pt.adjustColumnWidths(limit=30)
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
                    tkinter.messagebox.showinfo("Submitted To Set&Catch DB","Successfully Submitted To Update DB")      
        else:
            tkinter.messagebox.showinfo("Empty Set&Catch DB","Empty Set&Catch DB, Please Import Set&Catch CSV File To Submit")

    def BackendSubmitAndUpdateDB(Complete_df):
        conn_DB_Set_Catch_Analysis= sqlite3.connect(DB_Set_Catch_Analysis)
        cur_DB_Set_Catch_Analysis=conn_DB_Set_Catch_Analysis.cursor()
        conn_DB_SetCatch_Calculation= sqlite3.connect(DB_SetCatch_Val_Calculation)
        cur_DB_SetCatch_CalculationVal=conn_DB_SetCatch_Calculation.cursor()
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
                                list_item_NAFODivision,            
                                list_item_StartLatitude,                
                                list_item_StartLongitude,               
                                list_item_EndLatitude,                  
                                list_item_EndLongitude,                  
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
        
        cur_DB_SetCatch_CalculationVal.executemany("UPDATE SetCatch_NAFO_AreaQCAnalysis SET \
                NAFODivision =?, StartLatitude =? , StartLongitude = ?, EndLatitude =?, EndLongitude =?\
				WHERE DeploymentUID =?", 
				UpdateRecordList2_SetCatchDB)
        
        cur_DB_Set_Catch_Analysis.executemany("UPDATE DFO_NL_ASOP_Set_Catch_Analysis_IMPORT SET \
                SpeciesCode = ? , KeptWeight = ?, DiscardWeight = ?,\
                EstimatedWeightReleasedCrab =?, NumberIndividuals =?\
				WHERE RecordType =? AND DataBase_ID = ? ", 
				UpdateRecordList3_SetCatchDB)
                                    
        conn_DB_Set_Catch_Analysis.commit()
        conn_DB_Set_Catch_Analysis.close()
        conn_DB_SetCatch_Calculation.commit()
        conn_DB_SetCatch_Calculation.close()
     
    def SetCatchColName():
        SetCatchColNameList =  ['DeploymentUID', 'NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
        'StartPoints','EndPoints', 'Assigned_NAFOPloygon','Calculated_NAFOPolygon',
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
        'NumberIndividuals', 'DataBase_ID','RecordIdentifier']
        return SetCatchColNameList

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

            
            button_ViewCleartable.config(state="disabled")
            button_ReloadViewFlagged.config(state="disabled")
        else:
            tkinter.messagebox.showinfo("Set-Up Index Selection Message","Length Of Index Selection Must Be Between 1 To 5")

    def DefaultSetIndexDF():
        pt.prodyutCustomsetindex3()
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

        
        button_ViewCleartable.config(state="disabled")
        button_ReloadViewFlagged.config(state="disabled")
  
    def ReSetIndexDF_BackEnd():
        pt.resetIndex(ask=False, drop=False)
        Complete_df = pd.DataFrame(pt.model.df)
        Complete_df.reset_index(drop=True, inplace = True)
        Complete_df = SetCatchDFQC(Complete_df)
        Complete_df = Complete_df.loc[:,['DeploymentUID', 'NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
        'StartPoints','EndPoints', 'Assigned_NAFOPloygon',
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
        'NumberIndividuals', 'DataBase_ID','RecordIdentifier']]
        Complete_df.sort_values(by=['Year', 'ASOCCode', 'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
        Complete_df  = Complete_df.reset_index(drop=True)
        pt.prodyutCustomclearTable()
        pt.model.df = Complete_df
        pt.model.df.reset_index(drop=True)
        pt.update()
        pt.redraw()
        pt.resetColors()
        pt.setRowColors(rows=range(1,len(ObserverSetCatchDB),2), clr='lightblue', cols='all')
        pt.cellbackgr = 'aliceblue'
        options = config.load_options()
        options = { 'align': 'center',
                    'cellbackgr': '#F4F4F3',
                    'cellwidth': 150,
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

        
        button_ViewCleartable.config(state="normal")
        button_ReloadViewFlagged.config(state="normal")
       
    ### Supporting Functions
    def SetCatchDFQC(Complete_df):
        ObserverSetCatchDB  = pd.DataFrame(Complete_df)      
        ObserverSetCatchDB= (ObserverSetCatchDB.loc[:,
            ['DeploymentUID', 'NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartPoints','EndPoints', 'Assigned_NAFOPloygon','Calculated_NAFOPolygon',
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
            'NumberIndividuals', 'DataBase_ID','RecordIdentifier'
        ]]).replace(['', None, np.nan, 'None'], 99999999)

        ObserverSetCatchDB[['DataBase_ID', 'RecordIdentifier', 'GearDamage',
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
                    'NumberIndividuals']] = ObserverSetCatchDB[
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
                
        ObserverSetCatchDB[['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                    'EndLongitude','AverageTowSpeed', 'VesselLength']] = ObserverSetCatchDB[
                    ['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                    'EndLongitude','AverageTowSpeed', 'VesselLength']].astype(float)
            
        ObserverSetCatchDB['VesselSideNumber'] = pd.to_numeric(ObserverSetCatchDB[
                    'VesselSideNumber'], downcast='integer', errors='ignore')
    
        ObserverSetCatchDB['SubTripNumber'] = pd.to_numeric(ObserverSetCatchDB[
                    'SubTripNumber'], downcast='integer', errors='ignore')
                
        ObserverSetCatchDB[['NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartPoints','EndPoints', 'Assigned_NAFOPloygon', 'Calculated_NAFOPolygon','ObserverNumber', 'DeploymentUID', 
            'SubTripNumber','NAFODivision', 'VesselSideNumber',
            'UnitArea','DetailedCatchSpeciesCompCode']] = ObserverSetCatchDB[
            ['NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartPoints','EndPoints', 'Assigned_NAFOPloygon', 'Calculated_NAFOPolygon','ObserverNumber', 'DeploymentUID', 
            'SubTripNumber','NAFODivision', 'VesselSideNumber',
            'UnitArea','DetailedCatchSpeciesCompCode']].astype(str)
        
        ObserverSetCatchDB = ObserverSetCatchDB.replace([99999999, 99999999.0, np.nan], '')
        ObserverSetCatchDB = ObserverSetCatchDB.replace(['99999999.0', '99999999', '.'], 'None')
        ObserverSetCatchDB = (ObserverSetCatchDB.loc[:,
            ['DeploymentUID', 'NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartPoints','EndPoints', 'Assigned_NAFOPloygon','Calculated_NAFOPolygon',
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
            'NumberIndividuals', 'DataBase_ID','RecordIdentifier']])
        ObserverSetCatchDB.sort_values(by=['Year', 'ASOCCode', 'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
        ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)
        return ObserverSetCatchDB

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

            
            button_ViewCleartable.config(state="normal")
            button_ReloadViewFlagged.config(state="normal")
        else:
            tkinter.messagebox.showinfo("Set-Up Column Chooser Selection Message",
                                        "Length Of Column Chooser Selection Must Be Greater Than Zero")

    def ResetColumnChooser():
        Complete_df = pd.DataFrame(pt.model.df)
        Complete_df = SetCatchDFQC(Complete_df)
        Complete_df = Complete_df.loc[:,['DeploymentUID', 'NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
        'StartPoints','EndPoints', 'Assigned_NAFOPloygon','Calculated_NAFOPolygon',
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
        'NumberIndividuals', 'DataBase_ID','RecordIdentifier']]
        Complete_df.sort_values(by=['Year', 'ASOCCode', 'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
        Complete_df  = Complete_df.reset_index(drop=True)
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
                    'cellwidth': 150,
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

        
        button_ViewCleartable.config(state="normal")
        button_ReloadViewFlagged.config(state="normal")

    def DefaultColChooser():
        pt.prodyutCustomclearTable()
        Return_ObserverSetCatchDB = get_NAFO_AreaQC_dfDB()
        ObserverSetCatchDB = Return_ObserverSetCatchDB[0]
        ObserverSetCatchDB = (ObserverSetCatchDB.loc[:,
        ['DeploymentUID', 'NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
        'StartPoints','EndPoints', 'Assigned_NAFOPloygon','Calculated_NAFOPolygon',
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
        'NumberIndividuals', 'DataBase_ID','RecordIdentifier']]).replace(['', None, np.nan, 
        'None', ' ', '  ', '   ', '    '], 99999999)
    
        ObserverSetCatchDB[['DataBase_ID', 'RecordIdentifier', 'GearDamage',
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
                            'NumberIndividuals']] = ObserverSetCatchDB[
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
                        
        ObserverSetCatchDB[['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                    'EndLongitude','AverageTowSpeed', 'VesselLength']] = ObserverSetCatchDB[
                    ['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                    'EndLongitude','AverageTowSpeed', 'VesselLength']].astype(float)
                
        ObserverSetCatchDB['VesselSideNumber'] = pd.to_numeric(ObserverSetCatchDB[
                    'VesselSideNumber'], downcast='integer', errors='ignore')
        
        ObserverSetCatchDB['SubTripNumber'] = pd.to_numeric(ObserverSetCatchDB[
                    'SubTripNumber'], downcast='integer', errors='ignore')
                    
        ObserverSetCatchDB[['NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartPoints','EndPoints', 'Assigned_NAFOPloygon', 'Calculated_NAFOPolygon', 'ObserverNumber', 'DeploymentUID', 
            'SubTripNumber','NAFODivision', 'VesselSideNumber',
            'UnitArea','DetailedCatchSpeciesCompCode']] = ObserverSetCatchDB[
            ['NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartPoints','EndPoints', 'Assigned_NAFOPloygon','Calculated_NAFOPolygon', 'ObserverNumber', 'DeploymentUID', 
            'SubTripNumber','NAFODivision', 'VesselSideNumber',
            'UnitArea','DetailedCatchSpeciesCompCode']].astype(str)
        
        ObserverSetCatchDB = ObserverSetCatchDB.replace([99999999, 99999999.0, np.nan], '')
        ObserverSetCatchDB = ObserverSetCatchDB.replace(['99999999.0', '99999999', '.'], 'None')
        ObserverSetCatchDB = (ObserverSetCatchDB.loc[:,
            ['DeploymentUID', 'NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartLatitude', 'StartLongitude', 'StartPoints',
            'EndLatitude', 'EndLongitude','EndPoints', 'NAFODivision','Assigned_NAFOPloygon','Calculated_NAFOPolygon',
            'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType',
            'ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
            'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
            'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
            'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision','CodendMeshSize',
            'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
            'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
            'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
            'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
            'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 'EstimatedWeightReleasedCrab', 
            'NumberIndividuals', 'DataBase_ID','RecordIdentifier']])
        ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)
        pt.model.df = ObserverSetCatchDB
        pt.model.df.reset_index(drop=True)
        pt.redraw()
        pt.update()
        pt.resetColors()
        pt.setRowColors(rows=range(1,len(ObserverSetCatchDB),2), clr='lightblue', cols='all')
        pt.cellbackgr = 'aliceblue'
        options = config.load_options()
        options = { 'align': 'center',
                    'cellbackgr': '#F4F4F3',
                    'cellwidth': 150,
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

        
        button_ViewCleartable.config(state="disabled")
        button_ReloadViewFlagged.config(state="disabled")

    ## Top Menu 
    def ViewFlaggedOnly():
        get_NAFO_AreaQC_df = get_NAFO_AreaQC_dfDB()
        ObserverSetCatchDB = get_NAFO_AreaQC_df[0]
        ObserverSetCatchDB = SetCatchDFQC(ObserverSetCatchDB)
        ObserverSetCatchDB = (ObserverSetCatchDB.loc[:,
        ['DeploymentUID', 'NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
        'StartPoints','EndPoints', 'Assigned_NAFOPloygon','Calculated_NAFOPolygon',
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
        'NumberIndividuals', 'DataBase_ID','RecordIdentifier']])
        ObserverSetCatchDB.sort_values(by=['Year', 'ASOCCode', 'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
        ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)
        pt.model.df = ObserverSetCatchDB
        pt.model.df.reset_index(drop=True)
        pt.redraw()
        pt.update()
        pt.resetColors()
        pt.setRowColors(rows=range(1,len(ObserverSetCatchDB),2), clr='lightblue', cols='all')
        pt.cellbackgr = 'aliceblue'
        options = config.load_options()
        options = { 'align': 'center',
                    'cellbackgr': '#F4F4F3',
                    'cellwidth': 150,
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
        button_SetUpColChooser.config(state="normal")
        button_SetUpAsIndexCols.config(state="disabled")
        button_SetUpDefaultIndexCols.config(state="disabled")

    def get_AllNAFO_AreaQC_dfDB():
        Return_ObsSetCatchDB = get_ObserverSetCatchDB()
        try:
            sqliteConnection = sqlite3.connect(DB_SetCatch_Val_Calculation)
            cursor = sqliteConnection.cursor()
            NAFO_AreaQC_df = pd.read_sql_query("SELECT * FROM SetCatch_NAFO_AreaQCAnalysis;", sqliteConnection)
            length_NAFO_AreaQC_df = len(NAFO_AreaQC_df)
            if length_NAFO_AreaQC_df > 0:
                # NAFO_AreaQC_df['Assigned_NAFOPloygon'] = (NAFO_AreaQC_df
                # ['Assigned_NAFOPloygon'].map(lambda x: str(x)[0:7])) + ' - ' +\
                #  NAFO_AreaQC_df['NAFODivision']
                NAFO_AreaQC_df = NAFO_AreaQC_df.loc[:,
                ['DeploymentUID', 'NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
                 'StartPoints','EndPoints', 'Assigned_NAFOPloygon', 'Calculated_NAFOPolygon', 'RecordType']]
                NAFO_AreaQC_df = NAFO_AreaQC_df.reset_index(drop=True)
                NAFO_AreaQC_dfDB = pd.DataFrame(NAFO_AreaQC_df)
                NAFO_AreaQC_dfDB=  NAFO_AreaQC_dfDB.merge(
                    Return_ObsSetCatchDB, 
                    on = ['DeploymentUID', 'RecordType'],
                    indicator=True, 
                    how='left').query('_merge == "both"')
                sqliteConnection.commit()
                return NAFO_AreaQC_dfDB, length_NAFO_AreaQC_df
            else:
                messagebox.showerror('Set & Catch Database Is Empty', "Please Import Set & Catch CSV File To View")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()
    
    def GenQCFailAnalysisReport():
        root = tk.Toplevel(windows)
        root.title ("ExcelView Set&Catch Entries")
        root.geometry('1515x855+40+40')
        root.config(bg="cadet blue")
        def on_close():
            tkinter.messagebox.ABORT = 'abort'
        frame1 = tk.Frame(root)
        frame1.pack(fill=BOTH, expand=1)
        Return_ObserverSetCatchDB = get_AllNAFO_AreaQC_dfDB()
        ObserverSetCatchDB = Return_ObserverSetCatchDB[0]
        ObserverSetCatchDB = SetCatchDFQC(ObserverSetCatchDB)
        ObserverSetCatchDB = (ObserverSetCatchDB.loc[:,
        ['DeploymentUID', 'NAFOValidityCheck_StartPoints', 
        'Assigned_NAFOPloygon','Calculated_NAFOPolygon',
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
        'NumberIndividuals']])
        ObserverSetCatchDB.sort_values(by=['Year', 'ASOCCode', 'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
        ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)
        pt1 = Table(frame1, dataframe = ObserverSetCatchDB, showtoolbar=True, showstatusbar=True)
        pt1.setRowColors(rows=range(1,len(ObserverSetCatchDB),2), clr='lightblue', cols='all')
        pt1.cellbackgr = 'aliceblue'
        options = config.load_options()
        options = { 'align': 'center',
                    'cellbackgr': '#F4F4F3',
                    'cellwidth': 150,
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
        GetSetCatchDB_Columns = [
            'DeploymentUID', 'NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartPoints','EndPoints', 'Assigned_NAFOPloygon',
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
            'NumberIndividuals', 'DataBase_ID','RecordIdentifier'] 
        
        BaseColumns =['DeploymentUID', 'NAFOValidityCheck_StartPoints', 
                      'NAFOValidityCheck_EndPoints','StartPoints',
                      'EndPoints', 'Assigned_NAFOPloygon']
        TreeViewSelectedCols = list(BaseColumns + list((SelectedColumns)))
        get_NAFO_AreaQC_df = get_NAFO_AreaQC_dfDB()
        ObserverSetCatchDB = get_NAFO_AreaQC_df[0]
        ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB)
        ObserverSetCatchDB = ObserverSetCatchDB.reset_index(drop=True)
        
        ObserverSetCatchDB = (ObserverSetCatchDB.loc[:,
        ['DeploymentUID', 'NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
        'StartPoints','EndPoints', 'Assigned_NAFOPloygon',
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
        'NumberIndividuals', 'DataBase_ID','RecordIdentifier']]).replace(['', None, np.nan, 
        'None', ' ', '  ', '   ', '    '], 99999999)
    
        ObserverSetCatchDB[['DataBase_ID', 'RecordIdentifier', 'GearDamage',
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
                            'NumberIndividuals']] = ObserverSetCatchDB[
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
                        
        ObserverSetCatchDB[['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                    'EndLongitude','AverageTowSpeed', 'VesselLength']] = ObserverSetCatchDB[
                    ['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                    'EndLongitude','AverageTowSpeed', 'VesselLength']].astype(float)
            
        ObserverSetCatchDB['VesselSideNumber'] = pd.to_numeric(ObserverSetCatchDB[
                    'VesselSideNumber'], downcast='integer', errors='ignore')
        
        ObserverSetCatchDB['SubTripNumber'] = pd.to_numeric(ObserverSetCatchDB[
                    'SubTripNumber'], downcast='integer', errors='ignore')
                
        ObserverSetCatchDB[['NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartPoints','EndPoints', 'Assigned_NAFOPloygon', 'ObserverNumber', 'DeploymentUID', 
            'SubTripNumber','NAFODivision', 'VesselSideNumber',
            'UnitArea','DetailedCatchSpeciesCompCode']] = ObserverSetCatchDB[
            ['NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartPoints','EndPoints', 'Assigned_NAFOPloygon','ObserverNumber', 'DeploymentUID', 
            'SubTripNumber','NAFODivision', 'VesselSideNumber',
            'UnitArea','DetailedCatchSpeciesCompCode']].astype(str)
    
        ObserverSetCatchDB = ObserverSetCatchDB.replace([99999999, 99999999.0, np.nan], '')
        ObserverSetCatchDB = ObserverSetCatchDB.replace(['99999999.0', '99999999', '.'], 'None')
        ObserverSetCatchDB = (ObserverSetCatchDB.loc[:,
            ['DeploymentUID', 'NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartPoints','EndPoints', 'Assigned_NAFOPloygon',
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
            'NumberIndividuals', 'DataBase_ID','RecordIdentifier']])
        ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)

        ObserverSetCatchDB = ObserverSetCatchDB.loc[:,TreeViewSelectedCols]
        ObserverSetCatchDB = ObserverSetCatchDB.reset_index(drop=True)
        ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB)
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
                    'cellwidth': 150,
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
            'StartLatitude', 'StartLongitude', 'EndLatitude', 
            'EndLongitude', 'RecordType', 'NAFODivision',
            'UnitArea'
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
        get_NAFO_AreaQC_df = get_NAFO_AreaQC_dfDB()
        ObserverSetCatchDB = get_NAFO_AreaQC_df[0]
        ObserverSetCatchDB = (ObserverSetCatchDB.loc[:,
        ['DeploymentUID', 'NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
        'StartPoints','EndPoints', 'Assigned_NAFOPloygon',
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
        'NumberIndividuals', 'DataBase_ID','RecordIdentifier']]).replace(['', None, np.nan, 
        'None', ' ', '  ', '   ', '    '], 99999999)
    
        ObserverSetCatchDB[['DataBase_ID', 'RecordIdentifier', 'GearDamage',
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
                            'NumberIndividuals']] = ObserverSetCatchDB[
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
                        
        ObserverSetCatchDB[['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                    'EndLongitude','AverageTowSpeed', 'VesselLength']] = ObserverSetCatchDB[
                    ['Duration','StartLatitude','StartLongitude', 'EndLatitude', 
                    'EndLongitude','AverageTowSpeed', 'VesselLength']].astype(float)
                
        ObserverSetCatchDB['VesselSideNumber'] = pd.to_numeric(ObserverSetCatchDB[
                    'VesselSideNumber'], downcast='integer', errors='ignore')
    
        ObserverSetCatchDB['SubTripNumber'] = pd.to_numeric(ObserverSetCatchDB[
                    'SubTripNumber'], downcast='integer', errors='ignore')
                    
        ObserverSetCatchDB[['NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartPoints','EndPoints', 'Assigned_NAFOPloygon', 'ObserverNumber', 'DeploymentUID', 
            'SubTripNumber','NAFODivision', 'VesselSideNumber',
            'UnitArea','DetailedCatchSpeciesCompCode']] = ObserverSetCatchDB[
            ['NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartPoints','EndPoints', 'Assigned_NAFOPloygon','ObserverNumber', 'DeploymentUID', 
            'SubTripNumber','NAFODivision', 'VesselSideNumber',
            'UnitArea','DetailedCatchSpeciesCompCode']].astype(str)
    
        ObserverSetCatchDB = ObserverSetCatchDB.replace([99999999, 99999999.0, np.nan], '')
        ObserverSetCatchDB = ObserverSetCatchDB.replace(['99999999.0', '99999999', '.'], 'None')
        ObserverSetCatchDB = (ObserverSetCatchDB.loc[:,
            ['DeploymentUID', 'NAFOValidityCheck_StartPoints', 'NAFOValidityCheck_EndPoints',
            'StartPoints','EndPoints', 'Assigned_NAFOPloygon',
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
            'NumberIndividuals', 'DataBase_ID','RecordIdentifier']])
        ObserverSetCatchDB.sort_values(by=['Year', 'ASOCCode', 'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
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
                        'cellwidth': 150,
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
            length_GetSetCatchDB = int(entry_Flagged.get())
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
                else:
                    Complete_df.sort_values(by=[get_SortVarSelected], ascending=True, inplace=True)
                    Complete_df  = Complete_df.reset_index(drop=True)
                    Complete_df = pd.DataFrame(Complete_df)
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
                            'cellwidth': 150,
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
                button_ResetChooseCols.config(state="normal")

                button_SetUuListCols.config(state="normal")
                button_ResetChooseColList.config(state="normal")

                button_ViewCleartable.config(state="normal")
                button_ReloadView.config(state="normal")

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
            length_GetSetCatchDB = int(entry_Flagged.get())
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
                else:
                    Complete_df.sort_values(by=[get_SortVarSelected], ascending=False, inplace=True)
                    Complete_df  = Complete_df.reset_index(drop=True)
                    Complete_df = pd.DataFrame(Complete_df)
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
                            'cellwidth': 150,
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
                button_ResetChooseCols.config(state="normal")

                button_SetUuListCols.config(state="normal")
                button_ResetChooseColList.config(state="normal")

                button_ViewCleartable.config(state="normal")
                button_ReloadView.config(state="normal")

            else:
                tkinter.messagebox.showinfo("DB Sorting Message - Table Entries Must Be Same Total DB Entries",
                                            "Unable To Sort, Please Check If There is Row Filter Applied Or Not")
        else:
            tkinter.messagebox.showinfo("Sorting Table Message",
                                        "Please Select Sorting Variable From DropDown")
    
    
    ## Bottom Left Frame- ProcedureFrame Define
    ProcedureFrame = Frame(windows, width = 40,  bd = 2,relief = RIDGE, bg= "cadet blue")
    ProcedureFrame.pack(side = LEFT, padx= 0, pady=0)
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

    ## Frame Of Customized Column View : Column Chooser
    CuscolView_SetResetframe = tk.Frame(windows, bd = 2,relief = RIDGE, bg= "cadet blue")
    CuscolView_SetResetframe.pack(side =LEFT, padx=5, pady =2)

    lbl_AddStepProcess_CLV = Label(CuscolView_SetResetframe, font=('aerial', 11, 'bold'),
                            bg= "cadet blue", text="B: Customized View - Select & Move Columns")
    lbl_AddStepProcess_CLV.grid(row =0, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_Step1_ColChooser_CLV = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="1 : Press Ctrl Key & Select Columns To Move First")
    lbl_Step1_ColChooser_CLV.grid(row =2, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_Step2_ColChooser_CLV = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="2 : Hit Set-Up Column Chooser Button Below")
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

     ## Frame Of Customized Column View : Column List view
    CuscolView_SetResetframe = tk.Frame(windows, bd = 2,relief = RIDGE, bg= "cadet blue")
    CuscolView_SetResetframe.pack(side =LEFT, padx=5, pady =2)

    lbl_AddStepProcess_List = Label(CuscolView_SetResetframe, font=('aerial', 11, 'bold'),
                            bg= "cadet blue", text="C: Customized View - Select From List & View")
    lbl_AddStepProcess_List.grid(row =0, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_Step1_ColList_CLV = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="1 : Hit The Select From List & View Button Below")
    lbl_Step1_ColList_CLV.grid(row =1, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    button_SetUuListCols = Button(CuscolView_SetResetframe, bd = 2, text ="Set-Up Select From List & View", width =25,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =RunSelCols_SetAndCatchDB)
    button_SetUuListCols.grid(row =2, column = 0, padx=2, pady =1, ipady =1, sticky =W)

    lbl_Step2_ColList = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="2 : Select Columns from List & Hit Submit To View. OR")
    lbl_Step2_ColList.grid(row =3, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_OrMsg_CL = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="3 : Run Default Column List & Hit Submit To View")
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

    ## Frame Of Customized Column View : Set/Reset Index 
    CuscolView_SetResetframe = tk.Frame(windows, bd = 2,relief = RIDGE, bg= "cadet blue")
    CuscolView_SetResetframe.pack(side =LEFT, padx=3, pady =2)

    lbl_AddStepProcess_CLV = Label(CuscolView_SetResetframe, font=('aerial', 11, 'bold'),
                            bg= "cadet blue", text="D: Customized View - By Set/Reset Index")
    lbl_AddStepProcess_CLV.grid(row =0, column = 0, columnspan=1 ,padx=2, pady =2, sticky =W)

    lbl_Step1_SetResetIndex_CLV = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="1 : Choose Index Columns - Press Ctrl Key & Select (Max 3) Index Columns")
    lbl_Step1_SetResetIndex_CLV.grid(row =2, column = 0, columnspan=1 ,padx=12, pady =2, sticky =W)

    lbl_Step2_SetResetIndex_CLV = Label(CuscolView_SetResetframe, font=('aerial', 9, 'bold'),
                            bg= "cadet blue", text="2 : Set-Up Index Columns - Hit Set-Up Index Columns Button Below")
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
                            bg= "cadet blue", text="3 : Reset Index Columns (Must) - Hit Reset Index Columns Button Below")
    lbl_Step3_SetResetIndex_CLV.grid(row =7, column = 0, columnspan=1 ,padx=12, pady =2, sticky =W)

    button_ResetIndexCols = Button(CuscolView_SetResetframe, bd = 2, text ="Reset Index Columns", width =20,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ReSetIndexDF)
    button_ResetIndexCols.grid(row =8, column = 0, padx=12, pady =1, ipady =1, sticky =W)

    ## Header Frame
    button_ReloadView = Button(HeaderFrame, bd = 2, text ="↓ Ascending Sort ↓ ", width =18,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ViewAssendingSortVariable)
    button_ReloadView.grid(row =0, column = 2, columnspan=1 ,padx=2, pady =2, sticky =W)

    button_SortHighToLow = Button(HeaderFrame, bd = 2, text ="↑ Descending Sort ↑ ", width =18,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ViewDesendingSortVariable)
    button_SortHighToLow.grid(row =0, column = 3, columnspan=1 ,padx=2, pady =2, sticky =W)

    button_ReloadViewFlagged = Button(HeaderFrame, bd = 2, text ="Reload & View Flagged Entries", width =27,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ViewFlaggedOnly)
    button_ReloadViewFlagged.grid(row =0, column = 6, padx=12, pady =1, ipady =1, sticky =W)

    button_ViewCleartable = Button(HeaderFrame, bd = 2, text ="Clear View", width =10,
                                height=1, font=('aerial', 10, 'bold'), fg="blue", bg="cadet blue", 
                                command =ViewClearView)
    button_ViewCleartable.grid(row =0, column = 7, padx=12, pady =1, ipady =1, sticky =W)

    ## Adding File Menu 
    menu = Menu(windows)
    windows.config(menu=menu)
    
    filemenu  = Menu(menu, tearoff=0)
    View  = Menu(menu, tearoff=0)

    menu.add_cascade(label="File", menu=filemenu)
    menu.add_cascade(label="View", menu=View)
    
    filemenu.add_command(label="Exit", command=iExit)
    View.add_command(label="Generate QC Fail Analysis Report", command=GenQCFailAnalysisReport)
    
    windows.mainloop()


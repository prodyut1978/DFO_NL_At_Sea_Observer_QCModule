from tkinter import *
import numpy as np
import pandas as pd
import sqlite3

## Defining DB Path
DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
DB_Set_Catch_Misc = ("./BackEnd/Sqlite3_DB/SetCatch_Misc_DB/DFO_NL_ASOP_Set_Catch_Misc.db")

def RunSetCatch_RunTombstoneQC_BackEnd():

    def UpdateDeploymentUIDAfterUpdate():
           
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
       
    def GetSetCatchDBForCheck():
        UpdateDeploymentUIDAfterUpdate()
        try:
            sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = sqliteConnection.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT", sqliteConnection)
            if len(Complete_df) >0:
                data = pd.DataFrame(Complete_df)
                data = data.reset_index(drop=True)
                data  = data.iloc[:,0:(len(list(Complete_df.columns))-8)]
                data.sort_values(by=['ASOCCode', 'ObserverNumber',
                                    'DeploymentNumber','SetNumber','RecordType'], 
                                inplace=True)
                data = pd.DataFrame(data)
                return data      
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def GetColumnsForTombstoneCheck():
        DB_column_names = [
            'ObserverNumber', 'SubTripNumber','Country', 'Quota', 'SetType', 
            'VesselSideNumber','VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 
            'Month', 'HaulDay','HaulMonth', 'StartTime', 'Duration', 
            'PositionPrecision', 'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 
            'NAFODivision', 'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 
            'CodendMeshSize', 'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 
            'AverageGillnetLength', 'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 
            'NumberPots', 'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 
            'DataSource', 'DirectedSpecies', 'NumberSpecies'
            ]
        return DB_column_names

    def SubmitTombstonQCToStorage(TombstoneQCFailedDF):
        try:
            TombstoneQCFailedDF = pd.DataFrame(TombstoneQCFailedDF)
            sqliteConnection = sqlite3.connect(DB_Set_Catch_Misc)
            cursor = sqliteConnection.cursor()
            TombstoneQCFailedDF.to_sql('DFO_NL_ASOP_SetCatch_TombstoneQCFailOnImport', sqliteConnection, if_exists="replace",index = False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def SubmitDuplicatedQCToStorage(DuplicatedQCFailedDF):
        try:
            DuplicatedQCFailedDF = pd.DataFrame(DuplicatedQCFailedDF)
            sqliteConnection = sqlite3.connect(DB_Set_Catch_Misc)
            cursor = sqliteConnection.cursor()
            DuplicatedQCFailedDF.to_sql('DFO_NL_ASOP_SetCatch_DuplicateQCFailOnImport', 
                    sqliteConnection, if_exists="replace",index = False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()
    
    def CheckforDuplicatedDepUID(GetImportedData_Rec_1):
        GetImportedData_Rec_1 = GetImportedData_Rec_1.loc[:,
                    ['Year','ASOCCode','DeploymentNumber',
                    'SetNumber', 'DeploymentUID']]
        GetImportedData_Rec_1 ['DuplicatedEntries']=GetImportedData_Rec_1.sort_values(
            by =['Year','ASOCCode','DeploymentNumber',
                 'SetNumber', 'DeploymentUID']).duplicated(
            ['Year','ASOCCode','DeploymentNumber',
            'SetNumber', 'DeploymentUID'],keep='last')
        GetImportedData_Rec_1 = GetImportedData_Rec_1.loc[GetImportedData_Rec_1.DuplicatedEntries == True, 
            'Year': 'DuplicatedEntries']
        GetImportedData_Rec_1 = GetImportedData_Rec_1.reset_index(drop=True)
        GetImportedData_Rec_1['QC_Variable'] = "Year-ASOC-DepN-SetN"
        GetImportedData_Rec_1['QC_Message'] = "Duplicated DeploymentUID Found"
        GetImportedData_Rec_1 = GetImportedData_Rec_1.loc[:,
                    ['Year','ASOCCode','DeploymentNumber',
                    'SetNumber', 'DeploymentUID', 'QC_Variable', 'QC_Message']]
        DuplicatedQCFailedDF = pd.DataFrame(GetImportedData_Rec_1)
        SubmitDuplicatedQCToStorage(DuplicatedQCFailedDF)
        DuplicatedQCFailedEntries = len(DuplicatedQCFailedDF)
        return DuplicatedQCFailedEntries
       
    def PerformTombstoneCheck():
        GetImportedData = GetSetCatchDBForCheck()
        Variables_column = GetColumnsForTombstoneCheck()
        if len(GetImportedData) >0:
            Filter1_GetImportedData = (GetImportedData.groupby(
            ['DeploymentUID'], as_index=False)
            ['RecordType'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
            Filter1_GetImportedData = Filter1_GetImportedData[
                            (Filter1_GetImportedData.RecordType) == 2]
            Filter1_GetImportedData = Filter1_GetImportedData.loc[:,['DeploymentUID']]
            Filter1_GetImportedData = GetImportedData.merge(
                Filter1_GetImportedData, 
                on = ['DeploymentUID'], 
                indicator=True, 
                how='outer').query('_merge == "both"')
            Filter1_GetImportedData  = Filter1_GetImportedData.reset_index(drop=True)
            Filter1_GetImportedData  = Filter1_GetImportedData.iloc[:,0:(len(list(GetImportedData.columns)))]
            GetImportedData = pd.DataFrame(Filter1_GetImportedData)
            
            GetImportedData_Rec_1 =  GetImportedData[
                            (GetImportedData.RecordType) == 1]
            GetImportedData_Rec_1  = GetImportedData_Rec_1.reset_index(drop=True)
            GetImportedData_Rec_1 = pd.DataFrame(GetImportedData_Rec_1)
            DuplicatedQCFailedEntries = CheckforDuplicatedDepUID(GetImportedData_Rec_1)
            
            GetImportedData_Rec_2 =  GetImportedData[
                            (GetImportedData.RecordType) == 2]
            GetImportedData_Rec_2  = GetImportedData_Rec_2.reset_index(drop=True)
            GetImportedData_Rec_2 = GetImportedData_Rec_2.drop_duplicates(
                subset=['DeploymentUID'], keep="first")
            GetImportedData_Rec_2 = pd.DataFrame(GetImportedData_Rec_2)
            CombineImportedData = pd.concat([GetImportedData_Rec_1, GetImportedData_Rec_2])
            CombineImportedData.sort_values(
                                by=['Year','ASOCCode',
                                'DeploymentNumber','SetNumber', 
                                'RecordType'], inplace=True)
            CombineImportedData  = CombineImportedData.reset_index(drop=True)
            CombineImportedData  = pd.DataFrame(CombineImportedData)
            CombineImportedData_GB= CombineImportedData.groupby(
                ['Year','ASOCCode','DeploymentNumber','SetNumber', 'DeploymentUID'],  
                as_index=False)
            ConcatCheck_VariableDF =[]
            for variable in Variables_column:
                Check_Variable = CombineImportedData_GB.agg({variable: "nunique"})
                Check_Variable =  Check_Variable[
                            (Check_Variable[variable])>1]
                Check_Variable  = Check_Variable.reset_index(drop=True)
                Check_Variable['QC_Variable'] = variable
                Check_Variable['QC_Message'] = (variable) +"-" + "Tombstone Data Check Failed"
                Check_Variable = Check_Variable.loc[:,
                    ['Year','ASOCCode','DeploymentNumber',
                    'SetNumber', 'DeploymentUID', 'QC_Variable', 'QC_Message']]
                Check_Variable = pd.DataFrame(Check_Variable)
                ConcatCheck_VariableDF.append(Check_Variable)
            ConcatCheck_VariableDF = pd.concat(ConcatCheck_VariableDF)
            ConcatCheck_VariableDF.sort_values(
            by=['Year','ASOCCode','DeploymentNumber',
                'SetNumber'], inplace=True)
            ConcatCheck_VariableDF = ConcatCheck_VariableDF.reset_index(drop=True)
            TombstoneQCFailedDF = pd.DataFrame(ConcatCheck_VariableDF)
            SubmitTombstonQCToStorage(TombstoneQCFailedDF)
            TombQCFailedTotalEntries = len(TombstoneQCFailedDF)
            QCFailedTotalEntries = TombQCFailedTotalEntries + DuplicatedQCFailedEntries
            return QCFailedTotalEntries
           
    QCFailedTotalEntries = PerformTombstoneCheck()
    return QCFailedTotalEntries

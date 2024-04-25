from tkinter import*
from tkinter import messagebox
import sqlite3
import pandas as pd
import numpy as np

def RunSetCatch_PresenceValidation_BackEnd():
    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_SetCatch_Validation_Presence = ("./BackEnd/Sqlite3_DB/QC_Check_PresenceConsistency_DB/DFO_NL_ASOP_SetCatch_PresenceValidation.db")

    def RunPresenceMust_FailedVariables():
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                                        'ASOCCode','ObserverNumber','Year',
                                                                        'DeploymentNumber','SubTripNumber','SetNumber',
                                                                        'Country','Quota','SetType',
                                                                        'VesselSideNumber','VesselClass','Day', 
                                                                        'Month', 'HaulDay',  'HaulMonth',
                                                                        'StartTime','Duration','PositionPrecision',
                                                                        'StartLatitude','StartLongitude','EndLatitude', 
                                                                        'EndLongitude', 'InOut200MileLimit',  'NAFODivision',
                                                                        'GearType','RecordType','DetailedCatchSpeciesCompCode', 
                                                                        'DirectedSpecies', 'AverageDepth','DataSource']]
                    SetCatchProfileDB_DF  = SetCatchProfileDB_DF.reset_index(drop=True)
                    SetCatchProfileDB_DF  = pd.DataFrame(SetCatchProfileDB_DF)
                    return SetCatchProfileDB_DF
                else:
                    messagebox.showerror('DFO-NL-ASOP Set & Catch DB Message', "Void DFO-NL-ASOP Set & Catch DB...Please Import DFO-NL-ASOP Set & Catch CSV Files")
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()

        def Submit_SetCatch_QCFailedPresence(FailedValidation_PresenceMustDF):
            try:
                Submit_To_DBStorage = pd.DataFrame(FailedValidation_PresenceMustDF)
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Presence)
                cursor = sqliteConnection.cursor()
                Submit_To_DBStorage.to_sql('SetCatch_QCFailedPresence_MustVariables',
                                        sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        def Gen_QC_NullCheck(y):
            if y == 99999999:
                return 'Null'
            elif y == '99999999':
                return 'Null'
            elif y == 99999999.0:
                return 'Null'
            else:
                return y

        SetCatchProfileDB_DF = GetSetCatchProfileDB()
        SetCatchProfileDB_DF= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                'ASOCCode','ObserverNumber','Year',
                                'DeploymentNumber','SubTripNumber','SetNumber',
                                'Country','Quota','SetType',
                                'VesselSideNumber','VesselClass','Day', 
                                'Month', 'HaulDay',  'HaulMonth',
                                'StartTime','Duration','PositionPrecision',
                                'StartLatitude','StartLongitude','EndLatitude', 
                                'EndLongitude', 'InOut200MileLimit',  'NAFODivision',
                                'GearType','RecordType','DetailedCatchSpeciesCompCode', 
                                'DirectedSpecies', 'AverageDepth',
                                'DataSource']]).replace(['','None'], 99999999)
        
        SetCatchProfileDB_DF[['DataBase_ID','RecordIdentifier','ASOCCode','Year',
                                'DeploymentNumber','SetNumber','Country','Quota','SetType',
                                'VesselClass','Day', 'Month', 'HaulDay',  'HaulMonth',
                                'StartTime','PositionPrecision', 'InOut200MileLimit',
                                'GearType','RecordType', 'DirectedSpecies',
                                'AverageDepth','DataSource']] = SetCatchProfileDB_DF[
                                ['DataBase_ID','RecordIdentifier','ASOCCode','Year',
                                'DeploymentNumber','SetNumber','Country','Quota','SetType',
                                'VesselClass','Day', 'Month', 'HaulDay',  'HaulMonth',
                                'StartTime','PositionPrecision', 'InOut200MileLimit',
                                'GearType','RecordType', 'DirectedSpecies',
                                'AverageDepth','DataSource']
                                ].astype(int)
        
        SetCatchProfileDB_DF[['DeploymentUID','ObserverNumber','SubTripNumber',
                            'VesselSideNumber','NAFODivision','DetailedCatchSpeciesCompCode']] = SetCatchProfileDB_DF[
                            ['DeploymentUID','ObserverNumber','SubTripNumber',
                            'VesselSideNumber','NAFODivision', 'DetailedCatchSpeciesCompCode']
                            ].astype(str)
        
        SetCatchProfileDB_DF[['Duration','StartLatitude','StartLongitude','EndLatitude', 
                            'EndLongitude']] = SetCatchProfileDB_DF[
                            ['Duration','StartLatitude','StartLongitude','EndLatitude', 
                            'EndLongitude']
                            ].astype(float)
        ColList =['DataBase_ID','RecordIdentifier','DeploymentUID',
                'ASOCCode','ObserverNumber','Year',
                'DeploymentNumber','SubTripNumber','SetNumber',
                'Country','Quota','SetType',
                'VesselSideNumber','VesselClass','Day', 
                'Month', 'HaulDay',  'HaulMonth',
                'StartTime','Duration','PositionPrecision',
                'StartLatitude','StartLongitude','EndLatitude', 
                'EndLongitude', 'InOut200MileLimit',  'NAFODivision',
                'GearType','RecordType','DetailedCatchSpeciesCompCode', 
                'DirectedSpecies', 'AverageDepth',
                'DataSource']
        for ColName in ColList:
            SetCatchProfileDB_DF[ColName] = SetCatchProfileDB_DF[ColName].apply(Gen_QC_NullCheck)
        
        FailedValidation_PresenceMustDF= SetCatchProfileDB_DF[(SetCatchProfileDB_DF.DataBase_ID =="Null")|
                        (SetCatchProfileDB_DF.RecordIdentifier =="Null")|
                        (SetCatchProfileDB_DF.DeploymentUID =="Null")|
                        (SetCatchProfileDB_DF.ASOCCode =="Null")|
                        (SetCatchProfileDB_DF.ObserverNumber =="Null")|
                        (SetCatchProfileDB_DF.Year =="Null")|
                        (SetCatchProfileDB_DF.DeploymentNumber =="Null")|
                        (SetCatchProfileDB_DF.SubTripNumber =="Null")|
                        (SetCatchProfileDB_DF.SetNumber =="Null")|
                        (SetCatchProfileDB_DF.Country =="Null")|
                        (SetCatchProfileDB_DF.Quota =="Null")|
                        (SetCatchProfileDB_DF.SetType =="Null")|
                        (SetCatchProfileDB_DF.VesselSideNumber =="Null")|
                        (SetCatchProfileDB_DF.VesselClass =="Null")|
                        (SetCatchProfileDB_DF.Day =="Null")|
                        (SetCatchProfileDB_DF.Month =="Null")|
                        (SetCatchProfileDB_DF.HaulDay =="Null")|
                        (SetCatchProfileDB_DF.HaulMonth =="Null")|
                        (SetCatchProfileDB_DF.StartTime =="Null")|
                        (SetCatchProfileDB_DF.Duration =="Null")|
                        (SetCatchProfileDB_DF.PositionPrecision =="Null")|
                        (SetCatchProfileDB_DF.StartLatitude =="Null")|
                        (SetCatchProfileDB_DF.StartLongitude =="Null")|
                        (SetCatchProfileDB_DF.EndLatitude =="Null")|
                        (SetCatchProfileDB_DF.EndLongitude =="Null")|
                        (SetCatchProfileDB_DF.InOut200MileLimit =="Null")|
                        (SetCatchProfileDB_DF.NAFODivision =="Null")|
                        (SetCatchProfileDB_DF.GearType =="Null")|
                        (SetCatchProfileDB_DF.RecordType =="Null")|
                        (SetCatchProfileDB_DF.DetailedCatchSpeciesCompCode =="Null")|
                        (SetCatchProfileDB_DF.DirectedSpecies =="Null")|
                        (SetCatchProfileDB_DF.AverageDepth =="Null")|
                        (SetCatchProfileDB_DF.DataSource =="Null")
                        ]
        FailedValidation_PresenceMustDF.loc[
            FailedValidation_PresenceMustDF["Year"] < 2007, "ObserverNumber"] = 'None'
        
        FailedValidation_PresenceMustDF.loc[
            FailedValidation_PresenceMustDF["Year"] < 2013, "SubTripNumber"] = 'None'
        
        FailedValidation_PresenceMustDF.loc[
            FailedValidation_PresenceMustDF["Year"] < 2013, "DetailedCatchSpeciesCompCode"] = 'None'
        
        FailedValidation_PresenceMustDF.loc[
            FailedValidation_PresenceMustDF["Year"] < 2007, "HaulDay"] = ''
        
        FailedValidation_PresenceMustDF.loc[
            FailedValidation_PresenceMustDF["Year"] < 2007, "HaulMonth"] = ''
        
        FailedValidation_PresenceMustDF  = FailedValidation_PresenceMustDF.reset_index(drop=True)
        FailedValidation_PresenceMustDF  = pd.DataFrame(FailedValidation_PresenceMustDF)

        Submit_SetCatch_QCFailedPresence(FailedValidation_PresenceMustDF)
        Length_FailedPresenceMustDF = len(FailedValidation_PresenceMustDF)
        return Length_FailedPresenceMustDF

    def RunPresenceConditional_FailedVariables():
        
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,
                        ['DataBase_ID','RecordIdentifier','DeploymentUID',
                         'RecordType','GearType',
                        'AverageTowSpeed','CodendMeshSize','MeshSizeMG',
                        'NumberGillnets','AverageGillnetLength','NumberHooks',
                        'NumberWindows', 'NumberPots']]
                    SetCatchProfileDB_DF  = SetCatchProfileDB_DF.reset_index(drop=True)
                    SetCatchProfileDB_DF  = pd.DataFrame(SetCatchProfileDB_DF)
                    return SetCatchProfileDB_DF
                else:
                    messagebox.showerror('DFO-NL-ASOP Set & Catch DB Message', "Void DFO-NL-ASOP Set & Catch DB...Please Import DFO-NL-ASOP Set & Catch CSV Files")
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()

        def Submit_PresenceConditional_DB(AverageTowSpeedDB_Failed, CodendMeshSizeDB_Failed,
                                        MeshSizeMGDB_Failed, NumberGillnetsDB_Failed,
                                        AverageGillnetLengthDB_Failed, NumberHooksDB_Failed,
                                        NumberWindowsDB_Failed, NumberPotsDB_Failed):
            try:
                AverageTowSpeedDB_Failed = pd.DataFrame(AverageTowSpeedDB_Failed)
                CodendMeshSizeDB_Failed = pd.DataFrame(CodendMeshSizeDB_Failed)
                MeshSizeMGDB_Failed = pd.DataFrame(MeshSizeMGDB_Failed)
                NumberGillnetsDB_Failed = pd.DataFrame(NumberGillnetsDB_Failed)
                AverageGillnetLengthDB_Failed = pd.DataFrame(AverageGillnetLengthDB_Failed)
                NumberHooksDB_Failed = pd.DataFrame(NumberHooksDB_Failed)
                NumberWindowsDB_Failed = pd.DataFrame(NumberWindowsDB_Failed)
                NumberPotsDB_Failed = pd.DataFrame(NumberPotsDB_Failed)

                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Presence)
                cursor = sqliteConnection.cursor()
                AverageTowSpeedDB_Failed.to_sql('SetCatch_QCFailedPresence_AverageTowSpeed',
                                            sqliteConnection, if_exists="replace", index =False)
                CodendMeshSizeDB_Failed.to_sql('SetCatch_QCFailedPresence_CodendMeshSize',
                                            sqliteConnection, if_exists="replace", index =False)
                MeshSizeMGDB_Failed.to_sql('SetCatch_QCFailedPresence_MeshSizeMG',
                                            sqliteConnection, if_exists="replace", index =False)
                NumberGillnetsDB_Failed.to_sql('SetCatch_QCFailedPresence_NumberGillnets',
                                            sqliteConnection, if_exists="replace", index =False)
                AverageGillnetLengthDB_Failed.to_sql('SetCatch_QCFailedPresence_AverageGillnetLength',
                                            sqliteConnection, if_exists="replace", index =False)
                NumberHooksDB_Failed.to_sql('SetCatch_QCFailedPresence_NumberHooks',
                                            sqliteConnection, if_exists="replace", index =False)
                NumberWindowsDB_Failed.to_sql('SetCatch_QCFailedPresence_NumberWindows',
                                            sqliteConnection, if_exists="replace", index =False)
                NumberPotsDB_Failed.to_sql('SetCatch_QCFailedPresence_NumberPots',
                                            sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        SetCatchProfileDB_DF = GetSetCatchProfileDB()
        
        ## AverageTowSpeed QC
        GearType_AverageTowSpeed= [4,5,7,8,10,13,14,15,20,22,64,65]
        NotinList_AverageTowSpeed =[0.0, 0, 99999999.0, 99999999]
        AverageTowSpeedDB_DF= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'GearType', 'AverageTowSpeed']]).replace(['','None'], 99999999)
        AverageTowSpeedDB_DF[['DataBase_ID','RecordIdentifier','RecordType','GearType']]= AverageTowSpeedDB_DF[
                ['DataBase_ID','RecordIdentifier','RecordType','GearType']].astype(int)
        AverageTowSpeedDB_DF[['DeploymentUID']] = AverageTowSpeedDB_DF[['DeploymentUID']].astype(str)
        AverageTowSpeedDB_DF[['AverageTowSpeed']] = AverageTowSpeedDB_DF[['AverageTowSpeed']].astype(float)

        AverageTowSpeedDB_Failed =[]
        AverageTowSpeedDB_DF_1 = AverageTowSpeedDB_DF[(
                                (AverageTowSpeedDB_DF['GearType'].isin(GearType_AverageTowSpeed)) &\
                                (~(AverageTowSpeedDB_DF['AverageTowSpeed'].isin(NotinList_AverageTowSpeed)))
                                    )]
        AverageTowSpeedDB_DF_2 = AverageTowSpeedDB_DF[(
                                (~(AverageTowSpeedDB_DF['GearType'].isin(GearType_AverageTowSpeed))) &\
                                ((AverageTowSpeedDB_DF['AverageTowSpeed'].isin(NotinList_AverageTowSpeed)))
                                    )]
        
        AverageTowSpeedDB_Failed = pd.concat([AverageTowSpeedDB_DF_1, AverageTowSpeedDB_DF_2])
        AverageTowSpeedDB_Failed= (AverageTowSpeedDB_Failed.loc[:,[
                                        'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                        'GearType', 'AverageTowSpeed']]).replace([99999999.0, 99999999], '')
        AverageTowSpeedDB_Failed['QCAverageTowSpeed'] ="GType[4,5,7,8,10,13,14,15,20,22,64,65]=>AvgTowSpeed =0|Blank, Else > 0|NoBlank"
        AverageTowSpeedDB_Failed['QC_CaseType'] = 'Case-ATS'
        AverageTowSpeedDB_Failed  = AverageTowSpeedDB_Failed.reset_index(drop=True)
        AverageTowSpeedDB_Failed  = pd.DataFrame(AverageTowSpeedDB_Failed)

        ## CodendMeshSize QC
        GearType_CodendMeshSize= [1,2,3,9,16,17,18,21,24,66,67,97]
        NotinList_CodendMeshSize =[0, 99999999]
        CodendMeshSizeDB_DF= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'GearType', 'CodendMeshSize']]).replace(['','None'], 99999999)
        CodendMeshSizeDB_DF[['DataBase_ID','RecordIdentifier','RecordType','GearType']]= CodendMeshSizeDB_DF[
                          ['DataBase_ID','RecordIdentifier','RecordType','GearType']].astype(int)
        CodendMeshSizeDB_DF[['DeploymentUID']] = CodendMeshSizeDB_DF[['DeploymentUID']].astype(str)
        CodendMeshSizeDB_DF[['CodendMeshSize']] = CodendMeshSizeDB_DF[['CodendMeshSize']].astype(int)

        CodendMeshSizeDB_Failed =[]
        CodendMeshSizeDB_DF_1 = CodendMeshSizeDB_DF[(
                                (CodendMeshSizeDB_DF['GearType'].isin(GearType_CodendMeshSize)) &\
                                ((CodendMeshSizeDB_DF['CodendMeshSize'].isin(NotinList_CodendMeshSize)))
                                                        )]
        CodendMeshSizeDB_DF_2 = CodendMeshSizeDB_DF[(
                                (~(CodendMeshSizeDB_DF['GearType'].isin(GearType_CodendMeshSize))) &\
                                (~((CodendMeshSizeDB_DF['CodendMeshSize'].isin(NotinList_CodendMeshSize))))
                                                        )]
        CodendMeshSizeDB_Failed = pd.concat([CodendMeshSizeDB_DF_1, CodendMeshSizeDB_DF_2])
        CodendMeshSizeDB_Failed= (CodendMeshSizeDB_Failed.loc[:,[
                                        'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                        'GearType', 'CodendMeshSize']]).replace([99999999], '')
        CodendMeshSizeDB_Failed['QCCodendMeshSize'] ="GType[1,2,3,9,16,17,18,21,24,66,67,97]=>CodendMeshSize=NoBlank, Else Blank"
        CodendMeshSizeDB_Failed['QC_CaseType'] = 'Case-CMS'
        CodendMeshSizeDB_Failed  = CodendMeshSizeDB_Failed.reset_index(drop=True)
        CodendMeshSizeDB_Failed  = pd.DataFrame(CodendMeshSizeDB_Failed)

        ## MeshSizeMG QC
        GearType_MeshSizeMG= [1,2,3,6,9,16,17,18,21,23,24,66,67,97]
        NotinList_MeshSizeMG =[0, 99999999]
        MeshSizeMGDB_DF= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'GearType', 'MeshSizeMG']]).replace(['','None'], 99999999)
        MeshSizeMGDB_DF[['DataBase_ID','RecordIdentifier','RecordType','GearType']]= MeshSizeMGDB_DF[
            ['DataBase_ID','RecordIdentifier','RecordType','GearType']].astype(int)
        MeshSizeMGDB_DF[['DeploymentUID']] = MeshSizeMGDB_DF[['DeploymentUID']].astype(str)
        MeshSizeMGDB_DF[['MeshSizeMG']] = MeshSizeMGDB_DF[['MeshSizeMG']].astype(int)

        MeshSizeMGDB_Failed =[]
        MeshSizeMGDB_DF_1 = MeshSizeMGDB_DF[(
                                (MeshSizeMGDB_DF['GearType'].isin(GearType_MeshSizeMG)) &\
                                ((MeshSizeMGDB_DF['MeshSizeMG'].isin(NotinList_MeshSizeMG)))
                                        )]
        MeshSizeMGDB_DF_2 = MeshSizeMGDB_DF[(
                                (~(MeshSizeMGDB_DF['GearType'].isin(GearType_MeshSizeMG))) &\
                                (~((MeshSizeMGDB_DF['MeshSizeMG'].isin(NotinList_MeshSizeMG))))
                                        )]
        MeshSizeMGDB_Failed = pd.concat([MeshSizeMGDB_DF_1,MeshSizeMGDB_DF_2]) 
        MeshSizeMGDB_Failed= (MeshSizeMGDB_Failed.loc[:,[
                            'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                            'GearType', 'MeshSizeMG']]).replace([99999999], '')
        MeshSizeMGDB_Failed['QCMeshSizeMG'] ="GType[1,2,3,6,9,16,17,18,21,23,24,66,67,97]=>MeshSize_MG=NoBlank, Else Blank"
        MeshSizeMGDB_Failed['QC_CaseType'] = 'Case-MSMG'
        MeshSizeMGDB_Failed  = MeshSizeMGDB_Failed.reset_index(drop=True)
        MeshSizeMGDB_Failed  = pd.DataFrame(MeshSizeMGDB_Failed)
        
        ## NumberGillnets QC
        GearType_NumberGillnets= [5, 15]
        NotinList_NumberGillnets =[0, 99999999]
        NumberGillnetsDB_DF= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'GearType', 'NumberGillnets']]).replace(['','None'], 99999999)
        NumberGillnetsDB_DF[['DataBase_ID','RecordIdentifier','RecordType','GearType']]= NumberGillnetsDB_DF[
              ['DataBase_ID','RecordIdentifier','RecordType','GearType']].astype(int)
        NumberGillnetsDB_DF[['DeploymentUID']] = NumberGillnetsDB_DF[['DeploymentUID']].astype(str)
        NumberGillnetsDB_DF[['NumberGillnets']] = NumberGillnetsDB_DF[['NumberGillnets']].astype(int)

        NumberGillnetsDB_Failed =[]
        NumberGillnetsDB_DF_1 = NumberGillnetsDB_DF[(
                                (NumberGillnetsDB_DF['GearType'].isin(GearType_NumberGillnets)) &\
                                ((NumberGillnetsDB_DF['NumberGillnets'].isin(NotinList_NumberGillnets)))
                                        )]
        NumberGillnetsDB_DF_2 = NumberGillnetsDB_DF[(
                                (~(NumberGillnetsDB_DF['GearType'].isin(GearType_NumberGillnets))) &\
                                (~((NumberGillnetsDB_DF['NumberGillnets'].isin(NotinList_NumberGillnets))))
                                        )]
        NumberGillnetsDB_Failed = pd.concat([NumberGillnetsDB_DF_1, NumberGillnetsDB_DF_2])
        NumberGillnetsDB_Failed= (NumberGillnetsDB_Failed.loc[:,[
                            'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                            'GearType', 'NumberGillnets']]).replace([99999999], '')
        NumberGillnetsDB_Failed['QCNumberGillnets'] ="GType[5,15]=>NumberGillnets=NoBlank, Else Blank"
        NumberGillnetsDB_Failed['QC_CaseType'] = 'Case-NG'
        NumberGillnetsDB_Failed  = NumberGillnetsDB_Failed.reset_index(drop=True)
        NumberGillnetsDB_Failed  = pd.DataFrame(NumberGillnetsDB_Failed)

        ## AverageGillnetLength QC
        GearType_AverageGillnetLength= [5, 15]
        NotinList_AverageGillnetLength =[0, 99999999]
        AverageGillnetLengthDB_DF= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID', 'RecordType',
                                'GearType', 'AverageGillnetLength']]).replace(['','None'], 99999999)
        AverageGillnetLengthDB_DF[['DataBase_ID','RecordIdentifier','RecordType','GearType']]= AverageGillnetLengthDB_DF[
              ['DataBase_ID','RecordIdentifier','RecordType','GearType']].astype(int)
        AverageGillnetLengthDB_DF[['DeploymentUID']] = AverageGillnetLengthDB_DF[['DeploymentUID']].astype(str)
        AverageGillnetLengthDB_DF[['AverageGillnetLength']] = AverageGillnetLengthDB_DF[['AverageGillnetLength']].astype(int)

        AverageGillnetLengthDB_Failed =[]
        AverageGillnetLengthDB_DF_1 = AverageGillnetLengthDB_DF[(
                                (AverageGillnetLengthDB_DF['GearType'].isin(GearType_AverageGillnetLength)) &\
                                ((AverageGillnetLengthDB_DF['AverageGillnetLength'].isin(NotinList_AverageGillnetLength)))
                                        )]
        AverageGillnetLengthDB_DF_2 = AverageGillnetLengthDB_DF[(
                                (~(AverageGillnetLengthDB_DF['GearType'].isin(GearType_AverageGillnetLength))) &\
                                (~((AverageGillnetLengthDB_DF['AverageGillnetLength'].isin(NotinList_AverageGillnetLength))))
                                        )]
        AverageGillnetLengthDB_Failed =  pd.concat([AverageGillnetLengthDB_DF_1,AverageGillnetLengthDB_DF_2])
        AverageGillnetLengthDB_Failed= (AverageGillnetLengthDB_Failed.loc[:,[
                            'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                            'GearType', 'AverageGillnetLength']]).replace([99999999], '')
        AverageGillnetLengthDB_Failed['QCAverageGillnetLength'] ="GType[5,15]=>AverageGillnetLength=NoBlank, Else Blank"
        AverageGillnetLengthDB_Failed['QC_CaseType'] = 'Case-AGL'
        AverageGillnetLengthDB_Failed  = AverageGillnetLengthDB_Failed.reset_index(drop=True)
        AverageGillnetLengthDB_Failed  = pd.DataFrame(AverageGillnetLengthDB_Failed)

        ## NumberHooks QC
        GearType_NumberHooks= [7,8,22]
        NotinList_NumberHooks =[0, 99999999]
        NumberHooksDB_DF= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID', 'RecordType',
                                'GearType', 'NumberHooks']]).replace(['','None'], 99999999)
        NumberHooksDB_DF[['DataBase_ID','RecordIdentifier','RecordType','GearType']]= NumberHooksDB_DF[
                 ['DataBase_ID','RecordIdentifier','RecordType','GearType']].astype(int)
        NumberHooksDB_DF[['DeploymentUID']] = NumberHooksDB_DF[['DeploymentUID']].astype(str)
        NumberHooksDB_DF[['NumberHooks']] = NumberHooksDB_DF[['NumberHooks']].astype(int)

        NumberHooksDB_Failed =[]
        NumberHooksDB_DF_1 = NumberHooksDB_DF[(
                                (NumberHooksDB_DF['GearType'].isin(GearType_NumberHooks)) &\
                                ((NumberHooksDB_DF['NumberHooks'].isin(NotinList_NumberHooks)))
                                        )]
        NumberHooksDB_DF_2 = NumberHooksDB_DF[(
                                (~(NumberHooksDB_DF['GearType'].isin(GearType_NumberHooks))) &\
                                (~((NumberHooksDB_DF['NumberHooks'].isin(NotinList_NumberHooks))))
                                )]
        NumberHooksDB_Failed = pd.concat([NumberHooksDB_DF_1, NumberHooksDB_DF_2])
        NumberHooksDB_Failed= (NumberHooksDB_Failed.loc[:,[
                            'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                            'GearType', 'NumberHooks']]).replace([99999999], '')
        NumberHooksDB_Failed['QCNumberHooks'] ="GType[7,8,22]=>NumberHooks=NoBlank, Else Blank"
        NumberHooksDB_Failed['QC_CaseType'] = 'Case-NH'
        NumberHooksDB_Failed  = NumberHooksDB_Failed.reset_index(drop=True)
        NumberHooksDB_Failed  = pd.DataFrame(NumberHooksDB_Failed)

        ## NumberWindows QC
        GearType_NumberWindows= [1,2,16,17,18,21,66,67]
        NotinList_NumberWindows =[99999999]
        NumberWindowsDB_DF= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                                'GearType', 'NumberWindows']]).replace(['','None'], 99999999)
        NumberWindowsDB_DF[['DataBase_ID','RecordIdentifier','RecordType','GearType']]= NumberWindowsDB_DF[
               ['DataBase_ID','RecordIdentifier','RecordType','GearType']].astype(int)
        NumberWindowsDB_DF[['DeploymentUID']] = NumberWindowsDB_DF[['DeploymentUID']].astype(str)
        NumberWindowsDB_DF[['NumberWindows']] = NumberWindowsDB_DF[['NumberWindows']].astype(int)

        NumberWindowsDB_Failed =[]
        NumberWindowsDB_DF_1 = NumberWindowsDB_DF[(
                                (NumberWindowsDB_DF['GearType'].isin(GearType_NumberWindows)) &\
                                ((NumberWindowsDB_DF['NumberWindows'].isin(NotinList_NumberWindows)))
                                        )]
        NumberWindowsDB_DF_2 = NumberWindowsDB_DF[(
                        (~(NumberWindowsDB_DF['GearType'].isin(GearType_NumberWindows))) &\
                        (~(NumberWindowsDB_DF['NumberWindows'].isin(NotinList_NumberWindows)))
                            )]
        NumberWindowsDB_Failed =  pd.concat([NumberWindowsDB_DF_1, NumberWindowsDB_DF_2])
        NumberWindowsDB_Failed= (NumberWindowsDB_Failed.loc[:,[
                            'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                            'GearType', 'NumberWindows']]).replace([99999999], '')
        NumberWindowsDB_Failed['QCNumberWindows'] ="GType[1,2,16,17,18,21,66,67]=>NumberWindows=NoBlank, Else Blank"
        NumberWindowsDB_Failed['QC_CaseType'] = 'Case-NW'
        NumberWindowsDB_Failed  = NumberWindowsDB_Failed.reset_index(drop=True)
        NumberWindowsDB_Failed  = pd.DataFrame(NumberWindowsDB_Failed)

        ## NumberPots QC
        GearType_NumberPots= [64]
        NotinList_NumberPots =[99999999]
        NumberPotsDB_DF= (SetCatchProfileDB_DF.loc[:,
                        ['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                        'GearType', 'NumberPots']]).replace(['','None'], 99999999)
        NumberPotsDB_DF[['DataBase_ID','RecordIdentifier','RecordType','GearType']]= NumberPotsDB_DF[
                        ['DataBase_ID','RecordIdentifier','RecordType','GearType']].astype(int)
        NumberPotsDB_DF[['DeploymentUID']] = NumberPotsDB_DF[['DeploymentUID']].astype(str)
        NumberPotsDB_DF[['NumberPots']] = NumberPotsDB_DF[['NumberPots']].astype(int)

        NumberPotsDB_Failed =[]
        NumberPotsDB_DF_1  = NumberPotsDB_DF[(
                            (NumberPotsDB_DF['GearType'].isin(GearType_NumberPots)) &\
                            ((NumberPotsDB_DF['NumberPots'].isin(NotinList_NumberPots)))
                                )]
        
        NumberPotsDB_DF_2 = NumberPotsDB_DF[(
                        (~(NumberPotsDB_DF['GearType'].isin(GearType_NumberPots))) &\
                        (~(NumberPotsDB_DF['NumberPots'].isin(NotinList_NumberPots)))
                            )]
        
        NumberPotsDB_Failed = pd.concat([NumberPotsDB_DF_1, NumberPotsDB_DF_2])
        NumberPotsDB_Failed= (NumberPotsDB_Failed.loc[:,[
                            'DataBase_ID','RecordIdentifier','DeploymentUID','RecordType',
                            'GearType', 'NumberPots']]).replace([99999999.0, 99999999], '')
        NumberPotsDB_Failed['QCNumberPots'] ="GType[64]=>NumberPots=NoBlank, Else Blank"
        NumberPotsDB_Failed['QC_CaseType'] = 'Case-NP'
        NumberPotsDB_Failed  = NumberPotsDB_Failed.reset_index(drop=True)
        NumberPotsDB_Failed  = pd.DataFrame(NumberPotsDB_Failed)
        
        ## Submit To Presence Conditional DB Storage
        Submit_PresenceConditional_DB(AverageTowSpeedDB_Failed, CodendMeshSizeDB_Failed,
                                    MeshSizeMGDB_Failed, NumberGillnetsDB_Failed,
                                    AverageGillnetLengthDB_Failed, NumberHooksDB_Failed,
                                    NumberWindowsDB_Failed, NumberPotsDB_Failed)
        
        Length_FailedConditionalDF = (len(AverageTowSpeedDB_Failed)+\
                                    len(CodendMeshSizeDB_Failed) +\
                                    len(MeshSizeMGDB_Failed)+\
                                    len(NumberGillnetsDB_Failed) +\
                                    len(AverageGillnetLengthDB_Failed)+\
                                    len(NumberHooksDB_Failed) +\
                                    len(NumberWindowsDB_Failed) +\
                                    len(NumberPotsDB_Failed)
                                    )
        return Length_FailedConditionalDF

    def RunPreCondlMisc_FailedVariables():
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID',
                                                                     'ASOCCode','DeploymentNumber','SetNumber','Year',
                                                                     'GearType','RecordType','GearDamage']]
                    SetCatchProfileDB_DF  = SetCatchProfileDB_DF.reset_index(drop=True)
                    SetCatchProfileDB_DF  = pd.DataFrame(SetCatchProfileDB_DF)
                    return SetCatchProfileDB_DF
                else:
                    messagebox.showerror('DFO-NL-ASOP Set & Catch DB Message', "Void DFO-NL-ASOP Set & Catch DB...Please Import DFO-NL-ASOP Set & Catch CSV Files")
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()

        def Submit_PreCondlMisc_DB(QC_FailLogical_RecTGearDamage):
            try:
                QC_FailLogical_RecTGearDamage = pd.DataFrame(QC_FailLogical_RecTGearDamage)
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Presence)
                cursor = sqliteConnection.cursor()
                QC_FailLogical_RecTGearDamage.to_sql('SetCatch_QCFailedMiscPresence_RecTGearDamage',
                                            sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        SetCatchProfileDB_DF = GetSetCatchProfileDB()
        ## QC On RecordType_SetNumber
        RecType_GearDamage_FailLogical= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                             'ASOCCode','DeploymentNumber','SetNumber','Year',
                              'GearType','RecordType','GearDamage']]).replace(['','None'], 99999999)
        
        RecType_GearDamage_FailLogical[['DataBase_ID','RecordIdentifier','ASOCCode',
                            'DeploymentNumber','SetNumber', 'Year', 'RecordType','GearDamage']] = RecType_GearDamage_FailLogical[
                            ['DataBase_ID','RecordIdentifier','ASOCCode',
                            'DeploymentNumber','SetNumber', 'Year', 'RecordType','GearDamage']
                            ].astype(int)
        RecType_GearDamage_FailLogical[['DeploymentUID']] = RecType_GearDamage_FailLogical[['DeploymentUID']].astype(str)
        RecType_GearDamage_FailLogical = pd.DataFrame(RecType_GearDamage_FailLogical)
        
        ## Building PreCondlMisc Summary
        if len(RecType_GearDamage_FailLogical) >0:
            QC_FailLogical_RecTGearDamage   = (RecType_GearDamage_FailLogical.groupby(
            ['Year', 'ASOCCode','DeploymentNumber','SetNumber','DeploymentUID'], as_index=False)
            ['RecordType'].apply(lambda x: (np.sum(x))))
            QC_FailLogical_RecTGearDamage = QC_FailLogical_RecTGearDamage[
                            (QC_FailLogical_RecTGearDamage.RecordType) == 1]
            QC_FailLogical_RecTGearDamage = QC_FailLogical_RecTGearDamage.loc[:,['DeploymentUID']]
            QC_FailLogical_RecTGearDamage = RecType_GearDamage_FailLogical.merge(
                QC_FailLogical_RecTGearDamage, 
                on = ['DeploymentUID'], 
                indicator=True, 
                how='outer').query('_merge == "both"')
            QC_FailLogical_RecTGearDamage  = QC_FailLogical_RecTGearDamage.reset_index(drop=True)
            QC_FailLogical_RecTGearDamage = pd.DataFrame(QC_FailLogical_RecTGearDamage)
            QC_FailLogical_RecTGearDamage = QC_FailLogical_RecTGearDamage[
                            (QC_FailLogical_RecTGearDamage.RecordType) == 1]
            QC_FailLogical_RecTGearDamage= (QC_FailLogical_RecTGearDamage.loc[:,[
                                        'DataBase_ID','RecordIdentifier','DeploymentUID',
                                        'ASOCCode','DeploymentNumber','SetNumber','Year',
                                        'GearType','RecordType','GearDamage']])
            QC_FailLogical_RecTGearDamage  = QC_FailLogical_RecTGearDamage.reset_index(drop=True)
            QC_FailLogical_RecTGearDamage = pd.DataFrame(QC_FailLogical_RecTGearDamage)
            QC_FailLogical_RecTGearDamage = QC_FailLogical_RecTGearDamage[
                            (QC_FailLogical_RecTGearDamage.GearDamage) == 1]
            QC_FailLogical_RecTGearDamage  = QC_FailLogical_RecTGearDamage.reset_index(drop=True)
            QC_FailLogical_RecTGearDamage = pd.DataFrame(QC_FailLogical_RecTGearDamage)
            QC_FailLogical_RecTGearDamage = QC_FailLogical_RecTGearDamage.replace(np.nan, '')
            QC_FailLogical_RecTGearDamage = QC_FailLogical_RecTGearDamage.replace([99999999, 99999999.0, '.'], '')
            QC_FailLogical_RecTGearDamage = QC_FailLogical_RecTGearDamage.replace(['99999999', '.'], 'None')
            QC_FailLogical_RecTGearDamage['QC_Message'] ="GearDamage Presence Failed"
            QC_FailLogical_RecTGearDamage  = QC_FailLogical_RecTGearDamage.reset_index(drop=True)
            QC_FailLogical_RecTGearDamage = pd.DataFrame(QC_FailLogical_RecTGearDamage)
            LenQC_FailLogical_RTGD = len (QC_FailLogical_RecTGearDamage)
            Submit_PreCondlMisc_DB(QC_FailLogical_RecTGearDamage)
        else:
            QC_FailLogical_RecTGearDamage = pd.DataFrame(RecType_GearDamage_FailLogical)
            QC_FailLogical_RecTGearDamage['QC_Message'] ="GearDamage Presence Failed"
            LenQC_FailLogical_RTGD = len (QC_FailLogical_RecTGearDamage)
            Submit_PreCondlMisc_DB(QC_FailLogical_RecTGearDamage)
        return LenQC_FailLogical_RTGD
    
    FailedRunPresenceMust = RunPresenceMust_FailedVariables()
    FailedRunPresenceConditional = RunPresenceConditional_FailedVariables()
    FailedRunPresenceCondlMisc = RunPreCondlMisc_FailedVariables()
    TotalFailedQC_PresenceValidation = (int(FailedRunPresenceMust) + \
                                        int(FailedRunPresenceConditional)+ \
                                        int(FailedRunPresenceCondlMisc))
    return TotalFailedQC_PresenceValidation


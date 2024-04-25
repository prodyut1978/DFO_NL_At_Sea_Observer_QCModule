from tkinter import*
import tkinter.ttk as ttk
import tkinter.messagebox
from tkinter import messagebox
from tkinter import ttk, filedialog
import sqlite3
import pandas as pd
import datetime
import math
import numpy as np

def RunIntegratedRangeValidation_BackEnd():
    today = datetime.date.today()
    Currentyear = today.year

    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_SetCatch_Validation_Range = ("./BackEnd/Sqlite3_DB/QC_Check_RangeConsistency_DB/DFO_NL_ASOP_SetCatch_RangeValidation.db")
    
    def RunTowDistance_QCAnalysis_SetCatch():
        def get_ObserverSetCatchDB():
            try:
                sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = sqliteConnection.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", sqliteConnection)
                length_Complete_df = len(Complete_df)
                if length_Complete_df > 0:
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
    
        def fetchData_RangeLimitVariables():
            try:
                conn = sqlite3.connect(DB_SetCatch_Validation_Range)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_RangeLimitVariables_Define ORDER BY `VariablesID` ASC ;", conn)
                return Complete_df
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()
    
        def haversine(lat1, lon1, lat2, lon2):
            R = 6371  # Radius of the earth in km
            dLat = math.radians(lat2 - lat1)
            dLon = math.radians(lon2 - lon1)
            a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.radians(lat1)) \
                * math.cos(math.radians(lat2)) * math.sin(dLon / 2) * math.sin(dLon / 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            d = R * c  # Distance in km
            d = d * 0.539956803 # Distance in Nautical Mile
            return d
    
        def Submit_QCFailedRange_TowDistance(ObserverSetCatchDB):
            try:
                Submit_To_DBStorage = pd.DataFrame(ObserverSetCatchDB)
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Range)
                cursor = sqliteConnection.cursor()
                Submit_To_DBStorage.to_sql('SetCatch_QCFailedRange_TowDistance', sqliteConnection, 
                                           if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        def ApplyTowDiffFlag(TowDiffValue, 
            TowDiff_LowerRangeLimitValue,
            TowDiff_UpperRangeLimitValue):
        
            if TowDiffValue > TowDiff_UpperRangeLimitValue:
                TowDiffFlag = 'Yes'
            
            elif (TowDiffValue > TowDiff_LowerRangeLimitValue)&\
                (TowDiffValue < TowDiff_UpperRangeLimitValue):
                TowDiffFlag = 'No'
            
            else:
                TowDiffFlag = 'Unknown'
        
            return TowDiffFlag

        Get_RangeLimitVariables = fetchData_RangeLimitVariables()
        SLat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[6,'LowerRangeLimitValue'])
        SLat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[6,'UpperRangeLimitValue'])
        SLon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[7,'LowerRangeLimitValue'])
        SLon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[7,'UpperRangeLimitValue'])
        ELat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[8,'LowerRangeLimitValue'])
        ELat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[8,'UpperRangeLimitValue'])
        ELon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[9,'LowerRangeLimitValue'])
        ELon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[9,'UpperRangeLimitValue'])
        TowDiff_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[23,'LowerRangeLimitValue'])
        TowDiff_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[23,'UpperRangeLimitValue'])
        
        Return_ObserverSetCatchDB = get_ObserverSetCatchDB()
        ObserverSetCatchDB = Return_ObserverSetCatchDB[0]
        length_Complete_df = Return_ObserverSetCatchDB[1]
        if length_Complete_df > 0:
            ObserverSetCatchDB= (ObserverSetCatchDB.loc[:,
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
                            'NumberIndividuals']]).replace(['', None, np.nan, 'None'], 99999999)
            
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
                        
            ObserverSetCatchDB[['ObserverNumber', 'DeploymentUID', 
                    'SubTripNumber','NAFODivision', 'VesselSideNumber',
                    'UnitArea','DetailedCatchSpeciesCompCode']] = ObserverSetCatchDB[
                    ['ObserverNumber', 'DeploymentUID', 
                    'SubTripNumber','NAFODivision', 'VesselSideNumber',
                    'UnitArea','DetailedCatchSpeciesCompCode']].astype(str)

            ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
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
            ObserverSetCatchDB = ObserverSetCatchDB[(ObserverSetCatchDB.RecordType) == 1]
            ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
            ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)
            ObserverSetCatchDB = ObserverSetCatchDB[
                (ObserverSetCatchDB.StartLatitude < 99999999.0) & 
                (ObserverSetCatchDB.StartLongitude < 99999999.0) &
                (ObserverSetCatchDB.EndLatitude < 99999999.0) &
                (ObserverSetCatchDB.EndLongitude < 99999999.0) &
                (ObserverSetCatchDB.AverageTowSpeed < 99999999.0) &
                (ObserverSetCatchDB.Duration < 99999999.0)]
            ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
            ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)
            if len (ObserverSetCatchDB) > 0:
                ObserverSetCatchDB = ObserverSetCatchDB[
                    ((ObserverSetCatchDB.StartLatitude > SLat_LowerRangeLimitValue)&
                    (ObserverSetCatchDB.StartLatitude  < SLat_UpperRangeLimitValue))\
                    &
                    ((ObserverSetCatchDB.StartLongitude > SLon_LowerRangeLimitValue)& 
                    (ObserverSetCatchDB.StartLongitude < SLon_UpperRangeLimitValue))\
                    &
                    ((ObserverSetCatchDB.EndLatitude > ELat_LowerRangeLimitValue)&
                    (ObserverSetCatchDB.EndLatitude < ELat_UpperRangeLimitValue))\
                    &
                    ((ObserverSetCatchDB.EndLongitude > ELon_LowerRangeLimitValue)& 
                    (ObserverSetCatchDB.EndLongitude < ELon_UpperRangeLimitValue))]

                ObserverSetCatchDB = ObserverSetCatchDB.replace([99999999, 99999999.0, np.nan], '')
                ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)
                ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
                ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)

                GearType_Mobile= [1,2,3,9,10,14,16,17,18,21,66,67,97]
                ObserverSetCatchDB = ObserverSetCatchDB[
                                            (ObserverSetCatchDB['GearType'].isin(GearType_Mobile)) ]
                ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
                ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)

                if len (ObserverSetCatchDB) > 0:
                    ObserverSetCatchDB['DegSLat'] = (ObserverSetCatchDB['StartLatitude'].astype(str)).str[0:2]
                    ObserverSetCatchDB['MinSLat'] = (ObserverSetCatchDB['StartLatitude'].astype(str)).str[2:]
                    ObserverSetCatchDB['StartLatDec'] =  (ObserverSetCatchDB['DegSLat'].astype(int)) + \
                                                        ((ObserverSetCatchDB['MinSLat'].astype(float))/60)
                    
                    ObserverSetCatchDB['DegSLong'] = (ObserverSetCatchDB['StartLongitude'].astype(str)).str[0:2]
                    ObserverSetCatchDB['MinSLong'] = (ObserverSetCatchDB['StartLongitude'].astype(str)).str[2:]
                    ObserverSetCatchDB['StartLongDec'] = ((ObserverSetCatchDB['DegSLong'].astype(int)) + \
                                                        ((ObserverSetCatchDB['MinSLong'].astype(float))/60)).astype(float)
                    
                    ObserverSetCatchDB['DegELat'] = (ObserverSetCatchDB['EndLatitude'].astype(str)).str[0:2]
                    ObserverSetCatchDB['MinELat'] = (ObserverSetCatchDB['EndLatitude'].astype(str)).str[2:]
                    ObserverSetCatchDB['EndLatDec'] =  (ObserverSetCatchDB['DegELat'].astype(int)) + \
                                                    ((ObserverSetCatchDB['MinELat'].astype(float))/60)
                    
                    ObserverSetCatchDB['DegELong'] = (ObserverSetCatchDB['EndLongitude'].astype(str)).str[0:2]
                    ObserverSetCatchDB['MinELong'] = (ObserverSetCatchDB['EndLongitude'].astype(str)).str[2:]
                    ObserverSetCatchDB['EndLongDec'] =  ((ObserverSetCatchDB['DegELong'].astype(int)) + \
                                                        ((ObserverSetCatchDB['MinELong'].astype(float))/60)).astype(float)
                    ObserverSetCatchDB['TowDistance'] = ObserverSetCatchDB.apply(
                        lambda row: haversine(row['StartLatDec'], (-row['StartLongDec']), 
                        row['EndLatDec'], (-row['EndLongDec'])), axis=1)
                    
                    ObserverSetCatchDB['SCDistance'] = ObserverSetCatchDB.apply(
                        lambda row: ((row['AverageTowSpeed'])*(row['Duration'])), axis=1)
                    ObserverSetCatchDB['TowDifference'] =  abs(ObserverSetCatchDB['SCDistance'] - ObserverSetCatchDB['TowDistance'])
                    ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                                ['TowDistance', 'SCDistance', 'TowDifference',
                                'StartLatDec', 'StartLongDec', 'EndLatDec', 'EndLongDec',
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
                    ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
                    ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)

                    ObserverSetCatchDB['TowDiffFlag'] = ObserverSetCatchDB.apply(
                    lambda row: ApplyTowDiffFlag(row['TowDifference'], 
                                                (TowDiff_LowerRangeLimitValue),
                                                (TowDiff_UpperRangeLimitValue)), axis=1)
                    ObserverSetCatchDB = ObserverSetCatchDB.loc[:,[ 
                            'TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag',
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
                    ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)
                    Submit_QCFailedRange_TowDistance(ObserverSetCatchDB)
                    ## QC FailCount
                    QCFailCount = ObserverSetCatchDB[(ObserverSetCatchDB.TowDiffFlag) == 'Yes']
                    QCFailCount  = QCFailCount.reset_index(drop=True)
                    QCFailCount  = pd.DataFrame(QCFailCount)
                    Length_QCFailedDF = len(QCFailCount)
                    return Length_QCFailedDF
                else:
                    DFcolumns = ['TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag',
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
                    ObserverSetCatchDB = pd.DataFrame(columns = DFcolumns)
                    Submit_QCFailedRange_TowDistance(ObserverSetCatchDB)
                    Length_QCFailedDF = len(ObserverSetCatchDB)
                    tkinter.messagebox.showinfo("Mobile GearType Not Present For TowDistance QC",
                        "Mobile GearType - [1,2,3,9,10,14,16,17,18,21,66,67,97] Not Present")
                    print('Mobile GearType Not Present')
                    return Length_QCFailedDF
            else:
                DFcolumns = ['TowDistance', 'SCDistance', 'TowDifference','TowDiffFlag',
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
                ObserverSetCatchDB = pd.DataFrame(columns = DFcolumns)
                Submit_QCFailedRange_TowDistance(ObserverSetCatchDB)
                Length_QCFailedDF = len(ObserverSetCatchDB)
                return Length_QCFailedDF

    def RunTowSeparation_QCAnalysis_SetCatch():
        def get_ObserverSetCatchDB():
            try:
                sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = sqliteConnection.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", sqliteConnection)
                length_Complete_df = len(Complete_df)
                if length_Complete_df > 0:
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
    
        def fetchData_RangeLimitVariables():
            try:
                conn = sqlite3.connect(DB_SetCatch_Validation_Range)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_RangeLimitVariables_Define ORDER BY `VariablesID` ASC ;", conn)
                return Complete_df
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if conn:
                    cursor.close()
                    conn.close()
        
        def haversine(lat1, lon1, lat2, lon2):
            lat1 = float(lat1)
            lat2 = float(lat2)
            lon1 = float(lon1)
            lon2 = float(lon2)
            R = 6371  # Radius of the earth in km
            dLat = math.radians(lat2 - lat1)
            dLon = math.radians(lon2 - lon1)
            a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.radians(lat1)) \
                * math.cos(math.radians(lat2)) * math.sin(dLon / 2) * math.sin(dLon / 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            d = R * c  # Distance in km
            d = d * 0.539956803 # Distance in Nautical Mile
            return d
        
        def ApplyTowSepFlag(MaxTowSepValue, CalTowSepValue):
            if CalTowSepValue > MaxTowSepValue:
                TowSepFlag = 'Yes'
            else:
                TowSepFlag = 'No'
            return TowSepFlag

        def ApplyDepIDChangeflag(DepIDChanged):
            if DepIDChanged == True:
                DepIDFlag = "No"
            else:
                DepIDFlag = "Yes"
            return DepIDFlag
        
        def ApplySubTripChangeflag(SubTripChanged, SubTripN):
            if (SubTripN != '')| (SubTripN != 'None'):
                if SubTripChanged == True:
                    SubTripFlag = "No"
                else:
                    SubTripFlag = "Yes"
            if (SubTripN == '')|(SubTripN == 'None'):
                SubTripFlag = "None/Null Value"
            return SubTripFlag

        def ApplySepErrorFlag(TowSepFlag, DepIDChangeFlag, SubTripChangeFlag):
            if (TowSepFlag == 'Yes')&(DepIDChangeFlag == 'No')&(SubTripChangeFlag == 'No'):
                SepErrorflag = 'Yes'
            elif (TowSepFlag == 'Yes')&(DepIDChangeFlag == 'No')&(SubTripChangeFlag == 'None/Null Value'):
                SepErrorflag = 'Yes'
            else:
                SepErrorflag = 'No'
            return SepErrorflag

        def Submit_QCFailedRange_TowSep(ObserverSetCatchDB):
            try:
                Submit_To_DBStorage = pd.DataFrame(ObserverSetCatchDB)
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Range)
                cursor = sqliteConnection.cursor()
                Submit_To_DBStorage.to_sql('SetCatch_QCFailedRange_TowSeparation', sqliteConnection, 
                                            if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        Get_RangeLimitVariables = fetchData_RangeLimitVariables()
        SLat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[6,'LowerRangeLimitValue'])
        SLat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[6,'UpperRangeLimitValue'])
        SLon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[7,'LowerRangeLimitValue'])
        SLon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[7,'UpperRangeLimitValue'])
        ELat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[8,'LowerRangeLimitValue'])
        ELat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[8,'UpperRangeLimitValue'])
        ELon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[9,'LowerRangeLimitValue'])
        ELon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[9,'UpperRangeLimitValue'])
        MaxTowSepSpeedLimit=float(Get_RangeLimitVariables.at[24,'UpperRangeLimitValue'])
        MaxTowSeparationTolerance=float(Get_RangeLimitVariables.at[25,'UpperRangeLimitValue'])

        Return_ObserverSetCatchDB = get_ObserverSetCatchDB()
        ObserverSetCatchDB = Return_ObserverSetCatchDB[0]
        length_Complete_df = Return_ObserverSetCatchDB[1]
        if length_Complete_df > 0:
            ObserverSetCatchDB= (ObserverSetCatchDB.loc[:,
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
                            'NumberIndividuals']]).replace(['', None, np.nan, 'None'], 99999999)

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
                        
            ObserverSetCatchDB[['ObserverNumber', 'DeploymentUID', 
                    'SubTripNumber','NAFODivision', 'VesselSideNumber',
                    'UnitArea','DetailedCatchSpeciesCompCode']] = ObserverSetCatchDB[
                    ['ObserverNumber', 'DeploymentUID', 
                    'SubTripNumber','NAFODivision', 'VesselSideNumber',
                    'UnitArea','DetailedCatchSpeciesCompCode']].astype(str)

            ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
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
            ObserverSetCatchDB = ObserverSetCatchDB[(ObserverSetCatchDB.RecordType) == 1]
            ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
            ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)

            ObserverSetCatchDB = ObserverSetCatchDB[
            (ObserverSetCatchDB.StartLatitude < 99999999.0) & 
            (ObserverSetCatchDB.StartLongitude < 99999999.0) &
            (ObserverSetCatchDB.EndLatitude < 99999999.0) &
            (ObserverSetCatchDB.EndLongitude < 99999999.0) &
            (ObserverSetCatchDB.AverageTowSpeed < 99999999.0) &
            (ObserverSetCatchDB.Duration < 99999999.0)]
            ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
            ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)

            if len (ObserverSetCatchDB) > 0:
                ObserverSetCatchDB = ObserverSetCatchDB[
                        ((ObserverSetCatchDB.StartLatitude > SLat_LowerRangeLimitValue)&
                        (ObserverSetCatchDB.StartLatitude  < SLat_UpperRangeLimitValue))\
                        &
                        ((ObserverSetCatchDB.StartLongitude > SLon_LowerRangeLimitValue)& 
                        (ObserverSetCatchDB.StartLongitude < SLon_UpperRangeLimitValue))\
                        &
                        ((ObserverSetCatchDB.EndLatitude > ELat_LowerRangeLimitValue)&
                        (ObserverSetCatchDB.EndLatitude < ELat_UpperRangeLimitValue))\
                        &
                        ((ObserverSetCatchDB.EndLongitude > ELon_LowerRangeLimitValue)& 
                        (ObserverSetCatchDB.EndLongitude < ELon_UpperRangeLimitValue))]
                
                ObserverSetCatchDB = ObserverSetCatchDB.replace([99999999, 99999999.0, np.nan], '')
                ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB, index=None)
                ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
                ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)

                GearType_Mobile= [1,2,3,9,10,14,16,17,18,21,66,67,97]
                ObserverSetCatchDB = ObserverSetCatchDB[
                                    (ObserverSetCatchDB['GearType'].isin(GearType_Mobile)) ]
                ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
                ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)
                if len (ObserverSetCatchDB) > 0:
                    ObserverSetCatchDB['DegSLat'] = (ObserverSetCatchDB['StartLatitude'].astype(str)).str[0:2]
                    ObserverSetCatchDB['MinSLat'] = (ObserverSetCatchDB['StartLatitude'].astype(str)).str[2:]
                    ObserverSetCatchDB['StartLatDec'] =  (ObserverSetCatchDB['DegSLat'].astype(int)) + \
                                                        ((ObserverSetCatchDB['MinSLat'].astype(float))/60)
                    
                    ObserverSetCatchDB['DegSLong'] = (ObserverSetCatchDB['StartLongitude'].astype(str)).str[0:2]
                    ObserverSetCatchDB['MinSLong'] = (ObserverSetCatchDB['StartLongitude'].astype(str)).str[2:]
                    ObserverSetCatchDB['StartLongDec'] = ((ObserverSetCatchDB['DegSLong'].astype(int)) + \
                                                        ((ObserverSetCatchDB['MinSLong'].astype(float))/60)).astype(float)
                    
                    ObserverSetCatchDB['DegELat'] = (ObserverSetCatchDB['EndLatitude'].astype(str)).str[0:2]
                    ObserverSetCatchDB['MinELat'] = (ObserverSetCatchDB['EndLatitude'].astype(str)).str[2:]
                    ObserverSetCatchDB['EndLatDec'] =  (ObserverSetCatchDB['DegELat'].astype(int)) + \
                                                    ((ObserverSetCatchDB['MinELat'].astype(float))/60)
                    
                    ObserverSetCatchDB['DegELong'] = (ObserverSetCatchDB['EndLongitude'].astype(str)).str[0:2]
                    ObserverSetCatchDB['MinELong'] = (ObserverSetCatchDB['EndLongitude'].astype(str)).str[2:]
                    ObserverSetCatchDB['EndLongDec'] = ((ObserverSetCatchDB['DegELong'].astype(int)) + \
                                                        ((ObserverSetCatchDB['MinELong'].astype(float))/60)).astype(float)
                    
                    ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                                ['StartLatDec', 'StartLongDec', 'EndLatDec', 'EndLongDec',
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
                    ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
                    ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)

                    ObserverSetCatchDB['StartTime_Temp'] =  [str(num).zfill(4) for num in ObserverSetCatchDB['StartTime']]
                    ObserverSetCatchDB['StartHour'] = (ObserverSetCatchDB['StartTime_Temp'].str[0:2]).astype(int)
                    ObserverSetCatchDB['StartMin'] = (ObserverSetCatchDB['StartTime_Temp'].str[2:4]).astype(int)
                    ObserverSetCatchDB.drop('StartTime_Temp', axis=1, inplace=True)
                    ObserverSetCatchDB['DeploymentDate_Start'] = pd.to_datetime((ObserverSetCatchDB.Year.astype(str)+ \
                                            ' '+\
                                            ObserverSetCatchDB.Month.astype(str)+ \
                                            ' '+\
                                            ObserverSetCatchDB.Day.astype(str)
                                            ))
                    ObserverSetCatchDB['StartDate']=ObserverSetCatchDB.apply(
                                lambda g: g.DeploymentDate_Start + pd.DateOffset(hours=(g.StartHour), 
                                minutes = (g.StartMin)),axis=1)
                    ObserverSetCatchDB['EndDate']=ObserverSetCatchDB.apply(
                                lambda g: g.DeploymentDate_Start + pd.DateOffset(hours=(g.StartHour + g.Duration), 
                                minutes = (g.StartMin)),axis=1)
                    ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                            ['StartDate', 'EndDate', 'StartLatDec', 'StartLongDec', 'EndLatDec', 'EndLongDec',
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
                    ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
                    ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)

                    ObserverSetCatchDB["EndDateTemp"] = (ObserverSetCatchDB['EndDate'].shift(1, 
                                    fill_value = ObserverSetCatchDB.iloc[0]['StartDate']))
                    ObserverSetCatchDB["HourSeparation"] = (
                    ((ObserverSetCatchDB["StartDate"]).apply(pd.to_datetime)) -\
                    ((ObserverSetCatchDB["EndDateTemp"]).apply(pd.to_datetime))
                    ).dt.total_seconds()/ 60 / 60

                    ObserverSetCatchDB["TempEndLatDec"] = (ObserverSetCatchDB['EndLatDec'].shift(1, 
                                    fill_value = ObserverSetCatchDB.iloc[0]['StartLatDec']))
                    ObserverSetCatchDB["TempEndLongDec"] = (ObserverSetCatchDB['EndLongDec'].shift(1, 
                                    fill_value = ObserverSetCatchDB.iloc[0]['StartLongDec']))
                    ObserverSetCatchDB['TowSeparation'] = ObserverSetCatchDB.apply(
                        lambda row: haversine(row['StartLatDec'], (-row['StartLongDec']), 
                        row['TempEndLatDec'], (-row['TempEndLongDec'])), axis=1)
                    
                    ObserverSetCatchDB['MaxTowSeparation'] = (ObserverSetCatchDB['HourSeparation']*(MaxTowSepSpeedLimit))*(1+MaxTowSeparationTolerance/100)

                    ObserverSetCatchDB['TowSepFlag'] = ObserverSetCatchDB.apply(
                        lambda row: ApplyTowSepFlag(row['MaxTowSeparation'], 
                                                    row['TowSeparation'], ), axis=1)
                    
                    ObserverSetCatchDB['DepIDentity'] = ObserverSetCatchDB['DeploymentUID'].apply(
                        lambda x: '-'.join(y[:-4] if i == len(x.split('-'))-1 else y for i,y in enumerate(x.split('-'))))
                    ObserverSetCatchDB['DepIDentity'] = ObserverSetCatchDB[
                        'DepIDentity'].apply(lambda x: x[:-1] if x.endswith('-') else x)
                    
                    ObserverSetCatchDB['DepIDChanged'] = (ObserverSetCatchDB["DepIDentity"].shift(1, 
                        fill_value=ObserverSetCatchDB.iloc[0]["DepIDentity"])) == (ObserverSetCatchDB["DepIDentity"])
                    ObserverSetCatchDB['DepChangeFlag'] = ObserverSetCatchDB.apply(
                        lambda row: ApplyDepIDChangeflag(row['DepIDChanged']), axis=1)
                    
                    ObserverSetCatchDB['SubTripChanged'] = (ObserverSetCatchDB["SubTripNumber"].shift(1, 
                        fill_value=ObserverSetCatchDB.iloc[0]["SubTripNumber"])) == (ObserverSetCatchDB["SubTripNumber"])
                    ObserverSetCatchDB['SubTripChangeFlag'] = ObserverSetCatchDB.apply(
                        lambda row: ApplySubTripChangeflag(row['SubTripChanged'],
                                                        row['SubTripNumber']), axis=1)
                    
                    ObserverSetCatchDB['TowSepErrorFlag'] = ObserverSetCatchDB.apply(
                        lambda row: ApplySepErrorFlag(row['TowSepFlag'], 
                                                    row['DepChangeFlag'],
                                                    row['SubTripChangeFlag']),
                                                    axis=1)
                    
                    ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                        ['StartDate','EndDate', 'HourSeparation', 'StartLatDec', 'StartLongDec', 'EndLatDec', 'EndLongDec',
                            'TowSeparation', 'MaxTowSeparation', 'TowSepErrorFlag', 'DepChangeFlag', 'SubTripChangeFlag',
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
                    ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)
                    Submit_QCFailedRange_TowSep(ObserverSetCatchDB)
                    ## QC FailCount
                    QCFailCount = ObserverSetCatchDB[(ObserverSetCatchDB.TowSepErrorFlag) == 'Yes']
                    QCFailCount  = QCFailCount.reset_index(drop=True)
                    QCFailCount  = pd.DataFrame(QCFailCount)
                    Length_QCFailedDF = len(QCFailCount)
                    return Length_QCFailedDF
                else:
                    DFcolumns = ['StartDate','EndDate', 'HourSeparation', 'StartLatDec', 'StartLongDec', 'EndLatDec', 'EndLongDec',
                        'TowSeparation', 'MaxTowSeparation', 'TowSepErrorFlag', 'DepChangeFlag', 'SubTripChangeFlag',
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
                    ObserverSetCatchDB = pd.DataFrame(columns = DFcolumns)
                    Submit_QCFailedRange_TowSep(ObserverSetCatchDB)
                    Length_QCFailedDF = len(ObserverSetCatchDB)
                    tkinter.messagebox.showinfo("Mobile GearType Not Present For Tow Separation QC",
                        "Mobile GearType - [1,2,3,9,10,14,16,17,18,21,66,67,97] Not present")
                    print('Mobile GearType Not Present')
                    return Length_QCFailedDF      
            else:
                DFcolumns = ['StartDate','EndDate', 'HourSeparation', 'StartLatDec', 'StartLongDec', 'EndLatDec', 'EndLongDec',
                        'TowSeparation', 'MaxTowSeparation', 'TowSepErrorFlag', 'DepChangeFlag', 'SubTripChangeFlag',
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
                ObserverSetCatchDB = pd.DataFrame(columns = DFcolumns)
                Submit_QCFailedRange_TowSep(ObserverSetCatchDB)
                Length_QCFailedDF = len(ObserverSetCatchDB)
                return Length_QCFailedDF
    
    FailedRangeTowDistance = RunTowDistance_QCAnalysis_SetCatch()
    FailedRangeTowSeparation = RunTowSeparation_QCAnalysis_SetCatch()

    TotalFailedQC_RangeValidation = (int(FailedRangeTowDistance) +\
                                     int(FailedRangeTowSeparation))
    return TotalFailedQC_RangeValidation
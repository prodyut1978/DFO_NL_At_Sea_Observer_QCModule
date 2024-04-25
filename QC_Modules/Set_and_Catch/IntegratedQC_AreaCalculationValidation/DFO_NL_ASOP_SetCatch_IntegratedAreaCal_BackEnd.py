from tkinter import*
import tkinter.ttk as ttk
from tkinter import messagebox
import sqlite3
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon

def RunIntegratedAreaCal_BackEnd():
    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_SetCatch_Val_Calculation = ("./BackEnd/Sqlite3_DB/QC_Check_CalculationConsistency_DB/DFO_NL_ASOP_SetCatch_Calculation.db")
    DB_SetCatch_Validation_Range = ("./BackEnd/Sqlite3_DB/QC_Check_RangeConsistency_DB/DFO_NL_ASOP_SetCatch_RangeValidation.db")
    Path_CSV_NAFOBoundary = './External_Import/AreaCalculated_Import/CSV_AreaProfile/DFO_NL_ASOP_NAFOAreaProfile.csv'
    Path_CSV_UnitAreaBoundary ='./External_Import/AreaCalculated_Import/CSV_AreaProfile/DFO_NL_ASOP_UnitAreaProfile.csv'

    def RunNAFO_AreaCalc_SetCatch():
        
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
                    ObserverSetCatchDB= (ObserverSetCatchDB.loc[:,
                        ['DataBase_ID','DeploymentUID','StartLatitude', 
                        'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
                        'UnitArea', 'RecordType', 'GearType']
                        ]).replace(['', None, np.nan, 'None'], 99999999)
           
                    ObserverSetCatchDB[['DeploymentUID', 'NAFODivision','UnitArea']
                        ] = ObserverSetCatchDB[['DeploymentUID','NAFODivision','UnitArea']
                        ].astype(str)
            
                    ObserverSetCatchDB[
                        ['DataBase_ID', 'RecordType','GearType']] = ObserverSetCatchDB[
                        ['DataBase_ID', 'RecordType','GearType']].astype(int)
                    
                    ObserverSetCatchDB[
                        ['StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude']
                        ] = ObserverSetCatchDB[['StartLatitude', 'StartLongitude', 
                        'EndLatitude', 'EndLongitude']].astype(float)
                    
                    ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                        ['DataBase_ID','DeploymentUID','StartLatitude', 
                        'StartLongitude', 'EndLatitude', 'EndLongitude', 
                        'NAFODivision', 'UnitArea', 'RecordType', 'GearType']]
                    ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
                    ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)
                    ObserverSetCatchDB = ObserverSetCatchDB[
                        (ObserverSetCatchDB.StartLatitude < 99999999.0) & 
                        (ObserverSetCatchDB.StartLongitude < 99999999.0) &
                        (ObserverSetCatchDB.EndLatitude < 99999999.0) &
                        (ObserverSetCatchDB.EndLongitude < 99999999.0)]
                    ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
                    ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)
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
    
        def fetchData_NAFO_AreaProfile():
            con= sqlite3.connect(DB_SetCatch_Val_Calculation)
            cur=con.cursor()
            cur.execute("SELECT * FROM SetCatch_NAFO_AreaProfileImported ORDER BY `NAFO_ID` ASC")
            rows=cur.fetchall()
            rows = pd.DataFrame(rows)
            con.close()
            return rows

        def GetNAFO_Profile():
            rows = fetchData_NAFO_AreaProfile()
            rows.rename(columns={0:'NAFO_ID', 1:'NAFOSubArea', 2:'NAFODivision',
                                 3:'NAFOSubDivision', 4:'NAFOLabel', 5:'NAFO_PointOrder', 
                                 6:'NAFO_Latitude',7:'NAFO_Longitude'},inplace = True)
            rows = rows.reset_index(drop=True)
            df_CSV_NAFOBoundary= pd.DataFrame(rows)
            if (len(df_CSV_NAFOBoundary)) >0:
                df_CSV_NAFOBoundary = df_CSV_NAFOBoundary.reset_index(drop=True)
                df_CSV_NAFOBoundary = pd.DataFrame(df_CSV_NAFOBoundary)
                return df_CSV_NAFOBoundary
            else:
                try:
                    df_CSV_NAFOBoundary = pd.read_csv(Path_CSV_NAFOBoundary, sep=',' , low_memory=False)
                    df_CSV_NAFOBoundary= (df_CSV_NAFOBoundary.loc[:,
                    ['NAFO_ID','NAFOSubArea','NAFODivision',
                    'NAFOSubDivision', 'NAFOLabel', 'NAFO_PointOrder', 
                    'NAFO_Latitude', 'NAFO_Longitude']]
                    ).replace(['', None, np.nan, 'None', ' ', '  ', '   ', '    '], 99999999)
                    df_CSV_NAFOBoundary = df_CSV_NAFOBoundary.reset_index(drop=True)
                    df_CSV_NAFOBoundary = pd.DataFrame(df_CSV_NAFOBoundary)
                    df_CSV_NAFOBoundary[['NAFO_ID', 'NAFO_PointOrder']] = df_CSV_NAFOBoundary[
                                        ['NAFO_ID','NAFO_PointOrder']].astype(int)
                    df_CSV_NAFOBoundary[['NAFO_Latitude', 'NAFO_Longitude']] = df_CSV_NAFOBoundary[
                                        ['NAFO_Latitude', 'NAFO_Longitude']].astype(float)
                    df_CSV_NAFOBoundary.sort_values(
                        by=['NAFODivision', 'NAFOLabel','NAFO_PointOrder'], inplace=True)
                    df_CSV_NAFOBoundary = df_CSV_NAFOBoundary.replace([99999999, 99999999.0, np.nan], '')
                    df_CSV_NAFOBoundary = df_CSV_NAFOBoundary.replace(['99999999.0', '99999999', '.'], 'None')
                    df_CSV_NAFOBoundary = df_CSV_NAFOBoundary.reset_index(drop=True)
                    df_CSV_NAFOBoundary = pd.DataFrame(df_CSV_NAFOBoundary)
                    SubmitImport_To_DBStorage(df_CSV_NAFOBoundary)
                    return df_CSV_NAFOBoundary 
                except:
                    messagebox.showerror('DFO-NL-ASOP NAFO Table Generation Error Message', 
                                    "Void DFO-NL-ASOP NAFO Table In The Archived Folder, Name - DFO_NL_ASOP_NAFOAreaRange.csv")
        
        def SubmitImport_To_DBStorage(Raw_Imported_Df):
            try:
                Import_To_DBStorage = pd.DataFrame(Raw_Imported_Df)
                sqliteConnection = sqlite3.connect(DB_SetCatch_Val_Calculation)
                cursor = sqliteConnection.cursor()
                Import_To_DBStorage.to_sql('SetCatch_NAFO_AreaProfileImported', sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        def BuildPolygon(Cordpoints):
            poly = Polygon(Cordpoints)
            return poly
        
        def Submit_NAFO_AreaCalc_SetCatch(ObserverSetCatchDB):
            try:
                Submit_To_DBStorage = pd.DataFrame(ObserverSetCatchDB)
                sqliteConnection = sqlite3.connect(DB_SetCatch_Val_Calculation)
                cursor = sqliteConnection.cursor()
                Submit_To_DBStorage.to_sql('SetCatch_NAFO_AreaQCAnalysis', sqliteConnection, 
                                           if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()
        
        def ChangeTruthValue(TruthValue):
            if TruthValue == True:
                return 'NAFO-QC Passed'
            else:
                return 'NAFO-QC Failed'

        def ChangeOutRangeValue(OutValue):
            if pd.isna(OutValue)==True:
                return 'POLYGON-Out of Range'
            elif OutValue == None:
                return 'POLYGON-Out of Range'
            elif OutValue == '':
                return 'POLYGON-Out of Range'
            else:
                return OutValue
        
        df_CSV_NAFOBoundary = GetNAFO_Profile()
        df_CSV_NAFOBoundary= df_CSV_NAFOBoundary.loc[:,
                    ['NAFO_ID','NAFOSubArea','NAFODivision',
                    'NAFOSubDivision', 'NAFOLabel', 'NAFO_PointOrder', 
                    'NAFO_Latitude', 'NAFO_Longitude']]
        df_CSV_NAFOBoundary['NAFOBoundaryPoints'] = list(zip(df_CSV_NAFOBoundary.NAFO_Latitude, df_CSV_NAFOBoundary.NAFO_Longitude))
        df_CSV_NAFOBoundary = df_CSV_NAFOBoundary.groupby('NAFOLabel').agg({'NAFOBoundaryPoints': lambda x: list(x)})
        df_CSV_NAFOBoundary.reset_index(inplace=True)
        df_CSV_NAFOBoundary= df_CSV_NAFOBoundary.reset_index(drop=True)
        NAFOBoundaryDF = pd.DataFrame(df_CSV_NAFOBoundary)
        NAFOBoundaryDF['Assigned_NAFOPloygon'] = NAFOBoundaryDF.apply(
                lambda row: BuildPolygon(row['NAFOBoundaryPoints']), axis=1)
        NAFOBoundaryDF = NAFOBoundaryDF.loc[:,
            ['NAFOLabel', 'Assigned_NAFOPloygon']]
        NAFOBoundaryDF.rename(columns={'NAFOLabel':'NAFODivision', 
            'Assigned_NAFOPloygon':'Assigned_NAFOPloygon'},inplace = True)
        NAFOBoundaryDF= NAFOBoundaryDF.reset_index(drop=True)
        NAFOBoundaryDF = pd.DataFrame(NAFOBoundaryDF)

        Get_RangeLimitVariables = fetchData_RangeLimitVariables()
        SLat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[6,'LowerRangeLimitValue'])
        SLat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[6,'UpperRangeLimitValue'])
        SLon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[7,'LowerRangeLimitValue'])
        SLon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[7,'UpperRangeLimitValue'])
        ELat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[8,'LowerRangeLimitValue'])
        ELat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[8,'UpperRangeLimitValue'])
        ELon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[9,'LowerRangeLimitValue'])
        ELon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[9,'UpperRangeLimitValue'])

        Return_ObserverSetCatchDB = get_ObserverSetCatchDB()
        ObserverSetCatchDB = Return_ObserverSetCatchDB[0]
        length_Complete_df = Return_ObserverSetCatchDB[1]
        if length_Complete_df > 0:
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
            ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
            ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)
            
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
           
            ObserverSetCatchDB = ObserverSetCatchDB.round({'StartLatDec': 4, 'StartLongDec': 4,
                                      'EndLatDec': 4, 'EndLongDec': 4})
            ObserverSetCatchDB['StartPoints'] = list(zip(ObserverSetCatchDB.StartLatDec, -ObserverSetCatchDB.StartLongDec))
            ObserverSetCatchDB['EndPoints'] = list(zip(ObserverSetCatchDB.EndLatDec, -ObserverSetCatchDB.EndLongDec))
            
            ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                        ['DeploymentUID','RecordType', 'NAFODivision',
                         'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude',
                         'StartPoints', 'EndPoints', 'GearType'
                         ]]
            ObserverSetCatchDB= ObserverSetCatchDB.reset_index(drop=True)
            ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB)
            Merge_WithSetCatchDB=  ObserverSetCatchDB.merge(
                        NAFOBoundaryDF, 
                        on = ['NAFODivision'],
                        indicator=True, 
                        how='outer').query('_merge == "both"')
            
            Merge_WithSetCatchDB[['DeploymentUID', 'NAFODivision']] = Merge_WithSetCatchDB[
                        ['DeploymentUID','NAFODivision']].astype(str)
            
            Merge_WithSetCatchDB[['RecordType', 'GearType']] = Merge_WithSetCatchDB[
                ['RecordType', 'GearType']].astype(int)
            
            Merge_WithSetCatchDB[['StartLatitude', 'StartLongitude', 'EndLatitude', 
             'EndLongitude']] = Merge_WithSetCatchDB[['StartLatitude', 'StartLongitude', 
             'EndLatitude', 'EndLongitude']].astype(float)
        
            Merge_WithSetCatchDB = Merge_WithSetCatchDB.loc[:,
                ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 
                 'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 
                 'StartPoints', 'EndPoints', 'Assigned_NAFOPloygon'
                ]]
            Merge_WithSetCatchDB = Merge_WithSetCatchDB.reset_index(drop=True)
            ObserverSetCatchDB = pd.DataFrame(Merge_WithSetCatchDB)

            ObserverSetCatchDB["NAFOValidityCheck_StartPoints_Temp"] = ObserverSetCatchDB.apply(
            lambda row: (Point(row["StartPoints"])).within(row["Assigned_NAFOPloygon"]), axis=1)
            ObserverSetCatchDB["NAFOValidityCheck_EndPoints_Temp"] = ObserverSetCatchDB.apply(
            lambda row: (Point(row["EndPoints"])).within(row["Assigned_NAFOPloygon"]), axis=1)

            ObserverSetCatchDB['NAFOValidityCheck_StartPoints'] = ObserverSetCatchDB.apply(
                lambda row: ChangeTruthValue(row['NAFOValidityCheck_StartPoints_Temp']), axis=1)
            ObserverSetCatchDB['NAFOValidityCheck_EndPoints'] = ObserverSetCatchDB.apply(
                lambda row: ChangeTruthValue(row['NAFOValidityCheck_EndPoints_Temp']), axis=1)

            ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 
                 'StartLatitude','StartLongitude', 'EndLatitude', 'EndLongitude', 
                 'StartPoints','EndPoints', 'NAFOValidityCheck_StartPoints',
                 'NAFOValidityCheck_EndPoints','Assigned_NAFOPloygon']]
            ObserverSetCatchDB['Assigned_NAFOPloygon'] = (ObserverSetCatchDB
                ['Assigned_NAFOPloygon'].map(lambda x: str(x)[0:7])) + ' - ' +\
                 ObserverSetCatchDB['NAFODivision']
            ObserverSetCatchDB = ObserverSetCatchDB[
            ((ObserverSetCatchDB.NAFOValidityCheck_StartPoints) == 'NAFO-QC Failed')
            ]
            ObserverSetCatchDB = ObserverSetCatchDB.reset_index(drop=True)
            ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB)
            Length_QCFailedDF = len(ObserverSetCatchDB)
            if Length_QCFailedDF > 0:
            ### Finding Calculated NAFOPloygon -Actual Polygon
                DFcolumns =['NAFODivision', 'Assigned_NAFOPloygon', 
                            'FindActualPolygon','StartPoints']
                dfList =pd.DataFrame(columns = DFcolumns)
                for point in ObserverSetCatchDB['StartPoints']:
                    NAFOBoundaryDF = pd.DataFrame(NAFOBoundaryDF)
                    NAFOBoundaryDF["FindActualPolygon"] = NAFOBoundaryDF.apply(
                    lambda row: (Point(point)).within(row["Assigned_NAFOPloygon"]), axis=1)
                    NAFOBoundaryDF1 = pd.DataFrame(NAFOBoundaryDF)
                    NAFOBoundaryDF1["StartPoints"] = str(point)
                    NAFOBoundaryDF1 = NAFOBoundaryDF[
                                    (NAFOBoundaryDF.FindActualPolygon ==True) 
                                    ]
                    if len(NAFOBoundaryDF1)>0:
                        NAFOBoundaryDF1 = NAFOBoundaryDF1.reset_index(drop=True)
                        NAFOBoundaryDF1 = pd.DataFrame(NAFOBoundaryDF1)
                        dfList = pd.concat([dfList, NAFOBoundaryDF1]).reset_index(drop=True)
                        dfList = dfList.reset_index(drop=True)
                        dfList = pd.DataFrame(dfList)
                dfList.rename(columns={'NAFODivision':'NAFODivision', 
                                    'Assigned_NAFOPloygon':'Calculated_NAFOPolygon_1',
                                    'FindActualPolygon':'FindActualPolygon',
                                    'StartPoints':'StartPoints'},inplace = True)
                dfList['Calculated_NAFOPolygon'] = (dfList
                        ['Calculated_NAFOPolygon_1'].map(lambda x: str(x)[0:7])) + ' - ' +\
                        dfList['NAFODivision']
                dfList = dfList.loc[:,
                        ['Calculated_NAFOPolygon', 'StartPoints']]
                dfList['StartPoints'] = (dfList['StartPoints'].astype(str))
                dfList = dfList.reset_index(drop=True)
                dfList = pd.DataFrame(dfList)

                ObserverSetCatchDB['StartPoints'] = (ObserverSetCatchDB['StartPoints'].astype(str))
                Merge_WithSetCatchDB_1=  ObserverSetCatchDB.merge(
                            dfList, 
                            on = ['StartPoints'],
                            indicator=True, 
                            how='left')
                Merge_WithSetCatchDB_1 = Merge_WithSetCatchDB_1.loc[:,
                    ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 
                    'StartLatitude','StartLongitude', 'EndLatitude', 'EndLongitude', 
                    'StartPoints','EndPoints', 'NAFOValidityCheck_StartPoints',
                    'NAFOValidityCheck_EndPoints','Assigned_NAFOPloygon', 
                    'Calculated_NAFOPolygon']]
                
                Merge_WithSetCatchDB_1['Calculated_NAFOPolygon'] = Merge_WithSetCatchDB_1.apply(
                    lambda row: ChangeOutRangeValue(row['Calculated_NAFOPolygon']), axis=1)
                Merge_WithSetCatchDB_1 = Merge_WithSetCatchDB_1.loc[:,
                        ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 
                    'StartLatitude','StartLongitude', 'EndLatitude', 'EndLongitude', 
                    'StartPoints','EndPoints', 'NAFOValidityCheck_StartPoints',
                    'NAFOValidityCheck_EndPoints','Assigned_NAFOPloygon', 
                    'Calculated_NAFOPolygon']]
            
                Merge_WithSetCatchDB_1 = Merge_WithSetCatchDB_1.reset_index(drop=True)
                ObserverSetCatchDB = pd.DataFrame(Merge_WithSetCatchDB_1)

                ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                    ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 
                    'StartLatitude','StartLongitude', 'EndLatitude', 'EndLongitude', 
                    'StartPoints','EndPoints', 'NAFOValidityCheck_StartPoints',
                    'NAFOValidityCheck_EndPoints','Assigned_NAFOPloygon', 
                    'Calculated_NAFOPolygon']].replace(['', None, np.nan, 
                    'None', ' ', '  ', '   ', '    '], 99999999)
                ObserverSetCatchDB[['DeploymentUID', 'NAFODivision',
                    'StartPoints','EndPoints', 'Assigned_NAFOPloygon', 
                    'Calculated_NAFOPolygon']] = ObserverSetCatchDB[
                    ['DeploymentUID','NAFODivision','StartPoints',
                        'EndPoints', 'Assigned_NAFOPloygon', 'Calculated_NAFOPolygon']
                    ].astype(str)
                
                ObserverSetCatchDB[['RecordType', 'GearType']] = ObserverSetCatchDB[
                    ['RecordType', 'GearType']].astype(int)
                
                ObserverSetCatchDB[['StartLatitude', 'StartLongitude', 'EndLatitude', 
                'EndLongitude']] = ObserverSetCatchDB[['StartLatitude', 'StartLongitude', 
                'EndLatitude', 'EndLongitude']].astype(float)

                ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                    ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 
                    'StartLatitude','StartLongitude', 'EndLatitude', 'EndLongitude', 
                    'StartPoints', 'EndPoints', 'NAFOValidityCheck_StartPoints',
                    'NAFOValidityCheck_EndPoints', 'Assigned_NAFOPloygon', 
                    'Calculated_NAFOPolygon']]
                ObserverSetCatchDB = ObserverSetCatchDB.replace([99999999, 99999999.0, np.nan], '')
                ObserverSetCatchDB = ObserverSetCatchDB.replace(['99999999.0', '99999999', '.'], 'None')
                ObserverSetCatchDB = ObserverSetCatchDB.reset_index(drop=True)
                ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB)

                ObserverSetCatchDB[['Year_Sep', 'ASOC_Sep', 'DepN_Sep', 'SetN_Sep']] = \
                ObserverSetCatchDB['DeploymentUID'].str.split('-', expand=True)
                ObserverSetCatchDB[['Year_Sep', 'ASOC_Sep', 'DepN_Sep', 'SetN_Sep']] = ObserverSetCatchDB[
                ['Year_Sep', 'ASOC_Sep', 'DepN_Sep', 'SetN_Sep']].astype(int)
                ObserverSetCatchDB.sort_values(by=['Year_Sep', 'ASOC_Sep', 
                    'DepN_Sep', 'SetN_Sep'], ascending=True, inplace=True)
                ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                    ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 
                    'StartLatitude','StartLongitude', 'EndLatitude', 'EndLongitude', 
                    'StartPoints', 'EndPoints', 'NAFOValidityCheck_StartPoints',
                    'NAFOValidityCheck_EndPoints', 'Assigned_NAFOPloygon', 
                    'Calculated_NAFOPolygon']]
                ObserverSetCatchDB = ObserverSetCatchDB.reset_index(drop=True)
                ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB)
                Submit_NAFO_AreaCalc_SetCatch(ObserverSetCatchDB)
                
                # QC FailCount
                QCFailCount = ObserverSetCatchDB[
                ((ObserverSetCatchDB.NAFOValidityCheck_StartPoints) == 'NAFO-QC Failed')
                ]
                QCFailCount  = QCFailCount.reset_index(drop=True)
                QCFailCount  = pd.DataFrame(QCFailCount)
                Length_QCFailedDF = len(QCFailCount)
                return Length_QCFailedDF
            else:
                DFcolumns = ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 
                 'StartLatitude','StartLongitude', 'EndLatitude', 'EndLongitude', 
                 'StartPoints', 'EndPoints', 'NAFOValidityCheck_StartPoints',
                 'NAFOValidityCheck_EndPoints', 'Assigned_NAFOPloygon', 
                 'Calculated_NAFOPolygon']
                ObserverSetCatchDB = pd.DataFrame(columns = DFcolumns)
                Submit_NAFO_AreaCalc_SetCatch(ObserverSetCatchDB)
                Length_QCFailedDF = len(ObserverSetCatchDB)
                return Length_QCFailedDF
        
        else:
            DFcolumns = ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 
                 'StartLatitude','StartLongitude', 'EndLatitude', 'EndLongitude', 
                 'StartPoints', 'EndPoints', 'NAFOValidityCheck_StartPoints',
                 'NAFOValidityCheck_EndPoints', 'Assigned_NAFOPloygon', 
                 'Calculated_NAFOPolygon']
            ObserverSetCatchDB = pd.DataFrame(columns = DFcolumns)
            Submit_NAFO_AreaCalc_SetCatch(ObserverSetCatchDB)
            Length_QCFailedDF = len(ObserverSetCatchDB)
            return Length_QCFailedDF

    def RunUnitAreaCalc_SetCatch():
    
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
                    ObserverSetCatchDB= (ObserverSetCatchDB.loc[:,
                        ['DataBase_ID','DeploymentUID','StartLatitude', 
                        'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
                        'UnitArea', 'RecordType', 'GearType']
                        ]).replace(['', None, np.nan, 'None'], 99999999)
           
                    ObserverSetCatchDB[['DeploymentUID', 'NAFODivision','UnitArea']
                        ] = ObserverSetCatchDB[['DeploymentUID','NAFODivision','UnitArea']
                        ].astype(str)
            
                    ObserverSetCatchDB[
                        ['DataBase_ID', 'RecordType','GearType']] = ObserverSetCatchDB[
                        ['DataBase_ID', 'RecordType','GearType']].astype(int)
                    
                    ObserverSetCatchDB[
                        ['StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude']
                        ] = ObserverSetCatchDB[['StartLatitude', 'StartLongitude', 
                        'EndLatitude', 'EndLongitude']].astype(float)
                    
                    ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                        ['DataBase_ID','DeploymentUID','StartLatitude', 
                        'StartLongitude', 'EndLatitude', 'EndLongitude', 
                        'NAFODivision', 'UnitArea', 'RecordType', 'GearType']]
                    ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
                    ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)
                    ObserverSetCatchDB = ObserverSetCatchDB[
                        (ObserverSetCatchDB.StartLatitude < 99999999.0) & 
                        (ObserverSetCatchDB.StartLongitude < 99999999.0) &
                        (ObserverSetCatchDB.EndLatitude < 99999999.0) &
                        (ObserverSetCatchDB.EndLongitude < 99999999.0)]
                    ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
                    ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)
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
        
        def fetchData_UnitAreaProfile():
            con= sqlite3.connect(DB_SetCatch_Val_Calculation)
            cur=con.cursor()
            cur.execute("SELECT * FROM SetCatch_Unit_AreaProfileImported ORDER BY `UnitArea_ID` ASC")
            rows=cur.fetchall()
            rows = pd.DataFrame(rows)
            con.close()
            return rows
        
        def GetUnitArea_Profile():
            rows = fetchData_UnitAreaProfile()
            if (len(rows)) >0:
                rows = fetchData_UnitAreaProfile()
                rows.rename(columns={0:'UnitArea_ID', 1:'NAFODivision', 2:'PointOrder',
                                    3:'UnitArea',    4:'UnitArea_Latitude', 5:'UnitArea_Longitude', 
                                    6:'UnitAreaLabel'},inplace = True)
                rows = rows.reset_index(drop=True)
                df_CSV_UnitAreaBoundary= pd.DataFrame(rows)
                return df_CSV_UnitAreaBoundary 
            else:
                df_CSV_UnitAreaBoundary = pd.read_csv(Path_CSV_UnitAreaBoundary, sep=',' , 
                        low_memory=False, keep_default_na=False, na_filter=False)
                df_CSV_UnitAreaBoundary= df_CSV_UnitAreaBoundary.loc[:,
                    ['UnitArea_ID','NAFODivision', 'PointOrder',
                    'UnitArea', 'UnitArea_Latitude', 'UnitArea_Longitude', 
                    'UnitAreaLabel']]
        
                df_CSV_UnitAreaBoundary[['NAFODivision', 'UnitArea', 'UnitAreaLabel']] = df_CSV_UnitAreaBoundary[
                                ['NAFODivision', 'UnitArea', 'UnitAreaLabel']].astype(str)
                    
                df_CSV_UnitAreaBoundary[['UnitArea_ID', 'PointOrder']] = df_CSV_UnitAreaBoundary[
                    ['UnitArea_ID', 'PointOrder']].astype(int)
                
                df_CSV_UnitAreaBoundary[['UnitArea_Latitude', 'UnitArea_Longitude']
                ] = df_CSV_UnitAreaBoundary[['UnitArea_Latitude', 
                'UnitArea_Longitude']].astype(float)

                df_CSV_UnitAreaBoundary= (df_CSV_UnitAreaBoundary.loc[:,
                ['UnitArea_ID','NAFODivision', 'PointOrder',
                'UnitArea', 'UnitArea_Latitude', 'UnitArea_Longitude', 
                'UnitAreaLabel']]
                ).replace(['', None, np.nan, 'None', ' ', '  ', '   ', '    '], 99999999)
                df_CSV_UnitAreaBoundary = df_CSV_UnitAreaBoundary.reset_index(drop=True)
                df_CSV_UnitAreaBoundary = pd.DataFrame(df_CSV_UnitAreaBoundary)
                df_CSV_UnitAreaBoundary[['UnitArea_ID', 'PointOrder']] = df_CSV_UnitAreaBoundary[
                                    ['UnitArea_ID','PointOrder']].astype(int)
                df_CSV_UnitAreaBoundary[['UnitArea_Latitude', 'UnitArea_Longitude']] = df_CSV_UnitAreaBoundary[
                                    ['UnitArea_Latitude', 'UnitArea_Longitude']].astype(float)
                df_CSV_UnitAreaBoundary.sort_values(
                    by=['NAFODivision', 'UnitArea','PointOrder'], inplace=True)
                df_CSV_UnitAreaBoundary = df_CSV_UnitAreaBoundary.replace([99999999, 99999999.0, np.nan], '')
                df_CSV_UnitAreaBoundary = df_CSV_UnitAreaBoundary.replace(['99999999.0', '99999999', '.'], 'None')
                df_CSV_UnitAreaBoundary = df_CSV_UnitAreaBoundary.reset_index(drop=True)
                df_CSV_UnitAreaBoundary = pd.DataFrame(df_CSV_UnitAreaBoundary)
                SubmitImport_To_DBStorage(df_CSV_UnitAreaBoundary)
                return df_CSV_UnitAreaBoundary 

        def SubmitImport_To_DBStorage(Raw_Imported_Df):
            try:
                Import_To_DBStorage = pd.DataFrame(Raw_Imported_Df)
                sqliteConnection = sqlite3.connect(DB_SetCatch_Val_Calculation)
                cursor = sqliteConnection.cursor()
                Import_To_DBStorage.to_sql('SetCatch_Unit_AreaProfileImported', 
                    sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()
        
        def BuildPolygon(Cordpoints):
            poly = Polygon(Cordpoints)
            return poly
        
        def Submit_UnitAreaCalc_SetCatch(ObserverSetCatchDB):
            try:
                Submit_To_DBStorage = pd.DataFrame(ObserverSetCatchDB)
                sqliteConnection = sqlite3.connect(DB_SetCatch_Val_Calculation)
                cursor = sqliteConnection.cursor()
                Submit_To_DBStorage.to_sql('SetCatch_UnitAreaQCAnalysis', sqliteConnection, 
                                            if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()
        
        def ChangeTruthValue(TruthValue):
            if TruthValue == True:
                return 'UnitArea-QC Passed'
            else:
                return 'UnitArea-QC Failed'
        
        def ChangeOutRangeValue(OutValue):
            if pd.isna(OutValue)==True:
                return 'POLYGON-Out of Range'
            elif OutValue == None:
                return 'POLYGON-Out of Range'
            elif OutValue == '':
                return 'POLYGON-Out of Range'
            else:
                return OutValue
        
        df_CSV_UnitAreaBoundary = GetUnitArea_Profile()
        df_CSV_UnitAreaBoundary= df_CSV_UnitAreaBoundary.loc[:,
                ['UnitArea_ID','NAFODivision', 'PointOrder',
                'UnitArea', 'UnitArea_Latitude', 'UnitArea_Longitude', 
                'UnitAreaLabel']]
        
        df_CSV_UnitAreaBoundary[['NAFODivision', 'UnitArea', 'UnitAreaLabel']] = df_CSV_UnitAreaBoundary[
                        ['NAFODivision', 'UnitArea', 'UnitAreaLabel']].astype(str)
            
        df_CSV_UnitAreaBoundary[['UnitArea_ID', 'PointOrder']] = df_CSV_UnitAreaBoundary[
            ['UnitArea_ID', 'PointOrder']].astype(int)
        
        df_CSV_UnitAreaBoundary[['UnitArea_Latitude', 'UnitArea_Longitude']
        ] = df_CSV_UnitAreaBoundary[['UnitArea_Latitude', 
        'UnitArea_Longitude']].astype(float)

        df_CSV_UnitAreaBoundary['UnitAreaBoundaryPoints'] = list(zip(df_CSV_UnitAreaBoundary.UnitArea_Latitude, 
                    df_CSV_UnitAreaBoundary.UnitArea_Longitude))
        df_CSV_UnitAreaBoundary = df_CSV_UnitAreaBoundary.groupby('UnitAreaLabel').agg(
            {'UnitAreaBoundaryPoints': lambda x: list(x)})
        df_CSV_UnitAreaBoundary.reset_index(inplace=True)
        df_CSV_UnitAreaBoundary= df_CSV_UnitAreaBoundary.reset_index(drop=True)
    
        UnitAreaBoundaryDF = pd.DataFrame(df_CSV_UnitAreaBoundary)
        UnitAreaBoundaryDF['Assigned_UnitAreaPolygon'] = UnitAreaBoundaryDF.apply(
                lambda row: BuildPolygon(row['UnitAreaBoundaryPoints']), axis=1)
        UnitAreaBoundaryDF = UnitAreaBoundaryDF.loc[:,
            ['UnitAreaLabel', 'Assigned_UnitAreaPolygon']]
        UnitAreaBoundaryDF.rename(columns={'UnitAreaLabel':'UnitArea', 
            'Assigned_UnitAreaPolygon':'Assigned_UnitAreaPolygon'},inplace = True)
        UnitAreaBoundaryDF= UnitAreaBoundaryDF.reset_index(drop=True)
        UnitAreaBoundaryDF = pd.DataFrame(UnitAreaBoundaryDF)
        
        Get_RangeLimitVariables = fetchData_RangeLimitVariables()
        SLat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[6,'LowerRangeLimitValue'])
        SLat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[6,'UpperRangeLimitValue'])
        SLon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[7,'LowerRangeLimitValue'])
        SLon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[7,'UpperRangeLimitValue'])
        ELat_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[8,'LowerRangeLimitValue'])
        ELat_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[8,'UpperRangeLimitValue'])
        ELon_LowerRangeLimitValue=float(Get_RangeLimitVariables.at[9,'LowerRangeLimitValue'])
        ELon_UpperRangeLimitValue= float(Get_RangeLimitVariables.at[9,'UpperRangeLimitValue'])

        Return_ObserverSetCatchDB = get_ObserverSetCatchDB()
        ObserverSetCatchDB = Return_ObserverSetCatchDB[0]
        length_Complete_df = Return_ObserverSetCatchDB[1]
        
        if length_Complete_df > 0:
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
            ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
            ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)
            
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
            
            ObserverSetCatchDB = ObserverSetCatchDB.round({'StartLatDec': 4, 'StartLongDec': 4,
                                        'EndLatDec': 4, 'EndLongDec': 4})
            ObserverSetCatchDB['StartPoints'] = list(zip(ObserverSetCatchDB.StartLatDec, -ObserverSetCatchDB.StartLongDec))
            ObserverSetCatchDB['EndPoints'] = list(zip(ObserverSetCatchDB.EndLatDec, -ObserverSetCatchDB.EndLongDec))
            
            ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                        ['DeploymentUID','RecordType', 'NAFODivision', 'UnitArea',
                        'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude',
                        'StartPoints', 'EndPoints', 'GearType'
                        ]]
            ObserverSetCatchDB = ObserverSetCatchDB[
                (ObserverSetCatchDB.UnitArea != '99999999')
                ]
            ObserverSetCatchDB= ObserverSetCatchDB.reset_index(drop=True)
            ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB)
        
            ObserverSetCatchDB= ObserverSetCatchDB.reset_index(drop=True)
            ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB)
            Merge_WithSetCatchDB=  ObserverSetCatchDB.merge(
                        UnitAreaBoundaryDF, 
                        on = ['UnitArea'],
                        indicator=True, 
                        how='outer').query('_merge == "both"')
            
            Merge_WithSetCatchDB[['DeploymentUID', 'NAFODivision', 'UnitArea']] = Merge_WithSetCatchDB[
                        ['DeploymentUID','NAFODivision', 'UnitArea']].astype(str)
            
            Merge_WithSetCatchDB[['RecordType', 'GearType']] = Merge_WithSetCatchDB[
                ['RecordType', 'GearType']].astype(int)
            
            Merge_WithSetCatchDB[['StartLatitude', 'StartLongitude', 'EndLatitude', 
                'EndLongitude']] = Merge_WithSetCatchDB[['StartLatitude', 'StartLongitude', 
                'EndLatitude', 'EndLongitude']].astype(float)
        
            Merge_WithSetCatchDB = Merge_WithSetCatchDB.loc[:,
                ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 'UnitArea',
                'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 
                'StartPoints', 'EndPoints', 'Assigned_UnitAreaPolygon'
                ]]
            Merge_WithSetCatchDB = Merge_WithSetCatchDB.reset_index(drop=True)
            ObserverSetCatchDB = pd.DataFrame(Merge_WithSetCatchDB)

            ObserverSetCatchDB["UAValidityCheck_SP_Temp"] = ObserverSetCatchDB.apply(
            lambda row: (Point(row["StartPoints"])).within(row["Assigned_UnitAreaPolygon"]), axis=1)
            ObserverSetCatchDB["UAValidityCheck_EP_Temp"] = ObserverSetCatchDB.apply(
            lambda row: (Point(row["EndPoints"])).within(row["Assigned_UnitAreaPolygon"]), axis=1)

            ObserverSetCatchDB['UAValidityCheck_StartPoints'] = ObserverSetCatchDB.apply(
                lambda row: ChangeTruthValue(row['UAValidityCheck_SP_Temp']), axis=1)
            ObserverSetCatchDB['UAValidityCheck_EndPoints'] = ObserverSetCatchDB.apply(
                lambda row: ChangeTruthValue(row['UAValidityCheck_EP_Temp']), axis=1)

            ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 'UnitArea',
                'StartLatitude','StartLongitude', 'EndLatitude', 'EndLongitude', 
                'StartPoints','EndPoints', 'UAValidityCheck_StartPoints',
                'UAValidityCheck_EndPoints','Assigned_UnitAreaPolygon']]
            ObserverSetCatchDB = ObserverSetCatchDB[
            ((ObserverSetCatchDB.UAValidityCheck_StartPoints) == 'UnitArea-QC Failed')
            ]
            ObserverSetCatchDB  = ObserverSetCatchDB.reset_index(drop=True)
            ObserverSetCatchDB  = pd.DataFrame(ObserverSetCatchDB)
            Length_QCFailedDF = len(ObserverSetCatchDB)
            
            if Length_QCFailedDF > 0:
                ## Finding Calculated UnitAreaPloygon -Actual Polygon
                DFcolumns =['UnitArea', 'Assigned_UnitAreaPolygon', 
			                'FindActualPolygon','StartPoints']
                dfList =pd.DataFrame(columns = DFcolumns)
                for point in ObserverSetCatchDB['StartPoints']:
                    UnitAreaBoundaryDF = pd.DataFrame(UnitAreaBoundaryDF)
                    UnitAreaBoundaryDF["FindActualPolygon"] = UnitAreaBoundaryDF.apply(
		            lambda row: (Point(point)).within(row["Assigned_UnitAreaPolygon"]), axis=1)
                    UnitAreaBoundaryDF1 = pd.DataFrame(UnitAreaBoundaryDF)
                    UnitAreaBoundaryDF1["StartPoints"] = str(point)
                    UnitAreaBoundaryDF1 = UnitAreaBoundaryDF[
                                    (UnitAreaBoundaryDF.FindActualPolygon ==True) 
						]
                    if len(UnitAreaBoundaryDF1)>0:
                        UnitAreaBoundaryDF1 = UnitAreaBoundaryDF1.reset_index(drop=True)
                        UnitAreaBoundaryDF1 = pd.DataFrame(UnitAreaBoundaryDF1)
                        dfList = pd.concat([dfList, UnitAreaBoundaryDF1]).reset_index(drop=True)
                        dfList = dfList.reset_index(drop=True)
                        dfList = pd.DataFrame(dfList)
                dfList.rename(columns={'UnitArea':'UnitArea', 
                    'Assigned_UnitAreaPolygon':'Calculated_UnitAreaPolygon_1',
                    'FindActualPolygon':'FindActualPolygon',
                    'StartPoints':'StartPoints'},inplace = True)
                dfList['Calculated_UnitAreaPolygon'] = (dfList
			          ['Calculated_UnitAreaPolygon_1'].map(lambda x: str(x)[0:7])) + ' - ' +\
			          dfList['UnitArea']
                dfList = dfList.loc[:,
                        ['Calculated_UnitAreaPolygon', 'StartPoints']]
                dfList['StartPoints'] = (dfList['StartPoints'].astype(str))
                dfList = dfList.reset_index(drop=True)
                dfList = pd.DataFrame(dfList)
                ObserverSetCatchDB['StartPoints'] = (ObserverSetCatchDB['StartPoints'].astype(str))
                Merge_WithSetCatchDB_1=  ObserverSetCatchDB.merge(
                            dfList, 
                            on = ['StartPoints'],
                            indicator=True, 
                            how='left')
                Merge_WithSetCatchDB_1 = Merge_WithSetCatchDB_1.loc[:,
                ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 'UnitArea',
                'StartLatitude','StartLongitude', 'EndLatitude', 'EndLongitude', 
                'StartPoints', 'EndPoints', 'UAValidityCheck_StartPoints',
                'UAValidityCheck_EndPoints', 'Assigned_UnitAreaPolygon',
                'Calculated_UnitAreaPolygon']]
                Merge_WithSetCatchDB_1['Calculated_UnitAreaPolygon'] = Merge_WithSetCatchDB_1.apply(
                lambda row: ChangeOutRangeValue(row['Calculated_UnitAreaPolygon']), axis=1)
                Merge_WithSetCatchDB_1 = Merge_WithSetCatchDB_1.loc[:,
                ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 'UnitArea',
                'StartLatitude','StartLongitude', 'EndLatitude', 'EndLongitude', 
                'StartPoints', 'EndPoints', 'UAValidityCheck_StartPoints',
                'UAValidityCheck_EndPoints', 'Assigned_UnitAreaPolygon',
                'Calculated_UnitAreaPolygon']]

                Merge_WithSetCatchDB_1 = Merge_WithSetCatchDB_1.reset_index(drop=True)
                ObserverSetCatchDB = pd.DataFrame(Merge_WithSetCatchDB_1)
                ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 'UnitArea',
                'StartLatitude','StartLongitude', 'EndLatitude', 'EndLongitude', 
                'StartPoints', 'EndPoints', 'UAValidityCheck_StartPoints',
                'UAValidityCheck_EndPoints', 'Assigned_UnitAreaPolygon',
                'Calculated_UnitAreaPolygon']].replace(['', None, np.nan, 
                'None', ' ', '  ', '   ', '    '], 99999999)

                ObserverSetCatchDB[['DeploymentUID', 'NAFODivision','UnitArea',
                'StartPoints','EndPoints', 'Assigned_UnitAreaPolygon',
                'Calculated_UnitAreaPolygon']] = ObserverSetCatchDB[
                ['DeploymentUID','NAFODivision','UnitArea','StartPoints',
                'EndPoints', 'Assigned_UnitAreaPolygon',
                'Calculated_UnitAreaPolygon']].astype(str)
                
                ObserverSetCatchDB[['RecordType', 'GearType']] = ObserverSetCatchDB[
                    ['RecordType', 'GearType']].astype(int)
                
                ObserverSetCatchDB[['StartLatitude', 'StartLongitude', 'EndLatitude', 
                    'EndLongitude']] = ObserverSetCatchDB[['StartLatitude', 'StartLongitude', 
                'EndLatitude', 'EndLongitude']].astype(float)

                ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                    ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 'UnitArea',
                    'StartLatitude','StartLongitude', 'EndLatitude', 'EndLongitude', 
                    'StartPoints', 'EndPoints', 'UAValidityCheck_StartPoints',
                    'UAValidityCheck_EndPoints', 'Assigned_UnitAreaPolygon',
                    'Calculated_UnitAreaPolygon']]
                ObserverSetCatchDB = ObserverSetCatchDB.replace([99999999, 99999999.0, np.nan], '')
                ObserverSetCatchDB = ObserverSetCatchDB.replace(['99999999.0', '99999999', '.'], 'None')
                ObserverSetCatchDB = ObserverSetCatchDB.reset_index(drop=True)
                ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB)

                ObserverSetCatchDB[['Year_Sep', 'ASOC_Sep', 'DepN_Sep', 'SetN_Sep']] = \
                ObserverSetCatchDB['DeploymentUID'].str.split('-', expand=True)
                ObserverSetCatchDB[['Year_Sep', 'ASOC_Sep', 'DepN_Sep', 'SetN_Sep']] = ObserverSetCatchDB[
                ['Year_Sep', 'ASOC_Sep', 'DepN_Sep', 'SetN_Sep']].astype(int)
                ObserverSetCatchDB.sort_values(by=['Year_Sep', 'ASOC_Sep', 
                    'DepN_Sep', 'SetN_Sep'], ascending=True, inplace=True)
                ObserverSetCatchDB = ObserverSetCatchDB.loc[:,
                    ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 'UnitArea',
                    'StartLatitude','StartLongitude', 'EndLatitude', 'EndLongitude', 
                    'StartPoints', 'EndPoints', 'UAValidityCheck_StartPoints',
                    'UAValidityCheck_EndPoints', 'Assigned_UnitAreaPolygon',
                    'Calculated_UnitAreaPolygon']]
                ObserverSetCatchDB = ObserverSetCatchDB.reset_index(drop=True)
                ObserverSetCatchDB = pd.DataFrame(ObserverSetCatchDB)
                Submit_UnitAreaCalc_SetCatch(ObserverSetCatchDB)
                # QC FailCount
                QCFailCount = ObserverSetCatchDB[
                ((ObserverSetCatchDB.UAValidityCheck_StartPoints) == 'UnitArea-QC Failed')
                ]
                QCFailCount  = QCFailCount.reset_index(drop=True)
                QCFailCount  = pd.DataFrame(QCFailCount)
                Length_QCFailedDF = len(QCFailCount)
                return Length_QCFailedDF
            
            else:
                DFcolumns = ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 'UnitArea',
                'StartLatitude','StartLongitude', 'EndLatitude', 'EndLongitude', 
                'StartPoints', 'EndPoints', 'UAValidityCheck_StartPoints',
                'UAValidityCheck_EndPoints', 'Assigned_UnitAreaPolygon', 'Calculated_UnitAreaPolygon']
            ObserverSetCatchDB = pd.DataFrame(columns = DFcolumns)
            Submit_UnitAreaCalc_SetCatch(ObserverSetCatchDB)
            Length_QCFailedDF = len(ObserverSetCatchDB)
            return Length_QCFailedDF
        
        else:
            DFcolumns = ['DeploymentUID', 'RecordType', 'GearType', 'NAFODivision', 'UnitArea',
                'StartLatitude','StartLongitude', 'EndLatitude', 'EndLongitude', 
                'StartPoints', 'EndPoints', 'UAValidityCheck_StartPoints',
                'UAValidityCheck_EndPoints', 'Assigned_UnitAreaPolygon', 'Calculated_UnitAreaPolygon']
            ObserverSetCatchDB = pd.DataFrame(columns = DFcolumns)
            Submit_UnitAreaCalc_SetCatch(ObserverSetCatchDB)
            Length_QCFailedDF = len(ObserverSetCatchDB)
            return Length_QCFailedDF

    FailedNAFOAreaCal = RunNAFO_AreaCalc_SetCatch()
    FailedUnitAreaCal = RunUnitAreaCalc_SetCatch()
    
    TotalFailedQC_Validation = (int(FailedNAFOAreaCal) + int(FailedUnitAreaCal))
    return TotalFailedQC_Validation
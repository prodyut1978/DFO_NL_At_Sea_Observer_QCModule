from tkinter import*
from tkinter import messagebox
import tkinter.messagebox
import sqlite3
import pandas as pd
import numpy as np

DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
DB_SetCatch_Validation_Consistency = ("./BackEnd/Sqlite3_DB/QC_Check_ConsistencyValidate_DB/DFO_NL_ASOP_SetCatch_ConsistencyValidation.db")
DB_SetCatch_Validation_Range = ("./BackEnd/Sqlite3_DB/QC_Check_RangeConsistency_DB/DFO_NL_ASOP_SetCatch_RangeValidation.db")


def RunSetCatch_ConsistencyValidation_BackEnd():

    def RunConsistencyFailed_Year_CntryQuota():
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,
                                        ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                         'ASOCCode','ObserverNumber','DeploymentNumber',
                                         'SetNumber', 'VesselSideNumber', 'RecordType',
                                         'Year','Country','Quota']]
                    SetCatchProfileDB_DF.sort_values(by=['ASOCCode','DeploymentNumber','SetNumber',
                                 'RecordType'], inplace=True)
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

        def Submit_Year_Cntry_Quota_FailConsistency(Year_FailConsistency_DF,
                                                    Country_FailConsistency_DF,
                                                    Quota_FailConsistency_DF,
                                                    YCQ_FailedConsistencySummaryDF):
            try:
                Year_FailConsistency_DF = pd.DataFrame(Year_FailConsistency_DF)
                Country_FailConsistency_DF = pd.DataFrame(Country_FailConsistency_DF)
                Quota_FailConsistency_DF = pd.DataFrame(Quota_FailConsistency_DF)
                YCQ_FailedConsistencySummaryDF = pd.DataFrame(YCQ_FailedConsistencySummaryDF)
                
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Consistency)
                cursor = sqliteConnection.cursor()
                Year_FailConsistency_DF.to_sql('SetCatch_Year_FailConsistency_DF',
                                            sqliteConnection, if_exists="replace", index =False)
                Country_FailConsistency_DF.to_sql('SetCatch_Country_FailConsistency_DF',
                                            sqliteConnection, if_exists="replace", index =False)
                Quota_FailConsistency_DF.to_sql('SetCatch_Quota_FailConsistency_DF',
                                            sqliteConnection, if_exists="replace", index =False)
                YCQ_FailedConsistencySummaryDF.to_sql('SetCatch_YCQ_FailConsis_SummaryDF',
                                            sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        SetCatchProfileDB_DF = GetSetCatchProfileDB()
    
        ## QC On Year_Cntry_Quota
        Year_Cntry_Quota_FailConsistency= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                             'ASOCCode','ObserverNumber','DeploymentNumber',
                             'SetNumber', 'VesselSideNumber', 'RecordType',
                             'Year','Country','Quota']]).replace(['','None'], 99999999)
        
        Year_Cntry_Quota_FailConsistency[['DataBase_ID','RecordIdentifier','ASOCCode',
                                        'DeploymentNumber','SetNumber',
                                        'RecordType','Year',
                                        'Country','Quota']] = Year_Cntry_Quota_FailConsistency[
                                        ['DataBase_ID','RecordIdentifier','ASOCCode',
                                        'DeploymentNumber','SetNumber',
                                        'RecordType','Year',
                                        'Country','Quota']].astype(int)
        Year_Cntry_Quota_FailConsistency[
            ['DeploymentUID','ObserverNumber', 'VesselSideNumber']] = Year_Cntry_Quota_FailConsistency[
            ['DeploymentUID','ObserverNumber','VesselSideNumber']].astype(str)
        
        ## Year Filter & Building Year-DF
        Filter_DN_YCQ_Fail_Year = (Year_Cntry_Quota_FailConsistency.groupby(
            ['ASOCCode', 'ObserverNumber', 'DeploymentNumber'], 
            as_index=False)['Year'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
        Filter_DN_YCQ_Fail_Year = Filter_DN_YCQ_Fail_Year[
                        (Filter_DN_YCQ_Fail_Year.Year) > 1]
        Filter_DN_YCQ_Fail_Year = Filter_DN_YCQ_Fail_Year.loc[:,['ASOCCode', 'ObserverNumber','DeploymentNumber']]
        Filter_DN_YCQ_Fail_Year = Filter_DN_YCQ_Fail_Year.merge(
            Year_Cntry_Quota_FailConsistency, 
            on = ['ASOCCode', 'ObserverNumber', 'DeploymentNumber'], indicator=True, 
            how='outer').query('_merge == "both"')
        Filter_DN_YCQ_Fail_Year  = Filter_DN_YCQ_Fail_Year.reset_index(drop=True)
        Filter_DN_YCQ_Fail_Year= (Filter_DN_YCQ_Fail_Year.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID',
                'ASOCCode','ObserverNumber','DeploymentNumber',
                'SetNumber', 'VesselSideNumber', 'RecordType',
                'Year','Country','Quota']])
        Filter_DN_YCQ_Fail_Year = Filter_DN_YCQ_Fail_Year.replace([99999999, 99999999.0, '.'], '')
        Filter_DN_YCQ_Fail_Year = Filter_DN_YCQ_Fail_Year.replace(['99999999', '.'], 'None')
        Filter_DN_YCQ_Fail_Year  = Filter_DN_YCQ_Fail_Year.reset_index(drop=True)
        Filter_DN_YCQ_Fail_Year['QC_Year'] ="Year Consistency Failed"
        Year_FailConsistency_DF  = pd.DataFrame(Filter_DN_YCQ_Fail_Year)
        if len(Year_FailConsistency_DF)>0:
            Year_FailConsistency_Summary = (Year_FailConsistency_DF.groupby(
                ['Year', 'ASOCCode', 'ObserverNumber','DeploymentNumber'],
                as_index=False)['SetNumber'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
            Year_FailConsistency_Summary.rename(columns={'Year':'Year',
                                                         'ASOCCode':'ASOCCode',
                                                         'ObserverNumber':'ObserverNumber',
                                                         'DeploymentNumber':'DeploymentNumber',
                                                         'SetNumber':'NumOfSetsPerDeploymentNumber'
                                                        },inplace = True)
            Year_FailConsistency_Summary  = Year_FailConsistency_Summary.reset_index(drop=True)
            Year_FailConsistency_Summary  = pd.DataFrame(Year_FailConsistency_Summary)
            FailCount_Year_Consistency = Year_FailConsistency_Summary.drop_duplicates(
                                        subset=['ASOCCode', 'ObserverNumber','DeploymentNumber'], keep="first")
            Len_FailCount_Year_Consistency = len(FailCount_Year_Consistency)
        else:
            Len_FailCount_Year_Consistency = 0
        
        ## Country Filter & Building Country-DF
        Filter_DN_YCQ_Fail_Country = (Year_Cntry_Quota_FailConsistency.groupby(
            ['ASOCCode', 'ObserverNumber', 'DeploymentNumber'], 
            as_index=False)['Country'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
        Filter_DN_YCQ_Fail_Country = Filter_DN_YCQ_Fail_Country[
                        (Filter_DN_YCQ_Fail_Country.Country) > 1]
        Filter_DN_YCQ_Fail_Country = Filter_DN_YCQ_Fail_Country.loc[:,
                        ['ASOCCode', 'ObserverNumber', 'DeploymentNumber']]
        Filter_DN_YCQ_Fail_Country = Filter_DN_YCQ_Fail_Country.merge(
                        Year_Cntry_Quota_FailConsistency, 
                        on = ['ASOCCode', 'ObserverNumber', 'DeploymentNumber'], indicator=True, 
                        how='outer').query('_merge == "both"')
        Filter_DN_YCQ_Fail_Country  = Filter_DN_YCQ_Fail_Country.reset_index(drop=True)
        Filter_DN_YCQ_Fail_Country= (Filter_DN_YCQ_Fail_Country.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID',
                 'ASOCCode','ObserverNumber','DeploymentNumber',
                 'SetNumber', 'VesselSideNumber', 'RecordType',
                 'Year','Country','Quota']])
        Filter_DN_YCQ_Fail_Country = Filter_DN_YCQ_Fail_Country.replace([99999999, 99999999.0, '.'], '')
        Filter_DN_YCQ_Fail_Country = Filter_DN_YCQ_Fail_Country.replace(['99999999', '.'], 'None')
        Filter_DN_YCQ_Fail_Country  = Filter_DN_YCQ_Fail_Country.reset_index(drop=True)
        Filter_DN_YCQ_Fail_Country['QC_Country'] ="Country Consistency Failed"
        Country_FailConsistency_DF  = pd.DataFrame(Filter_DN_YCQ_Fail_Country)
        
        ## Country_FailConsistency_DF Summary
        if len(Country_FailConsistency_DF)>0:
            Country_FailConsistency_Summary = (Country_FailConsistency_DF.groupby([
                    'Country', 'ASOCCode', 'ObserverNumber','DeploymentNumber'], 
                    as_index=False)['SetNumber'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
            Country_FailConsistency_Summary.rename(columns={'Country':'Country',
                                                            'ASOCCode':'ASOCCode',
                                                            'ObserverNumber':'ObserverNumber',
                                                            'DeploymentNumber':'DeploymentNumber',
                                                            'SetNumber':'NumOfSetsPerDeploymentNumber'
                                                            },inplace = True)
            Country_FailConsistency_Summary  = Country_FailConsistency_Summary.reset_index(drop=True)
            Country_FailConsistency_Summary  = pd.DataFrame(Country_FailConsistency_Summary)
            FailCount_Country_Consistency = Country_FailConsistency_Summary.drop_duplicates(
                                        subset=['ASOCCode', 'ObserverNumber','DeploymentNumber'], keep="first")
            Len_FailCount_Country_Consistency = len(FailCount_Country_Consistency)
        else:
            Len_FailCount_Country_Consistency = 0
            
        ## Quota Filter & Building Quota-DF
        Filter_DN_YCQ_Fail_Quota = (Year_Cntry_Quota_FailConsistency.groupby(
            ['ASOCCode', 'ObserverNumber', 'DeploymentNumber'],
            as_index=False)['Quota'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
        Filter_DN_YCQ_Fail_Quota = Filter_DN_YCQ_Fail_Quota[
                        (Filter_DN_YCQ_Fail_Quota.Quota) > 1]
        Filter_DN_YCQ_Fail_Quota = Filter_DN_YCQ_Fail_Quota.loc[:,
            ['ASOCCode', 'ObserverNumber', 'DeploymentNumber']]
        Filter_DN_YCQ_Fail_Quota = Filter_DN_YCQ_Fail_Quota.merge(
            Year_Cntry_Quota_FailConsistency, 
            on = ['ASOCCode', 'ObserverNumber', 'DeploymentNumber'], indicator=True, 
            how='outer').query('_merge == "both"')
        Filter_DN_YCQ_Fail_Quota  = Filter_DN_YCQ_Fail_Quota.reset_index(drop=True)
        Filter_DN_YCQ_Fail_Quota= (Filter_DN_YCQ_Fail_Quota.loc[:,
            ['DataBase_ID','RecordIdentifier','DeploymentUID',
            'ASOCCode','ObserverNumber','DeploymentNumber',
            'SetNumber', 'VesselSideNumber', 'RecordType',
            'Year','Country','Quota']])
        Filter_DN_YCQ_Fail_Quota = Filter_DN_YCQ_Fail_Quota.replace([99999999, 99999999.0, '.'], '')
        Filter_DN_YCQ_Fail_Quota = Filter_DN_YCQ_Fail_Quota.replace(['99999999', '.'], 'None')
        Filter_DN_YCQ_Fail_Quota  = Filter_DN_YCQ_Fail_Quota.reset_index(drop=True)
        Filter_DN_YCQ_Fail_Quota['QC_Quota'] ="Quota Consistency Failed"
        Quota_FailConsistency_DF  = pd.DataFrame(Filter_DN_YCQ_Fail_Quota)
        
        ## Quota_FailConsistency_DF Summary
        if len(Quota_FailConsistency_DF)>0:
            Quota_FailConsistency_Summary = (Quota_FailConsistency_DF.groupby([
                    'Quota', 'ASOCCode', 'ObserverNumber','DeploymentNumber'], 
                    as_index=False)['SetNumber'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
            Quota_FailConsistency_Summary.rename(columns={'Quota':'Quota',
                                                          'ASOCCode':'ASOCCode',
                                                          'ObserverNumber':'ObserverNumber',
                                                          'DeploymentNumber':'DeploymentNumber',
                                                          'SetNumber':'NumOfSetsPerDeploymentNumber'
                                                        },inplace = True)
            Quota_FailConsistency_Summary  = Quota_FailConsistency_Summary.reset_index(drop=True)
            Quota_FailConsistency_Summary  = pd.DataFrame(Quota_FailConsistency_Summary)
            FailCount_Quota_Consistency = Quota_FailConsistency_Summary.drop_duplicates(
                                        subset=['ASOCCode', 'ObserverNumber','DeploymentNumber'], keep="first")
            Len_FailCount_Quota_Consistency = len(FailCount_Quota_Consistency)
        else:
            Len_FailCount_Quota_Consistency = 0
        
        ### Building Summary DF
        ListYCQ_FailedConsistency = ['FailCount_Year_Consistency',
                                     'FailCount_Country_Consistency',
                                     'FailCount_Quota_Consistency']
        NumYCQ_FailedConsistency = [Len_FailCount_Year_Consistency,
                                    Len_FailCount_Country_Consistency,
                                    Len_FailCount_Quota_Consistency]
        Append_List_NumbFailConsiste = {'VariableName': ListYCQ_FailedConsistency, 
                                        'QCFailCount': NumYCQ_FailedConsistency} 
        YCQ_FailedConsistencySummaryDF = pd.DataFrame(Append_List_NumbFailConsiste)
        YCQ_FailedConsistencySummaryDF[['QCFailCount']] = YCQ_FailedConsistencySummaryDF[['QCFailCount']].astype(int)
        YCQ_FailedConsistencySummaryDF.sort_values(by=['QCFailCount'], inplace=True, ascending=False)
        YCQ_FailedConsistencySummaryDF  = YCQ_FailedConsistencySummaryDF.reset_index(drop=True)
        YCQ_FailedConsistencySummaryDF  = pd.DataFrame(YCQ_FailedConsistencySummaryDF)
       
        Length_YCQ_FailedConsistency = (int(Len_FailCount_Year_Consistency)+\
                                        int(Len_FailCount_Country_Consistency)+\
                                        int(Len_FailCount_Quota_Consistency))
        # Submit Year_FailConsistency_DF Catch DB Storage
        Submit_Year_Cntry_Quota_FailConsistency(Year_FailConsistency_DF,
                                                Country_FailConsistency_DF,
                                                Quota_FailConsistency_DF,
                                                YCQ_FailedConsistencySummaryDF)        
        return Length_YCQ_FailedConsistency
        
    def RunConsistencyFailed_VesselVariables():
        ## Get GetSetCatchProfileDB
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,
                                        ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                        'ASOCCode','ObserverNumber','DeploymentNumber',
                                        'SetNumber', 'Year','RecordType','Country','Quota',
                                        'SubTripNumber','VesselSideNumber', 'VesselClass',
                                        'VesselLength', 'VesselHorsepower']]
                    SetCatchProfileDB_DF.sort_values(by=['ASOCCode','DeploymentNumber','SetNumber',
                                 'RecordType'], inplace=True)
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
        SetCatchProfileDB_DF = GetSetCatchProfileDB()
    
        def Submit_VessVar_FailConsistency(
            VSN_STN_FailConsistency_DF,
            VesselClass_FailConsistency_DF,
            VesselLength_FailConsistency_DF,
            VesselHorsepower_FailConsistency_DF,
            VessVar_FailedConsistencySummaryDF):
            try:
                VSN_STN_FailConsistency_DF = pd.DataFrame(VSN_STN_FailConsistency_DF)
                VesselClass_FailConsistency_DF = pd.DataFrame(VesselClass_FailConsistency_DF)
                VesselLength_FailConsistency_DF = pd.DataFrame(VesselLength_FailConsistency_DF)
                VesselHorsepower_FailConsistency_DF = pd.DataFrame(VesselHorsepower_FailConsistency_DF)
                VessVar_FailedConsistencySummaryDF = pd.DataFrame(VessVar_FailedConsistencySummaryDF)
                
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Consistency)
                cursor = sqliteConnection.cursor()
                VSN_STN_FailConsistency_DF.to_sql('SetCatch_VSN_STN_FailConsistency_DF',
                                            sqliteConnection, if_exists="replace", index =False)
                VesselClass_FailConsistency_DF.to_sql('SetCatch_VCLS_VSN_FailConsistency_DF',
                                            sqliteConnection, if_exists="replace", index =False)
                VesselLength_FailConsistency_DF.to_sql('SetCatch_VL_VSN_FailConsistency_DF',
                                            sqliteConnection, if_exists="replace", index =False)
                VesselHorsepower_FailConsistency_DF.to_sql('SetCatch_VHP_VSN_FailConsistency_DF',
                                            sqliteConnection, if_exists="replace", index =False)
                VessVar_FailedConsistencySummaryDF.to_sql('SetCatch_Vessel_FailConsis_SummaryDF',
                                            sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()

        ## QC On VesselSideNumber - SubTripNumber
        VSN_FailConsistency= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'ASOCCode','ObserverNumber','DeploymentNumber',
                            'SetNumber', 'Year','RecordType','Country','Quota',
                            'SubTripNumber','VesselSideNumber', 'VesselClass']]).replace(['','None'], 99999999)
        
        VSN_FailConsistency[['DataBase_ID','RecordIdentifier','ASOCCode','DeploymentNumber',
                            'SetNumber', 'Year','RecordType','Country','Quota','VesselClass']] = VSN_FailConsistency[
                            ['DataBase_ID','RecordIdentifier','ASOCCode','DeploymentNumber',
                            'SetNumber', 'Year','RecordType','Country','Quota','VesselClass']
                            ].astype(int)
        VSN_FailConsistency[['ObserverNumber', 'SubTripNumber','VesselSideNumber']] = VSN_FailConsistency[
                            ['ObserverNumber', 'SubTripNumber','VesselSideNumber']
                            ].astype(str)
        VSN_FailConsistency = VSN_FailConsistency[
                            ((VSN_FailConsistency.SubTripNumber) != '99999999')]
        VSN_FailConsistency = VSN_FailConsistency[
                            ((VSN_FailConsistency.VesselSideNumber) != '99999999')]
        VSN_FailConsistency  = VSN_FailConsistency.reset_index(drop=True)
        VSN_FailConsistency  = pd.DataFrame(VSN_FailConsistency)
        
        ## Finding fail in VesselSideNumber consistent in each alpha SubTripNumber.
        if len(VSN_FailConsistency) >0:
            Filter_VSN_FailConsistency1 = (VSN_FailConsistency.groupby(
                ['ASOCCode','ObserverNumber','DeploymentNumber',
                'Year','Country','Quota', 'SubTripNumber','VesselClass'], 
                as_index=False)['VesselSideNumber'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
            
            Filter_VSN_FailConsistency1 = Filter_VSN_FailConsistency1[
                                ((Filter_VSN_FailConsistency1.VesselSideNumber) > 1)]
            Filter_VSN_FailConsistency1 = Filter_VSN_FailConsistency1.loc[:,
                ['ASOCCode','ObserverNumber','DeploymentNumber','Year',
                'Country','Quota', 'SubTripNumber','VesselClass']]
            Filter_VSN_FailConsistency1 = Filter_VSN_FailConsistency1.merge(
                VSN_FailConsistency, 
                on = ['ASOCCode','ObserverNumber','DeploymentNumber',
                    'Year','Country','Quota', 'SubTripNumber','VesselClass'], indicator=True, 
                how='outer').query('_merge == "both"')
            Filter_VSN_FailConsistency1  = Filter_VSN_FailConsistency1.reset_index(drop=True)
            Filter_VSN_FailConsistency1= (Filter_VSN_FailConsistency1.loc[:,
                ['DataBase_ID','RecordIdentifier','DeploymentUID',
                'ASOCCode','ObserverNumber','DeploymentNumber',
                'SetNumber', 'Year','RecordType','Country','Quota',
                'SubTripNumber','VesselSideNumber', 'VesselClass']])
            Filter_VSN_FailConsistency1 = Filter_VSN_FailConsistency1.replace([99999999, 99999999.0, '.'], '')
            Filter_VSN_FailConsistency1 = Filter_VSN_FailConsistency1.replace(['99999999', '.'], 'None')
            Filter_VSN_FailConsistency1  = Filter_VSN_FailConsistency1.reset_index(drop=True)
            Filter_VSN_FailConsistency1['QC_Message'] ="VesselSideNumber (VSN) Must Be Consistent With SubTripNumber (STN)"
            Filter_VSN_FailConsistency1['QC_CaseType'] ="Case : VSN-STN Consistency"
            VSN_FailConsistency_DF  = pd.DataFrame(Filter_VSN_FailConsistency1)
        else:
            VSN_FailConsistency['QC_Message'] = None
            VSN_FailConsistency['QC_CaseType'] = None
            VSN_FailConsistency_DF  = pd.DataFrame(VSN_FailConsistency)

        ## QC On SubTripNumber 
        STN_FailConsistency= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'ASOCCode','ObserverNumber','DeploymentNumber',
                            'SetNumber', 'Year','RecordType','Country','Quota',
                            'SubTripNumber','VesselSideNumber', 'VesselClass']]).replace(['','None'], 99999999)
        
        STN_FailConsistency[['DataBase_ID','RecordIdentifier','ASOCCode','DeploymentNumber',
                            'SetNumber', 'Year','RecordType','Country','Quota','VesselClass']] = STN_FailConsistency[
                           ['DataBase_ID','RecordIdentifier','ASOCCode','DeploymentNumber',
                            'SetNumber', 'Year','RecordType','Country','Quota','VesselClass']
                            ].astype(int)
        STN_FailConsistency[['ObserverNumber', 'SubTripNumber','VesselSideNumber']] = STN_FailConsistency[
                            ['ObserverNumber', 'SubTripNumber','VesselSideNumber']
                            ].astype(str)
        STN_FailConsistency = STN_FailConsistency[
                            ((STN_FailConsistency.SubTripNumber) != '99999999')]
        STN_FailConsistency = STN_FailConsistency[
                            ((STN_FailConsistency.VesselSideNumber) != '99999999')]
        STN_FailConsistency  = STN_FailConsistency.reset_index(drop=True)
        STN_FailConsistency  = pd.DataFrame(STN_FailConsistency)
        
        ## Finding fail When SubTripNumber alpha designation changes With VesselsideNumber changes
        if len(STN_FailConsistency) >0:
            STN_FailConsistency["VessSideNum_Changed"] = STN_FailConsistency["VesselSideNumber"].shift(1, 
                fill_value=STN_FailConsistency.iloc[0]["VesselSideNumber"]) != STN_FailConsistency["VesselSideNumber"]
            STN_FailConsistency["SubTripNum_Changed"] = STN_FailConsistency["SubTripNumber"].shift(1, 
                fill_value=STN_FailConsistency.iloc[0]["SubTripNumber"]) != STN_FailConsistency["SubTripNumber"]
            STN_FailConsistency["DepNum_Changed"] = STN_FailConsistency["DeploymentNumber"].shift(1, 
                fill_value=STN_FailConsistency.iloc[0]["DeploymentNumber"]) != STN_FailConsistency["DeploymentNumber"]
            STN_FailConsistency["ObsvNum_Changed"] = STN_FailConsistency["ObserverNumber"].shift(1, 
                fill_value=STN_FailConsistency.iloc[0]["ObserverNumber"]) != STN_FailConsistency["ObserverNumber"]
            STN_FailConsistency["ASOC_Changed"] = STN_FailConsistency["ASOCCode"].shift(1, 
                fill_value=STN_FailConsistency.iloc[0]["ASOCCode"]) != STN_FailConsistency["ASOCCode"]
            STN_FailConsistency["Year_Changed"] = STN_FailConsistency["Year"].shift(1, 
                fill_value=STN_FailConsistency.iloc[0]["Year"]) != STN_FailConsistency["Year"]
            STN_FailConsistency["Country_Changed"] = STN_FailConsistency["Country"].shift(1, 
                fill_value=STN_FailConsistency.iloc[0]["Country"]) != STN_FailConsistency["Country"]
            STN_FailConsistency["Quota_Changed"] = STN_FailConsistency["Quota"].shift(1, 
                fill_value=STN_FailConsistency.iloc[0]["Quota"]) != STN_FailConsistency["Quota"]
            STN_FailConsistency["VesselClass_Changed"] = STN_FailConsistency["VesselClass"].shift(1, 
                fill_value=STN_FailConsistency.iloc[0]["VesselClass"]) != STN_FailConsistency["VesselClass"]
            
            Filter_STN_FailConsistency1 = STN_FailConsistency[
                                        (STN_FailConsistency.VessSideNum_Changed == True)&
                                        (STN_FailConsistency.SubTripNum_Changed == False)&
                                        (STN_FailConsistency.DepNum_Changed == False)&
                                        (STN_FailConsistency.ObsvNum_Changed == False)&
                                        (STN_FailConsistency.ASOC_Changed == False)&
                                        (STN_FailConsistency.Year_Changed == False)&
                                        (STN_FailConsistency.Country_Changed == False)&
                                        (STN_FailConsistency.Quota_Changed == False)&
                                        (STN_FailConsistency.VesselClass_Changed == False)
                                        ]
            Filter_STN_FailConsistency1 = Filter_STN_FailConsistency1.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                'ASOCCode','ObserverNumber','DeploymentNumber',
                                'SetNumber', 'Year','RecordType','Country','Quota',
                                'SubTripNumber','VesselSideNumber', 'VesselClass']]
            Filter_STN_FailConsistency1 = Filter_STN_FailConsistency1.loc[:,
                ['ASOCCode','ObserverNumber','DeploymentNumber','Year',
                'Country','Quota', 'SubTripNumber', 'VesselClass']]
            Filter_STN_FailConsistency1 = Filter_STN_FailConsistency1.merge(
                STN_FailConsistency, 
                on = ['ASOCCode','ObserverNumber','DeploymentNumber','Year',
                    'Country','Quota', 'SubTripNumber', 'VesselClass'], indicator=True, 
                how='outer').query('_merge == "both"')
            Filter_STN_FailConsistency1  = Filter_STN_FailConsistency1.reset_index(drop=True)
            Filter_STN_FailConsistency1 = Filter_STN_FailConsistency1.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                'ASOCCode','ObserverNumber','DeploymentNumber',
                                'SetNumber', 'Year','RecordType','Country','Quota',
                                'SubTripNumber','VesselSideNumber', 'VesselClass']]
            Filter_STN_FailConsistency1 = Filter_STN_FailConsistency1.replace([99999999, 99999999.0, '.'], '')
            Filter_STN_FailConsistency1 = Filter_STN_FailConsistency1.replace(['99999999', '.'], 'None')
            Filter_STN_FailConsistency1  = Filter_STN_FailConsistency1.reset_index(drop=True)
            Filter_STN_FailConsistency1['QC_Message'] ="VesselSideNumber (VSN) Must Be Consistent With SubTripNumber (STN)"
            Filter_VSN_FailConsistency1['QC_CaseType'] ="Case : VSN-STN Consistency"
            STN_FailConsistency_DF  = pd.DataFrame(Filter_STN_FailConsistency1)
        else:
            STN_FailConsistency['QC_Message'] = None
            STN_FailConsistency['QC_CaseType'] = None
            STN_FailConsistency_DF  = pd.DataFrame(STN_FailConsistency)
        
        ## Combining VSN_FailConsistency_DF & STN_FailConsistency_DF
        VSN_STN_FailConsistency_DF = pd.concat([VSN_FailConsistency_DF, STN_FailConsistency_DF])
        VSN_STN_FailConsistency_DF = VSN_STN_FailConsistency_DF.drop_duplicates(
                                        subset=['DataBase_ID','RecordIdentifier','DeploymentUID'], keep="first")
        VSN_STN_FailConsistency_DF  = VSN_STN_FailConsistency_DF.reset_index(drop=True)
        VSN_STN_FailConsistency_DF  = pd.DataFrame(VSN_STN_FailConsistency_DF)
        
        ## Building VSN_STN_FailConsistency_DF Summary And Count
        if len(VSN_STN_FailConsistency_DF)>0:
            VSN_STN_Summary = (VSN_STN_FailConsistency_DF.groupby(
                ['ASOCCode','ObserverNumber','DeploymentNumber','Year','Country','Quota', 'VesselClass'],
                as_index=False)['SubTripNumber'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
            VSN_STN_Summary.rename(columns={'ASOCCode':'ASOCCode',
                                        'ObserverNumber':'ObserverNumber',
                                        'DeploymentNumber':'DeploymentNumber',
                                        'Year':'Year',
                                        'Country':'Country',
                                        'Quota':'Quota',
                                        'VesselClass': 'VesselClass',
                                        'SubTripNumber':'QCFailCount'
                                        },inplace = True)
            VSN_STN_Summary  = VSN_STN_Summary.reset_index(drop=True)
            VSN_STN_Summary  = pd.DataFrame(VSN_STN_Summary)
            Len_FailCount_VSN_STN = sum(VSN_STN_Summary['QCFailCount']) 
        else:
            Len_FailCount_VSN_STN = 0
        
        ## QC On VesselClass - VesselSideNumber 
        VesselClass_FailConsistency= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'ASOCCode','ObserverNumber','DeploymentNumber',
                            'SetNumber', 'Year','RecordType','Country','Quota',
                            'VesselClass','VesselSideNumber']]).replace(['','None'], 99999999)
        
        VesselClass_FailConsistency[['DataBase_ID','RecordIdentifier','ASOCCode','DeploymentNumber',
                            'SetNumber', 'Year','RecordType', 'Country','Quota', 'VesselClass']] = VesselClass_FailConsistency[
                            ['DataBase_ID','RecordIdentifier','ASOCCode','DeploymentNumber',
                            'SetNumber', 'Year','RecordType', 'Country','Quota', 'VesselClass']
                            ].astype(int)
        VesselClass_FailConsistency[['ObserverNumber','VesselSideNumber']] = VesselClass_FailConsistency[
                            ['ObserverNumber', 'VesselSideNumber']
                            ].astype(str)
        VesselClass_FailConsistency = VesselClass_FailConsistency[
                            ((VesselClass_FailConsistency.VesselClass) != 99999999)]
        VesselClass_FailConsistency = VesselClass_FailConsistency[
                            ((VesselClass_FailConsistency.VesselSideNumber) != '99999999')]
        VesselClass_FailConsistency  = VesselClass_FailConsistency.reset_index(drop=True)
        VesselClass_FailConsistency  = pd.DataFrame(VesselClass_FailConsistency)
        
        ## Finding fail in VesselClass consistent in each alpha VesselSideNumber.
        if len(VesselClass_FailConsistency) >0:
            Filter_VesselClass_FailConsistency = (VesselClass_FailConsistency.groupby([
                'ASOCCode','ObserverNumber','DeploymentNumber','Year','Country','Quota', 'VesselSideNumber'], 
                as_index=False)['VesselClass'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
            Filter_VesselClass_FailConsistency = Filter_VesselClass_FailConsistency[
                                ((Filter_VesselClass_FailConsistency.VesselClass) > 1)]
           
            Filter_VesselClass_FailConsistency = Filter_VesselClass_FailConsistency.loc[:,
                                    ['ASOCCode', 'ObserverNumber','DeploymentNumber','Year','Country','Quota', 'VesselSideNumber']]
            Filter_VesselClass_FailConsistency = Filter_VesselClass_FailConsistency.merge(
                            VesselClass_FailConsistency, 
                            on = ['ASOCCode', 'ObserverNumber','DeploymentNumber','Year', 'Country','Quota', 'VesselSideNumber'], indicator=True, 
                            how='outer').query('_merge == "both"')
            Filter_VesselClass_FailConsistency  = Filter_VesselClass_FailConsistency.reset_index(drop=True)
            Filter_VesselClass_FailConsistency= (Filter_VesselClass_FailConsistency.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                'ASOCCode','ObserverNumber','DeploymentNumber',
                                'SetNumber', 'Year', 'RecordType','Country','Quota',
                                'VesselClass','VesselSideNumber']])
            Filter_VesselClass_FailConsistency = Filter_VesselClass_FailConsistency.replace([99999999, 99999999.0, '.'], '')
            Filter_VesselClass_FailConsistency = Filter_VesselClass_FailConsistency.replace(['99999999', '.'], 'None')
            Filter_VesselClass_FailConsistency  = Filter_VesselClass_FailConsistency.reset_index(drop=True)
            Filter_VesselClass_FailConsistency['QC_Message'] ="VesselClass (VCLS) Must Be Consistent With  VSN"
            Filter_VesselClass_FailConsistency['QC_CaseType'] ="Case : VCLS-VSN Consistency"
            VesselClass_FailConsistency_DF  = pd.DataFrame(Filter_VesselClass_FailConsistency)
        else:
            VesselClass_FailConsistency['QC_Message'] = None
            Filter_VesselClass_FailConsistency['QC_CaseType'] =None
            VesselClass_FailConsistency_DF  = pd.DataFrame(VesselClass_FailConsistency)

        ## Building VesselClass_FailConsistency_DF Summary And Count
        if len(VesselClass_FailConsistency_DF)>0:
            VesselClassSummary = (VesselClass_FailConsistency_DF.groupby(
                ['ASOCCode','ObserverNumber','DeploymentNumber','Year'],
                as_index=False)['VesselSideNumber'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
            VesselClassSummary.rename(columns={'ASOCCode':'ASOCCode',
                                        'ObserverNumber':'ObserverNumber',
                                        'DeploymentNumber':'DeploymentNumber',
                                        'Year':'Year',
                                        'VesselSideNumber':'QCFailCount'
                                        },inplace = True)
            VesselClassSummary  = VesselClassSummary.reset_index(drop=True)
            VesselClassSummary  = pd.DataFrame(VesselClassSummary)
            Len_FailCount_VesselClass= sum(VesselClassSummary['QCFailCount']) 
        else:
            Len_FailCount_VesselClass= 0
        
        ## QC On VesselLength - VesselSideNumber 
        VesselLength_FailConsistency= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'ASOCCode','ObserverNumber','DeploymentNumber',
                            'SetNumber', 'Year','RecordType','Country','Quota',
                            'VesselLength','VesselSideNumber']]).replace(['', None, np.nan, 
                            'None', ' ', '  ', '   ', '    '], 99999999)
        
        VesselLength_FailConsistency[['DataBase_ID','RecordIdentifier','ASOCCode','DeploymentNumber',
                            'SetNumber', 'Year','RecordType', 'Country','Quota']] = VesselLength_FailConsistency[
                            ['DataBase_ID','RecordIdentifier','ASOCCode','DeploymentNumber',
                            'SetNumber', 'Year','RecordType', 'Country','Quota']
                            ].astype(int)
        
        VesselLength_FailConsistency[['VesselLength']] = VesselLength_FailConsistency[
                            ['VesselLength']
                            ].astype(float)
        
        VesselLength_FailConsistency[['ObserverNumber','VesselSideNumber']] = VesselLength_FailConsistency[
                            ['ObserverNumber', 'VesselSideNumber']
                            ].astype(str)
        
        VesselLength_FailConsistency = VesselLength_FailConsistency[
                            ((VesselLength_FailConsistency.VesselLength) != 99999999.0)]
        VesselLength_FailConsistency = VesselLength_FailConsistency[
                            ((VesselLength_FailConsistency.VesselSideNumber) != '99999999')]
        VesselLength_FailConsistency  = VesselLength_FailConsistency.reset_index(drop=True)
        VesselLength_FailConsistency  = pd.DataFrame(VesselLength_FailConsistency)
        
        ## Finding fail in VesselLength consistent in each alpha VesselSideNumber.
        if len(VesselLength_FailConsistency) >0:
            Filter_VesselLength_FailConsistency = (VesselLength_FailConsistency.groupby([
                'ASOCCode','ObserverNumber','DeploymentNumber','Year','Country','Quota','VesselSideNumber'], 
                as_index=False)['VesselLength'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
            Filter_VesselLength_FailConsistency = Filter_VesselLength_FailConsistency[
                                ((Filter_VesselLength_FailConsistency.VesselLength) > 1)]
            
            Filter_VesselLength_FailConsistency = Filter_VesselLength_FailConsistency.loc[:,
                ['ASOCCode', 'ObserverNumber','DeploymentNumber','Year','Country','Quota', 'VesselSideNumber']]
            Filter_VesselLength_FailConsistency = Filter_VesselLength_FailConsistency.merge(
                    VesselLength_FailConsistency, 
                    on = ['ASOCCode', 'ObserverNumber','DeploymentNumber','Year','Country','Quota','VesselSideNumber'], indicator=True, 
                    how='outer').query('_merge == "both"')
            Filter_VesselLength_FailConsistency  = Filter_VesselLength_FailConsistency.reset_index(drop=True)
            Filter_VesselLength_FailConsistency= (Filter_VesselLength_FailConsistency.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                'ASOCCode','ObserverNumber','DeploymentNumber',
                                'SetNumber', 'Year', 'RecordType','Country','Quota',
                                'VesselLength','VesselSideNumber']])
            Filter_VesselLength_FailConsistency = Filter_VesselLength_FailConsistency.replace([99999999, 99999999.0, '.'], '')
            Filter_VesselLength_FailConsistency = Filter_VesselLength_FailConsistency.replace(['99999999', '.'], 'None')
            Filter_VesselLength_FailConsistency  = Filter_VesselLength_FailConsistency.reset_index(drop=True)
            Filter_VesselLength_FailConsistency['QC_Message'] ="VesselLength (VL) Must Be Consistent With VSN"
            Filter_VesselLength_FailConsistency['QC_CaseType'] ="Case : VL-VSN Consistency"
            VesselLength_FailConsistency_DF  = pd.DataFrame(Filter_VesselLength_FailConsistency)
        else:
            VesselLength_FailConsistency['QC_Message'] = None
            VesselLength_FailConsistency['QC_CaseType'] = None
            VesselLength_FailConsistency_DF  = pd.DataFrame(VesselLength_FailConsistency)

        ## Building VesselLength_FailConsistency_DF Summary And Count
        if len(VesselLength_FailConsistency_DF)>0:
            VesselLengthSummary = (VesselLength_FailConsistency_DF.groupby(
                ['ASOCCode','ObserverNumber','DeploymentNumber','Year'],
                as_index=False)['VesselSideNumber'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
            VesselLengthSummary.rename(columns={'ASOCCode':'ASOCCode',
                                        'ObserverNumber':'ObserverNumber',
                                        'DeploymentNumber':'DeploymentNumber',
                                        'Year':'Year',
                                        'VesselSideNumber':'QCFailCount'
                                        },inplace = True)
            VesselLengthSummary  = VesselLengthSummary.reset_index(drop=True)
            VesselLengthSummary  = pd.DataFrame(VesselLengthSummary)
            Len_FailCount_VesselLength= sum(VesselLengthSummary['QCFailCount']) 
        else:
            Len_FailCount_VesselLength= 0   
        
    ## QC On VesselHorsepower - VesselSideNumber 
        VesselHorsepower_FailConsistency= (SetCatchProfileDB_DF.loc[:,
                            ['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'ASOCCode','ObserverNumber','DeploymentNumber',
                            'SetNumber', 'Year','RecordType','Country','Quota',
                            'VesselHorsepower','VesselSideNumber']]).replace(['','None'], 99999999)
        
        VesselHorsepower_FailConsistency[['DataBase_ID','RecordIdentifier','ASOCCode','DeploymentNumber',
                            'SetNumber', 'Year','RecordType', 'Country','Quota','VesselHorsepower']] = VesselHorsepower_FailConsistency[
                            ['DataBase_ID','RecordIdentifier','ASOCCode','DeploymentNumber',
                            'SetNumber', 'Year','RecordType', 'Country','Quota', 'VesselHorsepower']
                            ].astype(int)
        VesselHorsepower_FailConsistency[['ObserverNumber','VesselSideNumber']] = VesselHorsepower_FailConsistency[
                            ['ObserverNumber', 'VesselSideNumber']
                            ].astype(str)
        VesselHorsepower_FailConsistency = VesselHorsepower_FailConsistency[
                            ((VesselHorsepower_FailConsistency.VesselHorsepower) != 99999999)]
        VesselHorsepower_FailConsistency = VesselHorsepower_FailConsistency[
                            ((VesselHorsepower_FailConsistency.VesselSideNumber) != '99999999')]
        VesselHorsepower_FailConsistency  = VesselHorsepower_FailConsistency.reset_index(drop=True)
        VesselHorsepower_FailConsistency  = pd.DataFrame(VesselHorsepower_FailConsistency)
        
        ## Finding fail in VesselHorsepower consistent in each alpha VesselSideNumber.
        if len(VesselHorsepower_FailConsistency) >0:
            Filter_VesselHorsepower_FailConsistency = (VesselHorsepower_FailConsistency.groupby([
                        'ASOCCode','ObserverNumber','DeploymentNumber','Year','Country','Quota','VesselSideNumber'], 
                        as_index=False)['VesselHorsepower'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
            Filter_VesselHorsepower_FailConsistency = Filter_VesselHorsepower_FailConsistency[
                                ((Filter_VesselHorsepower_FailConsistency.VesselHorsepower) > 1)]
            
            Filter_VesselHorsepower_FailConsistency = Filter_VesselHorsepower_FailConsistency.loc[:,
                                    ['ASOCCode', 'ObserverNumber','DeploymentNumber','Year','Country','Quota','VesselSideNumber']]
            Filter_VesselHorsepower_FailConsistency = Filter_VesselHorsepower_FailConsistency.merge(
                            VesselHorsepower_FailConsistency, 
                            on = ['ASOCCode', 'ObserverNumber','DeploymentNumber','Year','Country','Quota','VesselSideNumber'], indicator=True, 
                            how='outer').query('_merge == "both"')
            Filter_VesselHorsepower_FailConsistency  = Filter_VesselHorsepower_FailConsistency.reset_index(drop=True)
            Filter_VesselHorsepower_FailConsistency= (Filter_VesselHorsepower_FailConsistency.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                'ASOCCode','ObserverNumber','DeploymentNumber',
                                'SetNumber', 'Year', 'RecordType','Country','Quota',
                                'VesselHorsepower','VesselSideNumber']])
            Filter_VesselHorsepower_FailConsistency = Filter_VesselHorsepower_FailConsistency.replace([99999999, 99999999.0, '.'], '')
            Filter_VesselHorsepower_FailConsistency = Filter_VesselHorsepower_FailConsistency.replace(['99999999', '.'], 'None')
            Filter_VesselHorsepower_FailConsistency  = Filter_VesselHorsepower_FailConsistency.reset_index(drop=True)
            Filter_VesselHorsepower_FailConsistency['QC_Message'] ="VesselHorsepower (VHP) Must Be Consistent With VSN"
            Filter_VesselHorsepower_FailConsistency['QC_CaseType'] ="Case : VHP-VSN Consistency"
            VesselHorsepower_FailConsistency_DF  = pd.DataFrame(Filter_VesselHorsepower_FailConsistency)
        else:
            VesselHorsepower_FailConsistency['QC_Message'] = None
            VesselHorsepower_FailConsistency['QC_CaseType'] = None
            VesselHorsepower_FailConsistency_DF  = pd.DataFrame(VesselHorsepower_FailConsistency)
        
        ## Building VesselHorsepower_FailConsistency_DF Summary And Count
        if len(VesselHorsepower_FailConsistency_DF)>0:
            VesselHorsepowerSummary = (VesselHorsepower_FailConsistency_DF.groupby(
                ['ASOCCode','ObserverNumber','DeploymentNumber','Year'],
                as_index=False)['VesselSideNumber'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
            VesselHorsepowerSummary.rename(columns={'ASOCCode':'ASOCCode',
                                        'ObserverNumber':'ObserverNumber',
                                        'DeploymentNumber':'DeploymentNumber',
                                        'Year':'Year',
                                        'VesselSideNumber':'QCFailCount'
                                        },inplace = True)
            VesselHorsepowerSummary  = VesselHorsepowerSummary.reset_index(drop=True)
            VesselHorsepowerSummary  = pd.DataFrame(VesselHorsepowerSummary)
            Len_FailCount_VesselHorsepower= sum(VesselHorsepowerSummary['QCFailCount']) 
        else:
            Len_FailCount_VesselHorsepower= 0   

        ### Building Summary DF
        ListVessVar_FailedConsistency = ['FailCount_VesselSideNumber_Consistency',
                                        'FailCount_VesselClass_Consistency',
                                        'FailCount_VesselLength_Consistency',
                                        'FailCount_VesselHorsepower_Consistency']
        NumVessVar_FailedConsistency = [Len_FailCount_VSN_STN,
                                        Len_FailCount_VesselClass,
                                        Len_FailCount_VesselLength,
                                        Len_FailCount_VesselHorsepower]
        Append_List_NumbFailConsiste = {'VariableName': ListVessVar_FailedConsistency, 
                                        'QCFailCount': NumVessVar_FailedConsistency} 
        VessVar_FailedConsistencySummaryDF = pd.DataFrame(Append_List_NumbFailConsiste)
        VessVar_FailedConsistencySummaryDF[['QCFailCount']] = VessVar_FailedConsistencySummaryDF[['QCFailCount']].astype(int)
        VessVar_FailedConsistencySummaryDF.sort_values(by=['QCFailCount'], inplace=True, ascending=False)
        VessVar_FailedConsistencySummaryDF  = VessVar_FailedConsistencySummaryDF.reset_index(drop=True)
        VessVar_FailedConsistencySummaryDF  = pd.DataFrame(VessVar_FailedConsistencySummaryDF)
        
        Length_VessVar_FailedConsistency = (int(Len_FailCount_VSN_STN)+\
                                            int(Len_FailCount_VesselClass)+\
                                            int(Len_FailCount_VesselLength)+\
                                            int(Len_FailCount_VesselHorsepower))
        # Submit Year_FailConsistency_DF Catch DB Storage
        Submit_VessVar_FailConsistency(VSN_STN_FailConsistency_DF,
                                        VesselClass_FailConsistency_DF,
                                        VesselLength_FailConsistency_DF,
                                        VesselHorsepower_FailConsistency_DF,
                                        VessVar_FailedConsistencySummaryDF)        
        return Length_VessVar_FailedConsistency
        
    def RunConsistencyFailed_CalenderVariables():
        ## Calender Variables Limit Fetching
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
        Get_RangeLimitVariables = fetchData_RangeLimitVariables()
        # Year
        Year_LowerRangeLimitValue=int(Get_RangeLimitVariables.at[0,'LowerRangeLimitValue'])
        Year_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[0,'UpperRangeLimitValue'])
        Year_QCNullValue= Get_RangeLimitVariables.at[0,'QCNullValue']
        #Day
        Day_LowerRangeLimitValue=int(Get_RangeLimitVariables.at[3,'LowerRangeLimitValue'])
        Day_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[3,'UpperRangeLimitValue'])
        Day_QCNullValue= Get_RangeLimitVariables.at[1,'QCNullValue']
        #Month
        Month_LowerRangeLimitValue=int(Get_RangeLimitVariables.at[1,'LowerRangeLimitValue'])
        Month_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[1,'UpperRangeLimitValue'])
        Month_QCNullValue= Get_RangeLimitVariables.at[2,'QCNullValue']
        # HaulDay
        HaulDay_LowerRangeLimitValue=int(Get_RangeLimitVariables.at[4,'LowerRangeLimitValue'])
        HaulDay_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[4,'UpperRangeLimitValue'])
        HaulDay_QCNullValue= Get_RangeLimitVariables.at[3,'QCNullValue']
        # HaulMonth
        HaulMonth_LowerRangeLimitValue=int(Get_RangeLimitVariables.at[2,'LowerRangeLimitValue'])
        HaulMonth_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[2,'UpperRangeLimitValue'])
        HaulMonth_QCNullValue= Get_RangeLimitVariables.at[4,'QCNullValue']

        ## Get GetSetCatchProfileDB
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,
                                        ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                        'ASOCCode','ObserverNumber','DeploymentNumber','SetNumber' ,'RecordType',
                                        'Year','Day','Month', 'HaulDay','HaulMonth','StartTime','Duration']]
                    SetCatchProfileDB_DF.sort_values(by=['ASOCCode','DeploymentNumber','SetNumber',
                                 'RecordType'], inplace=True)
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
        
        ## Submit QC to DB
        def Submit_Calender_FailConsistency(Calender_DM_HDHM_FailConsistency,
                                            Calender_FailedConsistencySummaryDF):
            try:
                Calender_DM_HDHM_FailConsistency = pd.DataFrame(Calender_DM_HDHM_FailConsistency)
                Calender_FailedConsistencySummaryDF = pd.DataFrame(Calender_FailedConsistencySummaryDF)
                
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Consistency)
                cursor = sqliteConnection.cursor()
                Calender_DM_HDHM_FailConsistency.to_sql('SetCatch_DM_HDHM_FailConsistency_DF',
                                            sqliteConnection, if_exists="replace", index =False)
                Calender_FailedConsistencySummaryDF.to_sql('SetCatch_Calender_FailConsis_SummaryDF',
                                            sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()
    
        SetCatchProfileDB_DF = GetSetCatchProfileDB()
        
        calenderVarColumns =['DataBase_ID','RecordIdentifier','DeploymentUID',
                            'ASOCCode','ObserverNumber','DeploymentNumber', 
                            'SetNumber', 'RecordType',
                            'Year','Day','Month', 
                            'HaulDay','HaulMonth',
                            'StartTime', 'Duration',
                            'QC_Message']
        empty_Calender_DM_HDHM = pd.DataFrame({col: [] for col in calenderVarColumns})
        ## QC On Calender_DM_HDHM
        Calender_DM_HDHM_FailConsistency= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier',
                                'DeploymentUID','ASOCCode','ObserverNumber',
                                'DeploymentNumber','SetNumber' ,'RecordType',
                                'Year','Day','Month', 
                                'HaulDay','HaulMonth',
                                'StartTime','Duration']]).replace(['','None'], 99999999)
            
        Calender_DM_HDHM_FailConsistency[['DataBase_ID','RecordIdentifier',
                                'ASOCCode','DeploymentNumber', 'SetNumber',
                                'RecordType','Year','Day',
                                'Month', 'HaulDay','HaulMonth', 'StartTime']] = Calender_DM_HDHM_FailConsistency[
                                ['DataBase_ID','RecordIdentifier',
                                'ASOCCode','DeploymentNumber','SetNumber', 
                                'RecordType','Year','Day',
                                'Month', 'HaulDay','HaulMonth', 'StartTime']
                                ].astype(int)
        Calender_DM_HDHM_FailConsistency[['ObserverNumber']] = Calender_DM_HDHM_FailConsistency[
                                ['ObserverNumber']
                                ].astype(str)
        Calender_DM_HDHM_FailConsistency[['Duration']] = Calender_DM_HDHM_FailConsistency[
                                ['Duration']
                                ].astype(float)
        
        Calender_DM_HDHM_FailConsistency = Calender_DM_HDHM_FailConsistency[
                        ((Calender_DM_HDHM_FailConsistency.Year) != 99999999)&\
                        ((Calender_DM_HDHM_FailConsistency.Day) != 99999999)&\
                        ((Calender_DM_HDHM_FailConsistency.Month) != 99999999)&\
                        ((Calender_DM_HDHM_FailConsistency.HaulDay) != 99999999)&\
                        ((Calender_DM_HDHM_FailConsistency.HaulMonth) != 99999999)&\
                        ((Calender_DM_HDHM_FailConsistency.StartTime) != 99999999)&\
                        ((Calender_DM_HDHM_FailConsistency.Duration) != 99999999.0)]
        Calender_DM_HDHM_FailConsistency  = Calender_DM_HDHM_FailConsistency.reset_index(drop=True)
        Calender_DM_HDHM_FailConsistency  = pd.DataFrame(Calender_DM_HDHM_FailConsistency)
        
        Calender_Consistency = Calender_DM_HDHM_FailConsistency[
                    ((Calender_DM_HDHM_FailConsistency.Year) >=Year_LowerRangeLimitValue)&\
                    ((Calender_DM_HDHM_FailConsistency.Day) >= Day_LowerRangeLimitValue)&\
                    ((Calender_DM_HDHM_FailConsistency.Month) >= Month_LowerRangeLimitValue)&\
                    ((Calender_DM_HDHM_FailConsistency.HaulDay) >= HaulDay_LowerRangeLimitValue)&\
                    ((Calender_DM_HDHM_FailConsistency.HaulMonth) >= HaulMonth_LowerRangeLimitValue)\
                    ]
        Calender_Consistency  = Calender_Consistency.reset_index(drop=True)
        Calender_Consistency  = pd.DataFrame(Calender_Consistency)
        
        Calender_Consistency = Calender_Consistency[
                    ((Calender_Consistency.Year) <= Year_UpperRangeLimitValue)&\
                    ((Calender_Consistency.Day) <= Day_UpperRangeLimitValue)&\
                    ((Calender_Consistency.Month) <= Month_UpperRangeLimitValue)&\
                    ((Calender_Consistency.HaulDay) <= HaulDay_UpperRangeLimitValue)&\
                    ((Calender_Consistency.HaulMonth) <= HaulMonth_UpperRangeLimitValue)
                    ]
        Calender_Consistency  = Calender_Consistency.reset_index(drop=True)
        Calender_DM_HDHM_FailConsistency  = pd.DataFrame(Calender_Consistency)

        if len(Calender_DM_HDHM_FailConsistency)>0:
        
            Calender_DM_HDHM_FailConsistency['DeploymentDate'] = pd.to_datetime(Calender_DM_HDHM_FailConsistency.Year.astype(str)+ \
                                                            ' '+\
                                                            Calender_DM_HDHM_FailConsistency.Month.astype(str)+ \
                                                            ' '+\
                                                            Calender_DM_HDHM_FailConsistency.Day.astype(str))
            
            Calender_DM_HDHM_FailConsistency['HaulDate'] = pd.to_datetime(Calender_DM_HDHM_FailConsistency.Year.astype(str)+ \
                                                            ' '+\
                                                            Calender_DM_HDHM_FailConsistency.HaulMonth.astype(str)+ \
                                                            ' '+\
                                                            Calender_DM_HDHM_FailConsistency.HaulDay.astype(str))   
            
            Calender_DM_HDHM_FailConsistency['Day_Offset1'] = ((Calender_DM_HDHM_FailConsistency.HaulDate) - \
                                                            (Calender_DM_HDHM_FailConsistency.DeploymentDate))/ np.timedelta64(1, 'D')
            
            Calender_DM_HDHM_FailConsistency = Calender_DM_HDHM_FailConsistency[
                            ((Calender_DM_HDHM_FailConsistency.Day_Offset1) < 0)]
            Calender_DM_HDHM_FailConsistency= (Calender_DM_HDHM_FailConsistency.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                'ASOCCode','ObserverNumber','DeploymentNumber', 'SetNumber', 'RecordType',
                                'Year','Day','Month', 'HaulDay','HaulMonth','StartTime','Duration', 'DeploymentDate']])
            Calender_DM_HDHM_FailConsistency  = Calender_DM_HDHM_FailConsistency.reset_index(drop=True)
            Calender_DM_HDHM_FailConsistency  = pd.DataFrame(Calender_DM_HDHM_FailConsistency)
           
            ## Start Special case For Next year roll
            if len(Calender_DM_HDHM_FailConsistency)>0:
                Calender_DM_HDHM_FailConsistency['Hauldate_Temp1'] =  [str(num).zfill(4) for num in Calender_DM_HDHM_FailConsistency['StartTime']]
                Calender_DM_HDHM_FailConsistency['StartHour'] = (Calender_DM_HDHM_FailConsistency['Hauldate_Temp1'].str[0:2]).astype(int)
                Calender_DM_HDHM_FailConsistency['StartMin'] = (Calender_DM_HDHM_FailConsistency['Hauldate_Temp1'].str[2:4]).astype(int)
                Calender_DM_HDHM_FailConsistency.drop('Hauldate_Temp1', axis=1, inplace=True)
                Calender_DM_HDHM_FailConsistency['Hauldate_Temp2'] = pd.to_datetime((Calender_DM_HDHM_FailConsistency.Year.astype(str)+ \
                                        ' '+\
                                        Calender_DM_HDHM_FailConsistency.Month.astype(str)+ \
                                        ' '+\
                                        Calender_DM_HDHM_FailConsistency.Day.astype(str)
                                        ))
                Calender_DM_HDHM_FailConsistency['HaulDate_CreatedNewTemp']=Calender_DM_HDHM_FailConsistency.apply(
                            lambda g: g.Hauldate_Temp2 + pd.DateOffset(hours=(g.StartHour + g.Duration), 
                            minutes = (g.StartMin)),axis=1)
                
                Calender_DM_HDHM_FailConsistency['HaulDate_CreatedNewTemp'] = pd.to_datetime(
                    Calender_DM_HDHM_FailConsistency['HaulDate_CreatedNewTemp'],format='%Y-%m-%d')
                
                Calender_DM_HDHM_FailConsistency['HaulYear'] = (Calender_DM_HDHM_FailConsistency['HaulDate_CreatedNewTemp'].dt.strftime('%Y')).astype(int)
                
                Calender_DM_HDHM_FailConsistency['HaulDate_CreatedNew'] = pd.to_datetime((Calender_DM_HDHM_FailConsistency.HaulYear.astype(str)+ \
                                        ' '+\
                                        Calender_DM_HDHM_FailConsistency.HaulMonth.astype(str)+ \
                                        ' '+\
                                        Calender_DM_HDHM_FailConsistency.HaulDay.astype(str)
                                        ))
                
                Calender_DM_HDHM_FailConsistency['Day_Offset2'] = ((Calender_DM_HDHM_FailConsistency.HaulDate_CreatedNew) - \
                                                                (Calender_DM_HDHM_FailConsistency.DeploymentDate))/ np.timedelta64(1, 'D')
                Calender_DM_HDHM_FailConsistency = Calender_DM_HDHM_FailConsistency[
                                ((Calender_DM_HDHM_FailConsistency.Day_Offset2) <0)]
                
                Calender_DM_HDHM_FailConsistency= (Calender_DM_HDHM_FailConsistency.loc[:,
                                    ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                    'ASOCCode','ObserverNumber','DeploymentNumber', 'SetNumber', 'RecordType',
                                    'Year','Day','Month', 'HaulDay','HaulMonth','StartTime','Duration']])
                Calender_DM_HDHM_FailConsistency  = Calender_DM_HDHM_FailConsistency.reset_index(drop=True)
                Calender_DM_HDHM_FailConsistency  = pd.DataFrame(Calender_DM_HDHM_FailConsistency)
                
            Calender_DM_HDHM_FailConsistency = Calender_DM_HDHM_FailConsistency.replace([99999999, 99999999.0, '.'], '')
            Calender_DM_HDHM_FailConsistency = Calender_DM_HDHM_FailConsistency.replace(['99999999', '.'], 'None')
            Calender_DM_HDHM_FailConsistency['QC_Message'] ="Day-Month Consistency Failed"
            Calender_DM_HDHM_FailConsistency= (Calender_DM_HDHM_FailConsistency.loc[:,
                        ['DataBase_ID','RecordIdentifier','DeploymentUID',
                        'ASOCCode','ObserverNumber','DeploymentNumber', 'SetNumber', 'RecordType',
                        'Year','Day','Month', 'HaulDay','HaulMonth','StartTime','Duration','QC_Message']])
            Calender_DM_HDHM_FailConsistency  = Calender_DM_HDHM_FailConsistency.reset_index(drop=True)
            Calender_DM_HDHM_FailConsistency  = pd.DataFrame(Calender_DM_HDHM_FailConsistency)
        else:
            Calender_DM_HDHM_FailConsistency = empty_Calender_DM_HDHM
        
        ## Building Calender_DM_HDHM_FailConsistency Summary And Count
        if len(Calender_DM_HDHM_FailConsistency)>0:
            Calender_DM_HDHM_Summary = (Calender_DM_HDHM_FailConsistency.groupby(
                ['ASOCCode','ObserverNumber','DeploymentNumber','Year'],
                as_index=False)['SetNumber'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
            Calender_DM_HDHM_Summary.rename(columns={'ASOCCode':'ASOCCode',
                        'ObserverNumber':'ObserverNumber',
                        'DeploymentNumber':'DeploymentNumber',
                        'Year':'Year',
                        'SetNumber':'QCFailCount'
                        },inplace = True)
            Calender_DM_HDHM_Summary  = Calender_DM_HDHM_Summary.reset_index(drop=True)
            Calender_DM_HDHM_Summary  = pd.DataFrame(Calender_DM_HDHM_Summary)
            Len_FailCount_Cal_DM_HDHM = sum(Calender_DM_HDHM_Summary['QCFailCount']) 
        else:
            Len_FailCount_Cal_DM_HDHM = 0

        ### Building Calender Summary DF
        ListCalender_FailedConsistency = ['FailCount_Calender_Consistency']
        NumCalender_FailedConsistency = [Len_FailCount_Cal_DM_HDHM]
        Append_List_NumbFailConsiste = {'VariableName': ListCalender_FailedConsistency, 
                                        'QCFailCount': NumCalender_FailedConsistency} 
        Calender_FailedConsistencySummaryDF = pd.DataFrame(Append_List_NumbFailConsiste)
        Calender_FailedConsistencySummaryDF[['QCFailCount']] = Calender_FailedConsistencySummaryDF[['QCFailCount']].astype(int)
        Calender_FailedConsistencySummaryDF.sort_values(by=['QCFailCount'], inplace=True, ascending=False)
        Calender_FailedConsistencySummaryDF  = Calender_FailedConsistencySummaryDF.reset_index(drop=True)
        Calender_FailedConsistencySummaryDF  = pd.DataFrame(Calender_FailedConsistencySummaryDF)
        Length_Calender_FailedConsistency = (int(Len_FailCount_Cal_DM_HDHM))
        # Submit Calender_DM_HDHM_FailConsistency Catch DB Storage
        Submit_Calender_FailConsistency(Calender_DM_HDHM_FailConsistency,
                                        Calender_FailedConsistencySummaryDF)        
        return Length_Calender_FailedConsistency    
           
    def RunConsistencyFailed_MobileGear():
        ## Calender Variables Limit Fetching
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
        Get_RangeLimitVariables = fetchData_RangeLimitVariables()
        # Year
        Year_LowerRangeLimitValue=int(Get_RangeLimitVariables.at[0,'LowerRangeLimitValue'])
        Year_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[0,'UpperRangeLimitValue'])
        Year_QCNullValue= Get_RangeLimitVariables.at[0,'QCNullValue']
        #Day
        Day_LowerRangeLimitValue=int(Get_RangeLimitVariables.at[3,'LowerRangeLimitValue'])
        Day_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[3,'UpperRangeLimitValue'])
        Day_QCNullValue= Get_RangeLimitVariables.at[1,'QCNullValue']
        #Month
        Month_LowerRangeLimitValue=int(Get_RangeLimitVariables.at[1,'LowerRangeLimitValue'])
        Month_UpperRangeLimitValue= int(Get_RangeLimitVariables.at[1,'UpperRangeLimitValue'])
        Month_QCNullValue= Get_RangeLimitVariables.at[2,'QCNullValue']

        ## Get GetSetCatchProfileDB
        def GetSetCatchProfileDB():
            try:
                conn = sqlite3.connect(DB_Set_Catch_Analysis)
                cursor = conn.cursor()
                Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT;", conn)
                if len(Complete_df) >0:
                    SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                    SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,
                                        ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                        'ASOCCode','ObserverNumber','DeploymentNumber',
                                        'SetNumber' , 'VesselSideNumber', 'RecordType','GearType',
                                        'Year','Day','Month',
                                        'StartTime','Duration', 'Country']]
                    SetCatchProfileDB_DF.sort_values(by=['ASOCCode','DeploymentNumber','SetNumber',
                                 'RecordType'], inplace=True)
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
        
        ## Submit QC to DB
        def Submit_MobileGear_FailConsistency(MobileGear_FailConsistency,
                                            MobileGear_FailedConsistencySummaryDF):
            try:
                MobileGear_FailConsistency = pd.DataFrame(MobileGear_FailConsistency)
                MobileGear_FailedConsistencySummaryDF = pd.DataFrame(MobileGear_FailedConsistencySummaryDF)
                
                sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Consistency)
                cursor = sqliteConnection.cursor()
                MobileGear_FailConsistency.to_sql('SetCatch_MobileGear_FailConsistency_DF',
                                            sqliteConnection, if_exists="replace", index =False)
                MobileGear_FailedConsistencySummaryDF.to_sql('SetCatch_MobileGear_FailConsis_SummaryDF',
                                            sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()
        
        def DeleteDBStorage():
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Consistency)
            cursor = sqliteConnection.cursor()
            cursor.execute("DELETE FROM SetCatch_MobileGear_FailConsistency_DF")
            cursor.execute("DELETE FROM SetCatch_MobileGear_FailConsis_SummaryDF")
            sqliteConnection.commit()
            cursor.close()
            sqliteConnection.close()
    
        SetCatchProfileDB_DF = GetSetCatchProfileDB()
        ## QC On MobileGear
        MobileGear_FailConsistency= (SetCatchProfileDB_DF.loc[:,
                                ['DataBase_ID','RecordIdentifier','DeploymentUID',
                                'ASOCCode','ObserverNumber','DeploymentNumber',
                                'SetNumber' ,'RecordType', 'GearType',
                                'Year','Day','Month', 
                                'StartTime','Duration', 'VesselSideNumber','Country']]).replace(['','None'], 99999999)
        MobileGear_FailConsistency[['DataBase_ID','RecordIdentifier',
                                'ASOCCode','DeploymentNumber', 'SetNumber',
                                'RecordType', 'GearType', 'Year','Day',
                                'Month', 'StartTime','Country']] = MobileGear_FailConsistency[
                                ['DataBase_ID','RecordIdentifier',
                                'ASOCCode','DeploymentNumber','SetNumber', 
                                'RecordType','GearType','Year','Day',
                                'Month', 'StartTime','Country']
                                ].astype(int)
        MobileGear_FailConsistency[['ObserverNumber','VesselSideNumber']] = MobileGear_FailConsistency[
                                ['ObserverNumber', 'VesselSideNumber']
                                ].astype(str)
        MobileGear_FailConsistency[['Duration']] = MobileGear_FailConsistency[['Duration']].astype(float)
        MobileGear_FailConsistency = MobileGear_FailConsistency[
                        ((MobileGear_FailConsistency.Year) != 99999999)&\
                        ((MobileGear_FailConsistency.Day) != 99999999)&\
                        ((MobileGear_FailConsistency.Month) != 99999999)&\
                        ((MobileGear_FailConsistency.StartTime) != 99999999)&\
                        ((MobileGear_FailConsistency.GearType) != 99999999)&\
                        ((MobileGear_FailConsistency.Duration) != 99999999.0)]
        
        GearType_Mobile= [1,2,3,9,10,14,16,17,18,21,66,67,97]
        MobileGear_FailConsistency = MobileGear_FailConsistency[
                                    (MobileGear_FailConsistency['GearType'].isin(GearType_Mobile)) ]
        MobileGear_FailConsistency  = MobileGear_FailConsistency.reset_index(drop=True)
        MobileGear_FailConsistency  = pd.DataFrame(MobileGear_FailConsistency)
        if len (MobileGear_FailConsistency) > 0:
            MobileGear_Consistency = MobileGear_FailConsistency[
                        ((MobileGear_FailConsistency.Year) >=Year_LowerRangeLimitValue)&\
                        ((MobileGear_FailConsistency.Day) >= Day_LowerRangeLimitValue)&\
                        ((MobileGear_FailConsistency.Month) >= Month_LowerRangeLimitValue)]
            MobileGear_Consistency  = MobileGear_Consistency.reset_index(drop=True)
            MobileGear_Consistency  = pd.DataFrame(MobileGear_Consistency)

            MobileGear_Consistency = MobileGear_Consistency[
                        ((MobileGear_Consistency.Year) <=Year_UpperRangeLimitValue)&\
                        ((MobileGear_Consistency.Day) <= Day_UpperRangeLimitValue)&\
                        ((MobileGear_Consistency.Month) <= Month_UpperRangeLimitValue)]
            MobileGear_Consistency  = MobileGear_Consistency.reset_index(drop=True)
            MobileGear_FailConsistency  = pd.DataFrame(MobileGear_Consistency)
            
            ## MobileGear Filter & Building MobileGear-DF
            Filter_MobileGear_Rec1 = MobileGear_FailConsistency[
                            (MobileGear_FailConsistency.RecordType) == 1]
            Filter_MobileGear_Rec1 = Filter_MobileGear_Rec1.drop_duplicates(
                                subset=['DeploymentUID'], keep="first")
            Filter_MobileGear_Rec1  = Filter_MobileGear_Rec1.reset_index(drop=True)

            Filter_MobileGear_Rec1 = (Filter_MobileGear_Rec1.groupby(
                ['Year','Country','ASOCCode', 'DeploymentNumber', 
                'SetNumber', 'DeploymentUID', 'Day','Month', 'StartTime', 'Duration'], 
                as_index=False)['RecordType'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
            Filter_MobileGear_Rec1 = Filter_MobileGear_Rec1[
                            (Filter_MobileGear_Rec1.RecordType) == 1]
            
            Filter_MobileGear_Rec2 = MobileGear_FailConsistency[
                            (MobileGear_FailConsistency.RecordType) == 2]
            Filter_MobileGear_Rec2 = Filter_MobileGear_Rec2.drop_duplicates(
                                subset=['DeploymentUID'], keep="first")
            Filter_MobileGear_Rec2  = Filter_MobileGear_Rec2.reset_index(drop=True)
            Filter_MobileGear_Rec2 = (Filter_MobileGear_Rec2.groupby(
                ['Year','Country','ASOCCode', 'DeploymentNumber', 
                'SetNumber', 'DeploymentUID', 'Day','Month', 'StartTime', 'Duration'], 
                as_index=False)['RecordType'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
            Filter_MobileGear_Rec2 = Filter_MobileGear_Rec2[
                            (Filter_MobileGear_Rec2.RecordType) == 1]
            
            Filter_MobileGear = pd.concat([Filter_MobileGear_Rec1, Filter_MobileGear_Rec2])
            Filter_MobileGear.sort_values(by=['Year','Country','ASOCCode',
                            'DeploymentNumber','SetNumber'], inplace=True)
            Filter_MobileGear = Filter_MobileGear.drop_duplicates(
                                subset=['Year','Country','ASOCCode', 
                                'DeploymentNumber', 'SetNumber','DeploymentUID'],
                                keep="first")
            Filter_MobileGear.sort_values(by=['Year','Country','ASOCCode',
                            'DeploymentNumber','SetNumber'], inplace=True)
            Filter_MobileGear = Filter_MobileGear.loc[:,
                            ['ASOCCode', 'DeploymentNumber', 'SetNumber', 'DeploymentUID',
                            'Country','Year', 'Day', 'Month', 'StartTime', 'Duration']]
            Filter_MobileGear  = Filter_MobileGear.reset_index(drop=True)
            Filter_MobileGear  = pd.DataFrame(Filter_MobileGear)
            
            # Apply Special case for New Year Roll
            if len(Filter_MobileGear)>0:
                Filter_MobileGear['StartTime_Temp'] =  [str(num).zfill(4) for num in Filter_MobileGear['StartTime']]
                Filter_MobileGear['StartHour'] = (Filter_MobileGear['StartTime_Temp'].str[0:2]).astype(int)
                Filter_MobileGear['StartMin'] = (Filter_MobileGear['StartTime_Temp'].str[2:4]).astype(int)
                Filter_MobileGear.drop('StartTime_Temp', axis=1, inplace=True)
                Filter_MobileGear['DeploymentDate_Start'] = pd.to_datetime((Filter_MobileGear.Year.astype(str)+ \
                                        ' '+\
                                        Filter_MobileGear.Month.astype(str)+ \
                                        ' '+\
                                        Filter_MobileGear.Day.astype(str)
                                        ))
                Filter_MobileGear['DeploymentDate_End']=Filter_MobileGear.apply(
                            lambda g: g.DeploymentDate_Start + pd.DateOffset(hours=(g.StartHour + g.Duration), 
                            minutes = (g.StartMin)),axis=1)
                
                Filter_MobileGear['DeploymentDate_End'] = pd.to_datetime( Filter_MobileGear['DeploymentDate_End'],format='%Y-%m-%d')
                min_date = Filter_MobileGear['DeploymentDate_End'].min()
                max_date = Filter_MobileGear['DeploymentDate_End'].max()
                Filter_MobileGear = Filter_MobileGear[
                                ((Filter_MobileGear.DeploymentDate_End) >= min_date)&\
                                ((Filter_MobileGear.DeploymentDate_End) <= max_date)]
                Filter_MobileGear  = Filter_MobileGear.reset_index(drop=True)
                Filter_MobileGear  = pd.DataFrame(Filter_MobileGear)
                
                Filter_MobileGear['DeploymentEndYear'] = (Filter_MobileGear['DeploymentDate_End'].dt.strftime('%Y')).astype(int)
                
                Filter_MobileGear = Filter_MobileGear[
                            ((Filter_MobileGear.Year) == (Filter_MobileGear.DeploymentEndYear))]
                
                Filter_MobileGear  = Filter_MobileGear.reset_index(drop=True)
                Filter_MobileGear= (Filter_MobileGear.loc[:,
                                ['ASOCCode', 'DeploymentNumber', 'SetNumber', 'DeploymentUID',
                                'Country','Year', 'Day', 'Month', 'StartTime', 'Duration']])
                Filter_MobileGear  = pd.DataFrame(Filter_MobileGear)
        
            
            Filter_MobileGear['DeploymentTime'] =  ((Filter_MobileGear.StartTime)/100)
            
            Filter_MobileGear['DeploymentDate'] = pd.to_datetime(Filter_MobileGear.Year.astype(str)+ \
                                                            ' '+\
                                                            Filter_MobileGear.Month.astype(str)+ \
                                                            ' '+\
                                                            Filter_MobileGear.Day.astype(str)).dt.strftime('%Y-%m-%d')
            FillValueDate = pd.to_datetime((Filter_MobileGear.iloc[0]["DeploymentDate"])) + pd.DateOffset(days=-1)
            Filter_MobileGear  = pd.DataFrame(Filter_MobileGear)
            
            Filter_MobileGear["ASOCCode_Changed"] = (Filter_MobileGear["ASOCCode"].shift(1, 
            fill_value=Filter_MobileGear.iloc[0]["ASOCCode"])) - Filter_MobileGear["ASOCCode"]

            Filter_MobileGear["Month_Changed"] = abs((Filter_MobileGear["Month"].shift(1, 
            fill_value=Filter_MobileGear.iloc[0]["Month"])) - Filter_MobileGear["Month"])

            Filter_MobileGear["Day_Changed"] = abs((Filter_MobileGear["Day"].shift(1, 
            fill_value=Filter_MobileGear.iloc[0]["Day"])) - Filter_MobileGear["Day"])

            Filter_MobileGear["DeploymentNumber_Changed"] = (Filter_MobileGear["DeploymentNumber"].shift(1, 
            fill_value=Filter_MobileGear.iloc[0]["DeploymentNumber"])) - Filter_MobileGear["DeploymentNumber"]

            Filter_MobileGear["Year_Changed"] = (Filter_MobileGear["Year"].shift(1, 
            fill_value=Filter_MobileGear.iloc[0]["Year"])) - Filter_MobileGear["Year"]

            Filter_MobileGear["Country_Changed"] = (Filter_MobileGear["Country"].shift(1, 
            fill_value=Filter_MobileGear.iloc[0]["Country"])) - Filter_MobileGear["Country"]

            Filter_MobileGear["DeploymentTime_Changed"] = (Filter_MobileGear["DeploymentTime"].shift(1, 
                fill_value=Filter_MobileGear.iloc[0]["DeploymentTime"]-1)) - Filter_MobileGear["DeploymentTime"]
            
            Filter_MobileGear["DeploymentDate_Changed"] = (
                ((Filter_MobileGear["DeploymentDate"].shift(1, fill_value=FillValueDate)).apply(pd.to_datetime)) -\
                ((Filter_MobileGear["DeploymentDate"]).apply(pd.to_datetime))
                ).dt.days
            
            Filter1_MobileGear = Filter_MobileGear[
                            ((Filter_MobileGear.DeploymentDate_Changed) > 0)&\
                            ((Filter_MobileGear.ASOCCode_Changed) == 0) &\
                            (((Filter_MobileGear.Month_Changed) != 11 ) & ((Filter_MobileGear.Day_Changed) != 30 )) &\
                            ((Filter_MobileGear.DeploymentNumber_Changed) == 0)&\
                            ((Filter_MobileGear.Year_Changed) == 0)&\
                            ((Filter_MobileGear.Country_Changed) == 0)]
            
            Filter2_MobileGear = Filter_MobileGear[
                            ((Filter_MobileGear.DeploymentDate_Changed) == 0)&\
                            ((Filter_MobileGear.DeploymentTime_Changed) > 0)&\
                            ((Filter_MobileGear.ASOCCode_Changed) == 0) &\
                            (((Filter_MobileGear.Month_Changed) != 11 ) & ((Filter_MobileGear.Day_Changed) != 30 )) &\
                            ((Filter_MobileGear.DeploymentNumber_Changed) == 0)&\
                            ((Filter_MobileGear.Year_Changed) == 0)&\
                            ((Filter_MobileGear.Country_Changed) == 0)]
            
            ## Combining Filter1_MobileGear & Filter2_MobileGear
            Filter_MobileGear = pd.concat([Filter1_MobileGear, Filter2_MobileGear])
            Filter_MobileGear = Filter_MobileGear.drop_duplicates(
                                            subset=['DeploymentUID'], keep="first")
            Filter_MobileGear  = Filter_MobileGear.reset_index(drop=True)
            Filter_MobileGear  = pd.DataFrame(Filter_MobileGear)
        
            Filter_MobileGear = Filter_MobileGear.loc[:,
                                    ['DeploymentUID', 'ASOCCode','DeploymentNumber', 'SetNumber','Year', 'Country']]
            Filter_MobileGear  = pd.DataFrame(Filter_MobileGear)

            Filter_MobileGear = Filter_MobileGear.merge(
                            MobileGear_FailConsistency, 
                            on = ['DeploymentUID', 'ASOCCode','DeploymentNumber', 'SetNumber','Year','Country'], indicator=True, 
                            how='outer').query('_merge == "both"')
            Filter_MobileGear  = Filter_MobileGear.reset_index(drop=True)
            Filter_MobileGear= (Filter_MobileGear.loc[:,
                                ['DataBase_ID', 'RecordIdentifier', 'DeploymentUID', 
                                'ASOCCode','ObserverNumber', 'DeploymentNumber', 
                                'SetNumber', 'VesselSideNumber', 'RecordType', 'GearType', 'Country',
                                'Year','Day', 'Month', 
                                'StartTime', 'Duration']])
            Filter_MobileGear  = pd.DataFrame(Filter_MobileGear)
            Filter_MobileGear = Filter_MobileGear.replace([99999999, 99999999.0, '.'], '')
            Filter_MobileGear = Filter_MobileGear.replace(['99999999', '.'], 'None')
            Filter_MobileGear  = Filter_MobileGear.reset_index(drop=True)
            Filter_MobileGear['QC_Message'] ="Mobile Gear Consistency Failed"
            MobileGear_FailConsistency_DF  = pd.DataFrame(Filter_MobileGear)
            
            ## Building MobileGear_FailConsistency_DF Summary And Count
            if len(MobileGear_FailConsistency_DF)>0:
                MobileGear = (MobileGear_FailConsistency_DF.groupby(
                    ['ASOCCode','DeploymentNumber','Year'],
                    as_index=False)['SetNumber'].apply(lambda x: (np.count_nonzero(np.unique(x)))))
                MobileGear.rename(columns={'ASOCCode':'ASOCCode',
                                            'DeploymentNumber':'DeploymentNumber',
                                            'Year':'Year',
                                            'SetNumber':'QCFailCount'
                                            },inplace = True)
                MobileGear  = MobileGear.reset_index(drop=True)
                MobileGear  = pd.DataFrame(MobileGear)
                Len_FailCount_CalMobGear= sum(MobileGear['QCFailCount']) 
            else:
                Len_FailCount_CalMobGear= 0   
            
            ### Building MobileGear Summary DF
            ListMobileGear_FailedConsistency = ['FailCount_MobileGear_Consistency']
            NumMobileGear_FailedConsistency = [Len_FailCount_CalMobGear]
            Append_List_NumbFailConsiste = {'VariableName': ListMobileGear_FailedConsistency, 
                                            'QCFailCount': NumMobileGear_FailedConsistency} 
            MobileGear_FailedConsistencySummaryDF = pd.DataFrame(Append_List_NumbFailConsiste)
            MobileGear_FailedConsistencySummaryDF[['QCFailCount']] = MobileGear_FailedConsistencySummaryDF[['QCFailCount']].astype(int)
            MobileGear_FailedConsistencySummaryDF.sort_values(by=['QCFailCount'], inplace=True, ascending=False)
            MobileGear_FailedConsistencySummaryDF  = MobileGear_FailedConsistencySummaryDF.reset_index(drop=True)
            MobileGear_FailedConsistencySummaryDF  = pd.DataFrame(MobileGear_FailedConsistencySummaryDF)
            
            Length_MobileGear_FailedConsistency = (int(Len_FailCount_CalMobGear))
            # Submit Year_FailConsistency_DF Catch DB Storage
            Submit_MobileGear_FailConsistency(MobileGear_FailConsistency_DF,
                                            MobileGear_FailedConsistencySummaryDF)        
            return Length_MobileGear_FailedConsistency
        else:
            Length_QCFailedDF = 0
            tkinter.messagebox.showinfo("Mobile GearType Not Present For QC ID-C-05-4 Module",
                "Mobile GearType - [1,2,3,9,10,14,16,17,18,21,66,67,97] Not Present For QC ID-C-05-4 Module")
            print('Mobile GearType Not Present For QC ID-C-05-4 Module')
            DeleteDBStorage()
            return Length_QCFailedDF    
    
    ### Run Consistency QC 
    RunConsistencyFailed_YCQ = RunConsistencyFailed_Year_CntryQuota()
    RunConsistencyFailed_Vessel = RunConsistencyFailed_VesselVariables()
    RunConsistencyFailed_Calender = RunConsistencyFailed_CalenderVariables()
    RunConsistencyFailed_MG = RunConsistencyFailed_MobileGear()
    
    ## Count Total Consistency Failed
    TotalFailedQC_ConsistencyValidation = (int(RunConsistencyFailed_YCQ)+\
                                           int(RunConsistencyFailed_Vessel)+\
                                           int(RunConsistencyFailed_Calender)+\
                                           int(RunConsistencyFailed_MG))
    return TotalFailedQC_ConsistencyValidation





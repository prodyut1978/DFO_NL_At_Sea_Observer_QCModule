from tkinter import*
from tkinter import messagebox
import sqlite3
import pandas as pd

def RunLookUpTableValidation_BackEnd_Country():
    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")
    DB_SetCatch_Validation_LookUpTable = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")

    def GetCountryProfileDB():
        try:
            conn = sqlite3.connect(DB_Lookup_Table)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_CountryProfile ORDER BY `DataBaseUID` ASC ;", conn)
            if len(Complete_df) >0:
                CountryProfileDB_DF  = pd.DataFrame(Complete_df)
                CountryProfileDB_DF = CountryProfileDB_DF.loc[:,["CountryCode"]]
                CountryProfileDB_DF  = CountryProfileDB_DF.reset_index(drop=True)
                CountryProfileDB_DF.rename(columns={"CountryCode":"Country"},inplace = True)
                CountryProfileDB_DF  = pd.DataFrame(CountryProfileDB_DF)
                return CountryProfileDB_DF
            else:
                messagebox.showerror('Country Code Lookup Table Message', "Void Country Code Lookup Table...Please Import/Insert Country Coded Lookup Table")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def GetSetCatchProfileDB():
        try:
            conn = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','Country']]
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

    def Submit_QCFailedLookUpTable_Country(FailedValidation_CountryDB):
        try:
            Submit_To_DBStorage = pd.DataFrame(FailedValidation_CountryDB)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cursor = sqliteConnection.cursor()
            Submit_To_DBStorage.to_sql('SetCatch_QCFailedLookUpTable_Country', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    SetCatchProfileDB_DF = GetSetCatchProfileDB()
    SetCatchProfileDB_DF['Country'] = (SetCatchProfileDB_DF.loc[:,['Country']]).replace('', 99999999)
    SetCatchProfileDB_DF['Country'] = (SetCatchProfileDB_DF.loc[:,['Country']]).astype(int, errors='ignore')
    CountryProfileDB_DF  = GetCountryProfileDB()
    CountryProfileDB_DF['Country'] = (CountryProfileDB_DF.loc[:,['Country']]).replace('', 99999999)
    CountryProfileDB_DF['Country'] = (CountryProfileDB_DF.loc[:,['Country']]).astype(int, errors='ignore')
    FailedValidation_CountryDB = SetCatchProfileDB_DF.merge(
                                CountryProfileDB_DF, on = "Country", indicator=True, 
                                how='outer').query('_merge == "left_only"')
    FailedValidation_CountryDB = FailedValidation_CountryDB.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','Country']]
    FailedValidation_CountryDB['DataBase_ID'] = (FailedValidation_CountryDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
    FailedValidation_CountryDB['RecordIdentifier'] = (FailedValidation_CountryDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
    FailedValidation_CountryDB['Country'] = (FailedValidation_CountryDB.loc[:,['Country']]).astype(int, errors='ignore')
    FailedValidation_CountryDB['Country'] = (FailedValidation_CountryDB.loc[:,['Country']]).replace(99999999, '')
    FailedValidation_CountryDB['DeploymentIdentifier'] = 'None'
    FailedValidation_CountryDB  = FailedValidation_CountryDB.reset_index(drop=True)
    FailedValidation_CountryDB  = pd.DataFrame(FailedValidation_CountryDB)
    Submit_QCFailedLookUpTable_Country(FailedValidation_CountryDB)
    Length_FailedValidation_CountryDB = len(FailedValidation_CountryDB)
    return Length_FailedValidation_CountryDB

def RunLookUpTableValidation_BackEnd_ASOCCode():
    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")
    DB_SetCatch_Validation_LookUpTable = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")
    
    def GetASOCProfileDB():
        try:
            conn = sqlite3.connect(DB_Lookup_Table)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_ASOCCodeProfile ORDER BY `DatabaseUID` ASC ;", conn)
            if len(Complete_df) >0:
                ASOCProfileDB_DF  = pd.DataFrame(Complete_df)
                ASOCProfileDB_DF = ASOCProfileDB_DF.loc[:,["ASOCCode"]]
                ASOCProfileDB_DF  = ASOCProfileDB_DF.reset_index(drop=True)
                ASOCProfileDB_DF.rename(columns={"ASOCCode":"ASOCCode"},inplace = True)
                ASOCProfileDB_DF  = pd.DataFrame(ASOCProfileDB_DF)
                return ASOCProfileDB_DF
            else:
                messagebox.showerror('ASOC Code Lookup Table Message', "Void ASOC Code Lookup Table...Please Import/Insert ASOC Coded Lookup Table")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def GetSetCatchProfileDB():
        try:
            conn = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','ASOCCode']]
                SetCatchProfileDB_DF  = SetCatchProfileDB_DF.reset_index(drop=True)
                SetCatchProfileDB_DF  = pd.DataFrame(SetCatchProfileDB_DF)
                return SetCatchProfileDB_DF
            else:
                messagebox.showerror('DFO-NL-ASOP Set & Catch DB Message', 
                "Void DFO-NL-ASOP Set & Catch DB...Please Import DFO-NL-ASOP Set & \
                Catch CSV Files")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def Submit_QCFailedLookUpTable_ASOC(FailedValidation_ASOCDB):
        try:
            Submit_To_DBStorage = pd.DataFrame(FailedValidation_ASOCDB)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cursor = sqliteConnection.cursor()
            Submit_To_DBStorage.to_sql('SetCatch_QCFailedLookUpTable_ASOCCode', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    SetCatchProfileDB_DF = GetSetCatchProfileDB()
    SetCatchProfileDB_DF['ASOCCode'] = (SetCatchProfileDB_DF.loc[:,['ASOCCode']]).replace('', 99999999)
    SetCatchProfileDB_DF['ASOCCode'] = (SetCatchProfileDB_DF.loc[:,['ASOCCode']]).astype(int, errors='ignore')
    ASOCProfileDB_DF  = GetASOCProfileDB()
    ASOCProfileDB_DF['ASOCCode'] = (ASOCProfileDB_DF.loc[:,['ASOCCode']]).replace('', 99999999)
    ASOCProfileDB_DF['ASOCCode'] = (ASOCProfileDB_DF.loc[:,['ASOCCode']]).astype(int, errors='ignore')
    FailedValidation_ASOCDB = SetCatchProfileDB_DF.merge(
                                ASOCProfileDB_DF, on = "ASOCCode", indicator=True, 
                                how='outer').query('_merge == "left_only"')
    FailedValidation_ASOCDB = FailedValidation_ASOCDB.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','ASOCCode']]
    FailedValidation_ASOCDB['DataBase_ID'] = (FailedValidation_ASOCDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
    FailedValidation_ASOCDB['RecordIdentifier'] = (FailedValidation_ASOCDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
    FailedValidation_ASOCDB['ASOCCode'] = (FailedValidation_ASOCDB.loc[:,['ASOCCode']]).astype(int, errors='ignore')
    FailedValidation_ASOCDB['ASOCCode'] = (FailedValidation_ASOCDB.loc[:,['ASOCCode']]).replace(99999999, '')
    FailedValidation_ASOCDB['DeploymentIdentifier'] = 'None'
    FailedValidation_ASOCDB  = FailedValidation_ASOCDB.reset_index(drop=True)
    FailedValidation_ASOCDB  = pd.DataFrame(FailedValidation_ASOCDB)
    Submit_QCFailedLookUpTable_ASOC(FailedValidation_ASOCDB)
    Length_FailedValidation_ASOCDB = len(FailedValidation_ASOCDB)
    return Length_FailedValidation_ASOCDB

def RunLookUpTableValidation_BackEnd_DataSource():
    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")
    DB_SetCatch_Validation_LookUpTable = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")

    def GetDataSourceProfileDB():
        try:
            conn = sqlite3.connect(DB_Lookup_Table)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_DataSourceProfile ORDER BY `DatabaseUID` ASC ;", conn)
            if len(Complete_df) >0:
                DataSourceProfileDB_DF  = pd.DataFrame(Complete_df)
                DataSourceProfileDB_DF = DataSourceProfileDB_DF.loc[:,["DataSourceCode"]]
                DataSourceProfileDB_DF  = DataSourceProfileDB_DF.reset_index(drop=True)
                DataSourceProfileDB_DF.rename(columns={"DataSourceCode":"DataSource"},inplace = True)
                DataSourceProfileDB_DF  = pd.DataFrame(DataSourceProfileDB_DF)
                return DataSourceProfileDB_DF
            else:
                messagebox.showerror('DataSource Code Lookup Table Message', "Void DataSource Code Lookup Table...Please Import/Insert DataSource Coded Lookup Table")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def GetSetCatchProfileDB():
        try:
            conn = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','DataSource']]
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

    def Submit_QCFailedLookUpTable_DataSource(FailedValidation_DataSourceDB):
        try:
            Submit_To_DBStorage = pd.DataFrame(FailedValidation_DataSourceDB)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cursor = sqliteConnection.cursor()
            Submit_To_DBStorage.to_sql('SetCatch_QCFailedLookUpTable_DataSource', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    SetCatchProfileDB_DF = GetSetCatchProfileDB()
    SetCatchProfileDB_DF['DataSource'] = (SetCatchProfileDB_DF.loc[:,['DataSource']]).replace('', 99999999)
    SetCatchProfileDB_DF['DataSource'] = (SetCatchProfileDB_DF.loc[:,['DataSource']]).astype(int, errors='ignore')
    DataSourceProfileDB_DF  = GetDataSourceProfileDB()
    DataSourceProfileDB_DF['DataSource'] = (DataSourceProfileDB_DF.loc[:,['DataSource']]).replace('', 99999999)
    DataSourceProfileDB_DF['DataSource'] = (DataSourceProfileDB_DF.loc[:,['DataSource']]).astype(int, errors='ignore')
    FailedValidation_DataSourceDB = SetCatchProfileDB_DF.merge(
                                DataSourceProfileDB_DF, on = "DataSource", indicator=True, 
                                how='outer').query('_merge == "left_only"')
    FailedValidation_DataSourceDB = FailedValidation_DataSourceDB.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','DataSource']]
    FailedValidation_DataSourceDB['DataBase_ID'] = (FailedValidation_DataSourceDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
    FailedValidation_DataSourceDB['RecordIdentifier'] = (FailedValidation_DataSourceDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
    FailedValidation_DataSourceDB['DataSource'] = (FailedValidation_DataSourceDB.loc[:,['DataSource']]).astype(int, errors='ignore')
    FailedValidation_DataSourceDB['DataSource'] = (FailedValidation_DataSourceDB.loc[:,['DataSource']]).replace(99999999, '')
    FailedValidation_DataSourceDB['DeploymentIdentifier'] = 'None'
    FailedValidation_DataSourceDB  = FailedValidation_DataSourceDB.reset_index(drop=True)
    FailedValidation_DataSourceDB  = pd.DataFrame(FailedValidation_DataSourceDB)
    Submit_QCFailedLookUpTable_DataSource(FailedValidation_DataSourceDB)
    Length_FailedValidation_DataSourceDB = len(FailedValidation_DataSourceDB)
    return Length_FailedValidation_DataSourceDB

def RunLookUpTableValidation_BackEnd_GearDamage():
    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")
    DB_SetCatch_Validation_LookUpTable = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")

    def GetGearDamageProfileDB():
        try:
            conn = sqlite3.connect(DB_Lookup_Table)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_GearDamageProfile ORDER BY `DatabaseUID` ASC ;", conn)
            if len(Complete_df) >0:
                GearDamageProfileDB_DF  = pd.DataFrame(Complete_df)
                GearDamageProfileDB_DF = GearDamageProfileDB_DF.loc[:,["GearDamageCode"]]
                GearDamageProfileDB_DF  = GearDamageProfileDB_DF.reset_index(drop=True)
                GearDamageProfileDB_DF.rename(columns={"GearDamageCode":"GearDamage"},inplace = True)
                GearDamageProfileDB_DF  = pd.DataFrame(GearDamageProfileDB_DF)
                return GearDamageProfileDB_DF
            else:
                messagebox.showerror('GearDamage Code Lookup Table Message', "Void GearDamage Code Lookup Table...Please Import/Insert GearDamage Coded Lookup Table")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def GetSetCatchProfileDB():
        try:
            conn = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','GearDamage']]
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

    def Submit_QCFailedLookUpTable_GearDamage(FailedValidation_GearDamageDB):
        try:
            Submit_To_DBStorage = pd.DataFrame(FailedValidation_GearDamageDB)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cursor = sqliteConnection.cursor()
            Submit_To_DBStorage.to_sql('SetCatch_QCFailedLookUpTable_GearDamage', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    SetCatchProfileDB_DF = GetSetCatchProfileDB()
    SetCatchProfileDB_DF['GearDamage'] = (SetCatchProfileDB_DF.loc[:,['GearDamage']]).replace('', 99999999)
    SetCatchProfileDB_DF['GearDamage'] = (SetCatchProfileDB_DF.loc[:,['GearDamage']]).astype(int)
    GearDamageProfileDB_DF  = GetGearDamageProfileDB()
    GearDamageProfileDB_DF['GearDamage'] = (GearDamageProfileDB_DF.loc[:,['GearDamage']]).replace('', 99999999)
    GearDamageProfileDB_DF['GearDamage'] = (GearDamageProfileDB_DF.loc[:,['GearDamage']]).astype(int)
    
    FailedValidation_GearDamageDB = SetCatchProfileDB_DF.merge(
                                GearDamageProfileDB_DF, on = "GearDamage", indicator=True, 
                                how='outer').query('_merge == "left_only"')
    
    FailedValidation_GearDamageDB = FailedValidation_GearDamageDB.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','GearDamage']]
    FailedValidation_GearDamageDB['DataBase_ID'] = (FailedValidation_GearDamageDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
    FailedValidation_GearDamageDB['RecordIdentifier'] = (FailedValidation_GearDamageDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
    FailedValidation_GearDamageDB['GearDamage'] = (FailedValidation_GearDamageDB.loc[:,['GearDamage']]).astype(int, errors='ignore')
    FailedValidation_GearDamageDB['GearDamage'] = (FailedValidation_GearDamageDB.loc[:,['GearDamage']]).replace(99999999, '')
    FailedValidation_GearDamageDB['DeploymentIdentifier'] = 'None'
    FailedValidation_GearDamageDB  = FailedValidation_GearDamageDB.reset_index(drop=True)
    FailedValidation_GearDamageDB  = pd.DataFrame(FailedValidation_GearDamageDB)
    Submit_QCFailedLookUpTable_GearDamage(FailedValidation_GearDamageDB)
    Length_FailedValidation_GearDamageDB = len(FailedValidation_GearDamageDB)
    return Length_FailedValidation_GearDamageDB

def RunLookUpTableValidation_BackEnd_GearType():
    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")
    DB_SetCatch_Validation_LookUpTable = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")

    def GetGearTypeProfileDB():
        try:
            conn = sqlite3.connect(DB_Lookup_Table)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_GearTypeProfile ORDER BY `DatabaseUID` ASC ;", conn)
            if len(Complete_df) >0:
                GearTypeProfileDB_DF  = pd.DataFrame(Complete_df)
                GearTypeProfileDB_DF = GearTypeProfileDB_DF.loc[:,["GearTypeCode"]]
                GearTypeProfileDB_DF  = GearTypeProfileDB_DF.reset_index(drop=True)
                GearTypeProfileDB_DF.rename(columns={"GearTypeCode":"GearType"},inplace = True)
                GearTypeProfileDB_DF  = pd.DataFrame(GearTypeProfileDB_DF)
                return GearTypeProfileDB_DF
            else:
                messagebox.showerror('GearType Code Lookup Table Message', "Void GearType Code Lookup Table...Please Import/Insert GearType Coded Lookup Table")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def GetSetCatchProfileDB():
        try:
            conn = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','GearType']]
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

    def Submit_QCFailedLookUpTable_GearType(FailedValidation_GearTypeDB):
        try:
            Submit_To_DBStorage = pd.DataFrame(FailedValidation_GearTypeDB)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cursor = sqliteConnection.cursor()
            Submit_To_DBStorage.to_sql('SetCatch_QCFailedLookUpTable_GearType', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    SetCatchProfileDB_DF = GetSetCatchProfileDB()
    SetCatchProfileDB_DF['GearType'] = (SetCatchProfileDB_DF.loc[:,['GearType']]).replace('', 99999999)
    SetCatchProfileDB_DF['GearType'] = (SetCatchProfileDB_DF.loc[:,['GearType']]).astype(int, errors='ignore')
    GearTypeProfileDB_DF  = GetGearTypeProfileDB()
    GearTypeProfileDB_DF['GearType'] = (GearTypeProfileDB_DF.loc[:,['GearType']]).replace('', 99999999)
    GearTypeProfileDB_DF['GearType'] = (GearTypeProfileDB_DF.loc[:,['GearType']]).astype(int, errors='ignore')
    FailedValidation_GearTypeDB = SetCatchProfileDB_DF.merge(
                                GearTypeProfileDB_DF, on = "GearType", indicator=True, 
                                how='outer').query('_merge == "left_only"')
    FailedValidation_GearTypeDB = FailedValidation_GearTypeDB.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','GearType']]
    FailedValidation_GearTypeDB['DataBase_ID'] = (FailedValidation_GearTypeDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
    FailedValidation_GearTypeDB['RecordIdentifier'] = (FailedValidation_GearTypeDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
    FailedValidation_GearTypeDB['GearType'] = (FailedValidation_GearTypeDB.loc[:,['GearType']]).astype(int, errors='ignore')
    FailedValidation_GearTypeDB['GearType'] = (FailedValidation_GearTypeDB.loc[:,['GearType']]).replace(99999999, '')
    FailedValidation_GearTypeDB['DeploymentIdentifier'] = 'None'
    FailedValidation_GearTypeDB  = FailedValidation_GearTypeDB.reset_index(drop=True)
    FailedValidation_GearTypeDB  = pd.DataFrame(FailedValidation_GearTypeDB)
    Submit_QCFailedLookUpTable_GearType(FailedValidation_GearTypeDB)
    Length_FailedValidation_GearTypeDB = len(FailedValidation_GearTypeDB)
    return Length_FailedValidation_GearTypeDB

def RunLookUpTableValidation_BackEnd_Quota():
    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")
    DB_SetCatch_Validation_LookUpTable = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")

    def GetQuotaProfileDB():
        try:
            conn = sqlite3.connect(DB_Lookup_Table)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_QuotaProfile ORDER BY `DatabaseUID` ASC ;", conn)
            if len(Complete_df) >0:
                QuotaProfileDB_DF  = pd.DataFrame(Complete_df)
                QuotaProfileDB_DF = QuotaProfileDB_DF.loc[:,["QuotaCode"]]
                QuotaProfileDB_DF  = QuotaProfileDB_DF.reset_index(drop=True)
                QuotaProfileDB_DF.rename(columns={"QuotaCode":"Quota"},inplace = True)
                QuotaProfileDB_DF  = pd.DataFrame(QuotaProfileDB_DF)
                return QuotaProfileDB_DF
            else:
                messagebox.showerror('Quota Code Lookup Table Message', "Void Quota Code Lookup Table...Please Import/Insert Quota Coded Lookup Table")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def GetSetCatchProfileDB():
        try:
            conn = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','Quota']]
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

    def Submit_QCFailedLookUpTable_Quota(FailedValidation_QuotaDB):
        try:
            Submit_To_DBStorage = pd.DataFrame(FailedValidation_QuotaDB)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cursor = sqliteConnection.cursor()
            Submit_To_DBStorage.to_sql('SetCatch_QCFailedLookUpTable_Quota', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    SetCatchProfileDB_DF = GetSetCatchProfileDB()
    SetCatchProfileDB_DF['Quota'] = (SetCatchProfileDB_DF.loc[:,['Quota']]).replace('', 99999999)
    SetCatchProfileDB_DF['Quota'] = (SetCatchProfileDB_DF.loc[:,['Quota']]).astype(int, errors='ignore')
    QuotaProfileDB_DF  = GetQuotaProfileDB()
    QuotaProfileDB_DF['Quota'] = (QuotaProfileDB_DF.loc[:,['Quota']]).replace('', 99999999)
    QuotaProfileDB_DF['Quota'] = (QuotaProfileDB_DF.loc[:,['Quota']]).astype(int, errors='ignore')
    FailedValidation_QuotaDB = SetCatchProfileDB_DF.merge(
                                QuotaProfileDB_DF, on = "Quota", indicator=True, 
                                how='outer').query('_merge == "left_only"')
    FailedValidation_QuotaDB = FailedValidation_QuotaDB.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','Quota']]
    FailedValidation_QuotaDB['DataBase_ID'] = (FailedValidation_QuotaDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
    FailedValidation_QuotaDB['RecordIdentifier'] = (FailedValidation_QuotaDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
    FailedValidation_QuotaDB['Quota'] = (FailedValidation_QuotaDB.loc[:,['Quota']]).astype(int, errors='ignore')
    FailedValidation_QuotaDB['Quota'] = (FailedValidation_QuotaDB.loc[:,['Quota']]).replace(99999999, '')
    FailedValidation_QuotaDB['DeploymentIdentifier'] = 'None'
    FailedValidation_QuotaDB  = FailedValidation_QuotaDB.reset_index(drop=True)
    FailedValidation_QuotaDB  = pd.DataFrame(FailedValidation_QuotaDB)
    Submit_QCFailedLookUpTable_Quota(FailedValidation_QuotaDB)
    Length_FailedValidation_QuotaDB = len(FailedValidation_QuotaDB)
    return Length_FailedValidation_QuotaDB

def RunLookUpTableValidation_BackEnd_SetType():
    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")
    DB_SetCatch_Validation_LookUpTable = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")

    def GetSetTypeProfileDB():
        try:
            conn = sqlite3.connect(DB_Lookup_Table)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_SetTypeProfile ORDER BY `DatabaseUID` ASC ;", conn)
            if len(Complete_df) >0:
                SetTypeProfileDB_DF  = pd.DataFrame(Complete_df)
                SetTypeProfileDB_DF = SetTypeProfileDB_DF.loc[:,["SetTypeCode"]]
                SetTypeProfileDB_DF  = SetTypeProfileDB_DF.reset_index(drop=True)
                SetTypeProfileDB_DF.rename(columns={"SetTypeCode":"SetType"},inplace = True)
                SetTypeProfileDB_DF  = pd.DataFrame(SetTypeProfileDB_DF)
                return SetTypeProfileDB_DF
            else:
                messagebox.showerror('SetType Code Lookup Table Message', "Void SetType Code Lookup Table...Please Import/Insert SetType Coded Lookup Table")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def GetSetCatchProfileDB():
        try:
            conn = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','SetType']]
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

    def Submit_QCFailedLookUpTable_SetType(FailedValidation_SetTypeDB):
        try:
            Submit_To_DBStorage = pd.DataFrame(FailedValidation_SetTypeDB)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cursor = sqliteConnection.cursor()
            Submit_To_DBStorage.to_sql('SetCatch_QCFailedLookUpTable_SetType', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    SetCatchProfileDB_DF = GetSetCatchProfileDB()
    SetCatchProfileDB_DF['SetType'] = (SetCatchProfileDB_DF.loc[:,['SetType']]).replace('', 99999999)
    SetCatchProfileDB_DF['SetType'] = (SetCatchProfileDB_DF.loc[:,['SetType']]).astype(int, errors='ignore')
    SetTypeProfileDB_DF  = GetSetTypeProfileDB()
    SetTypeProfileDB_DF['SetType'] = (SetTypeProfileDB_DF.loc[:,['SetType']]).replace('', 99999999)
    SetTypeProfileDB_DF['SetType'] = (SetTypeProfileDB_DF.loc[:,['SetType']]).astype(int, errors='ignore')
    FailedValidation_SetTypeDB = SetCatchProfileDB_DF.merge(
                                SetTypeProfileDB_DF, on = "SetType", indicator=True, 
                                how='outer').query('_merge == "left_only"')
    FailedValidation_SetTypeDB = FailedValidation_SetTypeDB.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','SetType']]
    FailedValidation_SetTypeDB['DataBase_ID'] = (FailedValidation_SetTypeDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
    FailedValidation_SetTypeDB['RecordIdentifier'] = (FailedValidation_SetTypeDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
    FailedValidation_SetTypeDB['SetType'] = (FailedValidation_SetTypeDB.loc[:,['SetType']]).astype(int, errors='ignore')
    FailedValidation_SetTypeDB['SetType'] = (FailedValidation_SetTypeDB.loc[:,['SetType']]).replace(99999999, '')
    FailedValidation_SetTypeDB['DeploymentIdentifier'] = 'None'
    FailedValidation_SetTypeDB  = FailedValidation_SetTypeDB.reset_index(drop=True)
    FailedValidation_SetTypeDB  = pd.DataFrame(FailedValidation_SetTypeDB)
    Submit_QCFailedLookUpTable_SetType(FailedValidation_SetTypeDB)
    Length_FailedValidation_SetTypeDB = len(FailedValidation_SetTypeDB)
    return Length_FailedValidation_SetTypeDB

def RunLookUpTableValidation_BackEnd_SpeciesCode():
    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")
    DB_SetCatch_Validation_LookUpTable = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")

    def GetSpeciesCodeProfileDB():
        try:
            conn = sqlite3.connect(DB_Lookup_Table)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_SpeciesCodeProfile ORDER BY `DatabaseUID` ASC ;", conn)
            if len(Complete_df) >0:
                SpeciesCodeProfileDB_DF  = pd.DataFrame(Complete_df)
                SpeciesCodeProfileDB_DF = SpeciesCodeProfileDB_DF.loc[:,["SpeciesCode"]]
                SpeciesCodeProfileDB_DF  = SpeciesCodeProfileDB_DF.reset_index(drop=True)
                SpeciesCodeProfileDB_DF.rename(columns={"SpeciesCode":"SpeciesCode"},inplace = True)
                SpeciesCodeProfileDB_DF  = pd.DataFrame(SpeciesCodeProfileDB_DF)
                return SpeciesCodeProfileDB_DF
            else:
                messagebox.showerror('SpeciesCode Code Lookup Table Message', "Void SpeciesCode Code Lookup Table...Please Import/Insert SpeciesCode Coded Lookup Table")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def GetSetCatchProfileDB():
        try:
            conn = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType','SpeciesCode']]
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

    def Submit_QCFailedLookUpTable_SpeciesCode(FailedValidation_SpeciesCodeDB):
        try:
            Submit_To_DBStorage = pd.DataFrame(FailedValidation_SpeciesCodeDB)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cursor = sqliteConnection.cursor()
            Submit_To_DBStorage.to_sql('SetCatch_QCFailedLookUpTable_SpeciesCode', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    SetCatchProfileDB_DF = GetSetCatchProfileDB()
    SetCatchProfileDB_DF['RecordType'] = (SetCatchProfileDB_DF.loc[:,['RecordType']]).replace('', 99999999)
    SetCatchProfileDB_DF['SpeciesCode'] = (SetCatchProfileDB_DF.loc[:,['SpeciesCode']]).replace('', 99999999)
    SetCatchProfileDB_DF['RecordType'] = (SetCatchProfileDB_DF.loc[:,['RecordType']]).astype(int, errors='ignore')
    SetCatchProfileDB_DF['SpeciesCode'] = (SetCatchProfileDB_DF.loc[:,['SpeciesCode']]).astype(int, errors='ignore')
    SpeciesCodeProfileDB_DF  = GetSpeciesCodeProfileDB()
    SpeciesCodeProfileDB_DF['SpeciesCode'] = (SpeciesCodeProfileDB_DF.loc[:,['SpeciesCode']]).replace('', 99999999)
    SpeciesCodeProfileDB_DF['SpeciesCode'] = (SpeciesCodeProfileDB_DF.loc[:,['SpeciesCode']]).astype(int, errors='ignore')
    
    FailedValidation_SpeciesCodeDB = SetCatchProfileDB_DF.merge(
                                SpeciesCodeProfileDB_DF, on = "SpeciesCode", indicator=True, 
                                how='outer').query('_merge == "left_only"')
    FailedValidation_SpeciesCodeDB = FailedValidation_SpeciesCodeDB.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType','SpeciesCode']]
    FailedValidation_SpeciesCodeDB['DataBase_ID'] = (FailedValidation_SpeciesCodeDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
    FailedValidation_SpeciesCodeDB['RecordIdentifier'] = (FailedValidation_SpeciesCodeDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
    FailedValidation_SpeciesCodeDB['RecordType'] = (FailedValidation_SpeciesCodeDB.loc[:,['RecordType']]).astype(int, errors='ignore')
    FailedValidation_SpeciesCodeDB['SpeciesCode'] = (FailedValidation_SpeciesCodeDB.loc[:,['SpeciesCode']]).astype(int, errors='ignore')
    FailedValidation_SpeciesCodeDB = FailedValidation_SpeciesCodeDB.loc[FailedValidation_SpeciesCodeDB['RecordType'] == 2]
    FailedValidation_SpeciesCodeDB['SpeciesCode'] = (FailedValidation_SpeciesCodeDB.loc[:,['SpeciesCode']]).replace(99999999, '')
    FailedValidation_SpeciesCodeDB['RecordType'] = (FailedValidation_SpeciesCodeDB.loc[:,['RecordType']]).replace(99999999, '')
    FailedValidation_SpeciesCodeDB['DeploymentIdentifier'] = 'None'
    FailedValidation_SpeciesCodeDB  = FailedValidation_SpeciesCodeDB.reset_index(drop=True)
    FailedValidation_SpeciesCodeDB  = pd.DataFrame(FailedValidation_SpeciesCodeDB)
    Submit_QCFailedLookUpTable_SpeciesCode(FailedValidation_SpeciesCodeDB)
    Length_FailedValidation_SpeciesCodeDB = len(FailedValidation_SpeciesCodeDB)
    return Length_FailedValidation_SpeciesCodeDB

def RunLookUpTableValidation_BackEnd_DirectedSpecies():
    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")
    DB_SetCatch_Validation_LookUpTable = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")

    def GetDirectedSpeciesProfileDB():
        try:
            conn = sqlite3.connect(DB_Lookup_Table)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_SpeciesCodeProfile ORDER BY `DatabaseUID` ASC ;", conn)
            if len(Complete_df) >0:
                DirectedSpeciesProfileDB_DF  = pd.DataFrame(Complete_df)
                DirectedSpeciesProfileDB_DF = DirectedSpeciesProfileDB_DF.loc[:,["SpeciesCode"]]
                DirectedSpeciesProfileDB_DF  = DirectedSpeciesProfileDB_DF.reset_index(drop=True)
                DirectedSpeciesProfileDB_DF.rename(columns={"SpeciesCode":"DirectedSpecies"},inplace = True)
                DirectedSpeciesProfileDB_DF  = pd.DataFrame(DirectedSpeciesProfileDB_DF)
                return DirectedSpeciesProfileDB_DF
            else:
                messagebox.showerror('DirectedSpecies Code Lookup Table Message', "Void DirectedSpecies Code Lookup Table...Please Import/Insert DirectedSpecies Coded Lookup Table")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def GetSetCatchProfileDB():
        try:
            conn = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType','DirectedSpecies']]
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

    def Submit_QCFailedLookUpTable_DirectedSpecies(FailedValidation_DirectedSpeciesDB):
        try:
            Submit_To_DBStorage = pd.DataFrame(FailedValidation_DirectedSpeciesDB)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cursor = sqliteConnection.cursor()
            Submit_To_DBStorage.to_sql('SetCatch_QCFailedLookUpTable_DirectedSpecies', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    SetCatchProfileDB_DF = GetSetCatchProfileDB()
    SetCatchProfileDB_DF['DirectedSpecies'] = (SetCatchProfileDB_DF.loc[:,['DirectedSpecies']]).replace('', 99999999)
    SetCatchProfileDB_DF['RecordType'] = (SetCatchProfileDB_DF.loc[:,['RecordType']]).astype(int, errors='ignore')
    SetCatchProfileDB_DF['DirectedSpecies'] = (SetCatchProfileDB_DF.loc[:,['DirectedSpecies']]).astype(int, errors='ignore')
    DirectedSpeciesProfileDB_DF  = GetDirectedSpeciesProfileDB()
    DirectedSpeciesProfileDB_DF['DirectedSpecies'] = (DirectedSpeciesProfileDB_DF.loc[:,['DirectedSpecies']]).replace('', 99999999)
    DirectedSpeciesProfileDB_DF['DirectedSpecies'] = (DirectedSpeciesProfileDB_DF.loc[:,['DirectedSpecies']]).astype(int, errors='ignore')
    
    FailedValidation_DirectedSpeciesDB = SetCatchProfileDB_DF.merge(
                                DirectedSpeciesProfileDB_DF, on = "DirectedSpecies", indicator=True, 
                                how='outer').query('_merge == "left_only"')
    FailedValidation_DirectedSpeciesDB = FailedValidation_DirectedSpeciesDB.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','RecordType','DirectedSpecies']]
    FailedValidation_DirectedSpeciesDB['DataBase_ID'] = (FailedValidation_DirectedSpeciesDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
    FailedValidation_DirectedSpeciesDB['RecordIdentifier'] = (FailedValidation_DirectedSpeciesDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
    FailedValidation_DirectedSpeciesDB['RecordType'] = (FailedValidation_DirectedSpeciesDB.loc[:,['RecordType']]).astype(int, errors='ignore')
    FailedValidation_DirectedSpeciesDB['DirectedSpecies'] = (FailedValidation_DirectedSpeciesDB.loc[:,['DirectedSpecies']]).astype(int, errors='ignore')
    FailedValidation_DirectedSpeciesDB['DirectedSpecies'] = (FailedValidation_DirectedSpeciesDB.loc[:,['DirectedSpecies']]).replace(99999999, '')
    FailedValidation_DirectedSpeciesDB['DeploymentIdentifier'] = 'None'
    FailedValidation_DirectedSpeciesDB  = FailedValidation_DirectedSpeciesDB.reset_index(drop=True)
    FailedValidation_DirectedSpeciesDB  = pd.DataFrame(FailedValidation_DirectedSpeciesDB)
    Submit_QCFailedLookUpTable_DirectedSpecies(FailedValidation_DirectedSpeciesDB)
    Length_FailedValidation_DirectedSpeciesDB = len(FailedValidation_DirectedSpeciesDB)
    return Length_FailedValidation_DirectedSpeciesDB

def RunLookUpTableValidation_BackEnd_VesselClass():
    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")
    DB_SetCatch_Validation_LookUpTable = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")

    def GetVesselClassProfileDB():
        try:
            conn = sqlite3.connect(DB_Lookup_Table)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_VesselClassProfile ORDER BY `DatabaseUID` ASC ;", conn)
            if len(Complete_df) >0:
                VesselClassProfileDB_DF  = pd.DataFrame(Complete_df)
                VesselClassProfileDB_DF = VesselClassProfileDB_DF.loc[:,["VesselClassCode"]]
                VesselClassProfileDB_DF  = VesselClassProfileDB_DF.reset_index(drop=True)
                VesselClassProfileDB_DF.rename(columns={"VesselClassCode":"VesselClass"},inplace = True)
                VesselClassProfileDB_DF  = pd.DataFrame(VesselClassProfileDB_DF)
                return VesselClassProfileDB_DF
            else:
                messagebox.showerror('VesselClass Code Lookup Table Message', "Void VesselClass Code Lookup Table...Please Import/Insert VesselClass Coded Lookup Table")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def GetSetCatchProfileDB():
        try:
            conn = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','VesselClass']]
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

    def Submit_QCFailedLookUpTable_VesselClass(FailedValidation_VesselClassDB):
        try:
            Submit_To_DBStorage = pd.DataFrame(FailedValidation_VesselClassDB)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cursor = sqliteConnection.cursor()
            Submit_To_DBStorage.to_sql('SetCatch_QCFailedLookUpTable_VesselClass', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    SetCatchProfileDB_DF = GetSetCatchProfileDB()
    SetCatchProfileDB_DF['VesselClass'] = (SetCatchProfileDB_DF.loc[:,['VesselClass']]).replace('', 99999999)
    SetCatchProfileDB_DF['VesselClass'] = (SetCatchProfileDB_DF.loc[:,['VesselClass']]).astype(int, errors='ignore')
    VesselClassProfileDB_DF  = GetVesselClassProfileDB()
    VesselClassProfileDB_DF['VesselClass'] = (VesselClassProfileDB_DF.loc[:,['VesselClass']]).replace('', 99999999)
    VesselClassProfileDB_DF['VesselClass'] = (VesselClassProfileDB_DF.loc[:,['VesselClass']]).astype(int, errors='ignore')
    FailedValidation_VesselClassDB = SetCatchProfileDB_DF.merge(
                                VesselClassProfileDB_DF, on = "VesselClass", indicator=True, 
                                how='outer').query('_merge == "left_only"')
    FailedValidation_VesselClassDB = FailedValidation_VesselClassDB.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','VesselClass']]
    FailedValidation_VesselClassDB['DataBase_ID'] = (FailedValidation_VesselClassDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
    FailedValidation_VesselClassDB['RecordIdentifier'] = (FailedValidation_VesselClassDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
    FailedValidation_VesselClassDB['VesselClass'] = (FailedValidation_VesselClassDB.loc[:,['VesselClass']]).astype(int, errors='ignore')
    FailedValidation_VesselClassDB['VesselClass'] = (FailedValidation_VesselClassDB.loc[:,['VesselClass']]).replace(99999999, '')
    FailedValidation_VesselClassDB['DeploymentIdentifier'] = 'None'
    FailedValidation_VesselClassDB  = FailedValidation_VesselClassDB.reset_index(drop=True)
    FailedValidation_VesselClassDB  = pd.DataFrame(FailedValidation_VesselClassDB)
    Submit_QCFailedLookUpTable_VesselClass(FailedValidation_VesselClassDB)
    Length_FailedValidation_VesselClassDB = len(FailedValidation_VesselClassDB)
    return Length_FailedValidation_VesselClassDB

def RunLookUpTableValidation_BackEnd_NAFODivision():
    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")
    DB_SetCatch_Validation_LookUpTable = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")

    def GetNAFODivisionProfileDB():
        try:
            conn = sqlite3.connect(DB_Lookup_Table)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_NAFODivisionProfile ORDER BY `DatabaseUID` ASC ;", conn)
            if len(Complete_df) >0:
                NAFODivisionProfileDB_DF  = pd.DataFrame(Complete_df)
                NAFODivisionProfileDB_DF = NAFODivisionProfileDB_DF.loc[:,["AlphaNAFODivision"]]
                NAFODivisionProfileDB_DF  = NAFODivisionProfileDB_DF.reset_index(drop=True)
                NAFODivisionProfileDB_DF.rename(columns={"AlphaNAFODivision":"NAFODivision"},inplace = True)
                NAFODivisionProfileDB_DF  = pd.DataFrame(NAFODivisionProfileDB_DF)
                return NAFODivisionProfileDB_DF
            else:
                messagebox.showerror('NAFODivision Code Lookup Table Message', "Void NAFODivision Code Lookup Table...Please Import/Insert NAFODivision Coded Lookup Table")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def GetSetCatchProfileDB():
        try:
            conn = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','NAFODivision', 'UnitArea']]
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

    def Submit_QCFailedLookUpTable_NAFODivision(FailedValidation_NAFODivisionDB):
        try:
            Submit_To_DBStorage = pd.DataFrame(FailedValidation_NAFODivisionDB)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cursor = sqliteConnection.cursor()
            Submit_To_DBStorage.to_sql('SetCatch_QCFailedLookUpTable_NAFODivision', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    SetCatchProfileDB_DF = GetSetCatchProfileDB()
    SetCatchProfileDB_DF['NAFODivision'] = (SetCatchProfileDB_DF.loc[:,['NAFODivision']]).replace('None', '999999999')
    SetCatchProfileDB_DF['NAFODivision'] = (SetCatchProfileDB_DF.loc[:,['NAFODivision']]).astype(str, errors='ignore')
    SetCatchProfileDB_DF['NAFODivision'] = SetCatchProfileDB_DF['NAFODivision'].str.strip()
    SetCatchProfileDB_DF['NAFODivision'] = SetCatchProfileDB_DF['NAFODivision'].str.replace(" ", "")
    
    NAFODivisionProfileDB_DF  = GetNAFODivisionProfileDB()
    NAFODivisionProfileDB_DF['NAFODivision'] = (NAFODivisionProfileDB_DF.loc[:,['NAFODivision']]).replace('None', '999999999')
    NAFODivisionProfileDB_DF['NAFODivision'] = (NAFODivisionProfileDB_DF.loc[:,['NAFODivision']]).astype(str, errors='ignore')
    NAFODivisionProfileDB_DF['NAFODivision'] = NAFODivisionProfileDB_DF['NAFODivision'].str.strip()
    NAFODivisionProfileDB_DF['NAFODivision'] = NAFODivisionProfileDB_DF['NAFODivision'].str.replace(" ", "")
   
    FailedValidation_NAFODivisionDB = SetCatchProfileDB_DF.merge(
                                NAFODivisionProfileDB_DF, on = "NAFODivision", indicator=True, 
                                how='outer').query('_merge == "left_only"')
    FailedValidation_NAFODivisionDB = FailedValidation_NAFODivisionDB.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','NAFODivision']]
    FailedValidation_NAFODivisionDB['DataBase_ID'] = (FailedValidation_NAFODivisionDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
    FailedValidation_NAFODivisionDB['RecordIdentifier'] = (FailedValidation_NAFODivisionDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
    FailedValidation_NAFODivisionDB['NAFODivision'] = (FailedValidation_NAFODivisionDB.loc[:,['NAFODivision']]).astype(str, errors='ignore')
    FailedValidation_NAFODivisionDB['NAFODivision'] = (FailedValidation_NAFODivisionDB.loc[:,['NAFODivision']]).replace('999999999', 'None')
    FailedValidation_NAFODivisionDB['DeploymentIdentifier'] = 'None'
    FailedValidation_NAFODivisionDB  = FailedValidation_NAFODivisionDB.reset_index(drop=True)
    FailedValidation_NAFODivisionDB  = pd.DataFrame(FailedValidation_NAFODivisionDB)
    Submit_QCFailedLookUpTable_NAFODivision(FailedValidation_NAFODivisionDB)
    Length_FailedValidation_NAFODivisionDB = len(FailedValidation_NAFODivisionDB)
    return Length_FailedValidation_NAFODivisionDB

def RunLookUpTableValidation_BackEnd_UnitArea():
    DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
    DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")
    DB_SetCatch_Validation_LookUpTable = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")

    def GetUnitAreaProfileDB():
        try:
            conn = sqlite3.connect(DB_Lookup_Table)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_NAFODivisionProfile ORDER BY `DatabaseUID` ASC ;", conn)
            if len(Complete_df) >0:
                UnitAreaProfileDB_DF  = pd.DataFrame(Complete_df)
                UnitAreaProfileDB_DF = UnitAreaProfileDB_DF.loc[:,["AlphaNAFODivision", "AlphaUnitArea"]]
                UnitAreaProfileDB_DF  = UnitAreaProfileDB_DF.reset_index(drop=True)
                UnitAreaProfileDB_DF.rename(columns={"AlphaNAFODivision":"NAFODivision"},inplace = True)
                UnitAreaProfileDB_DF.rename(columns={"AlphaUnitArea":"UnitArea"},inplace = True)
                UnitAreaProfileDB_DF  = pd.DataFrame(UnitAreaProfileDB_DF)
                return UnitAreaProfileDB_DF
            else:
                messagebox.showerror('UnitArea Code Lookup Table Message', "Void UnitArea Code Lookup Table...Please Import/Insert UnitArea Coded Lookup Table")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def GetSetCatchProfileDB():
        try:
            conn = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_Analysis_IMPORT ORDER BY `DataBase_ID` ASC ;", conn)
            if len(Complete_df) >0:
                SetCatchProfileDB_DF  = pd.DataFrame(Complete_df)
                SetCatchProfileDB_DF = SetCatchProfileDB_DF.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','NAFODivision', 'UnitArea']]
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

    def Submit_QCFailedLookUpTable_UnitArea(FailedValidation_UnitAreaDB):
        try:
            Submit_To_DBStorage = pd.DataFrame(FailedValidation_UnitAreaDB)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cursor = sqliteConnection.cursor()
            Submit_To_DBStorage.to_sql('SetCatch_QCFailedLookUpTable_UnitArea', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    SetCatchProfileDB_DF = GetSetCatchProfileDB()
    SetCatchProfileDB_DF['UnitArea'] = (SetCatchProfileDB_DF.loc[:,['UnitArea']]).replace('None', '999999999')
    SetCatchProfileDB_DF['UnitArea'] = (SetCatchProfileDB_DF.loc[:,['UnitArea']]).astype(str, errors='ignore')
    SetCatchProfileDB_DF['UnitArea'] = SetCatchProfileDB_DF['UnitArea'].str.strip()
    SetCatchProfileDB_DF['UnitArea'] = SetCatchProfileDB_DF['UnitArea'].str.replace(" ", "")
    
    SetCatchProfileDB_DF['NAFODivision'] = (SetCatchProfileDB_DF.loc[:,['NAFODivision']]).replace('None', '999999999')
    SetCatchProfileDB_DF['NAFODivision'] = (SetCatchProfileDB_DF.loc[:,['NAFODivision']]).astype(str, errors='ignore')
    SetCatchProfileDB_DF['NAFODivision'] = SetCatchProfileDB_DF['NAFODivision'].str.strip()
    SetCatchProfileDB_DF['NAFODivision'] = SetCatchProfileDB_DF['NAFODivision'].str.replace(" ", "")
    
    UnitAreaProfileDB_DF  = GetUnitAreaProfileDB()
    UnitAreaProfileDB_DF['UnitArea'] = (UnitAreaProfileDB_DF.loc[:,['UnitArea']]).replace('None', '999999999')
    UnitAreaProfileDB_DF['UnitArea'] = (UnitAreaProfileDB_DF.loc[:,['UnitArea']]).astype(str, errors='ignore')
    UnitAreaProfileDB_DF['UnitArea'] = UnitAreaProfileDB_DF['UnitArea'].str.strip()
    UnitAreaProfileDB_DF['UnitArea'] = UnitAreaProfileDB_DF['UnitArea'].str.replace(" ", "")
    
    UnitAreaProfileDB_DF['NAFODivision'] = (UnitAreaProfileDB_DF.loc[:,['NAFODivision']]).replace('None', '999999999')
    UnitAreaProfileDB_DF['NAFODivision'] = (UnitAreaProfileDB_DF.loc[:,['NAFODivision']]).astype(str, errors='ignore')
    UnitAreaProfileDB_DF['NAFODivision'] = UnitAreaProfileDB_DF['NAFODivision'].str.strip()
    UnitAreaProfileDB_DF['NAFODivision'] = UnitAreaProfileDB_DF['NAFODivision'].str.replace(" ", "")

    FailedValidation_UnitAreaDB = SetCatchProfileDB_DF.merge(
                                UnitAreaProfileDB_DF, on = ["NAFODivision", "UnitArea"], indicator=True, 
                                how='outer').query('_merge == "left_only"')
    
    FailedValidation_UnitAreaDB = FailedValidation_UnitAreaDB.loc[:,['DataBase_ID','RecordIdentifier','DeploymentUID','NAFODivision', 'UnitArea']]
    FailedValidation_UnitAreaDB['DataBase_ID'] = (FailedValidation_UnitAreaDB.loc[:,['DataBase_ID']]).astype(int, errors='ignore')
    FailedValidation_UnitAreaDB['RecordIdentifier'] = (FailedValidation_UnitAreaDB.loc[:,['RecordIdentifier']]).astype(int, errors='ignore')
    
    FailedValidation_UnitAreaDB['NAFODivision'] = (FailedValidation_UnitAreaDB.loc[:,['NAFODivision']]).astype(str, errors='ignore')
    FailedValidation_UnitAreaDB['NAFODivision'] = (FailedValidation_UnitAreaDB.loc[:,['NAFODivision']]).replace('999999999', 'None')
    
    FailedValidation_UnitAreaDB['UnitArea'] = (FailedValidation_UnitAreaDB.loc[:,['UnitArea']]).astype(str, errors='ignore')
    FailedValidation_UnitAreaDB['UnitArea'] = (FailedValidation_UnitAreaDB.loc[:,['UnitArea']]).replace('999999999', 'None')
    FailedValidation_UnitAreaDB['DeploymentIdentifier'] = 'None'
    FailedValidation_UnitAreaDB  = FailedValidation_UnitAreaDB.reset_index(drop=True)
    FailedValidation_UnitAreaDB  = pd.DataFrame(FailedValidation_UnitAreaDB)
    Submit_QCFailedLookUpTable_UnitArea(FailedValidation_UnitAreaDB)
    Length_FailedValidation_UnitAreaDB = len(FailedValidation_UnitAreaDB)
    return Length_FailedValidation_UnitAreaDB



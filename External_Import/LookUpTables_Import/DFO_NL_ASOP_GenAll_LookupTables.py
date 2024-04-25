#Front End
from tkinter import*
import tkinter.messagebox
from tkinter import ttk, filedialog
from tkinter import messagebox
import tkinter as tk
import sqlite3
import numpy as np
import pandas as pd

def DFO_NL_ASOP_Generate_All_LookupTables():
    try:
        DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")

        LookupTable_ExternalImport_ASOC = './External_Import/LookUpTables_Import/CSV_FilesFor_Import_LookupTable/ASOCCodesTable.csv'
        df_ASOC = pd.read_csv(LookupTable_ExternalImport_ASOC, sep=',' , low_memory=False)

        LookupTable_ExternalImport_Country = './External_Import/LookUpTables_Import/CSV_FilesFor_Import_LookupTable/CountryCodesTable.csv'
        df_Country = pd.read_csv(LookupTable_ExternalImport_Country, sep=',' , low_memory=False)

        LookupTable_ExternalImport_DataSource = './External_Import/LookUpTables_Import/CSV_FilesFor_Import_LookupTable/DataSourceCodesTable.csv'
        df_DataSource = pd.read_csv(LookupTable_ExternalImport_DataSource, sep=',' , low_memory=False)

        LookupTable_ExternalImport_GearDamage = './External_Import/LookUpTables_Import/CSV_FilesFor_Import_LookupTable/GearDamageCodesTable.csv'
        df_GearDamage = pd.read_csv(LookupTable_ExternalImport_GearDamage, sep=',' , low_memory=False)

        LookupTable_ExternalImport_GearType = './External_Import/LookUpTables_Import/CSV_FilesFor_Import_LookupTable/GearTypeCodesTable.csv'
        df_GearType = pd.read_csv(LookupTable_ExternalImport_GearType, sep=',' , low_memory=False)

        LookupTable_ExternalImport_Quota = './External_Import/LookUpTables_Import/CSV_FilesFor_Import_LookupTable/QuotaCodesTable.csv'
        df_Quota = pd.read_csv(LookupTable_ExternalImport_Quota, sep=',' , low_memory=False)

        LookupTable_ExternalImport_SetType = './External_Import/LookUpTables_Import/CSV_FilesFor_Import_LookupTable/SetTypeCodesTable.csv'
        df_SetType = pd.read_csv(LookupTable_ExternalImport_SetType, sep=',' , low_memory=False)

        LookupTable_ExternalImport_Species = './External_Import/LookUpTables_Import/CSV_FilesFor_Import_LookupTable/SpeciesCodesTable.csv'
        df_Species = pd.read_csv(LookupTable_ExternalImport_Species, sep=',' , low_memory=False)

        LookupTable_ExternalImport_VesselClass = './External_Import/LookUpTables_Import/CSV_FilesFor_Import_LookupTable/VesselClassCodesTable.csv'
        df_VesselClass = pd.read_csv(LookupTable_ExternalImport_VesselClass, sep=',' , low_memory=False)

        LookupTable_ExternalImport_NAFODivision = './External_Import/LookUpTables_Import/CSV_FilesFor_Import_LookupTable/NAFODivisionCodesTable.csv'
        df_NAFODivision = pd.read_csv(LookupTable_ExternalImport_NAFODivision, sep=',' , low_memory=False)

        if (len(df_ASOC) >0) & (len(df_Country) >0) & \
        (len(df_DataSource) >0) & (len(df_GearDamage) >0) & \
        (len(df_GearType) >0) & (len(df_Quota) >0) & \
        (len(df_SetType) >0) & (len(df_Species) >0) & \
        (len(df_VesselClass) >0) & (len(df_NAFODivision) >0):
            try:
                Import_Lookup_df_ASOC = pd.DataFrame(df_ASOC)
                Import_Lookup_df_Country = pd.DataFrame(df_Country)
                Import_Lookup_df_DataSource = pd.DataFrame(df_DataSource)
                Import_Lookup_df_GearDamage = pd.DataFrame(df_GearDamage)
                Import_Lookup_df_GearType = pd.DataFrame(df_GearType)
                Import_Lookup_df_Quota = pd.DataFrame(df_Quota)
                Import_Lookup_df_SetType = pd.DataFrame(df_SetType)
                Import_Lookup_df_Species = pd.DataFrame(df_Species)
                Import_Lookup_df_VesselClass = pd.DataFrame(df_VesselClass)
                
                Import_Lookup_df_NAFODivision = pd.DataFrame(df_NAFODivision)
                Import_Lookup_df_NAFODivision['AlphaNAFODivision'] = (Import_Lookup_df_NAFODivision.loc[:,
                                            ['AlphaNAFODivision']]).fillna(9999999).astype(str, errors='ignore')
                Import_Lookup_df_NAFODivision['AlphaUnitArea'] = (Import_Lookup_df_NAFODivision.loc[:,
                                            ['AlphaUnitArea']]).fillna(9999999).astype(str, errors='ignore')
                Import_Lookup_df_NAFODivision['NumericNAFODivision'] = (Import_Lookup_df_NAFODivision.loc[:,
                                            ['NumericNAFODivision']]).fillna(9999999).astype(int, errors='ignore')
                Import_Lookup_df_NAFODivision['NumericUnitArea'] = (Import_Lookup_df_NAFODivision.loc[:,
                                            ['NumericUnitArea']]).fillna(9999999).astype(int, errors='ignore')
                Import_Lookup_df_NAFODivision = Import_Lookup_df_NAFODivision.replace('9999999', 'None')
                Import_Lookup_df_NAFODivision = Import_Lookup_df_NAFODivision.replace(9999999, '')

                RecordIdentifier_Get = 0
                Import_Lookup_df_ASOC.insert(loc=0, column="DatabaseUID", 
                                                value = np.arange(RecordIdentifier_Get, 
                                                len(Import_Lookup_df_ASOC) + RecordIdentifier_Get))
                Import_Lookup_df_Country.insert(loc=0, column="DatabaseUID", 
                                                value = np.arange(RecordIdentifier_Get, 
                                                len(Import_Lookup_df_Country) + RecordIdentifier_Get))

                Import_Lookup_df_DataSource.insert(loc=0, column="DatabaseUID", 
                                                value = np.arange(RecordIdentifier_Get, 
                                                len(Import_Lookup_df_DataSource) + RecordIdentifier_Get))
                Import_Lookup_df_GearDamage.insert(loc=0, column="DatabaseUID", 
                                                value = np.arange(RecordIdentifier_Get, 
                                                len(Import_Lookup_df_GearDamage) + RecordIdentifier_Get))
                Import_Lookup_df_GearType.insert(loc=0, column="DatabaseUID", 
                                                value = np.arange(RecordIdentifier_Get, 
                                                len(Import_Lookup_df_GearType) + RecordIdentifier_Get))
                Import_Lookup_df_Quota.insert(loc=0, column="DatabaseUID", 
                                                value = np.arange(RecordIdentifier_Get, 
                                                len(Import_Lookup_df_Quota) + RecordIdentifier_Get))

                Import_Lookup_df_SetType.insert(loc=0, column="DatabaseUID", 
                                                value = np.arange(RecordIdentifier_Get, 
                                                len(Import_Lookup_df_SetType) + RecordIdentifier_Get))
                Import_Lookup_df_Species.insert(loc=0, column="DatabaseUID", 
                                                value = np.arange(RecordIdentifier_Get, 
                                                len(Import_Lookup_df_Species) + RecordIdentifier_Get))
                Import_Lookup_df_VesselClass.insert(loc=0, column="DatabaseUID", 
                                                value = np.arange(RecordIdentifier_Get, 
                                                len(Import_Lookup_df_VesselClass) + RecordIdentifier_Get))
                Import_Lookup_df_NAFODivision.insert(loc=0, column="DatabaseUID", 
                                                value = np.arange(RecordIdentifier_Get, 
                                                len(Import_Lookup_df_NAFODivision) + RecordIdentifier_Get))
                
                sqliteConnection = sqlite3.connect(DB_Lookup_Table)
                cursor = sqliteConnection.cursor()
                Import_Lookup_df_ASOC.to_sql('DFO_NL_ASOP_ASOCCodeProfile', sqliteConnection, if_exists="replace", index =False)
                Import_Lookup_df_Country.to_sql('DFO_NL_ASOP_CountryProfile', sqliteConnection, if_exists="replace", index =False)
                Import_Lookup_df_DataSource.to_sql('DFO_NL_ASOP_DataSourceProfile', sqliteConnection, if_exists="replace", index =False)
                Import_Lookup_df_GearDamage.to_sql('DFO_NL_ASOP_GearDamageProfile', sqliteConnection, if_exists="replace", index =False)
                Import_Lookup_df_GearType.to_sql('DFO_NL_ASOP_GearTypeProfile', sqliteConnection, if_exists="replace", index =False)
                Import_Lookup_df_Quota.to_sql('DFO_NL_ASOP_QuotaProfile', sqliteConnection, if_exists="replace", index =False)
                Import_Lookup_df_SetType.to_sql('DFO_NL_ASOP_SetTypeProfile', sqliteConnection, if_exists="replace", index =False)
                Import_Lookup_df_Species.to_sql('DFO_NL_ASOP_SpeciesCodeProfile', sqliteConnection, if_exists="replace", index =False)
                Import_Lookup_df_VesselClass.to_sql('DFO_NL_ASOP_VesselClassProfile', sqliteConnection, if_exists="replace", index =False)
                Import_Lookup_df_NAFODivision.to_sql('DFO_NL_ASOP_NAFODivisionProfile', sqliteConnection, if_exists="replace", index =False)
                sqliteConnection.commit()
            except sqlite3.Error as error:
                print('Error occured - ', error)
            finally:
                if sqliteConnection:
                    cursor.close()
                    sqliteConnection.close()
                    messagebox.showinfo('DFO-NL-ASOP LookUp Table Message', 
                                "Successfully Generated And Stored All DFO-NL-ASOP LookUp Tables From Archived")
        else:
            messagebox.showerror('DFO-NL-ASOP LookUp Table Message', 
                                "Void DFO-NL-ASOP LookUp Table... One Or More Void LookUp Table In The Archived Folder, Name - CSV_FilesFor_Import_LookupTable")
    except:
        messagebox.showerror('DFO-NL-ASOP LookUp Table Generation Error Message', 
                            "Void DFO-NL-ASOP LookUp Table... One Or More LookUp Table Missing In The Archived Folder, Name - CSV_FilesFor_Import_LookupTable")

def DFO_NL_ASOP_Clear_All_LookupTables():
    DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")
    try:
        conn = sqlite3.connect(DB_Lookup_Table)
        cur=conn.cursor()
        cur.execute("DELETE FROM DFO_NL_ASOP_ASOCCodeProfile")
        cur.execute("DELETE FROM DFO_NL_ASOP_CountryProfile")
        cur.execute("DELETE FROM DFO_NL_ASOP_DataSourceProfile")
        cur.execute("DELETE FROM DFO_NL_ASOP_GearDamageProfile")
        cur.execute("DELETE FROM DFO_NL_ASOP_GearTypeProfile")
        cur.execute("DELETE FROM DFO_NL_ASOP_QuotaProfile")
        cur.execute("DELETE FROM DFO_NL_ASOP_SetTypeProfile")
        cur.execute("DELETE FROM DFO_NL_ASOP_SpeciesCodeProfile")
        cur.execute("DELETE FROM DFO_NL_ASOP_VesselClassProfile")
        cur.execute("DELETE FROM DFO_NL_ASOP_NAFODivisionProfile")
        conn.commit()
    except sqlite3.Error as error:
        print('Error occured - ', error)
        tkinter.messagebox.showinfo("DFO-NL-ASOP LookUp Table Message","DFO-NL-ASOP LookUp Tables Are Already Cleared")
    finally:
        if conn:
            cur.close()
            conn.close()
            tkinter.messagebox.showinfo("DFO-NL-ASOP LookUp Table Message","DFO-NL-ASOP LookUp Tables Are cleared")




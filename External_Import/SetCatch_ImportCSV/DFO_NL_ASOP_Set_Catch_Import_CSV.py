from tkinter import *
import tkinter.messagebox
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, filedialog
import numpy as np
import pandas as pd
import sqlite3
import functools
import os
import pickle

## Defining DB Path
DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
DB_SetCatch_Validation_LookUpTable = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")
Pickle_FileNameImport ="./Pickle_MetaData/ImportFileName.pickle"
DB_Set_Catch_Misc = ("./BackEnd/Sqlite3_DB/SetCatch_Misc_DB/DFO_NL_ASOP_Set_Catch_Misc.db")

## Import ImportQC Fail View 
from External_Import.SetCatch_ImportCSV import DFO_NL_ASOP_Set_Catch_Import_QCFailView

def Observer_Set_Catch_LogIMPORT():
    root=tk.Tk()
    root.title ("Observer Set & Catch External Import - A")
    root.geometry('1100x700+200+200')
    root.config(bg="cadet blue")

    Topframe = Frame(root, bd = 2, padx= 3, pady= 2, relief = RIDGE, bg= "aliceblue")
    Topframe.pack(side = TOP)

    lbl_Total_ImportedEntries = Label(Topframe, font=('aerial', 10, 'bold'), 
                                    bg= "aliceblue", text="Total Imported Entries :")
    lbl_Total_ImportedEntries.grid(row =0, column = 0, padx=8, pady =2)

    entry_Total_ImportedEntries = Entry(Topframe, font=('aerial', 12, 'bold'), 
                                        textvariable = IntVar(), width = 8, 
                                        bd=2, justify ='center')
    entry_Total_ImportedEntries.grid(row =0, column = 1, padx=10, pady =2)

    frame = tk.Frame(root, bg= "aliceblue")
    frame.pack(side = TOP, pady=0)

    tree = ttk.Treeview(frame, height=14, selectmode ='browse')
    scrollbary = ttk.Scrollbar(frame, orient ="vertical", command=tree.yview)
    scrollbary.pack(side ='right', fill ='y')
    tree.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(frame, orient ="horizontal", command=tree.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    tree.configure(xscrollcommand = scrollbarx.set)

    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 8), foreground="blue")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 8,'bold'), 
                    background='Ghost White', foreground='blue',
                    fieldbackground='Ghost White')
    tree.pack(side = TOP)

    BottomFrame = Frame(frame, bd = 2, padx= 10, pady= 2, relief = RIDGE, bg= "aliceblue")
    BottomFrame.pack(side = TOP)
    lbl_RecordIdentifier = Label(BottomFrame, font=('aerial', 12, 'bold'), 
                                text="Record Identifier Start Value")
    lbl_RecordIdentifier.grid(row =0, column = 0, padx=10, pady =2)
    entry_RecordIdentifier = Entry(BottomFrame, font=('aerial', 12, 'bold'), 
                                textvariable = IntVar(), width = 8,
                                bd=2, justify ='center')
    entry_RecordIdentifier.grid(row =1, column = 0)

    ## Defining Functions
    def Clear_DB_SetCatch_Validation_LookUpTable():
        try:
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
            cursor = sqliteConnection.cursor()
            cursor.execute("DELETE FROM SetCatch_QCFailedLookUpTable_ASOCCode")
            cursor.execute("DELETE FROM SetCatch_QCFailedLookUpTable_Country")
            cursor.execute("DELETE FROM SetCatch_QCFailedLookUpTable_DataSource")
            cursor.execute("DELETE FROM SetCatch_QCFailedLookUpTable_GearDamage")
            cursor.execute("DELETE FROM SetCatch_QCFailedLookUpTable_GearType")
            cursor.execute("DELETE FROM SetCatch_QCFailedLookUpTable_Quota")
            cursor.execute("DELETE FROM SetCatch_QCFailedLookUpTable_SetType")
            cursor.execute("DELETE FROM SetCatch_QCFailedLookUpTable_SpeciesCode")
            cursor.execute("DELETE FROM SetCatch_QCFailedLookUpTable_DirectedSpecies")
            cursor.execute("DELETE FROM SetCatch_QCFailedLookUpTable_VesselClass")
            cursor.execute("DELETE FROM SetCatch_QCFailedLookUpTable_NAFODivision")
            cursor.execute("DELETE FROM SetCatch_QCFailedLookUpTable_UnitArea")
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def Clear_DB_SetCatch_MiscDB():
        try:
            sqliteConnection = sqlite3.connect(DB_Set_Catch_Misc)
            cursor = sqliteConnection.cursor()
            cursor.execute("DELETE FROM DFO_NL_ASOP_SetCatch_TombstoneQCFailOnImport")
            cursor.execute("DELETE FROM DFO_NL_ASOP_SetCatch_DuplicateQCFailOnImport")
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def TreeView_DataFrame():
        dfList =[] 
        for child in tree.get_children():
            df = tree.item(child)["values"]
            dfList.append(df)
        ListBox_DF = pd.DataFrame(dfList)
        Len_ListBox_DF = len (ListBox_DF)
        return Len_ListBox_DF

    def TempImport_To_DBStorage(Raw_Imported_Df):
        try:
            TempImport_To_DBStorage = pd.DataFrame(Raw_Imported_Df)
            sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = sqliteConnection.cursor()
            TempImport_To_DBStorage.to_sql('DFO_NL_ASOP_Set_Catch_TEMP_IMPORT', sqliteConnection, if_exists="replace",index = False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def SubmitImport_To_QC_DBStorage():
        Len_ListBox_DF = TreeView_DataFrame()
        entry_ImportedFileName_Get = entry_ImportedFileName.get()
        with open(Pickle_FileNameImport, 'wb') as f:
            pickle.dump(entry_ImportedFileName_Get, f)
        if Len_ListBox_DF >0:
            iSubmit = tkinter.messagebox.askyesno("Submit DFO-NL ASOP Set & Catch Data Import",
                        "Confirm If You Want to Submit DFO-NL ASOP Set & Catch Data Import To QC Database ?")
            if iSubmit >0:
                try:
                    sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
                    cursor = sqliteConnection.cursor()
                    Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_TEMP_IMPORT ORDER BY `RecordIdentifier` ASC ;", sqliteConnection)
                    Complete_df.sort_values(by=['Year', 'ASOCCode', 'DeploymentNumber', 'SetNumber'], ascending=True, inplace=True)
                    data = pd.DataFrame(Complete_df)
                    data = data.reset_index(drop=True)
                    data.to_sql('DFO_NL_ASOP_Set_Catch_Analysis_IMPORT', sqliteConnection, if_exists="replace",index_label='DataBase_ID')
                    sqliteConnection.commit()
                except sqlite3.Error as error:
                    print('Error occured - ', error)
                finally:
                    if sqliteConnection:
                        cursor.execute("DELETE FROM DFO_NL_ASOP_Set_Catch_TEMP_IMPORT")
                        cursor.close()
                        sqliteConnection.close()
                        Clear_DB_SetCatch_Validation_LookUpTable()
                        Clear_DB_SetCatch_MiscDB()
                        Reset()
                        tkinter.messagebox.showinfo("Submit DFO-NL ASOP Set & Catch Data Import"," Submit Confirmed DFO-NL ASOP Set & Catch Data Import To QC Database")

    def iExit():
        iExit= tkinter.messagebox.askyesno("Observer Set & Catch Datasheet Import Widget", "Confirm If You Want To Exit")
        if iExit >0:
            root.destroy()
            return

    def ClearTextBox():
        tree.delete(*tree.get_children())
        entry_Total_ImportedEntries.delete(0,END)
        entry_ImportedFileName.delete(0,END)
        entry_DuplicatedEntries.delete(0,END)
        entry_TombCheckFail.delete(0,END)

    def Reset():
        ClearTextBox()
        try:
            entry_RecordIdentifier.delete(0,END)
            RecordIdentifier_Get = 0
            entry_RecordIdentifier.insert(tk.END,RecordIdentifier_Get)
        except:
            RecordIdentifier_Get = 0
            entry_RecordIdentifier.insert(tk.END,RecordIdentifier_Get)
        entry_Total_ImportedEntries.insert(tk.END,0)

    def ImportColumnCheck(List_Columns_Import):
        ReturnMatchedMessage    = "Import Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Headers MisMatch With Database Headers"
        DB_column_names = ['ASOCCode', 'ObserverNumber', 'Year', 'DeploymentNumber', 'SubTripNumber',
                        'SetNumber', 'Country', 'Quota', 'SetType', 'VesselSideNumber',
                        'VesselClass', 'VesselLength', 'VesselHorsepower', 'Day', 'Month', 
                        'HaulDay','HaulMonth', 'StartTime', 'Duration', 'PositionPrecision',
                        'StartLatitude', 'StartLongitude', 'EndLatitude', 'EndLongitude', 'NAFODivision',
                        'UnitArea', 'StatisticalArea', 'InOut200MileLimit', 'GearType', 'CodendMeshSize',
                        'MeshSizeMG', 'MeshSizeFG', 'RollerBobbbinDiameter', 'NumberGillnets', 'AverageGillnetLength', 
                        'GrateBarSpacing', 'FootropeLength','NumberWindows', 'NumberHooks', 'NumberPots', 
                        'NumberPotReleasedCrab', 'GearDamage', 'AverageTowSpeed', 'AverageDepth', 'DataSource', 
                        'DirectedSpecies', 'NumberSpecies', 'RecordType', 'DetailedCatchSpeciesCompCode', 'LogbookIDNumber1', 
                        'LogbookIDNumber2', 'SpeciesCode', 'KeptWeight', 'DiscardWeight', 
                        'EstimatedWeightReleasedCrab', 'NumberIndividuals']
        if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,DB_column_names,List_Columns_Import), True): 
            return ReturnMatchedMessage
        else: 
            return ReturnMisMatchedMessage 

    def Import_Set_Catch_CSV():
        ReturnMatchedMessage    = "Import Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Headers MisMatch With Database Headers"
        fileList = filedialog.askopenfilenames(title="Select Set & Catch .CSV File/Files", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.")))
        Length_fileList  =  len(fileList)
        if Length_fileList >0:
            if fileList:
                dfList =[]
                basename =[]
                for filename in fileList:
                    if filename.endswith('.csv'):
                        filename = r"{}".format(filename)
                        Basefile = os.path.basename(filename)
                        basename.append(Basefile + ',')
                        df = pd.read_csv(filename, sep=',' , low_memory=False)
                        List_Columns_Import = list(df.columns)
                        Return_Message = ImportColumnCheck(List_Columns_Import)
                        if Return_Message == ReturnMatchedMessage:
                            df = df.iloc[:,:]
                            ASOCCode                    = (df.loc[:,'ASOCCode']).fillna(99999999).astype(int, errors='ignore')
                            ObserverNumber              = (df.loc[:,'ObserverNumber']).fillna(8888888).astype(int, errors='ignore')
                            Year                        = (df.loc[:,'Year']).fillna(99999999).astype(int, errors='ignore')
                            DeploymentNumber            = (df.loc[:,'DeploymentNumber']).fillna(99999999).astype(int, errors='ignore')
                            SubTripNumber               = (df.loc[:,'SubTripNumber']).fillna(8888888).astype(int, errors='ignore')
                            SetNumber                   = (df.loc[:,'SetNumber']).fillna(99999999).astype(int, errors='ignore')
                            Country                     = (df.loc[:,'Country']).fillna(99999999).astype(int, errors='ignore')
                            Quota                       = (df.loc[:,'Quota']).fillna(99999999).astype(int, errors='ignore')
                            SetType                     = (df.loc[:,'SetType']).fillna(99999999).astype(int, errors='ignore')                
                            VesselSideNumber            = (df.loc[:,'VesselSideNumber']).fillna(8888888).astype(int, errors='ignore')
                            VesselClass                 = (df.loc[:,'VesselClass']).fillna(99999999).astype(int, errors='ignore')
                            VesselLength                = (df.loc[:,'VesselLength']).fillna(99999999).astype(float, errors='ignore')
                            VesselHorsepower            = (df.loc[:,'VesselHorsepower']).fillna(99999999).astype(int, errors='ignore')
                            Day                         = (df.loc[:,'Day']).fillna(99999999).astype(int, errors='ignore')
                            Month                       = (df.loc[:,'Month']).fillna(99999999).astype(int, errors='ignore')
                            HaulDay                     = (df.loc[:,'HaulDay']).fillna(99999999).astype(int, errors='ignore')
                            HaulMonth                   = (df.loc[:,'HaulMonth']).fillna(99999999).astype(int, errors='ignore')
                            StartTime                   = (df.loc[:,'StartTime']).fillna(99999999).astype(int, errors='ignore')
                            Duration                    = (df.loc[:,'Duration']).fillna(99999999).astype(float, errors='ignore')
                            PositionPrecision           = (df.loc[:,'PositionPrecision']).fillna(99999999).astype(int, errors='ignore')
                            StartLatitude               = (df.loc[:,'StartLatitude']).fillna(99999999).astype(float, errors='ignore')
                            StartLongitude               = (df.loc[:,'StartLongitude']).fillna(99999999).astype(float, errors='ignore')
                            EndLatitude                 = (df.loc[:,'EndLatitude']).fillna(99999999).astype(float, errors='ignore')
                            EndLongitude                = (df.loc[:,'EndLongitude']).fillna(99999999).astype(float, errors='ignore')
                            NAFODivision                = (df.loc[:,'NAFODivision']).fillna(8888888).astype(int, errors='ignore')
                            UnitArea                    = (df.loc[:,'UnitArea']).fillna(8888888).astype(int, errors='ignore')
                            StatisticalArea             = (df.loc[:,'StatisticalArea']).fillna(8888888).astype(int, errors='ignore')
                            InOut200MileLimit           = (df.loc[:,'InOut200MileLimit']).fillna(99999999).astype(int, errors='ignore')
                            GearType                    = (df.loc[:,'GearType']).fillna(99999999).astype(int, errors='ignore')
                            CodendMeshSize              = (df.loc[:,'CodendMeshSize']).fillna(99999999).astype(int, errors='ignore')
                            MeshSizeMG                  = (df.loc[:,'MeshSizeMG']).fillna(99999999).astype(int, errors='ignore')
                            MeshSizeFG                  = (df.loc[:,'MeshSizeFG']).fillna(99999999).astype(int, errors='ignore')
                            RollerBobbbinDiameter       = (df.loc[:,'RollerBobbbinDiameter']).fillna(99999999).astype(int, errors='ignore')
                            NumberGillnets              = (df.loc[:,'NumberGillnets']).fillna(99999999).astype(int, errors='ignore')
                            AverageGillnetLength        = (df.loc[:,'AverageGillnetLength']).fillna(99999999).astype(int, errors='ignore')
                            GrateBarSpacing             = (df.loc[:,'GrateBarSpacing']).fillna(99999999).astype(int, errors='ignore')
                            FootropeLength              = (df.loc[:,'FootropeLength']).fillna(99999999).astype(int, errors='ignore')
                            NumberWindows               = (df.loc[:,'NumberWindows']).fillna(99999999).astype(int, errors='ignore')
                            NumberHooks                 = (df.loc[:,'NumberHooks']).fillna(99999999).astype(int, errors='ignore')
                            NumberPots                  = (df.loc[:,'NumberPots']).fillna(99999999).astype(int, errors='ignore')
                            NumberPotReleasedCrab       = (df.loc[:,'NumberPotReleasedCrab']).fillna(99999999).astype(int, errors='ignore')
                            GearDamage                  = (df.loc[:,'GearDamage']).fillna(99999999).astype(int, errors='ignore')
                            AverageTowSpeed             = (df.loc[:,'AverageTowSpeed']).fillna(99999999).astype(float, errors='ignore')
                            AverageDepth                = (df.loc[:,'AverageDepth']).fillna(99999999).astype(int, errors='ignore')
                            DataSource                  = (df.loc[:,'DataSource']).fillna(99999999).astype(int, errors='ignore')
                            DirectedSpecies             = (df.loc[:,'DirectedSpecies']).fillna(99999999).astype(int, errors='ignore')
                            NumberSpecies               = (df.loc[:,'NumberSpecies']).fillna(99999999).astype(int, errors='ignore')
                            RecordType                  = (df.loc[:,'RecordType']).fillna(99999999).astype(int, errors='ignore')
                            DetailedCatchSpeciesCompCode= (df.loc[:,'DetailedCatchSpeciesCompCode']).fillna(8888888).astype(int, errors='ignore')
                            LogbookIDNumber1            = (df.loc[:,'LogbookIDNumber1']).fillna(99999999).astype(int, errors='ignore')
                            LogbookIDNumber2            = (df.loc[:,'LogbookIDNumber2']).fillna(99999999).astype(int, errors='ignore')
                            SpeciesCode                 = (df.loc[:,'SpeciesCode']).fillna(99999999).astype(int, errors='ignore')
                            KeptWeight                  = (df.loc[:,'KeptWeight']).fillna(99999999).astype(int, errors='ignore')
                            DiscardWeight               = (df.loc[:,'DiscardWeight']).fillna(99999999).astype(int, errors='ignore')
                            EstimatedWeightReleasedCrab = (df.loc[:,'EstimatedWeightReleasedCrab']).fillna(99999999).astype(int, errors='ignore')
                            NumberIndividuals           = (df.loc[:,'NumberIndividuals']).fillna(99999999).astype(int, errors='ignore')

                            column_names = [ASOCCode, ObserverNumber, Year, DeploymentNumber, SubTripNumber, SetNumber, Country, Quota, 
                                            SetType, VesselSideNumber, VesselClass, VesselLength, VesselHorsepower, Day, Month, HaulDay, HaulMonth, 
                                            StartTime, Duration, PositionPrecision, StartLatitude, StartLongitude, EndLatitude, EndLongitude, NAFODivision, 
                                            UnitArea, StatisticalArea, InOut200MileLimit, GearType, CodendMeshSize, MeshSizeMG, MeshSizeFG, RollerBobbbinDiameter,
                                            NumberGillnets, AverageGillnetLength, GrateBarSpacing, FootropeLength, NumberWindows, NumberHooks, NumberPots, NumberPotReleasedCrab, 
                                            GearDamage, AverageTowSpeed, AverageDepth, DataSource, DirectedSpecies, NumberSpecies, RecordType,
                                            DetailedCatchSpeciesCompCode, LogbookIDNumber1, LogbookIDNumber2, SpeciesCode, KeptWeight, DiscardWeight, EstimatedWeightReleasedCrab,
                                            NumberIndividuals]
                            catdf = pd.concat (column_names,axis=1,ignore_index =True)
                            dfList.append(catdf)
                        else:
                            messagebox.showerror('Import File Headers Mismatch', ReturnMisMatchedMessage)
                if Return_Message == ReturnMatchedMessage:
                    concatDf = pd.concat(dfList,axis=0, ignore_index =True)
                    concatDf.rename(columns={0:'ASOCCode', 1:'ObserverNumber', 2:'Year', 3:'DeploymentNumber', 4:'SubTripNumber', 
                                            5:'SetNumber', 6:'Country', 7:'Quota', 8:'SetType', 9:'VesselSideNumber', 
                                            10:'VesselClass', 11:'VesselLength', 12:'VesselHorsepower', 13:'Day', 14:'Month', 
                                            15:'HaulDay', 16:'HaulMonth', 17:'StartTime', 18:'Duration', 19:'PositionPrecision',
                                            20:'StartLatitude', 21:'StartLongitude', 22:'EndLatitude', 23:'EndLongitude', 24:'NAFODivision', 
                                            25:'UnitArea', 26:'StatisticalArea', 27:'InOut200MileLimit', 28:'GearType',
                                            29:'CodendMeshSize', 30:'MeshSizeMG', 31:'MeshSizeFG', 32:'RollerBobbbinDiameter', 33:'NumberGillnets',
                                            34:'AverageGillnetLength', 35:'GrateBarSpacing', 36:'FootropeLength', 37:'NumberWindows', 38:'NumberHooks',
                                            39:'NumberPots', 40:'NumberPotReleasedCrab', 41:'GearDamage', 42:'AverageTowSpeed', 43:'AverageDepth',
                                            44:'DataSource', 45:'DirectedSpecies', 46:'NumberSpecies', 47:'RecordType', 48:'DetailedCatchSpeciesCompCode',
                                            49:'LogbookIDNumber1', 50:'LogbookIDNumber2', 51:'SpeciesCode', 52:'KeptWeight', 53:'DiscardWeight', 
                                            54:'EstimatedWeightReleasedCrab', 55:'NumberIndividuals'},inplace = True)
                    
                    Raw_Imported_Df = pd.DataFrame(concatDf)
                    Len_Raw_Imported_Df = len(Raw_Imported_Df)
                    
                    if(len(entry_RecordIdentifier.get())!=0):
                        RecordIdentifier_Get         = entry_RecordIdentifier.get()
                    else:
                        RecordIdentifier_Get = 0
                        entry_RecordIdentifier.insert(tk.END,RecordIdentifier_Get)               
                    
                    Raw_Imported_Df = Raw_Imported_Df.replace(np.nan, '')
                    Raw_Imported_Df = Raw_Imported_Df.replace('     ', 9999999)
                    Raw_Imported_Df = Raw_Imported_Df.replace(' ', 99999999)
                    Raw_Imported_Df = Raw_Imported_Df.replace('  ', 99999999)
                    Raw_Imported_Df = Raw_Imported_Df.replace('   ', 99999999)
                    Raw_Imported_Df = Raw_Imported_Df.replace('    ', 99999999)
                    Raw_Imported_Df = Raw_Imported_Df.replace([99999999, 99999999.0, '.'], '')
                    Raw_Imported_Df = Raw_Imported_Df.replace([8888888, '8888888', '.'], 'None')

                    Raw_Imported_Df['DeploymentUID'] = Raw_Imported_Df["Year"].map(str) + "-" + \
                                                        Raw_Imported_Df["ASOCCode"].map(str)+ "-" +\
                                                        Raw_Imported_Df["DeploymentNumber"].map(str)+"-"+ \
                                                        Raw_Imported_Df["SetNumber"].map(str)
                    Raw_Imported_Df = Raw_Imported_Df[['DeploymentUID'] + [x for x in Raw_Imported_Df.columns if x != 'DeploymentUID']]

                    RecordIdentifier_Get         = int(RecordIdentifier_Get)
                    Raw_Imported_Df.insert(loc=0, column="RecordIdentifier", 
                        value = np.arange(RecordIdentifier_Get, Len_Raw_Imported_Df + RecordIdentifier_Get))

                    List_Columns = list(Raw_Imported_Df.columns)
                    tree['column'] = List_Columns
                    tree['show'] = "headings"
                    ClearTextBox()
                    TempImport_To_DBStorage(Raw_Imported_Df)
                    entry_Total_ImportedEntries.insert(tk.END,Len_Raw_Imported_Df)
                    entry_ImportedFileName.insert(tk.END,basename )

                    for col in tree['column']:
                        tree.heading(col, text=col, anchor = tk.CENTER)
                        tree.column(col, stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)
                    df_rows = Raw_Imported_Df.to_numpy().tolist()
                    countIndex = 0
                    for row in df_rows:
                        if countIndex % 2 == 0:
                            tree.insert("", "end", values =row, tags =("even",))
                        else:
                            tree.insert("", "end", values =row, tags =("odd",))
                        countIndex = countIndex+1
                    tree.tag_configure("even",foreground="black", background="lightblue")
                    tree.tag_configure("odd",foreground="black", background="ghost white")

    def GetImportForTombstoneCheck():
        try:
            sqliteConnection = sqlite3.connect(DB_Set_Catch_Analysis)
            cursor = sqliteConnection.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_Set_Catch_TEMP_IMPORT", sqliteConnection)
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
    
    def PerformTombstoneCheck():
        GetImportedData = GetImportForTombstoneCheck()
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
            CheckforDuplicatedDepUID(GetImportedData_Rec_1)
            
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
            String_QCFail = 'Total Tombstone Fail Found : ' + str(TombQCFailedTotalEntries)
            entry_TombCheckFail.delete(0,END)
            entry_TombCheckFail.insert(tk.END,String_QCFail)        
        
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
        DuplicatedQCFailedTotalEntries = len(DuplicatedQCFailedDF)
        String_QCFail = 'Total Duplicate UID Found : ' + str(DuplicatedQCFailedTotalEntries)
        entry_DuplicatedEntries.delete(0,END)
        entry_DuplicatedEntries.insert(tk.END,String_QCFail)        

    ## All Buttons And Functions
    ButtonFrame = Frame(root, bd = 2, padx= 1, pady= 2, relief = RIDGE, bg='cadet blue')
    ButtonFrame.pack(side = TOP)
    
    ## Import And Perform Tombstone Check
    button_Import_Set_Catch_CSV = Button(ButtonFrame, bd = 2, text ="Import Observer Set & Catch CSV File", width = 32,
                                height=2, font=28, fg="white", bg="#0078d7", command = Import_Set_Catch_CSV)
    button_Import_Set_Catch_CSV.grid (row =0, column =0, padx=2, pady =2)

    button_PerTombCheck = Button(ButtonFrame, bd = 2, text ="Perform Tombstone Check On Import", width = 32,
                                height=2, font=28, fg="white", bg="#0078d7", command =PerformTombstoneCheck)
    button_PerTombCheck.grid(row =0, column =1, padx=2, pady =2)

    ## Imported Filename
    lbl_ImportedFileName = Label(ButtonFrame, font=('aerial', 12), bg='cadet blue', fg="white",
                                text="Imported Set & Catch File Name (.csv) : ")
    lbl_ImportedFileName.grid(row =1, column = 0, padx=20, pady =4)
    entry_ImportedFileName = Entry(ButtonFrame, font=('aerial', 12, 'bold'), textvariable = StringVar(), width = 32, bd=2)
    entry_ImportedFileName.grid(row =1, column = 1, padx=1, pady=4, ipady =4)

    ## Total QC Failed Found
    EntryDuplicatedEntries = IntVar(ButtonFrame, value ='Total Duplicate UID Found: ')
    entry_DuplicatedEntries = Entry(ButtonFrame, font=('aerial', 10, 'bold'), 
                              textvariable = EntryDuplicatedEntries, width = 40, bd=2)
    entry_DuplicatedEntries.grid(row =2, column = 0, padx=1, pady=2, ipadx =4, ipady =4)

    EntryTombCheckFail = IntVar(ButtonFrame, value ='Total Tombstone Fail Found: ')
    entry_TombCheckFail = Entry(ButtonFrame, font=('aerial', 10, 'bold'), 
                              textvariable = EntryTombCheckFail, width = 40, bd=2)
    entry_TombCheckFail.grid(row =2, column = 1, padx=1, pady=2, ipadx =4, ipady =4)

    ## View QC Results
    button_ViewQCFail = Button(ButtonFrame, bd = 2, text ="View & Edit QC Fail Summary", width = 30,
                        height=2, font=28, fg="white", bg="#0078d7", 
                        command =DFO_NL_ASOP_Set_Catch_Import_QCFailView.ViewImportQCFailResult)
    button_ViewQCFail.grid(row =3, column =0, padx=2, pady =2, columnspan = 2)

    ## Submit To Setcatch DB
    button_Submit_Import_DB = Button(ButtonFrame, bd = 2, text ="Submit Import To QC Database", width = 30,
                                height=2, font=28, fg="white", bg="#0078d7", command =SubmitImport_To_QC_DBStorage)
    button_Submit_Import_DB.grid(row =5, column =0, padx=2, pady =4, columnspan = 2)

    ## Adding File Menu 
    menu = Menu(root)
    root.config(menu=menu)
    filemenu  = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=filemenu)  
    filemenu.add_command(label="Exit", command=iExit)
    filemenu.add_command(label="Reset", command=Reset)
    root.mainloop()


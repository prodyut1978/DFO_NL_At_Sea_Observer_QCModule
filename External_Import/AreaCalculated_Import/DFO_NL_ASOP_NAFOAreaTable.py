#Front End
from tkinter import*
import tkinter.messagebox
from tkinter import ttk, filedialog
from tkinter import messagebox
import tkinter as tk
import sqlite3
import pandas as pd
import numpy as np
import functools
import datetime

## Defing DB Connections & Path For Archived CSV
Path_CSV_NAFOBoundary = './External_Import/AreaCalculated_Import/CSV_AreaProfile/DFO_NL_ASOP_NAFOAreaProfile.csv'
DB_SetCatch_Val_Calculation = ("./BackEnd/Sqlite3_DB/QC_Check_CalculationConsistency_DB/DFO_NL_ASOP_SetCatch_Calculation.db")

def DFO_NL_ASOP_NAFOProfile():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP Set & Catch NAFO Profile")
    window.geometry("1180x710+200+100")
    window.config(bg="cadet blue")
    window.resizable(0, 0)
    
    ## Defining Main Frame
    MainFrame = Frame(window, bd = 2, padx= 2, pady= 1, relief = RIDGE)
    MainFrame.grid(row =0, column = 0, padx=2, pady =1, sticky =W, rowspan =1)

    ## Defining Top Left frame - A
    Topframe = Frame(MainFrame, bd = 2, padx= 3, pady= 10, relief = RIDGE)
    Topframe.grid(row =0, column = 0, padx=140, pady =1, sticky =W, rowspan =1, columnspan =1)
    VariablesID = IntVar(Topframe, value='')
    NAFOSubArea = StringVar()
    NAFODiv = StringVar()
    NAFOSubDiv = StringVar()
    NAFOLabel = StringVar()
    NAFOPointOrder = StringVar()
    NAFO_Lat = ''
    NAFO_Lon = ''
    
    lblTopLeftFrame = Label(Topframe, font=('aerial', 12, 'bold'), text="A. NAFO Area Profile:")
    lblTopLeftFrame.grid(row =0, column = 0, padx=0, pady =2, sticky =W, rowspan =1)

    lblVariablesID = Label(Topframe, font=('aerial', 10, 'bold'), text = "1. VariablesID :", padx =0, pady= 2)
    lblVariablesID.grid(row =2, column = 0, padx=0, pady =2, sticky =W)
    txtVariablesID  = Entry(Topframe, font=('aerial', 12, 'bold'),state=DISABLED, textvariable= VariablesID, width = 6)
    txtVariablesID.grid(row =2, column = 1, padx=1, pady =10, sticky =W)

    lblNAFOSubArea = Label(Topframe, font=('aerial', 10, 'bold'), text = "2. NAFO SubArea :", padx =0, pady= 2)
    lblNAFOSubArea.grid(row =3, column = 0, padx=0, pady =2, sticky =W)
    txtNAFOSubArea  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable= NAFOSubArea, width = 6)
    txtNAFOSubArea.grid(row =3, column = 1, padx=1, pady =10, sticky =W)

    lblNAFODivision = Label(Topframe, font=('aerial', 10, 'bold'), text = "3. NAFO Division :", padx =0, pady= 2)
    lblNAFODivision.grid(row =2, column = 2, padx=4, pady =2, sticky =W)
    txtNAFODivision  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable= NAFODiv, width = 6)
    txtNAFODivision.grid(row =2, column = 3, padx=5, pady =10, sticky =W)

    lblNAFOSubDivision = Label(Topframe, font=('aerial', 10, 'bold'), text = "4. NAFO SubDivision :", padx =0, pady= 2)
    lblNAFOSubDivision.grid(row =3, column = 2, padx=4, pady =2, sticky =W)
    txtNAFOSubDivision  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable= NAFOSubDiv, width = 6)
    txtNAFOSubDivision.grid(row =3, column = 3, padx=5, pady =10, sticky =W)

    lblNAFOLabel = Label(Topframe, font=('aerial', 10, 'bold'), text = "5. NAFO Label :", padx =0, pady= 2)
    lblNAFOLabel.grid(row =2, column = 4, padx=4, pady =2, sticky =W)
    txtNAFOLabel  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable= NAFOLabel, width = 6)
    txtNAFOLabel.grid(row =2, column = 5, padx=5, pady =10, sticky =W)

    lblNAFOPointOrder = Label(Topframe, font=('aerial', 10, 'bold'), text = "6. NAFO PointOrder :", padx =0, pady= 2)
    lblNAFOPointOrder.grid(row =3, column = 4, padx=4, pady =2, sticky =W)
    txtNAFOPointOrder  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable= NAFOPointOrder, width = 6)
    txtNAFOPointOrder.grid(row =3, column = 5, padx=5, pady =10, sticky =W)

    lblNAFO_Latitude = Label(Topframe, font=('aerial', 10, 'bold'), text = "7. NAFO Latitude :", padx =0, pady= 2)
    lblNAFO_Latitude.grid(row =2, column = 6, padx=4, pady =2, sticky =W)
    txtNAFO_Latitude  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable = NAFO_Lat, width = 10)
    txtNAFO_Latitude.grid(row =2, column = 7, padx=1, pady =10, sticky =W)

    lblNAFO_Longitude = Label(Topframe, font=('aerial', 10, 'bold'), text = "8. NAFO Longitude :", padx =0, pady= 2)
    lblNAFO_Longitude.grid(row =3, column = 6, padx=4, pady =2, sticky =W)
    txtNAFO_Longitude  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable = NAFO_Lon, width = 10)
    txtNAFO_Longitude.grid(row =3, column = 7, padx=1, pady =10, sticky =W)

    ## Defing Bottom - Tree Frame
    BottomFrame = Frame(MainFrame, bd = 2, padx= 1, pady= 10, relief = RIDGE)
    BottomFrame.grid(row =1, column = 0, padx=1, pady =1, sticky =W, rowspan =1, columnspan =1)

    lblBottomFrame = Label(BottomFrame, font=('aerial', 12, 'bold'), text="B. NAFO Area Profile Table:")
    lblBottomFrame.grid(row =0, column = 0, padx=5, pady =2, sticky =W, rowspan =1)

    TableMargin1 = Frame(BottomFrame, bd = 2, padx= 10, pady= 2, relief = RIDGE)
    TableMargin1.grid(row =1, column = 0, padx=1, pady =1, sticky =W, rowspan =1, columnspan =1)
    tree1 = ttk.Treeview(TableMargin1, 
            column=("column1", "column2", "column3", "column4",
                    "column5", "column6", "column7", "column8"), 
            height=20, show='headings')
    scrollbary = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
    scrollbary.pack(side ='right', fill ='y')
    tree1.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    tree1.configure(xscrollcommand = scrollbarx.set)
    tree1.heading("#1", text="NAFO_ID", anchor=tk.CENTER)
    tree1.heading("#2", text="NAFOSubArea", anchor=tk.CENTER)
    tree1.heading("#3", text="NAFODivision", anchor=tk.CENTER)
    tree1.heading("#4", text="NAFOSubDivision", anchor=tk.CENTER)
    tree1.heading("#5", text="NAFOLabel", anchor=tk.CENTER)
    tree1.heading("#6", text="NAFOPointOrder", anchor=tk.CENTER)
    tree1.heading("#7", text="NAFO Latitude", anchor=tk.CENTER)
    tree1.heading("#8", text="NAFO Longitude", anchor=tk.CENTER)
    
    tree1.column('#1', stretch=NO, minwidth=0, width=80, anchor=tk.CENTER)            
    tree1.column('#2', stretch=NO, minwidth=0, width=150, anchor=tk.CENTER)
    tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor=tk.CENTER)
    tree1.column('#4', stretch=NO, minwidth=0, width=150, anchor=tk.CENTER)
    tree1.column('#5', stretch=NO, minwidth=0, width=150, anchor=tk.CENTER)            
    tree1.column('#6', stretch=NO, minwidth=0, width=150, anchor=tk.CENTER)
    tree1.column('#7', stretch=NO, minwidth=0, width=150, anchor=tk.CENTER)
    tree1.column('#8', stretch=NO, minwidth=0, width=150, anchor=tk.CENTER)
   
    style = ttk.Style(window)
    style.theme_use('clam')
    style.configure(".", font=('aerial', 10), foreground="black")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
    tree1.pack()

    lbl_TotalEntries = Label(BottomFrame, font=('aerial', 10, 'bold'), text="Total Entries :")
    lbl_TotalEntries.grid(row =2, column = 0, padx=2, pady =2, sticky=W)
    TotalEntries = IntVar(BottomFrame, value='')
    txtTotalEntries = Entry(BottomFrame, font=('aerial', 12, 'bold'),textvariable = TotalEntries, width = 8)
    txtTotalEntries.grid(row =2, column = 0, padx=100, pady =2, sticky=W)

    ## All Functions defining
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

    def fetchData_NAFO_AreaProfile():
        con= sqlite3.connect(DB_SetCatch_Val_Calculation)
        cur=con.cursor()
        cur.execute("SELECT * FROM SetCatch_NAFO_AreaProfileImported ORDER BY `NAFO_ID` ASC")
        rows=cur.fetchall()
        con.close()
        return rows

    def Populate_Profile():
        tree1.delete(*tree1.get_children())
        rows = fetchData_NAFO_AreaProfile()
        if (len(rows)) >0:
            countIndex = 0
            for row in rows:
                if countIndex % 2 == 0:
                    tree1.insert("", tk.END, values=row , tags =("even",))
                else:
                    tree1.insert("", tk.END, values=row, tags =("odd",))
                countIndex = countIndex+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")
        else:
            try:
                df_CSV_NAFOBoundary = pd.read_csv(Path_CSV_NAFOBoundary, 
                    sep=',' , low_memory=False, na_values=None)
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
                ImportedVariablesRangeDF = pd.DataFrame(df_CSV_NAFOBoundary)
                SubmitImport_To_DBStorage(ImportedVariablesRangeDF)
                countIndex1 = 0
                for each_rec in range(len(ImportedVariablesRangeDF)):
                    if countIndex1 % 2 == 0:
                        tree1.insert("", tk.END, values=list(ImportedVariablesRangeDF.loc[each_rec]), tags =("even",))
                    else:
                        tree1.insert("", tk.END, values=list(ImportedVariablesRangeDF.loc[each_rec]), tags =("odd",))
                    countIndex1 = countIndex1+1
                tree1.tag_configure("even",foreground="black", background="lightblue")
                tree1.tag_configure("odd",foreground="black", background="ghost white")
            except:
                messagebox.showerror('DFO-NL-ASOP NAFO Table Generation Error Message', 
                                "Void DFO-NL-ASOP NAFO Table In The Archived Folder, Name - DFO_NL_ASOP_NAFOAreaProfile.csv")
        TotalEntriesInDB()       

    def TotalEntriesInDB():
        txtTotalEntries.delete(0,END)
        conn = sqlite3.connect(DB_SetCatch_Val_Calculation)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_NAFO_AreaProfileImported;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        TotalEntries = len(data)       
        txtTotalEntries.insert(tk.END,TotalEntries)              
        conn.commit()
        conn.close()

    def ClearRangeVariablesDetails():
        txtVariablesID.config(state= "normal")
        txtVariablesID.delete(0,END)
        txtVariablesID.config(state= "disabled")
        
    def InventoryRec(event):
        for nm in tree1.selection():
            sd = tree1.item(nm, 'values')
            txtVariablesID.config(state= "normal")
            
            txtVariablesID.delete(0,END)
            txtVariablesID.insert(tk.END,sd[0])

            txtNAFOSubArea.delete(0,END)
            txtNAFOSubArea.insert(tk.END,sd[1])

            txtNAFODivision.delete(0,END)
            txtNAFODivision.insert(tk.END,sd[2])

            txtNAFOSubDivision.delete(0,END)
            txtNAFOSubDivision.insert(tk.END,sd[3])

            txtNAFOLabel.delete(0,END)
            txtNAFOLabel.insert(tk.END,sd[4])

            txtNAFOPointOrder.delete(0,END)
            txtNAFOPointOrder.insert(tk.END,sd[5])

            txtNAFO_Latitude.delete(0,END)
            txtNAFO_Latitude.insert(tk.END,sd[6])

            txtNAFO_Longitude.delete(0,END)
            txtNAFO_Longitude.insert(tk.END,sd[7])

            txtVariablesID.config(state= "disabled")
            
    def ClearRangeTableA():
        tree1.delete(*tree1.get_children())
        txtTotalEntries.delete(0,END)  

    def ImportColumnCheck(List_Columns_Import):
        ReturnMatchedMessage    = "Import SetCatch NAFOProfile Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import SetCatch NAFOProfile Headers MisMatch With Database Headers"
        DB_column_names = ['NAFO_ID','NAFOSubArea','NAFODivision',
                           'NAFOSubDivision', 'NAFOLabel', 'NAFO_PointOrder', 
                           'NAFO_Latitude', 'NAFO_Longitude']
        if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,DB_column_names,List_Columns_Import), True): 
            return ReturnMatchedMessage
        else: 
            return ReturnMisMatchedMessage 

    def Import_NAFOAreaCSV():
        ClearRangeTableA()
        ClearRangeVariablesDetails()
        ReturnMatchedMessage    = "Import SetCatch NAFOProfile Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import SetCatch NAFOProfile Headers MisMatch With Database Headers"
        fileList = filedialog.askopenfilenames(title="Select SetCatch NAFOProfile .CSV File/Files", 
                                            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.")))
        Length_fileList  =  len(fileList)
        if Length_fileList >0:
            if fileList:
                dfList =[]
                for filename in fileList:
                    if filename.endswith('.csv'):
                        filename = r"{}".format(filename)
                        df = pd.read_csv(filename, sep=',' , low_memory=False)
                        List_Columns_Import = list(df.columns)
                        Return_Message = ImportColumnCheck(List_Columns_Import)
                        if Return_Message == ReturnMatchedMessage:
                            df = df.iloc[:,:]
                            NAFO_ID = (df.loc[:,'NAFO_ID'])
                            NAFOSubArea = (df.loc[:,'NAFOSubArea'])
                            NAFODivision = (df.loc[:,'NAFODivision'])
                            NAFOSubDivision = (df.loc[:,'NAFOSubDivision'])
                            NAFOLabel = (df.loc[:,'NAFOLabel'])
                            NAFO_PointOrder = (df.loc[:,'NAFO_PointOrder'])
                            NAFO_Latitude = (df.loc[:,'NAFO_Latitude'])
                            NAFO_Longitude = (df.loc[:,'NAFO_Longitude'])
                            column_names = [NAFO_ID, NAFOSubArea, NAFODivision, 
                                            NAFOSubDivision, NAFOLabel, NAFO_PointOrder, 
                                            NAFO_Latitude, NAFO_Longitude]
                            catdf = pd.concat (column_names,axis=1,ignore_index =True)
                            dfList.append(catdf)
                        else:
                            messagebox.showerror('Import File Headers Mismatch', ReturnMisMatchedMessage,)
                
                concatDf = pd.concat(dfList,axis=0, ignore_index =True)
                concatDf.rename(columns={0:'NAFO_ID', 1:'NAFOSubArea', 2:'NAFODivision',
                                        3:'NAFOSubDivision', 4:'NAFOLabel', 5:'NAFO_PointOrder', 
                                        6:'NAFO_Latitude',7:'NAFO_Longitude'},inplace = True)
                concatDf = concatDf.reset_index(drop=True)
                df_CSV_NAFOBoundary = pd.DataFrame(concatDf)
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
                SubmitImport_To_DBStorage(df_CSV_NAFOBoundary)
                Populate_Profile()
                TotalEntriesInDB()
                        
    def ExportNAFOAreaCSV():
        try:
            conn = sqlite3.connect(DB_SetCatch_Val_Calculation)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_NAFO_AreaProfileImported ORDER BY `NAFO_ID` ASC ;", conn)
            if len(Complete_df) >0:
                Export_MasterDF  = pd.DataFrame(Complete_df)
                Export_MasterDF  = Export_MasterDF.reset_index(drop=True)
                filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                        defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                if len(filename) >0:
                    Export_MasterDF.to_csv(filename,index=None)
                    tkinter.messagebox.showinfo("SetCatch NAFO Area Database Export","SetCatch NAFO Area Database Saved as CSV")
                else:
                    tkinter.messagebox.showinfo("SetCatch NAFO Area Database Export Message","Please Select File Name To Export")
            else:
                messagebox.showerror('Export Error', "Void File... Nothing to Export")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()

    def iExit():
        iExit= tkinter.messagebox.askyesno("DFO-NL-ASOP Country Codes Profile", "Confirm If You Want To Exit")
        if iExit >0:
            window.destroy()
            return

    def ReGen_NAFOAreaDF():
        ClearRangeTableA()
        try:
            df_CSV_NAFOBoundary = pd.read_csv(Path_CSV_NAFOBoundary, sep=',', low_memory=False)
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
            NAFOAreaDF = pd.DataFrame(df_CSV_NAFOBoundary)
            SubmitImport_To_DBStorage(NAFOAreaDF)
            countIndex1 = 0
            for each_rec in range(len(NAFOAreaDF)):
                if countIndex1 % 2 == 0:
                    tree1.insert("", tk.END, values=list(NAFOAreaDF.loc[each_rec]), tags =("even",))
                else:
                    tree1.insert("", tk.END, values=list(NAFOAreaDF.loc[each_rec]), tags =("odd",))
                countIndex1 = countIndex1+1
            tree1.tag_configure("even",foreground="black", background="lightblue")
            tree1.tag_configure("odd",foreground="black", background="ghost white")
        except:
            messagebox.showerror('DFO-NL-ASOP Range Variables Table Generation Error Message', 
                            "Void DFO-NL-ASOP Range Variables Table In The Archived Folder, Name - DFO_NL_ASOP_RangeVariables_ValidationList.csv")
        TotalEntriesInDB()   

    ##### Entry Wizard
    tree1.bind('<<TreeviewSelect>>',InventoryRec)

    # ### Button Wizard

    btnPopulateVariableRangeProfile = Button(BottomFrame, text="** Populate NAFO Area Profile Table ** ", 
                                    font=('aerial', 11, 'bold'), height =1, width=32, 
                                    bd=2, bg='alice blue', command = Populate_Profile)
    btnPopulateVariableRangeProfile.grid(row =0, column = 0, padx=450, pady =2, sticky =E)


    btnClearCountryTable = Button(BottomFrame, text="Clear Table", font=('aerial', 10, 'bold'), 
                                height =1, width=10, bd=1, command = ClearRangeTableA)
    btnClearCountryTable.grid(row =3, column = 0, padx=2, pady =2, sticky =W)

    ## Adding File Menu 
    menu = Menu(window)
    window.config(menu=menu)
    filemenu  = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=filemenu)  
    filemenu.add_command(label="Export NAFO Area CSV Database", command=ExportNAFOAreaCSV)
    filemenu.add_command(label="Import NAFO Area CSV", command=Import_NAFOAreaCSV)
    filemenu.add_command(label="Clear Old DB & ReGenerate From Archived CSV", command=ReGen_NAFOAreaDF)
    filemenu.add_command(label="Exit", command=iExit)
    window.mainloop()








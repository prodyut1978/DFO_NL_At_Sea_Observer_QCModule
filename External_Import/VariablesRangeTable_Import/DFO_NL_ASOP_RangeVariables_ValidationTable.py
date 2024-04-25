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

def DFO_NL_ASOP_VariablesRangeProfile():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP Set & Catch Variables Range Profile")
    window.geometry("970x788+200+100")
    window.config(bg="cadet blue")
    window.resizable(0, 0)
    today = datetime.date.today()
    Currentyear = today.year

    ## Defining Main Frame
    MainFrame = Frame(window, bd = 2, padx= 2, pady= 1, relief = RIDGE)
    MainFrame.grid(row =0, column = 0, padx=2, pady =1, sticky =W, rowspan =1)

    ## Defining Top Left frame - A
    Topframe = Frame(MainFrame, bd = 2, padx= 3, pady= 10, relief = RIDGE)
    Topframe.grid(row =0, column = 0, padx=13, pady =1, sticky =W, rowspan =1, columnspan =1)
    VariablesID = IntVar(Topframe, value='')
    VariablesType = StringVar()
    NameRangeVariables = StringVar()
    LowerRangeLimitValue = IntVar(Topframe, value='')
    UpperRangeLimitValue = IntVar(Topframe, value='')
    QCNullValue = StringVar()

    lblTopLeftFrame = Label(Topframe, font=('aerial', 12, 'bold'), text="A. Variables QC Range Profile:")
    lblTopLeftFrame.grid(row =0, column = 0, padx=0, pady =2, sticky =W, rowspan =1)

    lblVariablesID = Label(Topframe, font=('aerial', 10, 'bold'), text = "1. VariablesID :", padx =0, pady= 2)
    lblVariablesID.grid(row =2, column = 0, padx=0, pady =2, sticky =W)
    txtVariablesID  = Entry(Topframe, font=('aerial', 12, 'bold'),state=DISABLED, textvariable= VariablesID, width = 10)
    txtVariablesID.grid(row =2, column = 1, padx=5, pady =10, sticky =W)

    lblVariablesType = Label(Topframe, font=('aerial', 10, 'bold'), text = "2. VariablesType :", padx =0, pady= 2)
    lblVariablesType.grid(row =3, column = 0, padx=0, pady =2, sticky =W)
    txtVariablesType  = Entry(Topframe, font=('aerial', 12, 'bold'),state=DISABLED, textvariable= VariablesType, width = 25)
    txtVariablesType.grid(row =3, column = 1, padx=5, pady =10, sticky =W)

    lblNameRangeVariables = Label(Topframe, font=('aerial', 10, 'bold'), text = "3. NameRangeVariables :", padx =0, pady= 2)
    lblNameRangeVariables.grid(row =4, column = 0, padx=0, pady =2, sticky =W)
    txtNameRangeVariables  = Entry(Topframe, font=('aerial', 12, 'bold'), state=DISABLED, textvariable = NameRangeVariables, width = 25)
    txtNameRangeVariables.grid(row =4, column = 1, padx=5, pady =10, sticky =W)

    lblLowerRangeLimitValue = Label(Topframe, font=('aerial', 10, 'bold'), text = "4. LowerRangeLimitValue :", padx =0, pady= 2)
    lblLowerRangeLimitValue.grid(row =2, column = 2, padx=50, pady =2, sticky =W)
    txtLowerRangeLimitValue  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable = LowerRangeLimitValue, width = 15)
    txtLowerRangeLimitValue.grid(row =2, column = 3, padx=5, pady =10, sticky =W)

    lblUpperRangeLimitValue = Label(Topframe, font=('aerial', 10, 'bold'), text = "5. UpperRangeLimitValue :", padx =0, pady= 2)
    lblUpperRangeLimitValue.grid(row =3, column = 2, padx=50, pady =2, sticky =W)
    txtUpperRangeLimitValue  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable = UpperRangeLimitValue, width = 15)
    txtUpperRangeLimitValue.grid(row =3, column = 3, padx=5, pady =10, sticky =W)

    lblQCNullValue = Label(Topframe, font=('aerial', 10, 'bold'), text = "6. QCNullValue :", padx =0, pady= 2)
    lblQCNullValue.grid(row =4, column = 2, padx=50, pady =2, sticky =W)
    txtQCNullValue  = Entry(Topframe, font=('aerial', 10, 'bold'), 
                    textvariable = QCNullValue, width = 15, state=DISABLED)
    txtQCNullValue.grid(row =4, column = 3, padx=5, pady =10, sticky =W)
    
    ## Defing Bottom - Tree Frame
    BottomFrame = Frame(MainFrame, bd = 2, padx= 1, pady= 10, relief = RIDGE)
    BottomFrame.grid(row =1, column = 0, padx=1, pady =1, sticky =W, rowspan =1, columnspan =1)

    lblBottomFrame = Label(BottomFrame, font=('aerial', 12, 'bold'), text="B. Variables QC Range Table:")
    lblBottomFrame.grid(row =0, column = 0, padx=5, pady =2, sticky =W, rowspan =1)

    TableMargin1 = Frame(BottomFrame, bd = 2, padx= 10, pady= 2, relief = RIDGE)
    TableMargin1.grid(row =1, column = 0, padx=1, pady =1, sticky =W, rowspan =1, columnspan =1)
    tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3", "column4", "column5", "column6"), height=20, show='headings')
    scrollbary = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
    scrollbary.pack(side ='right', fill ='y')
    tree1.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    tree1.configure(xscrollcommand = scrollbarx.set)
    tree1.heading("#1", text="VariablesID", anchor=tk.CENTER)
    tree1.heading("#2", text="VariablesType", anchor=W)
    tree1.heading("#3", text="NameRangeVariables", anchor=W)
    tree1.heading("#4", text="LowerRangeLimitValue", anchor=tk.CENTER)
    tree1.heading("#5", text="UpperRangeLimitValue", anchor=tk.CENTER)
    tree1.heading("#6", text="QCNullValue", anchor=tk.CENTER)
    tree1.column('#1', stretch=NO, minwidth=0, width=100, anchor=tk.CENTER)            
    tree1.column('#2', stretch=NO, minwidth=0, width=150, anchor=W)
    tree1.column('#3', stretch=NO, minwidth=0, width=180, anchor=W)
    tree1.column('#4', stretch=NO, minwidth=0, width=190, anchor=tk.CENTER)
    tree1.column('#5', stretch=NO, minwidth=0, width=190, anchor=tk.CENTER)
    tree1.column('#6', stretch=NO, minwidth=0, width=105, anchor=tk.CENTER)
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

    ## Defing DB Connections & Path For Archived CSV
    DB_SetCatch_Validation_Range = ("./BackEnd/Sqlite3_DB/QC_Check_RangeConsistency_DB/DFO_NL_ASOP_SetCatch_RangeValidation.db")
    Path_CSV_VariablesRangeFile = './External_Import/VariablesRangeTable_Import/CSV_RangeVariables_ValidationTable/DFO_NL_ASOP_RangeVariables_ValidationTable.csv'

    ## All Functions defining
    def SubmitImport_To_DBStorage(ImportedVariablesRangeDF):
        try:
            Import_To_DBStorage = pd.DataFrame(ImportedVariablesRangeDF)
            sqliteConnection = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = sqliteConnection.cursor()
            Import_To_DBStorage.to_sql('SetCatch_RangeLimitVariables_Define', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def fetchData_RangeLimitVariables():
        con= sqlite3.connect(DB_SetCatch_Validation_Range)
        cur=con.cursor()
        cur.execute("SELECT * FROM SetCatch_RangeLimitVariables_Define ORDER BY `VariablesID` ASC")
        rows=cur.fetchall()
        con.close()
        return rows

    def Populate_RangeLimitVariables():
        tree1.delete(*tree1.get_children())
        rows = fetchData_RangeLimitVariables()
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
                df_CSV_VariablesRangeFile = pd.read_csv(Path_CSV_VariablesRangeFile, sep=',' , low_memory=False)
                df_CSV_VariablesRangeFile = df_CSV_VariablesRangeFile.reset_index(drop=True)
                ImportedVariablesRangeDF = pd.DataFrame(df_CSV_VariablesRangeFile)
                ImportedVariablesRangeDF.at[0,'UpperRangeLimitValue']=Currentyear
                ImportedVariablesRangeDF['LowerRangeLimitValue'] = (ImportedVariablesRangeDF.loc[:,
                                                            ['LowerRangeLimitValue']]).fillna(9999999).astype(int, errors='ignore')
                ImportedVariablesRangeDF['UpperRangeLimitValue'] = (ImportedVariablesRangeDF.loc[:,
                                                            ['UpperRangeLimitValue']]).fillna(9999999).astype(int, errors='ignore')
                ImportedVariablesRangeDF = ImportedVariablesRangeDF.replace(9999999, '')
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
                messagebox.showerror('DFO-NL-ASOP Range Variables Table Generation Error Message', 
                                "Void DFO-NL-ASOP Range Variables Table In The Archived Folder, Name - DFO_NL_ASOP_RangeVariables_ValidationList.csv")
        TotalEntriesInDB()       

    def TotalEntriesInDB():
        txtTotalEntries.delete(0,END)
        conn = sqlite3.connect(DB_SetCatch_Validation_Range)
        Complete_df= pd.read_sql_query("SELECT * FROM SetCatch_RangeLimitVariables_Define;", conn)
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
        txtVariablesType.config(state= "normal")
        txtVariablesType.delete(0,END)
        txtVariablesType.config(state= "disabled")
        txtNameRangeVariables.config(state= "normal")
        txtNameRangeVariables.delete(0,END)
        txtNameRangeVariables.config(state= "disabled")
        txtLowerRangeLimitValue.delete(0,END)
        txtUpperRangeLimitValue.delete(0,END)
        txtQCNullValue.config(state= "normal")
        txtQCNullValue.delete(0,END)
        txtQCNullValue.config(state= "readonly")

    def InventoryRec(event):
        for nm in tree1.selection():
            sd = tree1.item(nm, 'values')
            txtVariablesID.config(state= "normal")
            txtVariablesID.delete(0,END)
            txtVariablesID.insert(tk.END,sd[0])

            txtVariablesType.config(state= "normal")
            txtVariablesType.delete(0,END)
            txtVariablesType.insert(tk.END,sd[1])

            txtNameRangeVariables.config(state= "normal")
            txtNameRangeVariables.delete(0,END)
            txtNameRangeVariables.insert(tk.END,sd[2]) 
            
            txtLowerRangeLimitValue.delete(0,END)
            txtLowerRangeLimitValue.insert(tk.END,sd[3])                
            txtUpperRangeLimitValue.delete(0,END)
            txtUpperRangeLimitValue.insert(tk.END,sd[4])

            txtQCNullValue.config(state= "normal")
            txtQCNullValue.delete(0,END)
            txtQCNullValue.insert(tk.END,sd[5])

            txtVariablesID.config(state= "disabled")
            txtVariablesType.config(state= "disabled")
            txtNameRangeVariables.config(state= "disabled")
            txtQCNullValue.config(state= "disabled")

    def ClearRangeTableA():
        tree1.delete(*tree1.get_children())
        txtTotalEntries.delete(0,END)  

    def update_RangeLimitVariablesProfile():
        cur_id = tree1.focus()
        selvalue = tree1.item(cur_id)['values']
        Length_Selected  =  (len(selvalue))
        if Length_Selected != 0:
            SelectionTree = tree1.selection()
            if (len(SelectionTree)>0) & (len(SelectionTree)==1) & (len(SelectionTree)<2):
                iUpdate = tkinter.messagebox.askyesno("Update Entry From DFO-NL-ASOP Range Limit Variables Database", 
                            "Confirm If You Want To Update From DFO-NL-ASOP Range Limit Variables Database")
                if iUpdate >0:
                    for item in SelectionTree:
                        list_item = (tree1.item(item, 'values'))
                        list_item_VariablesID = int(list_item[0])
                        list_item_VariablesType = (list_item[1])
                        list_item_NameRangeVariables = (list_item[2])
                        LowerRangeLimitValue = txtLowerRangeLimitValue.get()
                        UpperRangeLimitValue = txtUpperRangeLimitValue.get()
                        QCNullValue = txtQCNullValue.get()
                        conn= sqlite3.connect(DB_SetCatch_Validation_Range)
                        cur=conn.cursor()
                        if (len(QCNullValue)!=0) & (len(LowerRangeLimitValue)!=0) & (len(UpperRangeLimitValue)!=0):
                            cur.execute("UPDATE SetCatch_RangeLimitVariables_Define SET LowerRangeLimitValue = ?, \
                                        UpperRangeLimitValue = ?, QCNullValue = ? WHERE VariablesID = ?", 
                                       (LowerRangeLimitValue, UpperRangeLimitValue, QCNullValue, list_item_VariablesID))
                            tree1.delete(*tree1.get_children())
                            tree1.insert("", tk.END,values=(list_item_VariablesID, list_item_VariablesType, list_item_NameRangeVariables,
                                                            LowerRangeLimitValue, UpperRangeLimitValue, QCNullValue ))
                            conn.commit()
                            conn.close()
                            TotalEntriesInDB() 
                        else:
                            tkinter.messagebox.showerror("Update Error","QCNullValue, LowerRangeLimitValue, UpperRangeLimitValue can not be empty")
            else:
                UpdatePossibleError =  ("Possible Reasons For Update Error: " + '\n' + '\n' + 
                        "1. Please Select One Entry Only From The Range Limit Variables Table To Update "  + '\n' + '\n' + 
                        "2. Please Donot Select More Than One Entry To Update At The Same time "  + '\n' + '\n' + 
                        "3. Please Do Not Update Without Selecting Entry From Range Limit Variables Table" )
                tkinter.messagebox.showerror("Update Error Possible Reasons",UpdatePossibleError)

    def ImportColumnCheck(List_Columns_Import):
        ReturnMatchedMessage    = "Import SetCatch RangeVariables Profile Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import SetCatch RangeVariables Profile Headers MisMatch With Database Headers"
        DB_column_names = ['VariablesID', 'VariablesType', 'NameRangeVariables',
                        'LowerRangeLimitValue', 'UpperRangeLimitValue', 'QCNullValue']
        if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,DB_column_names,List_Columns_Import), True): 
            return ReturnMatchedMessage
        else: 
            return ReturnMisMatchedMessage 

    def Import_SetCatch_RangeVariables_CSV():
        ClearRangeTableA()
        ClearRangeVariablesDetails()
        ReturnMatchedMessage    = "Import SetCatch RangeVariables Profile Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import SetCatch RangeVariables Profile Headers MisMatch With Database Headers"
        fileList = filedialog.askopenfilenames(title="Select SetCatch RangeVariables Profile .CSV File/Files", 
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
                            VariablesID = (df.loc[:,'VariablesID'])
                            VariablesType = (df.loc[:,'VariablesType'])
                            NameRangeVariables = (df.loc[:,'NameRangeVariables'])
                            LowerRangeLimitValue = (df.loc[:,'LowerRangeLimitValue'])
                            UpperRangeLimitValue = (df.loc[:,'UpperRangeLimitValue'])
                            QCNullValue = (df.loc[:,'QCNullValue'])
                            column_names = [VariablesID, VariablesType, NameRangeVariables, 
                                        LowerRangeLimitValue, UpperRangeLimitValue, QCNullValue]
                            catdf = pd.concat (column_names,axis=1,ignore_index =True)
                            dfList.append(catdf)
                        else:
                            messagebox.showerror('Import File Headers Mismatch', ReturnMisMatchedMessage,)
                
                concatDf = pd.concat(dfList,axis=0, ignore_index =True)
                concatDf.rename(columns={0:'VariablesID', 1:'VariablesType', 2:'NameRangeVariables',
                                        3:'LowerRangeLimitValue', 4:'UpperRangeLimitValue', 
                                        5:'QCNullValue'},inplace = True)
                concatDf = concatDf.reset_index(drop=True)
                Raw_Imported_Df = pd.DataFrame(concatDf)
                Raw_Imported_Df.at[0,'UpperRangeLimitValue']=Currentyear
                Raw_Imported_Df['LowerRangeLimitValue'] = (Raw_Imported_Df.loc[:,
                                                            ['LowerRangeLimitValue']]).fillna(9999999).astype(int, errors='ignore')
                Raw_Imported_Df['UpperRangeLimitValue'] = (Raw_Imported_Df.loc[:,
                                                            ['UpperRangeLimitValue']]).fillna(9999999).astype(int, errors='ignore')
                Raw_Imported_Df = Raw_Imported_Df.replace(9999999, '')
                SubmitImport_To_DBStorage(Raw_Imported_Df)
                Populate_RangeLimitVariables()
                TotalEntriesInDB()
                        
    def ExportRangeLimitVariablesDB():
        try:
            conn = sqlite3.connect(DB_SetCatch_Validation_Range)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM SetCatch_RangeLimitVariables_Define ORDER BY `VariablesID` ASC ;", conn)
            if len(Complete_df) >0:
                Export_MasterDF  = pd.DataFrame(Complete_df)
                Export_MasterDF  = Export_MasterDF.reset_index(drop=True)
                filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                        defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                if len(filename) >0:
                    Export_MasterDF.to_csv(filename,index=None)
                    tkinter.messagebox.showinfo("SetCatch Range Limit Variables Database Export","SetCatch Range Limit Variables Database Saved as CSV")
                else:
                    tkinter.messagebox.showinfo("SetCatch Range Limit Variables Database Export Message","Please Select File Name To Export")
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

    def ReGen_RangeLimitVariablesDB():
        ClearRangeTableA()
        try:
            df_CSV_VariablesRangeFile = pd.read_csv(Path_CSV_VariablesRangeFile, sep=',' , low_memory=False)
            df_CSV_VariablesRangeFile = df_CSV_VariablesRangeFile.reset_index(drop=True)
            ImportedVariablesRangeDF = pd.DataFrame(df_CSV_VariablesRangeFile)
            ImportedVariablesRangeDF.at[0,'UpperRangeLimitValue']=Currentyear
            ImportedVariablesRangeDF['LowerRangeLimitValue'] = (ImportedVariablesRangeDF.loc[:,
                                                        ['LowerRangeLimitValue']]).fillna(9999999).astype(int, errors='ignore')
            ImportedVariablesRangeDF['UpperRangeLimitValue'] = (ImportedVariablesRangeDF.loc[:,
                                                        ['UpperRangeLimitValue']]).fillna(9999999).astype(int, errors='ignore')
            ImportedVariablesRangeDF = ImportedVariablesRangeDF.replace(9999999, '')
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
            messagebox.showerror('DFO-NL-ASOP Range Variables Table Generation Error Message', 
                            "Void DFO-NL-ASOP Range Variables Table In The Archived Folder, Name - DFO_NL_ASOP_RangeVariables_ValidationList.csv")
        TotalEntriesInDB()   

    ##### Entry Wizard
    tree1.bind('<<TreeviewSelect>>',InventoryRec)

    # ### Button Wizard
    btnModifyRangeProfile = Button(Topframe, text="Modify Range Profile", font=('aerial', 10, 'bold'), 
                                height =2, width=20, bd=2, command = update_RangeLimitVariablesProfile)
    btnModifyRangeProfile.grid(row =8, column = 3, padx=0, pady =5, sticky =E)

    btnClearRangeProfile = Button(Topframe, text="Clear Range Details", font=('aerial', 10, 'bold'), 
                                height =2, width=20, bd=2, command = ClearRangeVariablesDetails)
    btnClearRangeProfile.grid(row =8, column = 2, padx=50, pady =5, sticky =E)

    btnPopulateVariableRangeProfile = Button(BottomFrame, text="** Populate Variable Range Table ** ", 
                                    font=('aerial', 11, 'bold'), height =1, width=32, 
                                    bd=2, bg='alice blue', command = Populate_RangeLimitVariables)
    btnPopulateVariableRangeProfile.grid(row =0, column = 0, padx=350, pady =2, sticky =W)


    btnClearCountryTable = Button(BottomFrame, text="Clear Table", font=('aerial', 10, 'bold'), 
                                height =1, width=10, bd=1, command = ClearRangeTableA)
    btnClearCountryTable.grid(row =2, column = 0, padx=50, pady =2, sticky =E)

    ## Adding File Menu 
    menu = Menu(window)
    window.config(menu=menu)
    filemenu  = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=filemenu)  
    filemenu.add_command(label="Export Range Limit Variables Database", command=ExportRangeLimitVariablesDB)
    filemenu.add_command(label="Import Range Limit Variables CSV", command=Import_SetCatch_RangeVariables_CSV)
    filemenu.add_command(label="Clear Old DB & ReGenerate From Archived CSV", command=ReGen_RangeLimitVariablesDB)
    filemenu.add_command(label="Exit", command=iExit)
    window.mainloop()










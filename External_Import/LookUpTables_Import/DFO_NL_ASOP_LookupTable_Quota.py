#Front End
from tkinter import*
import tkinter.messagebox
from tkinter import ttk, filedialog
from tkinter import messagebox
import tkinter as tk
import sqlite3
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilenames
import pandas as pd
import numpy as np
import functools

def DFO_NL_ASOP_Quota_Profile_Table():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP Quota Codes Profile")
    window.geometry("745x785+200+100")
    window.config(bg="cadet blue")
    window.resizable(0, 0)

    Topframe = Frame(window, bd = 2, padx= 3, pady= 10, relief = RIDGE)
    Topframe.pack(side = TOP)
    DatabaseUID = IntVar(Topframe, value='')
    QuotaCode = IntVar(Topframe, value='')
    QuotaName = StringVar()
    Comments  = StringVar()
    lblTitEntry = Label(Topframe, font=('aerial', 12, 'bold'), text="Quota Code Details:")
    lblTitEntry.grid(row =0, column = 0, padx=0, pady =2, sticky =W, rowspan =1)
    lblDatabaseUID = Label(Topframe, font=('aerial', 10, 'bold'), text = "1. Database UID :", padx =0, pady= 2)
    lblDatabaseUID.grid(row =2, column = 0, padx=0, pady =2, sticky =W)
    txtDatabaseUID  = Entry(Topframe, state=DISABLED, font=('aerial', 12, 'bold'),textvariable= DatabaseUID, width = 10)
    txtDatabaseUID.grid(row =2, column = 1, padx=5, pady =10, sticky =W)
    lblQuotaCode = Label(Topframe, font=('aerial', 10, 'bold'), text = "2. Quota Code :", padx =0, pady= 2)
    lblQuotaCode.grid(row =3, column = 0, padx=0, pady =2, sticky =W)
    txtQuotaCode  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable= QuotaCode, width = 25)
    txtQuotaCode.grid(row =3, column = 1, padx=5, pady =10, sticky =W)
    lblQuotaName = Label(Topframe, font=('aerial', 10, 'bold'), text = "3. Quota Name :", padx =0, pady= 2)
    lblQuotaName.grid(row =4, column = 0, padx=0, pady =2, sticky =W)
    txtQuotaName  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable = QuotaName, width = 25)
    txtQuotaName.grid(row =4, column = 1, padx=5, pady =10, sticky =W)
    lblComments = Label(Topframe, font=('aerial', 10, 'bold'), text = "4. Comments :", padx =0, pady= 2)
    lblComments.grid(row =5, column = 0, padx=0, pady =2, sticky =W)
    txtComments  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable = Comments, width = 35)
    txtComments.grid(row =5, column = 1, padx=5, pady =10, sticky =W)

    Midframe = Frame(window, bd = 2, padx= 3, pady= 0, relief = RIDGE, bg="cadet blue")
    Midframe.pack(side = TOP)
    lblQuotaTable = Label(Midframe, font=('aerial', 12, 'bold'), text="** Clear - View - Import : Quota Codes Lookup Table **", bg="cadet blue")
    lblQuotaTable.grid(row =0, column = 1, padx=50, pady =2, sticky =W, rowspan =1)

    TableMargin1 = Frame(window, bd = 2, padx= 10, pady= 2, relief = RIDGE)
    TableMargin1.pack(side=TOP)
    TableMargin1.pack(side=LEFT)
    tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3", "column4"), height=14, show='headings')
    scrollbary = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
    scrollbary.pack(side ='right', fill ='y')
    tree1.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    tree1.configure(xscrollcommand = scrollbarx.set)
    tree1.heading("#1", text="Database UID", anchor=tk.CENTER)
    tree1.heading("#2", text="Quota Code", anchor=tk.CENTER)
    tree1.heading("#3", text="Quota Name", anchor=W)
    tree1.heading("#4", text="Comments", anchor=W)
    tree1.column('#1', stretch=NO, minwidth=0, width=100, anchor=tk.CENTER)            
    tree1.column('#2', stretch=NO, minwidth=0, width=150, anchor=tk.CENTER)
    tree1.column('#3', stretch=NO, minwidth=0, width=300, anchor=W)
    tree1.column('#4', stretch=NO, minwidth=0, width=200, anchor=W)
    style = ttk.Style(window)
    style.configure(".", font=('aerial', 10), foreground="black")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
    tree1.pack()

    BottomFrame = Frame(TableMargin1, bd = 2, padx= 10, pady= 2, relief = RIDGE)
    BottomFrame.pack(side = BOTTOM)
    lbl_TotalEntries = Label(BottomFrame, font=('aerial', 10, 'bold'), text="Total Entries :")
    lbl_TotalEntries.grid(row =0, column = 0, padx=2, pady =2)
    TotalEntries = IntVar(BottomFrame, value='')
    txtTotalEntries = Entry(BottomFrame, font=('aerial', 12, 'bold'),textvariable = TotalEntries, width = 6)
    txtTotalEntries.grid(row =0, column = 1, padx=2, pady =2, sticky =W)

    DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")

    # All Functions defining
    def addInvRec_QuotaProfile(QuotaCode, QuotaName, Comments):
        sqliteConnection= sqlite3.connect(DB_Lookup_Table)
        cur=sqliteConnection.cursor()    
        cur.execute("INSERT INTO DFO_NL_ASOP_QuotaProfile (DatabaseUID, QuotaCode, QuotaName, Comments) VALUES (?,?,?,?)",[int(QuotaCode)+10000, QuotaCode, QuotaName, Comments])
        sqliteConnection.commit()
        sqliteConnection.close()

    def viewData_QuotaProfile():
        con= sqlite3.connect(DB_Lookup_Table)
        cur=con.cursor()
        cur.execute("SELECT * FROM DFO_NL_ASOP_QuotaProfile ORDER BY `QuotaCode` ASC")
        rows=cur.fetchall()
        con.close()
        return rows

    def iExit():
        iExit= tkinter.messagebox.askyesno("DFO-NL-ASOP Quota Codes Profile", "Confirm If You Want To Exit")
        if iExit >0:
            window.destroy()
            return

    def add_QuotaProfile():
        ReturnDuplicated    = "Insert Quota Code Duplicated With Previous DB Entries"
        ReturnNotDuplicated = "Insert Quota Code Not Duplicated With Previous DB Entries"
        ReturnFirstEntry    = "Initial Entry"
        if(len(txtQuotaCode.get())!=0) & (len(txtQuotaName.get())!=0):
            entryQuotaCode = int(txtQuotaCode.get())
            Return_Message = UniqueCheck_QuotaCode(entryQuotaCode)
            if (Return_Message == ReturnNotDuplicated)| (Return_Message == ReturnFirstEntry):
                addInvRec_QuotaProfile(txtQuotaCode.get(), txtQuotaName.get(), txtComments.get())
                view_QuotaProfile()
                ClearQuotaDetails()
                QuotaTotalEntries()
            else:
                messagebox.showerror('Insert Entry Duplicated Error', ReturnDuplicated)
        else:
            tkinter.messagebox.showinfo("Add Error","Entries can not be empty")

    def view_QuotaProfile():
        tree1.delete(*tree1.get_children())
        for row in viewData_QuotaProfile():
            tree1.insert("", tk.END, values=row)
        QuotaTotalEntries()       

    def ClearQuotaDetails():
        txtDatabaseUID.config(state= "normal")
        txtDatabaseUID.delete(0,END)
        txtDatabaseUID.config(state= "disabled")
        txtQuotaCode.delete(0,END)
        txtQuotaName.delete(0,END)
        txtComments.delete(0,END)

    def delete_QuotaProfile():
        SelectionTree = tree1.selection()
        if len(SelectionTree)>0:
            iDelete = tkinter.messagebox.askyesno("Delete Entry From DFO-NL-ASOP Quota Code Database", 
                        "Confirm If You Want To Delete The Selection Entries From DFO-NL-ASOP Quota Code Database")
            if iDelete >0:
                conn = sqlite3.connect(DB_Lookup_Table)
                cur = conn.cursor()
                if(len(txtQuotaCode.get())!=0) & (len(txtQuotaName.get())!=0):
                    for selected_item in tree1.selection():
                        cur.execute("DELETE FROM DFO_NL_ASOP_QuotaProfile WHERE DatabaseUID =? AND QuotaCode =? AND QuotaName = ? ", (tree1.set(selected_item, '#1'), tree1.set(selected_item, '#2'),tree1.set(selected_item, '#3'),))
                        conn.commit()
                        tree1.delete(selected_item)
                    conn.commit()
                    conn.close()
                tree1.delete(*tree1.get_children())
                ClearQuotaDetails()
                view_QuotaProfile()
                QuotaTotalEntries()
                return
        else:
            tkinter.messagebox.showinfo("Delete Error","Please Select Entries From Quota Code Table To Delete From Database")

    def update_QuotaProfile():
        cur_id = tree1.focus()
        selvalue = tree1.item(cur_id)['values']
        Length_Selected  =  (len(selvalue))
        if Length_Selected != 0:
            SelectionTree = tree1.selection()
            if (len(SelectionTree)>0) & (len(SelectionTree)==1) & (len(SelectionTree)<2):
                iUpdate = tkinter.messagebox.askyesno("Update Entry From DFO-NL-ASOP Quota Code Database", 
                            "Confirm If You Want To Update From DFO-NL-ASOP Quota Code Database")
                if iUpdate >0:
                    for item in SelectionTree:
                        list_item = (tree1.item(item, 'values'))
                        list_item_DatabaseUID = int(list_item[0])
                        QuotaCode = txtQuotaCode.get()
                        QuotaName = txtQuotaName.get()
                        Comments = txtComments.get()
                        conn= sqlite3.connect(DB_Lookup_Table)
                        cur=conn.cursor()
                        if(len(txtQuotaCode.get())!=0) & (len(txtQuotaName.get())!=0):
                            cur.execute("UPDATE DFO_NL_ASOP_QuotaProfile SET QuotaCode = ?,  QuotaName = ?, Comments = ? WHERE DatabaseUID =?", 
                                (QuotaCode, QuotaName, Comments, list_item_DatabaseUID))
                            tree1.delete(*tree1.get_children())
                            tree1.insert("", tk.END,values=(list_item_DatabaseUID, QuotaCode, QuotaName, Comments ))
                            conn.commit()
                            conn.close()
                            QuotaTotalEntries() 
                        else:
                            tkinter.messagebox.showerror("Add Error","Entries can not be empty")
            else:
                UpdatePossibleError =  ("Possible Reasons For Update Error: " + '\n' + '\n' + 
                        "1. Please Select One Entry Only From The Quota Table To Update "  + '\n' + '\n' + 
                        "2. Please Donot Select More Than One Entry To Update At The Same time "  + '\n' + '\n' + 
                        "3. Please Do Not Update Without Selecting Entry From Quota Table" )
                tkinter.messagebox.showerror("Update Error Possible Reasons",UpdatePossibleError)

    def ClearQuotaTable():
        tree1.delete(*tree1.get_children())
        txtTotalEntries.delete(0,END)   

    def InventoryRec(event):
        for nm in tree1.selection():
            sd = tree1.item(nm, 'values')
            txtDatabaseUID.config(state= "normal")
            txtDatabaseUID.delete(0,END)
            txtDatabaseUID.insert(tk.END,sd[0]) 
            txtQuotaCode.delete(0,END)
            txtQuotaCode.insert(tk.END,sd[1])                
            txtQuotaName.delete(0,END)
            txtQuotaName.insert(tk.END,sd[2])
            txtComments.delete(0,END)
            txtComments.insert(tk.END,sd[3])
            txtDatabaseUID.config(state= "disabled")

    def ImportColumnCheck(List_Columns_Import):
        ReturnMatchedMessage    = "Import Quota Code Profile Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Quota Code Profile Headers MisMatch With Database Headers"
        DB_column_names = ["QuotaCode", "QuotaName", "Comments"]
        if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,DB_column_names,List_Columns_Import), True): 
            return ReturnMatchedMessage
        else: 
            return ReturnMisMatchedMessage 

    def Import_To_DBStorage(Raw_Imported_Df):
        try:
            Import_To_DBStorage = pd.DataFrame(Raw_Imported_Df)
            RecordIdentifier_Get = 0
            Import_To_DBStorage.insert(loc=0, column="DatabaseUID", 
                                    value = np.arange(RecordIdentifier_Get, 
                                    len(Import_To_DBStorage) + RecordIdentifier_Get))
            sqliteConnection = sqlite3.connect(DB_Lookup_Table)
            cursor = sqliteConnection.cursor()
            Import_To_DBStorage.to_sql('DFO_NL_ASOP_QuotaProfile', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def Import_Quota_Profile_CSV():
        ClearQuotaTable()
        ClearQuotaDetails()
        ReturnMatchedMessage    = "Import Quota Code Profile Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Quota Code Profile Headers MisMatch With Database Headers"
        fileList = filedialog.askopenfilenames(title="Select Quota Code Profile .CSV File/Files", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.")))
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
                            QuotaCode = (df.loc[:,'QuotaCode'])
                            QuotaName = (df.loc[:,'QuotaName'])
                            Comments = (df.loc[:,'Comments'])
                            column_names = [QuotaCode, QuotaName, Comments]
                            catdf = pd.concat (column_names,axis=1,ignore_index =True)
                            dfList.append(catdf)
                        else:
                            messagebox.showerror('Import File Headers Mismatch', ReturnMisMatchedMessage)
                
                concatDf = pd.concat(dfList,axis=0, ignore_index =True)
                concatDf.rename(columns={0:'QuotaCode', 1:'QuotaName', 2:'Comments'},inplace = True)
                Raw_Imported_Df = pd.DataFrame(concatDf)
                if (Raw_Imported_Df["QuotaCode"].duplicated().values.any() == True) | \
                    (Raw_Imported_Df["QuotaCode"].isnull().values.any() == True)|\
                    (Raw_Imported_Df["QuotaName"].isnull().values.any() == True):
                    messagebox.showerror("Import Error In CSV File","Duplicated QuotaCode Or Empty QuotaCode/QuotaName Found")
                else:
                    Raw_Imported_Df = pd.DataFrame(concatDf)
                    ClearQuotaTable()
                    Import_To_DBStorage(Raw_Imported_Df)
                    view_QuotaProfile()
                    QuotaTotalEntries()
                        
    def QuotaTotalEntries():
        txtTotalEntries.delete(0,END)
        conn = sqlite3.connect(DB_Lookup_Table)
        Complete_df= pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_QuotaProfile ORDER BY `QuotaCode` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        TotalEntries = len(data)       
        txtTotalEntries.insert(tk.END,TotalEntries)              
        conn.commit()
        conn.close()

    def UniqueCheck_QuotaCode(entryQuotaCode):
        ReturnDuplicated    = "Insert Quota Code Duplicated With Previous DB Entries"
        ReturnNotDuplicated = "Insert Quota Code Not Duplicated With Previous DB Entries"
        ReturnFirstEntry    = "Initial Entry"
        try:
            entryQuotaCode = int(entryQuotaCode)
            sqliteConnection = sqlite3.connect(DB_Lookup_Table)
            cursor = sqliteConnection.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_QuotaProfile ORDER BY `QuotaCode` ASC ;", sqliteConnection)
            data = pd.DataFrame(Complete_df)
            data = data.reset_index(drop=True)
            TotalEntries = len(data)
            if TotalEntries > 0:
                if (entryQuotaCode in data["QuotaCode"].unique()) == True: 
                    return ReturnDuplicated
                else: 
                    return ReturnNotDuplicated
            else:
                return ReturnFirstEntry
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def ExportQuotaProfileDB():
        try:
            conn = sqlite3.connect(DB_Lookup_Table)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_QuotaProfile ORDER BY `QuotaCode` ASC ;", conn)
            if len(Complete_df) >0:
                Export_MasterTB_DF  = pd.DataFrame(Complete_df)
                Export_MasterTB_DF.drop(['DatabaseUID'], axis=1, inplace=True)
                Export_MasterTB_DF  = Export_MasterTB_DF.reset_index(drop=True)
                filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                        defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                if len(filename) >0:
                    Export_MasterTB_DF.to_csv(filename,index=None)
                    tkinter.messagebox.showinfo("Master Quota Profile Database Export","Master Quota Coded Profile Database Saved as CSV")
                else:
                    tkinter.messagebox.showinfo("Master Quota Profile Database Export Message","Please Select File Name To Export")
            else:
                messagebox.showerror('Export Error', "Void File... Nothing to Export")
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if conn:
                cursor.close()
                conn.close()


    ##### Entry Wizard
    tree1.bind('<<TreeviewSelect>>',InventoryRec)

    # ### Button Wizard
    btnAddQuotaProfile = Button(Topframe, text="Add Quota Profile", font=('aerial', 10, 'bold'), height =2, width=20, bd=2, command = add_QuotaProfile)
    btnAddQuotaProfile.grid(row =6, column = 1, padx=0, pady =5, sticky =E)

    btnModifyQuotaProfile = Button(Topframe, text="Modify Quota Profile", font=('aerial', 10, 'bold'), height =2, width=20, bd=2, command = update_QuotaProfile)
    btnModifyQuotaProfile.grid(row =7, column = 1, padx=0, pady =5, sticky =E)

    btnClearQuotaProfile = Button(Topframe, text="Clear Quota Details", font=('aerial', 10, 'bold'), height =2, width=20, bd=2, command = ClearQuotaDetails)
    btnClearQuotaProfile.grid(row =6, column = 0, padx=0, pady =5, sticky =E)

    btnDeleteQuotaProfile = Button(Topframe, text="Delete Quota Profile", font=('aerial', 10, 'bold'), height =2, width=20, bd=2, command = delete_QuotaProfile)
    btnDeleteQuotaProfile.grid(row =7, column = 0, padx=0, pady =5, sticky =E)

    btnClearQuotaTable = Button(Midframe, text="Clear Table", font=('aerial', 10, 'bold'), height =2, width=10, bd=2, command = ClearQuotaTable)
    btnClearQuotaTable.grid(row =6, column = 0, padx=2, pady =2, sticky =W)

    btnViewQuotaProfile = Button(Midframe, text="View Quota Codes Table", font=('aerial', 10, 'bold'), height =2, width=22, bd=2, command = view_QuotaProfile)
    btnViewQuotaProfile.grid(row =6, column = 1, padx=170, pady =2, sticky =W)

    btnImportQuotaTable = Button(Midframe, text="Import Table\n (.csv)", font=('aerial', 10, 'bold'), height =2, width=12, bd=2, command = Import_Quota_Profile_CSV)
    btnImportQuotaTable.grid(row =6, column = 2, padx=2, pady =2, sticky =E)

    ## Adding File Menu 
    menu = Menu(window)
    window.config(menu=menu)
    filemenu  = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=filemenu)  
    filemenu.add_command(label="Export Quota Profile DB", command=ExportQuotaProfileDB)
    filemenu.add_command(label="Exit", command=iExit)

    window.mainloop()











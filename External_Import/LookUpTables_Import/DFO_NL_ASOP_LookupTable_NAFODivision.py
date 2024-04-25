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

def DFO_NL_ASOP_NAFODivision_Profile_Table():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP NAFODivision Codes Profile")
    window.geometry("810x770+200+100")
    window.config(bg="cadet blue")
    window.resizable(0, 0)

    Topframe = Frame(window, bd = 2, padx= 3, pady= 10, relief = RIDGE)
    Topframe.pack(side = TOP)
    DatabaseUID = IntVar(Topframe, value='')
    AlphaNAFODivision = StringVar()
    AlphaUnitArea = StringVar()
    NumericNAFODivision = IntVar(Topframe, value='')
    NumericUnitArea = IntVar(Topframe, value='')

    lblTitEntry = Label(Topframe, font=('aerial', 12, 'bold'), text="NAFODivision Code Details:")
    lblTitEntry.grid(row =0, column = 0, padx=0, pady =2, sticky =W, rowspan =1)

    lblDatabaseUID = Label(Topframe, font=('aerial', 10, 'bold'), text = "1. Database UID :", padx =0, pady= 2)
    lblDatabaseUID.grid(row =2, column = 0, padx=0, pady =2, sticky =W)
    txtDatabaseUID  = Entry(Topframe, state=DISABLED, font=('aerial', 12, 'bold'),textvariable= DatabaseUID, width = 10)
    txtDatabaseUID.grid(row =2, column = 1, padx=5, pady =10, sticky =W)

    lblAlphaNAFODivision = Label(Topframe, font=('aerial', 10, 'bold'), text = "2. AlphaNAFODivision Code :", padx =0, pady= 2)
    lblAlphaNAFODivision.grid(row =3, column = 0, padx=0, pady =2, sticky =W)
    txtAlphaNAFODivision  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable= AlphaNAFODivision, width = 25)
    txtAlphaNAFODivision.grid(row =3, column = 1, padx=5, pady =10, sticky =W)

    lblAlphaUnitArea = Label(Topframe, font=('aerial', 10, 'bold'), text = "3. AlphaUnitArea Code :", padx =0, pady= 2)
    lblAlphaUnitArea.grid(row =4, column = 0, padx=0, pady =2, sticky =W)
    txtAlphaUnitArea  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable = AlphaUnitArea, width = 25)
    txtAlphaUnitArea.grid(row =4, column = 1, padx=5, pady =10, sticky =W)

    lblNumericNAFODivision = Label(Topframe, font=('aerial', 10, 'bold'), text = "4. NumericNAFODivision Code:", padx =0, pady= 2)
    lblNumericNAFODivision.grid(row =5, column = 0, padx=0, pady =2, sticky =W)
    txtNumericNAFODivision  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable = NumericNAFODivision, width = 35)
    txtNumericNAFODivision.grid(row =5, column = 1, padx=5, pady =10, sticky =W)

    lblNumericUnitArea = Label(Topframe, font=('aerial', 10, 'bold'), text = "5. NumericUnitArea Code:", padx =0, pady= 2)
    lblNumericUnitArea.grid(row =6, column = 0, padx=0, pady =2, sticky =W)
    txtNumericUnitArea  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable = NumericUnitArea, width = 35)
    txtNumericUnitArea.grid(row =6, column = 1, padx=5, pady =10, sticky =W)

    Midframe = Frame(window, bd = 2, padx= 3, pady= 0, relief = RIDGE, bg="cadet blue")
    Midframe.pack(side = TOP)
    lblNAFODivisionTable = Label(Midframe, font=('aerial', 12, 'bold'), text="** Clear - View - Import : NAFODivision Codes Lookup Table **", bg="cadet blue")
    lblNAFODivisionTable.grid(row =0, column = 1, padx=50, pady =2, sticky =W, rowspan =1)

    TableMargin1 = Frame(window, bd = 2, padx= 10, pady= 2, relief = RIDGE)
    TableMargin1.pack(side=TOP)
    TableMargin1.pack(side=LEFT)
    tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3", "column4", "column5"), height=14, show='headings')
    scrollbary = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
    scrollbary.pack(side ='right', fill ='y')
    tree1.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    tree1.configure(xscrollcommand = scrollbarx.set)
    tree1.heading("#1", text="Database UID", anchor=tk.CENTER)
    tree1.heading("#2", text="AlphaNAFODivision", anchor=tk.CENTER)
    tree1.heading("#3", text="AlphaUnitArea", anchor=tk.CENTER)
    tree1.heading("#4", text="NumericNAFODivision", anchor=tk.CENTER)
    tree1.heading("#5", text="NumericUnitArea", anchor=tk.CENTER)

    tree1.column('#1', stretch=NO, minwidth=0, width=100, anchor = tk.CENTER)            
    tree1.column('#2', stretch=NO, minwidth=0, width=200, anchor = tk.CENTER)
    tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor = tk.CENTER)
    tree1.column('#4', stretch=NO, minwidth=0, width=200, anchor = tk.CENTER)
    tree1.column('#5', stretch=NO, minwidth=0, width=200, anchor = tk.CENTER)

    style = ttk.Style(window)
    style.theme_use('clam')
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
    def addInvRec_NAFODivisionProfile(AlphaNAFODivision, AlphaUnitArea, NumericNAFODivision,NumericUnitArea):
        sqliteConnection= sqlite3.connect(DB_Lookup_Table)
        cur=sqliteConnection.cursor()    
        cur.execute("INSERT INTO DFO_NL_ASOP_NAFODivisionProfile (DatabaseUID, AlphaNAFODivision, AlphaUnitArea, NumericNAFODivision,NumericUnitArea) VALUES (?,?,?,?,?)",[int(NumericNAFODivision)+10000, AlphaNAFODivision, AlphaUnitArea, NumericNAFODivision,NumericUnitArea])
        sqliteConnection.commit()
        sqliteConnection.close()

    def viewData_NAFODivisionProfile():
        con= sqlite3.connect(DB_Lookup_Table)
        cur=con.cursor()
        cur.execute("SELECT * FROM DFO_NL_ASOP_NAFODivisionProfile ORDER BY `DatabaseUID` ASC")
        rows=cur.fetchall()
        con.close()
        return rows

    def iExit():
        iExit= tkinter.messagebox.askyesno("DFO-NL-ASOP NAFODivision Codes Profile", "Confirm If You Want To Exit")
        if iExit >0:
            window.destroy()
            return

    def add_NAFODivisionProfile():
        ReturnDuplicated    = "Insert NAFODivision Code Duplicated With Previous DB Entries"
        ReturnNotDuplicated = "Insert NAFODivision Code Not Duplicated With Previous DB Entries"
        ReturnFirstEntry    = "Initial Entry"
        if(len(txtAlphaNAFODivision.get())!=0) & (len(txtNumericNAFODivision.get())!=0):
            entryNAFODivisionCode = (txtAlphaNAFODivision.get())
            Return_Message = UniqueCheck_NAFODivisionCode(entryNAFODivisionCode)
            if (Return_Message == ReturnNotDuplicated)| (Return_Message == ReturnFirstEntry):
                addInvRec_NAFODivisionProfile(txtAlphaNAFODivision.get(), txtAlphaUnitArea.get(), txtNumericNAFODivision.get(), txtNumericUnitArea.get())
                view_NAFODivisionProfile()
                ClearNAFODivisionDetails()
                NAFODivisionTotalEntries()
            else:
                messagebox.showerror('Insert Entry Duplicated Error', ReturnDuplicated)
        else:
            tkinter.messagebox.showinfo("Add Error","Entries can not be empty")

    def UniqueCheck_NAFODivisionCode(entryNAFODivisionCode):
        ReturnDuplicated    = "Insert NAFODivision Code Duplicated With Previous DB Entries"
        ReturnNotDuplicated = "Insert NAFODivision Code Not Duplicated With Previous DB Entries"
        ReturnFirstEntry    = "Initial Entry"
        try:
            entryNAFODivisionCode = (entryNAFODivisionCode)
            sqliteConnection = sqlite3.connect(DB_Lookup_Table)
            cursor = sqliteConnection.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_NAFODivisionProfile ORDER BY `DatabaseUID` ASC ;", sqliteConnection)
            data = pd.DataFrame(Complete_df)
            data = data.reset_index(drop=True)
            TotalEntries = len(data)
            if TotalEntries > 0:
                if (entryNAFODivisionCode in data["AlphaNAFODivision"].unique()) == True: 
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

    def view_NAFODivisionProfile():
        tree1.delete(*tree1.get_children())
        countIndex = 0
        rows = viewData_NAFODivisionProfile()
        for row in rows:
            if countIndex % 2 == 0:
                tree1.insert("", tk.END, values=row, tags =("even",))       
            else:
                tree1.insert("", tk.END, values=row, tags =("odd",))  
            countIndex = countIndex+1
        tree1.tag_configure("even",foreground="black", background="lightblue")
        tree1.tag_configure("odd",foreground="black", background="ghost white")
        
        NAFODivisionTotalEntries()       

    def ClearNAFODivisionDetails():
        txtDatabaseUID.config(state= "normal")
        txtDatabaseUID.delete(0,END)
        txtDatabaseUID.config(state= "disabled")
        txtAlphaNAFODivision.delete(0,END)
        txtAlphaUnitArea.delete(0,END)
        txtNumericNAFODivision.delete(0,END)
        txtNumericUnitArea.delete(0,END)

    def NAFODivisionTotalEntries():
        txtTotalEntries.delete(0,END)
        conn = sqlite3.connect(DB_Lookup_Table)
        Complete_df= pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_NAFODivisionProfile ORDER BY `DatabaseUID` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        TotalEntries = len(data)       
        txtTotalEntries.insert(tk.END,TotalEntries)              
        conn.commit()
        conn.close()

    def delete_NAFODivisionProfile():
        SelectionTree = tree1.selection()
        if len(SelectionTree)>0:
            iDelete = tkinter.messagebox.askyesno("Delete Entry From DFO-NL-ASOP NAFODivision Code Database", 
                        "Confirm If You Want To Delete The Selection Entries From DFO-NL-ASOP NAFODivision Code Database")
            if iDelete >0:
                conn = sqlite3.connect(DB_Lookup_Table)
                cur = conn.cursor()
                if(len(txtAlphaNAFODivision.get())!=0) & (len(txtNumericNAFODivision.get())!=0):
                    for selected_item in tree1.selection():
                        cur.execute("DELETE FROM DFO_NL_ASOP_NAFODivisionProfile WHERE DatabaseUID =? AND AlphaNAFODivision =? AND NumericNAFODivision = ?", (tree1.set(selected_item, '#1'), tree1.set(selected_item, '#2'),tree1.set(selected_item, '#4'), ))
                        conn.commit()
                        tree1.delete(selected_item)
                    conn.commit()
                    conn.close()
                tree1.delete(*tree1.get_children())
                ClearNAFODivisionDetails()
                view_NAFODivisionProfile()
                NAFODivisionTotalEntries()
                return
        else:
            tkinter.messagebox.showinfo("Delete Error","Please Select Entries From VesselClass Code Table To Delete From Database")

    def update_NAFODivisionProfile():
        cur_id = tree1.focus()
        selvalue = tree1.item(cur_id)['values']
        Length_Selected  =  (len(selvalue))
        if Length_Selected != 0:
            SelectionTree = tree1.selection()
            if (len(SelectionTree)>0) & (len(SelectionTree)==1) & (len(SelectionTree)<2):
                iUpdate = tkinter.messagebox.askyesno("Update Entry From DFO-NL-ASOP NAFODivision Code Database", 
                            "Confirm If You Want To Update From DFO-NL-ASOP NAFODivision Code Database")
                if iUpdate >0:
                    for item in SelectionTree:
                        list_item = (tree1.item(item, 'values'))
                        list_item_DatabaseUID = int(list_item[0])
                        AlphaNAFODivision = txtAlphaNAFODivision.get()
                        AlphaUnitArea = txtAlphaUnitArea.get()
                        NumericNAFODivision = txtNumericNAFODivision.get()
                        NumericUnitArea = txtNumericUnitArea.get()
                        conn= sqlite3.connect(DB_Lookup_Table)
                        cur=conn.cursor()
                        if(len(txtAlphaNAFODivision.get())!=0) & (len(txtNumericNAFODivision.get())!=0):
                            cur.execute("UPDATE DFO_NL_ASOP_NAFODivisionProfile SET AlphaNAFODivision = ?,  AlphaUnitArea = ?, NumericNAFODivision = ? , NumericUnitArea = ? WHERE DatabaseUID =?", 
                                (AlphaNAFODivision, AlphaUnitArea, NumericNAFODivision, NumericUnitArea, list_item_DatabaseUID))
                            tree1.delete(*tree1.get_children())
                            tree1.insert("", tk.END,values=(list_item_DatabaseUID, AlphaNAFODivision, AlphaUnitArea, NumericNAFODivision, NumericUnitArea ))
                            conn.commit()
                            conn.close()
                            NAFODivisionTotalEntries() 
                        else:
                            tkinter.messagebox.showerror("Add Error","Entries can not be empty")
            else:
                UpdatePossibleError =  ("Possible Reasons For Update Error: " + '\n' + '\n' + 
                        "1. Please Select One Entry Only From The NAFODivision Table To Update "  + '\n' + '\n' + 
                        "2. Please Donot Select More Than One Entry To Update At The Same time "  + '\n' + '\n' + 
                        "3. Please Do Not Update Without Selecting Entry From NAFODivision Table" )
                tkinter.messagebox.showerror("Update Error Possible Reasons",UpdatePossibleError)

    def ClearNAFODivisionTable():
        tree1.delete(*tree1.get_children())
        txtTotalEntries.delete(0,END)   

    def InventoryRec(event):
        for nm in tree1.selection():
            sd = tree1.item(nm, 'values')
            txtDatabaseUID.config(state= "normal")
            txtDatabaseUID.delete(0,END)
            txtDatabaseUID.insert(tk.END,sd[0]) 
            txtAlphaNAFODivision.delete(0,END)
            txtAlphaNAFODivision.insert(tk.END,sd[1])                
            txtAlphaUnitArea.delete(0,END)
            txtAlphaUnitArea.insert(tk.END,sd[2])
            txtNumericNAFODivision.delete(0,END)
            txtNumericNAFODivision.insert(tk.END,sd[3])
            txtNumericUnitArea.delete(0,END)
            txtNumericUnitArea.insert(tk.END,sd[4])
            txtDatabaseUID.config(state= "disabled")

    def ImportColumnCheck(List_Columns_Import):
        ReturnMatchedMessage    = "Import NAFODivision Code Profile Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import NAFODivision Code Profile Headers MisMatch With Database Headers"
        DB_column_names = ["AlphaNAFODivision", "AlphaUnitArea", "NumericNAFODivision", "NumericUnitArea"]
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
            Import_To_DBStorage.to_sql('DFO_NL_ASOP_NAFODivisionProfile', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def Import_NAFODivision_Profile_CSV():
        ClearNAFODivisionTable()
        ClearNAFODivisionDetails()
        ReturnMatchedMessage    = "Import NAFODivision Code Profile Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import NAFODivision Code Profile Headers MisMatch With Database Headers"
        fileList = filedialog.askopenfilenames(title="Select NAFODivision Code Profile .CSV File/Files", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.")))
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
                            AlphaNAFODivision = (df.loc[:,'AlphaNAFODivision']).fillna(9999999).astype(str, errors='ignore')
                            AlphaUnitArea = (df.loc[:,'AlphaUnitArea']).fillna(9999999).astype(str, errors='ignore')
                            NumericNAFODivision = (df.loc[:,'NumericNAFODivision']).fillna(99999).astype(int, errors='ignore')
                            NumericUnitArea = (df.loc[:,'NumericUnitArea']).fillna(99999).astype(int, errors='ignore')
                            column_names = [AlphaNAFODivision, AlphaUnitArea, NumericNAFODivision,NumericUnitArea]
                            catdf = pd.concat (column_names,axis=1,ignore_index =True)
                            dfList.append(catdf)
                        else:
                            messagebox.showerror('Import File Headers Mismatch', ReturnMisMatchedMessage)
                concatDf = pd.concat(dfList,axis=0, ignore_index =True)
                concatDf.rename(columns={0:'AlphaNAFODivision', 1:'AlphaUnitArea', 2:'NumericNAFODivision', 3:'NumericUnitArea'},inplace = True)
                Raw_Imported_Df = pd.DataFrame(concatDf)
                if (Raw_Imported_Df["AlphaNAFODivision"].isnull().values.any() == True)|\
                (Raw_Imported_Df["NumericNAFODivision"].isnull().values.any() == True):
                    messagebox.showerror("Import Error In CSV File","Duplicated NAFODivisionCode Or Empty NAFODivisionCode/NAFODivisionName Found")
                else:
                    Raw_Imported_Df = pd.DataFrame(concatDf)
                    Raw_Imported_Df['NumericNAFODivision'] = (Raw_Imported_Df.loc[:,['NumericNAFODivision']]).astype(int, errors='ignore')
                    Raw_Imported_Df['NumericUnitArea'] = (Raw_Imported_Df.loc[:,['NumericUnitArea']]).astype(int, errors='ignore')
                    Raw_Imported_Df = Raw_Imported_Df.replace(99999, '')
                    Raw_Imported_Df = Raw_Imported_Df.replace('9999999', 'None')
                    ClearNAFODivisionTable()
                    Import_To_DBStorage(Raw_Imported_Df)
                    view_NAFODivisionProfile()
                    NAFODivisionTotalEntries()
                        
    def ExportNAFODivisionProfileDB():
        try:
            conn = sqlite3.connect(DB_Lookup_Table)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_NAFODivisionProfile ORDER BY `DatabaseUID` ASC ;", conn)
            if len(Complete_df) >0:
                Export_MasterTB_DF  = pd.DataFrame(Complete_df)
                Export_MasterTB_DF.drop(['DatabaseUID'], axis=1, inplace=True)
                Export_MasterTB_DF  = Export_MasterTB_DF.reset_index(drop=True)
                filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                        defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                if len(filename) >0:
                    Export_MasterTB_DF.to_csv(filename,index=None)
                    tkinter.messagebox.showinfo("Master NAFODivision Profile Database Export","Master NAFODivision Coded Profile Database Saved as CSV")
                else:
                    tkinter.messagebox.showinfo("Master NAFODivision Profile Database Export Message","Please Select File Name To Export")
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
    btnAddNAFODivisionProfile = Button(Topframe, text="Add Profile", font=('aerial', 10, 'bold'), height =1, width=22, bd=1, command = add_NAFODivisionProfile)
    btnAddNAFODivisionProfile.grid(row =7, column = 1, padx=0, pady =5, sticky =E)

    btnModifyNAFODivisionProfile = Button(Topframe, text="Modify Profile", font=('aerial', 10, 'bold'), height =1, width=22, bd=1, command = update_NAFODivisionProfile)
    btnModifyNAFODivisionProfile.grid(row =8, column = 1, padx=0, pady =5, sticky =E)

    btnClearNAFODivisionProfile = Button(Topframe, text="Clear Details", font=('aerial', 10, 'bold'), height =1, width=22, bd=1, command = ClearNAFODivisionDetails)
    btnClearNAFODivisionProfile.grid(row =7, column = 0, padx=0, pady =5, sticky =E)

    btnDeleteNAFODivisionProfile = Button(Topframe, text="Delete Profile", font=('aerial', 10, 'bold'), height =1, width=22, bd=1, command = delete_NAFODivisionProfile)
    btnDeleteNAFODivisionProfile.grid(row =8, column = 0, padx=0, pady =5, sticky =E)

    btnClearNAFODivisionTable = Button(Midframe, text="Clear Table", font=('aerial', 10, 'bold'), height =1, width=10, bd=1, command = ClearNAFODivisionTable)
    btnClearNAFODivisionTable.grid(row =6, column = 0, padx=2, pady =2, sticky =W)

    btnViewNAFODivisionProfile = Button(Midframe, text="View NAFODivision Table", font=('aerial', 10, 'bold'), height =1, width=22, bd=1, command = view_NAFODivisionProfile)
    btnViewNAFODivisionProfile.grid(row =6, column = 1, padx=180, pady =2, sticky =W)

    btnImportNAFODivisionTable = Button(Midframe, text="Import Table (.csv)", font=('aerial', 10, 'bold'), height =1, width=15, bd=1, command = Import_NAFODivision_Profile_CSV)
    btnImportNAFODivisionTable.grid(row =6, column = 2, padx=2, pady =2, sticky =W)

    # Adding File Menu 
    menu = Menu(window)
    window.config(menu=menu)
    filemenu  = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=filemenu)  
    filemenu.add_command(label="Export NAFODivision Profile DB", command=ExportNAFODivisionProfileDB)
    filemenu.add_command(label="Exit", command=iExit)

    window.mainloop()











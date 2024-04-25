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

def DFO_NL_ASOP_SpeciesCode_Profile_Table():
    window = tk.Tk()
    window.title ("DFO-NL-ASOP Species Codes Profile")
    window.geometry("900x900+10+10")
    window.config(bg="cadet blue")
    window.resizable(0, 0)

    Topframe = Frame(window, bd = 2, padx= 3, pady= 10, relief = RIDGE)
    Topframe.pack(side = TOP)
    DatabaseUID = IntVar(Topframe, value='')
    SpeciesCode = IntVar(Topframe, value='')
    CommonName = StringVar()
    Phylum = StringVar() 
    SpeciesClass = StringVar()
    SpeciesOrder = StringVar()
    SpeciesFamily = StringVar()
    SpeciesSubFamily = StringVar()
    GenusSpecies = StringVar()
    SpeciesCategory = StringVar() 

    lblTitEntry = Label(Topframe, font=('aerial', 12, 'bold'), text="Species Code Details:")
    lblTitEntry.grid(row =0, column = 0, padx=0, pady =2, sticky =W, rowspan =1)
    lblDatabaseUID = Label(Topframe, font=('aerial', 10, 'bold'), text = "1. Database UID :", padx =0, pady= 2)
    lblDatabaseUID.grid(row =2, column = 0, padx=0, pady =2, sticky =W)
    txtDatabaseUID  = Entry(Topframe, state=DISABLED, font=('aerial', 12, 'bold'),textvariable= DatabaseUID, width = 10)
    txtDatabaseUID.grid(row =2, column = 1, padx=5, pady =2, sticky =W)

    lblSpeciesCode = Label(Topframe, font=('aerial', 10, 'bold'), text = "2. SpeciesCode :", padx =0, pady= 2)
    lblSpeciesCode.grid(row =3, column = 0, padx=0, pady =2, sticky =W)
    txtSpeciesCode  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable= SpeciesCode, width = 25)
    txtSpeciesCode.grid(row =3, column = 1, padx=5, pady =2, sticky =W)

    lblCommonName = Label(Topframe, font=('aerial', 10, 'bold'), text = "3. Common Name :", padx =0, pady= 2)
    lblCommonName.grid(row =4, column = 0, padx=0, pady =2, sticky =W)
    txtCommonName  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable = CommonName, width = 60)
    txtCommonName.grid(row =4, column = 1, padx=5, pady =2, sticky =W)

    lblPhylum = Label(Topframe, font=('aerial', 10, 'bold'), text = "4. Phylum :", padx =0, pady= 2)
    lblPhylum.grid(row =5, column = 0, padx=0, pady =2, sticky =W)
    txtPhylum  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable = Phylum, width = 60)
    txtPhylum.grid(row =5, column = 1, padx=5, pady =2, sticky =W)

    lblSpeciesClass = Label(Topframe, font=('aerial', 10, 'bold'), text = "5. SpeciesClass :", padx =0, pady= 2)
    lblSpeciesClass.grid(row =6, column = 0, padx=0, pady =2, sticky =W)
    txtSpeciesClass  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable = SpeciesClass, width = 60)
    txtSpeciesClass.grid(row =6, column = 1, padx=5, pady =2, sticky =W)

    lblSpeciesOrder = Label(Topframe, font=('aerial', 10, 'bold'), text = "6. SpeciesOrder :", padx =0, pady= 2)
    lblSpeciesOrder.grid(row =7, column = 0, padx=0, pady =2, sticky =W)
    txtSpeciesOrder  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable = SpeciesOrder, width = 60)
    txtSpeciesOrder.grid(row =7, column = 1, padx=5, pady =2, sticky =W)

    lblSpeciesFamily = Label(Topframe, font=('aerial', 10, 'bold'), text = "7. SpeciesFamily :", padx =0, pady= 2)
    lblSpeciesFamily.grid(row =8, column = 0, padx=0, pady =2, sticky =W)
    txtSpeciesFamily  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable = SpeciesFamily, width = 60)
    txtSpeciesFamily.grid(row =8, column = 1, padx=5, pady =2, sticky =W)

    lblSpeciesSubFamily = Label(Topframe, font=('aerial', 10, 'bold'), text = "8. SpeciesSubFamily :", padx =0, pady= 2)
    lblSpeciesSubFamily.grid(row =9, column = 0, padx=0, pady =2, sticky =W)
    txtSpeciesSubFamily  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable = SpeciesSubFamily, width = 60)
    txtSpeciesSubFamily.grid(row =9, column = 1, padx=5, pady =2, sticky =W)

    lblGenusSpecies = Label(Topframe, font=('aerial', 10, 'bold'), text = "9. GenusSpecies :", padx =0, pady= 2)
    lblGenusSpecies.grid(row =10, column = 0, padx=0, pady =2, sticky =W)
    txtGenusSpecies  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable = GenusSpecies, width = 60)
    txtGenusSpecies.grid(row =10, column = 1, padx=5, pady =2, sticky =W)

    lblSpeciesCategory = Label(Topframe, font=('aerial', 10, 'bold'), text = "10. SpeciesCategory :", padx =0, pady= 2)
    lblSpeciesCategory.grid(row =11, column = 0, padx=0, pady =2, sticky =W)
    txtSpeciesCategory  = Entry(Topframe, font=('aerial', 12, 'bold'),textvariable = SpeciesCategory, width = 60)
    txtSpeciesCategory.grid(row =11, column = 1, padx=5, pady =2, sticky =W)

    Midframe = Frame(window, bd = 2, padx= 3, pady= 0, relief = RIDGE, bg="cadet blue")
    Midframe.pack(side = TOP)

    TableMargin1 = Frame(window, bd = 2, padx= 10, pady= 2, relief = RIDGE)
    TableMargin1.pack(side=TOP)
    TableMargin1.pack(side=LEFT)
    tree1 = ttk.Treeview(TableMargin1, column=("column1", "column2", "column3", 
                        "column4", "column5", "column6", "column7", "column8", 
                        "column9", "column10"), height=20, show='headings')
    scrollbary = ttk.Scrollbar(TableMargin1, orient ="vertical", command=tree1.yview)
    scrollbary.pack(side ='right', fill ='y')
    tree1.configure(yscrollcommand = scrollbary.set)
    scrollbarx = ttk.Scrollbar(TableMargin1, orient ="horizontal", command=tree1.xview)
    scrollbarx.pack(side ='bottom', fill ='x')
    tree1.configure(xscrollcommand = scrollbarx.set)
    tree1.heading("#1", text="Database UID", anchor=tk.CENTER)
    tree1.heading("#2", text="SpeciesCode", anchor=tk.CENTER)
    tree1.heading("#3", text="Common Name", anchor=W)
    tree1.heading("#4", text="Phylum", anchor=W)
    tree1.heading("#5", text="SpeciesClass", anchor=W)
    tree1.heading("#6", text="SpeciesOrder", anchor=W)
    tree1.heading("#7", text="SpeciesFamily", anchor=W)
    tree1.heading("#8", text="SpeciesSubFamily", anchor=W)
    tree1.heading("#9", text="GenusSpecies", anchor=W)
    tree1.heading("#10", text="SpeciesCategory", anchor=W)
    tree1.column('#1', stretch=NO, minwidth=0, width=100, anchor=tk.CENTER)            
    tree1.column('#2', stretch=NO, minwidth=0, width=150, anchor=tk.CENTER)
    tree1.column('#3', stretch=NO, minwidth=0, width=150, anchor=W)
    tree1.column('#4', stretch=NO, minwidth=0, width=150, anchor=W)
    tree1.column('#5', stretch=NO, minwidth=0, width=150, anchor=W)            
    tree1.column('#6', stretch=NO, minwidth=0, width=150, anchor=W)
    tree1.column('#7', stretch=NO, minwidth=0, width=150, anchor=W)
    tree1.column('#8', stretch=NO, minwidth=0, width=150, anchor=W)
    tree1.column('#9', stretch=NO, minwidth=0, width=150, anchor=W)
    tree1.column('#10', stretch=NO, minwidth=0, width=150, anchor=W)
    style = ttk.Style(window)
    style.configure(".", font=('aerial', 10), foreground="black")
    style.configure("Treeview", foreground='black')
    style.configure("Treeview.Heading",font=('aerial', 10,'bold'), background='Ghost White', foreground='blue',fieldbackground='Ghost White')
    tree1.pack()

    lbl_TotalEntries = Label(Midframe, font=('aerial', 10, 'bold'), text="Total Entries :")
    lbl_TotalEntries.grid(row =0, column = 4, padx=6, pady =2)
    TotalEntries = IntVar(Midframe, value='')
    txtTotalEntries = Entry(Midframe, font=('aerial', 10, 'bold'),textvariable = TotalEntries, width = 8)
    txtTotalEntries.grid(row =0, column = 5, padx=1, pady =2, ipady =5, sticky =W)

    DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")
    # DB_Lookup_Table = "./DFO_NL_ASOP_Lookup_Table.db"

    # # All Functions defining
    def addInvRec_SpeciesProfile(SpeciesCode, CommonName, Phylum, SpeciesClass, SpeciesOrder, SpeciesFamily, SpeciesSubFamily, GenusSpecies, SpeciesCategory):
        sqliteConnection= sqlite3.connect(DB_Lookup_Table)
        cur=sqliteConnection.cursor()
        cur.execute("INSERT INTO DFO_NL_ASOP_SpeciesCodeProfile (DatabaseUID, SpeciesCode, CommonName, Phylum, SpeciesClass, SpeciesOrder, SpeciesFamily, SpeciesSubFamily, GenusSpecies, SpeciesCategory) VALUES (?,?,?,?,?,?,?,?,?,?)",[int(SpeciesCode)+10000, SpeciesCode, CommonName, Phylum, SpeciesClass, SpeciesOrder, SpeciesFamily, SpeciesSubFamily, GenusSpecies, SpeciesCategory])
        sqliteConnection.commit()
        sqliteConnection.close()

    def viewData_SpeciesProfile():
        con= sqlite3.connect(DB_Lookup_Table)
        cur=con.cursor()
        cur.execute("SELECT * FROM DFO_NL_ASOP_SpeciesCodeProfile ORDER BY `SpeciesCode` ASC")
        rows=cur.fetchall()
        con.close()
        return rows

    def iExit():
        iExit= tkinter.messagebox.askyesno("DFO-NL-ASOP Species Codes Profile", "Confirm If You Want To Exit")
        if iExit >0:
            window.destroy()
            return

    def add_SpeciesProfile():
        ReturnDuplicated    = "Insert Species Code Duplicated With Previous DB Entries"
        ReturnNotDuplicated = "Insert Species Code Not Duplicated With Previous DB Entries"
        ReturnFirstEntry    = "Initial Entry"
        if(len(txtSpeciesCode.get())!=0) & (len(txtCommonName.get())!=0):
            entrySpeciesCode = int(txtSpeciesCode.get())
            Return_Message = UniqueCheck_SpeciesCode(entrySpeciesCode)
            if (Return_Message == ReturnNotDuplicated)| (Return_Message == ReturnFirstEntry):
                addInvRec_SpeciesProfile(txtSpeciesCode.get(), txtCommonName.get(), txtPhylum.get(), txtSpeciesClass.get(), txtSpeciesOrder.get(), txtSpeciesFamily.get(), txtSpeciesSubFamily.get(), txtGenusSpecies.get(), txtSpeciesCategory.get())
                view_SpeciesProfile()
                ClearSpeciesDetails()
                SpeciesTotalEntries()
            else:
                messagebox.showerror('Insert Entry Duplicated Error', ReturnDuplicated)
        else:
            tkinter.messagebox.showinfo("Add Error","Entries can not be empty")

    def view_SpeciesProfile():
        tree1.delete(*tree1.get_children())
        for row in viewData_SpeciesProfile():
            tree1.insert("", tk.END, values=row)
        SpeciesTotalEntries()       

    def ClearSpeciesDetails():
        txtDatabaseUID.config(state= "normal")
        txtDatabaseUID.delete(0,END)
        txtDatabaseUID.config(state= "disabled")
        txtSpeciesCode.delete(0,END)
        txtCommonName.delete(0,END)
        txtPhylum.delete(0,END)
        txtSpeciesClass.delete(0,END)
        txtSpeciesOrder.delete(0,END)
        txtSpeciesFamily.delete(0,END)
        txtSpeciesSubFamily.delete(0,END)
        txtGenusSpecies.delete(0,END)
        txtSpeciesCategory.delete(0,END)

    def delete_SpeciesProfile():
        SelectionTree = tree1.selection()
        if len(SelectionTree)>0:
            iDelete = tkinter.messagebox.askyesno("Delete Entry From DFO-NL-ASOP Species Code Database", 
                        "Confirm If You Want To Delete The Selection Entries From DFO-NL-ASOP Species Code Database")
            if iDelete >0:
                conn = sqlite3.connect(DB_Lookup_Table)
                cur = conn.cursor()
                if(len(txtSpeciesCode.get())!=0) & (len(txtCommonName.get())!=0):
                    for selected_item in tree1.selection():
                        cur.execute("DELETE FROM DFO_NL_ASOP_SpeciesCodeProfile WHERE DatabaseUID =? AND SpeciesCode =? AND CommonName = ? ", (tree1.set(selected_item, '#1'), tree1.set(selected_item, '#2'),tree1.set(selected_item, '#3'),))
                        conn.commit()
                        tree1.delete(selected_item)
                    conn.commit()
                    conn.close()
                tree1.delete(*tree1.get_children())
                ClearSpeciesDetails()
                view_SpeciesProfile()
                SpeciesTotalEntries()
                return
        else:
            tkinter.messagebox.showinfo("Delete Error","Please Select Entries From Species Code Table To Delete From Database")

    def update_SpeciesProfile():
        cur_id = tree1.focus()
        selvalue = tree1.item(cur_id)['values']
        Length_Selected  =  (len(selvalue))
        if Length_Selected != 0:
            SelectionTree = tree1.selection()
            if (len(SelectionTree)>0) & (len(SelectionTree)==1) & (len(SelectionTree)<2):
                iUpdate = tkinter.messagebox.askyesno("Update Entry From DFO-NL-ASOP Species Code Database", 
                            "Confirm If You Want To Update From DFO-NL-ASOP Species Code Database")
                if iUpdate >0:
                    for item in SelectionTree:
                        list_item = (tree1.item(item, 'values'))
                        list_item_DatabaseUID = int(list_item[0])
                        SpeciesCode = txtSpeciesCode.get()
                        CommonName = txtCommonName.get()
                        Phylum = txtPhylum.get()
                        SpeciesClass = txtSpeciesClass.get()
                        SpeciesOrder = txtSpeciesOrder.get()
                        SpeciesFamily = txtSpeciesFamily.get()
                        SpeciesSubFamily = txtSpeciesSubFamily.get()
                        GenusSpecies = txtGenusSpecies.get()
                        SpeciesCategory = txtSpeciesCategory.get()

                        conn= sqlite3.connect(DB_Lookup_Table)
                        cur=conn.cursor()
                        if(len(txtSpeciesCode.get())!=0) & (len(txtCommonName.get())!=0):
                            cur.execute("UPDATE DFO_NL_ASOP_SpeciesCodeProfile SET SpeciesCode = ?,  CommonName = ?, Phylum = ?,\
                                SpeciesClass = ?, SpeciesOrder = ?, SpeciesFamily = ?, SpeciesSubFamily =?, GenusSpecies = ?, SpeciesCategory = ? WHERE DatabaseUID =?", 
                                (SpeciesCode, CommonName, Phylum, SpeciesClass, SpeciesOrder, SpeciesFamily, SpeciesSubFamily, GenusSpecies, SpeciesCategory, list_item_DatabaseUID))
                            tree1.delete(*tree1.get_children())
                            tree1.insert("", tk.END,values=(list_item_DatabaseUID, SpeciesCode, CommonName, Phylum, SpeciesClass, SpeciesOrder, SpeciesFamily, SpeciesSubFamily, GenusSpecies, SpeciesCategory ))
                            conn.commit()
                            conn.close()
                            SpeciesTotalEntries() 
                        else:
                            tkinter.messagebox.showerror("Add Error","Entries can not be empty")
            else:
                UpdatePossibleError =  ("Possible Reasons For Update Error: " + '\n' + '\n' + 
                        "1. Please Select One Entry Only From The Species Table To Update "  + '\n' + '\n' + 
                        "2. Please Donot Select More Than One Entry To Update At The Same time "  + '\n' + '\n' + 
                        "3. Please Do Not Update Without Selecting Entry From Species Table" )
                tkinter.messagebox.showerror("Update Error Possible Reasons",UpdatePossibleError)

    def ClearSpeciesTable():
        tree1.delete(*tree1.get_children())
        txtTotalEntries.delete(0,END)   

    def InventoryRec(event):
        for nm in tree1.selection():
            sd = tree1.item(nm, 'values')
            txtDatabaseUID.config(state= "normal")
            txtDatabaseUID.delete(0,END)
            txtDatabaseUID.insert(tk.END,sd[0]) 
            txtSpeciesCode.delete(0,END)
            txtSpeciesCode.insert(tk.END,sd[1])                
            txtCommonName.delete(0,END)
            txtCommonName.insert(tk.END,sd[2])
            txtPhylum.delete(0,END)
            txtPhylum.insert(tk.END,sd[3])
            txtSpeciesClass.delete(0,END)
            txtSpeciesClass.insert(tk.END,sd[4])
            txtSpeciesOrder.delete(0,END)
            txtSpeciesOrder.insert(tk.END,sd[5])
            txtSpeciesFamily.delete(0,END)
            txtSpeciesFamily.insert(tk.END,sd[6])
            txtSpeciesSubFamily.delete(0,END)
            txtSpeciesSubFamily.insert(tk.END,sd[7])
            txtGenusSpecies.delete(0,END)
            txtGenusSpecies.insert(tk.END,sd[8])
            txtSpeciesCategory.delete(0,END)
            txtSpeciesCategory.insert(tk.END,sd[9])
            txtDatabaseUID.config(state= "disabled")

    def ImportColumnCheck(List_Columns_Import):
        ReturnMatchedMessage    = "Import Species Code Profile Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Species Code Profile Headers MisMatch With Database Headers"
        DB_column_names = ["SpeciesCode", "CommonName", "Phylum", "SpeciesClass", "SpeciesOrder", "SpeciesFamily","SpeciesSubFamily" ,"GenusSpecies", "SpeciesCategory"]
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
            Import_To_DBStorage.to_sql('DFO_NL_ASOP_SpeciesCodeProfile', sqliteConnection, if_exists="replace", index =False)
            sqliteConnection.commit()
        except sqlite3.Error as error:
            print('Error occured - ', error)
        finally:
            if sqliteConnection:
                cursor.close()
                sqliteConnection.close()

    def Import_Species_Profile_CSV():
        ClearSpeciesTable()
        ClearSpeciesDetails()
        ReturnMatchedMessage    = "Import Species Code Profile Headers Matched With Database Headers"
        ReturnMisMatchedMessage = "Import Species Code Profile Headers MisMatch With Database Headers"
        fileList = filedialog.askopenfilenames(title="Select Species Code Profile .CSV File/Files", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.")))
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
                            SpeciesCode = (df.loc[:,'SpeciesCode'])
                            CommonName = (df.loc[:,'CommonName'])
                            Phylum = (df.loc[:,'Phylum'])
                            SpeciesClass = (df.loc[:,'SpeciesClass'])
                            SpeciesOrder = (df.loc[:,'SpeciesOrder'])
                            SpeciesFamily = (df.loc[:,'SpeciesFamily'])
                            SpeciesSubFamily = (df.loc[:,'SpeciesSubFamily'])
                            GenusSpecies = (df.loc[:,'GenusSpecies'])
                            SpeciesCategory = (df.loc[:,'SpeciesCategory'])
                            column_names = [SpeciesCode, CommonName, Phylum, SpeciesClass, SpeciesOrder, SpeciesFamily, SpeciesSubFamily, GenusSpecies, SpeciesCategory]
                            catdf = pd.concat (column_names,axis=1,ignore_index =True)
                            dfList.append(catdf)
                        else:
                            messagebox.showerror('Import File Headers Mismatch', ReturnMisMatchedMessage)
                
                concatDf = pd.concat(dfList,axis=0, ignore_index =True)
                concatDf.rename(columns={0:'SpeciesCode', 1:'CommonName', 2:'Phylum', 3:'SpeciesClass', 4:'SpeciesOrder', 
                                        5:'SpeciesFamily', 6:'SpeciesSubFamily', 7:'GenusSpecies', 8:'SpeciesCategory'},inplace = True)
                Raw_Imported_Df = pd.DataFrame(concatDf)
                if (Raw_Imported_Df["SpeciesCode"].duplicated().values.any() == True) | \
                    (Raw_Imported_Df["SpeciesCode"].isnull().values.any() == True)|\
                    (Raw_Imported_Df["CommonName"].isnull().values.any() == True):
                    messagebox.showerror("Import Error In CSV File","Duplicated SpeciesCode Or Empty SpeciesCode/SpeciesName Found")
                else:
                    Raw_Imported_Df = pd.DataFrame(concatDf)
                    ClearSpeciesTable()
                    Import_To_DBStorage(Raw_Imported_Df)
                    view_SpeciesProfile()
                    SpeciesTotalEntries()
                        
    def SpeciesTotalEntries():
        txtTotalEntries.delete(0,END)
        conn = sqlite3.connect(DB_Lookup_Table)
        Complete_df= pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_SpeciesCodeProfile ORDER BY `SpeciesCode` ASC;", conn)
        data = pd.DataFrame(Complete_df)
        data = data.reset_index(drop=True)
        TotalEntries = len(data)       
        txtTotalEntries.insert(tk.END,TotalEntries)              
        conn.commit()
        conn.close()

    def UniqueCheck_SpeciesCode(entrySpeciesCode):
        ReturnDuplicated    = "Insert Species Code Duplicated With Previous DB Entries"
        ReturnNotDuplicated = "Insert Species Code Not Duplicated With Previous DB Entries"
        ReturnFirstEntry    = "Initial Entry"
        try:
            entrySpeciesCode = int(entrySpeciesCode)
            sqliteConnection = sqlite3.connect(DB_Lookup_Table)
            cursor = sqliteConnection.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_SpeciesCodeProfile ORDER BY `SpeciesCode` ASC ;", sqliteConnection)
            data = pd.DataFrame(Complete_df)
            data = data.reset_index(drop=True)
            TotalEntries = len(data)
            if TotalEntries > 0:
                if (entrySpeciesCode in data["SpeciesCode"].unique()) == True: 
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

    def ExportSpeciesProfileDB():
        try:
            conn = sqlite3.connect(DB_Lookup_Table)
            cursor = conn.cursor()
            Complete_df = pd.read_sql_query("SELECT * FROM DFO_NL_ASOP_SpeciesCodeProfile ORDER BY `SpeciesCode` ASC ;", conn)
            if len(Complete_df) >0:
                Export_MasterTB_DF  = pd.DataFrame(Complete_df)
                Export_MasterTB_DF.drop(['DatabaseUID'], axis=1, inplace=True)
                Export_MasterTB_DF  = Export_MasterTB_DF.reset_index(drop=True)
                filename = tkinter.filedialog.asksaveasfilename(initialdir = "/" ,title = "Select file",\
                        defaultextension='.csv', filetypes = (("CSV file",".csv"),("Excel file",".xlsx")))
                if len(filename) >0:
                    Export_MasterTB_DF.to_csv(filename,index=None)
                    tkinter.messagebox.showinfo("Master Species Profile Database Export","Master Species Coded Profile Database Saved as CSV")
                else:
                    tkinter.messagebox.showinfo("Master Species Profile Database Export Message","Please Select File Name To Export")
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
    btnAddSpeciesProfile = Button(Topframe, text="Add Species Profile", font=('aerial', 10, 'bold'), height =1, width=22, bd=2, command = add_SpeciesProfile)
    btnAddSpeciesProfile.grid(row =12, column = 1, padx=0, pady =5, sticky =E)

    btnModifySpeciesProfile = Button(Topframe, text="Modify Species Profile", font=('aerial', 10, 'bold'), height =1, width=22, bd=2, command = update_SpeciesProfile)
    btnModifySpeciesProfile.grid(row =13, column = 1, padx=0, pady =5, sticky =E)

    btnClearSpeciesProfile = Button(Topframe, text="Clear Species Details", font=('aerial', 10, 'bold'), height =1, width=22, bd=2, command = ClearSpeciesDetails)
    btnClearSpeciesProfile.grid(row =12, column = 0, padx=0, pady =5, sticky =E)

    btnDeleteSpeciesProfile = Button(Topframe, text="Delete Species Profile", font=('aerial', 10, 'bold'), height =1, width=22, bd=2, command = delete_SpeciesProfile)
    btnDeleteSpeciesProfile.grid(row =13, column = 0, padx=0, pady =5, sticky =E)

    btnClearSpeciesTable = Button(Midframe, text="Clear Table ", font=('aerial', 11, 'bold'), height =1, width=10, bd=2, command = ClearSpeciesTable)
    btnClearSpeciesTable.grid(row =0, column = 1, padx=2, pady =2, sticky =W)

    btnViewSpeciesProfile = Button(Midframe, text="View SpeciesCode Table", font=('aerial', 11, 'bold'), height =1, width=21, bd=2, command = view_SpeciesProfile)
    btnViewSpeciesProfile.grid(row =0, column = 2, padx=120, pady =2, sticky =W)

    btnImportSpeciesTable = Button(Midframe, text="Import Table (.csv)", font=('aerial', 11, 'bold'), height =1, width=17, bd=2, command = Import_Species_Profile_CSV)
    btnImportSpeciesTable.grid(row =0, column = 3, padx=2, pady =2, sticky =W)

    ## Adding File Menu 
    menu = Menu(window)
    window.config(menu=menu)
    filemenu  = Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=filemenu)  
    filemenu.add_command(label="Export Species Profile DB", command=ExportSpeciesProfileDB)
    filemenu.add_command(label="Exit", command=iExit)

    window.mainloop()











import sqlite3
#backend

DB_Set_Catch_Misc = ("./BackEnd/Sqlite3_DB/SetCatch_Misc_DB/DFO_NL_ASOP_Set_Catch_Misc.db")

def get_DB_Set_Catch_Misc():
    conn = sqlite3.connect(DB_Set_Catch_Misc)
    return conn

def DFO_NL_ASOP_Set_Catch_Misc():
    con= sqlite3.connect(DB_Set_Catch_Misc)
    cur=con.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_SetCatch_TombstoneQCFailOnImport(\
                Year integer, ASOCCode integer, DeploymentNumber integer, \
                SetNumber integer, DeploymentUID, QC_Variable, QC_Message)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_SetCatch_DuplicateQCFailOnImport(\
                Year integer, ASOCCode integer, DeploymentNumber integer, \
                SetNumber integer, DeploymentUID, QC_Variable, QC_Message)")
    
    con.commit()
    cur.close()
    con.close()






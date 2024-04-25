import sqlite3
#backend

DB_SetCatch_Validation_LookUpTable = ("./BackEnd/Sqlite3_DB/QC_Check_LookupConsistency_DB/DFO_NL_ASOP_SetCatch_QCLookupTables.db")

def get_DB_SetCatch_Validation_LookUpTable():
    conn = sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
    return conn

def DFO_NL_ASOP_LookUpTableValidation_DB():
    con= sqlite3.connect(DB_SetCatch_Validation_LookUpTable)
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLookUpTable_ASOCCode (DataBase_ID, RecordIdentifier, DeploymentUID, ASOCCode, DeploymentIdentifier)")
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLookUpTable_Country (DataBase_ID, RecordIdentifier, DeploymentUID, Country, DeploymentIdentifier)")
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLookUpTable_DataSource (DataBase_ID, RecordIdentifier, DeploymentUID, DataSource, DeploymentIdentifier)")
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLookUpTable_GearDamage (DataBase_ID, RecordIdentifier, DeploymentUID, GearDamage, DeploymentIdentifier)")
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLookUpTable_GearType (DataBase_ID, RecordIdentifier, DeploymentUID, GearType, DeploymentIdentifier)")
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLookUpTable_Quota (DataBase_ID, RecordIdentifier, DeploymentUID, Quota, DeploymentIdentifier)")
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLookUpTable_SetType (DataBase_ID, RecordIdentifier, DeploymentUID, SetType, DeploymentIdentifier)")
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLookUpTable_SpeciesCode (DataBase_ID, RecordIdentifier, DeploymentUID, RecordType, SpeciesCode, DeploymentIdentifier)")
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLookUpTable_DirectedSpecies (DataBase_ID, RecordIdentifier, DeploymentUID, RecordType, DirectedSpecies, DeploymentIdentifier)")
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLookUpTable_VesselClass (DataBase_ID, RecordIdentifier, DeploymentUID, VesselClass, DeploymentIdentifier)")
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLookUpTable_NAFODivision (DataBase_ID, RecordIdentifier, DeploymentUID, NAFODivision, UnitArea, DeploymentIdentifier)")
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedLookUpTable_UnitArea (DataBase_ID, RecordIdentifier, DeploymentUID, NAFODivision, UnitArea, DeploymentIdentifier)")

    con.commit()
    cur.close()
    con.close()


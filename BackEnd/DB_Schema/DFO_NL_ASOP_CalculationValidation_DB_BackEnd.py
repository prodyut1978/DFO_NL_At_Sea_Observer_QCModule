import sqlite3
#backend

DB_SetCatch_Val_Calculation = ("./BackEnd/Sqlite3_DB/QC_Check_CalculationConsistency_DB/DFO_NL_ASOP_SetCatch_Calculation.db")

def get_DB_SetCatch_Validation_Calculation():
    conn = sqlite3.connect(DB_SetCatch_Val_Calculation)
    return conn

def DFO_NL_ASOP_CalculationValidation_DB():
    con= sqlite3.connect(DB_SetCatch_Val_Calculation)
    cur=con.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_NAFO_AreaProfileImported (NAFO_ID, \
                NAFOSubArea, NAFODivision, NAFOSubDivision, NAFOLabel, NAFOPointOrder, NAFO_Latitude, NAFO_Longitude)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_NAFO_AreaQCAnalysis (DeploymentUID, \
                RecordType, GearType, NAFODivision, StartLatitude, StartLongitude,\
                EndLatitude, EndLongitude, StartPoints, EndPoints, \
                NAFOValidityCheck_StartPoints, NAFOValidityCheck_EndPoints,\
                Assigned_NAFOPloygon, Calculated_NAFOPolygon)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_Unit_AreaProfileImported (UnitArea_ID, \
                NAFODivision, PointOrder, UnitArea, UnitArea_Latitude, UnitArea_Longitude, UnitAreaLabel)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_UnitAreaQCAnalysis (DeploymentUID, \
                RecordType, GearType, NAFODivision, UnitArea, StartLatitude, StartLongitude,\
                EndLatitude, EndLongitude, StartPoints, EndPoints, \
                UAValidityCheck_StartPoints, UAValidityCheck_EndPoints, \
                Assigned_UnitAreaPolygon, Calculated_UnitAreaPolygon)")
    con.commit()
    cur.close()
    con.close()


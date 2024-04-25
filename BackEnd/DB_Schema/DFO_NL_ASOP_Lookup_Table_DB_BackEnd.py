import sqlite3
#backend

DB_Lookup_Table = ("./BackEnd/Sqlite3_DB/LookupTable_DB/DFO_NL_ASOP_Lookup_Table.db")

def get_DB_Lookup_Table():
    conn = sqlite3.connect(DB_Lookup_Table)
    return conn

def DFO_NL_ASOP_Lookup_Table_DB():
    con= sqlite3.connect(DB_Lookup_Table)
    cur=con.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_ASOCCodeProfile(DatabaseUID integer UNIQUE NOT NULL,\
                 ASOCCode integer UNIQUE NOT NULL, ASOCName text, Comments text)")

    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_CountryProfile(DatabaseUID integer UNIQUE NOT NULL,\
                CountryCode integer UNIQUE NOT NULL, CountryName text, Comments text)")

    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_DataSourceProfile(DatabaseUID integer UNIQUE NOT NULL, \
                DataSourceCode integer UNIQUE NOT NULL, DataSourceName text, Comments text)")

    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_GearDamageProfile(DatabaseUID integer UNIQUE NOT NULL, \
                GearDamageCode integer UNIQUE NOT NULL, GearDamageName text, Comments text)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_GearTypeProfile(DatabaseUID integer UNIQUE NOT NULL, \
                GearTypeCode integer UNIQUE NOT NULL, GearTypeName text, Comments text)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_QuotaProfile(DatabaseUID integer UNIQUE NOT NULL, \
                QuotaCode integer UNIQUE NOT NULL, QuotaName text, Comments text)")

    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_SetTypeProfile(DatabaseUID integer UNIQUE NOT NULL, \
                SetTypeCode integer UNIQUE NOT NULL, SetTypeName text, Comments text)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_SpeciesCodeProfile(DatabaseUID integer UNIQUE NOT NULL, \
                SpeciesCode integer UNIQUE NOT NULL, CommonName text, Phylum text, SpeciesClass text, \
                SpeciesOrder text, SpeciesFamily text, SpeciesSubFamily text, GenusSpecies text, SpeciesCategory text)")

    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_VesselClassProfile(DatabaseUID integer UNIQUE NOT NULL, \
                VesselClassCode integer UNIQUE NOT NULL, VesselClassName text, Comments text)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_NAFODivisionProfile(DatabaseUID integer UNIQUE NOT NULL, \
                AlphaNAFODivision text, AlphaUnitArea text, NumericNAFODivision, NumericUnitArea)")
    
    con.commit()
    cur.close()
    con.close()



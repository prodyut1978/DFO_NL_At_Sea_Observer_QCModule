#Front End


import pandas as pd
import pickle

## Database connections
DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")
## Pickle Location
Pickle_FileNameImport ="./Pickle_MetaData/ImportFileName.pickle"

def GetPickledImportedFileName():
    with open(Pickle_FileNameImport, 'rb') as f:
        FileNameImport = pickle.load(f)
    return FileNameImport

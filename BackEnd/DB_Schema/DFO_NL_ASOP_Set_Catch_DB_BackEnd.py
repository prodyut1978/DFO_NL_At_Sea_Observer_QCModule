import sqlite3
#backend

DB_Set_Catch_Analysis = ("./BackEnd/Sqlite3_DB/SetCatch_DB/DFO_NL_ASOP_Set_Catch_Analysis.db")

def get_DB_Set_Catch_Analysis():
    conn = sqlite3.connect(DB_Set_Catch_Analysis)
    return conn


def DFO_NL_ASOP_Set_Catch_Analysis():
    con= sqlite3.connect(DB_Set_Catch_Analysis)
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_Set_Catch_Analysis_IMPORT(\
                DataBase_ID integer PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, RecordIdentifier integer UNIQUE NOT NULL, DeploymentUID,\
                ASOCCode integer, ObserverNumber text, Year integer,\
                DeploymentNumber integer, SubTripNumber text, SetNumber integer,\
                Country integer, Quota integer, SetType integer,\
                VesselSideNumber text, VesselClass, VesselLength,\
                VesselHorsepower, Day integer, Month integer,\
                HaulDay integer, HaulMonth integer, StartTime,\
                Duration, PositionPrecision, StartLatitude real,\
                StartLongitude real, EndLatitude real, EndLongitude real,\
                NAFODivision text, UnitArea text, StatisticalArea,\
                InOut200MileLimit, GearType, CodendMeshSize,\
                MeshSizeMG, MeshSizeFG, RollerBobbbinDiameter,\
                NumberGillnets, AverageGillnetLength, GrateBarSpacing,\
                FootropeLength, NumberWindows, NumberHooks,\
                NumberPots, NumberPotReleasedCrab, GearDamage,\
                AverageTowSpeed, AverageDepth, DataSource integer,\
                DirectedSpecies, NumberSpecies, RecordType,\
                DetailedCatchSpeciesCompCode text, LogbookIDNumber1, LogbookIDNumber2,\
                SpeciesCode, KeptWeight,  DiscardWeight, \
                EstimatedWeightReleasedCrab, NumberIndividuals)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_Set_Catch_TEMP_IMPORT(\
                RecordIdentifier integer UNIQUE NOT NULL, DeploymentUID,\
                ASOCCode integer, ObserverNumber, Year integer,\
                DeploymentNumber integer, SubTripNumber, SetNumber integer,\
                Country integer, Quota integer, SetType integer,\
                VesselSideNumber, VesselClass integer, VesselLength,\
                VesselHorsepower, Day integer, Month integer,\
                HaulDay integer, HaulMonth integer, StartTime,\
                Duration, PositionPrecision, StartLatitude real,\
                StartLongitude real, EndLatitude real, EndLongitude real,\
                NAFODivision, UnitArea, StatisticalArea,\
                InOut200MileLimit, GearType, CodendMeshSize,\
                MeshSizeMG, MeshSizeFG, RollerBobbbinDiameter,\
                NumberGillnets, AverageGillnetLength, GrateBarSpacing,\
                FootropeLength, NumberWindows, NumberHooks,\
                NumberPots, NumberPotReleasedCrab, GearDamage,\
                AverageTowSpeed, AverageDepth, DataSource,\
                DirectedSpecies, NumberSpecies, RecordType,\
                DetailedCatchSpeciesCompCode, LogbookIDNumber1, LogbookIDNumber2,\
                SpeciesCode, KeptWeight, DiscardWeight,\
                EstimatedWeightReleasedCrab, NumberIndividuals)")

    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_Set_Catch_MultiSearchTempStorage(\
            DataBase_ID integer, RecordIdentifier integer, DeploymentUID,\
            ASOCCode integer, ObserverNumber, Year integer,\
            DeploymentNumber integer, SubTripNumber, SetNumber integer,\
            Country integer, Quota integer, SetType integer,\
            VesselSideNumber, VesselClass integer, VesselLength,\
            VesselHorsepower, Day integer, Month integer,\
            HaulDay integer, HaulMonth integer, StartTime,\
            Duration, PositionPrecision, StartLatitude real,\
            StartLongitude real, EndLatitude real, EndLongitude real,\
            NAFODivision, UnitArea, StatisticalArea,\
            InOut200MileLimit, GearType, CodendMeshSize,\
            MeshSizeMG, MeshSizeFG, RollerBobbbinDiameter,\
            NumberGillnets, AverageGillnetLength, GrateBarSpacing,\
            FootropeLength, NumberWindows, NumberHooks,\
            NumberPots, NumberPotReleasedCrab, GearDamage,\
            AverageTowSpeed, AverageDepth, DataSource,\
            DirectedSpecies, NumberSpecies, RecordType,\
            DetailedCatchSpeciesCompCode, LogbookIDNumber1, LogbookIDNumber2,\
            SpeciesCode, KeptWeight, DiscardWeight,\
            EstimatedWeightReleasedCrab, NumberIndividuals)")

    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_Set_Catch_SingleSearchTempStorage(\
            DataBase_ID integer, RecordIdentifier integer, DeploymentUID,\
            ASOCCode integer, ObserverNumber, Year integer,\
            DeploymentNumber integer, SubTripNumber, SetNumber integer,\
            Country integer, Quota integer, SetType integer,\
            VesselSideNumber, VesselClass integer, VesselLength,\
            VesselHorsepower, Day integer, Month integer,\
            HaulDay integer, HaulMonth integer, StartTime,\
            Duration, PositionPrecision, StartLatitude real,\
            StartLongitude real, EndLatitude real, EndLongitude real,\
            NAFODivision, UnitArea, StatisticalArea,\
            InOut200MileLimit, GearType, CodendMeshSize,\
            MeshSizeMG, MeshSizeFG, RollerBobbbinDiameter,\
            NumberGillnets, AverageGillnetLength, GrateBarSpacing,\
            FootropeLength, NumberWindows, NumberHooks,\
            NumberPots, NumberPotReleasedCrab, GearDamage,\
            AverageTowSpeed, AverageDepth, DataSource,\
            DirectedSpecies, NumberSpecies, RecordType,\
            DetailedCatchSpeciesCompCode, LogbookIDNumber1, LogbookIDNumber2,\
            SpeciesCode, KeptWeight, DiscardWeight,\
            EstimatedWeightReleasedCrab, NumberIndividuals)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_Set_Catch_TextualSearchTempStorage(\
            DataBase_ID integer, RecordIdentifier integer, DeploymentUID,\
            ASOCCode integer, ObserverNumber, Year integer,\
            DeploymentNumber integer, SubTripNumber, SetNumber integer,\
            Country integer, Quota integer, SetType integer,\
            VesselSideNumber, VesselClass integer, VesselLength,\
            VesselHorsepower, Day integer, Month integer,\
            HaulDay integer, HaulMonth integer, StartTime,\
            Duration, PositionPrecision, StartLatitude real,\
            StartLongitude real, EndLatitude real, EndLongitude real,\
            NAFODivision, UnitArea, StatisticalArea,\
            InOut200MileLimit, GearType, CodendMeshSize,\
            MeshSizeMG, MeshSizeFG, RollerBobbbinDiameter,\
            NumberGillnets, AverageGillnetLength, GrateBarSpacing,\
            FootropeLength, NumberWindows, NumberHooks,\
            NumberPots, NumberPotReleasedCrab, GearDamage,\
            AverageTowSpeed, AverageDepth, DataSource,\
            DirectedSpecies, NumberSpecies, RecordType,\
            DetailedCatchSpeciesCompCode, LogbookIDNumber1, LogbookIDNumber2,\
            SpeciesCode, KeptWeight, DiscardWeight,\
            EstimatedWeightReleasedCrab, NumberIndividuals)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_Set_Catch_TEMP_UPDATE(\
                DataBase_ID integer, RecordIdentifier integer, DeploymentUID,\
                ASOCCode integer, ObserverNumber, Year integer,\
                DeploymentNumber integer, SubTripNumber, SetNumber integer,\
                Country integer, Quota integer, SetType integer,\
                VesselSideNumber, VesselClass integer, VesselLength,\
                VesselHorsepower, Day integer, Month integer,\
                HaulDay integer, HaulMonth integer, StartTime,\
                Duration, PositionPrecision, StartLatitude real,\
                StartLongitude real, EndLatitude real, EndLongitude real,\
                NAFODivision, UnitArea, StatisticalArea,\
                InOut200MileLimit, GearType, CodendMeshSize,\
                MeshSizeMG, MeshSizeFG, RollerBobbbinDiameter,\
                NumberGillnets, AverageGillnetLength, GrateBarSpacing,\
                FootropeLength, NumberWindows, NumberHooks,\
                NumberPots, NumberPotReleasedCrab, GearDamage,\
                AverageTowSpeed, AverageDepth, DataSource,\
                DirectedSpecies, NumberSpecies, RecordType,\
                DetailedCatchSpeciesCompCode, LogbookIDNumber1, LogbookIDNumber2,\
                SpeciesCode, KeptWeight, DiscardWeight,\
                EstimatedWeightReleasedCrab, NumberIndividuals)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS DFO_NL_ASOP_Set_Catch_ExcelViewTEMP(\
                DataBase_ID integer, RecordIdentifier integer, DeploymentUID,\
                ASOCCode integer, ObserverNumber, Year integer,\
                DeploymentNumber integer, SubTripNumber, SetNumber integer,\
                Country integer, Quota integer, SetType integer,\
                VesselSideNumber, VesselClass integer, VesselLength,\
                VesselHorsepower, Day integer, Month integer,\
                HaulDay integer, HaulMonth integer, StartTime,\
                Duration, PositionPrecision, StartLatitude real,\
                StartLongitude real, EndLatitude real, EndLongitude real,\
                NAFODivision, UnitArea, StatisticalArea,\
                InOut200MileLimit, GearType, CodendMeshSize,\
                MeshSizeMG, MeshSizeFG, RollerBobbbinDiameter,\
                NumberGillnets, AverageGillnetLength, GrateBarSpacing,\
                FootropeLength, NumberWindows, NumberHooks,\
                NumberPots, NumberPotReleasedCrab, GearDamage,\
                AverageTowSpeed, AverageDepth, DataSource,\
                DirectedSpecies, NumberSpecies, RecordType,\
                DetailedCatchSpeciesCompCode, LogbookIDNumber1, LogbookIDNumber2,\
                SpeciesCode, KeptWeight, DiscardWeight,\
                EstimatedWeightReleasedCrab, NumberIndividuals)")

    con.commit()
    cur.close()
    con.close()






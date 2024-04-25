import sqlite3
#backend

DB_SetCatch_Validation_Range = ("./BackEnd/Sqlite3_DB/QC_Check_RangeConsistency_DB/DFO_NL_ASOP_SetCatch_RangeValidation.db")

def get_DB_SetCatch_Validation_Range():
    conn = sqlite3.connect(DB_SetCatch_Validation_Range)
    return conn

def DFO_NL_ASOP_RangeValidation_DB():
    con= sqlite3.connect(DB_SetCatch_Validation_Range)
    cur=con.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedRange_CalenderVariables (DataBase_ID, RecordIdentifier, DeploymentUID, RecordType,\
                 Year, Day, Month, HaulDay,  HaulMonth, \
                 YearRangeQC, DayRangeQC, MonthRangeQC, HaulDayRangeQC, \
                 HaulMonthRangeQC, DeploymentIdentifier, QC_Message)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedRange_PositionalVariables (DataBase_ID, RecordIdentifier, DeploymentUID, RecordType,\
                 PositionPrecision, StartLatitude, StartLongitude, EndLatitude, EndLongitude, InOut200MileLimit,\
                 PositionPrecisionRangeQC, StartLatitudeRangeQC, StartLongitudeRangeQC, EndLatitudeRangeQC, \
                 EndLongitudeRangeQC, InOut200MileLimitRangeQC, DeploymentIdentifier, QC_Message)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedRange_GearVariables (DataBase_ID, RecordIdentifier, DeploymentUID, RecordType,\
                 RollerBobbbinDiameter, NumberGillnets, AverageGillnetLength, GrateBarSpacing, NumberPots, NumberPotReleasedCrab,\
                 RollerBobbbinDiameterRangeQC, NumberGillnetsRangeQC, AverageGillnetLengthRangeQC, \
                 GrateBarSpacingRangeQC, NumberPotsRangeQC, NumberPotReleasedCrabRangeQC, \
                 DeploymentIdentifier, QC_Message)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedRange_CatchVariables (DataBase_ID, RecordIdentifier, DeploymentUID,\
                 RecordType, AverageTowSpeed, KeptWeight, DiscardWeight, NumberIndividuals, NumberWindows,\
                 RecordTypeRangeQC, AverageTowSpeedRangeQC, KeptWeightRangeQC, \
                 DiscardWeightRangeQC, NumberIndividualsRangeQC, NumberWindowsRangeQC,\
                 DeploymentIdentifier, QC_Message)")
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedRange_TowDistance (\
                TowDistance, SCDistance, TowDifference, TowDiffFlag, \
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
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedRange_TempTowDistance (\
                TowDistance, SCDistance, TowDifference, TowDiffFlag, \
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
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedRange_TowSeparation (StartDate, EndDate, HourSeparation,\
                StartLatDec, StartLongDec, EndLatDec, EndLongDec, TowSeparation,\
                MaxTowSeparation, TowSepErrorFlag, DepChangeFlag, SubTripChangeFlag,\
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
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_QCFailedRange_TempTowSeparation (StartDate, EndDate, HourSeparation,\
                StartLatDec, StartLongDec, EndLatDec, EndLongDec, TowSeparation,\
                MaxTowSeparation, TowSepErrorFlag, DepChangeFlag, SubTripChangeFlag,\
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
    
    cur.execute("CREATE TABLE IF NOT EXISTS SetCatch_RangeLimitVariables_Define (VariablesID, VariablesType, NameRangeVariables,\
                 LowerRangeLimitValue, UpperRangeLimitValue)")
    
    con.commit()
    cur.close()
    con.close()


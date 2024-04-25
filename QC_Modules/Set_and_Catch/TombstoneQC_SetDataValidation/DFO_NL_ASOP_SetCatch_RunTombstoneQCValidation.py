
from QC_Modules.Set_and_Catch.TombstoneQC_SetDataValidation import DFO_NL_ASOP_SetCatch_RunTombstoneQC_BackEnd

def SetCatch_TombSetDataValidation():
    TotalFailedAreaCalcValidation = DFO_NL_ASOP_SetCatch_RunTombstoneQC_BackEnd.RunSetCatch_RunTombstoneQC_BackEnd()
    ReturnFailedMessage = str(TotalFailedAreaCalcValidation) + " " + " Failed In QC"
    ReturnPassedMessage = "All Passed"
    if TotalFailedAreaCalcValidation > 0:
        ReturnMsg = ReturnFailedMessage
    else:
        ReturnMsg = ReturnPassedMessage
    return ReturnMsg, TotalFailedAreaCalcValidation
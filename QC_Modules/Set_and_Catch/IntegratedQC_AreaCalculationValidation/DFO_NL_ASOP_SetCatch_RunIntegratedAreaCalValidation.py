
from QC_Modules.Set_and_Catch.IntegratedQC_AreaCalculationValidation import DFO_NL_ASOP_SetCatch_IntegratedAreaCal_BackEnd

def SetCatch_IntegratedAreaCalcValidation():
    TotalFailedAreaCalcValidation = DFO_NL_ASOP_SetCatch_IntegratedAreaCal_BackEnd.RunIntegratedAreaCal_BackEnd()
    ReturnFailedMessage = str(TotalFailedAreaCalcValidation) + " " + " Failed In QC"
    ReturnPassedMessage = "All Passed"
    if TotalFailedAreaCalcValidation > 0:
        ReturnMsg = ReturnFailedMessage
    else:
        ReturnMsg = ReturnPassedMessage
    return ReturnMsg, TotalFailedAreaCalcValidation
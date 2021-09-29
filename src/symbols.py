speed_rpm_symbols = [
    "Transducer_Speed_IOP",
    " Transducer_Speed_IOP",
    "Transducer_Speed_MCP",
    " Transducer_Speed_MCP",
    " tesInputData.L2mPosSpdArb_RotorSpd_IOP",
    "tesInputData.L2mPosSpdArb_RotorSpd_IOP",
    " tesInputData.L2mPosSpdArb_RotorSpd_MCP",
    "tesInputData.L2mPosSpdArb_RotorSpd_MCP",
]

t_demanded_symbols = [
    "AvaIfData.AvaDataExch_TrqCond_MCP",
    " AvaIfData.AvaDataExch_TrqCond_MCP",
    "AvaIfData.AvaDataExch_TrqCond_IOP",
    " AvaIfData.AvaDataExch_TrqCond_IOP",
    "vcanOutputData.L2mVcan_TarTrq.val_IOP",
    " vcanOutputData.L2mVcan_TarTrq.val_IOP",
    "vcanOutputData.L2mVcan_TarTrq.val_MCP",
    " vcanOutputData.L2mVcan_TarTrq.val_MCP",
    " TesOp_B.L2m_TarTrq_MCP",
    "TesOp_B.L2m_TarTrq_MCP",
    " TesOp_B.L2m_TarTrq_IOP",
    "TesOp_B.L2m_TarTrq_IOP"
]

t_measured_symbols = [
        "Transducer_Torque_IOP",
        "Transducer_Torque_MCP",
        "Transducer_Trq_IOP",
        "Transducer_Trq_MCP"
]

torque_estimated_signals = [
    " tesOutputData.L2mTes_EstTrq.val_MCP",
    "tesOutputData.L2mTes_EstTrq.val_MCP",
    " tesOutputData.L2mTes_EstTrq.val_IOP",
    "tesOutputData.L2mTes_EstTrq.val_IOP"
]

vdc_symbols = [
    " sensvdcOutputData.L2mSensVdc_Vdc.val_MCP",
    "sensvdcOutputData.L2mSensVdc_Vdc.val_MCP",
    " sensvdcOutputData.L2mSensVdc_Vdc.val_IOP",
    "sensvdcOutputData.L2mSensVdc_Vdc.val_IOP",
]

idc_symbols = [
    " sensidcOutputData.L2mSensIdc_Idc.val_MCP",
    "sensidcOutputData.L2mSensIdc_Idc.val_MCP",
    " sensidcOutputData.L2mSensIdc_Idc.val_IOP",
    "sensidcOutputData.L2mSensIdc_Idc.val_IOP",
    " SensIdcOp_B.L2mSensIdc_IdcPhy_IOP",
    "SensIdcOp_B.L2mSensIdc_IdcPhy_IOP",
    " SensIdcOp_B.L2mSensIdc_IdcPhy_MCP",
    "SensIdcOp_B.L2mSensIdc_IdcPhy_MCP",
]

loss_inv_comp_symbols = [
    "InverterEfficiency_MCP",
    "InverterEfficiency_IOP"
]


def symbol_auto_select(data_symbols, compared_symbols):
    if data_symbols in compared_symbols:
        found_symbol = data_symbols
    else:
        found_symbol = "Not Selected"
    return found_symbol
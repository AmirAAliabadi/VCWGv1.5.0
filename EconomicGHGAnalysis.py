# Cacluate Anualized Cost and GHG Emission Saving
# Xuan Chen, Rachel M. McLeod, Amir A. Aliabadi
# Atmospheric Innovations Research (AIR) Laboratory, University of Guelph, Guelph, Canada
# last update: 21 March 2023

import random
import sys
import os
import numpy
import matplotlib.pyplot as plt
from UWG import UWG

def EconomicGHGAnalysis(RvalRoofBase, RvalWallBase, opt_RvalWall, opt_RvalRoof, opt_A_PV, opt_A_WT,
                                        opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz, opt_SHGC, opt_V_BITES, opt_A_ST,
                                        opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm,
                                        alb_roof, V_pcm, A_st, V_bites, A_wt, A_pv,
                                        TotalGasConsumpHeatSys, TotalGasConsumpWaterHeatSys,
                                        TotalElecCoolDemandSys, TotalElecHeatDemandSys,
                                        TotalElecProducedPVSys, TotalElecProducedWTSys, TotalElecDomesticDemand,
                                        TotalGasConsumpHeatBase, TotalGasConsumpWaterHeatBase, TotalElecCoolDemandBase):

    # Building envelope information
    A_building = 196                    # Building footprint area [m^2]
    A_walls = 336                       # Area of wall envelope [m^2]
    A_halfRoof = 135.52                 # Area of half the roof [m^2]
    A_Roof = 2 * A_halfRoof             # Area of full roof [m^2]
    CoolRoofAlbedoCutOff = 0.5          # Albedo cut off for cool roof [-]

    # Economic input
    # Annual inflation rate, mean/median over the last few decades
    # https://www.macrotrends.net/countries/CAN/canada/inflation-rate-cpi
    # Mean of 2001 - 2020: 20 years mean 1.8279%, 1991 - 2020: 30 years mean 1.8832%
    InfRate = 0.0183
    # Annual interest rate, prime rate, mean/median over the last few decades
    # https: // www150.statcan.gc.ca
    # https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1010014501&cubeTimeFrame.startDaily=1992-01-14&cubeTimeFrame.endDaily=2023-01-11&referencePeriods=19920114%2C20230111'''
    # Mean of prime rate: 1991 -2020 4.87%; 2001 -2021: 3.78%
    IntRate = 0.0378

    NYearsShift = 0                                 # The number of years to shift analysis into future 20 (2040), 40 (2060), etc.
    CIniBase = ((1 + InfRate) ** NYearsShift) * 5   # Marginal initial installation cost now per building foot print area [$ m^-2]
    CAnnOMBase = ((1 + InfRate) ** NYearsShift) * 1 # Marginal annual operation and maintenance cost now per building foot print area [$ m^-2] 0.9
    Nyears = 20                                     # Number of years for economic analysis
    # Marginal costs of base system without renewable energy
    # These costs are additional to the base cost of a system without renewable energy

    # Price input
    ElecPrice = 0.127            # Electricity price now [$ kW^-1 hr^-1]
    ElecPriceInc = 0.045         # Annual rate of electricity price increase, can be mean/median over many decades
    GasPrice = 0.137             # Gas price now [$ m^-3]
    GasPriceInc = 0.01           # Annual rate of gas price increase, can be mean/median over many decades
    PVPrice = 377                # PV price per collector area now (i.e portion of roof area) [$ m^-2]
    WTPrice = 490 * 2            # WT price per swept area now [$ m^-2] assuming 1 additional replacement
    STPrice = 340                # ST price per collector area [$ m^-2]
    BITESPrice = 200             # BITES price per unit volume [$ m^-3]
    PCMPrice = 1930 * 2          # PCM price per unit volume [$ m^-3] assuming 1 additional replacement
    HPPrice = 20 * 2             # HP price per building footprint area [$ m^-2] assuming 1 additional replacement
    TreePrice = 200              # Tree price per tree now
    CRPrice = 8 * 2              # Cool Roof price per roof area now [$ m^-2] assuming 1 additional coate
    AirTPrice = 1500 * 2         # Air tightness price per building [$ test^-1] (Assume 2 tests)
    RvalueWallPrice = 8          # Price of insulation of unit R value change for wall [$ m^-4 K^-1 W]
    RvalueRoofPrice = 8          # Price of insulation of unit R value change for roof [$ m^-4 K^-1 W]

    SalFactorBase = 0.03         # Fraction of initial investment of equipment that can be salvaged
    SalFactor = 0.05             # Fraction of initial investment of equipment that can be salvaged

    # CO2 savings with the reduction of electricity consumption from the grid
    ElecEmissionIntensity = 0.04  # [kgCO2e kW-h^-1]
    # CO2 uptake of 10.52 [kg coniferous tree^-1 year^-10] and 17.24 [kg deciduous tree^-10] which gives an average of 13.88 [kg Tree^-1]
    CO2UptakeTree10Years = 13.88  # [kgCO2 10 years-1]

    # Operation maintenance cost
    OMPV = 0.01 * PVPrice                # Operation maintenance cost for PV per collector area now [$ m^-2]
    OMWT = 0.02 * WTPrice                # Operation maintenance cost for WT per swept area now [$ m^-2]
    OMST = 0.01 * STPrice                # Operation maintenance cost for ST per collector area [$ m^-2]
    OMBITES = 0.01 * BITESPrice          # Operation maintenance cost for BITES per unit volume [$ m^-3]
    OMPCM = 0.01 * PCMPrice              # Operation maintenance cost for PCM per unit volume [$ m^-3]
    OMHP = 0.05 * HPPrice                # Operation maintenance cost for HP per building footprint area [$ m^-2]
    OMVeg = 130                          # Operation maintenance cost for lawn care per 0.5 LAI [m^2 m^-2] added. Each tree is an addition of 0.5 LAI [m^2 m^-2] now
    OMCR = 75                            # Operation maintenance cost for keeping Cool Roof clean now [$]

    # Government rebate
    ITCPV = 3000                         # Government rebate for PV panel system now [$]
    ITCAirT = 550                        # Government rebate for meeting air tightness target now [$]
    ITCRval = 2.15                       # Government rebate for insulation per wall area now [$ m^-4 K^-1 W)]

    # Number of additional trees, each extra tree adds 0.5 [m^2 m^-2] LAI
    Additional_Trees = 0

    # Optimization case and initial case parameter information

    # Check which variables are being included in the optimization
    '''opt_A_PV, opt_A_WT, opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz, opt_SHGC,
    opt_V_BITES, opt_A_ST, opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm'''

    # Area of PV [m^2]
    if opt_A_PV is not None:
        A_pv = opt_A_PV * A_building
    else:
        A_pv = A_pv * A_building

    # Swept area of wind turbine [m^2]
    if opt_A_WT is not None:
        A_wt = opt_A_WT * A_building
    else:
        A_wt = A_wt * A_building

    # Volume of Bites [m^3]
    if opt_V_BITES is not None:
        V_BITES = opt_V_BITES * A_building
    else:
        V_BITES = V_bites * A_building

    # Area of ST [m^2]
    if opt_A_ST is not None:
        A_ST = opt_A_ST * A_building
    else:
        A_ST = A_st * A_building

    # Volume of PCM [m^3]
    if opt_V_pcm is not None:
        V_pcm = opt_V_pcm * A_building
    else:
        V_pcm = V_pcm * A_building

    # R-value change from base case [m^2 K W^-1]
    if opt_RvalWall is not None:
        RvalueWall_quantity = numpy.abs(float(opt_RvalWall) - float(RvalWallBase))
    else:
        RvalueWall_quantity = 0

    # R-value change from base case [m^2 K W^-1]
    if opt_RvalRoof is not None:
        RvalueRoof_quantity = numpy.abs(float(opt_RvalRoof) - float(RvalRoofBase))
    else:
        RvalueRoof_quantity = 0

    # Area of cool roof [m^2]
    if opt_AlbRoof is not None:
        A_CR = 2 * A_halfRoof
    elif alb_roof > CoolRoofAlbedoCutOff:
        A_CR = 2 * A_halfRoof
    else:
        A_CR = 0

    # High performance envelop price [$]
    EnvPrice = A_walls * RvalueWall_quantity * RvalueWallPrice + A_Roof * RvalueRoof_quantity * RvalueRoofPrice

    # Compute annualized system cost
    EffIntRate = (IntRate - InfRate) / (1 + InfRate)
    PWFFullPeriod = 1 / ((1 + EffIntRate) ** Nyears)
    CRFFullPeriod = EffIntRate / (1 - (1 + EffIntRate) ** (-Nyears))

    # Calculate present worth of cost of gas and electricity for base and renewable energy systems for the entire footprint of the house [$]
    PresBaseGasCost = 0
    PresSysGasCost = 0

    PresBaseElecCost = 0
    PresSysElecCost = 0

    # Calculate present worth base and system cumulative gas and electricity cost
    for year in range(1, Nyears + 1):
        PresBaseGasCost = PresBaseGasCost + ((1 + InfRate) ** (NYearsShift)) * ((TotalGasConsumpHeatBase + TotalGasConsumpWaterHeatBase) * A_building) * \
                          GasPrice * (1 + GasPriceInc) ** year * 1 / ((1 + EffIntRate) ** year)
        PresSysGasCost = PresSysGasCost + ((1 + InfRate) ** (NYearsShift)) * ((TotalGasConsumpHeatSys + TotalGasConsumpWaterHeatSys) * A_building) * \
                         GasPrice * (1 + GasPriceInc) ** year * 1 / ((1 + EffIntRate) ** year)

        PresBaseElecCost = PresBaseElecCost + ((1 + InfRate) ** (NYearsShift)) * (TotalElecCoolDemandBase + TotalElecDomesticDemand) * A_building * \
                           ElecPrice * (1 + ElecPriceInc) ** year * 1 / ((1 + EffIntRate) ** year)
        PresSysElecCost = PresSysElecCost + ((1 + InfRate) ** (NYearsShift)) * (TotalElecCoolDemandSys + TotalElecHeatDemandSys + TotalElecDomesticDemand - TotalElecProducedPVSys - TotalElecProducedWTSys) * A_building * \
                          ElecPrice * (1 + ElecPriceInc) ** year * 1 / ((1 + EffIntRate) ** year)

    # Capital investment for the renewable system for the entire footprint of the house [$]
    CIniSys = ((1 + InfRate) ** (NYearsShift)) * (A_pv * PVPrice + A_wt * WTPrice + A_ST * STPrice + V_BITES * BITESPrice + V_pcm * PCMPrice + \
                                                  TreePrice * Additional_Trees + A_CR * CRPrice + EnvPrice + AirTPrice + HPPrice * A_building - \
            (ITCPV + ITCAirT + ITCRval * RvalueWall_quantity * A_walls + ITCRval * RvalueRoof_quantity * A_Roof))

    CAnnIniBase = CIniBase * A_building * CRFFullPeriod
    CAnnIniSys = CIniSys * CRFFullPeriod

    CAnnGasBase = PresBaseGasCost * CRFFullPeriod
    CAnnGasSys = PresSysGasCost * CRFFullPeriod

    CAnnElecBase = PresBaseElecCost * CRFFullPeriod
    CAnnElecSys = PresSysElecCost * CRFFullPeriod

    CAnnOMSys = ((1 + InfRate) ** (NYearsShift)) * (A_pv * OMPV + A_wt * OMWT + A_ST * OMST + V_BITES * OMBITES + V_pcm * OMPCM + OMHP * A_building + Additional_Trees * OMVeg + OMCR)

    CSalBase = SalFactorBase * CIniBase * A_building * PWFFullPeriod
    CSalSys = SalFactor * CIniSys * PWFFullPeriod

    CAnnSalBase = CSalBase * CRFFullPeriod
    CAnnSalSys = CSalSys * CRFFullPeriod

    CAnnBase = CAnnIniBase + CAnnGasBase + CAnnElecBase + CAnnOMBase * A_building - CAnnSalBase
    CAnnSys = CAnnIniSys + CAnnGasSys + CAnnElecSys + CAnnOMSys - CAnnSalSys

    PercAnnSaving = 100 * (CAnnBase - CAnnSys) / CAnnBase

    #Calculate the payback period

    PresBaseGasCost = 0
    PresSysGasCost = 0

    PresBaseElecCost = 0
    PresSysElecCost = 0

    PresBaseOMCost = 0
    PresSysOMCost = 0

    SumAnnualCostDiff = 0

    for year in range(1, Nyears + 1):
        #Calculate the present worth of difference of annual costs
        PresBaseGasCost = PresBaseGasCost + ((1 + InfRate) ** (NYearsShift)) * ((TotalGasConsumpHeatBase + TotalGasConsumpWaterHeatBase) * A_building) * \
                          GasPrice * (1 + GasPriceInc) ** year * 1 / ((1 + EffIntRate) ** year)
        PresSysGasCost = PresSysGasCost + ((1 + InfRate) ** (NYearsShift)) * ((TotalGasConsumpHeatSys + TotalGasConsumpWaterHeatSys) * A_building) * \
                         GasPrice * (1 + GasPriceInc) ** year * 1 / ((1 + EffIntRate) ** year)

        PresBaseElecCost = PresBaseElecCost + ((1 + InfRate) ** (NYearsShift)) * (TotalElecCoolDemandBase + TotalElecDomesticDemand) * A_building * ElecPrice * (
                1 + ElecPriceInc) ** year * \
                           1 / ((1 + EffIntRate) ** year)
        PresSysElecCost = PresSysElecCost + ((1 + InfRate) ** (NYearsShift)) * (TotalElecCoolDemandSys + TotalElecHeatDemandSys + TotalElecDomesticDemand - TotalElecProducedPVSys - TotalElecProducedWTSys) * A_building * \
                          ElecPrice * (1 + ElecPriceInc) ** year * 1 / ((1 + EffIntRate) ** year)

        PresBaseOMCost = PresBaseOMCost + CAnnOMBase * A_building * 1 / ((1 + EffIntRate) ** year)
        PresSysOMCost = PresSysOMCost + CAnnOMSys * 1 / ((1 + EffIntRate) ** year)

        SumAnnualCostDiff = PresSysGasCost + PresSysElecCost + PresSysOMCost - PresBaseGasCost - PresBaseElecCost - PresBaseOMCost

        PaybackDiff = SumAnnualCostDiff + CIniSys - CIniBase * A_building
        # print('Year, PaybackDiff = ', year, PaybackDiff)

    # CO2 savings over the investment period [kg]

    # CO2 savings with the addition of vegetation [kg]
    # EPA 2021 - Greenhouse Gases Equivalencies Calculator - Calculations and References
    VegCO2Sav = Additional_Trees * (CO2UptakeTree10Years / 10) * Nyears

    # CO2 savings with the reduction of natural gas [kg]
    # Saved natural gas [m^3]
    NatGasSave = (TotalGasConsumpHeatBase + TotalGasConsumpWaterHeatBase - TotalGasConsumpHeatSys - TotalGasConsumpWaterHeatSys) * A_building * Nyears
    MWCH4 = 12 + 4                                            # molecular weight of CH4 [gCH4 mol^-1]
    MWCO2 = 44                                                # molecular weight of CO2 [gCO2 mol^-1]
    rhoCH4 = 0.668                                            # density of methane [kgCH4 m^-3] at 293 K and 1 ATM
    NatGasCO2Sav = NatGasSave * rhoCH4 * MWCO2 / MWCH4        # Saved CO2 [kg]

    # Saved CO2 [kg]
    ElecCO2Sav = (TotalElecCoolDemandBase + TotalElecDomesticDemand - (TotalElecCoolDemandSys + TotalElecHeatDemandSys + TotalElecDomesticDemand - TotalElecProducedPVSys - TotalElecProducedWTSys)) *\
                 A_building * Nyears * ElecEmissionIntensity

    # Total CO2 savings [kg]
    TotalCO2Sav = VegCO2Sav + NatGasCO2Sav + ElecCO2Sav

    return CAnnBase, CAnnSys, PercAnnSaving, TotalCO2Sav
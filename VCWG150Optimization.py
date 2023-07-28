# VCWG in serial mode to run simulations for multiple months
# Developed by Xuan Chen and Amir A. Aliabadi
# Atmospheric Innovations Research (AIR) Laboratory, University of Guelph, Guelph, Canada
# last update: 22 December 2022

from UWG import UWG
from PostProcess2Serial import PostProcess2Serial
import os
import numpy

# Define the .epw, .uwg filenames to create an UWG object.
# UWG will look for the .epw file in the UWG/resources/epw folder,
# and the .uwg file in the UWG/resources/parameters folder.
# Pass all optimization variables, except for R value, which is updated in the CSV file
def opt_VCWG(ene_mode, opt_A_PV, opt_A_WT, opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz, opt_SHGC,
             opt_V_BITES, opt_A_ST, opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm, k, i, i_pop):

    epw_filename = "ERA5-Toronto-2020.epw"
    param_filename_1 = "initialize_Toronto_1.uwg"         # .uwg file name
    param_filename_2 = "initialize_Toronto_2.uwg"         # .uwg file name
    param_filename_3 = "initialize_Toronto_3.uwg"         # .uwg file name
    param_filename_4 = "initialize_Toronto_4.uwg"         # .uwg file name
    param_filename_5 = "initialize_Toronto_5.uwg"         # .uwg file name
    param_filename_6 = "initialize_Toronto_6.uwg"         # .uwg file name
    param_filename_7 = "initialize_Toronto_7.uwg"         # .uwg file name
    param_filename_8 = "initialize_Toronto_8.uwg"         # .uwg file name
    param_filename_9 = "initialize_Toronto_9.uwg"         # .uwg file name
    param_filename_10 = "initialize_Toronto_10.uwg"       # .uwg file name
    param_filename_11 = "initialize_Toronto_11.uwg"       # .uwg file name
    param_filename_12 = "initialize_Toronto_12.uwg"       # .uwg file name

    ene_mode_Jan = 1
    ene_mode_Feb = 1
    ene_mode_Mar = 1
    ene_mode_Apr = 1
    ene_mode_May = 1
    ene_mode_Jun = 0
    ene_mode_Jul = 0
    ene_mode_Aug = 0
    ene_mode_Sep = 0
    ene_mode_Oct = 1
    ene_mode_Nov = 1
    ene_mode_Dec = 1

    case_name = "Toronto-OuterIter"+str(k)+"InnerIter"+str(i)+"Idv"+str(i_pop)

    # Initialize the UWG objective functions and run the simulation
    GasConsumpHeat = numpy.zeros((12))
    ElecHeatDemand = numpy.zeros((12))
    ElecCoolDemand = numpy.zeros((12))
    GasConsumpWaterHeat = numpy.zeros((12))
    ElecDomesticDemand = numpy.zeros((12))
    ElecProducedPV = numpy.zeros((12))
    ElecProducedWT = numpy.zeros((12))

    #'''Jan
    uwg = UWG(ene_mode, opt_A_PV, opt_A_WT, opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz, opt_SHGC,
              opt_V_BITES, opt_A_ST, opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm,
              epw_filename, param_filename_1,'','','','')
    uwg.run()

    if ene_mode is None:
        PostProcessEneMode = ene_mode_Jan
    else:
        PostProcessEneMode = ene_mode

    GasConsumpHeat[0], ElecHeatDemand[0], ElecCoolDemand[0], GasConsumpWaterHeat[0], ElecDomesticDemand[0], ElecProducedPV[0], ElecProducedWT[0] = PostProcess2Serial(PostProcessEneMode, "Output/Perf-Metrics-"+case_name+"-Jan.txt")
    os.rename("Output/BEM_hourly.txt", "Output/BEM_hourly-"+case_name+"-Jan.txt")
    os.rename("Output/q_profiles_hourly.txt", "Output/q_profiles_hourly-"+case_name+"-Jan.txt")
    os.rename("Output/Tepw_hourly.txt", "Output/Tepw_hourly-"+case_name+"-Jan.txt")
    os.rename("Output/TKE_profiles_hourly.txt", "Output/TKE_profiles_hourly-"+case_name+"-Jan.txt")
    os.rename("Output/Tr_profiles_hourly.txt", "Output/Tr_profiles_hourly-"+case_name+"-Jan.txt")
    os.rename("Output/Tu_profiles_hourly.txt", "Output/Tu_profiles_hourly-"+case_name+"-Jan.txt")
    os.rename("Output/U_profiles_hourly.txt", "Output/U_profiles_hourly-"+case_name+"-Jan.txt")
    os.rename("Output/V_profiles_hourly.txt", "Output/V_profiles_hourly-"+case_name+"-Jan.txt")
    #'''

    #'''Feb
    uwg = UWG(ene_mode, opt_A_PV, opt_A_WT, opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz, opt_SHGC, 
              opt_V_BITES, opt_A_ST, opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm,
              epw_filename, param_filename_2,'','','','')
    uwg.run()

    if ene_mode is None:
        PostProcessEneMode = ene_mode_Feb
    else:
        PostProcessEneMode = ene_mode

    GasConsumpHeat[1], ElecHeatDemand[1], ElecCoolDemand[1], GasConsumpWaterHeat[1], ElecDomesticDemand[1], ElecProducedPV[1], ElecProducedWT[1] = PostProcess2Serial(PostProcessEneMode, "Output/Perf-Metrics-"+case_name+"-Feb.txt")
    os.rename("Output/BEM_hourly.txt", "Output/BEM_hourly-"+case_name+"-Feb.txt")
    os.rename("Output/q_profiles_hourly.txt", "Output/q_profiles_hourly-"+case_name+"-Feb.txt")
    os.rename("Output/Tepw_hourly.txt", "Output/Tepw_hourly-"+case_name+"-Feb.txt")
    os.rename("Output/TKE_profiles_hourly.txt", "Output/TKE_profiles_hourly-"+case_name+"-Feb.txt")
    os.rename("Output/Tr_profiles_hourly.txt", "Output/Tr_profiles_hourly-"+case_name+"-Feb.txt")
    os.rename("Output/Tu_profiles_hourly.txt", "Output/Tu_profiles_hourly-"+case_name+"-Feb.txt")
    os.rename("Output/U_profiles_hourly.txt", "Output/U_profiles_hourly-"+case_name+"-Feb.txt")
    os.rename("Output/V_profiles_hourly.txt", "Output/V_profiles_hourly-"+case_name+"-Feb.txt")
    #'''

    #'''Mar
    uwg = UWG(ene_mode, opt_A_PV, opt_A_WT, opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz, opt_SHGC,
              opt_V_BITES, opt_A_ST, opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm,
              epw_filename, param_filename_3,'','','','')
    uwg.run()

    if ene_mode is None:
        PostProcessEneMode = ene_mode_Mar
    else:
        PostProcessEneMode = ene_mode

    GasConsumpHeat[2], ElecHeatDemand[2], ElecCoolDemand[2], GasConsumpWaterHeat[2], ElecDomesticDemand[2], ElecProducedPV[2], ElecProducedWT[2] = PostProcess2Serial(PostProcessEneMode, "Output/Perf-Metrics-"+case_name+"-Mar.txt")
    os.rename("Output/BEM_hourly.txt", "Output/BEM_hourly-"+case_name+"-Mar.txt")
    os.rename("Output/q_profiles_hourly.txt", "Output/q_profiles_hourly-"+case_name+"-Mar.txt")
    os.rename("Output/Tepw_hourly.txt", "Output/Tepw_hourly-"+case_name+"-Mar.txt")
    os.rename("Output/TKE_profiles_hourly.txt", "Output/TKE_profiles_hourly-"+case_name+"-Mar.txt")
    os.rename("Output/Tr_profiles_hourly.txt", "Output/Tr_profiles_hourly-"+case_name+"-Mar.txt")
    os.rename("Output/Tu_profiles_hourly.txt", "Output/Tu_profiles_hourly-"+case_name+"-Mar.txt")
    os.rename("Output/U_profiles_hourly.txt", "Output/U_profiles_hourly-"+case_name+"-Mar.txt")
    os.rename("Output/V_profiles_hourly.txt", "Output/V_profiles_hourly-"+case_name+"-Mar.txt")
    #'''

    #'''Apr
    uwg = UWG(ene_mode, opt_A_PV, opt_A_WT, opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz, opt_SHGC,
              opt_V_BITES, opt_A_ST, opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm,
              epw_filename, param_filename_4,'','','','')
    uwg.run()

    if ene_mode is None:
        PostProcessEneMode = ene_mode_Apr
    else:
        PostProcessEneMode = ene_mode

    GasConsumpHeat[3], ElecHeatDemand[3], ElecCoolDemand[3], GasConsumpWaterHeat[3], ElecDomesticDemand[3], ElecProducedPV[3], ElecProducedWT[3] = PostProcess2Serial(PostProcessEneMode, "Output/Perf-Metrics-"+case_name+"-Apr.txt")
    os.rename("Output/BEM_hourly.txt", "Output/BEM_hourly-"+case_name+"-Apr.txt")
    os.rename("Output/q_profiles_hourly.txt", "Output/q_profiles_hourly-"+case_name+"-Apr.txt")
    os.rename("Output/Tepw_hourly.txt", "Output/Tepw_hourly-"+case_name+"-Apr.txt")
    os.rename("Output/TKE_profiles_hourly.txt", "Output/TKE_profiles_hourly-"+case_name+"-Apr.txt")
    os.rename("Output/Tr_profiles_hourly.txt", "Output/Tr_profiles_hourly-"+case_name+"-Apr.txt")
    os.rename("Output/Tu_profiles_hourly.txt", "Output/Tu_profiles_hourly-"+case_name+"-Apr.txt")
    os.rename("Output/U_profiles_hourly.txt", "Output/U_profiles_hourly-"+case_name+"-Apr.txt")
    os.rename("Output/V_profiles_hourly.txt", "Output/V_profiles_hourly-"+case_name+"-Apr.txt")
    #'''

    #'''May
    uwg = UWG(ene_mode, opt_A_PV, opt_A_WT, opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz, opt_SHGC,
              opt_V_BITES, opt_A_ST, opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm,
              epw_filename, param_filename_5,'','','','')
    uwg.run()

    if ene_mode is None:
        PostProcessEneMode = ene_mode_May
    else:
        PostProcessEneMode = ene_mode

    GasConsumpHeat[4], ElecHeatDemand[4], ElecCoolDemand[4], GasConsumpWaterHeat[4], ElecDomesticDemand[4], ElecProducedPV[4], ElecProducedWT[4] = PostProcess2Serial(PostProcessEneMode, "Output/Perf-Metrics-"+case_name+"-May.txt")
    os.rename("Output/BEM_hourly.txt", "Output/BEM_hourly-"+case_name+"-May.txt")
    os.rename("Output/q_profiles_hourly.txt", "Output/q_profiles_hourly-"+case_name+"-May.txt")
    os.rename("Output/Tepw_hourly.txt", "Output/Tepw_hourly-"+case_name+"-May.txt")
    os.rename("Output/TKE_profiles_hourly.txt", "Output/TKE_profiles_hourly-"+case_name+"-May.txt")
    os.rename("Output/Tr_profiles_hourly.txt", "Output/Tr_profiles_hourly-"+case_name+"-May.txt")
    os.rename("Output/Tu_profiles_hourly.txt", "Output/Tu_profiles_hourly-"+case_name+"-May.txt")
    os.rename("Output/U_profiles_hourly.txt", "Output/U_profiles_hourly-"+case_name+"-May.txt")
    os.rename("Output/V_profiles_hourly.txt", "Output/V_profiles_hourly-"+case_name+"-May.txt")
    #'''

    #'''Jun
    uwg = UWG(ene_mode, opt_A_PV, opt_A_WT, opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz, opt_SHGC,
              opt_V_BITES, opt_A_ST, opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm,
              epw_filename, param_filename_6,'','','','')
    uwg.run()

    if ene_mode is None:
        PostProcessEneMode = ene_mode_Jun
    else:
        PostProcessEneMode = ene_mode

    GasConsumpHeat[5], ElecHeatDemand[5], ElecCoolDemand[5], GasConsumpWaterHeat[5], ElecDomesticDemand[5], ElecProducedPV[5], ElecProducedWT[5] = PostProcess2Serial(PostProcessEneMode, "Output/Perf-Metrics-"+case_name+"-Jun.txt")
    os.rename("Output/BEM_hourly.txt", "Output/BEM_hourly-"+case_name+"-Jun.txt")
    os.rename("Output/q_profiles_hourly.txt", "Output/q_profiles_hourly-"+case_name+"-Jun.txt")
    os.rename("Output/Tepw_hourly.txt", "Output/Tepw_hourly-"+case_name+"-Jun.txt")
    os.rename("Output/TKE_profiles_hourly.txt", "Output/TKE_profiles_hourly-"+case_name+"-Jun.txt")
    os.rename("Output/Tr_profiles_hourly.txt", "Output/Tr_profiles_hourly-"+case_name+"-Jun.txt")
    os.rename("Output/Tu_profiles_hourly.txt", "Output/Tu_profiles_hourly-"+case_name+"-Jun.txt")
    os.rename("Output/U_profiles_hourly.txt", "Output/U_profiles_hourly-"+case_name+"-Jun.txt")
    os.rename("Output/V_profiles_hourly.txt", "Output/V_profiles_hourly-"+case_name+"-Jun.txt")
    #'''

    #'''Jul
    uwg = UWG(ene_mode, opt_A_PV, opt_A_WT, opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz, opt_SHGC,
              opt_V_BITES, opt_A_ST, opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm,
              epw_filename, param_filename_7, '', '', '', '')
    uwg.run()

    if ene_mode is None:
        PostProcessEneMode = ene_mode_Jul
    else:
        PostProcessEneMode = ene_mode

    GasConsumpHeat[6], ElecHeatDemand[6], ElecCoolDemand[6], GasConsumpWaterHeat[6], ElecDomesticDemand[6], ElecProducedPV[6], ElecProducedWT[6] = PostProcess2Serial(PostProcessEneMode, "Output/Perf-Metrics-"+case_name+"-Jul.txt")
    os.rename("Output/BEM_hourly.txt", "Output/BEM_hourly-"+case_name+"-Jul.txt")
    os.rename("Output/q_profiles_hourly.txt", "Output/q_profiles_hourly-"+case_name+"-Jul.txt")
    os.rename("Output/Tepw_hourly.txt", "Output/Tepw_hourly-"+case_name+"-Jul.txt")
    os.rename("Output/TKE_profiles_hourly.txt", "Output/TKE_profiles_hourly-"+case_name+"-Jul.txt")
    os.rename("Output/Tr_profiles_hourly.txt", "Output/Tr_profiles_hourly-"+case_name+"-Jul.txt")
    os.rename("Output/Tu_profiles_hourly.txt", "Output/Tu_profiles_hourly-"+case_name+"-Jul.txt")
    os.rename("Output/U_profiles_hourly.txt", "Output/U_profiles_hourly-"+case_name+"-Jul.txt")
    os.rename("Output/V_profiles_hourly.txt", "Output/V_profiles_hourly-"+case_name+"-Jul.txt")
    #'''

    #'''Aug
    uwg = UWG(ene_mode, opt_A_PV, opt_A_WT, opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz, opt_SHGC,
              opt_V_BITES, opt_A_ST, opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm,
              epw_filename, param_filename_8,'','','','')
    uwg.run()

    if ene_mode is None:
        PostProcessEneMode = ene_mode_Aug
    else:
        PostProcessEneMode = ene_mode

    GasConsumpHeat[7], ElecHeatDemand[7], ElecCoolDemand[7], GasConsumpWaterHeat[7], ElecDomesticDemand[7], ElecProducedPV[7], ElecProducedWT[7] = PostProcess2Serial(PostProcessEneMode, "Output/Perf-Metrics-"+case_name+"-Aug.txt")
    os.rename("Output/BEM_hourly.txt", "Output/BEM_hourly-"+case_name+"-Aug.txt")
    os.rename("Output/q_profiles_hourly.txt", "Output/q_profiles_hourly-"+case_name+"-Aug.txt")
    os.rename("Output/Tepw_hourly.txt", "Output/Tepw_hourly-"+case_name+"-Aug.txt")
    os.rename("Output/TKE_profiles_hourly.txt", "Output/TKE_profiles_hourly-"+case_name+"-Aug.txt")
    os.rename("Output/Tr_profiles_hourly.txt", "Output/Tr_profiles_hourly-"+case_name+"-Aug.txt")
    os.rename("Output/Tu_profiles_hourly.txt", "Output/Tu_profiles_hourly-"+case_name+"-Aug.txt")
    os.rename("Output/U_profiles_hourly.txt", "Output/U_profiles_hourly-"+case_name+"-Aug.txt")
    os.rename("Output/V_profiles_hourly.txt", "Output/V_profiles_hourly-"+case_name+"-Aug.txt")
    #'''

    #'''Sep
    uwg = UWG(ene_mode, opt_A_PV, opt_A_WT, opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz, opt_SHGC,
              opt_V_BITES, opt_A_ST, opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm,
              epw_filename, param_filename_9,'','','','')
    uwg.run()

    if ene_mode is None:
        PostProcessEneMode = ene_mode_Sep
    else:
        PostProcessEneMode = ene_mode

    GasConsumpHeat[8], ElecHeatDemand[8], ElecCoolDemand[8], GasConsumpWaterHeat[8], ElecDomesticDemand[8], ElecProducedPV[8], ElecProducedWT[8] = PostProcess2Serial(PostProcessEneMode, "Output/Perf-Metrics-"+case_name+"-Sep.txt")
    os.rename("Output/BEM_hourly.txt", "Output/BEM_hourly-"+case_name+"-Sep.txt")
    os.rename("Output/q_profiles_hourly.txt", "Output/q_profiles_hourly-"+case_name+"-Sep.txt")
    os.rename("Output/Tepw_hourly.txt", "Output/Tepw_hourly-"+case_name+"-Sep.txt")
    os.rename("Output/TKE_profiles_hourly.txt", "Output/TKE_profiles_hourly-"+case_name+"-Sep.txt")
    os.rename("Output/Tr_profiles_hourly.txt", "Output/Tr_profiles_hourly-"+case_name+"-Sep.txt")
    os.rename("Output/Tu_profiles_hourly.txt", "Output/Tu_profiles_hourly-"+case_name+"-Sep.txt")
    os.rename("Output/U_profiles_hourly.txt", "Output/U_profiles_hourly-"+case_name+"-Sep.txt")
    os.rename("Output/V_profiles_hourly.txt", "Output/V_profiles_hourly-"+case_name+"-Sep.txt")
    #'''

    #'''Oct
    uwg = UWG(ene_mode, opt_A_PV, opt_A_WT, opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz, opt_SHGC,
              opt_V_BITES, opt_A_ST, opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm,
              epw_filename, param_filename_10,'','','','')
    uwg.run()

    if ene_mode is None:
        PostProcessEneMode = ene_mode_Oct
    else:
        PostProcessEneMode = ene_mode

    GasConsumpHeat[9], ElecHeatDemand[9], ElecCoolDemand[9], GasConsumpWaterHeat[9], ElecDomesticDemand[9], ElecProducedPV[9], ElecProducedWT[9] = PostProcess2Serial(PostProcessEneMode, "Output/Perf-Metrics-"+case_name+"-Oct.txt")
    os.rename("Output/BEM_hourly.txt", "Output/BEM_hourly-"+case_name+"-Oct.txt")
    os.rename("Output/q_profiles_hourly.txt", "Output/q_profiles_hourly-"+case_name+"-Oct.txt")
    os.rename("Output/Tepw_hourly.txt", "Output/Tepw_hourly-"+case_name+"-Oct.txt")
    os.rename("Output/TKE_profiles_hourly.txt", "Output/TKE_profiles_hourly-"+case_name+"-Oct.txt")
    os.rename("Output/Tr_profiles_hourly.txt", "Output/Tr_profiles_hourly-"+case_name+"-Oct.txt")
    os.rename("Output/Tu_profiles_hourly.txt", "Output/Tu_profiles_hourly-"+case_name+"-Oct.txt")
    os.rename("Output/U_profiles_hourly.txt", "Output/U_profiles_hourly-"+case_name+"-Oct.txt")
    os.rename("Output/V_profiles_hourly.txt", "Output/V_profiles_hourly-"+case_name+"-Oct.txt")
    #'''

    #'''Nov
    uwg = UWG(ene_mode, opt_A_PV, opt_A_WT, opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz, opt_SHGC,
              opt_V_BITES, opt_A_ST, opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm,
              epw_filename, param_filename_11,'','','','')
    uwg.run()

    if ene_mode is None:
        PostProcessEneMode = ene_mode_Nov
    else:
        PostProcessEneMode = ene_mode

    GasConsumpHeat[10], ElecHeatDemand[10], ElecCoolDemand[10], GasConsumpWaterHeat[10], ElecDomesticDemand[10], ElecProducedPV[10], ElecProducedWT[10] = PostProcess2Serial(PostProcessEneMode, "Output/Perf-Metrics-"+case_name+"-Nov.txt")
    os.rename("Output/BEM_hourly.txt", "Output/BEM_hourly-"+case_name+"-Nov.txt")
    os.rename("Output/q_profiles_hourly.txt", "Output/q_profiles_hourly-"+case_name+"-Nov.txt")
    os.rename("Output/Tepw_hourly.txt", "Output/Tepw_hourly-"+case_name+"-Nov.txt")
    os.rename("Output/TKE_profiles_hourly.txt", "Output/TKE_profiles_hourly-"+case_name+"-Nov.txt")
    os.rename("Output/Tr_profiles_hourly.txt", "Output/Tr_profiles_hourly-"+case_name+"-Nov.txt")
    os.rename("Output/Tu_profiles_hourly.txt", "Output/Tu_profiles_hourly-"+case_name+"-Nov.txt")
    os.rename("Output/U_profiles_hourly.txt", "Output/U_profiles_hourly-"+case_name+"-Nov.txt")
    os.rename("Output/V_profiles_hourly.txt", "Output/V_profiles_hourly-"+case_name+"-Nov.txt")
    #'''

    #'''Dec
    uwg = UWG(ene_mode, opt_A_PV, opt_A_WT, opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz, opt_SHGC,
              opt_V_BITES, opt_A_ST, opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm,
              epw_filename, param_filename_12,'','','','')
    uwg.run()

    if ene_mode is None:
        PostProcessEneMode = ene_mode_Dec
    else:
        PostProcessEneMode = ene_mode

    GasConsumpHeat[11], ElecHeatDemand[11], ElecCoolDemand[11], GasConsumpWaterHeat[11], ElecDomesticDemand[11], ElecProducedPV[11], ElecProducedWT[11] = PostProcess2Serial(PostProcessEneMode, "Output/Perf-Metrics-"+case_name+"-Dec.txt")
    os.rename("Output/BEM_hourly.txt", "Output/BEM_hourly-"+case_name+"-Dec.txt")
    os.rename("Output/q_profiles_hourly.txt", "Output/q_profiles_hourly-"+case_name+"-Dec.txt")
    os.rename("Output/Tepw_hourly.txt", "Output/Tepw_hourly-"+case_name+"-Dec.txt")
    os.rename("Output/TKE_profiles_hourly.txt", "Output/TKE_profiles_hourly-"+case_name+"-Dec.txt")
    os.rename("Output/Tr_profiles_hourly.txt", "Output/Tr_profiles_hourly-"+case_name+"-Dec.txt")
    os.rename("Output/Tu_profiles_hourly.txt", "Output/Tu_profiles_hourly-"+case_name+"-Dec.txt")
    os.rename("Output/U_profiles_hourly.txt", "Output/U_profiles_hourly-"+case_name+"-Dec.txt")
    os.rename("Output/V_profiles_hourly.txt", "Output/V_profiles_hourly-"+case_name+"-Dec.txt")
    #'''

    # calculate the annual values of electricity and natural gas consumptions over all the months
    TotalGasConsumpHeatSys = numpy.sum(GasConsumpHeat)
    TotalGasConsumpWaterHeatSys = numpy.sum(GasConsumpWaterHeat)

    TotalElecHeatDemandSys = numpy.sum(ElecHeatDemand)
    TotalElecCoolDemandSys = numpy.sum(ElecCoolDemand)

    TotalElecProducedPVSys = numpy.sum(ElecProducedPV)
    TotalElecProducedWTSys = numpy.sum(ElecProducedWT)

    TotalElecDomesticDemand = numpy.sum(ElecDomesticDemand)

    # Copy some variables for use by other functions
    alb_roof = uwg.alb_roof     # Roof albedo [-]
    V_pcm = uwg.V_pcm           # Phase change material per building foot print area [m^3 m^-2]
    A_st = uwg.A_st             # Solar thermal area per building foot print area [m^2 m^-2]
    V_bites = uwg.V_bites       # Building thermal storage volume per building foot print area [m^3 m^-2]
    A_wt = uwg.A_wt             # Swept wind area per building foot print area [m^2 m^-2]
    A_pv = uwg.A_pv             # Solar photovoltaic area per building foot print area [m^2 m^-2]

    return TotalGasConsumpHeatSys, TotalGasConsumpWaterHeatSys, TotalElecHeatDemandSys, TotalElecCoolDemandSys, TotalElecProducedPVSys, TotalElecProducedWTSys, TotalElecDomesticDemand, \
           alb_roof, V_pcm, A_st, V_bites, A_wt, A_pv




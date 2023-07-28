# Main code for running the optimization for VCWG
# Developed by Xuan Chen and Amir A. Aliabadi
# Atmospheric Innovations Research (AIR) Laboratory, University of Guelph, Guelph, Canada
# last update: 21 March 2023

import os
import numpy
import pandas as pd
import logging
import opt_VariableSpace
import opt_UpdateCSV
import opt_MicroGenetic
from VCWG150Optimization import opt_VCWG
from EconomicGHGAnalysis import EconomicGHGAnalysis

# Set up the logging process to file
logging.basicConfig(filename='Output/Optimization.log', encoding='utf-8', level=logging.DEBUG)
logging.info('Starting Optimization ...')

# Part 1: set the building type and energy mode for the optimization
# Building type should be consistent with "bld" variable in the initialization file
buildingtype = 6
# set the energy mode for base case that SHOULD NOT include retrofits, renewable/alternative energy
base_ene_mode = 2
# Minimum electricity and gas consumption demand to ensure successful normalization of the objective functions
MinTotalNetElecDemand = 10  # [kW hr m-2]
MinTotalNetGasConsump = 20  # [m3 m-2]

# Part 2: user should run VCWG once for a base case that SHOULD NOT include retrofits, renewable/alternative energy
# 1) set variables in the 12 initialization files for each month, initialize_city_month.uwg
# A_st,0.001, V_bites,0.0001, m_dot_st_f,0.00002, m_dot_he_st,0.00008, A_pv,0.00, A_wt,0.000, V_pcm,0.0000001,
# 2) set correct starting R values in BLDX_LocationSummary.csv
# After optimization starts these variables will be updated and passed to the function opt_VCWG
base_A_PV = None
base_A_WT = None
base_V_BITES = None
base_A_ST = None
base_V_pcm = None
base_Infil = None
base_Vent = None
base_AlbRoof = None
base_Glz = None
base_SHGC = None
base_m_dot_st_f = None
base_m_dot_he_st = None
base_T_melt = None

DIR_CURR = os.path.abspath(os.path.dirname(__file__))
DIR_DOE_PATH = os.path.join(DIR_CURR, "resources", "DOERefBuildings")
file_doe_name_location = os.path.join("{}".format(DIR_DOE_PATH), "BLD{}".format(buildingtype),
                                      "BLD{}_LocationSummary.csv".format(buildingtype))
df = pd.read_csv(file_doe_name_location)

RvalRoofBase = df.iloc[16, -1]
RvalWallBase = df.iloc[14, -1]

TotalGasConsumpHeatBase, TotalGasConsumpWaterHeatBase, TotalElecHeatDemandBase, TotalElecCoolDemandBase,\
TotalElecProducedPVBase, TotalElecProducedWTBase, TotalElecDomesticDemandBase, \
Base_alb_roof, Base_V_pcm, Base_A_st, Base_V_bites, Base_A_wt, Base_A_pv = \
                       opt_VCWG(base_ene_mode, base_A_PV, base_A_WT, base_Infil, base_Vent, base_AlbRoof,
                                base_Glz, base_SHGC, base_V_BITES, base_A_ST, base_m_dot_st_f,
                                base_m_dot_he_st, base_T_melt, base_V_pcm, 9999, 9999, 9999)

print('Finished The Base Case Simulation.')
print('TotalGasConsumpHeatBase [m3 m-2], TotalGasConsumpWaterHeatBase [m3 m-2], TotalElecHeatDemandBase [kW hr m-2],'
      'TotalElecCoolDemandBase [kW hr m-2], TotalElecProducedPVBase [kW hr m-2], TotalElecProducedWTBase [kW hr m-2], '
      'TotalElecDomesticDemandBase [kW hr m-2]')
print(TotalGasConsumpHeatBase, TotalGasConsumpWaterHeatBase, TotalElecHeatDemandBase,
       TotalElecCoolDemandBase, TotalElecProducedPVBase, TotalElecProducedWTBase, TotalElecDomesticDemandBase)

logging.info('Finished The Base Case Simulation.')
logging.info('TotalGasConsumpHeatBase [m3 m-2] = ' + str(TotalGasConsumpHeatBase))
logging.info('TotalGasConsumpWaterHeatBase [m3 m-2] = ' + str(TotalGasConsumpWaterHeatBase))
logging.info('TotalElecHeatDemandBase [kW hr m-2] = ' + str(TotalElecHeatDemandBase))
logging.info('TotalElecCoolDemandBase [kW hr m-2] = ' + str(TotalElecCoolDemandBase))
logging.info('TotalElecProducedPVBase [kW hr m-2] = ' + str(TotalElecProducedPVBase))
logging.info('TotalElecProducedWTBase [kW hr m-2] = ' + str(TotalElecProducedWTBase))
logging.info('TotalElecDomesticDemandBase [kW hr m-2] = ' + str(TotalElecDomesticDemandBase))

logging.info('Summary of Base Case Net Electricity and Gas Consumption = ')
logging.info('Net Electricity Demand [kW hr m^-2] = ' + str(TotalElecHeatDemandBase + TotalElecCoolDemandBase +
                                                            TotalElecProducedPVBase + TotalElecProducedWTBase +
                                                            TotalElecDomesticDemandBase))
logging.info('Total Gas Consumption [m^3 m^-2] = ' + str(TotalGasConsumpHeatBase + TotalGasConsumpWaterHeatBase))

# Part 3: Set up the optimization
# The number of the objective functions to save
NumberOfObjFunSave = 4
# The number of the objective functions for the weighted sum
NumberOfObjFunWeightedSum = 3
# Equal weights for the weight sum overall objective function
wgt = 1.0/NumberOfObjFunWeightedSum
# Total number of the population in each iteration, it MUST be ODD
n_pop = 5
# The new population involved in each iteration, it MUST be EVEN
n_change = n_pop - 1
# Maximum and minimum number of inner iterations for generating new populations
iMaxInner = 6
iMinInner = 2
# Maximum and minimum number of outer iterations for generating new populations
iMaxOuter = 12
iMinOuter = 10
# Convergence threshold for inner iterations
ConvergenceThresholdInner = 0.03
# Convergence threshold for outer iterations
ConvergenceThresholdOuter = 0.001

# Generate the variables and their space; choose the optimized variables from the list
whole_choice_list = ['A_PV', 'A_WT', 'Rvalue_roof', 'Rvalue_wall', 'Infiltration', 'Ventilation', 'Albedo_roof',
                     'Glazing', 'SHGC', 'V_bites', ' A_ST', 'm_dot_st_f', 'm_dot_he_st', 'T_melt', 'V_pcm']
opt_in_VCWG_list = ['opt_A_PV', 'opt_A_WT', 'opt_RvalRoof', 'opt_RvaWall', 'opt_Infil', 'opt_Vent', 'opt_AlbRoof',
                    'opt_Glz','opt_SHGC', 'opt_V_BITES', 'opt_A_ST', 'opt_m_dot_st_f', 'opt_m_dot_he_st', 'opt_T_melt', 'opt_V_pcm']

# Set the energy mode for optimization process
# The Adv_ene_heat_mode should be consistent in the 12 monthly initialization files
# 3 for PV WT only, Adv_ene_heat_mode in the initialize files should be 3 for all
# 2 for no renewable energy, Adv_ene_heat_mode in the initialize files should be 2 for all
# None for heating and cooling mode, Adv_ene_heat_mode in the initialize files should be 0 or 1 depending on month
ene_mode = None

# Entire potential space and the minimun of the R values that will be passed to the EconomicGHGAnalysis.py
space, lRvalRoof, lRvalWall = opt_VariableSpace.Space()
# User's choice of optimized variables
choice = opt_VariableSpace.Choice(ene_mode)
# User's potential space and the number of variables
options_space, n_var = opt_VariableSpace.SetOptVar(space, choice)
# options_space is a dictionary, the var_name is set as key, the content is array

# To change the options_space and the variables that need to be optimized, go to the 'opt_VariableSpace.py'
print('User\'s Option Space For The Variables Chosen To Be Optimized = ')
logging.info('User\'s Option Space For The Variables Chosen To Be Optimized = ')
for key in options_space:
    print (key, options_space[key])
    logging.info(str(key)+' = '+str(options_space[key]))

# Part 4: Start the optimization
# Build empty arrays for saving the results from each iteration
# Best solution at each iteration
BestSolutionInner = numpy.zeros((iMaxOuter, iMaxInner, n_var))
# Best overall objective function value (smallest) at each iteration
BestOverallObjFunInner = numpy.zeros((iMaxOuter, iMaxInner))
# Individual objective functions and GHG savings [e, g, c, GHG] for the best solution after each iteration
BestIdvObjFunInner = numpy.zeros((iMaxOuter, iMaxInner, NumberOfObjFunSave))
# Index of the elite in each iteration
EliteIndex = numpy.zeros((iMaxOuter, iMaxInner))
BestSolutionInner.fill(numpy.nan)
BestOverallObjFunInner.fill(numpy.nan)
BestIdvObjFunInner.fill(numpy.nan)

pop = opt_MicroGenetic.starting_pop(options_space, n_pop, n_var)
print('Starting Population For Optimization = ')
logging.info('Starting Population For Optimization = ')
print(pop.to_string())
logging.info(pop.to_string())
SolutionHead = list(pop.columns)
print(SolutionHead)
logging.info(str(SolutionHead))

# Outer loop
for k in range(iMaxOuter):
    print('Outer Loop Optimization Iteration = ', k)
    logging.info('Outer Loop Optimization Iteration = ' + str(k))

    # Inner loop
    # The pop is a dataframe: Row = the index for population, Column = variables name
    for i in range(iMaxInner):
        print('Inner Loop Optimization Iteration = ', i)
        logging.info('Inner Loop Optimization Iteration = ' + str(i))

        # Calculation for the starting population, the start population is the very first time for all the iterations
        if k == 0 and i == 0:
            VCWGIdvObjFunOutInner = numpy.zeros((n_pop, NumberOfObjFunSave))

            # Run VCWG as many times as the size of the population
            for n in range(n_pop):
                print('Individual In Population = ', n)
                # logging.info('Individual In Population = ' + str(n))
                idv = pop.iloc[n]

                # Set the optimization parameters
                if whole_choice_list[0] in idv:
                    opt_A_PV = float("{:.2f}".format(idv[whole_choice_list[0]]))
                else:
                    opt_A_PV = None

                if whole_choice_list[1] in idv:
                    opt_A_WT =  float("{:.2f}".format(idv[whole_choice_list[1]]))
                else:
                    opt_A_WT = None

                if whole_choice_list[2] in idv:
                    opt_RvalRoof =  float("{:.2f}".format(idv[whole_choice_list[2]]))
                else:
                    opt_RvalRoof = None

                if whole_choice_list[3] in idv:
                    opt_RvalWall = float("{:.2f}".format(idv[whole_choice_list[3]]))
                else:
                    opt_RvalWall = None

                if whole_choice_list[4] in idv:
                    opt_Infil = float("{:.2f}".format(idv[whole_choice_list[4]]))
                else:
                    opt_Infil = None

                if whole_choice_list[5] in idv:
                    opt_Vent = float("{:.2f}".format(idv[whole_choice_list[5]])) /1000.0
                else:
                    opt_Vent = None

                if whole_choice_list[6] in idv:
                    opt_AlbRoof = float("{:.2f}".format(idv[whole_choice_list[6]]))
                else:
                    opt_AlbRoof = None

                if whole_choice_list[7] in idv:
                    opt_Glz = float("{:.2f}".format(idv[whole_choice_list[7]]))
                else:
                    opt_Glz = None

                if whole_choice_list[8] in idv:
                    opt_SHGC = float("{:.2f}".format(idv[whole_choice_list[8]]))
                else:
                    opt_SHGC = None

                if whole_choice_list[9] in idv:
                    opt_V_BITES = float("{:.5f}".format(idv[whole_choice_list[9]]))
                else:
                    opt_V_BITES = None

                if whole_choice_list[10] in idv:
                    opt_A_ST = float("{:.5f}".format(idv[whole_choice_list[10]]))
                else:
                    opt_A_ST = None

                if whole_choice_list[11] in idv:
                    opt_m_dot_st_f = float("{:.5f}".format(idv[whole_choice_list[11]]))
                else:
                    opt_m_dot_st_f = None

                if whole_choice_list[12] in idv:
                    opt_m_dot_he_st = float("{:.5f}".format(idv[whole_choice_list[12]]))
                else:
                    opt_m_dot_he_st = None

                if whole_choice_list[13] in idv:
                    opt_T_melt = float("{:.5f}".format(idv[whole_choice_list[13]]))
                else:
                    opt_T_melt = None

                if whole_choice_list[14] in idv:
                    opt_V_pcm = float("{:.5f}".format(idv[whole_choice_list[14]]))
                else:
                    opt_V_pcm = None

                # i for iteration, n for population
                # Only the R values updated in the .CSV file
                opt_UpdateCSV.Update_LocationSummary(buildingtype, opt_RvalWall, opt_RvalRoof)

                # Run VCWG and pass all the optimization variables, except for the ones updated in the CSV file
                TotalGasConsumpHeatSys, TotalGasConsumpWaterHeatSys, TotalElecHeatDemandSys, TotalElecCoolDemandSys, \
                TotalElecProducedPVSys, TotalElecProducedWTSys, TotalElecDomesticDemand, \
                alb_roof, V_pcm, A_st, V_bites, A_wt, A_pv \
                    = opt_VCWG(ene_mode, opt_A_PV, opt_A_WT, opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz,
                           opt_SHGC, opt_V_BITES, opt_A_ST, opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm,
                           k, i, n)

                # Run economic and GHG analysis
                CAnnBase, CAnnSys, PercAnnSaving, TotalCO2Sav = \
                    EconomicGHGAnalysis(RvalRoofBase, RvalWallBase, opt_RvalWall, opt_RvalRoof, opt_A_PV, opt_A_WT, opt_Infil,
                                        opt_Vent, opt_AlbRoof, opt_Glz, opt_SHGC, opt_V_BITES, opt_A_ST, opt_m_dot_st_f,
                                        opt_m_dot_he_st, opt_T_melt, opt_V_pcm,
                                        alb_roof, V_pcm, A_st, V_bites, A_wt, A_pv,
                                        TotalGasConsumpHeatSys, TotalGasConsumpWaterHeatSys,
                                        TotalElecCoolDemandSys, TotalElecHeatDemandSys,
                                        TotalElecProducedPVSys, TotalElecProducedWTSys, TotalElecDomesticDemand,
                                        TotalGasConsumpHeatBase, TotalGasConsumpWaterHeatBase, TotalElecCoolDemandBase)

                # Store values of each objective function
                VCWGIdvObjFunOutInner[n, 0] = TotalElecHeatDemandSys + TotalElecCoolDemandSys + TotalElecDomesticDemand \
                                              - TotalElecProducedPVSys - TotalElecProducedWTSys
                VCWGIdvObjFunOutInner[n, 1] = TotalGasConsumpHeatSys + TotalGasConsumpWaterHeatSys
                VCWGIdvObjFunOutInner[n, 2] = CAnnSys
                VCWGIdvObjFunOutInner[n, 3] = TotalCO2Sav

                print('Net Electricity Demand [kW hr m^-2] = %5.2f' % VCWGIdvObjFunOutInner[n, 0])
                print('Total Gas Consumption [m^3 m^-2] = %5.2f' % VCWGIdvObjFunOutInner[n, 1])
                print('Marginal Alternative Energy System Annualized Cost [$] = %5.2f' % VCWGIdvObjFunOutInner[n, 2])
                print('Total CO2 Emissions Saved From Vegetation and Natural Gas [kg CO2] = %5.2f' % VCWGIdvObjFunOutInner[n, 3])

                # logging.info('Net Electricity Demand [kW hr m^-2] = ' + str(VCWGIdvObjFunOutInner[n, 0]))
                # logging.info('Total Gas Consumption [m^3 m^-2] = ' + str(VCWGIdvObjFunOutInner[n, 1]))
                # logging.info('Marginal Alternative Energy System Annualized Cost [$] = ' + str(VCWGIdvObjFunOutInner[n, 2]))
                # logging.info('Total CO2 Emissions Saved From Vegetation and Natural Gas [kg CO2] = ' + str(VCWGIdvObjFunOutInner[n, 3]))

                # if the electric demand and gas demand are negative, set it as zero
                if VCWGIdvObjFunOutInner[n, 0] <= 0:
                    VCWGIdvObjFunOutInner[n, 0] = MinTotalNetElecDemand
                    print('Caution! Net Electricity Demand Was Negative and Thus Reset To A Minimum Value.')
                    # logging.info('Caution! Net Electricity Demand Was Negative and Thus Reset To A Minimum Value.')

                if VCWGIdvObjFunOutInner[n, 1] <= 0:
                    VCWGIdvObjFunOutInner[n, 1] = MinTotalNetGasConsump
                    print('Caution! Net Gas Consumption Was Negative And Thus Reset To A Minimum Value.')
                    # logging.info('Caution! Net Gas Consumption Was Negative And Thus Reset To A Minimum Value.')

            # Calculate the fitness
            fitness = numpy.zeros((n_pop))

            for j in range(n_pop):
                # Calculate fitness, smaller the better
                fitness[j] = numpy.sum(
                    wgt * VCWGIdvObjFunOutInner[j, 0] / VCWGIdvObjFunOutInner[0, 0] +
                    wgt * VCWGIdvObjFunOutInner[j, 1] / VCWGIdvObjFunOutInner[0, 1] + wgt *
                    VCWGIdvObjFunOutInner[j, 2] / VCWGIdvObjFunOutInner[0, 2])
            fitness = pd.DataFrame(fitness, columns=['FIT'])

        # Calculation for the populations after the first inner iteration
        else:
            # Select the base case for normalization of the overall objective function
            base = BestIdvObjFunInner[0, 0, :]
            print('Base Case For Normalization = ', base)
            # logging.info('Base Case For Normalization = ' + str(base))

            VCWGIdvObjFunOutInner = numpy.zeros((n_pop, NumberOfObjFunSave))
            # The last solution in the new population is from the last elite, which does not require a VCWG run
            VCWGIdvObjFunOutInner[n_pop - 1, :] = last_BestIdvObjFunInner

            # Run VCWG as many times as the size of the population minus the elite
            for n in range(n_pop - 1):
                print('Individual In Population = ', n)
                # logging.info('Individual In Population = ' + str(n))
                idv = pop.iloc[n]

                # Set the optimization parameters
                if whole_choice_list[0] in idv:
                    opt_A_PV = float("{:.2f}".format(idv[whole_choice_list[0]]))
                else:
                    opt_A_PV = None

                if whole_choice_list[1] in idv:
                    opt_A_WT = float("{:.2f}".format(idv[whole_choice_list[1]]))
                else:
                    opt_A_WT = None

                if whole_choice_list[2] in idv:
                    opt_RvalRoof = float("{:.2f}".format(idv[whole_choice_list[2]]))
                else:
                    opt_RvalRoof = None

                if whole_choice_list[3] in idv:
                    opt_RvalWall = float("{:.2f}".format(idv[whole_choice_list[3]]))
                else:
                    opt_RvalWall = None

                if whole_choice_list[4] in idv:
                    opt_Infil = float("{:.2f}".format(idv[whole_choice_list[4]]))
                else:
                    opt_Infil = None

                if whole_choice_list[5] in idv:
                    opt_Vent = float("{:.2f}".format(idv[whole_choice_list[5]])) / 1000.0
                else:
                    opt_Vent = None

                if whole_choice_list[6] in idv:
                    opt_AlbRoof = float("{:.2f}".format(idv[whole_choice_list[6]]))
                else:
                    opt_AlbRoof = None

                if whole_choice_list[7] in idv:
                    opt_Glz = float("{:.2f}".format(idv[whole_choice_list[7]]))
                else:
                    opt_Glz = None

                if whole_choice_list[8] in idv:
                    opt_SHGC = float("{:.2f}".format(idv[whole_choice_list[8]]))
                else:
                    opt_SHGC = None

                if whole_choice_list[9] in idv:
                    opt_V_BITES = float("{:.5f}".format(idv[whole_choice_list[9]]))
                else:
                    opt_V_BITES = None

                if whole_choice_list[10] in idv:
                    opt_A_ST = float("{:.5f}".format(idv[whole_choice_list[10]]))
                else:
                    opt_A_ST = None

                if whole_choice_list[11] in idv:
                    opt_m_dot_st_f = float("{:.5f}".format(idv[whole_choice_list[11]]))
                else:
                    opt_m_dot_st_f = None

                if whole_choice_list[12] in idv:
                    opt_m_dot_he_st = float("{:.5f}".format(idv[whole_choice_list[12]]))
                else:
                    opt_m_dot_he_st = None

                if whole_choice_list[13] in idv:
                    opt_T_melt = float("{:.5f}".format(idv[whole_choice_list[13]]))
                else:
                    opt_T_melt = None

                if whole_choice_list[14] in idv:
                    opt_V_pcm = float("{:.5f}".format(idv[whole_choice_list[14]]))
                else:
                    opt_V_pcm = None

                # i for iteration, n for population
                # Only the R values updated in the .CSV file
                opt_UpdateCSV.Update_LocationSummary(buildingtype, opt_RvalWall, opt_RvalRoof)

                # Run VCWG and pass all the optimization variables, except the ones updated in the CSV file
                TotalGasConsumpHeatSys, TotalGasConsumpWaterHeatSys, TotalElecHeatDemandSys, TotalElecCoolDemandSys, \
                TotalElecProducedPVSys, TotalElecProducedWTSys, TotalElecDomesticDemand, \
                alb_roof, V_pcm, A_st, V_bites, A_wt, A_pv \
                    = opt_VCWG(ene_mode, opt_A_PV, opt_A_WT, opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz,
                               opt_SHGC, opt_V_BITES, opt_A_ST, opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm,
                               k, i, n)

                # Run economic and GHG analysis
                CAnnBase, CAnnSys, PercAnnSaving, TotalCO2Sav = \
                    EconomicGHGAnalysis(RvalRoofBase, RvalWallBase, opt_RvalWall, opt_RvalRoof, opt_A_PV, opt_A_WT,
                                        opt_Infil, opt_Vent, opt_AlbRoof, opt_Glz, opt_SHGC, opt_V_BITES, opt_A_ST,
                                        opt_m_dot_st_f, opt_m_dot_he_st, opt_T_melt, opt_V_pcm,
                                        alb_roof, V_pcm, A_st, V_bites, A_wt, A_pv,
                                        TotalGasConsumpHeatSys, TotalGasConsumpWaterHeatSys,
                                        TotalElecCoolDemandSys, TotalElecHeatDemandSys,
                                        TotalElecProducedPVSys, TotalElecProducedWTSys, TotalElecDomesticDemand,
                                        TotalGasConsumpHeatBase, TotalGasConsumpWaterHeatBase, TotalElecCoolDemandBase)

                # Store values of each objective function
                VCWGIdvObjFunOutInner[n, 0] = TotalElecHeatDemandSys + TotalElecCoolDemandSys + TotalElecDomesticDemand \
                                              - TotalElecProducedPVSys - TotalElecProducedWTSys
                VCWGIdvObjFunOutInner[n, 1] = TotalGasConsumpHeatSys + TotalGasConsumpWaterHeatSys
                VCWGIdvObjFunOutInner[n, 2] = CAnnSys
                VCWGIdvObjFunOutInner[n, 3] = TotalCO2Sav

                print('Net Electricity Demand [kWhr m^-2]: %5.2f' % VCWGIdvObjFunOutInner[n, 0])
                print('Total Gas Consumption [m^3 m^-2]: %5.2f' % VCWGIdvObjFunOutInner[n, 1])
                print('Marginal Alternative Energy System Annualized Cost [$]: %5.2f' % VCWGIdvObjFunOutInner[n, 2])
                print('Total CO2 Emissions Saved From Vegetation and Natural Gas [kg CO2]: %5.2f' % VCWGIdvObjFunOutInner[n, 3])

                # logging.info('Net Electricity Demand [kWhr m^-2] = ' + str(VCWGIdvObjFunOutInner[n, 0]))
                # logging.info('Total Gas Consumption [m^3 m^-2] = ' + str(VCWGIdvObjFunOutInner[n, 1]))
                # logging.info('Marginal Alternative Energy System Annualized Cost [$] = ' + str(VCWGIdvObjFunOutInner[n, 2]))
                # logging.info('Total CO2 Emissions Saved From Vegetation and Natural Gas [kg CO2] = ' + str(VCWGIdvObjFunOutInner[n, 3]))

                # If the electric demand and gas demand are negative, set them as zero
                if VCWGIdvObjFunOutInner[n, 0] <= 0:
                    VCWGIdvObjFunOutInner[n, 0] = 0
                    print('Caution! Net Electricity Demand Was Negative And Thus Reset To Zero.')
                    # logging.info('Caution! Net Electricity Demand Was Negative And Thus Reset To Zero.')
                if VCWGIdvObjFunOutInner[n, 1] <= 0:
                    VCWGIdvObjFunOutInner[n, 1] = 0
                    print('Caution! Net Gas Consumption Was Negative And Thus Reset To Zero.')
                    # logging.info('Caution! Net Gas Consumption Was Negative And Thus Reset To Zero.')

            # Calculate the fitness, the smaller the better
            fitness = numpy.zeros((n_pop))
            for j in range(n_pop):
                fitness[j] = numpy.sum(
                    wgt * VCWGIdvObjFunOutInner[j, 0] / base[0] + wgt * VCWGIdvObjFunOutInner[j, 1] / base[1] + wgt *
                    VCWGIdvObjFunOutInner[j, 2] / base[2])
            fitness = pd.DataFrame(fitness, columns=['FIT'])

        # Select the parents and elite
        print('Population Fitness = ')
        # logging.info('Population Fitness = ')
        print(fitness)
        # logging.info(str(fitness))

        parents, elite, elite_fit, elite_idx = opt_MicroGenetic.tournament(fitness, pop, n_change, n_var)

        # Save the elite's VCWG objective function results (electricity, gas, cost, GHG)
        BestIdvObjFunInner[k, i, :] = VCWGIdvObjFunOutInner[elite_idx, :]
        BestSolutionInner[k, i, :] = pop.iloc[elite_idx]
        # Save the best elite location for each iteration for post analysis
        EliteIndex[k, i] = elite_idx
        print('Best Solution, Values of Variable Space = ')
        logging.info('Best Solution, Values of Variable Space = ')
        print(BestSolutionInner[k, i, :])
        logging.info(str(BestSolutionInner[k, i, :]))

        # Update the last best elite IdvObjFun for the next iteration usage
        last_BestIdvObjFunInner = VCWGIdvObjFunOutInner[elite_idx, :]

        BestOverallObjFunInner[k, i] = elite_fit
        print('Best Overall Objective Function = ', BestOverallObjFunInner[k, i])
        logging.info('Best Overall Objective Function = ' + str(BestOverallObjFunInner[k, i]))
        print('Best Individual Objective Functions And GHG Savings = ', BestIdvObjFunInner[k, i, :])
        logging.info('Best Individual Objective Functions And GHG Savings = ' + str(BestIdvObjFunInner[k, i, :]))

        # Break out of the inner for loop if convergence criteria is met and a minimum number of inner iterations have taken place
        NormDiffSuccessiveElitesInner = 0
        if i >= iMinInner:
            NormDiffSuccessiveElitesInner = numpy.abs((BestOverallObjFunInner[k, i] -
                                                       BestOverallObjFunInner[k, i-1])) / BestOverallObjFunInner[k, i-1]
            print ('NormDiffSuccessiveElitesInner = ', NormDiffSuccessiveElitesInner)
            # logging.info('NormDiffSuccessiveElitesInner = ' + str(NormDiffSuccessiveElitesInner))

        if (i >= iMinInner) and (NormDiffSuccessiveElitesInner <= ConvergenceThresholdInner):
            print ('Inner Loop Converged, Breaking Out Early.')
            # logging.info('Inner Loop Converged, Breaking Out Early.')
            pop = opt_MicroGenetic.out_pop(options_space, n_pop, n_var, n_change, elite)
            print('New Population = ')
            # logging.info('New Population = ')
            print(pop.to_string())
            # logging.info(pop.to_string())
            break
        else:
            print('Parents Surviving Out Of This Iteration = ')
            # logging.info('Parents Surviving Out Of This Iteration = ')
            print(parents)
            # logging.info(str(parents))
            offspring = opt_MicroGenetic.crossover(parents, n_change, n_var)
            print('Offsprings For The Next Iteration = ')
            # logging.info('Offsprings For The Next Iteration = ')
            print(offspring)
            # logging.info(str(offspring))
            pop = opt_MicroGenetic.in_pop(options_space, n_pop, n_var, n_change, elite, offspring)
            print('New Population = ')
            # logging.info('New Population = ')
            print(pop.to_string())
            # logging.info(pop.to_string())

    # Save results in CSV format
    df_BestSolutionInner = pd.DataFrame(BestSolutionInner[k, :, :], columns=SolutionHead)
    df_BestOverallObjFunInner = pd.DataFrame(BestOverallObjFunInner[k, :], columns=['Fitness'])
    df_BestIdvObjFunInner = pd.DataFrame(BestIdvObjFunInner[k, :, :], columns=['NetElecDemand [kW hr m-2]', 'TotalGasConsump [m3 m-2]', 'CostAnnual [CAD]', 'TotalCO2Save [kg CO2]'])

    df_BestSolutionInner.to_csv("Output/Result_BestOptSolOuterIter"+str(k)+"InnerIter"+str(i)+".csv",index=False)
    df_BestOverallObjFunInner.to_csv("Output/Result_BestOverallObjFunOuterIter"+str(k)+"InnerIter"+str(i)+".csv",index=False)
    df_BestIdvObjFunInner.to_csv("Output/Result_BestIdvObjFunOuterIter"+str(k)+"InnerIter"+str(i)+".csv",index=False)
    print('Finished Saving The Solution, Overall/Indvidual Objective Function, and GHG Savings, For Outer And Inner Loops = ', k, i)
    # logging.info('Finished Saving The Solution, Overall/Indvidual Objective Function, and GHG Savings, For Outer And Inner Loops = ' + str(k) + ', ' + str(i))

    # Break out of the outer for loop if convergence criteria is met and a minimum number of inner iterations have taken place

    NormDiffSuccessiveElitesOuter = 0
    if k >= iMinOuter:
        NormDiffSuccessiveElitesOuter = numpy.abs((numpy.nanmin(BestOverallObjFunInner[k, :]) - numpy.nanmin(BestOverallObjFunInner[k-1, :]))) / \
                                   numpy.nanmin(BestOverallObjFunInner[k-1, :])
        print('NormDiffSuccessiveElitesOuter = ', NormDiffSuccessiveElitesOuter)
        # logging.info('NormDiffSuccessiveElitesOuter = ' + str(NormDiffSuccessiveElitesOuter))

    if (k >= iMinOuter) and (NormDiffSuccessiveElitesOuter <= ConvergenceThresholdOuter):
        print('Optimization Finished.')
        # logging.info('Optimization Finished.')
        break

# Part 5: save final results in python array format in hyper-dimensions
numpy.save("Output/Results_BestOptSol.npy", BestSolutionInner)
numpy.save("Output/Results_BestOverallObjFun.npy", BestOverallObjFunInner)
numpy.save("Output/Results_BestIdvObjFun.npy", BestIdvObjFunInner)
numpy.save("Output/Results_EliteIndex.npy", EliteIndex)
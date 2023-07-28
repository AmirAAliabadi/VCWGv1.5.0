# VCWG in single mode to run simulations for only specific number of days
# Developed by Xuan Chen and Amir A. Aliabadi
# Atmospheric Innovations Research (AIR) Laboratory, University of Guelph, Guelph, Canada
# last update: 21 July 2022

from UWG import UWG

# Define the .epw, .uwg filenames to create an UWG object.
# UWG will look for the .epw file in the UWG/resources/epw folder,
# and the .uwg file in the UWG/resources/parameters folder.

epw_filename = "ERA5-Toronto-2020.epw"
param_filename = "initialize_Toronto_0.uwg"         # .uwg file name

# Initialize the UWG object and run the simulation
uwg = UWG(None, None, None, None, None, None, None, None, None, None, None, None, None, None,
          epw_filename, param_filename, '', '', '', '')
uwg.run()



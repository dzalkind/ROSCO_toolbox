'''
----------- Example_12 --------------
Load a turbine, tune a controller, determine APC pitch lookup table
-------------------------------------

In this example:
  - Load a turbine from OpenFAST
  - Tune a controller
  - Plot active power control pitch lookup table
  - Write open-loop input for soft-starting turbine

'''
# Python Modules
import yaml, os
# ROSCO toolbox modules 
from ROSCO_toolbox import controller as ROSCO_controller
from ROSCO_toolbox import turbine as ROSCO_turbine
from ROSCO_toolbox import sim as ROSCO_sim
from ROSCO_toolbox import utilities as ROSCO_utilities

import numpy as np
import matplotlib.pyplot as plt


# Load yaml file 
parameter_filename = '/Users/dzalkind/Tools/ROSCO_toolbox/Tune_Cases/IEA15MW.yaml'
inps = yaml.safe_load(open(parameter_filename))
path_params         = inps['path_params']
turbine_params      = inps['turbine_params']
controller_params   = inps['controller_params']

# Instantiate turbine, controller, and file processing classes
turbine         = ROSCO_turbine.Turbine(turbine_params)
controller      = ROSCO_controller.Controller(controller_params)

# Load turbine data from OpenFAST and rotor performance text file
rt_dir = os.path.dirname(os.path.dirname(__file__))
turbine.load_from_fast(path_params['FAST_InputFile'], \
  os.path.join(rt_dir,path_params['FAST_directory']), \
    dev_branch=True,rot_source='txt', \
      txt_filename= os.path.join(rt_dir,path_params['FAST_directory'],path_params['rotor_performance_filename']))

# Tune controller 
controller.tune_controller(turbine)

# Plot minimum pitch schedule
if True:
    plt.figure(1)
    plt.plot(controller.PwC_R, controller.PwC_B,label='Active Power Control LUT')
    plt.legend()
    plt.xlabel('Power Rating (-)')
    plt.ylabel('Blade pitch (rad)')
    plt.xlim((0,1.25))

    plt.figure(2)
    plt.plot(controller.SoftStart.tt,controller.SoftStart.R_ss)
    plt.xlabel('Time (sec.)')
    plt.ylabel('Power Rating (-)')

    plt.figure(3)
    plt.plot(controller.SoftCutOut.uu,controller.SoftCutOut.R_scu)
    plt.xlabel('Wind Speed (m/s)')
    plt.ylabel('Power Rating (-)')

    plt.show()


# Write parameter input file
param_file = '/Users/dzalkind/Tools/ROSCO_toolbox/Examples/DISCON.IN'   
ROSCO_utilities.write_DISCON(turbine,controller,param_file=param_file, txt_filename=path_params['rotor_performance_filename'])
ROSCO_utilities.write_ol_power(controller,'/Users/dzalkind/Tools/ROSCO_toolbox/Examples/soft_start_example.dat')
ROSCO_utilities.write_soft_cut_out(controller,'/Users/dzalkind/Tools/ROSCO_toolbox/Examples/soft_cut_out_example.dat')
# file_processing.write_ol_power(controller)




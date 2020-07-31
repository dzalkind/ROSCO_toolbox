'''
----------- Example_06 --------------
Load a turbine, tune a controller, run OpenFAST simulation 
-------------------------------------

In this example:
  - Load a turbine from OpenFAST
  - Tune a controller
  - Run an OpenFAST simulation

Note - you will need to have a compiled controller in ROSCO/build/ 
'''
# Python Modules
import yaml
# ROSCO toolbox modules 
from ROSCO_toolbox import controller as ROSCO_controller
from ROSCO_toolbox import turbine as ROSCO_turbine
from ROSCO_toolbox import sim as ROSCO_sim
from ROSCO_toolbox import utilities as ROSCO_utilities
import numpy as np

fast_plots = ROSCO_utilities.FAST_Plots()

# Load yaml file 
parameter_filename = '/Users/dzalkind/Tools/ROSCO_toolbox/Tune_Cases/SUMR-D.yaml'
inps = yaml.safe_load(open(parameter_filename))
path_params         = inps['path_params']
turbine_params      = inps['turbine_params']
controller_params   = inps['controller_params']

# Instantiate turbine, controller, and file processing classes
turbine         = ROSCO_turbine.Turbine(turbine_params)
controller      = ROSCO_controller.Controller(controller_params)
file_processing = ROSCO_utilities.FileProcessing()
fast_io         = ROSCO_utilities.FAST_IO()

# Load turbine data from OpenFAST and rotor performance text file
turbine.load_from_fast(path_params['FAST_InputFile'],path_params['FAST_directory'],dev_branch=True,rot_source='txt',txt_filename=path_params['rotor_performance_filename'])

# Tune controller 
controller.tune_controller(turbine)

# Hard Code SUMR-D Vars
controller.min_pitch = np.pi / 180 * -5
controller.vs_minspd = 27.1207
controller.vs_refspd = 99.30972
controller.vs_rgn2K  = 0.0475
controller.VS_ControlMode = 3

controller.pc_gain_schedule.legacy(controller, 0.1109,-0.1211,-0.0249)

# Write parameter input file
param_file = '/Users/dzalkind/Tools/SUMR-D/FAST8_IF/DISCON.IN'   # This must be named DISCON.IN to be seen by the compiled controller binary. 
file_processing.write_DISCON(turbine,controller,param_file=param_file, txt_filename=path_params['rotor_performance_filename'])

# Run OpenFAST
# --- May need to change fastcall if you use a non-standard command to call openfast
# fast_io.run_openfast(path_params['FAST_directory'], fastcall='/Users/dzalkind/Tools/openfast/install/bin/openfast', fastfile=path_params['FAST_InputFile'],chdir=True)

#  Define Plot cases 
#  --- Comment,uncomment, create, and change these as desired...
# cases = {}
# cases['Baseline'] = ['Wind1VelX', 'BldPitch1', 'GenTq', 'GenSpeed','GenPwr','RootMyb1','TwrBsMyt','PtfmPitch']

# # Plot, woohoo!
# fast_plots.plot_fast_out(cases, alldata,showplot=True)



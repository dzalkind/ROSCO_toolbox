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
import os
# ROSCO toolbox modules 
from ROSCO_toolbox import controller as ROSCO_controller
from ROSCO_toolbox import turbine as ROSCO_turbine
from ROSCO_toolbox.utilities import write_DISCON, run_openfast
from ROSCO_toolbox import sim as ROSCO_sim
from ROSCO_toolbox.ofTools.fast_io import output_processing

this_dir = os.path.dirname(__file__)

# Load yaml file 
parameter_filename = os.path.join(this_dir,'../Tune_Cases/IEA15MW.yaml')
inps = yaml.safe_load(open(parameter_filename))
path_params         = inps['path_params']
turbine_params      = inps['turbine_params']
controller_params   = inps['controller_params']

# Instantiate turbine, controller, and file processing classes
turbine         = ROSCO_turbine.Turbine(turbine_params)
controller      = ROSCO_controller.Controller(controller_params)

# Load turbine data from OpenFAST and rotor performance text file
rt_dir = os.path.dirname(this_dir)
turbine.load_from_fast(path_params['FAST_InputFile'], \
  os.path.join(rt_dir,path_params['FAST_directory']), \
    dev_branch=True,rot_source='txt', \
      txt_filename=os.path.join(rt_dir,path_params['FAST_directory'],path_params['rotor_performance_filename']))

# Tune controller 
controller.tune_controller(turbine)

# Write parameter input file
param_file = os.path.join(this_dir,'DISCON.IN')   # This must be named DISCON.IN to be seen by the compiled controller binary. 
write_DISCON(turbine,controller,param_file=param_file, txt_filename=path_params['rotor_performance_filename'])

# Run OpenFAST
# --- May need to change fastcall if you use a non-standard command to call openfast
run_openfast(os.path.join(rt_dir,path_params['FAST_directory']), fastcall='/Users/dzalkind/Tools/openfast-dev/install/bin/openfast',\
   fastfile=path_params['FAST_InputFile'], chdir=True)


# filenames = [os.path.join(this_dir,file) for file in filenames]

# #  Define Plot cases 
# #  --- Comment,uncomment, create, and change these as desired...
# cases = {}
# cases['Baseline'] = ['Wind1VelX', 'BldPitch1', 'GenTq', 'RotSpeed']
# cases['Rotor'] = ['BldPitch1', 'GenTq', 'GenPwr']

# # Instantiate fast_IO
# fast_out = output_processing.output_processing()
# # Can also do:
# # fast_out = output_processing.output_processing(filenames=filenames, cases=cases)
# # fast_out.plot_fast_out()

# # Load and plot
# fastout = fast_out.load_fast_out(filenames, tmin=10)
# fast_out.plot_fast_out(cases=cases)
# print('here')





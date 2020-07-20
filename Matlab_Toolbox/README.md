# Simulink Implementation of ROSCO
A simulink version of ROSCO has been created for rapid prototyping of new control ideas. The results do not exactly match results from the .DLL version of ROSCO due to the way that Simulink handles initial conditions. These differences change the wind speed estimate slightly and propogate to differences in the torque control and pitch saturation. The following modules in ROSCO have been implemented in Simulink:
  - TSR tracking torque control
  - PI gain-scheduled pitch control
  - Setpoint smoothing control
  - Extended Kalman Filter wind speed estimator
  - Pitch Saturation
  - Floating feedback control
  
The modules not currently implemented include:
  - k\omega^2 torque control
  - Individual pitch control
  - Shutdown control
  - Flap control
  
The `matlab-toolbox` is required for reading OpenFAST inputs, loading ROSCO parameters, and post processing the output files; it can be found [here](https://github.com/dzalkind/matlab-toolbox/tree/master/).

Follow the direction for installing the toolbox and use `runFAST.m` to run the Simulink model.  A more detailed version of `runFAST.m` can be round in the `matlab-toolbox`.
  

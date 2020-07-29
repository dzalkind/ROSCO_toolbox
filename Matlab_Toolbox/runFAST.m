%% runFAST.m
% This script will run a single FAST simulation with the ROSCO Simulink
% controller.  A more in depth version can be found at https://github.com/dzalkind/matlab-toolbox/tree/master/Simulations

clear;

% Compile FAST for use with simulink & mex using openfast docs
fast.FAST_SFuncDir     = '/Users/dzalkind/Tools/openfast-sim/glue-codes/simulink/src';  %%%% NEED FOR SIMULINK
fast.FAST_InputFile    = '5MW_Land_Simulink.fst';   % FAST input file (ext=.fst)
fast.FAST_directory    = '/Users/dzalkind/Tools/ROSCO_toolbox/Test_Cases/5MW_Land_Simulink';   % Path to fst directory files

% Simulink Parameters
% Model
simu.SimModel           = '/Users/dzalkind/Tools/ROSCO_toolbox/Matlab_Toolbox/Simulink/ROSCO';

% Script for loading parameters
simu.ParamScript        = '/Users/dzalkind/Tools/matlab-tools/Simulations/SimulinkModels/load_ROSCO_params';


%% Simulation Parameters

simu.TMax   = 60;


%% Simulink Setup

[ControlScriptPath,ControScript] = fileparts(simu.ParamScript);
addpath(ControlScriptPath);

addpath(fast.FAST_SFuncDir)

warning off all

%% Read FAST Files & Load ROSCO Params from DISCON.IN

[Param,Cx] = ReadWrite_FAST(fast);

simu.dt     = 1/80;   % hard code since we are not reading/writing fast files
[R,F] = feval(ControScript,Param,simu);

%% Premake OutList for Simulink

OutList = {'Time'};
OutList = [OutList;
    Param.IWP.OutList;
    Param.EDP.OutList;
    Param.ADP.OutList;
    Param.SvDP.OutList;
    ];

for iOut = 2:length(OutList)
    OutList{iOut} = OutList{iOut}(2:end-1); %strip "s
end


%% Exectute FAST

% Using Simulink/S_Func
FAST_InputFileName = [fast.FAST_directory,filesep,fast.FAST_InputFile];
TMax               = simu.TMax;

SimulinkModel = simu.SimModel;

Out         = sim(SimulinkModel, 'StopTime',num2str(GetFASTPar(Param.FP,'TMax')));
sigsOut     = get(Out,'sigsOut');   %internal control signals

%% Get OutData

SFuncOutStr = '.SFunc';

% Try text first, then binary
[OutData,OutList] = ReadFASTtext([fast.FAST_directory,filesep,fast.FAST_InputFile(1:end-4),SFuncOutStr,'.out']);
if isempty(OutData)
    [OutData,OutList] = ReadFASTbinary([fast.FAST_directory,filesep,fast.FAST_InputFile(1:end-4),SFuncOutStr,'.outb']);
end





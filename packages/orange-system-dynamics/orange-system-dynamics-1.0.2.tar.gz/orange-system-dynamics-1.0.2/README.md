# Orange3 System Dynamics Add-on

This is an add-on for [Orange3](https://orangedatamining.com/) allowing to
perform simulation using _System Dynamic Modeling_ (SDM) mechanism.

## Orange Data Mining
**ODM** (_Orange Data Mining_) is an open source machine learning and data
visualization tool. It allows to build data analysis workflows visually, with a
large, diverse toolbox.

We develop a list of widgets to be used in ODM, each widget has a functionality
to be mainly applied for _System Dynamic Modeling_. 

## Installation
_Orange3_ and the _SDM_ Addon must be installed in the same
_Python_ environment.

### Orange 3
```shell
pip install pyQt5 PyQtWebEngine
pip install orange3
```

### System Dynamics Addon
```shell
pip install orange-system-dynamics
```

## Usage
Orange3 can be run using the following command:
```shell
orange-canvas
```
or
```shell
python -m orange.canvas
```
New widgets should appear in the toolbox bar under the __System Dynamics__
section.


## Widgets Description

### System Dynamics

System dynamics (SD) is an approach to understanding the nonlinear behaviour
of complex systems over time using stocks, flows,
internal feedback loops, table functions and time delays.

![](https://gitlab.com/drb-python/samples/odm/sd_addon/-/raw/main/screenshots/Workflow_Example.png)

### Load Simulation Widget
`Load Simulation` widget is used to load simulation models in .mdl or .xmile format,
it outputs the model for Simulation.

![](https://gitlab.com/drb-python/samples/odm/sd_addon/-/raw/main/screenshots/Load.png)

### Simulation Widget
Once the model is loaded, the `Simulation` Widget is updated to show model's
variables grouped by:
- Time Controls: contains the initial time, the final time and defined time
step
- Stocks: contains all model’s stocks, can be used to change any stock’s
initial value
- Auxiliary Values: contains  all the auxiliary values, can also be changed

![](https://gitlab.com/drb-python/samples/odm/sd_addon/-/raw/main/screenshots/Simulation.png)

Once the Run Simulation button’s hit, the model is run, the widget outputs an
Orange Data Table, we use the `Line Chart` Widget to visualize results of
simulation: 

![](https://gitlab.com/drb-python/samples/odm/sd_addon/-/raw/main/screenshots/Line_Chart.png)

Other widgets have been used to perform step by step execution of simulation, by simply running the 
results through `As Timeseries` while indicating Time as the index variable:

![](https://gitlab.com/drb-python/samples/odm/sd_addon/-/raw/main/screenshots/As_Timeseries.png)

Next, using `Time Slice` which was adapted to commit a cumulative step by step simulation 
to the Line Chart:

![](https://gitlab.com/drb-python/samples/odm/sd_addon/-/raw/main/screenshots/Time_Slice.png)

In another example; we run the simulation in two different regions: 

- Paris (France)

- Algiers(Algeria) and Casablanca (Morocco)

with different simulation parameters each time, we variate the total population, 
contact infectivity and the stocks (infectious, recovered, susceptible).
We simply add the results together using Concatenate:

![](https://gitlab.com/drb-python/samples/odm/sd_addon/-/raw/main/screenshots/Workflow_Example1.png)

We can also show the results in Geo Map, after adding Latitude and Longitude information: 

![](https://gitlab.com/drb-python/samples/odm/sd_addon/-/raw/main/screenshots/Geo_Map.png)

### Agent Based Model 

An agent-based model (ABM) is a computational model for simulating the actions 
and interactions of autonomous agents (both individual or collective entities such as 
organizations or groups) in order to 
understand the behavior of a system and what governs its outcomes.

![](https://gitlab.com/drb-python/samples/odm/sd_addon/-/raw/main/screenshots/Workflow_Example2.png)

### State Machine Widget
`State Machine` widget is used to read a .yaml file containing a statemachine.

![](https://gitlab.com/drb-python/samples/odm/sd_addon/-/raw/main/screenshots/State_Machine.png)

### Agent Widget
̀Agent` widget creates an agent from a statemachine, it outputs the model used for 
creating multi-agent system environment.

![](https://gitlab.com/drb-python/samples/odm/sd_addon/-/raw/main/screenshots/Agent.png)

`Multi Agent Environment` is used to define interactions between agents 
in a multi-agent system configuration.

![](https://gitlab.com/drb-python/samples/odm/sd_addon/-/raw/main/screenshots/Multi_Agent.png)

Once the Run Simulation button’s hit, the model is run, the widget outputs an
Orange Data Table, we use the `Line Chart` Widget to visualize results of
simulation: 

![](https://gitlab.com/drb-python/samples/odm/sd_addon/-/raw/main/screenshots/Line_Chart.png)




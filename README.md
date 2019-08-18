# Interactive CoolProp 
<img align="right" width="400" src="https://github.com/stephansmit/interactive_coolprop/raw/master/dashboard.png">

Code to run an interactive CoolProp dashboard to explore the thermodynamic properties in 3 dimensions.

## Requirements

Install the following python modules
~~~~
pip3 install dash==0.41.0 plotly==3.7.1 ipywidgets==7.0.0 CoolProp
~~~~

Or use Singularity, see below.

## Use
The dashboard is hosted on [localhost:8050](https://localhost:8050)

To run local 
~~~~
python3 app.py
~~~~

Using Singularity
~~~~
singularity pull shub://stephansmit/python_containers:interactivecoolprop
singularity instance start python_containers_interactivecoolprop.sif dashboard
~~~~

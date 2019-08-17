# Interactive CoolProp 

Code to run an interactive CoolProp dashboard to explore the thermodynamic properties in 3 dimensions.

## Requirements

Install the following python modules
~~~~
pip3 install dash plotly CoolProp
~~~~

Or use Singularity, see below

## Use

Locally
~~~~
python3 app.py
~~~~

Using Singularity
~~~~
singularity pull shub://stephansmit/python_containers:InteractiveCoolProp
singularity run python_containers_InteractiveCoolProp.sif 
~~~~

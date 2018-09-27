# Business Prototyping Toolkit for Python 

__Welcome to the Business Prototyping Toolkit for Python! (BPTK_Py)__


## What is it?
BPTK_Py is the implementation of a simulation and plotting engine for System Dynamics models. 
It gives you the power to simulate System Dynamics Models within Python and create beautiful plots of the simulation results for use in Jupyter Lab/ Notebooks - or just export the simulation results for further processing outside the framework.

The framework requires a Python simulation model following certain conventions.
 
Typically System Dynamics models are created using visual modeling environments. To address this use case, BPTK_Py ships with __transentis' sdcc parser__  for transpiling such models into Python code.

Currently sdcc only supports models created using the [XMILE format](https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=xmile), which is an open XML protocol for sharing interoperable system dynamics models and simulations. 
The XMILE standard is governed by the OASIS standards consortium.

[Stella](http://www.iseesystems.com) is a visual modeling environment that stores system dynamics models in this format.
 
In future we may extend the sdcc transpiler to support other model formats (such as Vensim® by [Ventana Systems](http://www.vensim.com)).

## Main Features
* Simulation of System Dynamics simulation models
* Creating interactive plots from simulation results
* Retrieve simulation results as [Pandas DataFrame](https://github.com/pandas-dev/pandas) timeseries data
* Automatic conversion of XMILE models to Python 

# Getting Help
BPTK_Py has initially been developed by transentis Labs Gmbh. 
For questions regarding installation, usage and other help please contact us at: [support@transentis.com](mailto:support@transentis.com).

Our BPTK_Py tutorial contains sample models and Jupyter notebooks that explain how to use our framework. 
You can download the tutorial from our [website](https://www.transentis.com/products/business-prototyping-toolkit/). 
This readme covers the installation process, the main API methods and how to define a simulation model.

## Installing the BPTK_PY framework
Like every piece of software, BPTK_Py and its dependencies have to be installed correctly. 

If you already have a running Python and Jupyter environment, ``pip install BPTK-Py`` or ``pip3 install BPTK-Py`` will do!

Assuming you are starting from scratch, you need to perform the following steps

1. Install Python
2. Install Node and npm
3. Install BPTK_Py
4. Install JupyterLab (optional)
5. Setup a virtual environment (optional)
6. Download our [BPTK_Py tutorial](https://www.transentis.com/products/business-prototyping-toolkit/) (optional)

### Install Python
First of all, you need [Python](https://www.python.org/). Download the latest version for your operating system. 
BPTK-Py was tested with Python 3.7, 3.6 and 3.4. 


### Install Node and npm
Both for our sdcc compiler and also for displaying interactive widgets in Jupyter you need to install [Node.js](https://nodejs.org/en/) for your operating system.
Make sure you install npm (the node.js package manager) along with node.js. This should be done automatically when downloading and installing from the official site. 


#### Python and Node on your favorite Linux Distribution
If you are using a Linux Distribution, you may want to use your preferred package manager for downloading Python and node.

For Ubuntu using apt:
```commandline
sudo apt update
sudo apt install nodejs python3 python3-pip npm
```

Other Linux distributions should have similar packages. 
You may always refer to the official websites of [Python](https://www.python.org/) and [Node.js](https://nodejs.org/en/) for help on installing the dependencies for your specific operating system.

### Install BPTK_Py using Pip
After the prerequisites, we have to install ``BPTK_Py`` into our python environment.
This requires you to use the command shell. In windows, press ``windows + R`` and type "powershell". In Mac OS X run the Terminal app. 
Linux users may use their preferred terminal emulator.

To install the package, just type ``pip install BPTK-Py`` or ``pip3 install BPTK-Py``. Pip is a package manager that keeps Python packages up-to-date.

Pip installs the package and makes it available system-wide. It downloads all dependencies for the package automatically.

After Pip finished successfully, you are ready for working with the framework. 

If for some reason Pip is not available on your system, first download it. Regardless the operating system, this should do:
1. Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py). The file may open in your browser tab. Make sure to save it on your hard drive.
2. Install pip: in a terminal, go to the directory of the downloaded script and issue ``python3 ./get-pip.py`` and wait a minute or two.

Linux/UNIX shorthand: [[1](#Links)]
```commandline
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 ./get-pip.py
```

### Install JupyterLab
Additionally, you may want to use Jupyter Lab to work interactively on the simulations - just as we do.

```
pip install jupyterlab
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```
Now you have a functioning version of jupyter lab and can start working  interactively using jupyter notebooks. 
Just type ``jupyter lab`` in the terminal to get started.

In order to keep your system clean, you may want to use a [virtual environment](https://docs.python-guide.org/dev/virtualenvs/) instead of installing Python system-wide.

### Setup a virtual environment

A virtual environment is a local copy of your Python distribution that stores all packages required and does not interfere with your system's packages. 

Following steps are required to set up the venv and and install BPTK_Py into it:

```
pip install virtualenv
virtualenv bptk_test 

# Enter the virtual environment. In the beginning of your prompt you should see "(bptk_test)"
source bptk_test/bin/activate  #  For UNIX/Linux/Mac OS X
bptk_test\Scripts\activate.bat # For Windows

pip install BPTK-Py
pip install jupyterlab
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

 
## Package dependencies
If for any reason, you want to install the requirements manually or need to know why we need the packages, here comes the list. 

If you observe malfunctions in the framework and believe the reason may be incompatibilities with newer versions of the packages, please inform us.

So far, we tested the framework with Python 3.4, 3.6 and 3.7. It should be working fine with other Python 3.x versions.

Package name | What we use it for | Latest tested version
--- | --- | ---
pandas |DataFrames and internal results storage | 0.23.4
matplotlib |Plotting environment | 2.2.2
ipywidgets |Widget environment for notebooks | 7.4.0
scipy |Linear interpolation for graphical functions  | 1.1.0
numpy |Linear interpolation and required by pandas | 1.15.0
jupyter lab extension for jupyter-widgets |Use ipywidgets in jupyter lab | 0.36.1

## Limitations

Currently the BPTK_Py framework is geared towards our own need and has a number of limitations - we are happy to extend the framewor. Please let us know what you need so that we can prioritize our activities.

Here are the known limitations:

* Currently the simulator only supports the Euler method, Runge-Kutta Integration is not supported.
* The SD model transpiler only supports stocks, flows/biflows and converters. The other modeling elements provided by Stella (such as ovens and conveyors) are not supported.
* The SD model transpiler currently only supports the following builtin functions: ``size, stddev, sum, mean, rank, previous, abs, max, min, int, sin, cos, round, savediv, if, delay, init, normal, random, pulse, step``



## Using the Framework in Python

### Initializing the Framework in Your Python Code

To initialize the framework in your own python script / jupyter notebook and get access to the API methods (see later sections), use these lines:

**Required lines**
```python
from BPTK_Py.bptk import bptk 

bptk = bptk()

```
**Optional lines**
```python
# To Show all available scenarios and -managers:
print(Model)
managers = bptk.scenario_manager_factory.get_scenario_managers(scenario_managers_to_filter=[])

for key, manager in managers.items():
    print("")
    print("*** {} ***".format(key))

    for name in manager.get_scenario_names():
        print("\t {}".format(name))
```
On first run, the framework needs to download some additional dependencies for model compilation. Please be patient for some seconds. 
This will only occur on first-time run.
Now you are ready to play around with the APIs!


### Plotting API
After initializing BPTK_Py, let us dive into the plotting API, the heart of the simulation framework. 
An API exposes certain functionalities - "methods" or "functions" - for use by the actual application user. 
It is the interface between the complex simulations and the user.
``BPTK_Py`` aims at making simulation and result plotting as simple as possible. 
This is why there are only two functions that are doing everything for you: 
* the ``plot_scenarios`` method for static plots (described here)
* the ``dashboard`` method for interactive dashboards. All parameters for ``plot_scenarios`` are valid for this one as well.

You may use the API to generate plots from your simulation models almost instantly. 
You can control all major settings for the simulation and the later plot layout using a large set of parameters:
```python
bptk.plot_scenarios(
    scenarios,
    scenario_managers=[], 
    equations=[], 
    kind=config.kind, 
    alpha=config.alpha, 
    stacked=config.stacked, 
    freq="D", 
    start_date="1/1/2018", 
    title="", 
    visualize_from_period=0, 
    x_label="", 
    y_label="",
    series_names={"series_to_rename":"rename_to"},return_df=False)
```
The method plots one or multiple equations for an arbitrary amount of scenarios. The scenario names are specified in the scenario JSON file. 
The other parameters are optional. Always use Python's list notations for the plural parameters (``scenarios / equations / scenario_managers``).

* ``scenario_managers``: You may use a list to filter the scenarios by the scenario managers. If not specified, ``bptk_py`` will look for the specified scenarios(s) within all scenario managers. You might receive duplicates. We handle this by adding a suffix for all duplicates based on their scenario manager's name.
* ``scenarios``: Select the scenario(s) to plot. Only ``scenarios`` and ``equations`` are mandatory.
* ``equations``: Select the simulation's equation(s) to plot. If no equation is specified, the simulator has nothing to simulate.
* ``kind``: Kind of plot (area, line, bar, ...)
* ``alpha``: The alpha defines the opacity. Float 0.0 < alpha <= 1.0.
* ``freq``: Here we define the interval of the dates that we convert the ticks to. "D" means daily, "H" hourly, "M" monthly, "Y" annually and so on.
* ``start_date``: Date from which plot starts
* ``title``: Plot title
* ``visualize_from_period``: First t to visualize from (in case we want to cut off the first x periods)
* ```visualize_to_period```: Last t to visualize (to cut off later periods)
* ``x_label and y_label``: set the label names for the axis.
* ``series_names``: The equation names are not the kind of names we want to show the customer. You may use the ``series_names`` parameter to rename them. Supply the equations to rename and their destination names. Use Python's dict notation: ``{ equation_name : rename_to }``. The dictionary serves as a set of replacement rules. To correctly rename the series, you have to understand how the framework sets the names of series to avoid ambiguity in series names. If you use more than one scenario manager for plotting, bptk_py applies the following series naming schema: ``"scenarioManager"_"scenario"_"equation"``. If you want to replace this, use ``series_names={"scenarioManager_scenario_equation": "new name"}``. You may as well define a rule that replaces the name of each scenario Manager with a whitespace. The number of rules is not limited.


This was just a short intro. You may learn how to create interactive plots and define scenarios in our tutorial and blog posts available at [https://www.transentis.com/products/business-prototyping-toolkit/](https://www.transentis.com/products/business-prototyping-toolkit/).

# Creating your own Simulation models
Instead of converting 3rd party simulation models, you may define your own simulation model using the SystemDynamics API we created (starting with version 0.4.0).
A simulation model is a self-contained python script. 
This means, it can be executed as its own file without any dependencies. 

Here is the reduced code an example available in the interactive tutorial.


```python
from BPTK_Py import Model
from BPTK_Py import sd_functions as sd

class simulation_model(Model):

    def __init__(self):

        # Never forget calling the super method to initialize the main parameters
        super().__init__(starttime=0,stoptime=120,dt=1,name ='SimpleProjectManagament_scenario80' )

        # Stocks
        openTasks = self.stock("openTasks")
        closedTasks = self.stock("closedTasks")
        staff = self.stock("staff")

        # Flows
        completionRate = self.flow("completionRate")

        # Converters
        currentTime = self.converter("currentTime")
        remainingTime = self.converter("remainingTime")
    
       ...
        # Constants
        deadline = self.constant("deadline")
        effortPerTask = self.constant("effortPerTask")
        
        ...

        # Actual Logic

        openTasks.initial_value = 100
        closedTasks.initial_value = 0  # not really necessary, but I like to be explicit

        ...

        completionRate.equation = sd.max(0, sd.min(openTasks, staff * (productivity / effortPerTask)))
```


The model's class name __has to be__ ``simulation_model``, subclassing ``BPTK_Py.Model``. Following the call to the ``super().__init__`` method to setup the main parameters, 
we start defining the stocks, flows, converters and constants. You can set the equation using simple mathematical operators rather than defining complex Python code. 
Furthermore, the API implements some SystemDynamics functions such as min/max using the prefix ``sd.``
The API internally makes sure to create the equation logic in Python and register them with the model.

To use this model within your preferred environment, you can either import and initialize it within your code. Each model element can easily be plotted using ``element.plot(starttime=0,stoptime=120,dt=1)``.
But for convenience you may store it in a subfolder of your project and initialize it with ``BPTK`` instead. As for the generated models, we use the JSON notation. Store the following file in the ``scenarios/`` subfolder:
````json
{
  "smSimpleProjectManagement_Manual": {
    "model": "simulation_models/simple_project_manual",
    "base_constants": {
      "deadline": 100,
      "initialOpenTasks": 100
    },
    "base_points": {
      "productivity":  [ [0,0.4],[0.25,0.444],[0.5,0.506],[0.75,0.594],[1,1],[1.25,1.119],[1.5,1.1625],[1.75,1.2125],[2,1.2375],[2.25,1.245],[2.5,1.25] ]
    },
    "scenarios": {
      "scenario100": {
        "constants": {
          "initialOpenTasks": 100
        } } } } }
````

We highly recommend looking at our blog posts for details on BPTK, the System Dynamics API and the agent based models. 
Another great source for getting started is the regularly-updated [interactive tutorial](https://www.transentis.com/products/business-prototyping-toolkit/)!


# Links
[1] https://pip.pypa.io/en/stable/installing/

# License
Copyright (c) 2018 transentis labs GmbH <support@transentis.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Changelog

## 0.4.0
- Framework for Agent Based models
- Framework for defining System Dynamics models in code with less effort

## 0.3.7
- PULSE functions can now be defined within Jupyter environment. Just use the new ``pulse_function_create(scenarios,scenario_managers)`` method and be surprised.
- Cleaner method for strategy simulation. Now running stepwise, not using a complex while loop anymore. Improves readability tremendously!
- Optimize imports using ```__init__.py``` properly.
- Correct handling of decimal ``dt`` values within simulator. 


## 0.3.6.1
- Bugfix to reduce size of the package


## 0.3.6
- Now interpreting strategies that modify at '0' as constants values and overwrite the constants
- Use DT of simulation model 

## 0.3.5.5
- Fixed a bug that prevented from plotting properly when giving multiple scenario managers where one of them did not store the given scenario name

## 0.3.5.4
- Monitoring of Scenario JSON files:
    - Reload scenarios upon change (also works if Scenario manager spreads over multiple files)
    - Find added scenarios
    - Merge base values spread over multiple files
    

## 0.3.5.3
- horizontal lines in graphs to improve readability
- Improvements to readme file
- Small bug fixes
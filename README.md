# Predictive Analytics

Prediction for VISSIGHT data and csv Files with PROPHET and ARIMA


# Getting Started!

Requirements:
  - Git
  - PyCharm
  - Miniconda3 - tested with Python 3.7

#

Step 1: Clone it

-  start PyCharm -> Get from Version Control -> 
Repository URL -> select Version Control Git and clone: 
https://github.com/kaymaky/Predictive_Analytics_Project.git

#
Step 2: Create temporary environtment

-  File -> Settings -> Project: Predictive_Analytics_Project -> 
Project Interpreter -> settings_symbol -> ADD -> Conda Environment, check New Environment and confirm it

#
Step 3: Install the needed environment with the given environment.yml file

-  go in Terminal of PyCharm and put in: 
```sh
$ conda env create –f environment.yml
```

#
Step 4: bind the needed environment with the project

- similar process like step 2
File -> Settings -> Project: Predictive_Analytics_Project -> 
Project Interpreter -> settings_symbol -> ADD -> Conda Environment, check Existing Environment, add path to needed Environment and confirm


#
Step 5: setup django server

- Add Configuration -> + -> select django server -> give it a name and under Environment variables:
```sh
PYTHONUNBUFFERED=1;DJANGO_SETTINGS_MODULE=Predictive_Analytics_Project.settings
```

confirm it and start server

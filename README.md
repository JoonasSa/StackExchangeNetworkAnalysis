# Project

Group project for University of Helsinki's cource Network Analysis. 

We try to analyse and visualize open Stack Exchange data dump.

The project is run in a Jupyter Notebook inside of a Python3 virtual environment.

# Installation

You should have Python3 installed.

Run `python3 -m venv venv` to create a Python3 virtual environment called _venv_.

This virtual enviroment can be accessed by running `source venv/bin/activate` in the project root.

Using virtual environments is good practise with Python as handling global dependecies can get quite irritating.

After entering venv run `pip3 install -r requirements.txt` to install project dependencies.

Download the data dump from https://archive.org/details/stackexchange.

If everything went correct you should be ready now.

# Development and running project

Just access the virtual environment by running `source venv/bin/activate` in the project root.

Run `jupyter notebook` to launch notebook. The notebook should be running on _localhost:8888_.

You can also run the main file with `python3 main.py`. This might not be needed for the project.
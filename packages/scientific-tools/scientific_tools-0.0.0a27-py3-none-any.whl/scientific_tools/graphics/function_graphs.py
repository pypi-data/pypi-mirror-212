"""This module trace function graphs."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def set_label(labellingFunction, label) : 
    """Utility function. Set a label (or a title) to ax
    
    labelingFunction is the function use to add the label
    label can be a string, or a list of positional arguments, or a dict of keyword arguments
    """
    if isinstance(label, str) :
        labellingFunction(label)
    elif isinstance(label, list):
        labellingFunction(*label)
    else :
        labellingFunction(**label)


def plot_2Dfunction(function,
min_x: float, max_x: float, values_number: int,
args_before_x: list=[], args_after_x: list=[], function_kwargs: dict={},
title: str="", xlabel: str="", ylabel: str="", function_label: str="",
plot_kwargs:dict={}) :
    """Trace the 2D graphic of the function "function"
    
    function is a function with at least one argument x
    args_before_x is the list of positional arguments before the variable argument's position
    args_after_x is the list of positional arguments after the variable argument's position
    function_kwargs is a dictionary with keyword arguments to function
    
    The value of the variable argument x varies from min_x to max_variable by taking values_number values

    title can be the graph title or a list/a dict of (kw)args to plt.title
    xlabel and ylabel are texts/args/kwargs to put on the axes
    function_label is the label of the function. (Doesn't show it if you doesn't call plt.legend() after this plot_2Dfunction.)
    plot_kwargs is a dictionary with keyword arguments to plt.plot function (cf Matplotlib docs for futher information).
    """
    variable_list = np.linspace(min_x, max_x, values_number)
    results_list = []
    for variable in variable_list :
        results_list.append(function(*args_before_x, variable, *args_after_x, **function_kwargs))
    
    #displaying
    plt.plot(variable_list, results_list, label=function_label, **plot_kwargs)
    set_label(plt.title, title)
    set_label(plt.xlabel, xlabel)
    set_label(plt.ylabel, ylabel)

def plot_3Dfunction(function,
    min_x: float, max_x: float, values_x: int,
    min_y: float, max_y: float, values_y: int,
    args_before_variables: list=[], args_between_variables: list=[], args_after_variables: list=[], x_before_y: bool=True, function_kwargs: dict={},
    ax=None,
    title: str="", xlabel: str="", ylabel: str="", zlabel: str="", plot_kwargs: dict={"cmap":cm.RdYlGn}) :
    """Trace the 3D graphic of the function "function"
    
    function is a function with at least two arguments
    args_before_variable is the list of positional arguments before the first variable argument's position
    args_between_variables is the list of positional arguments between positions of the first and the second variable
    args_after_variables is the list of positional arguments after the second variable argument's position
    x_before_x is true if x variable is the first variable (in the function arguments order)
    function_kwargs is a dictionary with keyword arguments to function

    The value of the "x" variable varies from min_x to max_x by taking values_x values
    Idem for "y" variable
    
    ax a Ax object (a class of matplotplib.pyplot). ax is use to plot the function curve (if you doesn't give an ax, this function creates one)
    
    title is the graph title
    xlabel, ylabel and zlabel are texts to put on the axes
    plot_kwargs is a dictionary with keyword arguments to plt.plot_surface function (cf Matplotlib docs for futher information).
    """
    line = np.linspace(min_x, max_x, values_x)
    array_x = np.array([line for i in range(values_y) ], dtype=float)
    #create an array with x values
    column = np.linspace(min_y, max_y, values_y)
    array_y = np.array([[column[j]]*values_x for j in range(values_y)], dtype=float)
    #create an array with y values
    results = []#a array like object with values of function
    for i in range(values_y) :
        results_line = []
        for j in range(values_x) :
            variable1 = array_x[i][j]
            variable2 = array_y[i][j]
            if x_before_y is False :
                variable1, variable2 = variable2, variable1
            results_line.append(function(*args_before_variables, variable1, *args_between_variables, variable2, *args_after_variables, **function_kwargs))
        results.append(results_line)
    array_z = np.array(results, dtype=float)

    if "linewidth" not in plot_kwargs.keys() :
        plot_kwargs["linewidth"] = (max_x - min_x+ max_y - min_y)/20#to trace around 10 lines 

    #displaying
    if ax is None :
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(array_x, array_y, array_z, **plot_kwargs)#linewidth : distance between two lines
    
    set_label(ax.title, title)
    set_label(ax.set_xlabel, xlabel)
    set_label(ax.set_ylabel, ylabel)
    set_label(ax.set_zlabel, zlabel)

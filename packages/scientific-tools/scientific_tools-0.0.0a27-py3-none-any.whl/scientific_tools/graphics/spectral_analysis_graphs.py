"""This module trace figure to analyse spectrum of signals"""

import numpy as np
import matplotlib.pyplot as plt

import scientific_tools.physics.spectral_analysis as spectral_analysis
from scientific_tools.graphics.function_graphs import set_label

def plot_amplitudes_spectrum(function, f: float, fs: float,
    args_before_t: list=[], args_after_t: list=[], function_kwargs: dict={}, 
    title: str= "Spectrum of the signal", xlabel: str="Frequencies (in Hz)", ylabel: str="Amplitudes",
    plot_kwargs:dict={"color":"blue"}) :
    """Plot the amplitudes' spectrum of the function thanks to numpy.fft.fft()
    
    function is a function with at least one argument (the time)
    f is the signal frequency
    fs is the sampling frequency
    args_before_t is the list of positional arguments before the time argument's position
    args_after_t is the list of positional arguments after the time argument's position
    function_kwargs is a dict with kwargs to function

    title is the graph title
    xlabel and ylabel are texts to put on the axes
    
    plot_kwargs is a dict with kwargs to plot amplitudes with plt.vlines
    """
    frequencies = spectral_analysis.DFT_frequencies(f, fs)
    amplitudes = spectral_analysis.DFT_amplitudes_f(function, f, fs, args_before_t, args_after_t, function_kwargs)
    
    plt.vlines(frequencies, [0], amplitudes, **plot_kwargs)
    plt.axis([-1, 1.05*max(frequencies), 0, 1.05*max(amplitudes)])
    
    set_label(plt.title, title)
    set_label(plt.xlabel, xlabel)
    set_label(plt.ylabel, ylabel)

def plot_phases_spectrum(function, f: float, fs: float, deg: bool = True,
    args_before_t: list=[], args_after_t: list=[], function_kwargs:dict={},
    title: str= "Spectrum of the signal", xlabel: str="Frequencies (in Hz)", ylabel: str="Phases",
    plot_kwargs:dict={"color":"blue"}) :
    """Plot the phases' spectrum of the function thanks to numpy.fft.fft()
    
    function is a function with at least one argument (the time)
    f is the signal frequency
    fs is the sampling frequency
    If deg is True phases are in degree, else they are in radians.
    args_before_t is the list of positional arguments before the time argument's position
    args_after_t is the list of positional arguments after the time argument's position
    function_kwargs is a dict with kwargs to function

    title is the graph title
    xlabel and ylabel are texts to put on the axes
    
    plot_kwargs is a dict with kwargs to plot amplitudes with plt.vlines
    """
    frequencies = spectral_analysis.DFT_frequencies(f, fs)
    phases = spectral_analysis.DFT_phases_f(function, f, fs, deg, args_before_t, args_after_t, function_kwargs)

    plt.vlines(frequencies, [0], phases, **plot_kwargs)
    max_y = np.pi
    if deg :
        max_y = 360
    plt.axis([-1, 1.05*max(frequencies), -1.05*max_y, 1.05*max_y])
    
    set_label(plt.title, title)
    set_label(plt.xlabel, xlabel)
    set_label(plt.ylabel, ylabel)

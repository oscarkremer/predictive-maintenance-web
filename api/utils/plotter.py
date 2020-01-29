from __future__ import division
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
plt.style.use('seaborn-darkgrid')


def plot_timeseries(timeseries, predictions, pred_points, legend, plot_name, extension='.png', color='y', alpha=0.5, error_function='None'):
    x_axis = np.linspace(0,len(timeseries)-1, len(timeseries))
    plt.plot(x_axis, timeseries)
    axis_predictions = np.linspace(len(timeseries)-pred_points -1 , len(timeseries) - 1, pred_points + 1)
    for prediction in predictions:
        plot_pred = []
        plot_pred.append(timeseries[-pred_points-1])
        for pred in prediction:
            plot_pred.append(pred)
        plt.plot(axis_predictions, plot_pred)
    path = 'data/plots/'
    plt.ylim(top=0.5)
    plt.ylim(bottom=-0.2)
    plt.legend(legend)
    plt.savefig(path + plot_name + extension, transparent=False)
    plt.clf()



def plot(timeseries, prediction, pred_points, legend, plot_name, extension='.png', color='y', alpha=0.5, error_function='None'):
    x_axis = np.linspace(0,len(timeseries)-1, len(timeseries))
    plt.plot(x_axis, timeseries)
    axis_predictions = np.linspace(len(timeseries)-pred_points - 1, len(timeseries) - 1, pred_points + 1)
    plot_pred = []
    plot_pred.append(timeseries[-pred_points-1])
    for pred in prediction:
        plot_pred.append(pred)
    plt.plot(axis_predictions, plot_pred)
    path = 'data/plots/'
    plt.ylim(top=0.5)
    plt.ylim(bottom=-0.2)
    plt.legend(['real-DES', legend])
    plt.savefig(path + plot_name + extension, transparent=False)
    plt.clf()


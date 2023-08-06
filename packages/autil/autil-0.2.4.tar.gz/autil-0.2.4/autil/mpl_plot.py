"""
Useful plots in data anlysis
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from labellines import labelLine, labelLines

if __name__ != "__main__":
    __version__ = 0.1


def add_label_for_lines(ax, lw=3, zorder=2.5):
    """
    Add line labels for a line plot
    """
    ax.get_lines()[-1].set(lw=lw)
    labelLines(ax.get_lines(), zorder=zorder)
    return ax

def plot_scatter_with_text(
        data, x, y, z, hue=None, style=None,
        text_condition=None, text_adjust=False, adjust_precision=0.1):
    """
    Use seaborn, matplotlib and adjustText to plot scatter with text
    """
    data = data.copy().reset_index(drop=True)
    ax = sns.scatterplot(data=data, x=x, y=y, hue=hue, style=style)
    if isinstance(text_condition, pd.Series):
        data = data[text_condition].reset_index(drop=True)
    texts = [ax.annotate(text, (data.loc[i, x], data.loc[i, y])) for i, text in enumerate(data[z].values)]
    if text_adjust:
        from adjustText import adjust_text
        adjust_text(texts, precision=adjust_precision)
    return ax


def plot3D(x_min, x_max, y_min, y_max, x_n, y_n, z_func,
           x_label='x', y_label='y', z_label='z', zlim=None,
           figsize=(8, 6), cmap='summer', alpha=0.8, rotate=225):
    """
    This code is used to plot the 3D figure of a function with two variables
    """
    x_vals = np.linspace(x_min, x_max, x_n)
    y_vals = np.linspace(y_min, y_max, y_n)
    x_mesh, y_mesh = np.meshgrid(x_vals, y_vals, indexing='ij')
    try:
        z_vals = z_func(x_mesh, y_mesh)
    except ValueError:
        z_vals = np.zeros((x_n, y_n))
        for i in range(x_n):
            for j in range(y_n):
                z_vals[i, j] = z_func(x_vals[i], y_vals[j])
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    ax = fig.gca(projection='3d')
    ax.plot_surface(x_mesh, y_mesh, z_vals, cmap=cmap, alpha=alpha)  # winter
    ax.set(xlabel=x_label, ylabel=y_label, zlabel=z_label, zlim=zlim,)
    ax.zaxis.set_rotate_label(False)  # ?
    ax.view_init(ax.elev, rotate)  # view direction
    plt.close()
    return fig

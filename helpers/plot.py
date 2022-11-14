# Helper functions for calculating flux and plotting the gridded predictions
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_squared_error

def obs_vs_pred(obs, pred, ax=None, **kwargs):
    """
    Plot obs vs. pred, along with a 1:1 line and fit statistics.
    
    Paramerters
    -----------
    obs : array-like
        The observed data
    pred : array-like
        The predicted data
    ax : matplotlib.axes._subplots.AxesSubplot (optional)
        An axis to plot the data on. If None, a new figure
        is created with a single axis.
    **kwargs
        Passed to `ax.scatter()`.
        
    Returns
    -------
    fig, ax
    """
    
    if ax is None:
        fig, ax = plt.subplots(1,1)
    else:
        fig = ax.get_figure()
    
    r2 = r2_score(obs, pred)
    rmse = mean_squared_error(obs, pred)**0.5
    
    ax.scatter(obs, pred, label=f'{r2:0.3f}, {rmse:0.2f}', **kwargs)
    
    mn = min(ax.get_xlim()[0], ax.get_ylim()[0])
    mx = max(ax.get_xlim()[1], ax.get_ylim()[1])
    ax.set_xlim(mn,mx)
    ax.set_ylim(mn,mx)    
    ax.plot([mn,mx], [mn,mx], ls='dashed', c=(0,0,0,0.6))
    
    ax.legend(title='R2, RMSE')
    
    return fig, ax

def grid(pred, grid_df, clabel=None, **kwargs):
    """
    Transforms gridded prediction data to 2D array and plots it.
    
    Parameters
    ----------
    pred_DeltaCO2 : array-like
        Predicted values produced from the data in `testmap.csv`.
    grid_df : pandas.DataFrame
        Dridded predictor data containing lat and lon.
    
    Returns
    -------
    None
    """
    pred_grid = np.full((178, 360), np.nan)
    lon = np.arange(-179.5, 179.6, 1)
    lat = np.arange(-88.5, 88.6, 1)
    X, Y = np.meshgrid(lon, lat)
    if 'cmap' not in kwargs:
        kwargs['cmap'] = plt.cm.RdBu_r

    # assemble 2D grid
    for i, p in enumerate(pred):
        r = grid_df.iloc[i]
        pred_grid[(X==r.lon)  & (Y==r.lat)] = p
    
    fig = plt.figure(figsize=[8, 5])
    plt.pcolormesh(X, Y, pred_grid, shading='auto', 
                   **kwargs)
    if clabel is None:
        if hasattr(pred, 'name'):
            clabel = pred.name
        else:
            clabel = 'Predicted $\Delta pCO_2$'
    plt.colorbar(label=clabel)
    
def hist(obs_DeltaCO2, pred_DeltaCO2):
    """
    Plot histograms of observed and predicted Delta_CO2 data.
    
    Parameters
    ----------
    pred_DeltaCO2 : array-like
        Observed DeltaCO2 values from the GLODAP database.
    pred_DeltaCO2 : array-like
        Predicted DeltaCO2 values.
        
    Returns
    -------
    None
    """
    bins = np.linspace(-150, 100, 50)
    plt.hist(obs_DeltaCO2, bins=bins, label='GLODAP Bottles 2001-2015')
    plt.hist(pred_DeltaCO2, bins=bins, alpha=0.7, label='Prediction Feb 2019');
    plt.legend()
    plt.xlabel('$\Delta pCO_2$')
    plt.ylabel('n')
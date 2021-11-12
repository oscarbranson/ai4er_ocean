import numpy as np

def CO2_flux(DelCO2, grid_wind, unit='Pg'):
    """
    Returns carbon flux in moles, g or Pg (1e15 g) of carbon (not CO2) per year.
    
    F = A * E * DeltaCO2
    
    where:
        A is area in m2
        E is the gas transfer coefficient (mol CO2 m-2 yr-1 uatm-1) from Wanninkhof (1992)
        DeltaCO2 is the difference in pCO2 in uatm
    
    The gas transfer coefficient is an area of uncertainty. See Takahashi et al (1997, 10.1073/pnas.94.16.8292) for discussion.
    
    """
    E = 1.13e-3 * grid_wind.wind**2  # Gas transfer coefficient from Wanninkhof (1992)
    F = np.sum(grid_wind.area * E * DelCO2) # moles of C yr-1
    
    mC = 12.0107  # mass of C
    
    if unit=='g':
        return F * mC
    elif unit=='Pg':
        return  F * mC * 1e-15
    
    return F
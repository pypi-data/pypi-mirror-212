# SolFinder 

A library to find a solution among a set of Pareto optimal solutions, according to the preferences of the decision-maker.
In particular, this library has been developed with the aim of identifying eco-efficient aircraft trajectories.

**License:**

SolFinder is released under GNU Lesser General Public License v3.0 (LGPL-3.0-or-later).

**Copyright notice:**

Technische Universiteit Delft hereby disclaims all copyright interest in the program “SolFinder” (library to find a solution among a set of Pareto optimal solutions, in particular, eco-efficient aircraft trajectories) written by the Author(s).

Henri Werij, Faculty of Aerospace Engineering, Technische Universiteit Delft.

© 2023 Federica Castino

## Installation

```
pip install solfinder
```

## Get started

```python

import solfinder.MCDM as MCDM
import numpy as np
import matplotlib.pyplot as plt

# Upload example dataset
with open(r'tests/Data_example/POBJ_20180101000005_0_51_28_41.dat', 'r') as f:
    data = np.loadtxt(f, unpack=True)

# Values of objective functions
soc = data[0]
atr = data[1]

# Number of Pareto optimal solutions
n_sol = len(soc)

# Find Pareto optimal solutions using available options
index_target_05 = MCDM.Target.solution_found_with_target(MCDM.Target(),0.5,soc)
index_gra       = MCDM.GRA.solution_found_by_gra(MCDM.GRA(), data)
index_topsis    = MCDM.TOPSIS.solution_found_by_topsis(MCDM.TOPSIS(), data, [0.5,0.5])
set_indices_vikor, index_vikor = MCDM.VIKOR.solution_found_by_vikor(MCDM.VIKOR(), data, 0.5, [0.5, 0.5])

# Plot of Pareto front and selected solutions
plt.scatter(100 * (atr - max(atr)) / max(atr),
            MCDM.Target.rel_change(soc), s=20, c='grey')
plt.scatter(100 * (atr[index_target_05] - max(atr)) / max(atr),
            100 * (soc[index_target_05] - min(soc)) / min(soc), s=40, c='red', label='Target +0.5% SOC')
plt.scatter(100 * (atr[index_gra] - max(atr)) / max(atr),
            100 * (soc[index_gra] - min(soc)) / min(soc), s=40, c='blue', label='GRA')
plt.scatter(100 * (atr[index_topsis] - max(atr)) / max(atr),
            100 * (soc[index_topsis] - min(soc)) / min(soc), s=40, c='orange', label='TOPSIS')
plt.scatter(100 * (atr[index_vikor] - max(atr)) / max(atr),
            100 * (soc[index_vikor] - min(soc)) / min(soc), s=40, c='green', label='VIKOR')
plt.xlabel(r'Change in ATR20 [%]', fontsize=16, labelpad=15)
plt.ylabel(r'Change in SOC [%]', fontsize=16, labelpad=15)
plt.title('Number of solutions: {}'.format(n_sol))
plt.legend()
plt.grid(True)
plt.show()

```

## Acknowledgements

This library has been developed within EU-Projects FlyATM4E. FlyATM4E has received funding from the SESAR Joint Undertaking under the European Union's Horizon 2020 research and innovation programme under grant agreement No 891317. The JU receives support from the European Union’s Horizon 2020 research and innovation programme and the SESAR JU members other than the Union.

# dpdata_abinit
Abinit plugin for dpdata

Install
```
pip install .
```

Usage:

1. Prepare the abinit histfile which contains a set of structures 
and the corresponding energies, forces, and stresses. Here we call this file
 Abinit_hist_file.abihist

2. Write a python script like this. 
```Python
#!/usr/bin/env python3

import dpdata
# load data from the file Abinit_hist_file.abihist
d = dpdata.LabeledSystem("Abinit_hist_file.abihist", format='abihist')
# write to raw file
d.to_deepmd_raw('00.data')
# You can also write to npy file.  The data set is splitted into multiple npy files, each containing set_size of samples.
d.to_deepmd_npy('00.data', set_size=2638)
```

3. Run the script 

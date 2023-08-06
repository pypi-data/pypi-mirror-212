"""
Convert the Abinit HIST netcdf file to DeepMD raw file.
"""
import os
import numpy as np
from abipy.dynamics.hist import HistFile
from dpdata.format import Format
from dpdata_abinit.histnc import to_system_data


def to_system_data(fname,  rotate_structures=False):
    hist=HistFile.from_file(fname)
    ntime=hist.num_steps
    structures=hist.structures
    s0=structures[0].to_ase_atoms()

    symbols = s0.get_chemical_symbols()
    atom_names = list(set(symbols))
    atom_numbs = [symbols.count(symbol) for symbol in atom_names]
    atom_types = np.array([atom_names.index(symbol) for symbol in symbols]).astype(int)

    system={'atom_names': atom_names,
            'atom_numbs': atom_numbs,
            'atom_types': atom_types,
            'orig': np.zeros(3),
            'nopbc': not np.any(s0.get_pbc())
            }
    system['cells']=[]
    system['coords']=[]
    system['forces']=[]
    system['energies']=hist.etotals.tolist()
    # stress tensor in GPa
    system['virials'] =   hist.reader.read_cart_stress_tensors()[0]

    for s in structures:
        atoms=s.to_ase_atoms()
        system['cells'].append(atoms.get_cell().array)
        system['coords'].append(atoms.get_positions())
        system['forces'].append(atoms.arrays["cartesian_forces"])
        #system['forces'].append(atoms.arrays.cartesian_forces.flatten())



    system['cells'] = np.array(system['cells'])
    system['coords'] = np.array(system['coords'])
    system['energies'] = np.array(system['energies'])
    system['forces'] = np.array(system['forces'])

    # check the unit of the stress
    if 'virials' in system:
        # TODO: check this against https://github.com/mailhexu/dpdata/blob/master/dpdata/plugins/ase.py
        # line 162, where 1e3 is 1e4.
        #kbar-> virial  1e3
        #GPar-> virial  1e4
        v_pref = -1 * 1e4 / 1.602176621e6
        for ii in range(system['cells'].shape[0]):
            vol = np.linalg.det(np.reshape(system['cells'][ii], [3, 3]))
            system['virials'][ii] *= v_pref * vol
    return system

def write_npy_files(system, path):
    np.save(os.path.join(path, 'box.npy'), system['cells'])
    np.save(os.path.join(path, 'energy.npy'), system['energies'])
    np.save(os.path.join(path, 'forces.npy'), system['forces'])
    np.save(os.path.join(path, 'coords.npy'), system['coords'])


@Format.register("abihist")
class AbihistFormat(Format):
    def from_system(self, fname, **kwargs):
        return None

    def from_labeled_system(self, fname, **kwargs):
        return to_system_data(fname)

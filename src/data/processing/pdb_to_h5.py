
import numpy as np
import h5py
import argparse
import pickle
import sys
import os
import urllib.request
import pytraj as pt


def download_pdbfile(pdb):
    if not os.path.isfile(pdb+'.pdb'):
        urllib.request.urlretrieve('http://files.rcsb.org/download/'+pdb.upper()+'.pdb', pdb+'.pdb')

def run_leap(fileName, path):
    leapText = """
    source leaprc.protein.ff14SB
    source leaprc.water.tip3p
    exp = loadpdb PATH4amb.pdb
    saveamberparm exp PATHexp.top PATHexp.crd
    quit
    """
    with open(path+"leap.in", "w") as outLeap:
        outLeap.write(leapText.replace('PATH', path))	
    os.system("tleap -f "+path+"leap.in >> "+path+"leap.out")

def convert_to_amber_format(pdbName):
    fileName, path = pdbName+'.pdb', pdbName+'/'
    os.system("pdb4amber -i "+fileName+" -p -y -o "+path+"4amb.pdb -l "+path+"pdb4amber_protein.log")
    run_leap(fileName, path)
    traj = pt.iterload(path+'exp.crd', top = path+'exp.top')
    pt.write_traj(path+fileName, traj, overwrite= True)
    print(path+fileName+' was created. Please always use this file for inspection because the coordinates might get translated during amber file generation and thus might vary from the input pdb file.')
    return pt.iterload(path+'exp.crd', top = path+'exp.top')

def get_maps(mapPath):
    residueMap = pickle.load(open(mapPath+'atoms_residue_map_generate.pickle','rb'))
    nameMap = pickle.load(open(mapPath+'atoms_name_map_generate.pickle','rb'))
    typeMap = pickle.load(open(mapPath+'atoms_type_map_generate.pickle','rb'))
    elementMap = pickle.load(open(mapPath+'map_atomType_element_numbers.pickle','rb'))
    return residueMap, nameMap, typeMap, elementMap

def get_residues_atomwise(residues):
    atomwise = []
    for name, nAtoms in residues:
        for i in range(nAtoms):
            atomwise.append(name)
    return atomwise

def get_traj_info(traj, mapPath):
    coordinates  = traj.xyz
    residueMap, nameMap, typeMap, elementMap = get_maps(mapPath)
    types = [typeMap[a.type] for a in traj.top.atoms]
    elements = [elementMap[typ] for typ in types]
    atomic_numbers = [a.atomic_number for a in traj.top.atoms]
    molecule_begin_atom_index = [m.begin_atom for m in traj.top.mols]
    residues = [(residueMap[res.name], res.n_atoms) for res in traj.top.residues]
    residues_atomwise = get_residues_atomwise(residues)
    return coordinates[0], elements, types, atomic_numbers, residues_atomwise, molecule_begin_atom_index

def write_h5_info(struct, atoms_type, atoms_number, atoms_residue, atoms_element, molecules_begin_atom_index, atoms_coordinates_ref):
    with h5py.File('inference_from_pdb.hdf5', 'a') as oF:
        subgroup = oF.create_group(struct)     
        subgroup.create_dataset('atoms_residue', data= atoms_residue, compression = "gzip", dtype='i8')
        subgroup.create_dataset('molecules_begin_atom_index', data= molecules_begin_atom_index, compression = "gzip", dtype='i8')
        subgroup.create_dataset('atoms_type', data= atoms_type, compression = "gzip", dtype='i8')
        subgroup.create_dataset('atoms_number', data= atoms_number, compression = "gzip", dtype='i8')  
        subgroup.create_dataset('atoms_element', data= atoms_element, compression = "gzip", dtype='i8')
        subgroup.create_dataset('atoms_coordinates_ref', data= atoms_coordinates_ref, compression = "gzip", dtype='f8')
        subgroup.create_dataset('atoms_soft_hard', data= -np.ones(np.shape(atoms_type)), compression = "gzip", dtype='f8')
        subgroup.create_dataset('atoms_soft_hard_std', data= -np.ones(np.shape(atoms_type)), compression = "gzip", dtype='f8')


def setup(args):
    if args.pdbid is None and args.fileName is None:
        sys.exit('Please provide pdb-id or pdb file name')
    if args.fileName == None:
        pdbName = args.pdbid
        if not os.path.isdir(pdbName):
            os.mkdir(pdbName)
        download_pdbfile(pdbName)
    else:
        pdbName = args.fileName.split('.pdb')[0]
        if not os.path.isdir(pdbName):
            os.mkdir(pdbName)
    return pdbName    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument("-dataset", "--dataset", required=False, help="Dataset in hdf5 format", default='MD_dataset_mapped.hdf5', type=str)
    parser.add_argument("-pdbid", "--pdbid", required=False, help="ID that will be downloaded from the PDB", type=str)
    parser.add_argument("-fileName", "--fileName", required=False, help="Name of the pdb file, e.g. 1a4s.pdb", type=str)
    parser.add_argument("-mapPath", "--mapPath", required=False, help="Path to the maps for generating the h5 files", default= 'Maps/', type=str)
    parser.add_argument("-mask", "--mask", required=False, help="Mask that is applied on Trajectory, e.g. '!@H=' for no hydrogens, '@CA' for only ca atoms; see https://amberhub.chpc.utah.edu/atom-mask-selection-syntax/ for more info", default= '', type=str)    
    args = parser.parse_args()
    
    pdbName = setup(args)
    traj = convert_to_amber_format(pdbName)
    atoms_coordinates_ref, atoms_element, atoms_type, atoms_number, atoms_residue, molecules_begin_atom_index = get_traj_info(traj[args.mask], args.mapPath)
    write_h5_info(pdbName, atoms_type, atoms_number, atoms_residue, atoms_element, molecules_begin_atom_index, atoms_coordinates_ref)
    os.system('rm leap.log')








import numpy as np
import h5py
import argparse
import pickle
import sys
import os
import urllib.request
import re

atomic_numbers_Map = {1:'H',4:'Be', 5:'B', 6:'C', 7:'N', 8:'O',9:'F', 11:'Na',12:'Mg',14:'Si',15:'P',16:'S',17:'Cl',19:'K',20:'Ca',23:'V',26:'Fe',27:'Co', 29:'Cu',30:'Zn',33:'As',34:'Se', 35:'Br',44:'Ru', 45:'Rh',51:'Sb',52:'Te',53:'I', 75:'Re', 76:'Os', 77:'Ir', 78:'Pt'}
inv_atomic_numbers_Map = {v:k for k,v in atomic_numbers_Map.items()}


def download_pdbfile(pdb):
    if not os.path.isfile(pdb+'.pdb'):
        urllib.request.urlretrieve('https://files.rcsb.org/ligands/download/'+pdb.upper()+'_model.sdf', pdb+'.sdf')

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

def read_sdf_file(pdbName):
    print('reading', pdbName+'.sdf')
    file = open(pdbName+'.sdf', mode="r")
    content = file.read()
    file.close()
    match = re.search(r"^ {3,}-?\d.*(?:\r?\n {3,}-?\d.*)*", content, re.M)
    datasplit = []
    if match:
        for line in match.group().splitlines():
            datasplit.append([part for part in line.split()][:4])
    return datasplit

def write_h5_info(struct, atoms_type, values):
    with h5py.File('inference_for_qm.hdf5', 'a') as oF:
        structgroup = oF.create_group(struct)     
        atomprop_group = structgroup.create_group('atom_properties')
        molprop_group = structgroup.create_group('mol_properties')    
        atomprop_group.create_dataset('atoms_names', data= atoms_type, compression = "gzip", dtype = "i8")
        atomprop_group.create_dataset('atom_properties_values', data= values, compression = "gzip", dtype='f8')
        molprop_group.create_dataset('Electron_Affinity', data= [0], compression = "gzip", dtype = "f8")
        molprop_group.create_dataset('Hardness', data= [0], compression = "gzip", dtype = "f8")
        #atomprop_group.create_dataset('atoms_names', data= atoms_residue, compression = "gzip", dtype='i8')
        #atomprop_group.create_dataset('atoms_names', data= atoms_residue, compression = "gzip", dtype='i8')        
        #subgroup.create_dataset('atoms_type', data= atoms_type, compression = "gzip", dtype='i8')
        #subgroup.create_dataset('atoms_number', data= atoms_number, compression = "gzip", dtype='i8')  
        #subgroup.create_dataset('molecules_begin_atom_index', data= molecules_begin_atom_index, compression = "gzip", dtype='i8')
        #subgroup.create_dataset('atoms_element', data= atoms_element, compression = "gzip", dtype='i8')
        #subgroup.create_dataset('atoms_coordinates_ref', data= atoms_coordinates_ref, compression = "gzip", dtype='f8')
        #subgroup.create_dataset('atoms_soft_hard', data= -np.ones(np.shape(atoms_type)), compression = "gzip", dtype='f8')
        #subgroup.create_dataset('atoms_soft_hard_std', data= -np.ones(np.shape(atoms_type)), compression = "gzip", dtype='f8')

def process_content(content):
    print(inv_atomic_numbers_Map)
    x, y, z, atom_type = [], [], [], []    
    for x_i, y_i, z_i, atom_type_i in content:
        x.append(float(x_i))
        y.append(float(y_i))
        z.append(float(z_i))
        atom_type.append(inv_atomic_numbers_Map[atom_type_i])
    values = np.array([x,y,z]).T
    padded_values = np.pad(values, ((0,0),(0,25)), mode='constant', constant_values=(0))
    return padded_values, atom_type

def setup(args):
    if args.pdbid is None and args.fileName is None:
        sys.exit('Please provide pdb-id or pdb file name')
    if args.fileName == None:
        pdbName = args.pdbid
        if not os.path.isdir(pdbName):
            os.mkdir(pdbName)
        download_pdbfile(pdbName)
    else:
        pdbName = args.fileName.split('.sdf')[0]
        if not os.path.isdir(pdbName):
            os.mkdir(pdbName)
    return pdbName    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument("-dataset", "--dataset", required=False, help="Dataset in hdf5 format", default='MD_dataset_mapped.hdf5', type=str)
    parser.add_argument("-pdbid", "--pdbid", required=False, help="ID that will be downloaded from the PDB Ligand", type=str)
    parser.add_argument("-fileName", "--fileName", required=False, help="Name of the sdf file, e.g. vww.sdf", type=str)
    parser.add_argument("-mapPath", "--mapPath", required=False, help="Path to the maps for generating the h5 files", default= 'Maps/', type=str)
    #parser.add_argument("-mask", "--mask", required=False, help="Mask that is applied on Trajectory, e.g. '!@H=' for no hydrogens, '@CA' for only ca atoms; see https://amberhub.chpc.utah.edu/atom-mask-selection-syntax/ for more info", default= '', type=str)    
    args = parser.parse_args()
    
    pdbName = setup(args)
    content = read_sdf_file(pdbName)
    values, atom_types = process_content(content)
    print('values, atom types',values, atom_types)
    print(np.shape(values))
    write_h5_info(pdbName, atom_types, values)
    #traj = convert_to_amber_format(pdbName)
    #atoms_coordinates_ref, atoms_element, atoms_type, atoms_number, atoms_residue, molecules_begin_atom_index = get_traj_info(traj[args.mask], args.mapPath)
    #write_h5_info(pdbName, atoms_type, atoms_number, atoms_residue, atoms_element, molecules_begin_atom_index, atoms_coordinates_ref)
    #os.system('rm leap.log')







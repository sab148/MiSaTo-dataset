<div align="center">

# MISATO - Machine learning dataset for structure-based drug discovery

[![python](https://img.shields.io/badge/-Python_3.7_%7C_3.8_%7C_3.9_%7C_3.10-blue?logo=python&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pytorch](https://img.shields.io/badge/PyTorch_1.10+-ee4c2c?logo=pytorch&logoColor=white)](https://pytorch.org/get-started/locally/)
[![lightning](https://img.shields.io/badge/-Lightning_1.8+-792ee5?logo=pytorchlightning&logoColor=white)](https://pytorchlightning.ai/)


**Code base for QM and MD dataset**

- Quantum Mechanics: 19443 ligands, curated and refined
- Molecular Dynamics: 16972 protein-ligand structures, 10 ns 
- AI: pytorch dataloaders, base line models for MD and QM

![Alt text](logo.jpg?raw=true "MISATO")

## :purple_heart: Community

[Join our discord server!](https://discord.gg/tGaut92VYB)
Lets crack the **100 ns** MD, **30000 structures** and whole new world of **AI models** together.

## 📌  Introduction 
 
In this repository, we show how to load QM (Quantum Mechanics) and MD (Molecular Dynamics) dataset (h5 file). You can access the properties of different structures and use them in Pytorch based dataloaders. We provide a small sample of our dataset along with the repo.

You can download the FULL dataset from Zenodo using links below:

- MD
- QM
 
_Suggestions are always welcome!_





**You can use the notebook src/getting_started.ipynb to :**

- Understand the structures of our H5 files and read each molecule's properties.
- Load the PyTorch Dataloaders of each dataset.
- Load the PyTorch lightning Datamodules of each dataset.

<br>

## Required packages:

- torch>=1.10.0
- pytorch-lightning==1.8.3
- torch-geometric==2.0.4

<br>

## Project Structure

```
├── data                   <- Project data
│
│
│
├── src                    <- Source code
│   ├── data                    
│   │   ├── components           <- Datasets and transforms
│   │   ├── md_datamodule.py     <- MD Lightning data module
│   │   └── qm_datamodule.py     <- QM Lightning data module
│   │
│   │
│   └── getting_started.ipynb     <- Jupyter notebook : how to load h5 files, load dataset, datamodules and iterate over the data
│   └── inference.ipynb           <- Jupyter notebook : how to run inference
│
├── .gitignore                <- List of files ignored by git
├── requirements.txt          <- File for installing python dependencies
└── README.md
```

<br>

## 🚀  Quickstart

We recommend to pull our misato image from DockerHub or to create your own image (see [docker/](docker/)).  The images use cuda version 11.8. We recommend to install on your own system a version of CUDA that is a least 11.8 to ensure that the drivers work correctly.

```bash
# clone project
git clone https://github.com/sab148/MiSaTo-dataset.git
cd MiSaTo-dataset
```
For singularity use:
```bash
# clone project
singularity pull ...
singularity shell misato.sif
```

For docker use: 

```bash
docker pull ...
docker ...
```


## Installation using your own conda environment

In case you want to use conda for your own installation please create a new misato environment.

In order to install pytorch geometric we recommend to use pip (within conda) for installation and to follow the official installation instructions:[pytorch-geometric/install](
https://pytorch-geometric.readthedocs.io/en/latest/install/installation.html)

Depending on you CUDA version the instructions vary. We show an example for the cpu version.

```bash
conda create --name misato python=3
conda activate misato
conda install -c anaconda h5py pandas ipykernel ipywidgets==7.7.2
conda install -c conda-forge nglview pytorch-lightning==1.8.3
pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv torch_geometric -f https://data.pyg.org/whl/torch-1.13.0+cpu.html
```

To run inference for MD you have to install ambertools. We recommend to install it in a separate conda environment.

```bash
conda create --name ambertools
conda activate ambertools
conda install -c conda-forge ambertools
```



```bash
# [OPTIONAL] create virtual environment
python3 -m venv misato_env/

# activate the env
source misato_env/bin/activate

# install requirements
pip install -r requirements.txt
```
Alternatively you can use anaconda to install the environment
```bash

# create conda env

conda env create -f misato.yml
# activate the env
conda activate misato


```
## Singularity





You can now go to src/getting_started.ipynb and discover with the MiSaTo dataset.

## ❤️  Contributions

Have a question? Found a bug? Missing a specific feature? Feel free to file a new issue, discussion or PR with respective title and description.

Suggestions for improvements are always welcome!

<br>


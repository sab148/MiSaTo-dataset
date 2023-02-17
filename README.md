<div align="center">

# MISATO - Machine learning dataset for structure-based drug discovery

[![python](https://img.shields.io/badge/-Python_3.7_%7C_3.8_%7C_3.9_%7C_3.10-blue?logo=python&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pytorch](https://img.shields.io/badge/PyTorch_1.10+-ee4c2c?logo=pytorch&logoColor=white)](https://pytorch.org/get-started/locally/)
[![lightning](https://img.shields.io/badge/-Lightning_1.8+-792ee5?logo=pytorchlightning&logoColor=white)](https://pytorchlightning.ai/)


Code base for QM and MD dataset <br>

We present a novel dataset of 16972 protein-ligand structures along with 19443 ligand structures originating from the pdbBind library. We used semi-empirical quantum mechanics to curate every ligand. The refined ligands were extensively simulated in the respective protein pockets in explicit water molecular dynamics simulations. You can use the dataset directly from h5 or via simple PyTorch/pytorch-lightning data loaders. Structures are enriched with a diverse set of semi-empirical and MD derived properties. With our novel and highly curated dataset, we ought to facilitate the generation of future AI models, bridging the gap between in silico and in vivo drug discovery.
</div>
 
<br>

## 📌  Introduction 
 
In this repository, we show how to load QM and MD dataset (h5 file). You can access the properties of different structures and use them in Pytorch based dataloaders. We provide a small sample of our dataset along with the repo.

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
│   
│
├── .gitignore                <- List of files ignored by git
├── requirements.txt          <- File for installing python dependencies
└── README.md
```

<br>

## 🚀  Quickstart

```bash
# clone project
git clone https://github.com/sab148/MiSaTo-dataset.git
cd MiSaTo-dataset

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

You can now go to src/getting_started.ipynb and discover with the MiSaTo dataset.

## ❤️  Contributions

Have a question? Found a bug? Missing a specific feature? Feel free to file a new issue, discussion or PR with respective title and description.

Suggestions for improvements are always welcome!

<br>


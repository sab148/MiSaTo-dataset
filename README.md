<div align="center">

# MISATO - Machine learning dataset for structure-based drug discovery

[![python](https://img.shields.io/badge/-Python_3.7_%7C_3.8_%7C_3.9_%7C_3.10-blue?logo=python&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pytorch](https://img.shields.io/badge/PyTorch_1.10+-ee4c2c?logo=pytorch&logoColor=white)](https://pytorch.org/get-started/locally/)
[![lightning](https://img.shields.io/badge/-Lightning_1.8+-792ee5?logo=pytorchlightning&logoColor=white)](https://pytorchlightning.ai/)


Code base for QM and MD dataset <br>

_Suggestions are always welcome!_

</div>

<br>

## 📌  Introduction

**You can use the notebook src/getting_started.ipynb to :**

- Understand the structures of our H5 files and read each molecule's properties.
- Load the PyTorch Dataloaders of each dataset.
- Load the PyTorch lightning Datamodules of each dataset.

<br>

## Required packages:

- Pytorch-lightning=1.6.1
- Pytorch-Geometric=2.0.4
- PyTorch=1.11
- h5py=3.5.0

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

# [OPTIONAL] create conda environment
conda create -n myenv python=3.9
conda activate misato

# install pytorch according to instructions
# https://pytorch.org/get-started/

# install requirements
pip install -r requirements.txt
```

You can now go to src/getting_started.ipynb and discover with the MiSaTo dataset.

## ❤️  Contributions

Have a question? Found a bug? Missing a specific feature? Feel free to file a new issue, discussion or PR with respective title and description.

Suggestions for improvements are always welcome!

<br>


# DSSynth features for sound collections

## User instructions

git clone https://github.com/prashanthtr/DSSoundCollection.git

cd DSSoundCollection/

conda create -n DSSoundCollection python=3.8 ipykernel

conda activate DSSoundCollection

python3 -m pip install -r requirements.txt --src '.'(please run twice - due to numba dependency error)


## Setup and run jupyter notebook

pip install jupyter

python3 -m ipykernel install --user --name DSSoundCollection

jupyter notebook

Select *SegmentDatabase.ipynb* in the browser interface

## Generate files from commandline

python3 generate.py
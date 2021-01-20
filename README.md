# DSSynth features for sound collections


## User instructions

git clone https://github.com/prashanthtr/DSSoundCollection.git

cd DSSoundCollection/

conda create -n DSSoundCollection python=3.8 ipykernel

conda activate DSSoundCollection

python3 -m pip install -r requirements.txt --src '.'(please run twice - due to numba dependency error)

## FolderSetup:

Create two folders:
1) Foldername: "srcwav". Place the sound collection files here.
2) Foldername: "segmented". The code places the segmented wav and param files here.

## Setup and run jupyter notebook

pip install jupyter

python3 -m ipykernel install --user --name DSSoundCollection

jupyter notebook

Select *SegmentDatabase.ipynb* in the browser interface

## Generate files from commandline

python3 segmentDatabase.py ChunkDuration Format_Type

>> Chunkduration: Integer/Float in seconds (e.g., 1 or 1.0)

>> Formattype : 0 or "paramManager", 1 or "sonyGan", 2 or "tfrecords".

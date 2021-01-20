import numpy as np
import os  # for mkdir
import sys
import math
import librosa # conda install -c conda-forge librosa
import soundfile as sf

from parammanager import paramManager
from sonyganformat import sonyGanJson
from utils import longSilence

datapath='srcwav'  #root folder
fileList = [f for f in os.listdir(datapath) if os.path.isfile(os.path.join(datapath, f)) and (os.path.splitext(f)[1]==".wav" or os.path.splitext(f)[1]==".aif" or os.path.splitext(f)[1]==".aiff")]
#stub: fileList = ["silence.wav"]

''' Chunk duration as specified in arguments'''
chunkDuration = int(sys.argv[1]); # 1 sec

''' Chunk files into Nsecond durations'''
for fileName in fileList:

    sig,sr=librosa.core.load(datapath + "/" + fileName, sr=None)
    Fs = 22050

    # resample
    sig= librosa.core.resample(sig, sr, 22050) 

    fileBase = os.path.splitext(fileName)[0]

    numSamplesPerChunk = chunkDuration*Fs;
    numChunks = math.floor(len(sig)/numSamplesPerChunk)
    segment = []

    mean = np.mean(sig)

    for i in range(numChunks-1):
        segment = sig[i*numSamplesPerChunk:(i+1)*numSamplesPerChunk]
        if len(segment) > 0:
            mean = np.mean(segment)
            x = [sample-mean for sample in segment] #dc filter
            if( longSilence(x, 0.01) ):
                print(fileBase + " ",  i)
                norm = librosa.util.normalize(x)
                sf.write("segmented" + "/" + fileBase + "--" + "v-" + str(i) + ".wav", norm, sr)
            else:
                print("Discarding a silent segment ", i)
            i = i + 1;
        else:
            print("Discarding a segment ", i)

'''' Generate records from commandline arguments'''
print(sys.argv)

datapath = 'segmented'
parampath = 'segmented'

if sys.argv[2] == "sonyGan" or sys.argv[2]=="1":
    sg = sonyGanJson.SonyGanJson(datapath,"natural",22050,"O'REILLY")
    sg.write2File("sonyGan.json")

elif sys.argv[2] == "paramManager" or sys.argv[2]=="0":

    pm=paramManager.paramManager(datapath,parampath) #filebase is directory name
    pm.initParamFiles(overwrite=True) ##-----------   paramManager  interface ------------------##
    pm.checkIntegrity()

    paramList = [f for f in os.listdir(datapath) if os.path.isfile(os.path.join(parampath, os.path.splitext(f)[0] + ".params"))]
    for p in paramList:
        soundText = os.path.splitext(p)[0].split("--")
        foo=pm.getParams(datapath + '/' + p) #extension is optional
        pm.addMetaParam(parampath + '/' + p,"soundName", soundText[0])
        pm.addMetaParam(parampath + '/' + p,"segmentNum", int(soundText[len(soundText)-1].split("-")[1]))

else:
    print("IN progress, tfrecords")
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
chunkDuration = 1 if len(sys.argv) <= 1 else float(sys.argv[1]) # 1 sec
outType = 0 if len(sys.argv) <= 2 else int(sys.argv[2])
resampFreq = 22050 if len(sys.argv) <=3 else int(sys.argv[3]) # default 22050hz

outTypeString = ["Params", "SonyGan", "Tfrecords"]
print("---------------")
print("Generating files of ", chunkDuration, "seconds with outType of ", outTypeString[outType], " at ", resampFreq, " Hz")
print("---------------")

''' Chunk files into Nsecond durations'''
for fileName in fileList:

    sig,sr=librosa.core.load(datapath + "/" + fileName, sr=None)

    # resample
    sig= librosa.core.resample(sig, sr, resampFreq) 

    fileBase = os.path.splitext(fileName)[0]

    numSamplesPerChunk = int(chunkDuration*resampFreq);
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
                sf.write("segmented" + "/" + fileBase + "--" + "v-" + str(i) + ".wav", norm, resampFreq)
            else:
                print("Discarding a silent segment ", i)
            i = i + 1;
        else:
            print("Discarding a segment ", i)

'''' Generate records from commandline arguments'''
print(sys.argv)

datapath = 'segmented'
parampath = 'segmented'

if outType == "sonyGan" or outType==1:
    sg = sonyGanJson.SonyGanJson(datapath,"natural",22050,"O'REILLY")
    sg.write2File("sonyGan.json")

elif outType == "paramManager" or outType==0:

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
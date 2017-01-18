#!/usr/bin/env python2
#encoding: UTF-8
# Dieison Silveira

#aulapinroot@beagle1:~/cacti65/cfg/old/.results/

from subprocess import check_output, PIPE, STDOUT
import os
from sys import argv

videos=[]
frames=[]
width=[]
height=[]
presets = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow", "placebo"]

videoPath="~/Pesquisa/videos/1920x1080/"
pcm="/home/aulapinroot/Programs/IntelPerformanceCounterMonitor-V2.11/pcm.x"
hwCounters="L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores,L1-dcache-store-misses,LLC-stores,LLC-store-misses,LLC-loads,LLC-loads-misses"

def load_in():
	f = open('videos2.in','r')
	line = f.readline()

	while line:
		value = line.split(';')
		if value[0][0]!="#":
			videos.append(value[0])
			frames.append(value[1])
			width.append(value[2])
			height.append(value[3].rstrip())
		line = f.readline()

def encoder():
	arq = open("simulation_encoder2.txt", "w")
	i=0	
	for video in videos:
		for preset in presets:
			app = "encoder --input "+videoPath+video+".yuv --fps 50 --input-res "+width[i]+"x"+height[i]+" --frames "+frames[i]+" --preset " + preset + " --ssim --psnr --output "+videoPath+"bin/"+preset+video+".bin"
			pcmcmd="sudo -E "+pcm+" --noJKTWA -r --external-program ./"+app+" >> pcmResults/"+preset+video+".log"
			
			print pcmcmd
			outputpcm = check_output(pcmcmd, shell=True, stderr=STDOUT)
			
			perfcmd="sudo -E perf stat --output perfResults/"+preset+video+".log -e "+hwCounters+" ./"+app     
			print perfcmd
			outputperf = check_output(perfcmd, shell=True, stderr=STDOUT)
			
			# arq.write("######### "+preset+" #########")
			# arq.write("\n")
			# arq.write(output)
			# arq.write("\n\n")
	arq.close()

def decoder():
	arq = open("simulation_decoder.txt", "w")
	for video in videos:
		for preset in presets:
			cmd = "./decoder -b ~/Pesquisa/videos/1920x1080/bin/"+preset+video+".bin -o ~/Pesquisa/videos/1920x1080/reconstructed/teste/"+preset+video+".yuv"
			output = check_output(cmd, shell=True, stderr=PIPE)
			print cmd
			arq.write("######### "+preset+" #########")
			arq.write("\n")
			arq.write(output)
			arq.write("\n\n")
	arq.close()

if __name__ == "__main__":
	# main(argv[1], int(argv[2]))
	load_in()
	encoder()
	# decoder()

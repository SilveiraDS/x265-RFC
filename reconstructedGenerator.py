#!/usr/bin/env python2
#encoding: UTF-8
# Dieison Silveira

from subprocess import check_output, PIPE, STDOUT
import os
from sys import argv
import datetime

videos=[]
frames=[]
width=[]
height=[]
presets=["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow", "placebo"]
videoPath="~/Pesquisa/videos/1920x1080/"

def load_in(file):
	f = open(file,'r')
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
	file="outputSimulation/simulation_encoder"+datetime.datetime.now().strftime("%d-%m_%H_%M")+".txt"
	arq = open(file, "w")
	i=0	
	for video in videos:
		for preset in presets:
			cmd = "../x265 --input "+videoPath+video+".yuv --fps 50 --input-res "+width[i]+"x"+height[i]+" --frames "+frames[i]+" --preset " + preset + " --ssim --psnr --no-pmode --no-wpp --no-pme --output "+videoPath+"bin/"+preset+video+".bin"
			print cmd
			output = check_output(cmd, shell=True, stderr=STDOUT)
			arq.write("######### "+preset+" #########")
			arq.write("\n")
			arq.write(output)
			arq.write("\n\n")
	arq.close()

def decoder():
	file="outputSimulation/simulation_decoder"+datetime.datetime.now().strftime("%d-%m_%H_%M")+".txt"
	arq = open(file, "w")
	for video in videos:
		for preset in presets:
			cmd = "../TAppDecoderStaticd -b "+videoPath+"bin/"+preset+video+".bin -o "+videoPath+"reconstructed/"+preset+video+".yuv"
			print cmd
			output = check_output(cmd, shell=True, stderr=PIPE)
			arq.write("######### "+preset+" #########")
			arq.write("\n")
			arq.write(output)
			arq.write("\n\n")
	arq.close()

if __name__ == "__main__":
	# main(argv[1], int(argv[2]))
	load_in("videos3.in")
	encoder()
	load_in("videos2.in")
	decoder()

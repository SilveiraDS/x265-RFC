#!/usr/bin/env python2
#encoding: UTF-8
# Dieison Silveira


from subprocess import check_output, PIPE, STDOUT
import os
from sys import argv

videos=[]
frames=[]
width=[]
height=[]
presets = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow", "placebo"]
qp = "22"
videoPath="~/Pesquisa/videos/1920x1080/"
# pcm="/Programs/IntelPerformanceCounterMonitor-V2.11/pcm.x"
# hwCounters="L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores,L1-dcache-store-misses,LLC-stores,LLC-store-misses,LLC-loads,LLC-loads-misses"

def load_in():
	f = open('videos.in','r')
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
	arq = open("simulation_encoder1.txt", "w")
	i=0	
	for video in videos:
		for preset in presets:
			cmd = "./bin/x265 --input "+videoPath+"cct/"+video+".yuv --fps 50 --input-res "+width[i]+"x"+height[i]+" --frames "+frames[i]+" --qp "+qp+" --preset " + preset + " --ssim --psnr --output "+videoPath+"bin/"+qp+"_"+preset+"_"+video+".bin"
			
			print cmd
			outputcmd = check_output(cmd, shell=True, stderr=STDOUT)
			
			arq.write("######### "+preset+" #########")
			arq.write("\n")
			arq.write(outputcmd)
			arq.write("\n\n")
		i+=1
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
	qp = argv[1]
	load_in()
	encoder()
	# decoder()

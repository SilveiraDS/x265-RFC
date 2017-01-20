import os
import sys
import argparse
import datetime

videos=[]
frames=[]
fps=[]
width=[]
height=[]

# python ddrfc_simulation.py -qp 32 -ty 0 -bs 64 -ts 64 -dr

presets=["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow", "placebo"]
# presets=["fast"]
tipo_nomes=["bbc", "bbl", "bbc", "bbc"]
diretorio_videos="/home/dieison/Pesquisa/videos/1920x1080/reconstructed/"
diretorio_tabelas="/home/dieison/Pesquisa/ddrfc-bitstream/tables/"
diretorio_saida="results/"+datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")+"/"
diretorio_executavel="/home/dieison/Pesquisa/ddrfc-bitstream/"

def load_in():
	f = open('videos.in','r')
	line = f.readline()

	while line:
		value = line.split(';')
		if value[0][0]!="#":
			videos.append(value[0])
			fps.append(value[1])
			frames.append(value[2])
			width.append(value[3])
			height.append(value[4].rstrip())
		line = f.readline()

def execute(qp, tipo, block_size, table_size, fixed_codes, compress_lre, double_residue, compress_chroma, print_output, division_limit, divide_even, divide_odd, intra_block_size, division_factor, side_info_word_size, sub_blocks, table_upper_limit, table_lower_limit, optimization):
	i=0
	for video in videos:
		for preset in presets:
			command=diretorio_executavel + "bin/exec -s " + diretorio_videos+str(qp)+"_"+preset+"_rec_"+video+".yuv"
			command+=" -w " + str(width[i]) + " -h " + str(height[i]) + " -f " + str(frames[i]) + " -ty " + str(tipo) + " -bs " + str(block_size)
			command+=" -t " + diretorio_tabelas + "c_" + tipo_nomes[int(tipo)]
			if not(fixed_codes):
				command+="_" + str(block_size) + "x" + str(block_size)
			else:
				command+="_f"
			if table_size < 512:
				command+="e" + str(table_size)
			if division_limit:
				command+="_d"
				if divide_even:
					command+="e"
				if divide_odd:
					command+="o"
				command+=str(division_limit)
			if fixed_codes and optimization > 0:
				command+="_" + str(optimization)
			if double_residue:
				command+="_dr"
			command+=".txt"
			
			command+=" -ts " + str(table_size)
			command+=" -o " + diretorio_saida + "resultados_" + preset + ".csv"
			if fixed_codes:
				command+=" -fc"
				command+=" -tul " + str(table_upper_limit)
				command+=" -tll " + str(table_lower_limit)
			if compress_lre:
				command+=" -cl"
			if double_residue:
				command+=" -dr"
			if compress_chroma:
				command+=" -cc"
			if divide_even:
				command+=" -de"
			if divide_odd:
				command+=" -do"
			if division_limit:
				command+=" -dl " + str(division_limit)

			if intra_block_size:
				command+=" -ibs " + str(intra_block_size)
			if division_factor:
				command+=" -df " + str(division_factor)
			if side_info_word_size:
				command+=" -siws " + str(side_info_word_size)
			if sub_blocks:
				command+=" -sb "
	                
			if print_output:
				command+=" >> " + diretorio_saida + video + "_" + str(block_size) + "x" + str(block_size)
				if (table_size < 256 and not(double_residue)) or (table_size < 512 and double_residue):
					command+="e" + str(table_size)
				command+="qp" + str(qp) + "_" + str(tipo)
				if division_limit:
					command+="_d"
					if divide_even:
						command+="e"
					if divide_odd:
						command+="o"
					command+=str(division_limit)
				if compress_chroma:
					command+="_cc"
				if double_residue:
					command+="_dr"
				command+=".csv"
			print (command)
			os.system(command)
		i+=1

def execute_1(qp, tipos, block_sizes, table_sizes, fixed_codes, compress_lre, double_residue, compress_chroma, print_output, division_limits, divide_even, divide_odd, intra_block_size, division_factor, side_info_word_size, sub_blocks, table_upper_limit, table_lower_limit, optimization):
	for tipo in tipos:
		for block_size in block_sizes:
			for table_size in table_sizes:
				if division_limits:
					for division_limit in division_limits:
						execute(qp, tipo, block_size, table_size, fixed_codes, compress_lre, double_residue, compress_chroma, print_output, division_limit, divide_even, divide_odd, intra_block_size, division_factor, side_info_word_size, sub_blocks, table_upper_limit, table_lower_limit, optimization)
				else:
					execute(qp, tipo, block_size, table_size, fixed_codes, compress_lre, double_residue, compress_chroma, print_output, 0, divide_even, divide_odd, intra_block_size, division_factor, side_info_word_size, sub_blocks, table_upper_limit, table_lower_limit, optimization)
def main(argv):
	parser = argparse.ArgumentParser()
	
	parser.add_argument('-qp', '--qp', nargs='*', type=int, required=True)
	parser.add_argument('-ty', '--types', nargs='*', type=int, required=True)
	parser.add_argument('-bs', '--block_sizes', nargs='*', type=int, required=True)
	parser.add_argument('-ts', '--table_sizes', nargs='*', type=int, required=True)

	parser.add_argument('-dl', '--division_limits', nargs='*', type=int)
	parser.add_argument('-de', '--divide_even', action='store_true')
	parser.add_argument('-do', '--divide_odd', action='store_true')

	parser.add_argument('-fc', '--fixed_codes', action='store_true')
	parser.add_argument('-tul', '--table_upper_limit', type=int)
	parser.add_argument('-tll', '--table_lower_limit', type=int)
	parser.add_argument('-op', '--optimization', type=int)

	parser.add_argument('-cl', '--compress_lre', action='store_true')
	parser.add_argument('-dr', '--double_residue', action='store_true')
	parser.add_argument('-cc', '--compress_chroma', action='store_true')
	parser.add_argument('-po', '--print_output', action='store_true')

	parser.add_argument('-sb', '--sub_blocks', action='store_true')
	parser.add_argument('-ibs', '--intra_block_size', type=int)
	parser.add_argument('-df', '--division_factor', type=int)
	parser.add_argument('-siws', '--side_info_word_size', type=int)
	
	args = parser.parse_args()

	qps=args.qp
	divide_even=args.divide_even
	divide_odd=args.divide_odd
	division_limits=args.division_limits
	tipos=args.types
	block_sizes=args.block_sizes
	table_sizes=args.table_sizes
	fixed_codes=args.fixed_codes
	table_upper_limit=args.table_upper_limit
	table_lower_limit=args.table_lower_limit
	optimization=args.optimization
	
	compress_lre=args.compress_lre
	double_residue=args.double_residue
	compress_chroma=args.compress_chroma
	print_output=args.print_output

	sub_blocks=args.sub_blocks
	intra_block_size=args.intra_block_size
	division_factor=args.division_factor
	side_info_word_size=args.side_info_word_size

	if not os.path.exists(diretorio_saida):
		os.makedirs(diretorio_saida)
	
	load_in()

	for qp in qps:
		execute_1(qp, tipos, block_sizes, table_sizes, fixed_codes, compress_lre, double_residue, compress_chroma, print_output, division_limits, divide_even, divide_odd, intra_block_size, division_factor, side_info_word_size, sub_blocks, table_upper_limit, table_lower_limit, optimization)

# python ddrfc_simulation.py -qp 32 -ty 0 -bs 64 -ts 64 -dr
if __name__ == '__main__':
	main(sys.argv[1:])

### Adapted from HON code belonging to Xu Jian
### Demo of HON: please visit http://www.HigherOrderNetwork.com
### Latest code: please visit https://github.com/xyjprc/hon

### See details in README

import jianxu_BuildRulesFastParameterFree
import jianxu_BuildRulesFastParameterFreeFreq
import jianxu_BuildNetwork
import itertools
import csv
import sys

def fast_build_HON(MaxOrder = 99, MinSupport = 10, Input_Sequence_File = '../../Raw_data_processing_JSON_to_CSV/sequence.txt', Freq = False, out_file_add = ""):
	
	""" Initialise Algorithm Parameters / input or output filenames """
	## Default parameters if no system arguments are given:
	
	## For each path, the rule extraction process attempts to increase the order until the maximum order is reached. The default value of 5 should be sufficient for most applications. 	Setting this value as 1 will yield a conventional first-order network. Discussion of this parameter (how it influences the accuracy of representation and the size of the network) is given in the supporting information of the paper.
	MaxOrder = int(MaxOrder)
	
	## Observations that are less than min-support are discarded during preprocessing.
	## For example, if the pattern [Shanghai, Singapore] -> [Tokyo] appears 500 times and [Zhenjiang, Shanghai, Singapore] -> [Tokyo] happened only 3 times, and min-support is 10, then [Zhenjiang, Shanghai, Singapore] -> [Tokyo] will not be considered as a higher-order rule.
	MinSupport = int(MinSupport)
	
	
	InputFileName = Input_Sequence_File
	OutputRulesFile = 'rules-cell-' + str(MaxOrder) + str(out_file_add) +'.csv'
	OutputNetworkFile = 'network-cell-maxorder-'+str(MaxOrder)+ "MinSupport-"+ str(MinSupport) +str(out_file_add) +'.csv'
	
	## Try not to touch these unless you REALLY know what you're doing...
	LastStepsHoldOutForTesting = 0
	MinimumLengthForTraining = 1
	InputFileDeliminator = ' '
	Verbose = True
	
	
	###########################################
	# Functions
	###########################################
	
	def ReadSequentialData(InputFileName):
		if Verbose:
			print('Reading raw sequential data')
		RawTrajectories = []
		with open(InputFileName) as f:
			LoopCounter = 0
			for line in f:
				fields = line.strip().split(InputFileDeliminator)
				## In the context of global shipping, a ship sails among many ports
				## and generate trajectories.
				## Every line of record in the input file is in the format of:
				## [Ship1] [Port1] [Port2] [Port3]...
				ship = fields[0]
				movements = fields[1:]
				
				LoopCounter += 1
				if LoopCounter % 10000 == 0:
					VPrint(LoopCounter)
				
				## Other preprocessing or metadata processing can be added here
				
				## Test for movement length
				MinMovementLength = MinimumLengthForTraining + LastStepsHoldOutForTesting
				if len(movements) < MinMovementLength:
					continue
				
				RawTrajectories.append([ship, movements])
		return RawTrajectories
	
	
	def BuildTrainingAndTesting(RawTrajectories):
		VPrint('Building training and testing')
		Training = []
		Testing = []
		for trajectory in RawTrajectories:
			ship, movement = trajectory
			movement = [key for key,grp in itertools.groupby(movement)] # remove adjacent duplications
			if LastStepsHoldOutForTesting > 0:
				Training.append([ship, movement[:-LastStepsHoldOutForTesting]])
				Testing.append([ship, movement[-LastStepsHoldOutForTesting]])
			else:
				Training.append([ship, movement])
		return Training, Testing
	
	def DumpRules(Rules, OutputRulesFile):
		VPrint('Dumping rules to file')
		with open(OutputRulesFile, 'w') as f:
			for Source in Rules:
				for Target in Rules[Source]:
					f.write(' '.join([' '.join([str(x) for x in Source]), '=>', Target, str(Rules[Source][Target])]) + '\n')
	
	def DumpNetwork(Network, OutputNetworkFile):
		VPrint('Dumping network to file')
		LineCount = 0
		with open(OutputNetworkFile, 'w') as f:
			for source in Network:
				for target in Network[source]:
					f.write(','.join([SequenceToNode(source), SequenceToNode(target), str(Network[source][target])]) + '\n')
					LineCount += 1
		VPrint(str(LineCount) + ' lines written.')
	
	def SequenceToNode(seq):
		curr = seq[-1]
		node = curr + '|'
		seq = seq[:-1]
		while len(seq) > 0:
			curr = seq[-1]
			node = node + curr + '.'
			seq = seq[:-1]
		if node[-1] == '.':
			return node[:-1]
		else:
			return node
	
	def VPrint(string):
		if Verbose:
			print(string)
	
	
	def BuildHON(InputFileName, OutputNetworkFile):
		RawTrajectories = ReadSequentialData(InputFileName)
		TrainingTrajectory, TestingTrajectory = BuildTrainingAndTesting(RawTrajectories)
		VPrint(len(TrainingTrajectory))
		Rules = jianxu_BuildRulesFastParameterFree.ExtractRules(TrainingTrajectory, MaxOrder, MinSupport)
		# DumpRules(Rules, OutputRulesFile)
		Network = jianxu_BuildNetwork.BuildNetwork(Rules)
		DumpNetwork(Network, OutputNetworkFile)
		VPrint('Done: '+InputFileName)
	
	def BuildHONfreq(InputFileName, OutputNetworkFile):
		print('FREQ mode!!!!!!')
		RawTrajectories = ReadSequentialData(InputFileName)
		TrainingTrajectory, TestingTrajectory = BuildTrainingAndTesting(RawTrajectories)
		VPrint(len(TrainingTrajectory))
		Rules = jianxu_BuildRulesFastParameterFreeFreq.ExtractRules(TrainingTrajectory, MaxOrder, MinSupport)
		# DumpRules(Rules, OutputRulesFile)
		Network = jianxu_BuildNetwork.BuildNetwork(Rules)
		DumpNetwork(Network, OutputNetworkFile)
		VPrint('Done: '+InputFileName)
	
	###########################################
	# Main function
	###########################################
	RawTrajectories = ReadSequentialData(InputFileName)
	TrainingTrajectory, TestingTrajectory = BuildTrainingAndTesting(RawTrajectories)
	VPrint(len(TrainingTrajectory))
	if Freq == True:
		Rules = jianxu_BuildRulesFastParameterFreeFreq.ExtractRules(TrainingTrajectory, MaxOrder, MinSupport)
	else:
		Rules = jianxu_BuildRulesFastParameterFree.ExtractRules(TrainingTrajectory, MaxOrder, MinSupport)
	DumpRules(Rules, OutputRulesFile)
	Network = jianxu_BuildNetwork.BuildNetwork(Rules)
	DumpNetwork(Network, OutputNetworkFile)
	
	with open(OutputNetworkFile, newline='') as f:
		r = csv.reader(f)
		data = [line for line in r]
	with open(OutputNetworkFile, 'w',newline='') as f:
		w = csv.writer(f)
		w.writerow(['source','target','value'])
		w.writerows(data)

if len(sys.argv) == 3:
	fast_build_HON(MinSupport = sys.argv[1], MaxOrder= sys.argv[2])

elif len(sys.argv) !=3:
	print(" To creat HON from console, type: \n python3 jianxu_main minsupport maxorder \n where minsupport and maxorder are integers")

### Major update: parameter free and magnitudes faster than previous versions.
### Paper and pseudocode: https://arxiv.org/abs/1712.09658


### This package: Python implementation of the higher-order network (HON) construction algorithm.
### Paper: "Representing higher-order dependencies in networks"
### Code written by Jian Xu, Apr 2017

### Technical questions? Please contact i[at]jianxu[dot]net
### Demo of HON: please visit http://www.HigherOrderNetwork.com
### Latest code: please visit https://github.com/xyjprc/hon

### See details in README

import jianxu_BuildRulesFastParameterFree
import jianxu_BuildRulesFastParameterFreeFreq
import jianxu_BuildNetwork
import itertools

""" Initialise Algorithm Parameters / input or output filenames """
## Default parameters if no system arguments are given:

## For each path, the rule extraction process attempts to increase the order until the maximum order is reached. The default value of 5 should be sufficient for most applications. Setting this value as 1 will yield a conventional first-order network. Discussion of this parameter (how it influences the accuracy of representation and the size of the network) is given in the supporting information of the paper.
MaxOrder = 1

## Observations that are less than min-support are discarded during preprocessing.
## For example, if the patter [Shanghai, Singapore] -> [Tokyo] appears 500 times and [Zhenjiang, Shanghai, Singapore] -> [Tokyo] happened only 3 times, and min-support is 10, then [Zhenjiang, Shanghai, Singapore] -> [Tokyo] will not be considered as a higher-order rule.
MinSupport = 10


## Initialize user parameters
InputFileName = '../../Raw_data_processing_JSON_to_CSV/sequence.txt'
OutputRulesFile = 'rules-cell.csv'
OutputNetworkFile = 'network-cell-1storder-weights.csv'

## Vary the output to either frequency type weights (True) or values between 0-1 (False).
Freq = False

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

if __name__ == "__main__":
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

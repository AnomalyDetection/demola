#! /usr/bin/python
'''
Relation Probability algorithm
'''
import conf
import data_set

trainSet = data_set.getDataSet( conf.trainFile )
detectSet = data_set.getDataSet( conf.detectFile )

countDict = {}

# TRAIN PHASE
for line in trainSet:
	key = ''
	for featureIdx in conf.featureSet:
		key += line[featureIdx]

	if key in countDict:
		countDict[key] += 1
	else:
		countDict[key] = 1

print len( countDict ), ' unique keys'
#for item in countDict:
#	print item, countDict[item]

# DETECT PHASE
i = 0
for line in detectSet:
	if i == 30:
		print '---------------above should be 0 all--------------'
		print '---------------below should be positive all--------------'
	key = ''
	for featureIdx in conf.featureSet:
		key += line[featureIdx]

	if key in countDict:
		print countDict[key]
	else:
		print '0'
	i += 1

#done



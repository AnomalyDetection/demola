import conf
#! /usr/bin/python
'''
handle data_set
'''
def getDataSet( filename ):
	dataSet = []
	fd = file( filename, 'r' )
	
	while True:
		line = fd.readline().strip()
		if len(line) == 0:
			break	#EOF of file

		arr = line.split()
		dataSet.append( arr )

	fd.close()

	return dataSet

# unit test: getDataSet
#dataSet = getDataSet()
#print len(dataSet)
#for item in dataSet:
#	print item

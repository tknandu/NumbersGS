import itertools
import numpy as np 
import sys
import math
import copy

def delta(symbol, field, k):
	points = []
	try:
		symbolDict = tickDict[symbol]
	except KeyError:
		return 0
	for time in symbolDict.keys():
		try:
			for val in symbolDict[time][field]:
				points.append((time,val))
		except KeyError:
			c = 3
	points = sorted(points)

	# linear regression
	def findError(i,j):
					
		x = map(lambda x:x[0], points[i:(j+1)])
		y = map(lambda x:x[1], points[i:(j+1)])
		p = np.poly1d(np.polyfit(x, y, 1))
		z = map(lambda x: p(x), x)
		e = sum(map(lambda x,y: (x-y)**2,y,z))
		return e

	error = np.zeros((len(points), len(points)))
	M = np.zeros(len(points))
	def getM(i):
		if i==-1:
			return 0
		else:
			return M[i]

	def compute(points, j):
		# compute error & M for j
		for i in xrange(j):
			error[i,j] = findError(i,j)	
		error[j,j]=0
		minVal = sys.float_info.max
		for i in xrange(j+1):
			x = error[i,j] + k + getM(i-1) 
			if x < minVal:
				minVal = x
		return minVal

	for j in xrange(len(points)):
		M[j] = compute(points,j)
		try:
			if points[j][0]==points[j+1][0]:
				temp = points[j]
				points[j] = points[j+1]
				points[j+1] = points[j]
			newMin = compute(points, j)
			if newMin < M[j]:
				M[j] = newMin
			else:
				temp = points[j]
				points[j] = points[j+1]
				points[j+1] = points[j]
				M[j]=compute(points,j)
		except IndexError:
			c = 3
			

	return int(math.ceil(M[len(points)-1]))

def mysum(start, end, symbol, field):
	val = 0
	try:
		symbolDict = tickDict[symbol]
	except KeyError:
		return 0
	for time in symbolDict.keys():
		if time>=start and time<=end:
			try:
				val = val + sum(symbolDict[time][field])
			except KeyError:
				val = val + 0
	return val

def product(start, end, symbol, field1, field2):
	val = 0
	try:
		symbolDict = tickDict[symbol]
	except KeyError:
		return 0
	for time in symbolDict.keys():
		if time>=start and time<=end:
			try:
				val = val + sum(map(lambda x,y:x*y,symbolDict[time][field1],symbolDict[time][field2]))
			except KeyError:
				val = val + 0
	return val	


def mymax(start, end, symbol, field, k):
	array = []
	try:
		symbolDict = tickDict[symbol]
	except KeyError:
		return 0
	for time in symbolDict.keys():
		if time>=start and time<=end:
			try:
				array.extend(symbolDict[time][field])
			except KeyError:
				c = 3
	if len(array)<k:
		return reversed(sorted(array))
	else:
		return list(reversed(sorted(array)))[:k]

n = int(raw_input().split()[1])
tickDict = {}
# symbol: {timestamp: {fieldName: fieldValue}}
for i in xrange(n):
	line = raw_input().split()
	if not line[1] in tickDict.keys():
		tickDict[line[1]] = {int(line[0]): {}}
	else:
		if int(line[0]) not in tickDict[line[1]].keys(): # timestamp not present in dict of symbol
			tickDict[line[1]][int(line[0])] = {}
	j = 2
	while j < len(line): 
		if not line[j] in tickDict[line[1]][int(line[0])]:
			tickDict[line[1]][int(line[0])][line[j]] = [int(line[j+1])]
		else:
			tickDict[line[1]][int(line[0])][line[j]].append(int(line[j+1]))
		j = j+2

print 'tickfile completed'

while True:
	try:
		line = raw_input().split()
		if line[0]=='sum':
			print mysum(int(line[1]), int(line[2]), line[3], line[4])
		elif line[0]=='max':
			print " ".join(map(str,mymax(int(line[1]), int(line[2]), line[3], line[4], int(line[5]))))
		elif line[0]=='product':
			print product(int(line[1]), int(line[2]), line[3], line[4], line[5])	
		elif line[0]=='delta':
			print delta(line[1], line[2], int(line[3]))		
	except EOFError:
		break
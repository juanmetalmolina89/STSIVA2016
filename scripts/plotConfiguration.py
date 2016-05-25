#
import csv
import matplotlib
import matplotlib.pyplot as plt
import turtle
import math
import os
import numpy

def loadFiles(fname):
	
	if "LC8" in fname:
		print fname
	
		limitador = 7
	else:
		print fname

		limitador = 6
	with open(fname) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		included_cols = range(14)
		headers = reader.next()
		column = {}
		for h in headers:
			column[h] = []
		content = {}
		len(reader)
		for row in reader:
			for h, v in zip(headers, row):
				column[h].append(v)
		row_count = len(column['band'])
		intervale = row_count / limitador
		for i in range(intervale):
			init = i * limitador
			ending = (i + 1) * limitador	
			x = column['band'][init:ending]
			y = column[ 'ResultsRADMin'][init:ending]
			y1 = column[ 'ResultsRADMax'][init:ending]
			y2 = column[ 'ResultsRADMean'][init:ending]
	#		y3 = column[ 'ResultsTOAMin'][init:ending]
	#		y4 = column[ 'ResultsTOAMax'][init:ending]
	#		y5 = column[ 'ResultsTOAMean'][init:ending]
		
	#		content = list(row[i] for i in included_cols)
	#		y = content[8:14];
	#		plt.Figure()					
			corr_line, = plt.plot(x,y,'r')
			corr_line1, = plt.plot(x,y1,'g')
			corr_line2, = plt.plot(x,y2,'b')
	#		plt.plot(x,y3,'c')
	#		plt.plot(x,y4,'k')
	#		plt.plot(x,y5,'b')
			plt.ylabel('Reflectance Level')
			plt.xlabel('Bands')
			name = abspath + os.sep + basename + '-' + column['atmoProfile'][init] + '-' + column['aeroProfile'][init]+ '_' + column['GroundReflectance'][init] + '-' + column['AOT'][init] + '.png'
			#print name
			plt.savefig(name)
			corr_line.remove()
			corr_line1.remove()
			corr_line2.remove()	
			
			#plt.show()

		   	
		
def createImages(fname):
	if "LC8" in fnames:
		print fnames

		limitador = 7
		print limitador	
	else:
		print fnames

		limitador = 6
		print limitador
	with open(fnames) as csvfile:
		path = fnames[:-30]

		os.mkdir( path, 0755 );
		basename = os.path.basename(path)
		abspath = os.path.abspath(path)
		dirname = os.path.dirname(path)
		reader = csv.reader(csvfile, delimiter=',')
		included_cols = range(14)
		headers = reader.next()
		column = {}
		for h in headers:
			column[h] = []
		content = {}
		il = 0;
		x =  range(limitador)
		for row in reader:
			for h, v in zip(headers, row):
				column[h].append(v)
		row_count = len(column['band'])
		intervale = row_count / limitador
		for i in range(intervale):
			init = i * limitador
			ending = (i + 1) * limitador	
			x = column['band'][init:ending]
			y = column[ 'ResultsRADMin'][init:ending]
			y1 = column[ 'ResultsRADMax'][init:ending]
			y2 = column[ 'ResultsRADMean'][init:ending]
	#		y3 = column[ 'ResultsTOAMin'][init:ending]
	#		y4 = column[ 'ResultsTOAMax'][init:ending]
	#		y5 = column[ 'ResultsTOAMean'][init:ending]
			
	#		content = list(row[i] for i in included_cols)
	#		y = content[8:14];
	#		plt.Figure()					
			corr_line, = plt.plot(x,y,'r')
			corr_line1, = plt.plot(x,y1,'g')
			corr_line2, = plt.plot(x,y2,'b')
	#		plt.plot(x,y3,'c')
	#		plt.plot(x,y4,'k')
	#		plt.plot(x,y5,'b')
			plt.ylabel('Reflectance Level')
			plt.xlabel('Bands')
			name = abspath + os.sep + basename + '-' + column['atmoProfile'][init] + '-' + column['aeroProfile'][init]+ '_' + column['GroundReflectance'][init] + '-' + column['AOT'][init] + '.png'
			#print name
			plt.savefig(name)
			corr_line.remove()
			corr_line1.remove()
			corr_line2.remove()	
    # plt.show()

def createImagesLOAD(fname):
	if "LC8" in fnames:
		print fnames

		limitador = 7
		print limitador	
	else:
		print fnames

		limitador = 6
		print limitador
	with open(fnames) as csvfile:
		path = fnames[:-26]

		os.mkdir( path, 0755 );
		basename = os.path.basename(path)
		abspath = os.path.abspath(path)
		dirname = os.path.dirname(path)
		reader = csv.reader(csvfile, delimiter=',')
		included_cols = range(14)
		headers = reader.next()
		column = {}
		for h in headers:
			column[h] = []
		content = {}
		il = 0;
		x =  range(limitador)
		for row in reader:
			for h, v in zip(headers, row):
				column[h].append(v)
		row_count = len(column['band'])
		intervale = row_count / limitador
		for i in range(intervale):
			init = i * limitador
			ending = (i + 1) * limitador	
			x = column['band'][init:ending]
			y = column['MeanSRRAD'][init:ending]
			y1 = column['MaxSRRAD'][init:ending]
			y2 = column['MinSRRAD'][init:ending]
	#		y3 = column[ 'ResultsTOAMin'][init:ending]
	#		y4 = column[ 'ResultsTOAMax'][init:ending]
	#		y5 = column[ 'ResultsTOAMean'][init:ending]
			
	#		content = list(row[i] for i in included_cols)
	#		y = content[8:14];
	#		plt.Figure()					
			corr_line, = plt.plot(x,y,'r')
			corr_line1, = plt.plot(x,y1,'g')
			corr_line2, = plt.plot(x,y2,'b')
	#		plt.plot(x,y3,'c')
	#		plt.plot(x,y4,'k')
	#		plt.plot(x,y5,'b')
			plt.ylabel('Reflectance Level')
			plt.xlabel('Bands')
			name = abspath + os.sep + basename + '-' + column['atmoProfile'][init] + '-' + column['aeroProfile'][init]+ '_' + column['GroundReflectance'][init] + '-' + column['AOT'][init] + '.png'
			#print name
			plt.savefig(name)
			corr_line.remove()
			corr_line1.remove()
			corr_line2.remove()	
    # plt.show()
			
rootDir = '.'
for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
	#print('Found directory: %s' % dirName)
	if dirName == './Parameters': 	    
		for fname in fileList:
#			loadFiles(dirName+os.sep+fname)
			fnames = dirName+os.sep+fname
			#createImages(fnames)
	if dirName == './data': 	    
		for fname in fileList:
#			loadFiles(dirName+os.sep+fname)
			fnames = dirName+os.sep+fname
			createImagesLOAD(fnames)
					
					

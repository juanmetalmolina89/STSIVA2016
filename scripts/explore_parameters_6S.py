from Py6S import *
import arcsi
# Import the datetime module
import datetime
# Import the GDAL/OGR spatial reference library
from osgeo import osr
from osgeo import ogr
from osgeo import gdal
# Import OS path module for manipulating the file system 
import os.path
# Import the RSGISLib Image Calibration Module.
import rsgislib.imagecalibration
# Import the collections module
import collections
# Import the py6s module for running 6S from python.
import Py6S
# Import the python maths library
import math
# Import the RIOS RAT library
from rios import rat
# Import the GDAL python library
import osgeo.gdal as gdal
# Import the scipy optimisation library - used for finding AOD values form the imagery.
from scipy.optimize import minimize
# Import the numpy module
import numpy
# Import the glob module
import glob
#
import csv
#
import argparse
import sys
##
def statisticsImage(fileName):
	src_ds = gdal.Open( fileName )
	if src_ds is None:
	    print 'Unable to open INPUT.tif'
	    sys.exit(1)

	print "[ RASTER BAND COUNT ]: ", src_ds.RasterCount
	statss = list()
	for band in range( src_ds.RasterCount ):
	    band += 1
	    print "[ GETTING BAND ]: ", band
	    srcband = src_ds.GetRasterBand(band)
	    if srcband is None:
		continue

	    stats = srcband.GetStatistics( True, True )
	    if stats is None:
		continue
	    statss.append(stats)	
	    print "[ STATS ] =  Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % ( \
		        stats[0], stats[1], stats[2], stats[3] )
	return statss
def executionParameters6SusingARCSIls8(inputHeader,sensor,radianceImage,TOAImage,outpath):
	#inputHeader = '/home/juanmolina/Documents/6s/LE70080592013246EDC00/LE70080592013246EDC00_MTL.txt';
	wktStr = None
	#sensor = 'ls7'
	imagefile = None
	debug  = False
	#outNameRad = 'LE70080592013246EDC00_rad.kea'
	#outNameTOA = 'LE70080592013246EDC00_toa.kea'
	#outThermName = 'LE70080592013246EDC00_therm.kea'
	#outSRFName = 'LE70080592013246EDC00_srf'
	ARCSIClass = arcsi.ARCSI()
	sensorClass = ARCSIClass.sensorClassFactory(sensor,debug,imagefile)
	sensorClass.extractHeaderParameters(inputHeader, wktStr)
	outFormat = 'KEA'
	#outFilePath = '/home/juanmolina/Documents/6s/LE70080592013246EDC00/'
	statRAD = statisticsImage(radianceImage)
	statTOA = statisticsImage(TOAImage)
	#radianceImage, thermalRadImage = sensorClass.convertImageToRadiance(outFilePath, outNameRad, outThermName, outFormat)
	#TOAImage = sensorClass.convertImageToTOARefl(radianceImage,outFilePath, outNameTOA,outFormat)
	surfaceAltitude = float(0)
	useBRDF =  False
	Band6S = collections.namedtuple('Band6SCoeff', ['band', 'aX', 'bX', 'cX'])
	cont = 0
	with open(outpath+'/testAtmosphericparameters.csv', 'wb') as csvfile:
	    	fieldnames = ['atmoProfile', 'aeroProfile','GroundReflectance','AOT','band','aX', 'bX', 'cX','ResultsRADMin','ResultsRADMax','ResultsRADMean','ResultsTOAMin','ResultsTOAMax','ResultsTOAMean','MeanRAD','MaxRAD','MinRAD','StdRAD','MeanTOA','MaxTOA','MinTOA','StdTOA']
	    	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	    	writer.writeheader()

		for paramAtmProfile in [AtmosProfile.Tropical, AtmosProfile.MidlatitudeSummer, AtmosProfile.MidlatitudeWinter, AtmosProfile.SubarcticSummer,AtmosProfile.SubarcticWinter, AtmosProfile.NoGaseousAbsorption]:
			print('Perfiles atmosfericos')	
			print(paramAtmProfile)
			print('-------------------------------------------------------')
			for paramAeroProfile in [AeroProfile.NoAerosols, AeroProfile.Continental,AeroProfile.Maritime,AeroProfile.Urban,AeroProfile.Desert,AeroProfile.BiomassBurning,AeroProfile.Stratospheric]:
				print('Perfiles de Aerosoles')		
				print(paramAeroProfile)
				print('-------------------------------------------------------')
				for paramGroundReflect in [GroundReflectance.GreenVegetation, GroundReflectance.ClearWater, GroundReflectance.Sand,GroundReflectance.LakeWater]:
						print('Reflectancia de Suelo')	
						print(paramGroundReflect)
						print('-------------------------------------------------------')
						for aotvalue in numpy.linspace(0,1,11):
							print('AOT')	
							print(aotvalue)
							print('-------------------------------------------------------')
							#outputImage = os.path.join(outpath, outSRFName+'-'+str(paramAtmProfile)+'-'+str(paramAeroProfile)+'-'+str(paramGroundReflect)+'-'+str(aotvalue)+'.kea')

							imgBandCoeffs = list()
							sixsCoeffs = sensorClass.calc6SCoefficients(paramAeroProfile,paramAtmProfile, Py6S.GroundReflectance.HomogeneousLambertian(paramGroundReflect), surfaceAltitude, aotvalue, False)


							imgBandCoeffs.append(Band6S(band=1, aX=float(sixsCoeffs[0,0]), bX=float(sixsCoeffs[0,1]), cX=float(sixsCoeffs[0,2])))
							imgBandCoeffs.append(Band6S(band=2, aX=float(sixsCoeffs[1,0]), bX=float(sixsCoeffs[1,1]), cX=float(sixsCoeffs[1,2])))
							imgBandCoeffs.append(Band6S(band=3, aX=float(sixsCoeffs[2,0]), bX=float(sixsCoeffs[2,1]), cX=float(sixsCoeffs[2,2])))
							imgBandCoeffs.append(Band6S(band=4, aX=float(sixsCoeffs[3,0]), bX=float(sixsCoeffs[3,1]), cX=float(sixsCoeffs[3,2])))
							imgBandCoeffs.append(Band6S(band=5, aX=float(sixsCoeffs[4,0]), bX=float(sixsCoeffs[4,1]), cX=float(sixsCoeffs[4,2])))
							imgBandCoeffs.append(Band6S(band=6, aX=float(sixsCoeffs[5,0]), bX=float(sixsCoeffs[5,1]), cX=float(sixsCoeffs[5,2])))
							imgBandCoeffs.append(Band6S(band=7, aX=float(sixsCoeffs[6,0]), bX=float(sixsCoeffs[6,1]), cX=float(sixsCoeffs[6,2])))
		
							for band in imgBandCoeffs:
							    ymin = ((band.aX * statRAD[band.band - 1][0]) - band.bX)
							    bias = band.cX * ymin	
							    resultsRadMin = ymin/(1 + bias)
						            ymax = ((band.aX * statRAD[band.band - 1][1]) - band.bX)
							    bias = band.cX * ymax 	
							    resultsRadMax = ymax/(1 + bias)
							    ymean = ((band.aX * statRAD[band.band - 1][2]) - band.bX)
							    bias = band.cX * ymean			 
							    resultsRadMean = ymean/(1 + bias)
							    ymin = ((band.aX * statTOA[band.band - 1][0]) - band.bX)
							    bias = band.cX * ymin			
							    resultsToaMin = ymin/(1 + bias)
						            ymax = ((band.aX * statTOA[band.band - 1][1]) - band.bX)
							    bias = band.cX * ymax    	
							    resultsToaMax = ymax/(1 + bias)
							    ymean = ((band.aX * statTOA[band.band - 1][2]) - band.bX)
							    bias = band.cX * ymean	 
							    resultsToaMean = ymean/(1 + bias)     	
							    writer.writerow({'atmoProfile': str(paramAtmProfile), 'aeroProfile': str(paramAeroProfile),'GroundReflectance':str(paramGroundReflect),'AOT':str(aotvalue),'band':str(band.band),'aX':str(band.aX),'bX':str(band.bX),'cX':str(band.cX),'ResultsRADMin':str(resultsRadMin),'ResultsRADMax':str(resultsRadMax),'ResultsRADMean':str(resultsRadMean),'ResultsTOAMin':str(resultsToaMin),'ResultsTOAMax':str(resultsToaMax),'ResultsTOAMean':str(resultsToaMean),'MeanRAD':str(statRAD[band.band - 1][2]),'MinRAD':str(statRAD[band.band - 1][0]),'MaxRAD':str(statRAD[band.band - 1][1]),'StdRAD':str(statRAD[band.band - 1][3]),'MeanTOA':str(statTOA[band.band - 1][2]),'MinTOA':str(statTOA[band.band - 1][0]),'MaxTOA':str(statTOA[band.band - 1][1]),'StdTOA':str(statTOA[band.band - 1][3])})
							    print(band)	
							#rsgislib.imagecalibration.apply6SCoeffSingleParam(radianceImage, outputImage, outFormat, rsgislib.TYPE_16UINT, 1000, 0, True, imgBandCoeffs)
							#print(outputImage)
						
							cont = cont + 1

		print(cont)

##
def executionParameters6SusingARCSI(inputHeader,sensor,radianceImage,TOAImage,outpath):
	#inputHeader = '/home/juanmolina/Documents/6s/LE70080592013246EDC00/LE70080592013246EDC00_MTL.txt';
	wktStr = None
	#sensor = 'ls7'
	imagefile = None
	debug  = False
	#outNameRad = 'LE70080592013246EDC00_rad.kea'
	#outNameTOA = 'LE70080592013246EDC00_toa.kea'
	#outThermName = 'LE70080592013246EDC00_therm.kea'
	#outSRFName = 'LE70080592013246EDC00_srf'
	ARCSIClass = arcsi.ARCSI()
	sensorClass = ARCSIClass.sensorClassFactory(sensor,debug,imagefile)
	sensorClass.extractHeaderParameters(inputHeader, wktStr)
	outFormat = 'KEA'
	#outFilePath = '/home/juanmolina/Documents/6s/LE70080592013246EDC00/'
	statRAD = statisticsImage(radianceImage)
	statTOA = statisticsImage(TOAImage)
	#radianceImage, thermalRadImage = sensorClass.convertImageToRadiance(outFilePath, outNameRad, outThermName, outFormat)
	#TOAImage = sensorClass.convertImageToTOARefl(radianceImage,outFilePath, outNameTOA,outFormat)
	surfaceAltitude = float(0)
	useBRDF =  False
	Band6S = collections.namedtuple('Band6SCoeff', ['band', 'aX', 'bX', 'cX'])
	cont = 0
	with open(outpath+'/testAtmosphericparameters.csv', 'wb') as csvfile:
	    	fieldnames = ['atmoProfile', 'aeroProfile','GroundReflectance','AOT','band','aX', 'bX', 'cX','ResultsRADMin','ResultsRADMax','ResultsRADMean','ResultsTOAMin','ResultsTOAMax','ResultsTOAMean','MeanRAD','MaxRAD','MinRAD','StdRAD','MeanTOA','MaxTOA','MinTOA','StdTOA']
	    	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	    	writer.writeheader()

		for paramAtmProfile in [AtmosProfile.Tropical, AtmosProfile.MidlatitudeSummer, AtmosProfile.MidlatitudeWinter, AtmosProfile.SubarcticSummer,AtmosProfile.SubarcticWinter, AtmosProfile.NoGaseousAbsorption]:
			print('Perfiles atmosfericos')	
			print(paramAtmProfile)
			print('-------------------------------------------------------')
			for paramAeroProfile in [AeroProfile.NoAerosols, AeroProfile.Continental,AeroProfile.Maritime,AeroProfile.Urban,AeroProfile.Desert,AeroProfile.BiomassBurning,AeroProfile.Stratospheric]:
				print('Perfiles de Aerosoles')		
				print(paramAeroProfile)
				print('-------------------------------------------------------')
				for paramGroundReflect in [GroundReflectance.GreenVegetation, GroundReflectance.ClearWater, GroundReflectance.Sand,GroundReflectance.LakeWater]:
						print('Reflectancia de Suelo')	
						print(paramGroundReflect)
						print('-------------------------------------------------------')
						for aotvalue in numpy.linspace(0,1,11):
							print('AOT')	
							print(aotvalue)
							print('-------------------------------------------------------')
							#outputImage = os.path.join(outpath, outSRFName+'-'+str(paramAtmProfile)+'-'+str(paramAeroProfile)+'-'+str(paramGroundReflect)+'-'+str(aotvalue)+'.kea')

							imgBandCoeffs = list()
							sixsCoeffs = sensorClass.calc6SCoefficients(paramAeroProfile,paramAtmProfile, Py6S.GroundReflectance.HomogeneousLambertian(paramGroundReflect), surfaceAltitude, aotvalue, False)


							imgBandCoeffs.append(Band6S(band=1, aX=float(sixsCoeffs[0,0]), bX=float(sixsCoeffs[0,1]), cX=float(sixsCoeffs[0,2])))
							imgBandCoeffs.append(Band6S(band=2, aX=float(sixsCoeffs[1,0]), bX=float(sixsCoeffs[1,1]), cX=float(sixsCoeffs[1,2])))
							imgBandCoeffs.append(Band6S(band=3, aX=float(sixsCoeffs[2,0]), bX=float(sixsCoeffs[2,1]), cX=float(sixsCoeffs[2,2])))
							imgBandCoeffs.append(Band6S(band=4, aX=float(sixsCoeffs[3,0]), bX=float(sixsCoeffs[3,1]), cX=float(sixsCoeffs[3,2])))
							imgBandCoeffs.append(Band6S(band=5, aX=float(sixsCoeffs[4,0]), bX=float(sixsCoeffs[4,1]), cX=float(sixsCoeffs[4,2])))
							imgBandCoeffs.append(Band6S(band=6, aX=float(sixsCoeffs[5,0]), bX=float(sixsCoeffs[5,1]), cX=float(sixsCoeffs[5,2])))
					#		imgBandCoeffs.append(Band6S(band=7, aX=float(sixsCoeffs[6,0]), bX=float(sixsCoeffs[6,1]), cX=float(sixsCoeffs[6,2])))
		
							for band in imgBandCoeffs:
    							    ymin = ((band.aX * statRAD[band.band - 1][0]) - band.bX)
							    bias = band.cX * ymin
							    resultsRadMin = ymin/(1 + bias)
						            ymax = ((band.aX * statRAD[band.band - 1][1]) - band.bX)
							    bias = band.cX * ymax 	
							    resultsRadMax = ymax/(1 + bias)
							    ymean = ((band.aX * statRAD[band.band - 1][2]) - band.bX)
							    bias = band.cX * ymean			 
							    resultsRadMean = ymean/(1 + bias)
							    ymin = ((band.aX * statTOA[band.band - 1][0]) - band.bX)
							    bias = band.cX * ymin			
							    resultsToaMin = ymin/(1 + bias)
						            ymax = ((band.aX * statTOA[band.band - 1][1]) - band.bX)
							    bias = band.cX * ymax    	
							    resultsToaMax = ymax/(1 + bias)
							    ymean = ((band.aX * statTOA[band.band - 1][2]) - band.bX)
							    bias = band.cX * ymean	 
							    resultsToaMean = ymean/(1 + bias)     	
							    writer.writerow({'atmoProfile': str(paramAtmProfile), 'aeroProfile': str(paramAeroProfile),'GroundReflectance':str(paramGroundReflect),'AOT':str(aotvalue),'band':str(band.band),'aX':str(band.aX),'bX':str(band.bX),'cX':str(band.cX),'ResultsRADMin':str(resultsRadMin),'ResultsRADMax':str(resultsRadMax),'ResultsRADMean':str(resultsRadMean),'ResultsTOAMin':str(resultsToaMin),'ResultsTOAMax':str(resultsToaMax),'ResultsTOAMean':str(resultsToaMean),'MeanRAD':str(statRAD[band.band - 1][2]),'MinRAD':str(statRAD[band.band - 1][0]),'MaxRAD':str(statRAD[band.band - 1][1]),'StdRAD':str(statRAD[band.band - 1][3]),'MeanTOA':str(statTOA[band.band - 1][2]),'MinTOA':str(statTOA[band.band - 1][0]),'MaxTOA':str(statTOA[band.band - 1][1]),'StdTOA':str(statTOA[band.band - 1][3])})
							    print(band)	
							#rsgislib.imagecalibration.apply6SCoeffSingleParam(radianceImage, outputImage, outFormat, rsgislib.TYPE_16UINT, 1000, 0, True, imgBandCoeffs)
							#print(outputImage)
						
							cont = cont + 1

		print(cont)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='Calculate the differents configuration of model 6S in diferents images.')
	parser.add_argument('--mtl', required=True,
		                help='The full file path to the Landsat MTL file.')
	parser.add_argument('--sensor', required=True,
		                help='The sensor of the images')
	parser.add_argument('--outpath', required=True,
		                help='The number of pixels to be dilated for the cloud mask. Default is 3.')
	parser.add_argument('--radimage', required=True,
		                help='The Image in value Radiance.')
	parser.add_argument('--toaimage', required=True,
		                help='The Image in value Top of Atmosphere reflectance')
	parsed_args = parser.parse_args()
	mtl = parsed_args.mtl
	sensor = parsed_args.sensor
	outpath = parsed_args.outpath
	radImage = parsed_args.radimage
	TOAImage = parsed_args.toaimage
	if sensor == "ls8":
		executionParameters6SusingARCSIls8(mtl,sensor,radImage,TOAImage,outpath)	
	else:
		executionParameters6SusingARCSI(mtl,sensor,radImage,TOAImage,outpath)	
	


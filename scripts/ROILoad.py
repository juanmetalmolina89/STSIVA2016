import rsgislib
from rsgislib import imagecalc
from rsgislib.imagecalc import BandDefn
import subprocess

# 1) Create mask
#inImage = 'LT40080581989356-SC20160404232022/LT40080581989356XXX02_rad.kea'
#outMask = '1989_356_cut_mask.tif'
#outMask 
#gdalFormat = 'GTiff'
#dataType = rsgislib.TYPE_8UINT
#expression = 'b1 > 0?1:0' # Only include values greater than zero.
#bandDefns = []
#bandDefns.append(BandDefn('b1', inImage, 1)) # Use band one (variable b1) of in image
#imagecalc.bandMath(inImage, expression, gdalFormat, dataType, bandDefns)

# 2) Generate polygon from mask
subprocess.call("gdal_polygonize.py -mask mask/1989_356_cut_mask.tif mask/1989_356_cut_mask.tif -b 1 -f 'ESRI Shapefile' shp/LT40080581989356XXX02_mask.shp",shell=True)
subprocess.call("gdalwarp -cutline shp/LT40080581989356XXX02_mask.shp -crop_to_cutline LT40080581989356-SC20160404232022/LT40080581989356XXX02_rad.kea ROI-T/rad/LT40080581989356XXX02_rad.kea",shell=True)
subprocess.call("gdalwarp -cutline shp/LT40080581989356XXX02_mask.shp -crop_to_cutline LT40080581989356-SC20160404232022/LT40080581989356XXX02_rad_toa.kea ROI-T/toa/LT40080581989356XXX02_toa.kea",shell=True)
subprocess.call("gdalwarp -cutline shp/LT40080581989356XXX02_mask.shp -crop_to_cutline LT40080581989356-SC20160404232022/LT40080581989356XXX02_sr_stack.kea ROI-T/sr/LT40080581989356XXX02_sr.kea",shell=True)
subprocess.call("gdalwarp -cutline shp/LT40080581989356XXX02_mask.shp -crop_to_cutline LT40080581989356-SC20160404232022/LT40080581989356XXX02_stack.kea ROI-T/stack/LT40080581989356XXX02_stack.kea",shell=True)


#subprocess.call("gdal_polygonize.py -mask mask/2001_005_cut_mask.tif mask/2001_005_cut_mask.tif -b 1 -f 'ESRI Shapefile' shp/LE70080582001005AGS00_mask.shp",shell=True)
#subprocess.call("gdalwarp -cutline shp/LE70080582001005AGS00_mask.shp -crop_to_cutline LE70080582001005-SC20160404233459/LE70080582001005AGS00_rad.kea ROI-T/rad/LE70080582001005AGS00_rad.kea",shell=True)
#subprocess.call("gdalwarp -cutline shp/LE70080582001005AGS00_mask.shp -crop_to_cutline LE70080582001005-SC20160404233459/LE70080582001005AGS00_rad_toa.kea ROI-T/toa/LE70080582001005AGS00_toa.kea",shell=True)
#subprocess.call("gdalwarp -cutline shp/LE70080582001005AGS00_mask.shp -crop_to_cutline LE70080582001005-SC20160404233459/LE70080582001005AGS00_sr_stack.kea ROI-T/sr/LE70080582001005AGS00_sr.kea",shell=True)
#subprocess.call("gdalwarp -cutline shp/LE70080582001005AGS00_mask.shp -crop_to_cutline LE70080582001005-SC20160404233459/LE70080582001005AGS00_stack.kea ROI-T/stack/LE70080582001005AGS00_stack.kea",shell=True)

#subprocess.call("gdal_polygonize.py -mask mask/2015_052_cut_mask.tif mask/2015_052_cut_mask.tif -b 1 -f 'ESRI Shapefile' shp/LC80080582015052LGN00_mask.shp",shell=True)
#subprocess.call("gdalwarp -cutline shp/LC80080582015052LGN00_mask.shp -crop_to_cutline LC80080582015052-SC20160405003221/LC80080582015052LGN00_rad.kea ROI-T/rad/LC80080582015052LGN00_rad.kea",shell=True)
#subprocess.call("gdalwarp -cutline shp/LC80080582015052LGN00_mask.shp -crop_to_cutline LC80080582015052-SC20160405003221/LC80080582015052LGN00_rad_toa.kea ROI-T/toa/LC80080582015052LGN00_toa.kea",shell=True)
#subprocess.call("gdalwarp -cutline shp/LC80080582015052LGN00_mask.shp -crop_to_cutline LC80080582015052-SC20160405003221/LC80080582015052LGN00_sr_stack.kea ROI-T/sr/LC80080582015052LGN00_sr.kea",shell=True)
#subprocess.call("gdalwarp -cutline shp/LC80080582015052LGN00_mask.shp -crop_to_cutline LC80080582015052-SC20160405003221/LC80080582015052LGN00_stack.kea ROI-T/stack/LC80080582015052LGN00_stack.kea",shell=True)

#subprocess.call("gdal_polygonize.py -mask mask/2015_052_cut_b_mask.tif mask/2015_052_cut_b_mask.tif -b 1 -f 'ESRI Shapefile' shp/LC80080582015052LGN00_mask_b.shp",shell=True)
#subprocess.call("gdalwarp -cutline shp/LC80080582015052LGN00_mask_b.shp -crop_to_cutline LC80080582015052-SC20160405003221/LC80080582015052LGN00_rad.kea ROI-T/rad/LC80080582015052LGN00_b_rad.kea",shell=True)
#subprocess.call("gdalwarp -cutline shp/LC80080582015052LGN00_mask_b.shp -crop_to_cutline LC80080582015052-SC20160405003221/LC80080582015052LGN00_rad_toa.kea ROI-T/toa/LC80080582015052LGN00_b_toa.kea",shell=True)
#subprocess.call("gdalwarp -cutline shp/LC80080582015052LGN00_mask_b.shp -crop_to_cutline LC80080582015052-SC20160405003221/LC80080582015052LGN00_sr_stack.kea ROI-T/sr/LC80080582015052LGN00_b_sr.kea",shell=True)
#subprocess.call("gdalwarp -cutline shp/LC80080582015052LGN00_mask_b.shp -crop_to_cutline LC80080582015052-SC20160405003221/LC80080582015052LGN00_stack.kea ROI-T/stack/LC80080582015052LGN00_b_stack.kea",shell=True)

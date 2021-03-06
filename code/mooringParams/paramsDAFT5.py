# parameter library for Echoview processing

class wbatParams(): # daft/wbat metadata
    mooringNum = 5 # mooring id number
    mooringSer = 'NOAA2' # wbat serial number
    mooringSta = 'C1' # DAFT deployment station
    mooringDepth = 44.4 # depth of the mooring, used for surfAve line
    mooringLoc = [70.836015, -163.11475833] # DAFT deployment location
    
class evParams(): # Echoview specific needs
    newRaw = 0
    scrutinize = 0 # pause during batch for scrutinize
    numDays = 10 # number of days to include per file
    numFiles = [0] # number of files to create.  if '0', create ALL
    dataDir = 'E:\\MooredEchosounders\\data\\2019\\WBAT2\\' # directory of *.raw data
    outputDir = 'E:\\MooredEchosounders\\data\\2019\\EvFiles\\DAFT2\\' # directory for created EV files
    evTemplateFile = 'E:\\MooredEchosounders\\data\\EvTemplates\\ArcticEvTemplateWBAT2.EV' # EV template for file creation
    calFile = 'E:\\MooredEchosounders\\data\\EvTemplates\\wbatEmptyCal.ecs' # ecs file for specific wbat
    gridX = 60 # export grid, horizontal dimension (time, minutes)
    gridY = 5 # export grid, vertical dimension (meters)
    excludeBelow = 'transducerExclusionLine70'
    excludeAbove = 'surfaceExclusionLine70'
    singleTargetVar = '38 kHz single targets'
    classExport = 'fishTracks'
    surfaceLineBuffer = 2
    trackExportItems = ['Direction_horizontal','Direction_vertical','Distance_2D_unsmoothed','Distance_3D_unsmoothed','Fish_track_change_in_depth','Fish_track_change_in_range',
            'Speed_2D_max_unsmoothed','Speed_2D_mean_unsmoothed','Speed_4D_max_unsmoothed','Speed_4D_mean_unsmoothed','Time_in_beam','Tortuosity_2D','Tortuosity_3D',
            'Num_targets','Target_depth_max','Target_depth_mean','Target_depth_min','Target_length_mean','Target_range_max','Target_range_mean','Target_range_min',
            'TS_max','TS_mean','TS_min']
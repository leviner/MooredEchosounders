import win32com.client
import time
import pandas as pd
import numpy as np
'''
evBuilder will:
- Create a new file from params-defined template EV file
- Add *.raw files as outlined in 'fileSets' (i.e., fileSets = [[EV1 data list], [EV2 data list],...])
- Create a new surface exclusion line by adding a -2 meter offset to the surface threshold offset line
- Insert ST and ET markers at the first and last ping, assigning transect name by ct of fileSets
- Save and close file
'''

class evFiles():
    def evBuilder(processParams,fileSets,fileStart=0): # where fileSets is
        newFiles = []
        EvApp = win32com.client.Dispatch("EchoviewCom.EvApplication")
        EvApp.Minimize()
        if len(processParams.evParams.numFiles) == 1:
            if processParams.evParams.numFiles[0] == 0:
                fileCt = range(len(fileSets))
            else:
                fileCt = processParams.evParams.numFiles
        else:
            fileCt = processParams.evParams.numFiles
        for i in fileCt:
            start = time.time()
            print('\r Working on file '+str(i+1)+' of '+ str(np.max(fileCt)+1))
            # this will all be in a subloop, for i len total num files, e.g.
            EvFile = EvApp.NewFile(processParams.evParams.evTemplateFile)
            EvFileSet = EvFile.FileSets.FindByName('Fileset1') # replace with params value
            EvFileSet.SetCalibrationFile(processParams.evParams.calFile)
            for file in fileSets[i]: 
                EvFileSet.Datafiles.Add(file)

            EvSourceLine = EvFile.Lines.FindByName('surfaceThreshold'); # replace with params value
            EvNewLine1 = EvFile.Lines.CreateOffsetLinear(EvSourceLine,1,processParams.evParams.surfaceLineBuffer,1);
            EvNewLine1.Name = 'holdingLine2';
            EvLineOld = EvFile.Lines.FindByName(processParams.evParams.excludeAbove);
            EvLineOld.OverwriteWith(EvNewLine1)
            EvFile.Lines.Delete(EvNewLine1)

            EvVar = EvFile.Variables.FindByName('Fileset 1: Sv pings T1 (channel 1)')
            start_marker = 'ST_'+str(i+1)
            EvUpperLine = EvFile.Lines.FindByName(processParams.evParams.excludeAbove)
            EvLowerLine = EvFile.Lines.FindByName(processParams.evParams.excludeBelow)
            Region1 = EvVar.CreateLineRelativeRegion(start_marker,EvUpperLine,EvLowerLine,0,1)
            RegClassObj = EvFile.RegionClasses.FindByName('Unclassified regions')
            EvFile.Regions.FindByName(start_marker).RegionClass = RegClassObj
            EvFile.Regions.FindByName(start_marker).RegionType = 2 # 2 is marker, 1 is for analysis

            end_marker = 'ET_'+str(i+1)
            EvUpperLine = EvFile.Lines.FindByName(processParams.evParams.excludeAbove)
            EvLowerLine = EvFile.Lines.FindByName(processParams.evParams.excludeBelow)
            Region1 = EvVar.CreateLineRelativeRegion(end_marker,EvUpperLine,EvLowerLine,EvVar.MeasurementCount-1,EvVar.MeasurementCount);
            RegClassObj = EvFile.RegionClasses.FindByName('Unclassified regions');
            EvFile.Regions.FindByName(end_marker).RegionClass = RegClassObj
            EvFile.Regions.FindByName(end_marker).RegionType = 2 # 1 is for analysis
            if processParams.wbatParams.mooringNum < 4:
                EvFile.SaveAs(processParams.evParams.outputDir +'LoadedData-'+processParams.wbatParams.mooringSer +'-'+fileSets[i][0][-22:-14]+'-'+fileSets[i][-1][-22:-14]+'.EV')
                EvFile.Close()
                print('File Created. Total time: ' + str(int(np.floor((time.time()-start)/60)))+'m '+str(round((time.time()-start)%60))+ 's')
                newFiles.append(processParams.evParams.outputDir +'LoadedData-'+processParams.wbatParams.mooringSer +'-'+fileSets[i][0][-22:-14]+'-'+fileSets[i][-1][-22:-14]+'.EV')
            else:
                EvFile.SaveAs(processParams.evParams.outputDir +'LoadedData-'+processParams.wbatParams.mooringSer +'-'+fileSets[i][0][-25:-17]+'-'+fileSets[i][-1][-25:-17]+'.EV')
                EvFile.Close()
                print('File Created. Total time: ' + str(int(np.floor((time.time()-start)/60)))+'m '+str(round((time.time()-start)%60))+ 's')
                newFiles.append(processParams.evParams.outputDir +'LoadedData-'+processParams.wbatParams.mooringSer +'-'+fileSets[i][0][-25:-17]+'-'+fileSets[i][-1][-25:-17]+'.EV')
        EvApp.Quit()
        print('Done')
        return newFiles

    '''
    evExporter will:
    - Open file/files specified in the function call
    - Create line-relative region between exclude above and exclude below lines as defined in parameters
    - set analysis max/min thresholds
    - apply grid as defined by params
    - set analysis exclusion lines
    - export and close EV file
    '''
    def evExporter(processParams, evFiles): # where evFiles is a list of *.EV files (with complete path)
        newFiles = []
        EvApp = win32com.client.Dispatch("EchoviewCom.EvApplication")
        EvApp.Minimize()
        for file in evFiles:
            start = time.time()
            EvFile = EvApp.OpenFile(file)
            if processParams.evParams.newRaw ==1:
                EvFile.Properties.DataPaths.Add(processParams.evParams.dataDir)
                EvFile.SaveAs(file)
                EvApp.CloseFile(EvFile)
                EvFile = EvApp.OpenFile(file)
            
            EvFileSet = EvFile.FileSets.FindByName('Fileset1') # replace with params value
            EvFileSet.SetCalibrationFile(processParams.evParams.calFile)
            
            EvVar = EvFile.Variables.FindByName('Fileset 1: Sv pings T1 (channel 1)')

            EvUpperLine = EvFile.Lines.FindByName(processParams.evParams.excludeAbove);
            EvLowerLine = EvFile.Lines.FindByName(processParams.evParams.excludeBelow);
            Region1 = EvVar.CreateLineRelativeRegion('WaterColumn',EvUpperLine,EvLowerLine);
            RegClassObj = EvFile.RegionClasses.FindByName('WaterColumn');
            EvFile.Regions.FindByName('WaterColumn').RegionClass = RegClassObj;
            EvFile.Regions.FindByName('WaterColumn').RegionType = 1# 1 is for anlysis

            EvVar.Properties.Data.ApplyMinimumThreshold= 0;
            EvVar.Properties.Data.MinimumThreshold= -70;
            EvVar.Properties.Data.ApplyMaximumThreshold= 0;
            EvVar.Properties.Data.MaximumThreshold=-30;

            #  set grid settings for range in m and distance in nmi as defined by VL
            EvVar.Properties.Grid.SetDepthRangeGrid(1,processParams.evParams.gridY)
            EvVar.Properties.Grid.SetTimeDistanceGrid(1, processParams.evParams.gridX)# 1 is for time, 3 is for nmi

            # set exclusion lines
            EvVar.Properties.Analysis.ExcludeAboveLine = processParams.evParams.excludeAbove
            EvVar.Properties.Analysis.ExcludeBelowLine = processParams.evParams.excludeBelow

            ExportFileName=processParams.evParams.outputDir +'exports\\LoadedData-'+processParams.wbatParams.mooringSer + '-'+\
                 str(processParams.evParams.gridY)+'m'+'-'+file[-20:-12]+'-'+file[-11:-3]+'.csv'
            exporttest = EvVar.ExportIntegrationByRegionsByCellsAll(ExportFileName);
            if exporttest:
                print('File Exported. Total time: ' + str(int(np.floor((time.time()-start)/60)))+'m '+str(round((time.time()-start)%60))+ 's')
                newFiles.append(processParams.evParams.outputDir +'exports\\LoadedData-'+processParams.wbatParams.mooringSer + '-'+\
                                str(processParams.evParams.gridY)+'m'+'-'+file[-20:-12]+'-'+file[-11:-3]+'.csv')
            else:
                print('File Export Failed')
            EvFile.Close()
        EvApp.Quit()
        print('Done')
        return newFiles

    def evFishTracks(processParams, evFiles):
        newFiles = []
        EvApp = win32com.client.Dispatch("EchoviewCom.EvApplication")
        EvApp.Minimize()
        for file in evFiles:
            start = time.time()
            EvFile = EvApp.OpenFile(file)
            EvFileSet = EvFile.FileSets.FindByName('Fileset1') # replace with params value
            EvFileSet.SetCalibrationFile(processParams.evParams.calFile)
            EvVar = EvFile.Variables.FindByName(processParams.evParams.singleTargetVar) 
            EvVar.Properties.Analysis.ExcludeAboveLine = processParams.evParams.excludeAbove
            EvVar.Properties.Analysis.ExcludeBelowLine = processParams.evParams.excludeBelow
            EvVar.DetectFishTracks(processParams.evParams.classExport);
            EvFile.Properties.Export.Mode=1
            for item in processParams.evParams.trackExportItems:
                EvFile.Properties.Export.Variables.Item(item).Enabled=1
            EvFile.Properties.Export
            exporttest = EvVar.ExportFishTracksByRegionsAll(processParams.evParams.outputDir +'exports\\FishTracks-'+processParams.wbatParams.mooringSer +'-'+\
                                str(processParams.evParams.gridY)+'m'+'-'+file[-20:-12]+'-'+file[-11:-3]+'.csv')
            if exporttest:
                print('File Exported. Total time: ' + str(int(np.floor((time.time()-start)/60)))+'m '+str(round((time.time()-start)%60))+ 's')
                newFiles.append(processParams.evParams.outputDir +'exports\\FishTracks-'+processParams.wbatParams.mooringSer + '-'+\
                                    str(processParams.evParams.gridY)+'m'+'-'+file[-20:-12]+'-'+file[-11:-3]+'.csv')
            else:
                print('File Export Failed')
            EvFile.Close()
        EvApp.Quit()
        print('Done')
        return newFiles    
    
class evExports():
        # return pandas dataframe of datetime, layer number, and sA as long as 'Layer','PRC_NASC','Date_S', and 'Time_S' are in the export
    # export files can be a list of n-length of the csv files (full path)
    def readEvExports(exportFiles):
        nascDF = pd.DataFrame({'layer':[],'sA':[],'datetime':[]})
        for file in exportFiles:
            curFile = pd.read_csv(file)
            holding = {'layer':curFile['Layer'].values,'sA':curFile['PRC_NASC'].values,'datetime':pd.to_datetime(curFile['Date_S'].map(str)+'-'+curFile['Time_S'].map(str))}
            holdingDF = pd.DataFrame(holding)
            nascDF = nascDF.append(holdingDF)
        nascDF.set_index(nascDF["datetime"],inplace=True)
        return nascDF


def DICOM_HRD(dicomdirectory, hdrfilename, outfilepath):

     import itk
     import sys
     import os

     dirName = dicomdirectory

     PixelType = itk.ctype('signed short')
     Dimension = 3

     ImageType = itk.Image[PixelType, Dimension]

     namesGenerator = itk.GDCMSeriesFileNames.New()
     namesGenerator.SetUseSeriesDetails(True)
     namesGenerator.AddSeriesRestriction("0008|0021")
     namesGenerator.SetGlobalWarningDisplay(False)
     namesGenerator.SetDirectory(dirName)

     seriesUID = namesGenerator.GetSeriesUIDs()

     if len(seriesUID) < 1:
         print('No DICOMs in: ' + dirName)
         sys.exit(1)

     print('The directory: ' + dirName)
     print('Contains the following DICOM Series: ')
     for uid in seriesUID:
         print(uid)

     for uid in seriesUID:
         seriesIdentifier = uid

         print('Reading: ' + seriesIdentifier)
         fileNames = namesGenerator.GetFileNames(seriesIdentifier)

         reader = itk.ImageSeriesReader[ImageType].New()
         dicomIO = itk.GDCMImageIO.New()
         reader.SetImageIO(dicomIO)
         reader.SetFileNames(fileNames)
         reader.ForceOrthogonalDirectionOff()

         writer = itk.ImageFileWriter[ImageType].New()
         #outFileName = os.path.join(dirName, seriesIdentifier + '.nrrd')
         outFileName = os.path.join(outfilepath, hdrfilename + '.hdr')
         outFileNameimg=os.path.join(outfilepath, hdrfilename + '.img')
         if os.path.isfile(outFileName):
         	 os.remove(outFileName)
         if os.path.isfile(outFileNameimg):
         	 os.remove(outFileNameimg)

         writer.SetFileName(outFileName)
         writer.UseCompressionOn()
         writer.SetInput(reader.GetOutput())
         print('Writing: ' + outFileName)
         writer.Update()

     return seriesIdentifier, outFileName
 



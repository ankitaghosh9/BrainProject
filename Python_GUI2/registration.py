import timeit
import SimpleITK as sitk
from ipywidgets import interact, fixed
from IPython.display import clear_output
import itk
import matplotlib.pyplot as plt
import os
#get_ipython().run_line_magic('matplotlib', 'inline')

def display_images(fixed_image_z, moving_image_z, fixed_npa, moving_npa):
    # Create a figure with two subplots and the specified size.
    plt.subplots(1,2,figsize=(10,8))
    
    # Draw the fixed image in the first subplot.
    plt.subplot(1,2,1)
    plt.imshow(fixed_npa[fixed_image_z,:,:],cmap=plt.cm.Greys_r);
    plt.title('fixed image')
    plt.axis('off')
    
    # Draw the moving image in the second subplot.
    plt.subplot(1,2,2)
    plt.imshow(moving_npa[moving_image_z,:,:],cmap=plt.cm.Greys_r);
    plt.title('moving image')
    plt.axis('off')
    
    #plt.show()


def display_images_with_alpha(image_z, alpha, fixed, moving):
    img = (1.0 - alpha)*fixed[:,:,image_z] + alpha*moving[:,:,image_z] 
    plt.imshow(sitk.GetArrayViewFromImage(img),cmap=plt.cm.Greys_r);
    plt.axis('off')
    #plt.show()

# Callback invoked when the StartEvent happens, sets up our new data.
def start_plot():
    global metric_values, multires_iterations
    
    metric_values = []
    multires_iterations = []

# Callback invoked when the EndEvent happens, do cleanup of data and figure.
def end_plot():
    global metric_values, multires_iterations
    
    del metric_values
    del multires_iterations
    # Close figure, we don't want to get a duplicate of the plot latter on.
    plt.close()

# Callback invoked when the IterationEvent happens, update our data and display new figure.    
def plot_values(registration_method):
    global metric_values, multires_iterations
    
    metric_values.append(registration_method.GetMetricValue())                                       
    # Clear the output area (wait=True, to reduce flickering), and plot current data
    clear_output(wait=True)
    # Plot the similarity metric values
    plt.plot(metric_values, 'r')
    plt.plot(multires_iterations, [metric_values[index] for index in multires_iterations], 'b*')
    plt.xlabel('Iteration Number',fontsize=12)
    plt.ylabel('Metric Value',fontsize=12)
    #plt.show()
    
# Callback invoked when the sitkMultiResolutionIterationEvent happens, update the index into the 
# metric_values list. 
def update_multires_iterations():
    global metric_values, multires_iterations
    multires_iterations.append(len(metric_values)) 


def Affine(CTdata, MRIdata):

    fixed_image =  sitk.ReadImage(CTdata, sitk.sitkFloat32) #fixed image
    moving_image = sitk.ReadImage(MRIdata , sitk.sitkFloat32)  #moving image

    #interact(display_images, fixed_image_z=(0,fixed_image.GetSize()[2]-1), moving_image_z=(0,moving_image.GetSize()[2]-1), fixed_npa = fixed(sitk.GetArrayViewFromImage(fixed_image)), moving_npa=fixed(sitk.GetArrayViewFromImage(moving_image)));


    dim=3
    #f1=fixed_image.GetDimension(

    initial_transform = sitk.AffineTransform(dim)

    moving_resampled = sitk.Resample(moving_image, fixed_image, initial_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())

    #interact(display_images_with_alpha, image_z=(0,fixed_image.GetSize()[2]), alpha=(0.0,1.0,0.05), fixed = fixed(fixed_image), moving=fixed(moving_resampled));


    start = timeit.default_timer()
    registration_method = sitk.ImageRegistrationMethod()

    # Similarity metric settings.
    registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
    registration_method.SetMetricSamplingPercentage(0.01)

    registration_method.SetInterpolator(sitk.sitkLinear)

    # Optimizer settings.

    registration_method.SetOptimizerAsRegularStepGradientDescent(learningRate=5.0, minStep=1.0, numberOfIterations=100,relaxationFactor= 0.5, gradientMagnitudeTolerance=1e-4)
    #first : minstep=2,iterations=100,relaxation factor=0.5
    #second : minstep=1iterations=30,relaxation factor=0.0005
    #registration_method.SetOptimizerAsGradientDescent(learningRate=5.0, numberOfIterations=100, convergenceMinimumValue=1e-6, convergenceWindowSize=5)
    registration_method.SetOptimizerScalesFromPhysicalShift()



    # Setup for the multi-resolution framework.            
    registration_method.SetShrinkFactorsPerLevel(shrinkFactors = [6,2,1])
    registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[6,2,1])
    registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

    # Don't optimize in-place, we would possibly like to run this cell multiple times.
    registration_method.SetInitialTransform(initial_transform, inPlace=False)

    # Connect all of the observers so that we can perform plotting during registration.
    registration_method.AddCommand(sitk.sitkStartEvent, start_plot)
    registration_method.AddCommand(sitk.sitkEndEvent, end_plot)
    registration_method.AddCommand(sitk.sitkMultiResolutionIterationEvent, update_multires_iterations) 
    registration_method.AddCommand(sitk.sitkIterationEvent, lambda: plot_values(registration_method))

    # final_transform = registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkUInt8), 
#                                               sitk.Cast(moving_image, sitk.sitkUInt8))
    final_transform = registration_method.Execute(fixed_image, moving_image)

    stop = timeit.default_timer()

    print('Time: ', stop - start)  

    minut=(stop-start)//60
    print("Time {0} minutes ".format(minut))


    print('Final metric value: {0}'.format(registration_method.GetMetricValue()))
    print('Optimizer\'s stopping condition, {0}'.format(registration_method.GetOptimizerStopConditionDescription()))


    moving_resampled = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())

    #interact(display_images_with_alpha, image_z=(0,fixed_image.GetSize()[2]), alpha=(0.0,1.0,0.05), fixed = fixed(fixed_image), moving=fixed(moving_resampled));

    #sitk.WriteImage(moving_resampled, '/home/ghosh/Documents/Kumudha/Python_GUI2/Cache/hrdCT_affine.hdr') #output image
    return moving_resampled



def Bspline(CTdata, MRIdata):
    
    fixed_image =  sitk.ReadImage(CTdata, sitk.sitkFloat32) #fixed image
    moving_image = sitk.ReadImage(MRIdata , sitk.sitkFloat32)  #moving image
    #interact(display_images, fixed_image_z=(0,fixed_image.GetSize()[2]-1), moving_image_z=(0,moving_image.GetSize()[2]-1), fixed_npa = fixed(sitk.GetArrayViewFromImage(fixed_image)), moving_npa=fixed(sitk.GetArrayViewFromImage(moving_image)));

    transformDomainMeshSize=[10]*moving_image.GetDimension()
    initial_transform = sitk.BSplineTransformInitializer(fixed_image,
                                      transformDomainMeshSize )

    moving_resampled = sitk.Resample(moving_image, fixed_image, initial_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())

    #interact(display_images_with_alpha, image_z=(0,fixed_image.GetSize()[2]), alpha=(0.0,1.0,0.05), fixed = fixed(fixed_image), moving=fixed(moving_resampled));

    start = timeit.default_timer()
    registration_method = sitk.ImageRegistrationMethod()

    # Similarity metric settings.
    registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
    registration_method.SetMetricSamplingPercentage(0.01)

    registration_method.SetInterpolator(sitk.sitkLinear)

    # Optimizer settings.

    registration_method.SetOptimizerAsRegularStepGradientDescent(learningRate=5.0, minStep=1.0, numberOfIterations=300,relaxationFactor= 0.0005, gradientMagnitudeTolerance=1e-4)
    #first : minstep=2,iterations=100,relaxation factor=0.5
    #second : minstep=1iterations=30,relaxation factor=0.0005
    #registration_method.SetOptimizerAsGradientDescent(learningRate=5.0, numberOfIterations=100, convergenceMinimumValue=1e-6, convergenceWindowSize=5)
    registration_method.SetOptimizerScalesFromPhysicalShift()

    # Setup for the multi-resolution framework.            
    registration_method.SetShrinkFactorsPerLevel(shrinkFactors = [6,2,1])
    registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[6,2,1])
    registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

    # Don't optimize in-place, we would possibly like to run this cell multiple times.
    registration_method.SetInitialTransform(initial_transform, inPlace=False)

    # Connect all of the observers so that we can perform plotting during registration.
    registration_method.AddCommand(sitk.sitkStartEvent, start_plot)
    registration_method.AddCommand(sitk.sitkEndEvent, end_plot)
    registration_method.AddCommand(sitk.sitkMultiResolutionIterationEvent, update_multires_iterations) 
    registration_method.AddCommand(sitk.sitkIterationEvent, lambda: plot_values(registration_method))

    # final_transform = registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkUInt8), 
    #                                               sitk.Cast(moving_image, sitk.sitkUInt8))
    final_transform = registration_method.Execute(fixed_image, moving_image)


    stop = timeit.default_timer()

    print('Time: ', stop - start)  

    minut=(stop-start)//60
    print("Time {0} minutes ".format(minut))

    # R = sitk.ImageRegistrationMethod()
    # R.SetMetricAsMattesMutualInformation(50)
    # R.SetOptimizerAsGradientDescentLineSearch(5.0, 100,
    #                                           convergenceMinimumValue=1e-4,
    #                                           convergenceWindowSize=5)
    # R.SetOptimizerScalesFromPhysicalShift( )
    # R.SetInitialTransform(initial_transform)
    # R.SetInterpolator(sitk.sitkLinear)

    # R.SetShrinkFactorsPerLevel([6,2,1])
    # R.SetSmoothingSigmasPerLevel([6,2,1])


    print('Final metric value: {0}'.format(registration_method.GetMetricValue()))
    print('Optimizer\'s stopping condition, {0}'.format(registration_method.GetOptimizerStopConditionDescription()))

    moving_resampled = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())

    #interact(display_images_with_alpha, image_z=(0,fixed_image.GetSize()[2]), alpha=(0.0,1.0,0.05), fixed = fixed(fixed_image), moving=fixed(moving_resampled));

    #sitk.WriteImage(moving_resampled, '/home/ghosh/Documents/Kumudha/Python_GUI2/Cache/hrdCT_bspline.hdr') #Output file
    return moving_resampled
    #sitk.WriteTransform(final_transform, os.path.join(OUTPUT_DIR, 'RIRE_training_001_CT_2_mr_T1.tfm'))

def Both_AffineBspline(CTdata,MRIdata):
    
    affineCT=Affine(CTdata,MRIdata)
    intermediate_path= os.path.join(os.path.dirname(os.path.abspath(__file__)),"Cache","affineCT_intermediate.hdr")
    sitk.WriteImage(affineCT, intermediate_path)
    bothCT=Bspline(intermediate_path,MRIdata)
    os.remove(intermediate_path)
    os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Cache","affineCT_intermediate.img"))
    return bothCT

def Fusion(CTdata,Regdata):
    Ctimage =  sitk.ReadImage(CTdata, sitk.sitkFloat32) #CT Image
    regis = sitk.ReadImage(Regdata, sitk.sitkFloat32) #Registration Image

    space=regis.GetSpacing()
    #space

    Direction=regis.GetDirection()
    #Direction
    space=Ctimage.GetSpacing()
    #space
    Direction=Ctimage.GetDirection()
    #Direction

    regis.SetSpacing(Ctimage.GetSpacing())
    regis.GetSpacing()

    #Ctimage.SetSpacing([1000.0, 1000.0, 1000.0])
    #result=itk.AddImageFilter(Ctimage,regis,)
    result=sitk.AddImageFilter()
    #regis.SetSpacing(space)
    result1=result.Execute(Ctimage,regis)

    #sitk.WriteImage(result1, 'final_ctbone_affine1.hdr') #Output file
    return result1

#Affine()
#Bspline()
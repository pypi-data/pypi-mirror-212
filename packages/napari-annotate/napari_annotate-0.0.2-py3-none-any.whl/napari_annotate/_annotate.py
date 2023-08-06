import numpy as np
import os
from glob import glob
from napari.layers import Image, Shapes, Labels
from napari.viewer import Viewer
from napari.types import LayerDataTuple
from magicgui import magic_factory
import tifffile
from skimage.io import imsave, imread

@magic_factory(call_button='Next slide',
               path={'tooltip': 'Path to the folder containing the data.'},
               keyword={'tooltip': 'Keyword to fetch data to annotate'},
               resolution={'tooltip': 'Resolution of pulled image. Higher resolution might lead to lags and slow annotation',
                           'widget_type': 'ComboBox',
                           'choices': [0, 1, 2],
                           'value': 1},
               )
def next_slide_huron(viewer: Viewer,
               path: str='',
               keyword: str='*DAPI.tif',
               resolution: int=1) -> LayerDataTuple:
    """
    Go to next slide for annotating:
        1) Save current annotation if there is one to save
        2) Fetch the next slide to annotate

    Parameters
    ----------
    viewer: napari.Viewer
        viewer object to access layers
    path: str
        path to folder containing the data
    keyword: str
        keyword to select slides
    resolution: int
        resolution to read tiff files

    Returns
    -------
    list of LayerDataTuple to be displayed by napari
    """
    # First we check if there is something to save
    if len(viewer.layers) > 0:
        filename = viewer.layers[0].metadata['source'][:-4] + '_annotations.tif'
        imsave(filename, viewer.layers[2].data, compression='ZLIB', check_contrast=False)
        # Remove previous layers
        for i in range(len(viewer.layers)):
            del viewer.layers[0]

    # Then we find all images that can be annotated
    microscopy_slides = sorted(glob(os.path.join(path, '*/')))
    list_to_annotate = []
    for folder in microscopy_slides:
        existing_slides = glob(os.path.join(folder, keyword))
        # Add the slide only if there is no existing annotation
        for s in existing_slides:
            if not os.path.exists(s[:-4] + '_annotations.tif'):
                list_to_annotate.append(s)

    # If there are no slides left to annotate, go to review mode
    if list_to_annotate == []:
        review_annotations_huron(viewer, path, keyword, resolution)

    data = read_slide(list_to_annotate[0], resolution)
    tuple_data = (data,
                  {'name': 'Slide ({} left)'.format(len(list_to_annotate)), 'contrast_limits': [0, 65000],
                   'metadata': {'source': list_to_annotate[0]}},
                  'image')
    tuple_label = (np.zeros_like(data, dtype='uint8'),
                   {'name': 'Annotation mask'},
                   'labels')
    tuple_text = (None,
                  {'name': '{}'.format(os.path.basename(list_to_annotate[0]))},
                  'shapes')

    return [tuple_data, tuple_text, tuple_label]

@magic_factory(call_button='Next slide',
               path={'tooltip': 'Path to the folder containing the data.'},
               keyword1={'tooltip': 'Keyword to fetch data to annotate'},
               keyword2={'tooltip': 'Keyword to fetch data to annotate'},
               resolution={'tooltip': 'Resolution of pulled image. Higher resolution might lead to lags and slow annotation',
                           'widget_type': 'ComboBox',
                           'choices': [0, 1, 2, 3, 4],
                           'value': 1},
               )
def next_slide_olympus(viewer: Viewer,
               path: str='',
               keyword1: str='CH1',
               keyword2: str='CH3',
               resolution: int=1) -> LayerDataTuple:
    """
    Go to next slide for annotating:
        1) Save current annotation if there is one to save
        2) Fetch the next slide to annotate

    Parameters
    ----------
    viewer: napari.Viewer
        viewer object to access layers
    path: str
        path to folder containing the data
    keyword1: str
        keyword to select slides
    keyword2: str (optional)
        keyword to select slides
    resolution: int
        resolution to read tiff files

    Returns
    -------
    list of LayerDataTuple to be displayed by napari
    """
    # First we check if there is something to save
    if len(viewer.layers) > 0:
        filename = os.path.join(viewer.layers[0].metadata['source'], 'annotations.tif')
        imsave(filename, viewer.layers[-1].data[::-1, :], compression='ZLIB', check_contrast=False)
        print(viewer.layers[-1].data[::-1, :].max())
        # Remove previous layers
        for i in range(len(viewer.layers)):
            del viewer.layers[0]

    # Then we find all images that can be annotated
    existing_slides = sorted(glob(os.path.join(path, '*', 'Layer*')))

    # Add the slide only if there is no existing annotation
    list_to_annotate = []
    for s in existing_slides:
        if s.endswith('0'):
            continue
        if not os.path.exists(os.path.join(s, 'annotations.tif')):
            list_to_annotate.append(s)

    # If there are no slides left to annotate, go to review mode
    if list_to_annotate == []:
        review_annotations_olympus(viewer, path, keyword1, keyword2, resolution)

    data1 = read_slide(os.path.join(list_to_annotate[0], keyword1 + '_{}.tif'.format(16-resolution)),
                                    resolution=0)
    tuple_data1 = (data1[::-1, :],
                  {'name': '{} ({} left)'.format(keyword1, len(list_to_annotate)), 'contrast_limits': [0, 1500],
                   'gamma': 0.5, 'colormap': 'gray' if keyword2=='' else 'red', 'blending': 'additive',
                   'metadata': {'source': list_to_annotate[0]}},
                  'image')
    tuple_label = (np.zeros_like(data1, dtype='uint8'),
                   {'name': 'Annotation mask'},
                   'labels')
    tuple_text = (None,
                  {'name': '{}/{}'.format(list_to_annotate[0].split('/')[-3],
                                          list_to_annotate[0].split('/')[-2])},
                  'shapes')

    if keyword2 != '':
        data2 = read_slide(os.path.join(list_to_annotate[0], keyword2 + '_{}.tif'.format(16 - resolution)),
                           resolution=0)
        tuple_data2 = (data2[::-1, :],
                      {'name': '{}'.format(keyword2), 'contrast_limits': [0, 1500], 'gamma': 0.5,
                       'colormap': 'green', 'blending': 'additive'},
                      'image')
        return [tuple_data1, tuple_data2, tuple_text, tuple_label]

    return [tuple_data1, tuple_text, tuple_label]

@magic_factory(call_button='Review annotations',
               path={'tooltip': 'Path to the folder containing the data.'},
               keyword={'tooltip': 'Keyword to fetch data to annotate'},
               resolution={'tooltip': 'Resolution of pulled image. Higher resolution might lead to lags and slow annotation',
                           'widget_type': 'ComboBox',
                           'choices': [0, 1, 2],
                           'value': 1}
               )
def review_annotations_huron(viewer: Viewer,
                       path: str='',
                       keyword: str='*DAPI.tif',
                       resolution: int=1) -> LayerDataTuple:
    """
    Go to next slide for reviewing:
        1) List all annotated slides if not done already
        2) Fetch the next slide to review

    Parameters
    ----------
    viewer: napari.Viewer
        viewer object to access layers
    path: str
        path to folder containing the data
    keyword: str
        keyword to select slides
    resolution: int
        resolution to read tiff files

    Returns
    -------
    list of LayerDataTuple to be displayed by napari
    """

    if len(viewer.layers) == 0:
        # Case when you start reviewing from scratch
        # Find all images that are already annotated
        microscopy_slides = sorted(glob(os.path.join(path, '*')))
        list_annotated = []
        for folder in microscopy_slides:
            existing_slides = glob(os.path.join(folder, keyword))
            # Add the slide only if there is no existing annotation
            for s in existing_slides:
                if os.path.exists(s[:-4] + '_annotations.tif'):
                    list_annotated.append(s)
    # First we check if there is something to save
    elif len(viewer.layers) > 0:
        if 'source' in viewer.layers[0].metadata:
            # Previous mode was annotating
            # Remove previous layers
            for i in range(len(viewer.layers)):
                del viewer.layers[0]
            # Find all images that are already annotated
            microscopy_slides = glob(os.path.join(path, '*'))
            list_annotated = []
            for folder in microscopy_slides:
                existing_slides = glob(os.path.join(folder, keyword))
                # Add the slide only if there is no existing annotation
                for s in existing_slides:
                    if os.path.exists(s[:-4] + '_annotations.tif'):
                        list_annotated.append(s)
        elif 'list_annotated' in viewer.layers[0].metadata:
            # Previous mode was review
            list_annotated = viewer.layers[0].metadata['list_annotated']
            list_annotated.pop(0)
            # Remove previous layers
            for i in range(len(viewer.layers)):
                del viewer.layers[0]

    if len(list_annotated)>0:
        data = read_slide(list_annotated[0], resolution)
        labels = imread(list_annotated[0][:-4] + '_annotations.tif')
        tuple_data = (data,
                      {'name': 'Slide ({} left)'.format(len(list_annotated)), 'contrast_limits': [0, 65000],
                       'metadata': {'list_annotated': list_annotated}},
                      'image')
        tuple_label = (labels,
                       {'name': 'Annotation mask',
                        'scale': [data.shape[0]/labels.shape[0], data.shape[1]/labels.shape[1]]},
                        'labels')
        tuple_text = (None,
                      {'name': '{}'.format(os.path.basename(list_annotated[0]))},
                      'shapes')

        return [tuple_data, tuple_text, tuple_label]
    else:
        return None

@magic_factory(call_button='Review annotations',
               path={'tooltip': 'Path to the folder containing the data.'},
               keyword1={'tooltip': 'Keyword to fetch data to annotate'},
               keyword2={'tooltip': 'Keyword to fetch data to annotate'},
               resolution={'tooltip': 'Resolution of pulled image. Higher resolution might lead to lags and slow annotation',
                           'widget_type': 'ComboBox',
                           'choices': [0, 1, 2, 3, 4],
                           'value': 1}
               )
def review_annotations_olympus(viewer: Viewer,
               path: str='',
               keyword1: str='CH1',
               keyword2: str='CH3',
               resolution: int=1) -> LayerDataTuple:
    """
    Go to next slide for reviewing:
        1) List all annotated slides if not done already
        2) Fetch the next slide to review

    Parameters
    ----------
    viewer: napari.Viewer
        viewer object to access layers
    path: str
        path to folder containing the data
    keyword1: str
        keyword to select slides
    keyword2: str (optional)
        keyword to select slides
    resolution: int
        resolution to read tiff files

    Returns
    -------
    list of LayerDataTuple to be displayed by napari
    """

    if len(viewer.layers) == 0:
        # Case when you start reviewing from scratch
        # Find all images that are already annotated
        existing_slides = sorted(glob(os.path.join(path, '*', 'Layer*')))
        list_annotated = []
        for s in existing_slides:
            if s.endswith('0'):
                continue
            if os.path.exists(os.path.join(s, 'annotations.tif')):
                list_annotated.append(s)

    elif len(viewer.layers) > 0:
        if 'source' in viewer.layers[0].metadata:
            # Previous mode was annotating
            # Remove previous layers
            for i in range(len(viewer.layers)):
                del viewer.layers[0]
            # Find all images that are already annotated
            existing_slides = sorted(glob(os.path.join(path, '*', 'Layer*')))
            list_annotated = []
            for s in existing_slides:
                if s.endswith('0'):
                    continue
                if os.path.exists(os.path.join(s, 'annotations.tif')):
                    list_annotated.append(s)
        elif 'list_annotated' in viewer.layers[0].metadata:
            # Previous mode was review
            list_annotated = viewer.layers[0].metadata['list_annotated']
            list_annotated.pop(0)
            # Remove previous layers
            for i in range(len(viewer.layers)):
                del viewer.layers[0]

    if len(list_annotated)>0:
        data1 = read_slide(os.path.join(list_annotated[0], keyword1 + '_{}.tif'.format(16 - resolution)),
                           resolution=0)
        labels = imread(os.path.join(list_annotated[0], 'annotations.tif'))
        tuple_data1 = (data1[::-1, :],
                       {'name': '{} ({} left)'.format(keyword1, len(list_annotated)), 'contrast_limits': [0, 1500],
                        'gamma': 0.5, 'colormap': 'gray' if keyword2 == '' else 'red', 'blending': 'additive',
                        'metadata': {'list_annotated': list_annotated}},
                       'image')
        tuple_label = (labels[::-1, :],
                       {'name': 'Annotation mask',
                        'scale': [data1.shape[0]/labels.shape[0], data1.shape[1]/labels.shape[1]]},
                        'labels')
        tuple_text = (None,
                      {'name': '{}/{}'.format(list_annotated[0].split('/')[-3],
                                              list_annotated[0].split('/')[-2])},
                      'shapes')

        if keyword2 != '':
            data2 = read_slide(os.path.join(list_annotated[0], keyword2 + '_{}.tif'.format(16 - resolution)),
                               resolution=0)
            tuple_data2 = (data2[::-1, :],
                           {'name': '{}'.format(keyword2), 'contrast_limits': [0, 1500], 'gamma': 0.5,
                            'colormap': 'green', 'blending': 'additive'},
                           'image')
            return [tuple_data1, tuple_data2, tuple_text, tuple_label]
        else:
            return [tuple_data1, tuple_text, tuple_label]
    else:
        return None

@magic_factory(call_button='Review segmentations',
               path={'tooltip': 'Path to the folder containing the data.'},
               keyword={'tooltip': 'Keyword to fetch data'},
               resolution={'tooltip': 'Resolution of pulled image. Higher resolution might lead to lags and slow annotation',
                           'widget_type': 'ComboBox',
                           'choices': [0, 1, 2],
                           'value': 1},
               force_roi={'tooltip': 'Display data only when ROI is available'}
               )
def review_segmentations(viewer: Viewer,
                         path: str='',
                         keyword: str='*DAPI.tif',
                         resolution: int=1,
                         force_roi: bool=False) -> LayerDataTuple:
    """
    Go to next slide for reviewing:
        1) List all annotated slides if not done already
        2) Fetch the next slide to review

    Parameters
    ----------
    viewer: napari.Viewer
        viewer object to access layers
    path: str
        path to folder containing the data
    keyword: str
        keyword to select slides
    resolution: int
        resolution to read tiff files
    force_roi: bool
        display only the segmentation when ROI is available

    Returns
    -------
    list of LayerDataTuple to be displayed by napari
    """

    if len(viewer.layers) == 0:
        # Case when you start reviewing from scratch
        # Find all images that are already segmented
        microscopy_slides = sorted(glob(os.path.join(path, '*')))
        list_segmented = []
        for folder in microscopy_slides:
            existing_slides = glob(os.path.join(folder, keyword))
            for s in existing_slides:
                if os.path.exists(s[:-4] + '_lmap.tif'):
                    list_segmented.append(s)
    # First we check if there is something to save
    elif len(viewer.layers) > 0:
        if 'source' in viewer.layers[0].metadata:
            # Previous mode was annotating
            # Remove previous layers
            for i in range(len(viewer.layers)):
                del viewer.layers[0]
            # Find all images that are already segmented
            microscopy_slides = glob(os.path.join(path, '*'))
            list_segmented = []
            for folder in microscopy_slides:
                existing_slides = glob(os.path.join(folder, keyword))
                # Add the slide only if there is no existing annotation
                for s in existing_slides:
                    if force_roi and os.path.exists(s[:-4] + '_lmap.tif'):
                        list_segmented.append(s)
                    elif not force_roi:
                        list_segmented.append(s)
        elif 'list_segmented' in viewer.layers[0].metadata:
            # Previous mode was review
            list_segmented = viewer.layers[0].metadata['list_segmented']
            list_segmented.pop(0)
            # Remove previous layers
            for i in range(len(viewer.layers)):
                del viewer.layers[0]

    if force_roi:
        if len(list_segmented)>0:
            # Check if annotation is not empty
            while len(list_segmented)>0:
                folder, filename = os.path.split(list_segmented[0])
                file_annotation = glob(os.path.join(folder, filename[:7]) + '*_annotations.tif')
                if len(file_annotation)==1:
                    labels = imread(file_annotation[0])
                    if labels.max() > 0:
                        data = read_slide(list_segmented[0], resolution)
                        lmap = imread(list_segmented[0][:-4] + '_lmap.tif')
                        tuple_data = (data,
                                      {'name': 'Slide ({} left)'.format(len(list_segmented)), 'contrast_limits': [0, 65000],
                                       'metadata': {'list_segmented': list_segmented}},
                                      'image')
                        tuple_lmap = (imread(list_segmented[0][:-4] + '_lmap.tif'),
                                      {'name': 'Segmentation',
                                       'scale': [data.shape[0] / lmap.shape[0], data.shape[1] / lmap.shape[1]]},
                                      'labels')
                        tuple_text = (None,
                                      {'name': '{}'.format(os.path.basename(list_segmented[0]))},
                                      'shapes')
                        if force_roi:
                            tuple_label = (labels,
                                           {'name': 'Annotation mask',
                                            'scale': [data.shape[0] / labels.shape[0], data.shape[1] / labels.shape[1]]},
                                           'labels')

                        return [tuple_data, tuple_text, tuple_lmap, tuple_label]
                    else:
                        list_segmented.pop(0)
                else:
                    list_segmented.pop(0)

    else:
        if len(list_segmented) > 0:
            data = read_slide(list_segmented[0], resolution)
            lmap = imread(list_segmented[0][:-4] + '_lmap.tif')
            tuple_data = (data,
                          {'name': 'Slide ({} left)'.format(len(list_segmented)), 'contrast_limits': [0, 65000],
                           'metadata': {'list_segmented': list_segmented}},
                          'image')
            tuple_lmap = (imread(list_segmented[0][:-4] + '_lmap.tif'),
                          {'name': 'Segmentation',
                           'scale': [data.shape[0] / lmap.shape[0], data.shape[1] / lmap.shape[1]]},
                          'labels')
            tuple_text = (None,
                          {'name': '{}'.format(os.path.basename(list_segmented[0]))},
                          'shapes')

            return [tuple_data, tuple_text, tuple_lmap]
        else:
            return None

@magic_factory(call_button='Add annotations',
               path={'tooltip': 'Path to the folder containing the data.'},
               keyword={'tooltip': 'Keyword to fetch data to annotate'},
               resolution={'tooltip': 'Resolution of pulled image. Higher resolution might lead to lags and slow annotation',
                           'widget_type': 'ComboBox',
                           'choices': [0, 1, 2],
                           'value': 1}
               )
def add_annotations(viewer: Viewer,
                       path: str='',
                       keyword: str='*DAPI.tif',
                       resolution: int=1,
                    ) -> LayerDataTuple:
    """
    Go to next slide for adding annotations:
        1) List all annotated slides if not done already
        2) Fetch the next slide to review

    Parameters
    ----------
    viewer: napari.Viewer
        viewer object to access layers
    path: str
        path to folder containing the data
    keyword: str
        keyword to select slides
    resolution: int
        resolution to read tiff files

    Returns
    -------
    list of LayerDataTuple to be displayed by napari
    """

    if len(viewer.layers) == 0:
        # Case when you start adding from scratch
        # Find all images that are already annotated
        microscopy_slides = sorted(glob(os.path.join(path, '*')))
        list_annotated = []
        for folder in microscopy_slides:
            existing_slides = glob(os.path.join(folder, keyword))
            # Add the slide only if there is no existing annotation
            for s in existing_slides:
                if os.path.exists(s[:-4] + '_annotations.tif'):
                    list_annotated.append(s)
    # First we check if there is something to save
    elif len(viewer.layers) > 0:
        if 'list_annotated' not in viewer.layers[0].metadata:
            # Previous mode was annotating
            # Remove previous layers
            for i in range(len(viewer.layers)):
                del viewer.layers[0]
            # Find all images that are already annotated
            microscopy_slides = glob(os.path.join(path, '*'))
            list_annotated = []
            for folder in microscopy_slides:
                existing_slides = glob(os.path.join(folder, keyword))
                # Add the slide only if there is no existing annotation
                for s in existing_slides:
                    if os.path.exists(s[:-4] + '_annotations.tif'):
                        list_annotated.append(s)

        else:
            # Previous mode was review
            list_annotated = viewer.layers[0].metadata['list_annotated']

            # Save previous annotations
            filename = list_annotated[0][:-4] + '_annotations.tif'
            imsave(filename, viewer.layers[2].data, compression='ZLIB', check_contrast=False)

            list_annotated.pop(0)
            # Remove previous layers
            for i in range(len(viewer.layers)):
                del viewer.layers[0]

    if len(list_annotated)>0:
        data = read_slide(list_annotated[0], resolution)
        labels = imread(list_annotated[0][:-4] + '_annotations.tif')
        tuple_data = (data,
                      {'name': 'Slide ({} left)'.format(len(list_annotated)), 'contrast_limits': [0, 65000],
                       'metadata': {'list_annotated': list_annotated}},
                      'image')
        tuple_label = (labels,
                       {'name': 'Annotation mask',
                        'scale': [data.shape[0]/labels.shape[0], data.shape[1]/labels.shape[1]]},
                        'labels')
        tuple_text = (None,
                      {'name': '{}'.format(os.path.basename(list_annotated[0]))},
                      'shapes')

        return [tuple_data, tuple_text, tuple_label]
    else:
        raise ValueError('ANNOTATIONS COMPLETE')

def read_slide(path, resolution):
    """
    Read tiff at a given resolution.

    Parameters
    ----------
    path: str
        path to the stored tiff file
    resolution: int
        resolution to read (0 is highest, then 1, etc.)

    Returns
    -------
    Array containing the tiff data.
    """
    u =  tifffile.imread(path, level=resolution)
    return u
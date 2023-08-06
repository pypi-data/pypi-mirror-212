import numpy as np
import os
from os import listdir
import glob
import copy
from pathlib import Path
import pathlib

import re
from typing import List, Any, Union, Tuple, Dict
from tkinter import Tk, filedialog, simpledialog
import xml.etree.cElementTree as ET
import shutil

import dask
import dask_image.imread
import dask.array as da
import tifffile

from PIL import Image
from skimage import io

import PySimpleGUI as sg


def get_num_values_text(path_text, target_values_string):

    '''
    This function extracts the needed meta-data from a text file. It extracts the numerical values from the line of the
    text files that contains the string in target_values_string. This function works only if there are no lines that start
    with the same string in the text file. This is why there is a second function get_num_values_text_2

    Parameters:
    ----------
    path_text: str path of the text file from which to extract the meta data
    target_values_string: list of str that contains the names of the meta data to extract
    '''

    with open(path_text) as f:
        lines = f.readlines()
    size_loop = len(target_values_string)
    num_values = np.zeros(size_loop)

    for ind1 in range(
            len(lines)):  # loops over all the lines of the text files, for each of them, check if the strings in target_values_string are present
        for ind2 in range(size_loop):
            string_test = lines[ind1]
            string_target = target_values_string[ind2]

            # the target string has to be smaller than the line of text (string_test variable) that contains it
            if len(string_target) < len(string_test):

                # if the string_target is present in the line of text, the number present in the line is extracted and saved
                # (This works since there is a single number per line of meta data text)
                if string_target in string_test:
                    temp = re.findall('[0-9]+', string_test)
                    # Here the two strings corresponding to each side of the decimal points are merged to form a float
                    if len(temp) == 2:
                        num_values[ind2] = np.array(float(temp[0]) + float(temp[1]) / 10 ** len(temp[1]))
                    # If the value of the meta-data data of interest is an integer, the single string is directly converted to a float
                    if len(temp) == 1:
                        num_values[ind2] = np.array(float(temp[0]))


    return num_values


def get_num_values_text2(path_text, target_line_number):

    '''
    This second version of get_num_values_text will search for numerical values at specified lines in the text file.
    This is used for the COLM meta-data where more than one line start with the same key string, making the other version
    of get_num_values_text not working.

    Parameters:
    ----------
    path_text: str path of the text file from which to extract the meta data
    target_line_number: list of str that contains the lines of the text file from which to extract the numerical values
    corresponding to the desired meta-data
    '''

    target_line_number = np.array(target_line_number)

    with open(path_text) as f:
        lines = f.readlines()
    size_loop = target_line_number.size
    num_values = np.zeros(size_loop)

    for ind1 in range(size_loop):
        target_line = target_line_number[ind1]
        string_test = lines[target_line]
        '''
        This function expects that there is a single numerical value stored per line in the meta-data file. If there is
        a decimal point, the temp variable will contain to strings, 1 for each side of the decimal point.
        '''
        temp = re.findall('[0-9]+', string_test)

        # Here the two strings corresponding to each side of the decimal points are merged to form a float
        if len(temp) == 2:
            num_values[ind1] = np.array(float(temp[0])+float(temp[1])/10**len(temp[1]))
        # If the value of the meta-data data of interest is an integer, the single string is directly converted to a float
        if len(temp) == 1:
            num_values[ind1] = np.array(float(temp[0]))
    return num_values


def get_type_microscope(path):
    """
    Returns the type of microscope. This functions looks for specific files / folder to each type of acquisition
    that are found in the base folder.

    In order to add additional microscope, a new sting must be added at the end of the diff_types_microscopes
    and test_string_list_microscopes variables.
    """

    # Names of types of microscopes
    diff_types_microscopes = ["Clear Scope", "COLM", "MesoSPIM_2D", "MesoSPIM_3D"]

    # Files / folders present in the base folder (that is dragged and dropped) corresponding to the above
    # types of microscopes
    test_string_list_microscopes = ["AssemblyData.txt", "VW0", "MetaDataMesoSPIM", "tiff_meta"]

    file_list = sorted(listdir(path))

    count_true = 0
    for ind1 in range(len(diff_types_microscopes)):
        for ind2 in range(len(file_list)):

            fullstring = file_list[ind2]
            substring = test_string_list_microscopes[ind1]

            # if substring in fullstring:
            if fullstring.find(substring) != -1:
                count_true = count_true + 1
                type_microscope = diff_types_microscopes[ind1]

    if count_true == 0:
        raise FileNotFoundError("ERROR: There are no files that correspond on of the types of microscope in the folder")

    '''
    To determine the subtype of microscope between MesoSPIM_3D and MesoSPIM_3D_substack, the goal is to find the mumber
    of underscores "_" between the "Ch" and "Sh" part of the name of the files, which are 1 and 2 respectively.
    It's 2 since there is an added number in between indicating the substack as seen in the example names:
     *Tile0_Ch647_Sh0 and *Tile0_Ch647_2_Sh0
    
    The loop is stopped after the first file name that contains the mentionned strings
    '''
    if type_microscope == "MesoSPIM_3D":

        is_continue_loop = True
        for ind in range(len(file_list)):
            fullstring = file_list[ind]

            ind_str_1 = fullstring.find("Ch")
            ind_str_2 = fullstring.find("Sh")

            if ind_str_1 != -1 and ind_str_2 != -1:
                if fullstring[ind_str_1:ind_str_2].count("_") > 1:
                    type_microscope = 'MesoSPIM_3D_substack'
                is_continue_loop = False

            if not is_continue_loop:
                break


    return type_microscope


def range_overlap(range_1, range_2):
    '''
    This finds the intersection of two ranges.
    Examples [0, 10] and [5, 20] -> [5, 10], [0, 10] and [5, 7] -> [5, 7]
    This function is used when creating the xml file of a partial tiling.
    It is used to determine the smaller ROI compared to the whole tiling.

    :param range_1:
    :param range_2:
    :return:
    '''

    range_1 = np.array([range_1])
    range_2 = np.array([range_2])
    intersect_range = np.array([np.maximum(np.amin(range_1), np.amin(range_2)),
                             np.minimum(np.amax(range_1), np.amax(range_2))])
    return intersect_range


def add_meta_data_field_in_layer_list(my_layer_list, name_field, content_field):
    '''
    This function adds the content_field (can be anything) to the metadata field of the directory of each layer in the
    my_layer_list object

    :param my_layer_list: object that is passed to napari and contains all the information to create the layers in the
    naparis layer
    :param name_field: name of the new field that is added in the meta data dictionary
    :param content_field: variable or object that will be added to in the new field in meta_data
    :return: returns a modified version of the input object my_layer_list
    '''

    for ind in range(len(my_layer_list)):
        temp_layer = my_layer_list[ind]
        temp_dict = temp_layer[1]['metadata']
        temp_dict[name_field] = content_field
        temp_layer[1]['metadata'] = temp_dict
        my_layer_list[ind] = temp_layer

    return my_layer_list

    '''
    For each file test if contains _Tiles to ensure it is a file that needs converting, and not an xml, or a preview
    from TerasTitcher.
        Then if its a tiff:
            1. Create a folder with the same name as the tiff file. 
            2. Open tiff3D
            3. Convert it into array.
            4. Loop over z and:
                a. create a 2D array that contains the slice
                b. save in the folder, with the same name + "_slice_zn"
        If its not a tif, thus a metadata file, 
            copy paste the meta data file in the new location
            
            
    
    '''


def convert_tiff_images_from_3D_to_2D(base_path, target_path):
    '''
    :param base_path: path where the 3D tiff are stored
    :param target_path: path where to store teh 2D tiff
    :return:
    '''
    isMetaDataFolderCreated = False
    # Loop over all the files in base path
    file_list = sorted(listdir(base_path))
    size_loop1 = len(file_list)
    count = 0
    is_to_extract_for_substack = np.ones((size_loop1,1))
    for ind1 in range(size_loop1):
        '''
        For each file test if contains _Tiles to ensure it is a file that needs converting, and not an xml, or a preview
        from TerasTitcher.
        
        It must contains the string "_Tile"
        '''

        if '_Tile' in file_list[ind1]:
            ext = pathlib.Path(file_list[ind1]).suffixes[-1]


            # If the file extension is .txt, the file is simply copy pasted in the folder MetaDataMesoSPIM
            if ext in '.txt':
                if isMetaDataFolderCreated is False:
                    target_path_meta = os.path.join(target_path, "MetaDataMesoSPIM")
                    #target_path_meta = target_path
                    os.mkdir(target_path_meta)
                    isMetaDataFolderCreated = True

                source = os.path.join(base_path, file_list[ind1])
                destination = os.path.join(target_path_meta, file_list[ind1])
                shutil.copy2(source, destination)

            # If the file extension is .tiff, the file is converted into an 3-D array, split into 2-D arrays, which are then saved as 2D-tifs
            if ext in '.tiff':

                is_substack = False
                temp_name = file_list[ind1]

                im = io.imread(os.path.join(base_path, temp_name))

                dims = np.array(im.shape)

                vector = np.array([0, dims[0], 0, dims[1], 0, dims[2]])

                unique_dims = np.unique(dims)
                mini = np.inf

                '''
                finds the z-axis, by looking at the shape, and finding which of the 3 dimensions is different then the others.
                '''
                for ind_dim in range(len(unique_dims)):
                    if (dims == unique_dims[ind_dim]).sum() < mini:
                        mini = (dims == unique_dims[ind_dim]).sum()
                        ind_mini = ind_dim

                value_mini = unique_dims[ind_mini]
                ind_mini = np.where(dims == unique_dims[ind_mini])
                '''
                Loops over the z-axis and extract each individual slice.
                '''

                temp_name = temp_name[0:-(len(ext))]
                temp_path_tif_2D = os.path.join(target_path, temp_name)
                os.mkdir(temp_path_tif_2D)

                sizeNumForZeroFill = len(str(value_mini))

                for ind_z in range(value_mini):
                    vector[ind_mini[0]*2] = ind_z
                    vector[ind_mini[0]*2 + 1] = ind_z+1
                    temp_im = np.squeeze(im[vector[0]:vector[1], vector[2]:vector[3], vector[4]:vector[5]])
                    temp_im = Image.fromarray(temp_im)

                    tempSliceNum = str(ind_z + 1)
                    tempSliceNum = tempSliceNum.zfill(sizeNumForZeroFill)
                    temp_name_current_slice = temp_name + '_slice_' + tempSliceNum + '.tif'
                    temp_im.save(os.path.join(temp_path_tif_2D, temp_name_current_slice))


class MyData:
    '''
    This is the parent class, from which a child class for each microscope will inherit.
    '''
    def __init__(self, path, current_chan):
        # Most of the attributes are initialized in the different children classes
        '''
        :param path: The input path corresponding to the path of the folder of the acquisition when it is dragged and
        dropped when opening

        :param current_chan: For multichannel acquisitions, this corresponds to the channel that will / is displayed in napari.
        It is set to 0, unless when the object is created when the channel is changed in the plugin GUI, where it will
        be the selected channel number instead.
        '''

        self.base_path = path
        self.type_microscope = 'NaN'
        self.dir_tiles_path = 'NaN'
        self.subpath = 'NaN'
        self.name_for_xml = 'NaN'
        self.type_display = 'standard'

        self.partial_tiling = False

        self.list_paths_individual_tiles = []
        self.list_paths_individual_tiles_for_xml = []

        self.n_planes = []

        # DS_factor is currently hard-coded to 1. But it appears throughout the code in case some functionality
        # involving down-sampling will have to be added in the future

        self.DS_factor = 1

        # The channel that is initially shown upon the opening of the importation of the images of the base folder is
        # the first one. This could be changed for the last one for faster inspection if it turns out to be the most
        # informative about the quality of the acquisition.
        self.current_chan = current_chan

        # This is a hard-coded constant that is used to build the information layer
        self.const_shift_border = -0.5

    def display(self):
        '''
        This function is used to display informations about the object itself
        :return:
        '''
        #print("Type of microscope: " + self.type_microscope)
        print("type_microscope = " + self.type_microscope)
        print("subpath = " + self.subpath)
        print("coord_x = " + str(self.coord_x))
        print("coord_y = " + str(self.coord_y))
        print("numbering = " + str(self.numbering))

    def create_numbering(self):
        '''
        The output are 3 vectors that contains the x, and y, coordinates of each tile, and the corresponding number in
        the microscope numbering.
        Example for a 3x3 Clear Scope tiling:
        coord_x = [1, 2, 3, 1, 2, 3, 1, 2, 3]
        coord_y = [1, 1, 1, 2, 2, 2, 3, 4, 3]
        numbering = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        Example for a 3x3 Clear Scope tiling:
        coord_x = [1, 2, 3, 1, 2, 3, 1, 2, 3]
        coord_y = [1, 1, 1, 2, 2, 2, 3, 4, 3]
        numbering = [1, 2, 3, 6, 5, 4, 7, 8, 9]

        :return:
        '''
        coord_x = np.tile(np.arange(1, self.dim_x + 1), self.dim_y)
        coord_y = np.repeat(np.arange(1, self.dim_y + 1), self.dim_x)
        numbering = self._convert_coord_xy_to_microscope(coord_x, coord_y)

        return numbering, coord_x, coord_y

    def create_info_layer(self):
        '''
        This create a shape layer that will be displayed in the napari viewer that contains the [y, x] coordinates of each
        tiles in white text, and a square white box that delimits the portion of each tile that is not overlapping with
        any neighboring tiles.

        :return: a layer object that is passed to the napari viever
        '''


        color_display ='white'
        box = []
        label_boxes = []
        edge_color_boxes = []

        border_to_crop_x = int(np.around((self.size_tile - self.size_tile_no_overlap_x) // self.DS_factor))
        border_to_crop_y = int(np.around((self.size_tile - self.size_tile_no_overlap_y) // self.DS_factor))

        for ind in range(len(self.numbering)):

            ind_x = self.coord_x[ind]
            ind_y = self.coord_y[ind]

            y_0 = (ind_y - 1) * self.size_tile_no_overlap_y // self.DS_factor + border_to_crop_y * (self.const_shift_border + 1)
            x_0 = (ind_x - 1) * self.size_tile_no_overlap_x // self.DS_factor + border_to_crop_x * (self.const_shift_border + 1)

            y_1 = y_0 + self.size_tile_no_overlap_y // self.DS_factor + border_to_crop_y * (self.const_shift_border - 0.5)
            x_1 = x_0 + self.size_tile_no_overlap_x // self.DS_factor + border_to_crop_x * (self.const_shift_border - 0.5)

            box.append(np.array([[y_0, x_0], [y_0, x_1], [y_1, x_1], [y_1, x_0]]))
            label_boxes.append('')
            edge_color_boxes.append(color_display)

            y_0 = (ind_y - 2) * self.size_tile_no_overlap_y // self.DS_factor + border_to_crop_y * (self.const_shift_border + 2)
            x_0 = (ind_x - 1) * self.size_tile_no_overlap_x // self.DS_factor + border_to_crop_x * (self.const_shift_border + 1)
            y_1 = y_0 + self.size_tile_no_overlap_y // self.DS_factor + border_to_crop_y * (self.const_shift_border - 0.5)
            x_1 = x_0 + self.size_tile_no_overlap_x // self.DS_factor + border_to_crop_x * (self.const_shift_border - 0.5)

            box.append(np.array([[y_0, x_0], [y_0, x_1], [y_1, x_1], [y_1, x_0]]))

            temp_name = '[' + str(ind_y) + ', ' + str(ind_x) + ']'

            label_boxes.append(temp_name)
            edge_color_boxes.append('transparent')

        properties = {
            'label': label_boxes,
        }
        edge_width = 5
        text_parameters = {
            'text': 'label',
            'size': 14,
            'color': color_display,
            'anchor': 'lower_left',
            'translation': [1.5 * edge_width, 1.5 * edge_width],
        }
        shapes_layer = (
            box,
            {'face_color': 'transparent', 'edge_color': edge_color_boxes, 'edge_width': edge_width,
             'properties': properties, 'text': text_parameters, 'name': 'bounding box'},
            'shapes',
        )

        return shapes_layer

    def _determine_tile_display_param(self, x, y):
        if self.type_display == 'standard':
            colormap = 'gray'
            blending = 'translucent'
        else:
            # currently all the non-gray displaying mode use the same methods, where the checker board is the defaul
            # if a different displaying mode is added one must take this into account
            blending = 'additive'


            f_x = 1
            f_y = 1

            # To alternate between rows, the current x position must have no influence, so f_x is set to zero
            if self.type_display == "row":
                f_x = 0

            if self.type_display == "column":
                f_y = 0

            test_checkerboard = np.power(-1, y * f_y + x * f_x)

            if test_checkerboard > 0:
                colormap = 'red'
            else:
                colormap = 'green'

        return colormap, blending

    def create_image_layer(self):
        '''
        This function creates the image layer, that will passed into the napari viewer.
        :return:
        '''
        my_layer_list = []

        #This dictionary contains the metadata of the tile.
        base_dict = {
            "n_planes": self.n_planes,
            "dim_x": self.dim_x,
            "dim_y": self.dim_y,
            "size_tile": self.size_tile,
            "size_tile_no_overlap_x": self.size_tile_no_overlap_x,
            "size_tile_no_overlap_y": self.size_tile_no_overlap_y,
            "path": self.base_path,
            "type_microscope": self.type_microscope,
            'is_small_tile': False,
            'x_coord': np.NaN,
            'y_coord': np.NaN,
            'DS_factor': self.DS_factor,
            'current_chan': self.current_chan,
            'n_chans': self.n_chans,
            'channel_values': self.channel_values,
        }

        border_to_crop_x = int(np.around((self.size_tile - self.size_tile_no_overlap_x) // self.DS_factor))
        border_to_crop_y = int(np.around((self.size_tile - self.size_tile_no_overlap_y) // self.DS_factor))

        for ind in range(len(self.numbering)):

            ind_x = self.coord_x[ind]
            ind_y = self.coord_y[ind]

            #temp_path_stack = path_meta.format(path_filling[self.order_path_format[0]], path_filling[self.order_path_format[1]])
            temp_path_stack = self.list_paths_individual_tiles[ind]

            stack = dask_image.imread.imread(temp_path_stack)

            # Downsample
            if self.DS_factor > 1:
                stack = stack[:, ::self.DS_factor, ::self.DS_factor]

            y_offset = (ind_y - 1) * self.size_tile_no_overlap_y // self.DS_factor
            x_offset = (ind_x - 1) * self.size_tile_no_overlap_x // self.DS_factor

            temp_name = '[' + str(ind_y) + ', ' + str(ind_x) + ']'

            # Meta data exclusive to the current tile are added to dictionary
            temp_dict = base_dict.copy()
            temp_dict['is_small_tile'] = True
            temp_dict['y_coord'] = ind_y
            temp_dict['x_coord'] = ind_x
            temp_dict['tile_microscope_number'] = self.numbering[ind]
            temp_dict['path_individual_tiles'] = self.list_paths_individual_tiles[ind]
            temp_dict['path_individual_tiles_for_xml'] = self.list_paths_individual_tiles_for_xml[ind]
            temp_dict['data_acquisition'] = self

            temp_colormap, temp_blending = self._determine_tile_display_param(ind_x, ind_y)
            my_layer_list.append((stack, {'colormap': temp_colormap, 'blending': temp_blending, 'translate': (border_to_crop_y * self.const_shift_border + y_offset, border_to_crop_x * self.const_shift_border + x_offset), 'contrast_limits': [0, 5000], 'multiscale': False, 'name': temp_name, 'metadata': temp_dict}))

        return my_layer_list

    def reset_ROI(self):
        '''
        When creating and xml of only a partial portion of the tiling, this ROI is changed in order to include
        information only about tiles in this ROI in the xml.
        This function resets the ROI to the whole timimng after the creation of a partial xml file.
        :return:
        '''
        self.range_x_ROI_for_xml = np.array([1, self.dim_x])
        self.range_y_ROI_for_xml = np.array([1, self.dim_y])


class MyClearScopeData(MyData):

    def __init__(self, path, current_chan):

        super().__init__(path, current_chan)

        # The following two string are used when creating the xml. They can defere depending on the type of data
        self.volumeFormat = "TiledXY|2Dseries"
        self.typeFile = "tiff2D"

        # This is the path where the folders containing the images are stored.
        self.dir_tiles_path = self.base_path
        self.n_planes, self.dim_x, self.dim_y, self.size_tile, self.size_tile_no_overlap_x, self.size_tile_no_overlap_y, self.n_chans, self.channel_values = self._get_meta_data()

        self.sign_x = 1
        self.sign_y = -1

        self.numbering, self.coord_x, self.coord_y = self.create_numbering()

        self.range_x_ROI_for_xml = np.array([1, self.dim_x])
        self.range_y_ROI_for_xml = np.array([1, self.dim_y])

        self.type_microscope = "Clear Scope"

        self.subpath = os.path.join('000000_{}___{}c', "*.tif")
        self.name_for_xml = ".*.*{}c*.tif"
        self.create_list_paths_individual_tiles()

    def _get_meta_data(self):
        """
        Returns the meta data
        """
        # Extract the meta data from the AssemblyData text file
        path_text = os.path.join(self.base_path, "AssemblyData.txt")
        meta_data_values = get_num_values_text(path_text,
                                               ["NumberOfPlanes", "GridX", "GridY ", "TileResolutionX ",
                                                "TileActualSizeX"])
        n_planes = int(meta_data_values[0])
        dim_x = int(meta_data_values[1])
        dim_y = int(meta_data_values[2])
        size_tile = int(meta_data_values[3])
        size_tile_no_overlap = int(meta_data_values[4])
        size_tile_no_overlap_x = int(size_tile_no_overlap)
        size_tile_no_overlap_y = int(size_tile_no_overlap)

        n_chans = 0
        for name_file in os.listdir(self.base_path):
            if os.path.isdir(os.path.join(self.base_path, name_file)) and name_file[-5:-2] + name_file[-1] == '___c':
                n_chans = np.maximum(n_chans, int(name_file[-2]))
        n_chans = n_chans + 1
        channel_values = np.arange(n_chans)
        return n_planes, dim_x, dim_y, size_tile, size_tile_no_overlap_x, size_tile_no_overlap_y, n_chans, channel_values

    def _create_list_dir_single_tiles(self):
        list_dir = []

    def _convert_coord_xy_to_microscope(self, coord_x, coord_y):
        coord_x = np.array(coord_x)
        coord_y = np.array(coord_y)

        if self.sign_x == -1:
            coord_x = np.flipud(coord_x)

        if self.sign_y == -1:
            coord_y = np.flipud(coord_y)

        p_min_one = np.power(-1, coord_y)

        coord_microscope = self.dim_x * (coord_y + (p_min_one - 1) / 2) - coord_x * p_min_one + (p_min_one + 1) / 2
        coord_microscope = coord_microscope.astype(int)

        return coord_microscope

    def _convert_coord_microscope_to_xy(self, coord_microscope):
        coord_microscope = np.array(coord_microscope)

        coord_x = np.absolute(np.mod(coord_microscope - self.dim_x - 1, 2 * self.dim_x) - self.dim_x + 0.5) + 0.5
        coord_y = np.ceil(coord_microscope / self.dim_x)

        coord_x = coord_x.astype(int)
        coord_y = coord_y.astype(int)

        return coord_x, coord_y

    def create_list_paths_individual_tiles(self):
        self.list_paths_individual_tiles = []
        self.list_paths_individual_tiles_for_xml = []

        for ind in range(len(self.numbering)):
            path_meta = os.path.join(self.dir_tiles_path, self.subpath)
            temp_path_stack = path_meta.format(str(int(self.numbering[ind])).zfill(6), self.channel_values[self.current_chan])

            self.list_paths_individual_tiles.append(temp_path_stack)
            self.list_paths_individual_tiles_for_xml.append(self.name_for_xml.format(str(self.channel_values[self.current_chan])))

    def create_xml(self):
        ref_sys = np.array([1, 2, 3])
        voxel_dim = np.array([1, 1, 1])

        # First creates the base of the xml, that is the same no matter if the xml is based on whole tiling or only partial tiling
        ET.Element("!DOCTYPE TeraStitcher SYSTEM 'TeraStitcher.DDT'")

        root = ET.Element("TeraStitcher", volume_format=self.volumeFormat, input_plugin=self.typeFile)

        sub_element_branch_1_1 = ET.SubElement(root, "stacks_dir ", value=self.dir_tiles_path)
        sub_element_branch_1_2 = ET.SubElement(root, "ref_sys", ref1=str(ref_sys[0]), ref2=str(ref_sys[1]),
                                               ref3=str(ref_sys[2]))
        sub_element_branch_1_3 = ET.SubElement(root, "voxel_dims", V=str(voxel_dim[0]), H=str(voxel_dim[1]),
                                               D=str(voxel_dim[2]))
        sub_element_branch_1_4 = ET.SubElement(root, "origin", V=str(0), H=str(0), D=str(0))
        sub_element_branch_1_5 = ET.SubElement(root, "mechanical_displacements",
                                               V=str(self.size_tile_no_overlap_y),
                                               H=str(self.size_tile_no_overlap_x))
        sub_element_branch_1_6 = ET.SubElement(root, "dimensions",
                                               stack_rows=str(self.range_y_ROI_for_xml[1] - self.range_y_ROI_for_xml[0] + 1),
                                               stack_columns=str(self.range_x_ROI_for_xml[1] - self.range_x_ROI_for_xml[0] + 1),
                                               stack_slices=str(self.n_planes))
        stacks = ET.SubElement(root, "STACKS")

        # bool vector that stores the tiles that are part of the selected ROI out of the whole tiling
        bool_ROI = np.logical_and(np.logical_and(self.coord_x >= self.range_x_ROI_for_xml[0],
                                                 self.coord_x <= self.range_x_ROI_for_xml[1]),
                                  np.logical_and(self.coord_y >= self.range_y_ROI_for_xml[0],
                                                 self.coord_y <= self.range_y_ROI_for_xml[1]))

        for ind in range(len(self.numbering)):

            ind_x = self.coord_x[ind]
            ind_y = self.coord_y[ind]


            if bool(bool_ROI[ind]) is True:

                temp_path_stack = self.list_paths_individual_tiles[ind]

                files = glob.glob(os.path.dirname(temp_path_stack))
                name_IMG_REGEX_for_xml = self.list_paths_individual_tiles_for_xml[ind]

                str_Z_RANGES = "[" + str(0) + "," + str(self.n_planes) + ")"

                stack = ET.SubElement(stacks, "Stack", N_CHANS="1", N_BYTESxCHAN="2", ROW=str(ind_y - 1),
                                      COL=str(ind_x - 1),
                                      ABS_V=str((ind_y - 1) * self.size_tile_no_overlap_y),
                                      ABS_H=str((ind_x - 1) * self.size_tile_no_overlap_x),
                                      ABS_D="0", STITCHABLE="no", DIR_NAME=os.path.basename(files[0]),
                                      _RANGES=str_Z_RANGES, IMG_REGEX=name_IMG_REGEX_for_xml)

                sub_element_branch_3_1 = ET.SubElement(stack, "NORTH_displacements")
                sub_element_branch_3_2 = ET.SubElement(stack, "EAST_displacements")
                sub_element_branch_3_3 = ET.SubElement(stack, "SOUTH_displacements ")
                sub_element_branch_3_4 = ET.SubElement(stack, "WEST_displacements ")

        tree = ET.ElementTree(root)

        ROOT = Tk()
        ROOT.withdraw()
        target_path_xml = filedialog.askdirectory()

        ROOT = Tk()
        ROOT.withdraw()
        name_xml = simpledialog.askstring(title="Input window", prompt="Name of the xml file:")
        wd = os.getcwd()
        #tree.write(name_xml + ".xml")
        current_path_xml = os.path.join(wd, name_xml + ".xml")
        target_path_xml = os.path.join(target_path_xml, name_xml + ".xml")
        tree.write(target_path_xml)
        #shutil.move(current_path_xml, target_path_xml)
        #Path(current_path_xml).rename(target_path_xml)
        #os.replace(current_path_xml, target_path_xml)


class MyColmData(MyData):

    def __init__(self, path, current_chan):

        super().__init__(path, current_chan)

        self.volumeFormat = "TiledXY|2Dseries"
        self.typeFile = "tiff2D"

        self.dir_tiles_path = os.path.join(self.base_path, "VW0")
        self.n_planes, self.dim_x, self.dim_y, self.size_tile, self.size_tile_no_overlap_x, self.size_tile_no_overlap_y, self.n_chans, self.channel_values = self._get_meta_data()

        self.sign_x = 1
        self.sign_y = 1

        self.numbering, self.coord_x, self.coord_y = self.create_numbering()

        self.range_x_ROI_for_xml = np.array([1, self.dim_x])
        self.range_y_ROI_for_xml = np.array([1, self.dim_y])

        self.type_microscope = "COLM"

        self.subpath = os.path.join("LOC{}", "*_CH*{}_*.tif")
        self.name_for_xml = ".*_CHN{}_PLN.*.tif"

        self.create_list_paths_individual_tiles()

    def _get_meta_data(self):
        """
        Returns the meta data
        """
        path_text = os.path.join(self.base_path, "Experiment.ini")

        # Looks the number of files in the first directory, and divide it by the number of channels to find n_planes

        temp_path = os.path.join(self.dir_tiles_path, "LOC000")

        file_list = sorted(listdir(temp_path))
        n_files = len(file_list)
        last_file_name = file_list[-1]

        target = "CHN"
        n = last_file_name.find(target) + len(target)
        n_chans = int(last_file_name[n:n + 2]) + 1
        n_planes = int(n_files / n_chans)

        #
        temp_path = os.path.join(temp_path, "VW0_LOC000D_CM0_CHN00_PLN0000.tif")
        im = io.imread(temp_path)
        size_tile = im.shape
        size_tile = int(size_tile[0])

        meta_data_values = get_num_values_text(
            path_text,["Horizontal = ", "Vertical = ", "Actual Vertical Overlap", "Actual Horizontal Overlap"])

        dim_x = int(meta_data_values[0])
        dim_y = int(meta_data_values[1])
        overlap_y = meta_data_values[2]
        overlap_x = meta_data_values[3]

        size_tile_no_overlap_x = size_tile * (100 - overlap_x) / 100
        size_tile_no_overlap_y = size_tile * (100 - overlap_y) / 100
        channel_values = np.arange(n_chans)
        return n_planes, dim_x, dim_y, size_tile, size_tile_no_overlap_x, size_tile_no_overlap_y, n_chans, channel_values

    def _convert_coord_xy_to_microscope(self, coord_x, coord_y):
        '''
        :param coord_x: x coordinate of a given tile
        :param coord_y: y coordinate of a given tile
        :return: the (x,y) coordinate pair converted to the microscope numering
        '''
        coord_x = np.array(coord_x)
        coord_y = np.array(coord_y)

        if self.sign_x == -1:
            coord_x = np.flipud(coord_x)

        if self.sign_y == -1:
            coord_y = np.flipud(coord_y)

        coord_microscope = self.dim_x * (coord_y - 1) + coord_x - 1
        coord_microscope = coord_microscope.astype(int)
        return coord_microscope

    def _convert_coord_microscope_to_xy(self, coord_microscope):
        '''
        This function converts a given tile number expressed in the microscope numbering convention in its corresponding
        x and y coordinates loctaion in the acquisition tiling. This function is different for each microscope.
        :param coord_microscope:
        :return: x and y coordinates
        '''
        coord_microscope = np.array(coord_microscope)

        coord_x = np.mod(coord_microscope - 1, self.dim_x) + 1
        coord_y = np.ceil(coord_microscope / self.dim_x)

        coord_x = coord_x.astype(int)
        coord_y = coord_y.astype(int)

        return coord_x, coord_y

    def create_list_paths_individual_tiles(self):
        '''
        This function creates two list of paths equal to the number of tiles in the tiling. The first one is used to
        locate the folders from where to load the images in the napari viewer.
        The second is during the xml, and its component are used as fields in the xml.
        :return:
        '''
        self.list_paths_individual_tiles = []
        self.list_paths_individual_tiles_for_xml = []

        for ind in range(len(self.numbering)):
            path_meta = os.path.join(self.dir_tiles_path, self.subpath)
            temp_path_stack = path_meta.format(str(int(self.numbering[ind])).zfill(3), self.channel_values[self.current_chan])

            self.list_paths_individual_tiles.append(temp_path_stack)
            self.list_paths_individual_tiles_for_xml.append(self.name_for_xml.format(str(self.channel_values[self.current_chan]).zfill(2)))

    def create_xml(self):

        ref_sys = np.array([1, 2, 3])
        voxel_dim = np.array([1, 1, 1])

        # First creates the base of the xml, that is the same no matter if the xml is based on whole tiling or only partial tiling
        ET.Element("!DOCTYPE TeraStitcher SYSTEM 'TeraStitcher.DDT'")

        root = ET.Element("TeraStitcher", volume_format=self.volumeFormat, input_plugin=self.typeFile)

        sub_element_branch_1_1 = ET.SubElement(root, "stacks_dir ", value=self.dir_tiles_path)
        sub_element_branch_1_2 = ET.SubElement(root, "ref_sys", ref1=str(ref_sys[0]), ref2=str(ref_sys[1]),
                                               ref3=str(ref_sys[2]))
        sub_element_branch_1_3 = ET.SubElement(root, "voxel_dims", V=str(voxel_dim[0]), H=str(voxel_dim[1]),
                                               D=str(voxel_dim[2]))
        sub_element_branch_1_4 = ET.SubElement(root, "origin", V=str(0), H=str(0), D=str(0))
        sub_element_branch_1_5 = ET.SubElement(root, "mechanical_displacements",
                                               V=str(int(self.size_tile_no_overlap_y)),
                                               H=str(int(self.size_tile_no_overlap_x)))
        sub_element_branch_1_6 = ET.SubElement(root, "dimensions",
                                               stack_rows=str(self.range_y_ROI_for_xml[1] - self.range_y_ROI_for_xml[0] + 1),
                                               stack_columns=str(self.range_x_ROI_for_xml[1] - self.range_x_ROI_for_xml[0] + 1),
                                               stack_slices=str(self.n_planes))
        stacks = ET.SubElement(root, "STACKS")

        '''
        bool vector that stores the tiles that are part of the selected ROI out of the whole tiling. By default is 
        equal to the tiling dimension, but it can be smaller when creating a partial xml.
        '''
        bool_ROI = np.logical_and(np.logical_and(self.coord_x >= self.range_x_ROI_for_xml[0],
                                                 self.coord_x <= self.range_x_ROI_for_xml[1]),
                                  np.logical_and(self.coord_y >= self.range_y_ROI_for_xml[0],
                                                 self.coord_y <= self.range_y_ROI_for_xml[1]))
        # Loops over all the tiles in the tiling
        for ind in range(len(self.numbering)):

            ind_x = self.coord_x[ind]
            ind_y = self.coord_y[ind]

            # test if the tile is inside the ROI
            if bool(bool_ROI[ind]) is True:

                temp_path_stack = self.list_paths_individual_tiles[ind]

                files = glob.glob(os.path.dirname(temp_path_stack))
                name_IMG_REGEX_for_xml = self.list_paths_individual_tiles_for_xml[ind]

                str_Z_RANGES = "[" + str(0) + "," + str(self.n_planes) + ")"

                stack = ET.SubElement(stacks, "Stack", N_CHANS="1", N_BYTESxCHAN="2", ROW=str(ind_y - 1),
                                      COL=str(ind_x - 1),
                                      ABS_V=str(int((ind_y - 1) * self.size_tile_no_overlap_y)),
                                      ABS_H=str(int((ind_x - 1) * self.size_tile_no_overlap_x)),
                                      ABS_D="0", STITCHABLE="no", DIR_NAME=os.path.basename(files[0]),
                                      _RANGES=str_Z_RANGES, IMG_REGEX=name_IMG_REGEX_for_xml)

                sub_element_branch_3_1 = ET.SubElement(stack, "NORTH_displacements")
                sub_element_branch_3_2 = ET.SubElement(stack, "EAST_displacements")
                sub_element_branch_3_3 = ET.SubElement(stack, "SOUTH_displacements ")
                sub_element_branch_3_4 = ET.SubElement(stack, "WEST_displacements ")

        tree = ET.ElementTree(root)

        ROOT = Tk()
        ROOT.withdraw()
        target_path_xml = filedialog.askdirectory()

        ROOT = Tk()
        ROOT.withdraw()
        name_xml = simpledialog.askstring(title="Input window", prompt="Name of the xml file:")
        wd = os.getcwd()
        #tree.write(name_xml + ".xml")
        current_path_xml = os.path.join(wd, name_xml + ".xml")
        target_path_xml = os.path.join(target_path_xml, name_xml + ".xml")
        tree.write(target_path_xml)
        #shutil.move(current_path_xml, target_path_xml)
        #Path(current_path_xml).rename(target_path_xml)
        #os.replace(current_path_xml, target_path_xml)


class MyMesoSpimDataParentClass(MyData):

    def __init__(self, path, current_chan):

        super().__init__(path, current_chan)

        self.dir_tiles_path = self.base_path

    def _get_meta_data(self):
        """
        Returns the meta data
        """
        path_text = self.path_meta_data

        file_list = sorted(listdir(self.path_meta_data))

        size_loop1 = len(file_list)
        count = 0
        x_pos = []
        y_pos = []

        temp_path_meta_tile = '_Tile{}_'

        for ind1 in range(size_loop1):

            if '_Tile' in file_list[ind1]:
                count = count + 1
                size_loop2 = len(re.findall('[0-9]+', file_list[ind1]))

            # Extracts each pairs of x/y coordinates of each tile from the meta data
            if 'meta' in file_list[ind1]:
                meta_data = get_num_values_text(os.path.join(path_text, file_list[ind1]), ["[x_pos]", "[y_pos]"])
                x_pos.append(meta_data[0])
                y_pos.append(meta_data[1])
            # get the path of the first tile, by checking that the name of the file contains "_Tile0_" and "meta"
            if temp_path_meta_tile.format(0) in file_list[ind1] and 'meta' in file_list[ind1]:
                path_first_tile = file_list[ind1]

        # Gets the pixel size and the number of planes from the meta data of the first tile.
        pixel_size = get_num_values_text2(os.path.join(path_text, path_first_tile), [8])
        pixel_size = pixel_size[0]

        n_planes = get_num_values_text2(os.path.join(path_text, path_first_tile), [2])
        n_planes = int(n_planes[0])

        x_pos = np.asarray(x_pos)
        y_pos = np.asarray(y_pos)

        x_pos = sorted(np.unique(x_pos))
        y_pos = sorted(np.unique(y_pos))

        print("x_pos")
        print(x_pos)

        print("y_pos")
        print(y_pos)

        dim_x = len(x_pos)
        dim_y = len(y_pos)

        dim_tiling = dim_x * dim_y

        print("---------------------------------------------")
        print("dim_x")
        print(dim_x)

        print("dim_y")
        print(dim_y)
        print("---------------------------------------------")


        size_tile = 2048

        if dim_x == 1:
            size_tile_no_overlap_x = size_tile
        else:
            delta_x = x_pos[1] - x_pos[0]
            size_tile_no_overlap_x = round(delta_x / pixel_size)

        if dim_y == 1:
            size_tile_no_overlap_y = size_tile
        else:
            delta_y = y_pos[1] - y_pos[0]
            size_tile_no_overlap_y = round(delta_y / pixel_size)

        temp_num = np.zeros((count, size_loop2))

        # The meta data are extracted from the number in the name of the files in the self.base_path
        count = 0
        for ind1 in range(size_loop1):
            if '_Tile' in file_list[ind1]:
                temp = re.findall('[0-9]+', file_list[ind1])
                for ind2 in range(size_loop2):
                    temp_num[count, ind2] = int(temp[ind2])
                count = count + 1

        unique_num_values = np.zeros(size_loop2)
        for ind2 in range(size_loop2):
            unique_num_values[ind2] = int(len(np.unique(temp_num[:, ind2])))

        n_tiles = unique_num_values[-3]
        n_tiles = n_tiles.astype(int)

        channel_values = np.unique(temp_num[:, -2])
        channel_values = channel_values.astype(int)

        n_chans = unique_num_values[-2]
        n_chans = n_chans.astype(int)

        return n_planes, dim_x, dim_y, size_tile, size_tile_no_overlap_x, size_tile_no_overlap_y, n_chans, channel_values

    def _convert_coord_xy_to_microscope(self, coord_x, coord_y):
        coord_x = np.array(coord_x)
        coord_y = np.array(coord_y)
        coord_y = np.flipud(coord_y)

        if self.sign_x == -1:
            coord_x = np.flipud(coord_x)

        if self.sign_y == -1:
            coord_y = np.flipud(coord_y)

        #coord_microscope = self.dim_x * (coord_y - 1) + coord_x - 1
        coord_microscope = self.dim_y * (coord_x - 1) + coord_y - 1

        coord_microscope = coord_microscope.astype(int)

        return coord_microscope

    def _convert_coord_microscope_to_xy(self, coord_microscope):
        coord_microscope = np.array(coord_microscope)

        coord_x = np.ceil(coord_microscope / self.dim_y)
        coord_y = np.mod(coord_microscope - 1, self.dim_y) + 1

        coord_x = coord_x.astype(int)
        coord_y = coord_y.astype(int)

        return coord_x, coord_y


class MyMesoSpimData_3D(MyMesoSpimDataParentClass):

    def __init__(self, path, current_chan):

        super().__init__(path, current_chan)
        self.volumeFormat = "TiledXY|3Dseries"
        self.typeFile = "tiff3D"

        self.path_meta_data = self.base_path

        self.n_planes, self.dim_x, self.dim_y, self.size_tile, self.size_tile_no_overlap_x, self.size_tile_no_overlap_y, self.n_chans, self.channel_values = self._get_meta_data()

        self.sign_x = 1
        self.sign_y = -1


        self.numbering, self.coord_x, self.coord_y = self.create_numbering()

        #self.coord_y = np.flipud(self.coord_y)

        self.type_microscope = "MesoSPIM_3D"

        self.range_x_ROI_for_xml = np.array([1, self.dim_x])
        self.range_y_ROI_for_xml = np.array([1, self.dim_y])

        self._get_type_tiff()

        self.subpath = "*_Tile{}_Ch{}_Sh0" + self.type_tif
        self.name_for_xml = ".*_Tile{}_Ch{}_Sh0" + self.type_tif

        self.create_list_paths_individual_tiles()

    def create_list_paths_individual_tiles(self):
        self.list_paths_individual_tiles = []
        self.list_paths_individual_tiles_for_xml = []

        for ind in range(len(self.numbering)):
            path_meta = os.path.join(self.dir_tiles_path, self.subpath)
            temp_path_stack = path_meta.format(int(self.numbering[ind]), self.channel_values[self.current_chan])

            self.list_paths_individual_tiles.append(temp_path_stack)
            self.list_paths_individual_tiles_for_xml.append(self.name_for_xml.format(int(self.numbering[ind]), self.channel_values[self.current_chan]))

    def create_xml(self):
        event, values = sg.Window('Warning message',
                                  [[sg.Text('Creating an xml first requires the conversion of tiff 3D to tiff 2D.'
                                            'This operation may request a lot of time and memory, do you confirm you want to carry on?')],
                                   [sg.Button('Confirm'), sg.Button('Cancel')]]).read(close=True)
        if event == 'Confirm':

            ROOT = Tk()
            ROOT.withdraw()
            name_folder_tiff2D = simpledialog.askstring(title="Input window",
                                                        prompt="Name of the new folder were you want to store the tiff 2D files")

            ROOT = Tk()
            ROOT.withdraw()
            target_path_folder_tiff2D = filedialog.askdirectory(title="Where do you want to put the new folder?")

            path_tiff2D = os.path.join(target_path_folder_tiff2D, name_folder_tiff2D)
            os.mkdir(path_tiff2D)

            target_path_meta = os.path.join(path_tiff2D, "MetaDataMesoSPIM")
            # target_path_meta = target_path
            os.mkdir(target_path_meta)

            for ind_chans in range(self.n_chans):

                data_acquisition = MyMesoSpimData_3D(self.base_path, ind_chans)
                my_layer_list = data_acquisition.create_image_layer()
                for ind_tile in range(len(my_layer_list)):

                    im = my_layer_list[ind_tile][0]
                    shape_im = np.shape(im)

                    temp_name = my_layer_list[ind_tile][1]['metadata']['name_tile']
                    ext = pathlib.Path(temp_name).suffixes[-1]
                    name_tile_tif_2D = temp_name[0:-len(ext) + 1]

                    ind_str = name_tile_tif_2D.find("_Sh")
                    name_tile_tif_2D = name_tile_tif_2D[0:ind_str - 2] + name_tile_tif_2D[ind_str: -1]

                    temp_path_tile_tif_2D = os.path.join(path_tiff2D, name_tile_tif_2D)
                    os.mkdir(temp_path_tile_tif_2D)
                    # --------------------------------------------------------------------------------------------------------------------------
                    # Add code here to save the tiff in the new folder

                    sizeNumForZeroFill = len(str(shape_im[0]))

                    # for ind_z in range(shape_im[0]):

                    n_slice = shape_im[0]
                    '''
                    a = int(np.round(n_slice/2))-5
                    b = int(np.round(n_slice/2))+5

                    n_slice = b-a
                    '''

                    for ind_z in range(n_slice):
                        # for ind_z in range(a, b, 1):
                        temp_im = np.asarray(np.squeeze(im[ind_z, :, :]))
                        temp_im = Image.fromarray(temp_im)

                        tempSliceNum = str(ind_z + 1)
                        tempSliceNum = tempSliceNum.zfill(sizeNumForZeroFill)

                        temp_name_current_slice = name_tile_tif_2D + '_slice_' + tempSliceNum + '.tif'
                        temp_im.save(os.path.join(temp_path_tile_tif_2D, temp_name_current_slice))
                    # --------------------------------------------------------------------------------------------------------------------------

                    temp_name_meta = temp_name + "_meta.txt"

                    # ind_str = temp_name_meta.find("_Sh")
                    source = os.path.join(self.base_path, temp_name_meta)
                    destination_meta = temp_name_meta
                    ind_str = destination_meta.find("_Sh")
                    destination_meta = destination_meta[0:ind_str - 2] + destination_meta[ind_str: -1] + 't'
                    destination_meta = os.path.join(target_path_meta, destination_meta)

                    shutil.copy2(source, destination_meta)

                    target_values_string = "[z_planes] "
                    with open(destination_meta) as f:
                        lines = f.readlines()

                    # loops over all the lines of the text files, for each of them, check if the strings in target_values_string are present
                    for ind1 in range(len(lines)):
                        string_test = lines[ind1]

                        # the target string has to be smaller than the line of text (string_test variable) that contains it
                        if len(target_values_string) < len(string_test):

                            # if the string_target is present in the line of text, the number present in the line is extracted and saved
                            # (This works since there is a single number per line of meta data text)
                            if target_values_string in string_test:
                                text_to_replaced_old = string_test
                                text_to_replaced_new = target_values_string + str(n_slice) + '\n'

                                f = open(destination_meta, 'r')
                                filedata = f.read()
                                f.close()

                                newdata = filedata.replace(text_to_replaced_old, text_to_replaced_new)

                                f = open(destination_meta, 'w')
                                f.write(newdata)
                                f.close()

            # convert_tiff_images_from_3D_to_2D(self.base_path, path_tiff2D)

            sg.popup(f'Convertion from tiff3D to tiff 2D completed!')
            data_acquisition = MyMesoSpimData_2D(path_tiff2D, self.current_chan)
            data_acquisition.sign_x = copy.copy(self.sign_x)
            data_acquisition.sign_y = copy.copy(self.sign_y)
            data_acquisition.numbering, data_acquisition.coord_x, data_acquisition.coord_y = data_acquisition.create_numbering()
            data_acquisition.create_list_paths_individual_tiles()
            data_acquisition.create_xml()

            self.base_path = MyMesoSpimData_2D

            return data_acquisition

    def create_image_layer(self):
        my_layer_list = []

        base_dict = {
            "n_planes": self.n_planes,
            "dim_x": self.dim_x,
            "dim_y": self.dim_y,
            "size_tile": self.size_tile,
            "size_tile_no_overlap_x": self.size_tile_no_overlap_x,
            "size_tile_no_overlap_y": self.size_tile_no_overlap_y,
            "path": self.base_path,
            "type_microscope": self.type_microscope,
            'is_small_tile': False,
            'x_coord': np.NaN,
            'y_coord': np.NaN,
            'DS_factor': self.DS_factor,
            'current_chan': self.current_chan,
            'n_chans': self.n_chans,
            'channel_values': self.channel_values,

        }

        border_to_crop_x = int(np.around((self.size_tile - self.size_tile_no_overlap_x) // self.DS_factor))
        border_to_crop_y = int(np.around((self.size_tile - self.size_tile_no_overlap_y) // self.DS_factor))

        for ind in range(len(self.numbering)):

            ind_x = self.coord_x[ind]
            ind_y = self.coord_y[ind]

            '''
            path_filling = [str(int(self.numbering[ind])), self.current_chan]
            path_filling[0] = path_filling[0].zfill(self.zero_pad)

            path_meta = os.path.join(self.dir_tiles_path, self.subpath)
            '''
            #temp_path_stack = path_meta.format(path_filling[self.order_path_format[0]], path_filling[self.order_path_format[1]])
            temp_path_stack = self.list_paths_individual_tiles[ind]

            path = glob.glob(temp_path_stack)

            zarr_store = tifffile.imread(path, aszarr = True)
            name_tile = os.path.split(path[0])
            name_tile = str(name_tile[1])

            stack = dask.array.from_zarr(zarr_store)
            list_stacks_all_chans = []

            old_curr_chan = self.current_chan

            # Downsample
            if self.DS_factor > 1:
                stack = stack[:, ::self.DS_factor, ::self.DS_factor]

            y_offset = (ind_y - 1) * self.size_tile_no_overlap_y // self.DS_factor
            x_offset = (ind_x - 1) * self.size_tile_no_overlap_x // self.DS_factor

            temp_name = '[' + str(ind_y) + ', ' + str(ind_x) + ']'

            temp_dict = base_dict.copy()
            temp_dict['is_small_tile'] = True
            temp_dict['y_coord'] = ind_y
            temp_dict['x_coord'] = ind_x
            temp_dict['tile_microscope_number'] = self.numbering[ind]
            temp_dict['path_individual_tiles'] = self.list_paths_individual_tiles[ind]
            temp_dict['path_individual_tiles_for_xml'] = self.list_paths_individual_tiles_for_xml[ind]
            temp_dict['name_tile'] = name_tile

            #temp_dict['order_path_format'] = self.order_path_format

            temp_dict['data_acquisition'] = self

            temp_colormap, temp_blending = self._determine_tile_display_param(ind_x, ind_y)
            my_layer_list.append((stack, {'colormap': temp_colormap, 'blending': temp_blending, 'translate': (border_to_crop_y * self.const_shift_border + y_offset, border_to_crop_x * self.const_shift_border + x_offset), 'contrast_limits': [0, 5000], 'multiscale': False, 'name': temp_name, 'metadata': temp_dict}))

        return my_layer_list

    def _get_type_tiff(self):
        path_text = self.path_meta_data

        file_list = sorted(listdir(path_text))
        size_loop1 = len(file_list)

        for ind1 in range(size_loop1):

            temp_string = file_list[ind1]

            if temp_string[-4:-1] == 'tif':
                self.type_tif = '.tiff'

            if temp_string[-4:-1] == '.ti':
                self.type_tif = '.tif'


class MyMesoSpimData_3D_substack(MyMesoSpimDataParentClass):

    def __init__(self, path, current_chan):

        super().__init__(path, current_chan)
        self.volumeFormat = "TiledXY|3Dseries"
        self.typeFile = "tiff3D"

        self.path_meta_data = self.base_path

        self.n_planes, self.dim_x, self.dim_y, self.n_tiles, self.tiles_values, self.size_tile, self.size_tile_no_overlap_x, self.size_tile_no_overlap_y, self.n_chans, self.channel_values, self.n_substacks, self.substacks_values = self._get_meta_data()

        self.sign_x = 1
        self.sign_y = -1

        self.numbering, self.coord_x, self.coord_y = self.create_numbering()

        self.is_tile_missing = np.empty((len(self.numbering), 1))
        for ind1 in range(len(self.coord_x)):

            temp_is_missing = True

            for ind2 in range(len(self.coord_x_partial)):

                if self.coord_x[ind1] == self.coord_x_partial[ind2] and self.coord_y[ind1] == self.coord_y_partial[ind2]:
                    temp_is_missing = False

            if temp_is_missing:
                self.is_tile_missing[ind1] = True
            else:
                self.is_tile_missing[ind1] = False

        #self.coord_y = np.flipud(self.coord_y)

        self.type_microscope = "MesoSPIM_3D_substack"

        self.range_x_ROI_for_xml = np.array([1, self.dim_x])
        self.range_y_ROI_for_xml = np.array([1, self.dim_y])

        self._get_type_tiff()

        self.subpath = "*_Tile{}_Ch{}_{}_Sh0" + self.type_tif
        self.name_for_xml = ".*_Tile{}_Ch{}_{}_Sh0" + self.type_tif

        self.create_list_paths_individual_tiles()

    def _get_meta_data(self):
        """
        Returns the meta data
        """
        path_text = self.path_meta_data

        file_list = sorted(listdir(self.path_meta_data))

        size_loop1 = len(file_list)
        count = 0
        count_tif_files = 0
        x_pos = []
        y_pos = []
        tile_num = []

        temp_path_meta_tile = '_Tile{}_'

        for ind1 in range(size_loop1):

            if '_Tile' in file_list[ind1]:
                count = count + 1
                size_loop2 = len(re.findall('[0-9]+', file_list[ind1]))

            # here counts the number of tiff files
            if 'tif' in file_list[ind1] and file_list[ind1].find('meta') == -1:
                count_tif_files = count_tif_files + 1
            # Extracts each pairs of x/y coordinates of each tile from the meta data
            if 'meta' in file_list[ind1]:
                meta_data = get_num_values_text(os.path.join(path_text, file_list[ind1]), ["[x_pos]", "[y_pos]"])
                x_pos.append(meta_data[0])
                y_pos.append(meta_data[1])
                temp = re.findall('[0-9]+', file_list[ind1])
                tile_num.append(temp[-4])
                path_tile = file_list[ind1]

        # Gets the pixel size and the number of planes from the meta data of the first tile.
        pixel_size = get_num_values_text2(os.path.join(path_text, path_tile), [8])
        pixel_size = pixel_size[0]

        n_planes = get_num_values_text2(os.path.join(path_text, path_tile), [2])
        n_planes = int(n_planes[0])

        x_pos = np.asarray(x_pos)
        y_pos = np.asarray(y_pos)
        tile_num = np.asarray(tile_num)

        x_pos_unique = sorted(np.unique(x_pos))
        y_pos_unique = sorted(np.unique(y_pos))

        dim_x = len(x_pos_unique)
        dim_y = len(y_pos_unique)

        dim_tiling = dim_x * dim_y

        size_tile = 2048

        if dim_x == 1:
            size_tile_no_overlap_x = size_tile
            delta_x = x_pos_unique[0]
        else:
            delta_x = x_pos_unique[1] - x_pos_unique[0]
            size_tile_no_overlap_x = round(delta_x / pixel_size)

        if dim_y == 1:
            size_tile_no_overlap_y = size_tile
            delta_y = y_pos_unique[0]
        else:
            delta_y = y_pos_unique[1] - y_pos_unique[0]
            size_tile_no_overlap_y = round(delta_y / pixel_size)



        temp_num = np.zeros((count, size_loop2))

        # The meta data are extracted from the number in the name of the files in the self.base_path
        count = 0
        for ind1 in range(size_loop1):
            if '_Tile' in file_list[ind1]:
                temp = re.findall('[0-9]+', file_list[ind1])
                for ind2 in range(size_loop2):
                    temp_num[count, ind2] = int(temp[ind2])
                count = count + 1

        unique_num_values = np.zeros(size_loop2)
        for ind2 in range(size_loop2):
            unique_num_values[ind2] = int(len(np.unique(temp_num[:, ind2])))

        substacks_values = np.unique(temp_num[:, -2])
        substacks_values = substacks_values.astype(int)

        print('substacks values : ')
        print(substacks_values)
        n_substacks = unique_num_values[-2]
        n_substacks = n_substacks.astype(int)

        channel_values = np.unique(temp_num[:, -3])
        channel_values = channel_values.astype(int)
        print('channel values: ')
        print(channel_values)
        n_chans = unique_num_values[-3]
        n_chans = n_chans.astype(int)

        tiles_values = np.unique(temp_num[:, -4])
        tiles_values = tiles_values.astype(int)

        n_tiles = unique_num_values[-4]
        n_tiles = n_tiles.astype(int)
        print("n_tiles = " + str(n_tiles))

        x_pos = np.around(x_pos / delta_x)
        y_pos = np.around(y_pos / delta_y)

        tile_num = tile_num[0:len(tile_num):n_substacks]
        x_pos = x_pos[0:len(x_pos):n_substacks]
        y_pos = y_pos[0:len(y_pos):n_substacks]

        x_pos = x_pos - np.amin(x_pos) + 1
        y_pos = y_pos - np.amin(y_pos) + 1

        tile_num = tile_num.astype(int)
        x_pos = x_pos.astype(int)
        y_pos = y_pos.astype(int)

        self.numbering_partial = tile_num
        self.coord_x_partial = dim_x + 1 - x_pos
        self.coord_y_partial = dim_y + 1 - y_pos

        if dim_tiling != n_tiles:
            self.partial_tiling = True

        return n_planes, dim_x, dim_y, n_tiles, tiles_values, size_tile, size_tile_no_overlap_x, size_tile_no_overlap_y, n_chans, channel_values, n_substacks, substacks_values

    def create_list_paths_individual_tiles(self):
        self.list_paths_individual_tiles = []
        self.list_paths_individual_tiles_for_xml = []

        for ind in range(len(self.numbering)):
            path_meta = os.path.join(self.dir_tiles_path, self.subpath)
            temp_path_stack = path_meta.format(int(self.numbering[ind]), self.channel_values[self.current_chan], "{}")

            self.list_paths_individual_tiles.append(temp_path_stack)
            self.list_paths_individual_tiles_for_xml.append(self.name_for_xml.format(int(self.numbering[ind]), self.channel_values[self.current_chan], "{}"))

    def create_xml(self):
        event, values = sg.Window('Warning message',
                                  [[sg.Text('Creating an xml first requires the conversion of tiff 3D to tiff 2D.'
                                            'This operation may request a lot of time and memory, do you confirm you want to carry on?')],
                                   [sg.Button('Confirm'), sg.Button('Cancel')]]).read(close=True)
        if event == 'Confirm':

            ROOT = Tk()
            ROOT.withdraw()
            name_folder_tiff2D = simpledialog.askstring(title="Input window", prompt="Name of the new folder were you want to store the tiff 2D files")

            ROOT = Tk()
            ROOT.withdraw()
            target_path_folder_tiff2D = filedialog.askdirectory(title="Where do you want to put the new folder?")

            path_tiff2D = os.path.join(target_path_folder_tiff2D, name_folder_tiff2D)
            os.mkdir(path_tiff2D)

            target_path_meta = os.path.join(path_tiff2D, "MetaDataMesoSPIM")
            # target_path_meta = target_path
            os.mkdir(target_path_meta)

            for ind_chans in range(self.n_chans):

                data_acquisition = MyMesoSpimData_3D_substack(self.base_path, ind_chans)
                my_layer_list = data_acquisition.create_image_layer()
                for ind_tile in range(len(my_layer_list)):

                    im = my_layer_list[ind_tile][0]
                    shape_im = np.shape(im)

                    temp_name = my_layer_list[ind_tile][1]['metadata']['name_tile']
                    ext = pathlib.Path(temp_name).suffixes[-1]
                    name_tile_tif_2D = temp_name[0:-len(ext)+1]

                    ind_str = name_tile_tif_2D.find("_Sh")
                    name_tile_tif_2D = name_tile_tif_2D[0:ind_str - 2] + name_tile_tif_2D[ind_str: -1]

                    temp_path_tile_tif_2D = os.path.join(path_tiff2D, name_tile_tif_2D)
                    os.mkdir(temp_path_tile_tif_2D)
                    #--------------------------------------------------------------------------------------------------------------------------
                    #Add code here to save the tiff in the new folder

                    sizeNumForZeroFill = len(str(shape_im[0]))

                    #for ind_z in range(shape_im[0]):

                    n_slice = shape_im[0]
                    '''
                    a = int(np.round(n_slice/2))-5
                    b = int(np.round(n_slice/2))+5

                    n_slice = b-a
                    '''

                    for ind_z in range(n_slice):
                    #for ind_z in range(a, b, 1):
                        temp_im = np.asarray(np.squeeze(im[ind_z, :, :]))
                        temp_im = Image.fromarray(temp_im)

                        tempSliceNum = str(ind_z + 1)
                        tempSliceNum = tempSliceNum.zfill(sizeNumForZeroFill)

                        temp_name_current_slice = name_tile_tif_2D + '_slice_' + tempSliceNum + '.tif'
                        temp_im.save(os.path.join(temp_path_tile_tif_2D, temp_name_current_slice))
                    #--------------------------------------------------------------------------------------------------------------------------

                    temp_name_meta = temp_name + "_meta.txt"

                    #ind_str = temp_name_meta.find("_Sh")
                    source = os.path.join(self.base_path, temp_name_meta)
                    destination_meta = temp_name_meta
                    ind_str = destination_meta.find("_Sh")
                    destination_meta = destination_meta[0:ind_str - 2] + destination_meta[ind_str: -1] + 't'
                    destination_meta = os.path.join(target_path_meta, destination_meta)

                    shutil.copy2(source, destination_meta)

                    target_values_string = "[z_planes] "
                    with open(destination_meta) as f:
                        lines = f.readlines()

                    # loops over all the lines of the text files, for each of them, check if the strings in target_values_string are present
                    for ind1 in range(len(lines)):
                        string_test = lines[ind1]

                        # the target string has to be smaller than the line of text (string_test variable) that contains it
                        if len(target_values_string) < len(string_test):

                            # if the string_target is present in the line of text, the number present in the line is extracted and saved
                            # (This works since there is a single number per line of meta data text)
                            if target_values_string in string_test:

                                text_to_replaced_old = string_test
                                text_to_replaced_new = target_values_string + str(n_slice) + '\n'

                                f = open(destination_meta, 'r')
                                filedata = f.read()
                                f.close()

                                newdata = filedata.replace(text_to_replaced_old, text_to_replaced_new)

                                f = open(destination_meta, 'w')
                                f.write(newdata)
                                f.close()

            #convert_tiff_images_from_3D_to_2D(self.base_path, path_tiff2D)

            sg.popup(f'Convertion from tiff3D to tiff 2D completed!')

            data_acquisition = MyMesoSpimData_2D(path_tiff2D, self.current_chan)
            data_acquisition.sign_x = copy.copy(self.sign_x)
            data_acquisition.sign_y = copy.copy(self.sign_y)
            data_acquisition.numbering, data_acquisition.coord_x, data_acquisition.coord_y = data_acquisition.create_numbering()
            data_acquisition.create_list_paths_individual_tiles()
            data_acquisition.create_xml()
            
            self.base_path = MyMesoSpimData_2D

            return data_acquisition

    def create_image_layer(self):
        my_layer_list = []

        base_dict = {
            "n_planes": self.n_planes,
            "dim_x": self.dim_x,
            "dim_y": self.dim_y,
            "size_tile": self.size_tile,
            "size_tile_no_overlap_x": self.size_tile_no_overlap_x,
            "size_tile_no_overlap_y": self.size_tile_no_overlap_y,
            "path": self.base_path,
            "type_microscope": self.type_microscope,
            'is_small_tile': False,
            'x_coord': np.NaN,
            'y_coord': np.NaN,
            'DS_factor': self.DS_factor,
            'current_chan': self.current_chan,
            'n_chans': self.n_chans,
            'channel_values': self.channel_values,

        }

        border_to_crop_x = int(np.around((self.size_tile - self.size_tile_no_overlap_x) // self.DS_factor))
        border_to_crop_y = int(np.around((self.size_tile - self.size_tile_no_overlap_y) // self.DS_factor))

        for ind in range(len(self.numbering)):

            ind_x = self.coord_x[ind]
            ind_y = self.coord_y[ind]

            '''
            path_filling = [str(int(self.numbering[ind])), self.current_chan]
            path_filling[0] = path_filling[0].zfill(self.zero_pad)

            path_meta = os.path.join(self.dir_tiles_path, self.subpath)
            '''
            #temp_path_stack = path_meta.format(path_filling[self.order_path_format[0]], path_filling[self.order_path_format[1]])

            if self.is_tile_missing[ind]:
                stack = np.zeros((2, 2, 2))
            else:
                for ind_substatcks in range(self.n_substacks):
                    temp_path_stack = self.list_paths_individual_tiles[ind]
                    temp_path_stack = temp_path_stack.format(self.substacks_values[ind_substatcks])

                    path = glob.glob(temp_path_stack)

                    if ind_substatcks == 0:
                        name_tile = os.path.split(path[0])
                        name_tile = str(name_tile[1])

                    zarr_store = tifffile.imread(path, aszarr = True)
                    if ind_substatcks == 0:
                        stack = dask.array.from_zarr(zarr_store)
                    else:
                        stack = np.concatenate((stack, dask.array.from_zarr(zarr_store)), axis=0)
                    list_stacks_all_chans = []
                    old_curr_chan = self.current_chan

                # Downsample
                if self.DS_factor > 1:
                    stack = stack[:, ::self.DS_factor, ::self.DS_factor]

                y_offset = (ind_y - 1) * self.size_tile_no_overlap_y // self.DS_factor
                x_offset = (ind_x - 1) * self.size_tile_no_overlap_x // self.DS_factor

                temp_name = '[' + str(ind_y) + ', ' + str(ind_x) + ']'

                temp_dict = base_dict.copy()
                temp_dict['is_small_tile'] = True
                temp_dict['y_coord'] = ind_y
                temp_dict['x_coord'] = ind_x
                temp_dict['tile_microscope_number'] = self.numbering[ind]

                temp_dict['path_individual_tiles'] = self.list_paths_individual_tiles[ind]
                temp_dict['path_individual_tiles_for_xml'] = self.list_paths_individual_tiles_for_xml[ind]
                temp_dict['name_tile'] = name_tile

                temp_dict['data_acquisition'] = self

                temp_colormap, temp_blending = self._determine_tile_display_param(ind_x, ind_y)
                my_layer_list.append((stack, {'colormap': temp_colormap, 'blending': temp_blending, 'translate': (border_to_crop_y * self.const_shift_border + y_offset, border_to_crop_x * self.const_shift_border + x_offset), 'contrast_limits': [0, 5000], 'multiscale': False, 'name': temp_name, 'metadata': temp_dict}))

        return my_layer_list

    def _get_type_tiff(self):

        path_text = self.path_meta_data
        file_list = sorted(listdir(path_text))
        size_loop1 = len(file_list)

        for ind1 in range(size_loop1):

            temp_string = file_list[ind1]

            if temp_string[-4:-1] == 'tif':
                self.type_tif = '.tiff'

            if temp_string[-4:-1] == '.ti':
                self.type_tif = '.tif'


class MyMesoSpimData_2D(MyMesoSpimDataParentClass):

    def __init__(self, path, current_chan):

        super().__init__(path, current_chan)
        self.volumeFormat = "TiledXY|2Dseries"
        self.typeFile = "tiff2D"

        self.path_meta_data = os.path.join(self.base_path, "MetaDataMesoSPIM")

        self.n_planes, self.dim_x, self.dim_y, self.size_tile, self.size_tile_no_overlap_x, self.size_tile_no_overlap_y, self.n_chans, self.channel_values = self._get_meta_data()

        print("chan info:")
        print(self.n_chans)
        print(self.channel_values)

        print("tiling dim xy")
        print(self.dim_x)
        print(self.dim_y)


        self.sign_x = 1
        self.sign_y = -1

        self.numbering, self.coord_x, self.coord_y = self.create_numbering()

        self.type_microscope = "MesoSPIM_2D"

        self.range_x_ROI_for_xml = np.array([1, self.dim_x])
        self.range_y_ROI_for_xml = np.array([1, self.dim_y])

        self.subpath = os.path.join("*_Tile{}_Ch{}_*", "*.tif")
        self.name_for_xml = ".*.tif"

        self.create_list_paths_individual_tiles()

    def create_list_paths_individual_tiles(self):
        self.list_paths_individual_tiles = []
        self.list_paths_individual_tiles_for_xml = []

        for ind in range(len(self.numbering)):
            path_meta = os.path.join(self.dir_tiles_path, self.subpath)
            temp_path_stack = path_meta.format(int(self.numbering[ind]), self.channel_values[self.current_chan])

            self.list_paths_individual_tiles.append(temp_path_stack)
            self.list_paths_individual_tiles_for_xml.append(self.name_for_xml.format(str(self.channel_values[self.current_chan])))

    def create_xml(self):
        ref_sys = np.array([1, 2, 3])
        voxel_dim = np.array([1, 1, 1])

        # First creates the base of the xml, that is the same no matter if the xml is based on whole tiling or only partial tiling
        ET.Element("!DOCTYPE TeraStitcher SYSTEM 'TeraStitcher.DDT'")

        root = ET.Element("TeraStitcher", volume_format=self.volumeFormat, input_plugin=self.typeFile)

        sub_element_branch_1_1 = ET.SubElement(root, "stacks_dir ", value=self.dir_tiles_path)
        sub_element_branch_1_2 = ET.SubElement(root, "ref_sys", ref1=str(ref_sys[0]), ref2=str(ref_sys[1]),
                                               ref3=str(ref_sys[2]))
        sub_element_branch_1_3 = ET.SubElement(root, "voxel_dims", V=str(voxel_dim[0]), H=str(voxel_dim[1]),
                                               D=str(voxel_dim[2]))
        sub_element_branch_1_4 = ET.SubElement(root, "origin", V=str(0), H=str(0), D=str(0))
        sub_element_branch_1_5 = ET.SubElement(root, "mechanical_displacements",
                                               V=str(self.size_tile_no_overlap_y),
                                               H=str(self.size_tile_no_overlap_x))
        sub_element_branch_1_6 = ET.SubElement(root, "dimensions",
                                               stack_rows=str(self.range_y_ROI_for_xml[1] - self.range_y_ROI_for_xml[0] + 1),
                                               stack_columns=str(self.range_x_ROI_for_xml[1] - self.range_x_ROI_for_xml[0] + 1),
                                               stack_slices=str(self.n_planes))
        stacks = ET.SubElement(root, "STACKS")

        # bool vector that stores the tiles that are part of the selected ROI out of the whole tiling


        bool_ROI = np.logical_and(np.logical_and(self.coord_x >= self.range_x_ROI_for_xml[0],
                                                 self.coord_x <= self.range_x_ROI_for_xml[1]),
                                  np.logical_and(self.coord_y >= self.range_y_ROI_for_xml[0],
                                                 self.coord_y <= self.range_y_ROI_for_xml[1]))

        for ind in range(len(self.numbering)):

            ind_x = self.coord_x[ind]
            ind_y = self.coord_y[ind]

            if bool(bool_ROI[ind]) is True:

                temp_path_stack = self.list_paths_individual_tiles[ind]

                files = glob.glob(os.path.dirname(temp_path_stack))
                name_IMG_REGEX_for_xml = self.list_paths_individual_tiles_for_xml[ind]

                str_Z_RANGES = "[" + str(0) + "," + str(self.n_planes) + ")"

                stack = ET.SubElement(stacks, "Stack", N_CHANS="1", N_BYTESxCHAN="2", ROW=str(ind_y - 1),
                                      COL=str(ind_x - 1),
                                      ABS_V=str((ind_y - 1) * self.size_tile_no_overlap_y),
                                      ABS_H=str((ind_x - 1) * self.size_tile_no_overlap_x),
                                      ABS_D="0", STITCHABLE="no", DIR_NAME=os.path.basename(files[0]),
                                      _RANGES=str_Z_RANGES, IMG_REGEX=name_IMG_REGEX_for_xml)

                sub_element_branch_3_1 = ET.SubElement(stack, "NORTH_displacements")
                sub_element_branch_3_2 = ET.SubElement(stack, "EAST_displacements")
                sub_element_branch_3_3 = ET.SubElement(stack, "SOUTH_displacements ")
                sub_element_branch_3_4 = ET.SubElement(stack, "WEST_displacements ")

        tree = ET.ElementTree(root)

        ROOT = Tk()
        ROOT.withdraw()
        target_path_xml = filedialog.askdirectory()

        ROOT = Tk()
        ROOT.withdraw()
        name_xml = simpledialog.askstring(title="Input window", prompt="Name of the xml file:")

        wd = os.getcwd()
        current_path_xml = os.path.join(wd, name_xml + ".xml")
        target_path_xml = os.path.join(target_path_xml, name_xml + ".xml")
        tree.write(target_path_xml)


def napari_get_reader(path: Union[str, List[str]]): # -> Optional[ReaderFunction]:
    """
    Return a function named microscope_reader capable of reading different light-sheet microscope data into napari layer data.
    Parameters
    -------
    function:
        Return a function that accepts the
        same path or list of paths, and returns a list of layer data tuples.
    """
    return microscope_reader


def microscope_reader(path: Union[str, List[str]]) -> List[Tuple[Any, Dict, str]]:

    # First test to determine the type of microscope. Than instanciate an object from the corresponding subclass
    type_microscope = get_type_microscope(path)
    if type_microscope == "Clear Scope":
        data_acquisition = MyClearScopeData(path, 0)
    elif type_microscope == "COLM":
        data_acquisition = MyColmData(path, 0)
    elif type_microscope == "MesoSPIM_2D":
        data_acquisition = MyMesoSpimData_2D(path, 0)
    elif type_microscope == "MesoSPIM_3D":
        data_acquisition = MyMesoSpimData_3D(path, 0)
    elif type_microscope == "MesoSPIM_3D_substack":
        data_acquisition = MyMesoSpimData_3D_substack(path, 0)

    # Create the image layer list from the information stored in the object
    my_layer_list = data_acquisition.create_image_layer()

    # Create the information list from the information stored in the object
    shapes_layer = data_acquisition.create_info_layer()

    my_layer_list.append(shapes_layer)
    if data_acquisition.partial_tiling:
        print("is_tile_missing")
        print(data_acquisition.is_tile_missing)

    return my_layer_list

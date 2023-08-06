"""
This module contains the Napari widget.

It implements the ``napari_experimental_provide_dock_widget`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""

from ._reader import range_overlap

import numpy as np
from qtpy.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSlider, QLabel
from PyQt5.QtCore import Qt


def test_if_inside_rect(x, y, rect):
    '''
    This function test if a point (pair of x and y coordinates) is inside a rectangle

    :param x: float variable the represent the x coordinate of a point in 2D
    :param y: float variable the represent the y coordinate of a point in 2D
    :param rect: a 2x2 array that contains (x0,x1) and (yo,y1) where x0 and y0 are the coord of the top left coorner
    and x1 and y1 the ones of the bottom right corner
    return: returns a boolean
    '''
    result_test = np.amin(rect[:, 0]) <= x <= np.amax(rect[:, 0]) and np.amin(rect[:, 1]) <= y <= np.amax(rect[:, 1])
    return result_test


def is_square(rect):
    '''
    This function test if a rectangle is a square

    :param rect:
    :return:
    '''
    result_test = (np.amin(rect[:, 0]) - np.amax(rect[:, 0])) == (np.amin(rect[:, 1]) - np.amax(rect[:, 1]))
    return result_test


class DataPreview(QWidget):

    def __init__(self, napari_viewer):
        super().__init__()

        self.viewer = napari_viewer
        self.data_acquisition = []
        '''
        Orientation of the x and y dimensions: are changed to -1 depending on if the tiles are showed from top to 
        bottom or from bottom to top and from left to right or from right to left
        '''
        self.sign_x = 1
        self.sign_y = 1

        # config
        self.active = False
        self.mouse_down = False
        self.mode = None
        self.n_clicks = 0
        self.n_cklicks_inside_square = 0
        self.is_smaller_portion = False

        self.x_min = np.NINF
        self.x_max = np.inf

        self.y_min = np.NINF
        self.y_max = np.inf

        self.x_ROI = []
        self.y_ROI = []

        self.is_portion_selected = False

        # different buttons to change the tiling displaying colors
        btn1 = QPushButton("Checkerboard")
        btn1.clicked.connect(self._on_click_bt1)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(btn1)

        btn2 = QPushButton("Row")
        btn2.clicked.connect(self._on_click_bt2)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(btn2)

        btn3 = QPushButton("Column")
        btn3.clicked.connect(self._on_click_bt3)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(btn3)

        btn4 = QPushButton("Reset Grayscale")
        btn4.clicked.connect(self._on_click_bt4)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(btn4)
        #----------------------------
        #overlap
        label_overlap_txt = QLabel('Overlap', self)
        label_overlap_txt.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label_overlap_txt.setMinimumWidth(80)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(label_overlap_txt)
        self.slider_overlap = QSlider(Qt.Horizontal, self)

        self.value_slider_overlap = 50
        self.slider_overlap.setRange(0, 100)
        self.slider_overlap.setSliderPosition(50)
        self.slider_overlap.valueChanged.connect(self._update_overlap)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.slider_overlap)

        self.label_overlap = QLabel('50', self)
        self.label_overlap.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label_overlap.setMinimumWidth(80)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label_overlap)

        # ----------------------------
        label_max_contrast_txt = QLabel('Upper contrast limit', self)
        label_max_contrast_txt.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label_max_contrast_txt.setMinimumWidth(80)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(label_max_contrast_txt)

        self.slider_max_contrast = QSlider(Qt.Horizontal, self)

        self.factor_finest_step_slider = 1000
        self.is_log = True
        if self.is_log is True:
            max_contrast_range = 16*self.factor_finest_step_slider
            self.value_slider_min_contrast = 1
            self.value_slider_max_contrast = 10*self.factor_finest_step_slider
            self.slider_max_contrast.setRange(1, max_contrast_range)
            self.slider_max_contrast.setSliderPosition(12*self.factor_finest_step_slider)
        else:
            max_contrast_range = 2 ** 16 - 1
            self.value_slider_min_contrast = 1
            self.value_slider_max_contrast = self.factor_finest_step_slider
            self.slider_max_contrast.setRange(1, max_contrast_range)
            self.slider_max_contrast.setSliderPosition(5000)

        self.slider_max_contrast.valueChanged.connect(self._update_max_contrast)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.slider_max_contrast)

        if self.is_log is True:
            self.label_max_contrast = QLabel('4096', self)
        else:
            self.label_max_contrast = QLabel('5000', self)

        self.label_max_contrast.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label_max_contrast.setMinimumWidth(80)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label_max_contrast)

        label_min_contrast_txt = QLabel('Lower contrast limit', self)
        label_min_contrast_txt.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label_min_contrast_txt.setMinimumWidth(80)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(label_min_contrast_txt)

        self.slider_min_contrast = QSlider(Qt.Horizontal, self)
        self.slider_min_contrast.setRange(0, max_contrast_range - 1)
        self.slider_min_contrast.setSliderPosition(0)
        self.slider_min_contrast.valueChanged.connect(self._update_min_contrast)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.slider_min_contrast)

        self.label_min_contrast = QLabel('0', self)
        self.label_min_contrast.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label_min_contrast.setMinimumWidth(80)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label_min_contrast)

        # #----------------------------------------------------------------
        # btnV = QPushButton("Rearrange tiles vertically")
        # btnV.clicked.connect(self._on_click_btV)
        # self.setLayout(QVBoxLayout())
        # self.layout().addWidget(btnV)
        #
        # #----------------------------------------------------------------
        # btnH = QPushButton("Rearrange tiles horizontally")
        # btnH.clicked.connect(self._on_click_btH)
        # self.setLayout(QVBoxLayout())
        # self.layout().addWidget(btnH)

        #----------------------------------------------------------------

        self.current_chan = self.viewer.layers[0].metadata["current_chan"]
        self.n_chans = self.viewer.layers[0].metadata["n_chans"]

        current_chan = QLabel('Current channel', self)
        current_chan.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        current_chan.setMinimumWidth(80)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(current_chan)

        self.slider_chan = QSlider(Qt.Horizontal, self)

        self.value_slider_current_chan = self.current_chan + 1
        self.slider_chan.setRange(1, self.n_chans)
        self.slider_chan.setSliderPosition(1)

        self.slider_chan.valueChanged.connect(self._change_channel_with_slider)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.slider_chan)

        #self.label_current_chan = QLabel(str(self.current_chan + 1), self)
        self.label_current_chan = QLabel(str(self.current_chan + 1) + ' / ' + str(self.n_chans), self)

        self.label_current_chan.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label_current_chan.setMinimumWidth(80)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label_current_chan)

        #----------------------------------------------------------------

        btn_save_1 = QPushButton("Create xml whole tiling")
        btn_save_1.clicked.connect(self._on_click_xml_1)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(btn_save_1)

        btn_save_2 = QPushButton("Create xml partial tiling")
        btn_save_2.clicked.connect(self._on_click_xml_2)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(btn_save_2)

    def _change_channel_with_slider(self, value_slider):
        '''
        This function looks into the first layer to find the data_aquisition object stored in the metadata field of the
        first viewer layer. It then changes the current_chan attribute to its new value, and update the data_acquisition
        accordingly.

        :param value_slider: Value of the change channel slider that can be manually changed by the user in the GUI
        :return:
        '''
        #self.label_current_chan.setText(str(value_slider))
        self.label_current_chan.setText(str(value_slider) + ' / ' + str(self.n_chans))
        self.current_chan = value_slider - 1

        data_acquisition = self.viewer.layers[0].metadata["data_acquisition"]
        print("here is the object infos: ")
        data_acquisition.display()

        current_chan = data_acquisition.current_chan
        n_chans = data_acquisition.n_chans

        my_layer_list = []
        if current_chan == value_slider - 1:
            print("target chan and current chan are the same")
        else:
            if value_slider > n_chans:
                print("target chan is too big")

            else:
                print("target chan is an acceptable target")
                '''
                The current channel of the data_acquisition object is changed to the slider value. Then its list of
                individual files is updated. A new layer list is created based on the updated path and current channel
                number.
                The data field of each layer in the napari viewer (that contains the image) is updated with the image
                of the same tile but with the new channel.
                The metadata field is also updated.
                '''
                data_acquisition.current_chan = int(value_slider - 1)
                data_acquisition.create_list_paths_individual_tiles()
                my_layer_list = data_acquisition.create_image_layer()
                shapes_layer = data_acquisition.create_info_layer()
                my_layer_list.append(shapes_layer)

                for ind in range(len(self.viewer.layers)):
                    # This test exclude the shape layer which has an empty metadata field
                    if len(self.viewer.layers[ind].metadata) > 1:

                        self.viewer.layers[ind].metadata = my_layer_list[ind][1]['metadata']
                        self.viewer.layers[ind].data = np.array([[0, 0], [0, 0]])
                        self.viewer.layers[ind].data = my_layer_list[ind][0]

    def _update_overlap(self, value_slider):
        '''
        This function takes care of updating the overlap of each tile in the layer list of the viewer, both by changing the translate attribute of the layer, as
        well as the fields size_tile_no_overlap_x and size_tile_no_overlap_y in the data_aquisition object stored in the metadata of each layer
        '''
        test = 0
        self.label_overlap.setText(str(value_slider))
        self.value_slider_overlap = value_slider

        size_loop = len(self.viewer.layers)
        for ind in range(size_loop):

            self.current_layer = self.viewer.layers[ind]

            if len(self.current_layer.metadata) > 0:
                layer_info_original = self.viewer.layers[ind]

                layer_info = layer_info_original.as_layer_data_tuple()
                layer_info = layer_info[1]
                layer_info = layer_info['metadata']

                if layer_info['is_small_tile'] == True:

                    f = 1. - value_slider/(2.*100.)
                    size_tile = layer_info["size_tile"]
                    size_tile_no_overlap_x_old = layer_info["size_tile_no_overlap_x"]
                    size_tile_no_overlap_y_old = layer_info["size_tile_no_overlap_y"]

                    size_tile_no_overlap_x = int(size_tile * f)
                    size_tile_no_overlap_y = int(size_tile * f)

                    DS_factor = layer_info['DS_factor']

                    x_coord = layer_info['x_coord']
                    y_coord = layer_info['y_coord']

                    y_offset = (y_coord - 1) * size_tile_no_overlap_y // DS_factor
                    x_offset = (x_coord - 1) * size_tile_no_overlap_x // DS_factor

                    border_to_crop_x = int(np.around((size_tile - size_tile_no_overlap_x) // DS_factor))
                    border_to_crop_y = int(np.around((size_tile - size_tile_no_overlap_y) // DS_factor))

                    border_to_crop_x_old = int(np.around((size_tile - size_tile_no_overlap_x_old) // DS_factor))
                    border_to_crop_y_old = int(np.around((size_tile - size_tile_no_overlap_y_old) // DS_factor))

                    const_shift_border = -0.5

                    translate_y = border_to_crop_y * const_shift_border + y_offset
                    translate_x = border_to_crop_x * const_shift_border + x_offset

                    self.current_layer.translate = [translate_y, translate_x]


                    self.data_acquisition = self.viewer.layers[ind].metadata["data_acquisition"]
                    self.data_acquisition.size_tile_no_overlap_x = size_tile_no_overlap_x
                    self.data_acquisition.size_tile_no_overlap_y = size_tile_no_overlap_y
                    self.viewer.layers[ind].metadata["data_acquisition"] = self.data_acquisition

        new_shape_layer =  self.data_acquisition.create_info_layer()
        new_shape_layer = new_shape_layer[0]
        old_shape_layer = self.viewer.layers[-1].data

        self.viewer.layers[-1].data = new_shape_layer
        '''
        for ind in range(len(self.viewer.layers[-1].data)):
            x = self.viewer.layers[-1].data
            y = self.viewer.layers[-1].data
        '''

        '''
        shapes_layer_text, shapes_layer_squares = self.data_acquisition.create_info_layer()
        self.viewer.layers.pop(len(self.viewer.layers) - 1)
        self.viewer.add_shapes(shapes_layer_squares[0], shape_type='polygon', edge_width=10, edge_color='white', face_color='white')
        '''

    def _update_max_contrast(self, value_slider):
        '''
        This function changes the upper bound of the contrast range of each tile. The default mode is set to change it in a logarithmic fashion
        to make it easier to accomodate the frequent very large range of pixel intensity present in mos acquisitions.
        '''
        if self.is_log is True:
            self.label_max_contrast.setText(str(int(2**(value_slider/self.factor_finest_step_slider))))
        else:
            self.label_max_contrast.setText(str(value_slider))
        self.value_slider_max_contrast = value_slider


        size_loop = len(self.viewer.layers)
        for ind in range(size_loop):

            self.current_layer = self.viewer.layers[ind]

            if len(self.current_layer.metadata) > 0:
                layer_info = self.viewer.layers[ind]
                layer_info = layer_info.as_layer_data_tuple()
                layer_info = layer_info[1]
                layer_info = layer_info['metadata']

                if layer_info['is_small_tile'] == True:

                    if value_slider <= self.value_slider_min_contrast:
                        self.value_slider_min_contrast = value_slider - 1
                        if self.is_log is True:
                            self.label_min_contrast.setText(str(int(2**(value_slider/self.factor_finest_step_slider - 1))))
                        else:
                            self.label_min_contrast.setText(str(value_slider - 1))
                        self.slider_min_contrast.setSliderPosition(value_slider - 1)

                        value_contrast = self.value_slider_min_contrast
                    else:
                        value_contrast = self.current_layer.contrast_limits[0]
                    if self.is_log is True:
                        self.current_layer.contrast_limits = [value_contrast, 2**(value_slider/self.factor_finest_step_slider)]
                    else:
                        self.current_layer.contrast_limits = [value_contrast, value_slider]

    def _update_min_contrast(self, value_slider):
        '''
        This function changes the lower bound of the contrast range of each tile. The default mode is set to change it in a logarithmic fashion
        to make it easier to accomodate the frequent very large range of pixel intensity present in mos acquisitions.
        '''
        if self.is_log is True:
            self.label_min_contrast.setText(str(int(2**(value_slider/self.factor_finest_step_slider))))
        else:
            self.label_min_contrast.setText(str(value_slider))

        self.value_slider_min_contrast = value_slider
        size_loop = len(self.viewer.layers)
        for ind in range(size_loop):
            self.current_layer = self.viewer.layers[ind]
            if len(self.current_layer.metadata) > 0:
                layer_info = self.viewer.layers[ind]
                layer_info = layer_info.as_layer_data_tuple()
                layer_info = layer_info[1]
                layer_info = layer_info['metadata']

                if layer_info['is_small_tile'] == True:
                    if value_slider >= self.value_slider_max_contrast:
                        self.value_slider_max_contrast = value_slider + 1
                        if self.is_log is True:
                            self.label_max_contrast.setText(str(int(2**(value_slider/self.factor_finest_step_slider + 1))))
                        else:
                            self.label_max_contrast.setText(str(value_slider + 1))
                        self.slider_max_contrast.setSliderPosition(value_slider + 1)
                        value_contrast = self.value_slider_max_contrast
                    else:
                        value_contrast = self.current_layer.contrast_limits[1]
                    if self.is_log is True:
                        self.current_layer.contrast_limits = [2**(value_slider/self.factor_finest_step_slider), value_contrast]
                    else:
                        self.current_layer.contrast_limits = [value_slider, value_contrast]

   
    def _on_click_xml_1(self):
        self.is_smaller_portion = False
        self._save_xml()

    def _on_click_xml_2(self):
        self.is_smaller_portion = True
        self._save_xml()

    def _save_xml(self):

        # There are two cases, either everything is saved, or a smaller portion of the aquisition

        # Creates a data_acquisition object from the meta data saved in the layer
        self.data_acquisition = self.viewer.layers[0].metadata["data_acquisition"]

        if self.is_smaller_portion is True:

            self.copy_on_mouse_press = self.viewer.window.qt_viewer.on_mouse_press

            # Save the two clicks
            self.count_clicks = 0

            self.dat = self.viewer.layers[-1].data
            self.labels_shape = self.viewer.layers[-1].properties['label']
            print(self.dat)

            def our_mouse_press(event=None):
                print("mouse press", event.native.x(), event.native.y(), event.native.button())
                self.n_clicks = self.n_clicks + 1

                # self.x_ROI is in pixel coordinates
                self.x_ROI.append(self.viewer.cursor.position[2])
                self.y_ROI.append(self.viewer.cursor.position[1])
                # Ensure to reset after 2 clicks

                # color selected squares

                for ind in range(len(self.dat)):
                    test_inside = test_if_inside_rect(self.viewer.cursor.position[1], self.viewer.cursor.position[2],  self.dat[ind])
                    if test_inside and len(self.labels_shape[ind]) == 0:
                        self.n_cklicks_inside_square = self.n_cklicks_inside_square + 1
                        self.viewer.add_shapes(self.dat[ind], shape_type='polygon', edge_width=10, edge_color='blue', face_color='royalblue')

                        print(ind)
                        print(self.dat[ind])
                        print("position: [" + str(self.viewer.cursor.position[2]) + ", " + str(
                            self.viewer.cursor.position[1]) + "]")
                        print(test_inside)

                if self.n_cklicks_inside_square >= 2:

                    self.viewer.window.qt_viewer.on_mouse_press = self.copy_on_mouse_press

                    # Needs to convert the ROI to tiles coord instead of viewer coords.

                    self.x_min = np.min(np.asarray(self.x_ROI))
                    self.x_max = np.max(np.asarray(self.x_ROI))

                    self.y_min = np.min(np.asarray(self.y_ROI))
                    self.y_max = np.max(np.asarray(self.y_ROI))

                    # Here it is converted into tiles coordinates
                    self.x_ROI = (np.ceil(np.asarray(self.x_ROI) / (self.data_acquisition.size_tile_no_overlap_x // self.data_acquisition.DS_factor))).astype(int)
                    self.y_ROI = (np.ceil(np.asarray(self.y_ROI) / (self.data_acquisition.size_tile_no_overlap_y // self.data_acquisition.DS_factor))).astype(int)

                    # Here takes the intersection of the input (by clicking) ROI, self.x_ROI, with the base ROI, which contains the whole tiling, self.data_acquisition.range_x_ROI_for_xml

                    self.data_acquisition.range_x_ROI_for_xml = range_overlap(self.data_acquisition.range_x_ROI_for_xml, self.x_ROI)
                    self.data_acquisition.range_y_ROI_for_xml = range_overlap(self.data_acquisition.range_y_ROI_for_xml, self.y_ROI)

                    # resets the variable back to original state
                    self.x_ROI = []
                    self.y_ROI = []
                    self.n_clicks = 0
                    self.n_cklicks_inside_square = 0
                    if self.data_acquisition.type_microscope == "MesoSPIM_3D" or self.data_acquisition.type_microscope == "MesoSPIM_3D_substack":
                        self.data_acquisition = self.data_acquisition.create_xml()
                    else:
                        self.data_acquisition.create_xml()
                    self.viewer.window.qt_viewer.on_mouse_press = self.copy_on_mouse_press

                    for i in range(2):
                        self.viewer.layers.pop(len(self.viewer.layers)-1)

            self.viewer.window.qt_viewer.on_mouse_press = our_mouse_press
        else:
            if self.data_acquisition.type_microscope == "MesoSPIM_3D" or self.data_acquisition.type_microscope == "MesoSPIM_3D_substack":
                self.data_acquisition = self.data_acquisition.create_xml()

            else:
                self.data_acquisition.create_xml()

        self.data_acquisition.reset_ROI()

    #-----------
    '''
    The 4 following function linked to the event when the 4 buttons that change the tiling coloring will change
    the coloring mode before calling the _activate_coloring_layers which will change the coloring mode of each layer
    in the napari viewer accordingly 
    '''
    def _on_click_bt1(self):
        self.mode = "checkerboard"
        self._activate_coloring_layers()

    def _on_click_bt2(self):
        self.mode = "row"
        self._activate_coloring_layers()

    def _on_click_bt3(self):
        self.mode = "column"
        self._activate_coloring_layers()

    def _on_click_bt4(self):
        self.mode = "standard"
        self._activate_coloring_layers()

    # -----------

    def _on_click_btV(self):
        self.data_acquisition = self.viewer.layers[0].metadata["data_acquisition"]
        '''self.data_acquisition.sign_y is used when creating the numbering
        depending if it 1 or -1, the first tiles are located in the upper or lower row of the tiling
        '''
        self.data_acquisition.sign_y = -self.data_acquisition.sign_y
        self._update_tile_position()

    def _on_click_btH(self):
        self.data_acquisition = self.viewer.layers[0].metadata["data_acquisition"]
        '''self.data_acquisition.sign_x is used when creating the numbering
        depending if it 1 or -1, the first tiles are located in the furthest left or right colums of the tiling the tiling
        '''
        self.data_acquisition.sign_x = -self.data_acquisition.sign_x
        self._update_tile_position()

    def _update_tile_position(self):

        '''
        This funcion updates the numbering to account for the modification of the self.data_acquisition.sign_y and
        self.data_acquisition.sign_x in _on_click_btV or _on_click_btH above respectivelly.
        :return:
        '''

        old_numbering = self.data_acquisition.numbering

        self.data_acquisition.numbering, self.data_acquisition.coord_x, self.data_acquisition.coord_y = self.data_acquisition.create_numbering()
        new_numbering = self.data_acquisition.numbering
        self.data_acquisition.create_list_paths_individual_tiles()
        self.viewer.layers[0].metadata["data_acquisition"] = self.data_acquisition

        layer_numbers = []
        layer_microscope_numbering = []
        for ind in range(len(self.viewer.layers)):
            layer_info = self.viewer.layers[ind]
            layer_info = layer_info.as_layer_data_tuple()
            layer_info = layer_info[1]
            layer_info = layer_info['metadata']
            if len(layer_info) > 0:
                if layer_info['is_small_tile'] is True:
                    layer_numbers = np.append(layer_numbers, ind)
                    layer_microscope_numbering = np.append(layer_microscope_numbering, self.viewer.layers[ind].metadata["tile_microscope_number"])
                    '''
                    self.viewer.layers[ind].data = np.flip(self.viewer.layers[ind].data, target_dim)
                    self.viewer.layers[ind].metadata["data_acquisition"] = self.data_acquisition
                    print(self.viewer.layers[ind].metadata)
                    '''

        layer_numbers = np.array(layer_numbers)
        layer_microscope_numbering = np.array(layer_microscope_numbering)
        array_control_switch = np.zeros(len(layer_microscope_numbering))

        for ind_1 in range(len(array_control_switch)):
            if array_control_switch[ind_1] == 0:
                ind_a = int(layer_numbers[ind_1])

                num_micro_a = layer_microscope_numbering[ind_1]
                temp = np.where(old_numbering == num_micro_a)
                num_micro_b = new_numbering[int(temp[0])]

                ind_b = np.where(layer_microscope_numbering == num_micro_b)
                ind_b = int(ind_b[0])

                temp_image = self.viewer.layers[ind_a].data
                self.viewer.layers[ind_a].data = self.viewer.layers[ind_b].data
                self.viewer.layers[ind_b].data = temp_image

                self.viewer.layers[ind_b].metadata["tile_microscope_number"] = num_micro_a
                self.viewer.layers[ind_a].metadata["tile_microscope_number"] = num_micro_b

                array_control_switch[ind_1] = 1
                ind_2 = np.where(layer_numbers == ind_b)
                ind_2 = int(ind_2[0])
                array_control_switch[ind_2] = 1

    def _activate_coloring_layers(self):
        my_layer_list = []

        '''
        To alternate between colors, a -1 is raised to a given power in order for odd and even rows or column to alternate 
        between -1 and 1, one being red and the other green.
        Both factors f_x and f_y are set to 1 by default to obtain a checkerboard.
        '''
        f_x = 1
        f_y = 1

        '''
        There are two color maps for even and odd tile x and/or y coordinates
        '''
        # to make a colormap, the colors of both end of the gradient must be defined (here black and green, or black and red)
        colormap_odd = np.array([[0., 0., 0., 1.], [0., 1., 0., 1.]])
        colormap_even = np.array([[0., 0., 0., 1.], [1., 0., 0., 1.]])
        opacity = 1

        blending_type = "additive"

        '''
        If you want to alternate only beteen rows, the x coordinate shouldn't play a role, so the factor f_x latter
        present in the exponential is set to zero. If one want to alternate columns, f_y is set to zero instead
        '''

        if self.mode == "row":
            f_x = 0

        if self.mode == "column":
            f_y = 0

        '''
        If the selected mode is standard, the color maps of both even and odd tiles are set to grayscale
        
        '''
        if self.mode == "standard":
            # to make a colormap, the colors of both end of the gradient must be defined (here black and white)
            colormap_odd = np.array([[0., 0., 0., 1.], [1., 1., 1., 1.]])
            colormap_even = np.array([[0., 0., 0., 1.], [1., 1., 1., 1.]])
            blending_type = "translucent"

        size_loop = len(self.viewer.layers)

        for ind in range(size_loop):

            self.current_layer = self.viewer.layers[ind]

            if len(self.current_layer.metadata) > 0:
                layer_info = self.viewer.layers[ind]
                layer_info = layer_info.as_layer_data_tuple()
                layer_info = layer_info[1]
                layer_info = layer_info['metadata']

                if layer_info['is_small_tile'] == True:
                    self.current_layer.opacity = opacity
                    self.current_layer.blending = blending_type
                    temp_colormap = self.current_layer.colormap

                    x = layer_info['x_coord']
                    y = layer_info['y_coord']

                    #For each layer in the viewer, the colormap will be modified according to it's x and/or y coordinates

                    test_checkerboard = np.power(-1, y*f_y + x*f_x)

                    if test_checkerboard > 0:
                        new_colormap = colormap_even
                        name_colormap = 'red'
                    else:
                        new_colormap = colormap_odd
                        name_colormap = 'green'

                    temp_colormap.colors = new_colormap
                    temp_colormap.name = name_colormap
                    temp_colormap.controls = np.array([0., 1.])

                    self.current_layer.colormap = temp_colormap


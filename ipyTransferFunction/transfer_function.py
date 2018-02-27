#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2018, Cyrille Favreau <cyrille.favreau@gmail.ch>
#
# This file is part of ipyTransferFunction
# <https://github.com/favreau/ipyTransferFunction>
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License version 3.0 as published
# by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# All rights reserved. Do not distribute without further notice.

import seaborn as sns
from ipywidgets import widgets, Layout, Box, VBox, ColorPicker
from IPython.display import display


class TransferFunctionEditor(object):

    def __init__(self, filename=None, name='rainbow',
                 size=32, alpha=0.0, data_range=(0, 255),
                 continuous_update=False, on_change=None):
        self.palette = list()
        self.alpha_sliders = list()
        self.color_pickers = list()
        self.continuous_update = continuous_update
        self.data_range = data_range
        self.send_updates_to_renderer = True
        self._on_change = on_change

        if filename is None:
            # Initialize palette from seaborn
            self.palette.clear()
            for color in sns.color_palette(name, size):
                self.palette.append([color[0], color[1], color[2], alpha])
        else:
            # Load palette from file
            self._load(filename)

        # Create control and assign palette
        self._create_controls()
        self._update_controls()
        self._callback()

    def _load(self, filename):
        # Clear controls
        self.alpha_sliders.clear()
        self.color_pickers.clear()

        # Read colormap file
        lines = tuple(open(filename, 'r'))
        self.palette.clear()
        for line in lines:
            words = line.split()
            if len(words) == 4:
                r = float(words[0])
                g = float(words[1])
                b = float(words[2])
                a = float(words[3])
                color = [r, g, b, a]
                self.palette.append(color)

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(str(len(self.palette)) + '\n')
            for color in self.palette:
                f.write(str(color[0]) + ' ' + str(color[1]) + ' ' + str(color[2]) + ' ' + str(color[3]) + '\n')
            f.close()

    def set_palette(self, name):
        size = len(self.palette)
        newPalette = sns.color_palette(name, size)
        for i in range(size):
            color = newPalette[i]
            self.palette[i] = [color[0], color[1], color[2], self.palette[i][3]]
        self._update_controls()
        self._callback()

    def set_range(self, range):
        self.data_range = range
        self._callback()

    def _html_color(self, index):
        color = self.palette[index]
        color_as_string = '#' \
                          '%02x' % (int)(color[0] * 255) + \
                          '%02x' % (int)(color[1] * 255) + \
                          '%02x' % (int)(color[2] * 255)
        return color_as_string

    def _update_colormap(self, change):
        self._callback()

    def _update_colorpicker(self, change):
        for i in range(len(self.palette)):
            self.alpha_sliders[i].style.handle_color = self.color_pickers[i].value
        self._callback()

    def _create_controls(self):
        self.send_updates_to_renderer = False
        # Layout
        alpha_slider_item_layout = Layout(
            overflow_x='hidden', height='180px', max_width='20px')
        color_picker_item_layout = Layout(
            overflow_x='hidden', height='20px', max_width='20px')
        box_layout = Layout(display='inline-flex', flex_flow='row wrap')

        # Sliders
        self.alpha_sliders = [widgets.IntSlider(
            continuous_update=self.continuous_update,
            layout=alpha_slider_item_layout,
            description=str(i),
            orientation='vertical',
            readout=True,
            value=self.palette[i][3] * 256, min=0, max=255, step=1
        ) for i in range(len(self.palette))]

        # Color pickers
        self.color_pickers = [
            ColorPicker(
                layout=color_picker_item_layout,
                concise=True,
                disabled=False) for i in range(len(self.palette))
        ]
        # Display controls
        color_box = Box(children=self.color_pickers)
        alpha_box = Box(children=self.alpha_sliders)
        box = VBox([color_box, alpha_box], layout=box_layout)

        # Attach observers
        for i in range(len(self.palette)):
            self.alpha_sliders[i].observe(self._update_colormap, names='value')
            self.color_pickers[i].observe(self._update_colorpicker, names='value')
        display(box)
        self.send_updates_to_renderer = True

    def _update_controls(self):
        self.send_updates_to_renderer = False
        for i in range(len(self.palette)):
            color = self._html_color(i)
            self.alpha_sliders[i].style.handle_color = color
            self.color_pickers[i].value = color
        self.send_updates_to_renderer = True

    def _callback(self):
        from webcolors import name_to_rgb, hex_to_rgb

        if not self.send_updates_to_renderer:
            return

        for i in range(len(self.palette)):
            try:
                color = name_to_rgb(self.color_pickers[i].value)
            except ValueError:
                color = hex_to_rgb(self.color_pickers[i].value)

            c = [
                float(color.red) / 255.0,
                float(color.green) / 255.0,
                float(color.blue) / 255.0,
                float(self.alpha_sliders[i].value) / 255.0
            ]
            self.palette[i] = c

        if self._on_change:
            self._on_change(self)

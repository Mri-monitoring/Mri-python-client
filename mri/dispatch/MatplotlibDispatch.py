from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from future import standard_library
standard_library.install_aliases()
import logging
import os

from .BaseDispatch import BaseDispatch

try:
    import matplotlib.pyplot as plt
    import numpy as np
    IMPORTED = True
except Exception as e:
    logging.warning('Failed to import numpy or matplotlib. Are you sure they are properly installed?')
    logging.warning('You can ignore this warning if you do not plan to use Matplotlib')
    logging.warning(e)
    IMPORTED = False


class MatplotlibDispatch(BaseDispatch):
    """Display events via Matplotlib backend. This class requires some heavy dependencies, and so
    trying to run it without Matplotlib and Numpy installed will result in pass-thru behavior

    Arguments
    ---------
    task_params : dict
        Dictionary of the task json specification, including name and ID number

    img_folder : string
        Folder to save output images to
    """
    def __init__(self, task_params, img_folder):
        super().__init__()
        # Data will be a dictionary of lists
        self._data = {}
        self.task_params = task_params
        self._img_folder = img_folder

    def setup_display(self, time_axis, attributes, show_windows=False):
        if IMPORTED:
            super().setup_display(time_axis, attributes)
            # Setup data
            for item in self._attributes:
                if item != self._time_axis:
                    self._data[item] = []
            # Setup plotting
            plt.figure(figsize=(12, 10))
            if show_windows:
                plt.ion()
                plt.show()
        else:
            logging.error('You need Matplotlib and Numpy to run the MatplotlibDispatch, please install them')

    def train_event(self, event):
        """Plot a basic training and testing curve via Matplotlib

        Arguments
        ---------
        event : TrainingEvent.TrainingEvent
            Event to add to Matplotlib plot
        """
        if IMPORTED:
            super().train_event(event)

            time = event.attributes[event.time_axis]
            for item in event.attributes:
                if item != event.time_axis:
                    val = event.attributes[item]
                    self._data[item].append([time, val])

            # Convert to numpy arrays
            np_data = []
            mins = {}
            maxes = {}
            for key in self._data:
                if self._data[key]:
                    data = np.array(self._data[key])
                    mins[key] = np.min(data, axis=0)[1]
                    maxes[key] = np.max(data, axis=0)[1]
                    np_data.append(data[:, 0])
                    np_data.append(data[:, 1])

            plt.clf()
            plt.plot(*np_data)
            legend_keys = []
            for k in self._data.keys():
                text = "{} (".format(k.title())
                if k in maxes:
                    text += "Max: {} ".format(maxes[k])
                if k in mins:
                    text += "Min: {}".format(mins[k])
                text += ")"
                legend_keys.append(text)

            ax = plt.gca()
            box = ax.get_position()
            ax.set_position([box.x0, box.y0 + box.height * 0.1,
                             box.width, box.height*0.9])
            plt.legend(legend_keys,
                       bbox_to_anchor=(0.5, -0.05),
                       loc='upper center',
                       ncol=2,
                       borderaxespad=0.)
            plt.title(self.task_params['title'])
            plt.grid(True, which='both')
            plt.draw()
        else:
            logging.error('Improper requirements, skipping train event')

    def train_finish(self):
        """Save our output figure to PNG format, as defined by the save path `img_folder`"""
        if IMPORTED:
            filename = self.task_params['title'].replace(' ', '_')
            save_path = os.path.join(self._img_folder, filename)
            logging.info('Finished training! Saving output image to {0}'.format(save_path))
            plt.savefig(save_path, bbox_inches='tight', format='png')
            plt.close()
        else:
            logging.error('Improper requirements, skipping train finish')

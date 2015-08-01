from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from future import standard_library
standard_library.install_aliases()
import logging
import requests
import json

from .BaseDispatch import BaseDispatch
from mri.utilities import ServerConsts, send_request


class MriServerDispatch(BaseDispatch):
    """Display events via the mri-Server front-end. For this dispatch, we will treat
    each task as a separate report. There may be multiple visualizations on the server
    for a report, and there may be multiple directives in a task. These two, however, aren't
    necessarily bijective. Each dispatch is isolated from the server itself to emphasize the
    stateless nature of the monitoring tool and avoid deadlikes and the like. That means that
    to perform actions like clearing the server or clearing a specific visualization you'll need
    to create an MriServer class instead.

    Arguments
    ---------
    task_params : dict
        Dictionary of the task json specification, including title and ID number

    address : string
        Server address, generally a hosted URL

    username : string
        Username for the mri-server

    password : string
        Password for the mri-server
    """
    def __init__(self, task_params, address, username, password):
        super().__init__()
        self.task_params = task_params
        self.address = address
        self.auth = (username, password)
        self.report_id = None

    def setup_display(self, time_axis, attributes):
        """Create a report for this dispatch, usually done at init

        Arguments
        ---------
        time_axis : string
            Name of attribute representing time eg. iterations, epoch, etc

        attributes : list
            List of strings representing attributes to plot eg. loss, accuracy,
            learning rate, etc. If time_axis attribute is present it will be ignored.

        Returns
        -------
        result : requests.Response
            Result of the report creation request
        """
        super().setup_display(time_axis, attributes)
        report_json = self._new_report()
        if 'id' in report_json:
            self.report_id = report_json['id']
        elif 'data' in report_json:
            # This is for unit testing
            self.report_id = ''
        return self._format_report()

    def train_event(self, event):
        """Dispatch training events to the mri-server via REST interface

        Arguments
        ---------
        event : TrainingEvent
            Info for this training event

        event_url : string
            URI to send post events to in mri-server (shouldn't need to change)

        Returns
        -------
        result : requests.Response
            Result of the training event request
        """
        super().train_event(event)
        payload = self._format_train_request(event)
        result = self._send_request(ServerConsts.API_URL.EVENT, 'POST', payload)
        return result

    def train_finish(self):
        """Final call for training, can be used to issue alerts/etc. Currently unused."""
        pass

    def _send_request(self, suffix, protocol, data):
        """Send a report via HTTP, but allow for non-responsive or dead servers. Fill
        in information from the class to reduce the burden on the caller."""
        url = requests.compat.urljoin(self.address, suffix)
        auth = self.auth
        return send_request(url, protocol, data, auth)

    def _format_report(self):
        """Called after creating a new report, formats a report to display mri events"""
        if not self.setup:
            raise ValueError('Dispatch not setup yet, please call setup_report')
        full_url = requests.compat.urljoin(ServerConsts.API_URL.REPORT_ID, self.report_id)
        # Compile fields, etc
        attr_no_time = self._attributes
        attr_no_time.remove(self._time_axis)
        fields = ','.join(attr_no_time)
        scales = ','.join(['auto'] * len(attr_no_time))
        sample = self._time_axis

        # Add training visualizations
        payload = json.dumps({
            'title': self.task_params['title'],
            'visualizations': [
                {
                    'type': 'plot',
                    'eventName': 'train.'+self.task_params['id'],
                    'configuration': {
                        'title': 'Training Progress',
                        'sample': sample,
                        'fields': fields,
                        'scales': scales,
                        'limit': 100000,
                        'size': 'big',
                        'interpolation': 'linear'
                    }
                }
            ]
        })
        result = self._send_request(full_url, 'PUT', payload)
        return result

    def _new_report(self):
        """Called during init, creates a new report on the server and returns its ID"""
        payload = json.dumps({'title': self.task_params['title']})
        result = self._send_request(ServerConsts.API_URL.REPORT, 'POST', payload).text
        result_obj = json.loads(result)
        return result_obj

    def _format_train_request(self, train_event):
        """Generate the payload for the train request"""
        event_type = 'train.{0}'.format(self.task_params['id'].replace(' ', ''))
        properties = train_event.attributes
        payload = {
            'type': event_type,
            'properties': properties
        }
        return json.dumps(payload)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
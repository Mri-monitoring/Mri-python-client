import urllib.parse

from mri.utilities import send_request
from mri.dispatch import MriServerDispatch


class MriServer(object):
    def __init__(self, address, username, password):
        """MriServer is a high level object that interfaces with an instance of Mri-server

        Arguments
        ----------
        address : string
            URL of the server to connect to

        username : string
            Server username

        password : string
            Server password
        """
        self.address = address
        self.auth = (username, password)

    def new_dispatch(self, task):
        """Creates a new dispatch based on the passed task. The dispatch is standalone, so this class will not have
        any information about it or its state.

        Arguments
        ----------
        task : dict
            A dictionary defining a task. At the minimum must have a name and a unique ID
        """
        return MriServerDispatch(task, self.address, self.auth[0], self.auth[1])

    def wipe_database(self):
        """Completely wipe the database of the server, which includes events, reports, and alerts

        Arguments
        ----------
        None

        Returns
        ----------
        result : requests.Response
            Response from the server, includes response code, encoding, and text
        """
        endpoint = urllib.parse.urljoin(self.address, "/api/data")
        return send_request(endpoint, "DELETE", None, self.auth)

    def delete_report(self, report_id):
        """Remove a report from the database by ID

        Arguments
        ----------
        report_id : string
            ID of the report to remove. This ID is accessible from an MriServerDispatch instance under `report_id`

        Returns
        ----------
        result : requests.Response
            Response from the server, includes response code, encoding, and text
        """
        endpoint = urllib.parse.urljoin(self.address, "/api/report/" + report_id)
        return send_request(endpoint, "DELETE", None, self.auth)

import urllib.parse

from mri.utilities import send_request
from mri.dispatch import MriServerDispatch


class MriServer(object):
    """MriServer is a high level object that interfaces with an instance of Mri-server. This
    class allows management of the server itself. Unlike MriServerDispatch where a new instance is
    created for each report, one of these instances represents one server endpoint.

    Arguments
    ----------
    address : string
        URL of the server to connect to

    username : string
        Server username

    password : string
        Server password
    """
    def __init__(self, address, username, password):
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

    def get_reports(self):
        """Get a list of reports on this server

        Arguments
        ----------
        None

        Returns
        ----------
        reports : dict
            List of reports, in format {id: title}
        """
        endpoint = urllib.parse.urljoin(self.address, "/api/reports")
        req = send_request(endpoint, "GET", None, self.auth)
        reports = {}
        for r in req.json():
            reports[r['id']] = r['title']
        return reports

    def search_reports(self, title):
        """Search for reports by title on this server

        Arguments
        ----------
        title : string
            Name of the report to find

        Returns
        ----------
        ids : list
            List of ids matching the title
        """
        ids = []
        reports = self.get_reports()
        for id_val, name in reports.items():
            if name == title:
                ids.append(id_val)
        return ids

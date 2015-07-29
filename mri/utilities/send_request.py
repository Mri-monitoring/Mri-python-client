import requests
import logging


def send_request(address, protocol, data, auth):
    """Send an HTTP request

    Arguments
    ----------
    address : string
        Full address for this request

    protocol : string
        HTTP protocol request to make

    data : dict
        JSON object of data to pass in the request

    auth : tuple
        (username, pass) for server

    Returns
    ----------
    result : requests.Response
        Response from the server, includes response code, encoding, and text
    """
    headers = {'Content-Type': 'application/json'}
    try:
        protocol = protocol.upper()
        result = requests.request(method=protocol, url=address, data=data, headers=headers, auth=auth)
        logging.info('Sent request, result {0}'.format(result.status_code))
        if result.status_code != 200:
            logging.warning('Request not 200, server says {0}'.format(result.text))
    except requests.exceptions.ConnectionError as ex:
        logging.warning('Failed to send request because of a network problem')
        logging.warning('Message from exception: {0}'.format(ex))
        return None
    except requests.exceptions.ConnectTimeout as ex:
        logging.warning('Failed to send request because the server timed out')
        logging.warning('Message from exception: {0}'.format(ex))
        return None
    return result

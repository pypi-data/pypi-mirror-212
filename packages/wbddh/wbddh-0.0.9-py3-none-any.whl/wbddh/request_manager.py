import requests
from .exceptions import *

public_API_URL = "https://ddhoutboundapiuat.asestg.worldbank.org"

def get(endpoint, params=None, headers=None, session=None):
    '''Send a GET request

    Arguments:
        endpoint:		the endpoint (e.g., "datasets")
        params:			parameters
        headers:		additional headers

    Returns:
        a Response object (from the requests package)
    '''
    if session:
        session.check_tokens()
        return requests.get(get_endpoint(endpoint, session), params=params, verify=session.verify, headers=session.get_headers(headers))
    else:
        return requests.get(get_endpoint(endpoint), params=params)

def try_get(endpoint, params=None, headers=None, session=None, num_try=3, interval=300):
    '''Repeat sending a GET request until it succeeds or it tries {num_try} times

    Additional arguments:
        num_try:        number of tries
        interval:       interval between tries in seconds
    '''
    count = 0
    while True:
        try:
            count = count + 1
            if session:
                session.check_tokens()
                return requests.get(get_endpoint(endpoint, session), params=params, verify=session.verify, headers=session.get_headers(headers))
            else:
                return requests.get(get_endpoint(endpoint), params=params)
        except requests.exceptions.RequestException as e:
            print (f"[{count} try] Error: ", e)
            if count > num_try:
                raise Exception(f"Request failed after {count} tries.")
            continue

    
def post(endpoint, params=None, json=None, headers=None, session=None):
    '''Send a POST request

    Arguments:
        endpoint:		the endpoint (e.g., "dataset/listpage")
        json:			data object
        params:			query parameters
        headers:		additional headers

    Returns:
        a Response object (from the requests package)
    '''
    if session:
        session.check_tokens()
        return requests.post(get_endpoint(endpoint, session), params=params, json=json, verify=session.verify, headers=session.get_headers(headers))
    else:
        raise DDHSessionException("DDH POST request requires a session")

def try_post(endpoint, params=None, json=None, headers=None, session=None, num_try=3, interval=300):
    '''Repeat sending a POST request until it succeeds or it tries {num_try} times

    Additional arguments:
        num_try:        number of tries
        interval:       interval between tries in seconds
    '''
    if session:
        count = 0
        while True:
            try:
                count = count + 1
                session.check_tokens()
                return requests.post(get_endpoint(endpoint, session), params=params, json=json, verify=session.verify, headers=session.get_headers(headers))
            except requests.exceptions.RequestException as e:
                print (f"[{count} try] Error: ", e)
                if count > num_try:
                    raise Exception(f"Request failed after {count} tries.")
                continue
                        
    else:
        raise DDHSessionException("DDH POST request requires a session")

def post_file(endpoint, files=None, headers=None, session=None):
    '''Send a POST request with file

    Arguments:
        endpoint:		the endpoint (e.g., "dataset/listpage")
        files:			multi-part form object
        headers:		additional headers

    Returns:
        a Response object (from the requests package)
    '''
    if session:
        session.check_tokens()
        return requests.post(get_endpoint(endpoint, session), files=files, verify=session.verify, headers=session.get_headers(headers))
    else:
        raise DDHSessionException("DDH POST request requires a session")


def get_endpoint(endpoint, session=None):
    if session:
        return '/'.join([session.api_host, endpoint.strip()])
    else:
        return '/'.join([public_API_URL, endpoint.strip()])
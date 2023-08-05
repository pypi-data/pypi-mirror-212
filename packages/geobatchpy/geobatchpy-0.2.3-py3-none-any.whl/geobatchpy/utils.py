import json
import logging
import os
from pathlib import Path
from typing import Union, Dict, Any, List

API_GEOCODE = '/v1/geocode/search'
API_REVERSE_GEOCODE = '/v1/geocode/reverse'
API_PLACE_DETAILS = '/v2/place-details'
API_PLACES = '/v2/places'
API_BATCH = '/v1/batch'
API_ISOLINE = '/v1/isoline'
API_BOUNDARIES_PART_OF = '/v1/boundaries/part-of'
API_BOUNDARIES_CONSISTS_OF = '/v1/boundaries/consists-of'
API_ROUTE_MATRIX = '/v1/routematrix'

Json = Union[Dict[str, Any], List[Any]]  # A superset of the JSON specification, excluding atomic objects


def get_api_key(api_key: str = None, env_variable_name: str = 'GEOAPIFY_KEY') -> str:
    """Simply passes the first argument if not None else returns value of environment variable.

    Args:
        api_key: API key or None.
        env_variable_name: If api_key is None, returns instead the value of the environment variable.

    Returns:
        API key as a string.
    """
    if api_key is None:
        try:
            api_key = os.environ[env_variable_name]
        except KeyError:
            logging.error(f'Set the --key option or set the key in the \'{env_variable_name}\' environment variable.')
            raise
    return api_key


def get_api_url(api: str, api_key: str = None, version: int = None) -> str:
    if api_key is None:
        api_key = get_api_key()
    if version is None:
        # Use version as defined above
        return f'https://api.geoapify.com{api}?apiKey={api_key}'
    else:
        api = f'/v{version}/' + '/'.join(api.split('/')[2:])
        return f'https://api.geoapify.com{api}?apiKey={api_key}'


def read_data_from_json_file(file_path: Union[str, Path]) -> Json:
    """Reads data from a JSON file.

    Json = Union[Dict[str, Any], List[Any]] is a superset of the JSON specification, excluding scalar objects.

    Arguments:
        file_path: path to the JSON file.

    Returns:
        The Python equivalent of the JSON object.
    """
    with open(Path(file_path), 'r') as f:
        data = json.load(fp=f)
    logging.info(f'File \'{file_path}\' read from disk.')
    return data


def write_data_to_json_file(data: Json, file_path: Union[str, Path]) -> None:
    """Writes data to a JSON file.

    Json = Union[Dict[str, Any], List[Any]] is a superset of the JSON specification, excluding scalar objects.

    Arguments:
        data: an object of Json type.
        file_path: destination path of the JSON file.
    """
    with open(Path(file_path), 'w') as f:
        json.dump(data, fp=f, indent=4)
    logging.info(f'File \'{file_path}\' written to disk.')

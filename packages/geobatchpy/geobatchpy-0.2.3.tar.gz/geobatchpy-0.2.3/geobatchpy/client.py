"""A Python client for the Geoapify API.

"""
import logging
from typing import Dict, List, Tuple, Union

import requests

from geobatchpy.batch import BatchClient
from geobatchpy.boundaries import BoundariesClient
from geobatchpy.utils import (
    get_api_key, get_api_url, API_GEOCODE, API_REVERSE_GEOCODE, API_PLACES, API_PLACE_DETAILS, API_ISOLINE,
    API_ROUTE_MATRIX
)


class Client:

    def __init__(self, api_key: str):
        self._api_key = get_api_key(api_key=api_key)
        self.batch = BatchClient(api_key=api_key)
        self.boundaries = BoundariesClient(api_key=api_key)
        self._headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self._logger = logging.getLogger(__name__)

    def places(self, categories: Union[str, List[str]], filter_by_region: str = None,
               filter_by_name: str = None, proximity_by: Tuple[float, float] = None,
               conditions: Union[str, List[str]] = None, limit: int = 20, offset: int = None,
               language: str = None) -> dict:
        """Query locations of different categories.

        See the Geoapify API documentation for a full list of categories and any other supported parameters.

        Arguments:
            categories: returned places must be in one of the chosen categories.
            filter_by_region: places must be within boundaries of the specified geometry.
            filter_by_name: places' names are used for filtering.
            proximity_by: (lon, lat) tuple; places will be returned in order of proximity to the coordinates.
            conditions: places must fulfill all of the provided conditions.
            limit: maximal number of places returned.
            offset: return next places by starting counting from `offset`.
            language: iso code of the language in which places should be returned.

        Returns:
            List of places encoded in JSON like dictionaries.
        """
        request_url = get_api_url(api=API_PLACES, api_key=self._api_key)
        params = dict()
        if isinstance(categories, str):
            params['categories'] = categories
        else:
            params['categories'] = ','.join(categories)
        if filter_by_region is not None:
            params['filter'] = filter_by_region
        if filter_by_name is not None:
            params['name'] = filter_by_name
        if proximity_by is not None:
            params['bias'] = f'proximity:{proximity_by[0]},{proximity_by[1]}'
        if isinstance(conditions, str):
            params['conditions'] = conditions
        elif conditions is not None:
            params['conditions'] = ','.join(conditions)

        params['limit'] = limit
        params['offset'] = offset
        if language is not None:
            params['lang'] = language

        return requests.get(url=request_url, params=params, headers=self._headers).json()

    def place_details(self, place_id: str = None, longitude: float = None, latitude: float = None,
                      features: List[str] = None, language: str = None) -> dict:
        """Returns place details of a location.

        Use either the `place_id` (returned by geocoding) or geo coordinates to specify a location. The `features`
        argument specifies which kind of details to request. See the geoapify.com documentation.

        Arguments:
            place_id: the Nominatim place_id as a string.
            latitude: float or string representing latitude.
            longitude: float or string representing longitude.
            features: list of types of details. Defaults to just ["details"] if not specified.
            language: 2-character iso language code.

        Returns:
            Structured location details.
        """
        request_url = get_api_url(api=API_PLACE_DETAILS, api_key=self._api_key)
        params = dict()
        if place_id is not None:
            params['id'] = place_id
        elif latitude is not None and longitude is not None:
            params['lat'] = str(latitude)
            params['lon'] = str(longitude)
        else:
            raise ValueError('Either place_id or latitude and longitude must be provided.')
        if features is not None:
            params['features'] = ','.join(features)
        if language is not None:
            params['lang'] = language

        return requests.get(url=request_url, params=params, headers=self._headers).json()

    def geocode(self, text: str = None, parameters: Dict[str, str] = None) -> dict:
        """Returns geocoding results as a dictionary.

        Use either a free text search wit the `text` argument or alternatively provide input in a structured
        form using the `parameters` argument. See the geoapify.com API documentation.

        Arguments:
            text: free text search of a location.
            parameters: structured search as key value pairs and other optional parameters.

        Returns:
            Structured, geocoded, and enriched address record.
        """
        request_url = get_api_url(api=API_GEOCODE, api_key=self._api_key)

        params = {'text': text} if text is not None else dict()
        if parameters is not None:
            params = {**params, **parameters}

        return requests.get(url=request_url, params=params, headers=self._headers).json()

    def reverse_geocode(self, longitude: float, latitude: float) -> dict:
        """Returns reverse geocoding results as a dictionary.

        Arguments:
            latitude: float representing latitude.
            longitude: float representing longitude.

        Returns:
            Structured, reverse geocoded, and enriched address record.
        """
        request_url = get_api_url(api=API_REVERSE_GEOCODE, api_key=self._api_key)
        params = {'lat': str(latitude), 'lon': str(longitude)}

        return requests.get(url=request_url, params=params, headers=self._headers).json()

    def isoline(self, longitude: float, latitude: float, travel_range: int,
                travel_mode: str = 'drive', isoline_type: str = 'time', output_format: str = 'geojson') -> dict:
        """Returns isoline results as a dictionary.

        Args:
            longitude: float representing longitude.
            latitude: float representing latitude.
            travel_range: either travel time in seconds or travel distance in meters, depending on `isoline_type`.
            travel_mode: one of the many supported 'mode's - see the Geoapify API docs.
            isoline_type: either 'time' or 'distance'.
            output_format: one of 'geojson', 'topojson', 'geobuf'.

        Returns:
            Structured isoline details.
        """
        request_url = get_api_url(api=API_ISOLINE, api_key=self._api_key)
        params = {'lon': str(longitude), 'lat': str(latitude), 'range': travel_range, 'mode': travel_mode,
                  'type': isoline_type, 'format': output_format}
        return requests.get(url=request_url, params=params, headers=self._headers).json()

    def route_matrix(self, source_geocodes: List[Tuple[float, float]],
                     target_geocodes: List[Tuple[float, float]] = None,
                     travel_mode: str = 'drive', ) -> dict:
        """Returns route matrix results as a dictionary.

        `target_geocodes = None` translates to `target_geocodes = source_geocodes`.

        Args:
            source_geocodes: list of (lon, lat) tuples of source locations.
            target_geocodes: list of (lon, lat) tuples of target locations or None.
            travel_mode: one of 'drive', 'truck', 'walk', 'bicycle'.

        Returns:

        """
        request_url = get_api_url(api=API_ROUTE_MATRIX, api_key=self._api_key)
        if target_geocodes is None:
            target_geocodes = source_geocodes
        data = {
            'mode': travel_mode,
            'sources': [{'location': geocode} for geocode in source_geocodes],
            'targets': [{'location': geocode} for geocode in target_geocodes]
        }
        return requests.post(url=request_url, json=data, headers=self._headers).json()

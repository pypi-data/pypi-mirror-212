import requests
import time

class APIResource:
    """Class that is used to represent something that will be returned from the api

    Attributes
    ----------
    api : LordOfTheRings
        The instance of the LordOfTheRings class that this resource will use to make requests
    endpoint : str
        The endpoint associated with this API resource
    id : str, optional
        The id of the resource you wish to get from the api.

    """
    def __init__(self, api, endpoint, id=None):
        """Initialize an APIResource instance.

        Parameters
        ----------
        api : LordOfTheRings
            The instance of the LordOfTheRings class that this resource will use to make requests.
        endpoint : str
            The endpoint associated with this API resource.
        id : str, optional
            The unique identifier of this resource (default is None).

        """
        self.api = api
        self.endpoint = endpoint
        self.id = id

    def get_all(self):
        """Fetch all resources of this type

        Returns
        -------
        ChainableMethods
            An instance of ChainableMethods to allow for option chaining like filtering, sorting, or pagination.

        """
        return ChainableMethods(self)

    def get(self):
        """Fetch a single resource by the id of the resource

        Returns
        -------
        dict
            The JSON response with the data from the resource that was queried

        Raises
        ------
        Exception
            If the ID of the resource has not been set.

        """
        if self.id:
            return self.api.request('GET', f'{self.endpoint}/{self.id}')
        else:
            raise Exception('Resource ID not provided')
        
class ChainableMethods:
    """Class to allow chainable methods on a resource.

    Attributes
    ----------
    resource : APIResource
        The resource that will have method chaining.
    params : dict
        A dictionary of parameters for the API request.

    """
    def __init__(self, resource):
        """Initialize a ChainableMethods instance.

        Parameters
        ----------
        resource : APIResource
            The resource on which the methods should be chained.

        """
        self.resource = resource
        self.params = {}

    def limit(self, limit):
        """Set the limit parameter for the request, limitting the amount of records returned by the api

        Parameters
        ----------
        limit : int
            The maximum number of results to return.

        Returns
        -------
        ChainableMethods
            The current instance to allow method chaining.

        """
        self.params['limit'] = limit
        return self

    def page(self, page):
        """Set the page parameter for the request, specifying which page of results should be returned

        Parameters
        ----------
        page : int
            The page of results to return.

        Returns
        -------
        ChainableMethods
            The current instance to allow method chaining.

        """
        self.params['page'] = page
        return self

    def offset(self, offset):
        """Set the offset parameter for the request.

        Parameters
        ----------
        offset : int
            The number of results to skip before starting to fetch.

        Returns
        -------
        ChainableMethods
            The current instance to allow method chaining.

        """
        self.params['offset'] = offset
        return self

    def filter_by(self, **filters):
        """Set filter parameters for the request.

        Parameters
        ----------
        **filters : dict
            The filters to apply to the request.

        Returns
        -------
        ChainableMethods
            The current instance to allow method chaining.

        """
        for key, value in filters.items():
            if isinstance(value, str):
                # match
                self.params[key] = value
            elif isinstance(value, tuple):
                if value[0] == 'not':
                    # negate match
                    self.params[f"{key}!"] = value[1]
                elif value[0] in ('<', '>'):
                    # less than, greater than or equal to
                    self.params[f"{key}{value[0]}"] = value[1]
            elif isinstance(value, list):
                if all(isinstance(v, str) for v in value):
                    # include
                    self.params[key] = ','.join(value)
                elif all(isinstance(v, tuple) and v[0] == 'not' for v in value):
                    # exclude
                    self.params[f"{key}!"] = ','.join(v[1] for v in value)
        return self
    
    def sort_by(self, sort_by):
        """Set the sort parameter for the request.

        Parameters
        ----------
        sort_by : str
            The field by which to sort the results. For example, name:asc

        Returns
        -------
        ChainableMethods
            The current instance to allow method chaining.

        """
        self.params['sort'] = sort_by
        return self

    def fetch(self):
        """Make the API request and return the response.

        Returns
        -------
        dict
            The JSON response from the server.

        """
        return self.resource.api.request('GET', self.resource.endpoint, params=self.params)

class Movie(APIResource):
    """A class representing a movie resource.
    
    Attributes
    ----------
    quotes : Quotable
        A Quotable instance composed with the movie, allowing the user to get quotes for a particular movie
    """
    def __init__(self, api, id=None):
        """Initialize a Movie instance.

        Parameters
        ----------
        api : LordOfTheRings
            The main API instance.
        id : str, optional
            The ID of the movie. 
        """
        endpoint = 'movie'
        super().__init__(api, endpoint, id)
        self.quotes = Quotable(api, endpoint, self.id)

class Quote(APIResource):
    """A class representing a quote resource."""
    def __init__(self, api, id=None):
        """Initialize a Quote instance.

        Parameters
        ----------
        api : LordOfTheRings
            The main API instance.
        id : str, optional
            The ID of the quote.
        """
        endpoint = 'quote'
        super().__init__(api, endpoint, id)

class Quotable(APIResource):
    """A class representing a quotable resource, that can have quotes in the form of {resource}/{id}/quote"""
    def __init__(self, api, parent_endpoint, parent_id):
        """Initialize a Quotable instance.

        Parameters
        ----------
        api : LordOfTheRings
            The main API instance.
        parent_endpoint : str
            The endpoint of the parent resource.
        parent_id : str
            The ID of the parent resource.
        """
        super().__init__(api, f'{parent_endpoint}/{parent_id}/quote')

class LordOfTheRings:
    """The client for interfacing with the Lord of The Rings API.

    Attributes
    ----------
    base_url : str
        The base URL for the API.
    auth_token : str
        The authentication token for the API.
    session : requests.Session
        The session for making HTTP requests.
    max_retries : int
        The maximum number of retries when a request fails.
    failure_delay : int
        The delay (in seconds) between retries.
    """
    def __init__(self, auth_token, max_retries=3, failure_delay=1):
        """Initialize a LordOfTheRings client instance.

        Parameters
        ----------
        auth_token : str
            The authentication token for the API.
        max_retries : int, optional
            The maximum number of retries when a request fails.
        failure_delay : int, optional
            The delay (in seconds) between retries.
        """
        self.base_url = 'https://the-one-api.dev/v2/'
        self.auth_token = auth_token
        self.session = requests.Session()
        self.max_retries = max_retries
        self.failure_delay = failure_delay
        if auth_token:
            self.session.headers.update({'Authorization': f'Bearer {auth_token}'})

    def request(self, method, endpoint, **kwargs):
        """Send a request to the API.

        Parameters
        ----------
        method : str
            The HTTP method ('GET', 'POST', etc.).
        endpoint : str
            The API endpoint (excluding the base URL).
        **kwargs
            Any other parameters to pass to requests.Session.request.

        Returns
        -------
        dict
            The JSON response from the API.

        Raises
        ------
        Exception
            If the request fails after max_retries.
        """
        url = f'{self.base_url.rstrip("/")}/{endpoint.lstrip("/")}'
        for _ in range(self.max_retries):
            response = self.session.request(method, url, **kwargs)
            if response.status_code == 429:  # Rate limit error
                print("Rate limit reached. Retrying...")
                time.sleep(self.failure_delay)
                continue
            elif response.status_code >= 500: # Server error
                print("Server error. Retrying...")
                time.sleep(self.failure_delay)
                continue
            elif response.status_code >= 400: # Client error
                raise Exception(f'Request failed with status {response.status_code}')
            else:
                return response.json()
        raise Exception('Max retries exceeded')
    
    def movies(self, id=None):
        """Get a movie resource.

        Parameters
        ----------
        id : str, optional
            The ID of the movie.

        Returns
        -------
        Movie
            A Movie instance.
        """
        return Movie(self, id)

    def quotes(self, id=None):
        """Get a quote resource.

        Parameters
        ----------
        id : str, optional
            The ID of the quote.

        Returns
        -------
        Quote
            A Quote instance.
        """
        return Quote(self, id)
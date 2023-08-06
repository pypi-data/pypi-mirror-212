import unittest
from unittest.mock import patch, Mock
from lordoftherings import LordOfTheRings
import requests

class TestLordOfTheRings(unittest.TestCase):
    def setUp(self):
        self.auth_token = 'YOUR API TOKEN'
        self.api = LordOfTheRings(self.auth_token)

    # Test the authorization header being set properly
    def test_authorization_header(self):
        api = LordOfTheRings('test-token')
        self.assertEqual(api.session.headers['Authorization'], 'Bearer test-token')

    # Testing /movie
    @patch('lordoftherings.lordoftherings.LordOfTheRings.request')
    def test_get_all_movies(self, mock_request):
        self.api.movies().get_all().fetch()
        mock_request.assert_called_once_with('GET', 'movie', params={})

    # Testing /movie/{id}
    @patch('lordoftherings.lordoftherings.LordOfTheRings.request')
    def test_get_movie(self, mock_request):
        movie_id = '5cd95395de30eff6ebccde56'
        self.api.movies(movie_id).get()
        mock_request.assert_called_once_with('GET', f'movie/{movie_id}')

    # Testing /movie/{id}/quote
    @patch('lordoftherings.lordoftherings.LordOfTheRings.request')
    def test_get_movie_quotes(self, mock_request):
        movie_id = '5cd95395de30eff6ebccde56'
        self.api.movies(movie_id).quotes.get_all().fetch()
        mock_request.assert_called_once_with('GET', f'movie/{movie_id}/quote', params={})

    # Testing /quote
    @patch('lordoftherings.lordoftherings.LordOfTheRings.request')
    def test_get_all_quotes(self, mock_request):
        self.api.quotes().get_all().fetch()
        mock_request.assert_called_once_with('GET', 'quote', params={})

    # Testing /quote/{id}
    @patch('lordoftherings.lordoftherings.LordOfTheRings.request')
    def test_get_quote(self, mock_request):
        quote_id = '5cd96e05de30eff6ebccfb2b'
        self.api.quotes(quote_id).get()
        mock_request.assert_called_once_with('GET', f'quote/{quote_id}')

    # Testing pagination when just the limit() function is used
    @patch.object(requests.Session, 'request')
    def test_limit_pagination(self, mock_request):
        mock_request.return_value = Mock(ok=True, status_code=200, json=lambda: {'docs': []})
        limit = 5
        self.api.movies().get_all().limit(limit).fetch()
        mock_request.assert_called_once_with('GET', f'{self.api.base_url}movie', params={'limit': limit})

    # Testing pagination when just the page() function is used
    @patch.object(requests.Session, 'request')
    def test_page_pagination(self, mock_request):
        mock_request.return_value = Mock(ok=True, status_code=200, json=lambda: {'docs': []})
        page = 2
        self.api.movies().get_all().page(page).fetch()
        mock_request.assert_called_once_with('GET', f'{self.api.base_url}movie', params={'page': page})

    # Testing pagination when just the offset() function is used
    @patch.object(requests.Session, 'request')
    def test_offset_pagination(self, mock_request):
        mock_request.return_value = Mock(ok=True, status_code=200, json=lambda: {'docs': []})
        offset = 10
        self.api.movies().get_all().offset(offset).fetch()
        mock_request.assert_called_once_with('GET', f'{self.api.base_url}movie', params={'offset': offset})

    # Testing pagination when all functions for pagination are used together
    @patch.object(requests.Session, 'request')
    def test_combined_pagination(self, mock_request):
        mock_request.return_value = Mock(ok=True, status_code=200, json=lambda: {'docs': []})
        limit = 5
        page = 2
        offset = 10
        self.api.movies().get_all().limit(limit).page(page).offset(offset).fetch()
        mock_request.assert_called_once_with('GET', f'{self.api.base_url}movie', params={'limit': limit, 'page': page, 'offset': offset})

    # Testing filtering match
    @patch.object(requests.Session, 'request')
    def test_filtering_match(self, mock_request):
        mock_request.return_value = Mock(ok=True, status_code=200, json=lambda: {})
        self.api.movies().get_all().filter_by(name="The Lord of the Rings Series").fetch()
        mock_request.assert_called_once_with('GET', f'{self.api.base_url}movie', params={'name': 'The Lord of the Rings Series'})

    # Testing filtering negate match
    @patch.object(requests.Session, 'request')
    def test_filtering_negate_match(self, mock_request):
        mock_request.return_value = Mock(ok=True, status_code=200, json=lambda: {})
        self.api.movies().get_all().filter_by(name=('not', 'Frodo')).fetch()
        mock_request.assert_called_once_with('GET', f'{self.api.base_url}movie', params={'name!': 'Frodo'})

    # Testing filtering includes
    @patch.object(requests.Session, 'request')
    def test_filtering_includes(self, mock_request):
        mock_request.return_value = Mock(ok=True, status_code=200, json=lambda: {})
        self.api.movies().get_all().filter_by(name=['The Lord of the Rings Series', 'The Desolation of Smaug']).fetch()
        mock_request.assert_called_once_with('GET', f'{self.api.base_url}movie', params={'name': 'The Lord of the Rings Series,The Desolation of Smaug'})
    
    # Testing filtering excludes
    @patch.object(requests.Session, 'request')
    def test_filtering_excludes(self, mock_request):
        mock_request.return_value = Mock(ok=True, status_code=200, json=lambda: {})
        self.api.movies().get_all().filter_by(name=[('not', 'The Lord of the Rings Series'), ('not', 'The Desolation of Smaug')]).fetch()
        mock_request.assert_called_once_with('GET', f'{self.api.base_url}movie', params={'name!': 'The Lord of the Rings Series,The Desolation of Smaug'})

    # Testing filtering less than
    @patch.object(requests.Session, 'request')
    def test_filtering_less_than(self, mock_request):
        mock_request.return_value = Mock(ok=True, status_code=200, json=lambda: {})
        self.api.movies().get_all().filter_by(budgetInMillions=('<', 100)).fetch()
        mock_request.assert_called_once_with('GET', f'{self.api.base_url}movie', params={'budgetInMillions<': 100})

    # Testing filtering greater than
    @patch.object(requests.Session, 'request')
    def test_filtering_greater_than(self, mock_request):
        mock_request.return_value = Mock(ok=True, status_code=200, json=lambda: {})
        self.api.movies().get_all().filter_by(runtimeInMinutes=('>', 160)).fetch()
        mock_request.assert_called_once_with('GET', f'{self.api.base_url}movie', params={'runtimeInMinutes>': 160})

    # Testing sorting with only the sort_by() function
    @patch.object(requests.Session, 'request')
    def test_sorting(self, mock_request):
        mock_request.return_value = Mock(ok=True, status_code=200, json=lambda: {})
        self.api.movies().get_all().sort_by('name:desc').fetch()
        mock_request.assert_called_once_with('GET', f'{self.api.base_url}movie', params={'sort': 'name:desc'})

    # Testing status code 429 to check that rate limits have been handled
    @patch.object(requests.Session, 'request', side_effect=[Mock(ok=False, status_code=429, json=lambda: {})]*4)
    def test_rate_limit_error_handling(self, mock_request):
        with self.assertRaises(Exception) as context:
            self.api.movies('5cd95395de30eff6ebccde56').get()
        self.assertTrue('Max retries exceeded' in str(context.exception))
        self.assertEqual(mock_request.call_count, self.api.max_retries)

    # Testing status code 500 for server errors
    @patch.object(requests.Session, 'request', side_effect=[Mock(ok=False, status_code=500, json=lambda: {})]*4)
    def test_server_error_handling(self, mock_request):
        with self.assertRaises(Exception) as context:
            self.api.movies('5cd95395de30eff6ebccde56').get()
        self.assertTrue('Max retries exceeded' in str(context.exception))
        self.assertEqual(mock_request.call_count, self.api.max_retries)

    # Testing the status code 400 for client errors when calling the api
    @patch.object(requests.Session, 'request', return_value=Mock(ok=False, status_code=400))
    def test_client_error_handling(self, mock_request):
        with self.assertRaises(Exception) as context:
            self.api.movies('5cd95395de30eff6ebccde56').get()
        self.assertTrue('Request failed with status 400' in str(context.exception))

if __name__ == '__main__':
    unittest.main()

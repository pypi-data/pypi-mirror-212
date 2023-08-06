''' Loggers '''
import logging
from os import getenv
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

AUDIT_LOG_CLIENT_LOGGER = 'py-audit-logger-client'
RETRY_COUNT = int(getenv('AUDITLOG_CONNECTION_RETRY_COUNT', '5'))
BACKOFF_FACTOR = float(getenv('AUDITLOG_CONNECTION_BACKOFF_FACTOR', '1'))
TIMEOUT = getenv('AUDITLOG_CONNECTION_TIMEOUT', None)

class ConsoleLogger: # pylint: disable=too-few-public-methods
    ''' ConsoleLogger '''
    @staticmethod
    def log(message, endpoint):
        ''' Print to standart out '''
        print('{0}: {1}'.format(endpoint, message)) # pylint: disable=superfluous-parens

class HttpLogger: # pylint: disable=too-few-public-methods
    ''' HttpLogger '''

    def __init__(self, plan):
        self._plan = plan
        self._request_back_off_factor = BACKOFF_FACTOR
        self._request_retry_count = RETRY_COUNT
        self._request_timeout = TIMEOUT

        logging.basicConfig()
        self._logger = logging.getLogger(__name__)

    def log(self, message, endpoint):
        ''' Send message to service '''
        url = self._plan.url() + endpoint
        self._logger.debug('>>> URL: %s, message:%s', url, message)
        session = self._get_retriable_session()
        req_options = self._plan.auth()
        _add_request_content_type(req_options)
        response = session.post(
            url, json=message, timeout=self._request_timeout, **req_options)
        session.close()

        _check_status_code(response, url)

    def _get_retriable_session(self):
        session = requests.Session()
        retry = Retry(
            total=self._request_retry_count,
            backoff_factor=self._request_back_off_factor,
            status_forcelist=[404, 502, 503, 504],
            allowed_methods=['POST']
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session


def _add_request_content_type(req_options):
    if "headers" not in req_options:
        req_options['headers'] = {}
    req_options['headers']['Content-Type'] = 'application/json'


def _check_status_code(response, url):
    if response.status_code not in [200, 201, 204]:
        raise RuntimeError(
            'Unexpected status code {0} while requesting {1}. Response from server: {2}'
            .format(response.status_code, url, response.text)
        )

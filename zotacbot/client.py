import urllib.parse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tenacity import (
    retry as tenacity_retry,
    retry_if_exception,
    wait_fixed,
    stop_after_attempt,
)

# (avoid multiple of 3s for connect timeout for TCP to align with TCP retransmission timing - 2.5-3s)
DEFAULT_TIMEOUT = (61, 60)  # Connect & Read timeout (NOT overall request timeout)
MAX_RETRY_ATTEMPTS = 3
BACKOFF_FACTOR = 2
MAX_CONNECTION_ATTEMPTS = 3
WAIT_TILL_NEXT_CONNECTION_ATTEMPT = 0.33


def _requests_retry_session(
    retries=MAX_RETRY_ATTEMPTS,
    backoff_factor=BACKOFF_FACTOR,
    status_forcelist=(500, 502, 503, 504, 429),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    adapter.max_retries.respect_retry_after_header = False
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def should_retry(exc):
    return isinstance(exc, requests.RequestException) and (
        500 <= exc.response.status_code < 600
    )


def is_absolute_url(url):
    return url.startswith("http://") or url.startswith("https://")


class Client(requests.Session):
    def __init__(self, base=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _requests_retry_session(session=self)
        self.base = base

    def get_absolute_url(self, endpoint):
        if not self.base or is_absolute_url(endpoint):
            return endpoint
        else:
            # "/" is by default a safe character in urllib.parse.quote()
            return self.base.strip("/") + "/" + urllib.parse.quote(endpoint.strip("/"))

    @tenacity_retry(
        retry=retry_if_exception(should_retry),
        wait=wait_fixed(WAIT_TILL_NEXT_CONNECTION_ATTEMPT),
        stop=stop_after_attempt(MAX_CONNECTION_ATTEMPTS),
        reraise=True,
    )
    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
        **kwargs
    ):
        # URL may just be the endpoint or an entire URL
        url = self.get_absolute_url(url)
        timeout = timeout or DEFAULT_TIMEOUT
        resp = super().request(
            method,
            url,
            params,
            data,
            headers,
            cookies,
            files,
            auth,
            timeout,
            allow_redirects,
            proxies,
            hooks,
            stream,
            verify,
            cert,
            json,
        )
        resp.raise_for_status()
        return resp

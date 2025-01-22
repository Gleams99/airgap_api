import http
import logging

import requests
import urllib.parse
from urllib.parse import urlparse
from urllib.parse import parse_qs
from loguru import logger
from tenacity import after_log, before_log, retry, retry_if_exception_type, stop_after_attempt, wait_exponential


def log_summary(r, *args, **kwargs) -> None:
    summary = f"[{r.request.method}]{r.url} = {r.status_code} in {r.elapsed}"
    logger.debug(summary)


def log_response_json(r, *args, **kwargs) -> None:
    try:
        response_json = r.json()
        logger.debug(response_json)
    except requests.exceptions.JSONDecodeError:
        pass


class RateLimitReachedError(Exception):
    """Raised when API rate limit reached."""


class BaseAPIClient:
    def __init__(self, *, base_url: str, headers: dict[str, str] | None = None) -> None:
        self._base_url = base_url
        self._session = requests.Session()
        self._session.headers = headers
        self._session.hooks['response'].extend([log_summary, log_response_json])

    @staticmethod
    def include_page_param(*, parameters: dict | None, page: int | None = None):
        if parameters is None:
            parameters = {}
        if page:
            parameters["page"] = page
        return parameters

    @staticmethod
    def extract_parameter_value(*, url: str, parameter_name: str):
        parsed_url = urlparse(url)
        try:
            return parse_qs(parsed_url.query)[parameter_name][0]
        except (KeyError, IndexError):
            return None

    def make_url(self, *, url):
        return urllib.parse.urljoin(self._base_url, url)

    @retry(
        stop=stop_after_attempt(10),
        wait=wait_exponential(multiplier=1, min=5, max=20),
        retry=retry_if_exception_type(exception_types=RateLimitReachedError),
        reraise=True,
        before=before_log(logger, logging.DEBUG),
        after=after_log(logger, logging.DEBUG)
    )
    def get(self, *, url: str, page: int | None = None, **kwargs):
        params = self.include_page_param(parameters=kwargs.pop("params", None), page=page)
        response = self._session.get(url=self.make_url(url=url), params=params, **kwargs)
        if response.status_code == http.HTTPStatus.TOO_MANY_REQUESTS:
            raise RateLimitReachedError()
        return response

    @retry(
        stop=stop_after_attempt(10),
        wait=wait_exponential(multiplier=1, min=5, max=20),
        retry=retry_if_exception_type(exception_types=RateLimitReachedError),
        reraise=True,
        before=before_log(logger, logging.DEBUG),
        after=after_log(logger, logging.DEBUG)
    )
    def post(self, *, url: str, **kwargs):
        response = self._session.post(url=self.make_url(url=url), **kwargs)
        if response.status_code == http.HTTPStatus.TOO_MANY_REQUESTS:
            raise RateLimitReachedError()
        return response

    @retry(
        stop=stop_after_attempt(10),
        wait=wait_exponential(multiplier=1, min=5, max=20),
        retry=retry_if_exception_type(exception_types=RateLimitReachedError),
        reraise=True,
        before=before_log(logger, logging.DEBUG),
        after=after_log(logger, logging.DEBUG)
    )
    def patch(self, *, url: str, **kwargs):
        response = self._session.patch(url=self.make_url(url=url), **kwargs)
        if response.status_code == http.HTTPStatus.TOO_MANY_REQUESTS:
            raise RateLimitReachedError()
        return response

    @retry(
        stop=stop_after_attempt(10),
        wait=wait_exponential(multiplier=1, min=5, max=20),
        retry=retry_if_exception_type(exception_types=RateLimitReachedError),
        reraise=True,
        before=before_log(logger, logging.DEBUG),
        after=after_log(logger, logging.DEBUG)
    )
    def delete(self, *, url: str, **kwargs):
        response = self._session.delete(url=self.make_url(url=url), **kwargs)
        if response.status_code == http.HTTPStatus.TOO_MANY_REQUESTS:
            raise RateLimitReachedError()
        return response

    def get_all_pages(self, *, url: str, **kwargs):
        next_page = 1
        while next_page:
            logger.info(f"Getting page: {next_page}")
            response = self.get(url=url, page=next_page, **kwargs).json()
            yield response.get("data", [])
            next_url = response.get("links", {}).get("next")
            next_page = self.extract_parameter_value(url=next_url, parameter_name="page")

import logging

from playwright.sync_api import APIRequestContext, APIResponse

log = logging.getLogger(__name__)


class BaseClient:
    """Thin wrapper over Playwright's APIRequestContext.

    The context already holds base_url and default headers, so clients only
    pass paths. Every request is logged to reports/test.log for debugging.
    """

    def __init__(self, request: APIRequestContext):
        self.request = request

    def _send(self, method: str, path: str, **kwargs) -> APIResponse:
        response = self.request.fetch(path, method=method, **kwargs)
        log.info("%s %s -> %s", method, path, response.status)
        return response

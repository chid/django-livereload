"""
Middleware for injecting the live-reload script.
"""
import re

from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import smart_str


SCRIPT_TAG = '<script src="http://localhost:35729/livereload.js"></script>'
HEAD_CLOSE_RE = re.compile(r'</head\s*>', re.IGNORECASE)
SCRIPT_PRESENT_RE = re.compile(
    r'<script\b[^>]*\bsrc=["\']http://localhost:35729/livereload\.js["\']',
    re.IGNORECASE,
)


class LiveReloadScript(MiddlewareMixin):
    """
    Inject the live-reload script into your webpages.
    """

    def process_response(self, request, response):
        if response.status_code != 200:
            return response

        content_type = response.get(
            'Content-Type', '').split(';')[0].strip().lower()
        if content_type not in ['text/html', 'application/xhtml+xml']:
            return response

        content = smart_str(response.content)

        if SCRIPT_PRESENT_RE.search(content):
            return response

        match = HEAD_CLOSE_RE.search(content)
        if not match:
            return response

        response.content = content[:match.start()] + SCRIPT_TAG + content[match.start():]
        return response

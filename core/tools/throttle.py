import time

from rest_framework.throttling import AnonRateThrottle


class AnonThrottle(AnonRateThrottle):
    """Overrides original timer method.

    Why?
    https://github.com/encode/django-rest-framework/pull/7955

    """

    def timer(self):
        return time.time()

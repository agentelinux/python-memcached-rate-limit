#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from hashlib import sha1
from distutils.version import StrictVersion
#from redis.exceptions import NoScriptError
#from redis import Redis, ConnectionPool
from google.appengine.api import memcache


__version__ = "0.0.1"

MEMCACHE_NAMESPACE='rate_limiter'



class MemcacheWriteError(Exception):
    """Error thrown when memcache compare and set fails too many times."""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class TooManyRequests(Exception):
    """
    Occurs when the maximum number of requests is reached for a given resource
    of an specific user.
    """
    pass


class RateLimit(object):
    """
    This class offers an abstraction of a Rate Limit algorithm implemented on
    top of Redis >= 2.6.0.
    """
    def __init__(self, resource, client, max_requests, expire=None):
        """
        Class initialization method checks if the Rate Limit algorithm is
        actually supported by the installed Redis version and sets some
        useful properties.

        If Rate Limit is not supported, it raises an Exception.

        :param resource: resource identifier string (i.e. ‘user_pictures’)
        :param client: client identifier string (i.e. ‘192.168.0.10’)
        :param max_requests: integer (i.e. ‘10’)
        :param expire: seconds to wait before resetting counters (i.e. ‘60’)
        """
        self._memcached = memcache.Client()

        self._rate_limit_key = "rate_limit:{0}_{1}".format(resource, client)
        self._max_requests = max_requests
        self._expire = expire or 1

    def __enter__(self):
        self.increment_usage()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_usage(self):
        """
        Returns actual resource usage by client. Note that it could be greater
        than the maximum number of requests set.

        :return: integer: current usage
        """
        return int(self._memcached.get(self._rate_limit_key, namespace=MEMCACHE_NAMESPACE) or 0)

    def has_been_reached(self):
        """
        Checks if Rate Limit has been reached.

        :return: bool: True if limit has been reached or False otherwise
        """
        return self.get_usage() >= self._max_requests

    def increment_usage(self):
        """
        Calls a LUA script that should increment the resource usage by client.

        If the resource limit overflows the maximum number of requests, this
        method raises an Exception.

        :return: integer: current usage
        """        
        current_usage = self._memcached.gets(self._rate_limit_key , namespace=MEMCACHE_NAMESPACE)
        
        if int(current_usage) > self._max_requests:
            raise TooManyRequests()

        return current_usage

    def _is_rate_limit_supported(self):
        """
        Checks if Rate Limit is supported which can basically be found by
        looking at Redis database version that should be 2.6.0 or greater.

        :return: bool
        """
        pass

    def _reset(self):
        """
        Deletes all keys that start with ‘rate_limit:’.
        """
        self._memcached.delete_multi_async(self._rate_limit_key ,namespace=MEMCACHE_NAMESPACE)


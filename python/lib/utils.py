#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['utils']

import json
from datetime import time
from functools import reduce
import time
import datetime

import requests

__create__ = '2018. 01. 05'
__author__ = 'ZUM internet'


class HTTP:
    """ Wrapper http class, based requests library ( http://docs.python-requests.org/en/master/ )
    """
    __host = 'cse.zum.com'
    __port = 80
    __api = '/'
    __method = 'GET'
    __data = None
    __timeout = 5

    def __init__(self, _host, _port, _api, _method, _data, _timeout=5000):
        self.__host = _host
        self.__port = int(_port)
        self.__api = _api
        self.__method = _method
        self.__data = _data
        self.__timeout = _timeout

    def __del__(self):
        pass

    def get_request_obj(self):
        return 'http://' + self.__host + ':' + str(self.__port) + self.__api + ' || ' + self.__method + ' || ' + str(
            self.__timeout) + ' || ' + json.dumps(self.__data)

    def get_url(self):
        return 'http://' + self.__host + ':' + str(self.__port) + self.__api

    def execute_request(self, headers={'Content-Type': 'application/x-www-form-urlencoded'}):
        url = self.get_url()
        try:
            if self.__method == 'POST':
                r = requests.post(url, timeout=self.__timeout, headers=headers, data={'doc': json.dumps(self.__data)})
            elif self.__method == 'PUT':
                r = requests.put(url, timeout=self.__timeout, headers=headers, data={'doc': json.dumps(self.__data)})
            elif self.__method == 'DELETE':
                r = requests.delete(url, timeout=self.__timeout)
            elif self.__method == 'GET':
                r = requests.get(url, timeout=self.__timeout)
            else:
                r = requests.get(url, timeout=self.__timeout)

            if r.status_code == 200:
                return True, r.status_code, r.text
            else:
                return False, r.status_code, r.text
        except requests.ConnectionError:
            return False, 0, 'connection error(DNS failure, refused connection, etc) is occurred.( ' + url + ' ) in ' + self.__class__.__name__ + ': execute request'
        except requests.exceptions.Timeout:
            return False,  0, 'timeout is occurred.( ' + url + ' ) in ' + self.__class__.__name__ + ': execute request'
        except requests.exceptions.RequestException as error:
            return False,  0, 'exception  (' + str(error) + ') is occurred.( ' + url + ' ) in ' + self.__class__.__name__ + ': execute request'


def list_to_str(convert_list, concat=', '):
    """ convert list to string
    """
    if isinstance(convert_list, list):
        if convert_list:
            return reduce(lambda x, y: str(x) + concat + str(y).strip() if y and str(y).strip() else str(x).strip(),
                          convert_list)
        else:
            return ''
    else:
        return convert_list


def dict_to_str(convert_dict, concat=', '):
    """ convert dict to string
    """
    if isinstance(convert_dict, dict):
        dict_to_list = lambda dic: [(k, v) for (k, v) in dic.items()]
        convert_list = dict_to_list(convert_dict)
        if convert_list:
            return reduce(lambda x, y: str(x) + concat + str(y), convert_list)
        else:
            return ''
    else:
        return convert_dict

def get_unix_time(date_time_str, date_time_format='%Y-%m-%d-%H:%M:%S'):
    """ convert date time string to unixtime.
    """
    if isinstance(date_time_str, str):
        return int(time.mktime(datetime.datetime.strptime(date_time_str, date_time_format).timetuple()))
    else:
        return date_time_str

def remove_all_space(str, concat=None):
    """ remove white space in string.
        ex)  "   123, abc, str "   --> "123,abc,str"
    """
    if concat:
        return concat.join([temp.strip() for temp in str.split(concat)])
    else:
        return str.strip()

def timed(fn):
    """ Decorator 함수 수행 시간 체크 함수.
    """
    def wrapped(*arg, **kw):
        ts = time.time()
        result = fn(*arg, **kw)
        te = time.time()

        print("[elapsed time] Function = %s, Time = %2.2f sec" % (fn.__name__, (te - ts)))

        return result

    return wrapped

#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import numbers
from urllib.parse import urlencode

from lib.utils import HTTP, get_unix_time, remove_all_space

__create__ = '2018. 01. 05'
__author__ = 'ZUM internet'


class CSE:
    """ Wrapper CSE class, document add, delete, update, update field, search document
    """
    __host = 'cse.zum.com'
    __port = 80
    __collection_id = ''
    __api_key = ''
    __method = 'GET'
    __data = None
    __timeout = 5

    def __init__(self, _host, _port, _collection_id, _api_key, _timeout=5000):
        r"""CSE search object initialize.

        :param _host: url for CSE
        :param _port: port for CSE
        :param _collection_id: collection id for user.
        :param _api_key: api key for user auth
        :param _timeout: (optional) http object timeout
        :return: result(Boolean), CSE Response Code, CSE Response Body
        """
        self.__host = _host
        self.__port = _port
        self.__collection_id = _collection_id
        self.__api_key = _api_key
        self.__timeout = _timeout

    def __del__(self):
        pass

    def add_document(self, _doc, _doc_key, _force=0):
        r"""add document.

        :param _doc: add document info (dictionary type).
        :param _doc_key: add document key.
        :param _force: (optional) add type.
        :return: result(Boolean), CSE Response Code, CSE Response Body
        """
        for field_name in ['icontents_title', 'icontents_body', 'score_regdate']:
            if field_name not in _doc:
                return False, -1, 'check doc field ("' + field_name + '"), is not exists\nthis field ("icontents_title", "icontents_body", "score_regdate") is required'

        if _force not in [0, 1]:
            _force = 0

        if not _doc_key.strip():
            return False, -1, 'document key is not exists'

        self.__method = 'POST'
        encoding_search_parm = urlencode({'dockey': _doc_key, 'force': _force})
        api = '/v2/' + self.__collection_id + '/docs?apikey=' + self.__api_key + '&' + encoding_search_parm
        data = _doc

        cse = HTTP(self.__host, self.__port, api, self.__method, data, self.__timeout)
        result, response_code, response_body = cse.execute_request()
        return result, response_code, response_body

    def delete_document(self, _doc_key):
        r"""delete document.

        :param _doc_key: delete document key.
        :return: result(Boolean), CSE Response Code, CSE Response Body
        """
        if not _doc_key.strip():
            return False, -1, 'document key is not exists'

        self.__method = 'DELETE'
        encoding_search_parm = urlencode({'dockey': _doc_key})
        api = '/v2/' + self.__collection_id + '/docs?apikey=' + self.__api_key + '&' + encoding_search_parm
        data = None
        cse = HTTP(self.__host, self.__port, api, self.__method, data, self.__timeout)
        print(cse.get_request_obj())
        result, response_code, response_body = cse.execute_request()
        return result, response_code, response_body

    def update_document(self, _doc, _doc_key):
        r"""add document.

        :param _doc: update document info (dictionary type).
        :param _doc_key: update document key.
        :return: result(Boolean), CSE Response Code, CSE Response Body
        """
        for field_name in ['icontents_title', 'icontents_body', 'score_regdate']:
            if field_name not in _doc:
                return False, -1, 'check doc field ("' + field_name + '"), is not exists\nthis field ("icontents_title", "icontents_body", "score_regdate") is required'

        if not _doc_key.strip():
            return False, -1, 'document key is not exists'

        self.__method = 'PUT'
        encoding_search_parm = urlencode({'dockey': _doc_key})
        api = '/v2/' + self.__collection_id + '/docs?apikey=' + self.__api_key + '&' + encoding_search_parm
        data = _doc

        cse = HTTP(self.__host, self.__port, api, self.__method, data, self.__timeout)
        print(cse.get_request_obj())
        result, response_code, response_body = cse.execute_request()
        return result, response_code, response_body

    def update_field(self, _doc_key, _field_name, _field_value):
        r"""update field.

        :param _doc_key: update document key.
        :param _field_name: update field name.
        :param _field_value: update field value.
        :return: result(Boolean), CSE Response Code, CSE Response Body
        """
        if not _doc_key.strip():
            return False, -1, 'document key is not exists'

        if not _field_name.strip():
            return False, -1, 'update field name is not exists'

        if not isinstance(_field_value, (numbers.Integral)):
            return False, -1, 'update value type ( number type ) is allowed'

        self.__method = 'PUT'
        encoding_search_parm = urlencode({'dockey': _doc_key, 'fieldname': _field_name, 'fieldvalue': _field_value})
        print(encoding_search_parm)
        api = '/v2/' + self.__collection_id + '/docs/fields?apikey=' + self.__api_key + '&' + encoding_search_parm
        data = None

        cse = HTTP(self.__host, self.__port, api, self.__method, data, self.__timeout)
        print(cse.get_request_obj())
        result, response_code, response_body = cse.execute_request()
        return result, response_code, response_body

    def status(self, _doc_type):
        r"""status index info.

        :param _doc_type: return doc type
        :return: result(Boolean), CSE Response Code, CSE Response Body
        """
        self.__method = 'GET'
        api = '/v2/' + self.__collection_id + '/status/' + _doc_type + '?apikey=' + self.__api_key
        data = None
        cse = HTTP(self.__host, self.__port, api, self.__method, data, self.__timeout)
        print(cse.get_request_obj())
        result, response_code, response_body = cse.execute_request()
        return result, response_code, response_body

    def search(self, _doc_type, _search_param):
        r"""update field.

         :param _doc_type: return doc type
         :param _search_param: search parameter
                             : q - querym
                               ca - category code
                               ex_ca - exclude category
                               startdate - startdate unixtime
                               enddate - enddate unixtime
                               start - search result document start number
                               len - search result document get size number
                               sort - sort type
         :return: result(Boolean), CSE Response Code, CSE Response Body
         """
        if not 'q' in _search_param:
            return False, -1, 'check search parameter, query is not exists'

        self.__method = 'GET'
        encoding_search_parm = urlencode({k: v for k, v in _search_param.items() if str(v)})
        api = '/v2/' + self.__collection_id + '/search/' + _doc_type + '?apikey=' + self.__api_key + '&' + encoding_search_parm
        data = None
        cse = HTTP(self.__host, self.__port, api, self.__method, data, self.__timeout)
        print(cse.get_request_obj())
        result, response_code, response_body = cse.execute_request()
        return result, response_code, response_body


if __name__ == '__main__':
    # CSE sample test scenario
    #  0. status index
    #  1. add document ( 5 document: test_doc_[001-005] )
    #  2. search document ( 5 document: test_doc_[001-005] )
    #  3. update document ( 1 document: test_doc_003 )
    #  4. delete document ( 1 document: test_doc_001 )
    #  5. search document ( 4 document: test_doc_[002-005] )
    #  6. update field  ( document: test_doc_004 )
    #  7. search document ( 4 document: test_doc_[002-005] )
    #  8. status index

    register_host = 'cse.zum.com'
    search_host = 'search.cse.zum.com'
    port = 80

    collection_id = '' # 발급 받은 collection id
    api_key = ''       # 발급 받은 api_key
    timeout = 10
    doc_type = 'json'

    #  0. status index
    print('0. 색인 정보를 조회합니다.')
    register_cse = CSE(register_host, port, collection_id, api_key, timeout)
    result, response_code, response_body = register_cse.status(doc_type)
    print(result, response_code, response_body)

    #  1. add document ( 5 document: test_doc_[001-005] )
    print('1. 신규 문서 5개를 입력합니다.')
    test_data = ['아침', '오전간식', '점심', '오후간식', '저녁']
    import time

    for i in range(0, 5):
        temp_name = '00' + str(i + 1)
        doc = {
            "contents_url": "http://test.cse.com/?doc=" + temp_name,
            "icontents_title": test_data[i] + "인데, 배고프다.",
            "icontents_body": test_data[i] + "밥 먹자.",
            "score_regdate": round(time.time()) + i,
            "categories": [1],
            "contents_image": "http://img.cse.com/image.jpg",
            "score_rate": i + 1,
            "score_update_field": (i + 1) * 5
        }
        doc_key = 'test_doc_' + temp_name
        force = 0
        result, response_code, response_body = register_cse.add_document(doc, doc_key, force)
        print(result, response_code, response_body)

    #  2. search document ( 5 document: test_doc_[001-005] )
    print('2. 입력 한 문서를 검색합니다.')
    search_cse = CSE(search_host, port, collection_id, api_key, timeout)

    # unix time
    start_date = '2018-12-24 00:00:00'
    end_date = '2018-12-25 23:59:59'
    startdate = get_unix_time(start_date, date_time_format='%Y-%m-%d %H:%M:%S')
    enddate = get_unix_time(end_date, date_time_format='%Y-%m-%d %H:%M:%S')

    startdate = ''
    enddate = ''
    ca = remove_all_space('   19,   56', ',')  # '   19,   56' --> '19,56'
    ca = ''
    ex_ca = ''

    search_param = {'q': '밥', 'ca': ca, 'ex_ca': ex_ca, 'startdate': startdate, 'enddate': enddate, 'start': 0,
                    'len': 30, 'sort': 1} # 해당 필드의 값이 없는 경우, 해당 필드를 제외하고 검색.

    result, response_code, response_body = search_cse.search(doc_type, search_param)
    print(result, response_code)
    print(response_body)
    # response_body is string to json
    search_result = json.loads(response_body)
    print('query:', search_param['q'], 'querytime: ', search_result['querytime'])
    print('search result docs count:', search_result['numfound'])
    docs = search_result['docs']
    for doc in docs:
        print(doc)


    #  3. update document ( 1 document: test_doc_003 )
    print('3. test_doc_003 번 문서를 업데이트 합니다.')
    update_doc = {
        "contents_url": "http://test.cse.com/?doc=006",
        "icontents_title": "점심인데, 배부르다.",
        "icontents_body": "점심 밥 다 먹었다.",
        "score_regdate": round(time.time()),
        "categories": [3],
        "contents_image": "http://img.cse.com/image.jpg",
        "score_rate": 33,
        "score_update_field": 200
    }

    doc_key = 'test_doc_003'
    result, response_code, response_body = register_cse.update_document(doc, doc_key)
    print(result, response_code, response_body)

    #  4. delete document ( 1 document: test_doc_001 )
    print('4. test_doc_001 번 문서를 삭제 합니다.')
    doc_key = 'test001'
    result, response_code, response_body = register_cse.delete_document(doc_key)
    print(result, response_code, response_body)

    #  5. search document ( 4 document: test_doc_[002-005] )
    print('5. 현재 문서(업데이트, 삭제 된)를 검색합니다.')
    result, response_code, response_body = search_cse.search(doc_type, search_param)
    print(result, response_code)
    print(response_body)
    # response_body is string to json
    search_result = json.loads(response_body)
    print('query:', search_param['q'], 'querytime: ', search_result['querytime'])
    print('search result docs count:', search_result['numfound'])
    docs = search_result['docs']
    for doc in docs:
        print(doc)

    #  6. update field  ( document: test_doc_004 )
    print('6. test_doc_004 번 문서 필드를 업데이트 합니다.')
    doc_key = 'test_doc_004'
    update_field_name = 'score_update_field'

    update_field_value = 1999
    result, response_code, response_body = register_cse.update_field(doc_key, update_field_name, update_field_value)
    print(result, response_code, response_body)

    print('6-1. field update 반영을 기다립니다....')
    time.sleep(5)

    #  7. search document ( 4 document: test_doc_002-005] )
    print('7. 현재 문서(업데이트 된 필드 문서를 확인)를 검색합니다.')
    result, response_code, response_body = search_cse.search(doc_type, search_param)
    print(result, response_code)
    print(response_body)
    # response_body is string to json
    search_result = json.loads(response_body)
    print('query:', search_param['q'], 'querytime: ', search_result['querytime'])
    print('search result docs count:', search_result['numfound'])
    docs = search_result['docs']
    for doc in docs:
        print(doc)

    #  8. status index
    print('8. 색인 정보를 조회합니다.')
    result, response_code, response_body = register_cse.status(doc_type)
    print(result, response_code, response_body)

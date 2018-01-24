# CSE (Cloud Search Engine)

줌 Cloud Search Engine (이하 CSE) 은 경쟁력 있는 콘텐츠를 갖고 있으나 검색 기능이 없는 매체 및 서비스에서 자체 검색 서비스를 제공할 수 있도록 줌의 검색기술과 자원을 이용하여 검색엔진을 API 형태로 제공하는 서비스 입니다.

## 1. requirement
##### 1) python >= 3.6.1
- [requests](http://docs.python-requests.org/en/master/)=2.18.4
- requests를 http client 사용하며, 기본적은 예외처리 및 기타 처리를 위해 HTTP class 로 한번더 wrapping  해서 사용한다. 

## 2. 사용자 등록 ( [CSE API 매뉴얼](http://dev.zum.com/search/cse_manual) 참고)
##### 1) 사용자등록을 통한 COLLECTION_ID, API_KEY 를 발급 받는다.
   
## 3. 사용법
##### 1) 객체 생성
``` 
    register_host = 'cse.zum.com'                                             //  연결할 CSE 서버 호스트 
    search_host = 'search.cse.zum.com'
    port = 80                                                                 //  연결할 CSE 서버 포트

    collection_id = 'xxxxxxxx'                                                // 사용자 등록을 통해 발급 받은 collection id
    api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'                       // 사용자 등록을 통해 발급 받은 api key
    timeout = 10                                                              // http client 에서 사용하는 타임아웃 
    doc_type = 'json'                                                         // cse 로 부터 받은 응답 문서 포맷   
    
    // 위에 정의된 정보를 통한 CSE 객체 생성
    register_cse = Search(register_host, port, collection_id, api_key, timeout)
```       
##### 2) 문서 추가
```
    // 입력할 문서를 아래와 같이 정의, dictionary 타입으로 (key/value) 로 정의
    doc = {
        "contents_url": "http://test.cse.com/?doc=005",
        "icontents_title": "아침인데, 배고프다.",
        "icontents_body": "아침밥 먹자.",
        "score_regdate": 1515394300,
        "categories": [1],
        "contents_image": "http://img.cse.com/image.jpg",
        "score_rate": 2,
        "score_update_field": 10
    }
         
    doc_key = 'test_doc_001'                                                       // 입력 할 문서 키    
    force = 0                                                                 // 입력 문서 방식  
    
    // 1) 에서 생성된 객체를 통해 위에 정의한 parameter를 같이 문서 추가 호출함
    result, response_code, response_body = register_cse.add_document(doc, doc_key, force)
    
    // 응답은 3가지로 이루어진다.
    // 호출 성공 여부, cse 서버에서 리턴되는 http code, cse 서버에서 리턴되는 http body    
    print(result, response_code, response_body)                                   
```
##### 3) 문서 검색
```
    // 검색 기간 입력 포맷은 UNIXTIMESTAMP    
    start_date = '2018-12-24 00:00:00'
    end_date = '2018-12-25 23:59:59'
    // datetime 문자열을 get_unix_time을 통해서 UNIXTIMESTAMP 로 변경 
    startdate = get_unix_time(start_date, date_time_format='%Y-%m-%d %H:%M:%S')
    enddate = get_unix_time(end_date, date_time_format='%Y-%m-%d %H:%M:%S')    
    startdate = ''
    enddate = ''
    
    // ca, ex_ca 는 ","로 구분하며, 공백 문자는 허용 하지않으므로, remove_all_space를 통해서 공백 제거
    // '   19,   56' --> '19,56' 
    ca = remove_all_space('   19,   56', ',')  
    ca = ''
    ex_ca = ''

    // 호출 옵션을 dictionary 타입으로 (key/vaelu) 로 구성해서 함수 호출에서 paramer로 사용
    // 해당 필드의 값이 없는 경우, 해당 필드를 제외하고 검색
    search_param = {'q': '밥', 'ca': ca, 'ex_ca': ex_ca, 'startdate': startdate, 'enddate': enddate, 'start': 0,
                    'len': 30, 'sort': 1}

    // 1) 에서 생성된 객체를 통해 위에 정의한 parameter를 같이 문서 검색 호출함
    result, response_code, response_body = search_cse.search(doc_type, search_param)

    // 응답은 3가지로 이루어진다.
    // 호출 성공 여부, CSE 서버에서 리턴되는 http code, CSE 서버에서 리턴되는 http body    
    print(result, response_code)
    print(response_body)
    
    // response_body은 문자열 타입으로 아래와 같이 json으로 파싱해서 쉽게 사용 가능함
    search_result = json.loads(response_body)
    print('query:', search_param['q'], 'querytime: ', search_result['querytime'])
    print('search result docs count:', search_result['numfound'])
    docs = search_result['docs']
    for doc in docs:
        print(doc)
```
##### 4) 문서 삭제
```
    // 삭제 할 문서 키
    doc_key = 'test_doc_001'
    
    // 1) 에서 생성된 객체를 통해 위에 정의한 parameter를 같이 문서 삭제 호출함
    result, response_code, response_body = register_cse.delete_document(doc_key)
    // 응답은 3가지로 이루어진다.
    // 호출 성공 여부, CSE 서버에서 리턴되는 http code, CSE 서버에서 리턴되는 http body
    print(result, response_code, response_body)
```
##### 5) 문서 업데이트
```
    // 업데이트 할 문서를 아래와 같이 정의, dictionary 타입으로 (key/vaelu) 로 정의
    update_doc = {
        "contents_url": "http://test.cse.com/?doc=005",
        "icontents_title": "점심인데, 배부르다.",
        "icontents_body": "점심 밥 다 먹었다.",
        "score_regdate": round(time.time()),
        "categories": [3],
        "contents_image": "http://img.cse.com/image.jpg",
        "score_rate": 33,
        "score_update_field": 200
    }

    // 업데이트 할 문서 키
    doc_key = 'test_doc_001'

    // 1) 에서 생성된 객체를 통해 위에 정의한 parameter를 같이 문서 업데이트 호출함
    result, response_code, response_body = register_cse.update_document(doc, doc_key)
    // 응답은 3가지로 이루어진다.
    // 호출 성공 여부, CSE 서버에서 리턴되는 http code, CSE 서버에서 리턴되는 http body    
    print(result, response_code, response_body)
```
##### 6) 문서 필드 업데이트 ( 필드 업데이트 반영은 다소 시간이 소요 되므로, 업데이트 확인은 어느정도 시간을 두고 확인 해야 한다.)
```
    // 업데이트 할 필드를 아래와 같이 정의    
    update_field_name = 'score_update_field'
    update_field_value = 1999

    // 업데이트 할 문서 키
    doc_key = 'test_doc_001'

     // 1) 에서 생성된 객체를 통해 위에 정의한 parameter를 같이 문서 필드 업데이트 호출함        
    result, response_code, response_body = register_cse.update_field(doc_key, update_field_name, update_field_value)
    // 응답은 3가지로 이루어진다.
    // 호출 성공 여부, CSE 서버에서 리턴되는 http code, CSE 서버에서 리턴되는 http body    
    print(result, response_code, response_body)    
```
##### 7) 문서 정보 조회
```
    // 1) 에서 생성된 객체를 통해 위에 정의한 parameter를 문서같이 색인정보 조회를 호출함 
    result, response_code, response_body = register_cse.status(doc_type)
    // 응답은 3가지로 이루어진다.
    // 호출 성공 여부, CSE 서버에서 리턴되는 http code, CSE 서버에서 리턴되는 http body    
    print(result, response_code, response_body)
```

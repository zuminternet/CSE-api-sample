# CSE (Cloud Search Engine)

줌 Cloud Search Engine (이하 CSE) 은 경쟁력 있는 콘텐츠를 갖고 있으나 검색 기능이 없는 매체 및 서비스에서 자체 검색 서비스를 제공할 수 있도록 줌의 검색기술과 자원을 이용하여 검색엔진을 API 형태로 제공하는 서비스 입니다.


### 1. Requirements
----------------
- Java 7 이상

- Library Dependencies
    - JSON Simpe 1.1
    - HttpClient 4.5

### 2. 사용자 등록 ([CSE API 매뉴얼](http://dev.zum.com/search/cse_manual) 참고)
-----------------------------------------------------------------------------
줌 CSE API를 사용을 위한 API 이용 신청(COLLECTION_ID, API_KEY 발급)


### 3. 사용법
---------------
**1) CSE api 객체 생성**

CSE 문서 추가, 검색, 삭제, 업데이트, 상태 확인을 수행할 api 객체 생성

```
//사용자 등록을 통해 발급 받은 apikey
String apikey="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
//사용자 등록을 통해 발급 받은 collection ID  
String collectionId="xxxxxxxx";                    

// 위의 apikey, collectionId 정보를 통해 CSEApi 객체 생성
CSEApi cse = new CSEApi(apikey, collectionId);
```

**2) CSE doc 객체 생성**

문서 추가 및 업데이트에 사용되는 CSEDoc 객체 생성
```
//문서 키 정의
String dockey="testDocKey";  
//regdate는 unixtimestamp    							       
long regdate=new Timestamp(System.currentTimeMillis()).getTime();  
CSEDoc doc=new CSEDoc(docKey);

//addField(fieldName,fieldValue)로 문서의 필드 추가
doc.addField("contents_url", "http://host/sample.html?idx=1");
doc.addField("icontents_title", "점심인데, 배고프다.");
doc.addField("icontents_body", "점심 밥 먹자.");
doc.addField("score_regdate",regdate);
doc.addField("categories", Arrays.asList(1,2));
doc.addField("contents_image", "http://img.cse.com/image.jpg");
doc.addField("score_rate", i+1);
doc.addField("score_update_field", (i+1)*5);
```

**3) 문서 추가**

*1)*에서 생성한 CSEApi 객체를 통해 force,  *2)*와 같이 생성한 CSEDoc 객체를 인자로 문서 추가 호출
```
// 문서 추가 방식에 대한 선택적 변수
int force=0;                         

//추가할 문서를 아래와 같이CSEDoc 객체로 생성, addField(key,value)로 필드 추가
CSEDoc doc=new CSEDoc(docKey);
doc.addField("contents_url", "http://host/sample.html?idx=1");
doc.addField("icontents_title", docKeys[i] + "인데, 배고프다.");
doc.addField("icontents_body", docKeys[i] + " 밥 먹자.");
doc.addField("score_regdate",regdate);
doc.addField("categories", Arrays.asList(1,2));
doc.addField("contents_image", "http://img.cse.com/image.jpg");
doc.addField("score_rate", i+1);
doc.addField("score_update_field", (i+1)*5);
String result=cse.insert(force,doc);
```

**4) 문서 검색**

```
//httpget요청의 responseType 지정(json,xml)
String responseType="json";           

//검색 변수는 아래와 같이 (key,value) 형태의 hashmap에 정의
Map<String,String> search_params=new HashMap<String,String>(){{
			put("q", "밥");
			put("start","0");
			put("len","30");
			put("sort","1");
			put("ca",null);
			put("ex_ca","4");
			put("startdate",null);
			put("enddate",null);
		}};
//1)에서 생성한 CSEApi 객체를 통해 responseType,hash map으로 정의한 parameter를 인자로 문서 검색 호출
String result=test.search(responseType, search_params);
```

**5) 문서 삭제**

삭제하려는 문서의 키 혹은 문서 객체 자체를 *1)*에서 생성한 CSEApi 객체의 삭제 인자로 전달
```
String result=cse.delete(docKey);
result=cse.delete(doc);
```
**6) 문서 업데이트**

```
//업데이트 할 문서를 아래와 같이 CSEDoc 객체로 생성, addField(key,value) 로 필드 추가
CSEDoc updateDoc=new CSEDoc(docKey);
updateDoc.addField("contents_url", "http://host/sample.html?idx=1");
updateDoc.addField("icontents_title", "점심인데, 배고프다.");
updateDoc.addField("icontents_body", "점심 밥 다먹었다.");
updateDoc.addField("score_regdate",System.currentTimeMillis()/1000);
updateDoc.addField("categories", Arrays.asList(3));
updateDoc.addField("contents_image", "http://img.cse.com/image.jpg");
updateDoc.addField("score_rate", 33);
updateDoc.addField("score_update_field", 200);

String result=cse.updateDoc(updateDoc);
```
**7) 필드 업데이트**

필드 업데이트 반영은 다소 시간이 소요 되므로, 업데이트 확인에는 어느정도 시간이 필요
```
//업데이트 할 문서의 키, 필드 이름, 필드 값을 아래와 같이 정의
String docKey="testDocKey";
String updateFieldName="score_update_field";
String updateFieldValue="1";
		
String result=cse.updateField(docKey, updateFieldName, updateFieldValue);
```
**8) 색인 정보**

*1)*에서 생성한 CSEApi 객체를 통해 responseType을 인자로 색인 정보 조회 호출
```
//httpget요청의 responseType 지정(json,xml)
String responseType="json";         
String result=cse.status("json"); 
```
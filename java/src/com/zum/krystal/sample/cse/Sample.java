package com.zum.krystal.sample.cse;

import java.sql.Timestamp;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class Sample {
	public static void main(String[] args) throws Exception {
		/*
		 * CSE sample test scenario
		 * 0. status
		 * 1. add documents (5 documents)
		 * 2. search document
		 * 3. update document
		 * 4. delete document 
		 * 5. search document
		 * 6. update field 
		 * 7. search document
		 * 8. status index
		 */
		
		String apikey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"; // 발급 받은 api key 입력
		String collectionId = "xxxxxxxx";                 // 발급 받은 collection id 입력
		String responseType;

		/*
		 * Initializes CSEApi object. Each function of CSEApi(document insert, search, delete, update, status check) 
		 * can cause ClientProtocolException, IOException that http execution failed.
		 * Each function of CSEApi return the result of each execution.(String)
		*/
		CSEApi cse = new CSEApi(apikey, collectionId);

		/* 0. status index */
		System.out.println("-----0. status index-----");
		responseType = "json";
		String result = cse.status(responseType);
		System.out.println(result);

		/* 1. add documents*/
		System.out.println("-----1. add documents-----");
		String[] docKeys = new String[] { "아침", "오전간식", "점심", "오후간식", "저녁" };
		for (int i = 0; i < 5; i++) {
			String docKey = "b00" + i;
			
			/*
			 * Initializes CSEDoc object. IllegalStateException occurs when perform CEsApi function with CSEDoc object 
			 * missing necessary fields. NecessaryFields: icontents_title, icontents_body, score_regdate
			 */
			CSEDoc doc = new CSEDoc(docKey);
			long regdate = new Timestamp(System.currentTimeMillis()).getTime();

			doc.addField("contents_url", "http://host/sample.html?idx=1");
			doc.addField("icontents_title", docKeys[i] + "인데, 배고프다.");
			doc.addField("icontents_body", docKeys[i] + " 밥 먹자.");
			doc.addField("score_regdate", regdate);
			doc.addField("categories", Arrays.asList(1, 2));
			doc.addField("contents_image", "http://img.cse.com/image.jpg");
			doc.addField("score_rate", i + 1);
			doc.addField("score_update_field", (i + 1) * 5);

			int force = 0;
			result = cse.insert(force, doc);
			System.out.println(result);
		}

		/* 2. search document */
		System.out.println("-----2. search document-----");
		responseType = "json";

		@SuppressWarnings("serial")
		Map<String, String> search_params = new HashMap<String, String>() {
			{
				put("q", "밥");
				put("start", "0");
				put("len", "30");
				put("sort", "1");
				put("ca", null);
				put("ex_ca", "4");
				put("startdate", null);
				put("enddate", null);
			}
		};

		result = cse.search(responseType, search_params);
		System.out.println(result);

		/* 3. update document */
		System.out.println("-----3. update document-----");
		String docKey = "b000";
		CSEDoc updateDoc = new CSEDoc(docKey);
		updateDoc.addField("contents_url", "http://host/sample.html?idx=1");
		updateDoc.addField("icontents_title", "점심인데, 배고프다.");
		updateDoc.addField("icontents_body", "점심 밥 다먹었다.");
		updateDoc.addField("score_regdate", System.currentTimeMillis() / 1000);
		updateDoc.addField("categories", Arrays.asList(3));
		updateDoc.addField("contents_image", "http://img.cse.com/image.jpg");
		updateDoc.addField("score_rate", 33);
		updateDoc.addField("score_update_field", 200);

		result = cse.updateDoc(updateDoc);
		System.out.println(result);

		/* 4. delete document */
		System.out.println("-----4. delete document-----");
		docKey = "b001";
		result = cse.delete(docKey);
		System.out.println(result);

		/* 5. search document */
		System.out.println("-----5. search document-----");
		result = cse.search(responseType, search_params);
		System.out.println(result);

		/* 6. update field
		 * Score field can be updated only.
		 */		 
		System.out.println("-----6. update field-----");
		docKey = "b002";
		String updateFieldName = "score_update_field";
		String updateFieldValue = "1";

		result = cse.updateField(docKey, updateFieldName, updateFieldValue);
		System.out.println(result);
		
		
		System.out.println("Field update takes time to reflect changes....");
		Thread.sleep(10000);
		
		/* 7. search document */
		System.out.println("-----7. search document-----");
		result = cse.search(responseType, search_params);
		System.out.println(result);

		/* 8. status index */
		System.out.println("-----8. status index-----");
		responseType = "json";
		result = cse.status(responseType);
		System.out.println(result);
	}
}

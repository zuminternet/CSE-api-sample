package com.zum.krystal.sample.cse;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.json.simple.JSONObject;

public class CSEDoc {
	private final String key;
	private static final String[] essentialFields=new String[]{"icontents_title","icontents_body","score_regdate"};
	private final Map<String, Object> docMap = new HashMap<String, Object>();

	public CSEDoc(String key) {
		this.key = key;
	}

	public void addField(String fieldName, Object fieldValue) {
		docMap.put(fieldName, fieldValue);
	}

	public String toJsonString() {
		JSONObject json = new JSONObject();
		for (String fieldName : docMap.keySet()) {
			json.put(fieldName, docMap.get(fieldName));
		}
		return json.toString();
	}
	
	public boolean containEssentialFields(){
		for(String essential:essentialFields){
			if(!docMap.containsKey(essential))return false;
		}
		return true;
	}
	
	public String getKey() {
		return key;
	}
}

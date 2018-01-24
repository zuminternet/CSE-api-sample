package com.zum.krystal.sample.cse;

import java.io.IOException;
import java.util.*;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpDelete;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.client.utils.URLEncodedUtils;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

public class CSEApi {
	private final String apiKey;
	private final String collectionID;
	private final HttpClient httpClient;

	private final static String register_url = "http://cse.zum.com/v2/";
	private final static String search_url = "http://search.cse.zum.com/v2/";

	private final static String charset = "UTF-8";
	private final static String updatableFieldRegex = "score_.*";
	private final static List<String> validResponseType = new ArrayList<String>(Arrays.asList("json", "xml"));
	private static final Set<String> searchParamsSet = new HashSet<String>(
			Arrays.asList(ParamsName.query, ParamsName.start, ParamsName.length, ParamsName.category,
					ParamsName.exceptCategory, ParamsName.sort, ParamsName.startDate, ParamsName.endDate));

	private class UrlPath {
		static final String search = "/search/";
		static final String insert = "/docs";
		static final String updateDoc = "/docs";
		static final String updateField = "/docs/fields";
		static final String delete = "/docs";
		static final String status = "/status/";
	}

	private class ParamsName {
		static final String apikey = "apikey";
		static final String dockey = "dockey";
		static final String doc = "doc";
		static final String force = "force";
		static final String fieldName = "fieldname";
		static final String fieldValue = "fieldvalue";
		static final String query = "q";
		static final String start = "start";
		static final String length = "len";
		static final String category = "ca";
		static final String exceptCategory = "ex_ca";
		static final String sort = "sort";
		static final String startDate = "startdate";
		static final String endDate = "enddate";
	}

	public CSEApi(String apiKey, String collectionID) {
		this.apiKey = apiKey;
		this.collectionID = collectionID;
		httpClient = HttpClientBuilder.create().build();
	}

	public String search(String responseType, Map<String, String> search_params) throws Exception {
		if (search_params == null)
			throw new IllegalArgumentException("The search parameters are not valid..");
		if (!search_params.containsKey(ParamsName.query))
			throw new IllegalStateException("The query field must be exist.");

		String url = getSearchURL(UrlPath.search + responseType);
		List<NameValuePair> params = new LinkedList<>();

		for (String param : search_params.keySet()) {
			if (searchParamsSet.contains(param) && search_params.get(param) != null)
				params.add(new BasicNameValuePair(param, search_params.get(param)));
		}

		if (!url.toString().endsWith("&"))
			url += "&";

		url += URLEncodedUtils.format(params, charset);

		HttpGet httpGet = new HttpGet(url);
		return geHttpRequestResponse(httpGet);
	}

	public String insert(CSEDoc doc) throws ClientProtocolException, IOException {
		return insert(0, doc);
	}

	public String insert(int force, CSEDoc doc) throws ClientProtocolException, IOException {
		if (doc == null) {
			throw new IllegalArgumentException("document is invalid.");
		}

		if (!doc.containEssentialFields()) {
			throw new IllegalStateException(
					"The essential fields in the document are missing. (\"icontents_title\", \"icontents_body\", \"score_regdate\") is required.");
		}

		String url = getRegisterURL(UrlPath.insert);
		HttpPost httpPost = new HttpPost(url);

		List<NameValuePair> inserteParameters = new ArrayList<>();
		inserteParameters.add(new BasicNameValuePair(ParamsName.force, String.valueOf(force)));
		inserteParameters.add(new BasicNameValuePair(ParamsName.dockey, doc.getKey()));
		inserteParameters.add(new BasicNameValuePair(ParamsName.doc, doc.toJsonString()));
		httpPost.setEntity(new UrlEncodedFormEntity(inserteParameters, charset));

		return geHttpRequestResponse(httpPost);
	}

	public String updateDoc(CSEDoc doc) throws ClientProtocolException, IOException {
		if (doc == null) {
			throw new IllegalArgumentException("document is invalid.");
		}

		if (!doc.containEssentialFields()) {
			throw new IllegalStateException(
					"The essential fields in the document are missing. (\"icontents_title\", \"icontents_body\", \"score_regdate\") is required.");
		}

		String url = getRegisterURL(UrlPath.updateDoc);
		HttpPut httpPut = new HttpPut(url);

		List<NameValuePair> updateParameters = new ArrayList<>();
		updateParameters.add(new BasicNameValuePair(ParamsName.dockey, doc.getKey()));
		updateParameters.add(new BasicNameValuePair(ParamsName.doc, doc.toJsonString()));
		httpPut.setEntity(new UrlEncodedFormEntity(updateParameters, charset));

		return geHttpRequestResponse(httpPut);
	}

	public String updateField(String dockey, String fieldName, String fieldValue)
			throws ClientProtocolException, IOException {
		if (!fieldName.matches(updatableFieldRegex)) {
			throw new IllegalArgumentException("Invalid fieldName. Score field can be updated only.");
		}

		String url = getRegisterURL(UrlPath.updateField);
		HttpPut httpPut = new HttpPut(url);

		List<NameValuePair> updateParameters = new ArrayList<>();
		updateParameters.add(new BasicNameValuePair(ParamsName.dockey, dockey));
		updateParameters.add(new BasicNameValuePair(ParamsName.fieldName, fieldName));
		updateParameters.add(new BasicNameValuePair(ParamsName.fieldValue, fieldValue));
		httpPut.setEntity(new UrlEncodedFormEntity(updateParameters, charset));

		return geHttpRequestResponse(httpPut);
	}

	public String delete(CSEDoc doc) throws ClientProtocolException, IOException {
		if (doc == null) {
			throw new IllegalArgumentException("document is invalid.");
		}
		return delete(doc.getKey());
	}

	public String delete(String dockey) throws ClientProtocolException, IOException {
		if (dockey == null) {
			throw new IllegalArgumentException("document key is not exists");
		}
		String url = getRegisterURL(UrlPath.delete);

		if (!url.endsWith("&"))
			url += "&";
		url += ParamsName.dockey + "=" + dockey;

		HttpDelete httpDelete = new HttpDelete(url);
		return geHttpRequestResponse(httpDelete);
	}

	public String status(String responseType) throws ClientProtocolException, IOException {
		if (!validResponseType.contains(responseType))
			throw new IllegalArgumentException("The response type supports only xml and json.");

		String url = getSearchURL(UrlPath.status + responseType);
		HttpGet httpget = new HttpGet(url);
		return geHttpRequestResponse(httpget);
	}

	private String geHttpRequestResponse(HttpUriRequest req) throws ClientProtocolException, IOException {
		HttpResponse response = httpClient.execute(req);
		HttpEntity respEntity = response.getEntity();
		if (respEntity == null)
			throw new IOException();
		return EntityUtils.toString(respEntity, charset);
	}

	private String getRegisterURL(String urlPath) {
		return register_url + collectionID + urlPath + "?" + ParamsName.apikey + "=" + apiKey;
	}

	private String getSearchURL(String urlPath) {
		return search_url + collectionID + urlPath + "?" + ParamsName.apikey + "=" + apiKey;
	}

}

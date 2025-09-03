import static com.kms.katalon.core.checkpoint.CheckpointFactory.findCheckpoint
import static com.kms.katalon.core.testcase.TestCaseFactory.findTestCase
import static com.kms.katalon.core.testdata.TestDataFactory.findTestData
import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import static com.kms.katalon.core.testobject.ObjectRepository.findWindowsObject
import javax.swing.*
import java.awt.*
import java.io.*
import com.kms.katalon.core.annotation.Keyword
import com.kms.katalon.core.checkpoint.Checkpoint
import com.kms.katalon.core.cucumber.keyword.CucumberBuiltinKeywords as CucumberKW
import com.kms.katalon.core.mobile.keyword.MobileBuiltInKeywords as Mobile
import com.kms.katalon.core.model.FailureHandling
import com.kms.katalon.core.testcase.TestCase
import com.kms.katalon.core.testdata.TestData
import com.kms.katalon.core.testobject.TestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.kms.katalon.core.windows.keyword.WindowsBuiltinKeywords as Windows
import com.kms.katalon.core.annotation.Keyword
import groovy.json.JsonOutput
import groovy.json.JsonSlurper
import com.kms.katalon.core.util.KeywordUtil

import internal.GlobalVariable

public class aitest {
	@Keyword
	static String flaskUrl = "http://127.0.0.1:5000/generate"
	
		@Keyword
		def static String generateTestCase(String scenario) {
			try {
				def jsonBody = JsonOutput.toJson([scenario: scenario])
				def connection = new URL(flaskUrl).openConnection()
				connection.setRequestMethod("POST")
				connection.setDoOutput(true)
				connection.setRequestProperty("Content-Type", "application/json")
				connection.getOutputStream().write(jsonBody.getBytes("UTF-8"))
	
				if (connection.responseCode == 200) {
					def responseText = connection.inputStream.text
					def jsonResponse = new JsonSlurper().parseText(responseText)
					KeywordUtil.logInfo(jsonResponse.message)
					return jsonResponse.message
				} else {
					KeywordUtil.markFailed("Failed: HTTP " + connection.responseCode)
					return null
				}
			} catch (Exception e) {
				KeywordUtil.markFailed("Exception: " + e.getMessage())
				return null
			}
		}
	}
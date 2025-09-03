import java.net.*
import java.io.*
import groovy.json.JsonOutput

// السيناريو
String userScenario = "Login with valid credentials" // ممكن تخليه متغير من واجهة لاحقًا

// بناء الـ JSON
def json = JsonOutput.toJson([scenario: userScenario])

// إعداد الاتصال بالـ API
URL url = new URL("http://127.0.0.1:5000/generate") // endpoint من Flask
HttpURLConnection connection = (HttpURLConnection) url.openConnection()
connection.setRequestMethod("POST")
connection.setRequestProperty("Content-Type", "application/json")
connection.setDoOutput(true)

// إرسال الطلب
OutputStream os = connection.getOutputStream()
os.write(json.getBytes("UTF-8"))
os.close()

// قراءة الرد
InputStream responseStream = connection.getInputStream()
BufferedReader reader = new BufferedReader(new InputStreamReader(responseStream))
String line
StringBuilder response = new StringBuilder()
while ((line = reader.readLine()) != null) {
	response.append(line)
}
reader.close()

println("✅ Response from API: " + response.toString())

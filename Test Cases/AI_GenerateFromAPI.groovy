import java.net.*
import java.io.*
import groovy.json.JsonOutput

String userScenario = "Login with valid credentials"

def json = JsonOutput.toJson([scenario: userScenario])

URL url = new URL("http://127.0.0.1:5000/generate")
HttpURLConnection connection = (HttpURLConnection) url.openConnection()
connection.setRequestMethod("POST")
connection.setRequestProperty("Content-Type", "application/json")
connection.setDoOutput(true)

OutputStream os = connection.getOutputStream()
os.write(json.getBytes("UTF-8"))
os.close()

InputStream responseStream = connection.getInputStream()
BufferedReader reader = new BufferedReader(new InputStreamReader(responseStream))
String line
StringBuilder response = new StringBuilder()
while ((line = reader.readLine()) != null) {
    response.append(line)
}
reader.close()

println("✅ Response from API: " + response.toString())
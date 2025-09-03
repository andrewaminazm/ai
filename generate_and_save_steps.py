from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    scenario = data.get('scenario', 'Login with valid credentials')

    file_content = f"""import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI

// Generated steps for scenario: {scenario}
WebUI.openBrowser('')
WebUI.navigateToUrl('http://example.com')
WebUI.setText(findTestObject('Page_Login/txt_Username'), 'user')
WebUI.setEncryptedText(findTestObject('Page_Login/txt_Password'), 'password')
WebUI.click(findTestObject('Page_Login/btn_Login'))
WebUI.verifyElementPresent(findTestObject('Page_Home/lbl_Welcome'), 10)
WebUI.closeBrowser()
"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"AI_Generated_{timestamp}.groovy"
    path = os.path.join("Test Cases", "AI_Generated")
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, filename)

    with open(filepath, "w") as f:
        f.write(file_content)

    return jsonify({"message": "✅ Test Case Generated", "file": filepath})

if __name__ == '__main__':
    app.run(debug=True)

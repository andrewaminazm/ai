from flask import Flask, request, render_template_string, jsonify
import subprocess

app = Flask(__name__)

html_template = '''
<html>
<head><title>AI Test Generator</title></head>
<body>
    <h2>أدخل السيناريو</h2>
    <input type="text" id="scenario" placeholder="مثلاً: تسجيل الدخول">
    <button onclick="generateTestCase()">توليد Test Case</button>
    <p id="result"></p>

<script>
function generateTestCase() {
    let scenario = document.getElementById("scenario").value;
    if(!scenario) {
        alert("من فضلك ادخل السيناريو");
        return;
    }
    fetch('/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({scenario: scenario})
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = data.message;
    })
    .catch(error => {
        document.getElementById("result").innerText = "حدث خطأ: " + error;
    });
}
</script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(html_template)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    scenario = data.get('scenario', '')

    try:
        result = subprocess.run(
            ['python', 'generate_and_save_steps.py', scenario],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            return jsonify({'message': 'خطأ في التوليد:\n' + result.stderr}), 500

        return jsonify({'message': 'تم توليد Test Case بنجاح!\n' + result.stdout})

    except Exception as e:
        return jsonify({'message': f'حدث استثناء: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)

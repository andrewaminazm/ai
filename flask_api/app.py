import sys
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from datetime import datetime
import os

def main():
    prompt_input = sys.argv[1] if len(sys.argv) > 1 else "Login with valid credentials"
    prompt = f"// Katalon test case to: {prompt_input}\n"

    # ✅ استخدم موديل أخف وأكثر استقرارًا
    model_id = "Salesforce/codegen2-1B"
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=256, do_sample=True, temperature=0.7)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    lines = result.split("\n")
    generated_steps = "\n".join([line for line in lines if line.strip().startswith("WebUI")])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    katalon_tests_path = os.path.join("Test Cases", "AI_Generated")
    os.makedirs(katalon_tests_path, exist_ok=True)

    file_name = f"AI_TestCase_{timestamp}.groovy"
    file_path = os.path.join(katalon_tests_path, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI\n\n")
        f.write(generated_steps)

    print(f"✅ Test case saved: {file_path}")

if __name__ == "__main__":
    main()

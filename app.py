from flask import Flask, request, jsonify
import requests
import re
import urllib.parse

app = Flask(__name__)

# Define a regex pattern to match ANSI escape codes
ansi_pattern = re.compile(r'\u001b\[[0-9;]*m')

# Define a mapping utility function
def map_type(language):
    type_map = {
        "javascript": "typescript",
        "x-java": "java",
        "x-c++src": "cpp",
        "x-c": "c",
        "x-python": "python3",
        "x-sql": "sql",
        "x-shell": "shell",
        "x-powershell": "powershell",
        "x-php": "php",
    }
    mapped_type = type_map.get(language.lower(), "unknown")
    if mapped_type == "unknown":
        raise ValueError(f"Unsupported language: {language}")
    return mapped_type


# Execute user code function
def execute_user_code(code, lang_type, stdin):
    lang_type = map_type(lang_type)
    encoded_code = code.replace("\n", "%0A").replace(" ", "%20") \
        .replace("{", "%7B").replace("}", "%7D") \
        .replace("\"", "%22").replace("\t", "")

    print(encoded_code)

    request_data = {
        "code": encoded_code,
        "type": lang_type,
        "stdin": stdin
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en-GB;q=0.7,en;q=0.6,zh-TW;q=0.5,de-DE;q=0.4,de;q=0.3",
        "Origin": "https://r.xjq.icu",
        "Priority": "u=1, i",
        "Referer": "https://r.xjq.icu/",
        "Sec-CH-UA": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\"",
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }

    response = requests.post("https://rapi.xjq.icu/code/run", json=request_data, headers=headers)
    return response.text


# Define the /codeeditor endpoint
@app.route('/codeeditor', methods=['POST'])
def codeeditor():
    try:
        code_request = request.json
        code = code_request['code']
        lang_type = code_request['type']
        stdin = code_request.get('stdin', "")

        print(f"Executing code: {code}")
        execution_result = execute_user_code(code, lang_type, stdin)
        print(f"Execution result: {execution_result}")

        return execution_result
    except Exception as e:
        return jsonify({"error": f"Code execution error: {str(e)}"}), 400


if __name__ == '__main__':
    app.run(debug=True)

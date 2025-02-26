from flask import Flask, request, jsonify, render_template_string
import json

app = Flask(__name__)

template = """
<!DOCTYPE html>
<html>
<head>
    <title>Robot Command Converter</title>
    <script>
        function copyToClipboard() {
            var outputText = document.getElementById("output").innerText;
            navigator.clipboard.writeText(outputText)
        }
    </script>
</head>
<body>
    <h2>Enter Robot Command JSON</h2>
    <form action="/convert" method="post">
        <textarea name="json_input" rows="6" cols="50">{{ input_text }}</textarea><br>
        <input type="submit" value="Convert">
    </form>
    {% if output %}
    <h3>Converted Command:</h3>
    <p id="output">{{ output }}</p>
    <button onclick="copyToClipboard()">Copy to Clipboard</button>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(template, input_text="")

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.form['json_input']
        json_data = json.loads(data)
        
        # Extract parameters
        cmd = json_data.get("cmd", "")
        rel = json_data.get("rel", 0)
        
        # Fixed parameters
        vel, accel, jerk, turn, cont = "vel", "accel", "jerk", "turn", "cont"
        
        # Determine command type and extract relevant parameters
        if cmd == "lmove":
            z = json_data.get("z", 0)
            function_string = f"robot.{cmd}(rel={rel},vel={vel},accel={accel},jerk={jerk},turn={turn},cont={cont},z={-z})"
        else:
            j_values = {key: json_data[key] for key in json_data if key.startswith("j")}
            function_string = f"robot.{cmd}(rel={rel},vel={vel},accel={accel},jerk={jerk},turn={turn},cont={cont}," \
                              + ",".join([f"{k}={v}" for k, v in j_values.items()]) + ")"
        
        return render_template_string(template, output=function_string, input_text=data)
    except Exception as e:
        return render_template_string(template, output=f"Error: {str(e)}", input_text=data)

if __name__ == '__main__':
    app.run(debug=True)

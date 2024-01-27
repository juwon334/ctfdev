from flask import Flask, render_template, request,jsonify
import base64
import re
import subprocess
import shlex

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

allowed_command_list = [
    'ping',
    'ifconfig',
]

def is_allowed_command(command):
    for pattern in allowed_command_list:
        if re.search(pattern,command,re.IGNORECASE):
            return True
    return False

def get_ifconfig_result():
    return """
lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
"""
def execute_command(command):
    parsed_command = shlex.split(command)
    arg = None

    if parsed_command[0] == 'ping' and len(parsed_command) > 1:
        arg = parsed_command[1]

    if arg is None:
        return "인자를 추가해주세요"

    if arg != "127.0.0.1":
        result = "보낼 수 없습니다."
        return result

    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"

    if f"ping {arg}" in command:
        if arg == "127.0.0.1":
            result = f"{result}Qk9CMTJERVZUT1AzMENURg=="

    return result

def get_arp_result():
    return """
arp
"""
def do_simulation(command):
    if "ifconfig" in command:
        result = get_ifconfig_result()
    elif "arp" in command:
        result = execute_command(command)
    elif "ping" in command:
        result = execute_command(command)

    return result

@app.route("/simulate", methods=["POST"])
def simulate():
    command = request.form['command']
    print("입력 명령어:", command)
    if is_allowed_command(command):
        result = do_simulation(command)
        
    else:
        result = "사용이 불가능한 명령어입니다."
    
    return render_template("index.html", command=command, result=result)

correct_answer = "BOB12DEVTOP30CTF"

@app.route('/answer',methods=['POST'])
def check_ans():
    user_input = request.form.get('ans',"")
    if user_input == correct_answer:
        return jsonify({'result': '정답입니다.'})
    else:
        return jsonify({'result': 'wrong'})

if __name__ == "__main__":
    app.run(debug=True)
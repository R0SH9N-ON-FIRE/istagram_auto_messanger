from flask import Flask, render_template, request
from threading import Thread
from messenger import send_messages
from datetime import datetime

app = Flask(__name__)
is_running = False
latest_inputs = {}
last_deploy_time = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global is_running, latest_inputs, last_deploy_time

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'run':
            if not is_running:
                is_running = True
                last_deploy_time = datetime.now().strftime('%d %B %Y, %I:%M:%S %p')
                latest_inputs = {
                    'username': request.form.get('username'),
                    'password': request.form.get('password'),
                    'targets': [u.strip() for u in request.form.get('targets').split('\n') if u.strip()],
                    'messages': [m.strip() for m in request.form.get('messages').split('\n') if m.strip()]
                }
                Thread(target=send_messages, args=(latest_inputs, lambda: is_running)).start()

        elif action == 'stop':
            is_running = False

    return render_template('index.html', running=is_running, deploy_time=last_deploy_time)

if __name__ == '__main__':
    app.run(debug=True)

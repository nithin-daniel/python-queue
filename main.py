from flask import Flask, request, jsonify, render_template
import heapq
import time
import threading
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

pq = []

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/add_task', methods=['POST'])
def add_task():
    global pg
    data = request.json
    task = (data['priority'], data['name'], data['duration'])
    heapq.heappush(pq, task)
    return jsonify({"message": "Task added successfully"}), 201


def process_next_task():    
    while pq:
        task = heapq.heappop(pq)
        print("Processing task:", task)
        time.sleep(task[2])
        socketio.emit('task_processed', {'message': task[1]})
    return jsonify({"message": "No tasks remaining"}), 200
    

@app.route('/get_task', methods=['GET'])
def get_task():
    return process_next_task()

@app.route('/start_processing', methods=['POST'])
def start_processing():
    threading.Thread(target=process_next_task).start()
    return jsonify({"message": "Task processing started"}), 200

if __name__ == '__main__':
    app.run(debug=True)

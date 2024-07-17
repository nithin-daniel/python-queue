from flask import Flask, request, jsonify
import heapq
import time
import threading

app = Flask(__name__)

pq = []

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
    return jsonify({"message": "No tasks remaining"}), 200
    
    
@app.route('/get_task', methods=['GET'])
def get_task():
    return process_next_task()

if __name__ == '__main__':
    app.run(debug=True)

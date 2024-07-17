from flask import Flask, request, jsonify
import heapq
import time
import threading

app = Flask(__name__)

# # Create a priority queue
# pq = []

# # Function to process tasks
# def process_tasks():
#     while True:
#         if pq:
#             task = heapq.heappop(pq)
#             print(f"Processing task: {task}")
#             time.sleep(task[2])
#         else:
#             time.sleep(1)  # Sleep for a second if the queue is empty

# # Start the task processing in a separate thread
# threading.Thread(target=process_tasks, daemon=True).start()

# @app.route('/add_task', methods=['POST'])
# def add_task():
#     data = request.json
#     if 'priority' in data and 'name' in data and 'duration' in data:
#         task = (data['priority'], data['name'], data['duration'])
#         heapq.heappush(pq, task)
#         return jsonify({"message": "Task added successfully"}), 201
#     return jsonify({"error": "Invalid task data"}), 400

# @app.route('/get_tasks', methods=['GET'])
# def get_tasks():
#     return jsonify(list(pq))

# if __name__ == '__main__':
#     app.run(debug=True)

import heapq
import time


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
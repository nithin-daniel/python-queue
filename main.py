from flask import Flask, request, jsonify
import time
from queue import PriorityQueue
from threading import Thread

app = Flask(__name__)

customers = PriorityQueue()

def process_queue():
    while True:
        if not customers.empty():
            priority, name, delay = customers.get()
            print((priority, name))
            time.sleep(delay)
        else:
            time.sleep(1)

queue_list = []
def log_queue_state():
    temp_queue = PriorityQueue()
    
    while not customers.empty():
        item = customers.get()
        queue_list.append({'priority': item[0], 'name': item[1], 'delay': item[2]})
        temp_queue.put(item)
    
    while not temp_queue.empty():
        customers.put(temp_queue.get())
    
    # Print the queue list to the console
    print("Queue list:", queue_list)

# Start the queue processing thread
thread = Thread(target=process_queue, daemon=True)
thread.start()

@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    name = data.get('name')
    priority = data.get('priority')
    delay = data.get('delay')
    
    if not name or not priority or not delay:
        return jsonify({'error': 'Missing data'}), 400
    
    customers.put((priority, name, delay))
    
    # Print the queue state after adding the customer
    log_queue_state()
    
    return jsonify({'message': 'Customer added'}), 200

@app.route('/queue', methods=['GET'])
def get_queue():
    temp_queue = PriorityQueue()
    queue_list = []
    
    while not customers.empty():
        item = customers.get()
        print(item)
        queue_list.append({'priority': item[0], 'name': item[1], 'delay': item[2]})
        temp_queue.put(item)
    
    while not temp_queue.empty():
        customers.put(temp_queue.get())
    
    return jsonify(queue_list)

if __name__ == '__main__':
    app.run(debug=True)

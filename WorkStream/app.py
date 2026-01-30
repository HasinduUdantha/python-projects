from flask import Flask, jsonify, request, render_template
import mysql.connector
from datetime import date

app = Flask(__name__)

# Database Configuration
db_config = {
    'user': 'root',          # Replace with your MySQL username
    'password': 'password',  # Replace with your MySQL password
    'host': 'localhost',
    'database': 'job_manager'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# 1. READ: Get all jobs (Sorted by Due Date)
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Sorting logic: Latest due dates first, as you requested before
    cursor.execute("SELECT * FROM jobs ORDER BY due_date DESC")
    jobs = cursor.fetchall()
    
    # Calculate stats for the header
    total = len(jobs)
    completed = sum(1 for job in jobs if job['status'] == 'Completed')
    
    cursor.close()
    conn.close()
    return jsonify({'jobs': jobs, 'stats': {'total': total, 'completed': completed}})

# 2. CREATE: Add a new job
@app.route('/api/jobs', methods=['POST'])
def add_job():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO jobs (title, assignee, status, due_date) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (data['title'], data['assignee'], 'Not Started', data['due_date']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Job added!'}), 201

# 3. UPDATE: Change Status or Details
@app.route('/api/jobs/<int:id>', methods=['PUT'])
def update_job(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # We allow updating specific fields dynamically
    fields = []
    values = []
    for key in ['title', 'assignee', 'status', 'due_date']:
        if key in data:
            fields.append(f"{key} = %s")
            values.append(data[key])
    
    values.append(id)
    query = f"UPDATE jobs SET {', '.join(fields)} WHERE id = %s"
    
    cursor.execute(query, tuple(values))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Job updated!'})

# 4. DELETE: Remove a job
@app.route('/api/jobs/<int:id>', methods=['DELETE'])
def delete_job(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Job deleted!'})

# Serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
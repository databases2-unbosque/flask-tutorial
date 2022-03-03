import psycopg2
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Function to connect to the database
def connecto_to_database():
    return psycopg2.connect(
        host = 'localhost',
        database = 'sala',
        user = 'postgres',
        password = 'postgres'
    )

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subjects', methods = ['POST'])
def create_subject():
    print('Creating a new subject')

    # Getting the request body in JSON format
    body = request.json
    print('Request body:', body)

    # Connecting to the database
    conn = connecto_to_database()
    
    # Executing the query and getting the result
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO subject (code, name, departmentid)
        VALUES (%s, %s, %s)
        RETURNING subjectid'''
    , (body['code'], body['name'], body['department_id'])
    )
    subject_id = cur.fetchone()[0]
    conn.commit()
    print('Subject created with id:', subject_id)

    # Closing the connection
    conn.close()

    return jsonify({'subject_id': subject_id}), 201

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)

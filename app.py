# app.py
from flask import Flask, render_template, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Get Neon PostgreSQL connection string from environment variable
DATABASE_URL = os.getenv('DATABASE_URL')

def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT availability_country FROM drugs_list ORDER BY availability_country")
        countries = [row[0] for row in cur.fetchall() if row[0] is not None]
    return render_template('index.html', countries=countries)

@app.route('/search')
def search():
    query = request.args.get('q', '').upper()
    country = request.args.get('country')
    sql = "SELECT DISTINCT drug_name FROM drugs_list WHERE UPPER(drug_name) LIKE %s"
    params = [query + '%']
    if country and country != '':
        sql += " AND UPPER(availability_country) = %s"
        params.append(country.upper())
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        results = [row[0] for row in cur.fetchall()]
    return jsonify(results)

@app.route('/drug_detail')
def drug_detail():
    name = request.args.get('name')
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM drugs_list WHERE drug_name = %s", [name])
        desc = [d.name for d in cur.description]
        row = cur.fetchone()
        if not row:
            return jsonify({'error': 'Not found'})
        data = dict(zip(desc, row))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

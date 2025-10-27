from flask import Flask, render_template, request, jsonify
import cx_Oracle

app = Flask(__name__)

dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XEPDB1")
DB_USER = "Neprology_drugs"
DB_PASS = "Das"

def get_connection():
    return cx_Oracle.connect(DB_USER, DB_PASS, dsn)

@app.route('/')
def index():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT AVAILABILITY_COUNTRY FROM drugs_list ORDER BY AVAILABILITY_COUNTRY")
        countries = [row[0] for row in cur.fetchall() if row[0] is not None]
    return render_template('index.html', countries=countries)

@app.route('/search')
def search():
    query = request.args.get('q', '').upper()
    country = request.args.get('country')  # Optionally add country filtering
    sql = "SELECT DISTINCT DRUG_NAME FROM drugs_list WHERE UPPER(DRUG_NAME) LIKE :name"
    params = {'name': query + '%'}
    if country and country != '':
        sql += " AND UPPER(AVAILABILITY_COUNTRY) = :country"
        params['country'] = country.upper()
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
        cur.execute("SELECT * FROM drugs_list WHERE DRUG_NAME = :name", {'name': name})
        desc = [d[0] for d in cur.description]
        row = cur.fetchone()
        if not row:
            return jsonify({'error': 'Not found'})
        data = dict(zip(desc, row))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

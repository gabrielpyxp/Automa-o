from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    conn = sqlite3.connect('relatorios.db')
    conn.row_factory = sqlite3.Row
    
    # Obter parâmetros de filtro
    sla_filter = request.args.get('sla_filter')
    
    # Construir consulta base
    query = "SELECT ID, NomeCliente, SLA, Abertura, Status FROM relatorios"
    params = []
    
    # Aplicar filtros
    if sla_filter == "positivo":
        query += " WHERE SLA >= 90"
    elif sla_filter == "negativo":
        query += " WHERE SLA <= 90"
    elif sla_filter == "todos":
        pass  # Sem filtro adicional
    
    # Executar consulta
    cursor = conn.execute(query, params)
    dados = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in dados])

if __name__ == '__main__':
    app.run(debug=True)
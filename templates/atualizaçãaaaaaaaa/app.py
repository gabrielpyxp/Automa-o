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
    query = "SELECT ID, NomeCliente, SLA, Abertura FROM relatorios"
    params = []
    
    # Aplicar filtros
    if sla_filter == "positivo":
        query += " WHERE SLA >= 90"
    elif sla_filter == "negativo":
        query += " WHERE SLA <= -90"  # Alterado para pegar apenas SLAs ≤ -90
    elif sla_filter == "todos":
        pass  # Sem filtro adicional
    
    # Executar consulta
    cursor = conn.execute(query, params)
    dados = cursor.fetchall()
    conn.close()
    
    # Converter para lista de dicionários e adicionar flag de alerta
    result = []
    for row in dados:
        item = dict(row)
        # Adiciona flag para destacar em vermelho (SLA ≤ -90)
        item['alerta'] = item['SLA'] is not None and float(item['SLA']) <= -90
        result.append(item)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
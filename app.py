from flask import Flask, request, jsonify, g, send_from_directory
import os
import sqlite3

app = Flask(__name__)
DATABASE = 'reservas.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                descricao TEXT NOT NULL,
                responsavel TEXT NOT NULL,
                contato TEXT NOT NULL,
                status TEXT NOT NULL,
                ultimoUsuario TEXT
            )
        ''')
        db.commit()

# Adicione esta nova rota no seu app.py
@app.route('/')
def serve_html():
    return send_from_directory(os.path.abspath(os.path.dirname(__file__)), 'index.html')


@app.route('/api/reservas', methods=['GET', 'POST'])
def handle_reservas():
    if request.method == 'POST':
        dados = request.get_json()
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO reservas (data, descricao, responsavel, contato, status, ultimoUsuario) VALUES (?, ?, ?, ?, ?, ?)",
            (dados['data'], dados['descricao'], dados['responsavel'], dados['contato'], 'Reservado', dados['ultimoUsuario'])
        )
        db.commit()
        return jsonify({"message": "Reserva adicionada com sucesso!", "id": cursor.lastrowid}), 201
    elif request.method == 'GET':
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM reservas ORDER BY data ASC")
        reservas = [dict(row) for row in cursor.fetchall()]
        return jsonify(reservas), 200

@app.route('/api/reservas/<int:reserva_id>', methods=['PUT'])
def update_reserva_completa(reserva_id):
    dados = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE reservas SET data = ?, descricao = ?, responsavel = ?, contato = ?, ultimoUsuario = ? WHERE id = ?",
        (dados['data'], dados['descricao'], dados['responsavel'], dados['contato'], dados['ultimoUsuario'], reserva_id)
    )
    db.commit()
    return jsonify({"message": f"Reserva {reserva_id} atualizada com sucesso!"}), 200

@app.route('/api/reservas/status/<int:reserva_id>', methods=['PUT'])
def update_status(reserva_id):
    dados = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE reservas SET status = ? WHERE id = ?",
        (dados['status'], reserva_id)
    )
    db.commit()
    return jsonify({"message": f"Status da reserva {reserva_id} atualizado com sucesso!"}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
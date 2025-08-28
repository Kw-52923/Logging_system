"""Flask para crear APIs web, request para peticion HTTP,jsonify convierte datos python en JSON """
from flask import Flask, request,jsonify
from datetime import datetime # Para trabajar con fechas y horas
import sqlite3
import json # para manejar datos en formato JSON 

app = Flask(__name__) # Crea instancia de la app Flask.Es como decir "Hola mundo"

# Toquens validos para autenticar servicios que envian logs
VALID_TOKENS = {
    "servicio1_token123",
    "servicio2_token456",
    "servicio3_token789"
}
DB_NAME = "logging.db" # Guarda el nombre de la BD

# Configuracion de la BD 
def init_database():
    """Inicializa la BD y crea la tabla si no existe"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    service TEXT NOT NULL,
    severity  TEXT NOT NULL,
    message  TEXT NOT NULL,
    received_at  TEXT NOT NULL,
    )
    ''')
    conn.commit()
    conn.close()

def validacion_token (auth_header):
    """Valida el token de autenticacion"""
    if not auth_header or not auth_header.startswith('Token'):
        return False
    token = auth_header[6:]
    return token in VALID_TOKENS

def save_log_to_db(log_data):
    """GUARDA UN LOG EN LA BD"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(''' 
    INSERT INTO logs (timestamp, services, severity, message, received_at)
    VALUES (?,?,?,?,?)
    ''', (
        log_data['timestamp'],
        log_data['service'],
        log_data['severity'],
        log_data['message'],
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

def get_logs_from_db(filters):
    """RECUPERA LOGS DE LA BD CON FILTROS OPCIONALES"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = "SELECT * FROM logs WHERE 1=1"
    params = []

    # Aplicar filtros
    if 'timestamp_start' in filters:
        query += "AND timestamp >= ?"
        params.append(filters['timestamp_start'])
    
    if 'timestart_end' in filters:
        query += "AND timestamp <= ?"
        params.append(filters['timestamp_end'])

    if 'received_at_start' in filters:
        query += "AND received_at >= ?"
        params.append(filters['received_at_start'])

    if 'received_at_end' in filters:
        query += "AND received_at >= ?"
        params.append(filters['received_at_end'])
    
    if 'service' in filters:
        query += "AND service = ?"
        params.append(filters['service'])
    
    if 'severity' in filters:
        query += "AND severity = ?"
        params.append(filters['severity'])
    
    query += "ORDER BY received_at DESC"

    cursor.execute(query , params )
    logs = cursor.fetchall()

    conn.close()


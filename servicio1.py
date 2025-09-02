
import requests
import random
from datetime import datetime, timedelta
import time

# Configuración
SERVER_URL = "http://localhost:5000/logs"
TOKENS = ["servicio1_token123", "servicio2_token456", "servicio3_token789"]
SERVICES = ["auth-service", "payment-service", "user-service", "inventory-service"]
SEVERITY_LEVELS = ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]

def generate_log_message(service):
    """Genera un mensaje de log aleatorio para un servicio"""
    messages = {
        "auth-service": [
            "User login successful",
            "Failed login attempt",
            "Password changed",
            "Token expired"
        ],
        "payment-service": [
            "Payment processed successfully",
            "Payment failed: insufficient funds",
            "Refund initiated",
            "Transaction timeout"
        ],
        "user-service": [
            "User profile updated",
            "New user registered",
            "User deleted",
            "Profile picture changed"
        ],
        "inventory-service": [
            "Stock level updated",
            "Low stock alert",
            "Product added",
            "Inventory sync completed"
        ]
    }
    
    return random.choice(messages.get(service, ["Event processed"]))

def generate_fake_logs(service_name, count=1):
    """Genera logs falsos para un servicio"""
    logs = []
    
    for _ in range(count):
        # Generar timestamp aleatorio en las últimas 24 horas
        random_hours = random.randint(0, 23)
        random_minutes = random.randint(0, 59)
        timestamp = (datetime.now() - timedelta(hours=random_hours, minutes=random_minutes)).isoformat()
        
        log = {
            "timestamp": timestamp,
            "service": service_name,
            "severity": random.choice(SEVERITY_LEVELS),
            "message": generate_log_message(service_name)
        }
        logs.append(log)
    
    return logs

def send_logs_to_server(logs, token):
    """Envía logs al servidor"""
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    data = {"logs": logs}
    
    try:
        response = requests.post(SERVER_URL, json=data, headers=headers)
        print(f"Response: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending logs: {e}")
        return False

def simulate_service(service_name, token, interval=5, logs_per_interval=3):
    """Simula un servicio que envía logs periódicamente"""
    print(f"Starting simulation for {service_name}...")
    
    while True:
        logs = generate_fake_logs(service_name, logs_per_interval)
        print(f"{service_name} generated {len(logs)} logs")
        
        success = send_logs_to_server(logs, token)
        if success:
            print(f"{service_name} sent logs successfully")
        else:
            print(f"{service_name} failed to send logs")
        
        time.sleep(interval)

# Ejecutar un servicio simulado
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        service_index = int(sys.argv[1]) % len(SERVICES)
        service_name = SERVICES[service_index]
        token = TOKENS[service_index % len(TOKENS)]
        
        simulate_service(service_name, token)
    else:
        print("Usage: python simulated_services.py <service_index>")
        print("Available services:")
        for i, service in enumerate(SERVICES):
            print(f"{i}: {service}")
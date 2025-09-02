# run_simulation.py
import subprocess
import sys
import time

def run_multiple_services():
    """Ejecuta múltiples servicios simulados en procesos separados"""
    processes = []
    
    # Iniciar 3 servicios diferentes
    for i in range(3):
        process = subprocess.Popen([sys.executable, "simulated_services.py", str(i)])
        processes.append(process)
        print(f"Started service {i}")
        time.sleep(1)  # Pequeña pausa entre servicios
    
    print("All services started. Press Ctrl+C to stop.")
    
    try:
        # Mantener el script ejecutándose
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping all services...")
        for process in processes:
            process.terminate()

if __name__ == '__main__':
    run_multiple_services()
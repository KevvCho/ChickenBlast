from datetime import datetime
DEBUG = False

def cambiar_modo():
    global DEBUG
    DEBUG = not DEBUG

def get_mode():
    return DEBUG

def creador_logs(e):
    now = datetime.now()

    current_time_hr = now.strftime("%H-%M-%S")
    current_time_dt = now.strftime("%d-%m-%y")

    print("Mapa no cargado")
    file = open(f"logs/{current_time_dt} LogError.txt","w")
    file.write(f"{current_time_hr} - {e}")
    file.close()

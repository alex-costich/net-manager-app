#Script patrocinado por GePeTo para simular mensajes syslog
import socket

def send_syslog_message(message, host='localhost', port=514):
    """
    Envía un mensaje syslog a un servidor y puerto específicos.
    
    Args:
        message (str): El mensaje syslog a enviar.
        host (str): La dirección IP o el nombre de host del servidor syslog. Por defecto, 'localhost'.
        port (int): El puerto en el que el servidor syslog está escuchando. Por defecto, 514.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(message.encode(), (host, port))
        print(f"Mensaje enviado a {host}:{port}: {message}")
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    # Número de mensajes a enviar
    num_messages = 6
    
    # Enviar los mensajes
    for i in range(num_messages):
        send_syslog_message(f"00:00:46: %LINK-1-UPDOWN: Interface Port-channel1, changed state to up {i+1}")
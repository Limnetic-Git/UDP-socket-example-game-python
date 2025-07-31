import socket
import ast
import time

MAX_RETRIES = 3
TIMEOUT = 1.0  # секунды

def reliable_send_receive(sock, data, address):
    """
    Надежная отправка и прием данных поверх UDP с повторными попытками
    Возвращает полученные данные или None после всех попыток
    """
    for attempt in range(MAX_RETRIES):
        try:
            sock.sendto(str.encode(str(data)), address)
            sock.settimeout(TIMEOUT)
            response, addr = sock.recvfrom(20480)
            sock.settimeout(None)
            return ast.literal_eval(response.decode('utf-8'))
        except (socket.timeout, ValueError, SyntaxError):
            print(f"Attempt {attempt + 1} failed, retrying...")
            continue
    
    print("Max retries reached, operation failed")
    return None

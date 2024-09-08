# FTP Brute Force Script

Estos script realiza un ataque de fuerza bruta a un servidor FTP y SSH utilizando una lista de contraseñas. Además, permite el uso de proxies para evadir firewalls y evitar bloqueos.

## Requisitos

- Python 3.x
- Librerías: `colorama`, `ftplib`, `socks`, `requests`

Puedes instalar las librerías necesarias con el siguiente comando:

```bash
pip3 install -r requierements.txt


1.Carga de proxies: El script puede cargar una lista de proxies desde un archivo de texto.
2.Selección de proxy aleatorio: Selecciona un proxy aleatorio de la lista cargada.
3.Verificación de proxy: Verifica si el proxy seleccionado está funcionando.
4.Configuración de proxy: Configura el proxy para las conexiones HTTP o SOCKS.
5.Ataque de fuerza bruta: Intenta conectarse al servidor FTP utilizando las contraseñas de la lista proporcionada.

Ejecución
Para ejecutar el script, utiliza el siguiente comando:

python3 ftp_bruteforce.py
python3 ssh_bruteforce.py


Parámetros
host: Dirección IP del servidor FTP objetivo.
port: Puerto del servidor FTP (por defecto es 21).
username: Nombre de usuario para el inicio de sesión.
password_file: Ruta del archivo de texto que contiene las contraseñas.
use_proxies: Indica si se deben usar proxies (Y/N).
proxy_type: Tipo de proxy (http, socks4, socks5).
proxy_ip: Dirección IP del proxy.
proxy_port: Puerto del proxy.
wait_time: Tiempo de espera entre intentos (en segundos).

Ejemplo

Introduce la IP del objetivo: 192.168.1.1
Introduce el nombre de usuario: admin
Introduce la ruta del archivo de contraseñas: passwords.txt
¿Deseas usar proxies? (Y/N): Y
Introduce el tipo de proxy (http/socks4/socks5): socks5
Introduce la IP del proxy: 127.0.0.1
Introduce el puerto del proxy: 1080
Introduce el tiempo de espera entre intentos (en segundos): 1

Este script debe ser utilizado únicamente con fines educativos y en entornos controlados. El uso no autorizado de este script en sistemas ajenos puede ser ilegal y está prohibido.

Adrian Quintero
¡Espero que te sea útil! Si necesitas alguna otra cosa, no dudes en decírmelo.

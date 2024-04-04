#!/usr/bin/python3

from concurrent.futures import ThreadPoolExecutor
import socket
import argparse
from threading import Lock, Thread
from termcolor import colored
import signal
import sys


def welcome():
    print(colored("""                                                                                                 
@@@@@@@    @@@@@@   @@@@@@@   @@@@@@@     @@@@@@@@  @@@  @@@  @@@  @@@@@@@   @@@@@@@@  @@@@@@@   
@@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@     @@@@@@@@  @@@  @@@@ @@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  
@@!  @@@  @@!  @@@  @@!  @@@    @@!       @@!       @@!  @@!@!@@@  @@!  @@@  @@!       @@!  @@@  
!@!  @!@  !@!  @!@  !@!  @!@    !@!       !@!       !@!  !@!!@!@!  !@!  @!@  !@!       !@!  @!@  
@!@@!@!   @!@  !@!  @!@!!@!     @!!       @!!!:!    !!@  @!@ !!@!  @!@  !@!  @!!!:!    @!@!!@!   
!!@!!!    !@!  !!!  !!@!@!      !!!       !!!!!:    !!!  !@!  !!!  !@!  !!!  !!!!!:    !!@!@!    
!!:       !!:  !!!  !!: :!!     !!:       !!:       !!:  !!:  !!!  !!:  !!!  !!:       !!: :!!   
:!:       :!:  !:!  :!:  !:!    :!:       :!:       :!:  :!:  !:!  :!:  !:!  :!:       :!:  !:!  
 ::       ::::: ::  ::   :::     ::        ::        ::   ::   ::   :::: ::   :: ::::  ::   :::  
 :         : :  :    :   : :     :         :        :    ::    :   :: :  :   : :: ::    :   : :                            
             .%@@@@@@@@@-                        
           @@@*        -@@@          "A FAST TCP PORT SCANNER WRITTEN IN PYTHON"           
         -@@              @@%                    
        -@@ :              #@*             github: @amezolaMartin   
        @@ #                @@             version: 1.0
        @@ #                %@.                  
        %@ =                @@                   
         @@                @@-                   
          @@*            -@@:                    
           :@@@*      =@@@@@@@+                  
               +@@@@@@*    @@@@@@=               
                            @:.@@@@-             
                              @-.@@@@*           
                                @- @@@@+         
                                  @= @@@@        
                                    @@@@# ""","red"))
    print("\n")


open_sockets = []

def def_handler(sig, frame):
    print(colored("\n[!] Saliendo del programa... ", "red"))

    for sock in open_sockets:
        try:
            sock.close()
        except Exception as e:
            print(colored(f"Error al cerrar el socket: {e}", "yellow"))
    
    sys.exit(1)

# Asigna la función de manejo de señales al evento SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, def_handler)


# Función para obtener los argumentos de la línea de comandos (como un menu)
def get_arguments():
    parser = argparse.ArgumentParser(description='Fast TCP Port Scanner')
    parser.add_argument("-t", "--target", dest="target", required=True, help="Victim targets IP (EX: -t 192.168.0.1)")
    parser.add_argument("-p", "--port", dest="port", required=True,  help="(Ex: -p 1-100 or -p22 or -p22,80,8080)")
    options = parser.parse_args()


    return options.target, options.port

# Funcion que llama mediante hilos a port_scanner (el escaneador de puertos)
def scan_ports(ports, target):
    #threads = []
    lock = Lock()
    
    with ThreadPoolExecutor(max_workers=100) as executor:  # Numero de hilos ajustable segun necesidad
        executor.map(lambda port: port_scanner(port, target, lock), ports)
        

# Funcion que hace el parseo de la entrada del usuario y devuelve iterable
def parse_ports(ports_str:str):
    
    if '-' in ports_str:
        start_port, end_port = map(int, ports_str.split('-'))
        return range(start_port, end_port+1)

    elif ',' in ports_str:
        return map(int, ports_str.split(','))
    else: # Aunque sea un puerto, devolvemos un iterable (una tupla)
        return (int(ports_str),)


# Función para crear un socket
def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)  # Establecer timeout a medio segundo
    open_sockets.append(s)
    return s

# Función para escanear un puerto
def port_scanner(port, target, lock):
    s = create_socket()
    try:
        result = s.connect_ex((target, port))
        if result == 0:
            #with lock:
            print(colored(f"[+] Port {port} is OPEN.", "green"))
        s.close()
    except Exception as e:
        pass

# Función principal
def main():
    target, ports_str = get_arguments()
    ports = parse_ports(ports_str)
    scan_ports(ports, target)


if __name__ == "__main__":
    welcome()
    main()

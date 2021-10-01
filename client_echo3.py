#!/usr/bin/python3
# Echo client program
# Version con dos threads: uno lee de stdin hacia el socket y el otro al revés
import jsockets
import sys
import os
import threading
import filecmp
import time

HOST = "anakena.dcc.uchile.cl"
PORT = 1818
TIMEOUT_SECONDS = 3

initial_time = time.perf_counter()
def Rdr(s):
    f = open(file="resultado.txt", mode="w+")  # [, newline='']

    while True:
        try:
            # max_packet_size debe ser una variable global para el interprete a la hora de invocar a Rdr en su thread.
            data = s.recv(int(max_packet_size)).decode()
        except:
            data = None
        if not data:
            break
        print(f"Servidor responde: {data}")
        f.write(data)
        s.settimeout(TIMEOUT_SECONDS)
    f.close()
    final_time = time.perf_counter()

    delta_time = final_time - initial_time
    print(f"Tiempo que tomó: {delta_time} (segundos)")

    # 
    if filecmp.cmp(filename, "resultado.txt"):
        print("Los archivos son iguales.")  
    else:
        print("Los archivos son distintos.")
        original_size = os.stat(filename).st_size
        resultado_size = os.stat("resultado.txt").st_size

        loss = original_size - resultado_size

        print(f'Hay una diferencia de {loss} en bytes entre la respuesta obtenida por el servidor y el archivo original.')



if len(sys.argv) != 3:
    print('Use: '+sys.argv[0]+' filename max_packet_size')
    sys.exit(1)

s = jsockets.socket_udp_connect(HOST, PORT)
if s is None:
    print('could not open socket')
    sys.exit(1)

# Envíamos 'Hola' encodeado en bytes para realizar el Handshake.
s.send("Hola".encode())
data = s.recv(1024).decode()    # Recibimos respuesta del server

print(f"Cliente envía: Hola")
print(f"Servidor responde: {data}")

packet_size = sys.argv[2].zfill(5).encode()
s.send(packet_size)   # Envíamos propuesta de paquetes
data = s.recv(1024).decode()            # Recibimos respuesta del server
max_packet_size = data

print(f"Cliente envía: {packet_size.decode()}")
print(f"Servidor responde: {data}")

# Creo thread que lee desde el socket hacia stdout:
newthread = threading.Thread(target=Rdr, args=(s,))
newthread.start()

# En este otro thread leo desde stdin hacia socket:
filename = sys.argv[1]

f = open(filename, 'r')

while True:
    buf = f.buffer.read1(int(max_packet_size))
    if not buf:
        break
    s.send(buf)
    print(f"Cliente envía: {buf.decode()}")

# --------------------------------------
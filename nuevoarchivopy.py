def generate_packet(byte_size):
    s = '0'
    i = 0
    while len(s) < byte_size:
        i = (i + 1) % 10
        s += str(i)
    with open(f"paquetes_{byte_size}.txt", 'w') as f:
        f.write(s)

for x in [1,10,100,1000,10000,100000]: # <- en la lista poner los valores que quieres generar paquetes
    generate_packet(x)
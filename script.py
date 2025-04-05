import tkinter as tk
from tkinter import messagebox

def validar_ip(ip):
    partes = ip.split(".")
    if len(partes) != 4:
        return False
    for parte in partes:
        if not parte.isdigit() or not 0 <= int(parte) <= 255:
            return False
    return True

def validar_binario(bin_str):
    partes = bin_str.split(".")
    if len(partes) != 4:
        return False
    for parte in partes:
        if len(parte) != 8 or not all(bit in "01" for bit in parte):
            return False
    return True

def ip_a_binario(ip):
    return '.'.join(f"{int(octeto):08b}" for octeto in ip.split('.'))

def binario_a_ip(bin_str):
    return '.'.join(str(int(b, 2)) for b in bin_str.split('.'))

def obtener_mascara(prefijo):
    bin_str = '1' * prefijo + '0' * (32 - prefijo)
    return '.'.join([bin_str[i:i+8] for i in range(0, 32, 8)])

def calcular_subred(ip, prefijo):
    ip_bin = ''.join(f"{int(octeto):08b}" for octeto in ip.split('.'))
    mascara_bin = '1' * prefijo + '0' * (32 - prefijo)
    
    # Dirección de red
    red_bin = ''.join(str(int(ip_bin[i]) & int(mascara_bin[i])) for i in range(32))
    red = '.'.join(str(int(red_bin[i:i+8], 2)) for i in range(0, 32, 8))

    # Broadcast
    broadcast_bin = red_bin[:prefijo] + '1' * (32 - prefijo)
    broadcast = '.'.join(str(int(broadcast_bin[i:i+8], 2)) for i in range(0, 32, 8))

    # Rango de hosts
    if prefijo == 32:
        host_min = host_max = red
        num_hosts = 1
    elif prefijo == 31:
        host_min = red
        host_max = broadcast
        num_hosts = 2
    else:
        host_min_int = int(red_bin, 2) + 1
        host_max_int = int(broadcast_bin, 2) - 1
        host_min = '.'.join(str((host_min_int >> (8 * i)) & 255) for i in reversed(range(4)))
        host_max = '.'.join(str((host_max_int >> (8 * i)) & 255) for i in reversed(range(4)))
        num_hosts = (2 ** (32 - prefijo)) - 2

    return red, broadcast, host_min, host_max, num_hosts, obtener_mascara(prefijo)

def convertir():
    entrada = entry.get().strip()

    try:
        if "/" in entrada:
            ip, cidr = entrada.split("/")
            prefijo = int(cidr)
        else:
            ip = entrada
            prefijo = 32

        # Verificar si la entrada es binaria o decimal
        if '.' in ip:
            if all(c in '01.' for c in ip):
                if not validar_binario(ip):
                    raise ValueError
                ip = binario_a_ip(ip)  # Convertir binario a decimal
            elif not validar_ip(ip):
                raise ValueError
        elif not validar_ip(ip):
            raise ValueError

        if not (0 <= prefijo <= 32):
            raise ValueError

        ip_bin = ip_a_binario(ip)
        red, broadcast, host_min, host_max, num_hosts, mascara_bin = calcular_subred(ip, prefijo)

        resultado = (
            f"IP decimal: {ip}\n"
            f"IP binario: {ip_bin}\n"
            f"Máscara: /{prefijo}\n"
            f"Máscara binaria: {mascara_bin}\n\n"
            f"Dirección de red: {red}\n"
            f"Broadcast: {broadcast}\n"
            f"Rango de hosts: {host_min} - {host_max}\n"
            f"Cantidad de hosts válidos: {num_hosts}"
        )
        output_var.set(resultado)

    except:
        messagebox.showerror("Error", "Entrada inválida. Usa formato: IP o IP/CIDR")

# Interfaz
root = tk.Tk()
root.title("Calculadora de Subredes")

tk.Label(root, text="Ingresa IP (opcional con /CIDR):").pack(pady=5)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

tk.Button(root, text="Calcular", command=convertir).pack(pady=5)

output_var = tk.StringVar()
tk.Label(root, textvariable=output_var, fg="blue", font=("Courier", 10), justify="left").pack(pady=10)

root.mainloop()

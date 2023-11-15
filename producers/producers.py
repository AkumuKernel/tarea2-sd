from kafka import KafkaProducer
from json import dumps
from datetime import datetime
import random
import string

servidores_bootstrap = 'kafka:9092'
topic_mote = 'mote'
topic_formulario = 'mote.formulario'
topic_ingredientes = 'mote.ingredientes'
topic_ventas = 'mote.ventas'

productor = KafkaProducer(
    bootstrap_servers=[servidores_bootstrap],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

def generar_nombre_correo():
    nombre = ''.join(random.choices(string.ascii_letters, k=8))
    email = f"{nombre}@example.com"
    return nombre, email

# Mapeo de unidades a números de partición
unidad_particion_map = {
    'normal': 0,
    'pagado': 1,
}

stock_mote_con_huesillo = 1000  # Stock inicial de Mote con Huesillo

def enviar_formulario(repeticiones):
    topic = topic_formulario
    try:
        for _ in range(repeticiones):
            tipo = random.choice(['normal', 'pagado'])  # Seleccionar aleatoriamente un tipo
            particion = unidad_particion_map[tipo]
            nombre, email = generar_nombre_correo()
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            mensaje = {
                "timestamp": datetime.now().isoformat(),
                "nombre": nombre,
                "email": email,
                "password": password,
                "tipo": tipo
            }
            productor.send(topic, value=mensaje, partition=particion)
            print(f"Enviando JSON a la partición {particion}: {mensaje}")
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")

def reponer_ingredientes(repeticiones):
    topic = topic_ingredientes
    try:
        for _ in range(repeticiones):
            # Ingredientes agotados para Mote con Huesillo
            ingredientes = ['huesillo', 'mote', 'azúcar', 'cáscara de limón', 'agua', 'hielo']
            ingrediente = random.choice(ingredientes)
            mensaje = {
                "timestamp": datetime.now().isoformat(),
                "ingrediente": ingrediente,
                "estado": "agotado"
            }
            productor.send(topic, value=mensaje)
            print(f"Enviando notificación de ingrediente agotado para Mote con Huesillo: {mensaje}")
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")

def registrar_venta(repeticiones):
    global stock_mote_con_huesillo
    topic = topic_ventas
    try:
        for _ in range(repeticiones): 
            if stock_mote_con_huesillo <= 0:
                print("¡Se ha agotado el stock de Mote con Huesillo!")
                break
            cantidad = min(random.randint(1, 10), stock_mote_con_huesillo)
            stock_mote_con_huesillo -= cantidad
            valor = 2000  # Precio de Mote con Huesillo
            mensaje = {
                "timestamp": datetime.now().isoformat(),
                "cantidad": cantidad,
                "valor": valor
            }
            productor.send(topic, value=mensaje)
            print(f"Registro de venta de Mote con Huesillo (x{cantidad}) enviado: {mensaje}")
    except Exception as e:
        print(f"Error al enviar mensaje de venta: {e}")

if __name__ == "__main__":
    while True:
        selection = input("Ingresa la cantidad de repeticiones: ")
        if selection.isnumeric():
         repeticiones = int(selection)
         break
        else:
         continue
    while True:
        print("\nMenú:")
        print("1. Enviar formulario aleatorio")
        print("2. Notificar ingrediente agotado (Mote con Huesillo)")
        print("3. Registrar venta de Mote con Huesillo")
        print("4. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            enviar_formulario(repeticiones)

        elif opcion == "2":
            reponer_ingredientes(repeticiones)

        elif opcion == "3":
            registrar_venta(repeticiones)

        elif opcion == "4":
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

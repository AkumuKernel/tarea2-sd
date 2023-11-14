from kafka import KafkaConsumer
import psycopg2
import json
import random
import string, time
from datetime import datetime
from mailer import mail

servidores_bootstrap = 'kafka:9092'

DATABASE_CONFIG = {
    'dbname': 'proyecto',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db',
    'port': '5432'
}

counter = 0

def consume_messages(topic_name, table_name):
    # Conectar a PostgreSQL
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()
    consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=servidores_bootstrap,
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    consumer_timeout_ms=5000  # Cierra el consumidor después de 5 segundos si no se reciben mensajes
)

    mensajes_guardados = []  # Lista para guardar los primeros 10 mensajes
    cont = 0
    global counter
    try:
        for message in consumer:
            if cont < counter:
             continue
            
            print(f"Recibido mensaje de {message.topic} en la partición {message.partition} con offset {message.offset}:")
            print(message.value)
            
            # Agregamos el mensaje a la lista
            mensajes_guardados.append(message.value)
            
            # Generar un timestamp actual
            timestamp = datetime.now().isoformat()
            
            # Crear una copia del mensaje y agregar el timestamp
            message_with_timestamp = message.value.copy()
            message_with_timestamp['timestamp'] = timestamp
            
            if "mote.formulario" not in message.topic:
             select_id = 'SELECT id FROM formulario ORDER BY random() LIMIT 1'
             try:
                cursor.execute(select_id)
                conn.commit()
                formulario_id = cursor.fetchone()
                message_with_timestamp['formulario_id'] = formulario_id
             except psycopg2.Error as e:
                print(f"Error al seleccionar en la base de datos: {e}")
                conn.rollback()
            
            columns = ", ".join(message_with_timestamp.keys())
            values = tuple(message_with_timestamp.values())
            placeholders = ", ".join(['%s'] * len(message_with_timestamp.values()))
            insert_stmt = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            try:
                cursor.execute(insert_stmt, values)
                conn.commit()
            except psycopg2.Error as e:
                print(f"Error al insertar en la base de datos: {e}")
                conn.rollback()

            cont += 1
    finally:
        # Cerramos el consumidor explícitamente
        consumer.close()
        cursor.close()
        conn.close()
        counter = cont
        # Imprimir los mensajes guardados
        print("Mensajes guardados:", mensajes_guardados)

if __name__ == "__main__":
 while True:
     print("Menú Consumidores:")
     print("1. Consumir mensajes de mote.formulario")
     print("2. Consumir mensajes de mote.ingredientes")
     print("3. Consumir mensajes de mote.ventas")
     print("4. Terminar la semana")
     print("5. Salir")

     opcion = input("Elige una opción: ")

     if opcion == "1":
         consume_messages('mote.formulario', 'formulario')
     elif opcion == "2":
         consume_messages('mote.ingredientes', 'ingredientes')
     elif opcion == "3":
         consume_messages('mote.ventas', 'ventas')
     elif opcion == "4":
         print("\nSemana Terminada")
         mail.menu()
     elif opcion == "5":
         print("Saliendo...")
         break
     else:
         print("Opción no válida.")

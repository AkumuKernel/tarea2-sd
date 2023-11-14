import smtplib
import psycopg2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuracion de base de datos
DATABASE_CONFIG = {
    'dbname': 'proyecto', 
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db',
    'port': '5432'
}

# Configuracion de SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "mamochi621@gmail.com"
SMTP_PASSWORD = "nrly rkrn zymm fotg"

def send_email(subject, body, to_email):
    msg = MIMEMultipart()
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_email, msg.as_string())

def send_verdict_email(user_email):
    with psycopg2.connect(**DATABASE_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT nombre, tipo FROM formulario WHERE email = %s;", (user_email,))
            result = cur.fetchone()
            if result:
                nombre = result
                subject = "Notificacion de Veredicto"
                body = f"Hola {nombre},\n\nSe ha aprobado tu solicitud.\n\nSaludos,\nEquipo de MAMOCHI"
                send_email(subject, body, user_email)
                print(f"Correo enviado exitosamente a {user_email}")

def send_ingredient_email(user_email):
    with psycopg2.connect(**DATABASE_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT nombre, ingrediente FROM formulario JOIN ingredientes ON formulario.id = ingredientes.formulario_id WHERE formulario.email = %s;", (user_email,))
            result = cur.fetchone()
            if result:
                nombre, ingrediente = result
                subject = "Reposicion de Ingrediente"
                body = f"Hola {nombre},\n\nEl ingrediente: {ingrediente} ha sido repuesto.\n\nSaludos,\nTu Equipo"
                send_email(subject, body, user_email)
                print(f"Correo enviado exitosamente a {user_email}")

def send_sales_email(user_email):
    with psycopg2.connect(**DATABASE_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT nombre, cantidad, valor FROM formulario JOIN ventas ON formulario.id = ventas.formulario_id WHERE formulario.email = %s;", (user_email,))
            result = cur.fetchone()
            if result:
                nombre, cantidad_vendida, ganancias = result
                subject = "Resumen de Ventas"
                body = f"Hola {nombre},\n\nCantidad Vendida: {cantidad_vendida}\nGanancias: ${ganancias*cantidad_vendida}\n\nSaludos,\nTu Equipo"
                send_email(subject, body, user_email)
                print(f"Correo enviado exitosamente a {user_email}")

def select_mails():
    mapeo = []
    with psycopg2.connect(**DATABASE_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT email FROM formulario WHERE tipo = 'pagado'")
            result = cur.fetchall()
            for i, row in enumerate(result, start=0):
             mapeo.append(row[0])
             print(f'{i+1}. {row[0]}')
    return mapeo

def menu():
    while True:
        print("\nMenú:")
        print("1. Enviar notificacion de vedericto")
        print("2. Notificar reposicion")
        print("3. Enviar ganacias y ventas")
        print("4. Salir")

        opcion = input("Elige una opción: ")

        if "1" in opcion or "2" in opcion or "3" in opcion:
         print("\nLista de emails:")
         dictionary = select_mails()
         tmp = int(input(f"Elija un email (1-{len(dictionary)}): "))
         email = dictionary[tmp-1]

        if opcion == "1":
            send_verdict_email(email)

        elif opcion == "2":
            send_ingredient_email(email)

        elif opcion == "3":
            send_sales_email(email)

        elif opcion == "4":
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
 menu()
# Tarea 2 Sistemas Distribuidos

Tarea 2 de Sistemas Distribuidos EIT UDP CIT-2011

## Obtención
Para poder tener los contenedores hechos para esta actividad se tiene que hacer el siguiente comando:
```
git clone https://github.com/AkumuKernel/tarea2-sd.git
```

## Ejecución de instancias
Para poder ejecutar los contenedores que fueron descargados gracias al paso anterior, se debe hacer lo siguiente en la carpeta raíz del proyecto:
```
docker compose up -d
```

Para así poder iniciar los contenedores deseados, se pueden ejecutar los 3 compose al mismo tiempo.

## Acceso a los contenedores

Para acceder al contenedor para la ejecución correcta de los datos:

### Para kafka
```
docker exec -it kafka bash
```

### Para los producers

```
docker exec -it producer_kafka# bash
```
El # puede no estar o ser 2 o 3.

### Para los consumer

```
docker exec -it consumer_kafka bash
```

### Para el acceso a la base de datos

```
docker exec -it db bash
```

## Ejecución del programa

Cabe señalar que lo primero que se tiene que hacer es crear los tópicos en la red de Apache Kafka

### Crear tópicos
Dentro del contendor de Kafka se deben poner los siguientes comandos
```
chmod +x init.sh && ./init.sh
```

### Iniciar los datos de los productores
Dentro del contenedor de los producers se debe poner el siguiente comando
```
python producers.py
```
### Iniciar el consumo de mensajes de los consumidores
Dentro del contenedor de los consumers se debe poner el siguiente comando
```
python consumers.py
```

### Iniciar la vista de la base de datos:
Existen 2 formas de acceder a la base de datos, la primera es en base a pgadmin4, utilizando el link [localhost:81](http://localhost:81/), y accediendo con las siguientes credenciales
> admin@admin.com
> admin
Dentro de pgAdmin4 seleccionar "Add new server"
En el apartado de general se inserta el nombre que usted desee.
En el apartado de "Connection" debe ingresar los siguientes datos:
> Host name/ address: db
> Port: 5432
> Username: postgres
> Password: postgres
Y así se tendrá acceso a la base de datos.

O utilizando el siguiente comando dentro del contendor db
```
psql -U postgres -d proyecto
```

## Información adicional

Al momento de ejecutar el producers.py dentro del contenedor de producers_kafka apararecerá la siguiente interfaz:
>Menú:
>1. Enviar formulario aleatorio
>2. Notificar ingrediente agotado (Mote con Huesillo)
>3. Registrar venta de Mote con Huesillo
>4. Salir
>Elige una opción:

Aquí se pueden insertar cualquier tipo de opcion, sin que el programa tenga problemas.

Al ejecutar el programa consumers.py dentro del contendor de consumers_kafka aparecerá la siguiente interfaz:
> Menú Consumidores:
> 1. Consumir mensajes de mote.formulario
> 2. Consumir mensajes de mote.ingredientes
> 3. Consumir mensajes de mote.ventas
> 4. Terminar la semana
> 5. Salir
>Elige una opción:

Aquí se pueden insertar cualquier tipo de opcion, sin que el programa tenga problemas.

Al momento de seleccionar el 4 aparecerá este otro menú:
> Menú:
> 1. Enviar notificacion de vedericto
> 2. Notificar reposicion
> 3. Enviar ganacias y ventas
> 4. Salir
>Elige una opción:

Aquí pueden existir problemas si no se inserta una variable únicamente númerica.

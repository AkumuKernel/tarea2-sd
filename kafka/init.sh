kafka-topics.sh --create --bootstrap-server kafka:9092 --topic mote

kafka-topics.sh --create --bootstrap-server kafka:9092 --topic mote.formulario

kafka-topics.sh --create --bootstrap-server kafka:9092 --topic mote.ingredientes

kafka-topics.sh --create --bootstrap-server kafka:9092 --topic mote.ventas

kafka-topics.sh --alter --bootstrap-server kafka:9092 --partitions 2 --topic mote.formulario
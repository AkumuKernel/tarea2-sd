CREATE EXTENSION "uuid-ossp";

CREATE TABLE formulario (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    timestamp TIMESTAMP, 
    nombre TEXT, 
    email TEXT, 
    password TEXT, 
    tipo TEXT
);
CREATE TABLE ingredientes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY, 
    timestamp TIMESTAMP,
    ingrediente TEXT, 
    estado TEXT,
    formulario_id UUID REFERENCES formulario(id) ON DELETE CASCADE
);

CREATE TABLE ventas (
    id_venta UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    timestamp TIMESTAMP,
    cantidad INT, 
    valor FLOAT,
    formulario_id UUID REFERENCES formulario(id) ON DELETE CASCADE
);
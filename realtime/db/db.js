const pg = require('pg');
const connectionString = "postgres://postgres:081011@localhost:5432/requisicionesdb";
const client = new pg.Client(connectionString);

client.connect();

const query = client.query(
	'CREATE TABLE public.node_mensaje(' +
	  	'id serial NOT NULL,' +
	  	'mensaje text,' +
	  	'fecha_creacion timestamp with time zone NOT NULL,' +
	  	'receptor_id integer NOT NULL,' +
	  	'remitente_id integer NOT NULL,' +
	  	'CONSTRAINT node_mensaje_pkey PRIMARY KEY (id)' +
	')'  
);

console.log('Proceso completado.');
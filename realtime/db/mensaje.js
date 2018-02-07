const pg = require('pg');
const connectionString = "postgres://postgres:081011@localhost:5432/requisicionesdb";
const client = new pg.Client(connectionString);

const create_sql = 'INSERT INTO node_mensaje (mensaje, fecha_creacion, receptor_id, remitente_id) VALUES ($1, $2, $3, $4);';
const read_sql = 'SELECT * FROM node_mensaje WHERE (receptor_id = $1 AND remitente_id = $2) OR (receptor_id = $2 and remitente_id = $1)';

client.connect();

var chat_list = function (perfil1, perfil2) {
	client.query( read_sql, [perfil1, perfil2], (err, res) => {		
		if (err) {
			console.log(err.stack) 
			client.end()
			return;			
		}

		for (var i in res.rows) {
			console.log(res.rows[i]);
		}
		client.end()
	});
}

module.exports = {
	chat_list: chat_list
}
const conn = require('./conexion');
const pg = require('pg');
const connectionString = 'postgres://'+conn.user+':'+conn.password+'@'+conn.host+':'+conn.port+'/requisicionesdb';
const client = new pg.Client(connectionString);

const create_sql = 'INSERT INTO node_mensaje (mensaje, receptor_id, remitente_id) VALUES ($1, $2, $3);';
const read_sql = 'SELECT * FROM node_mensaje WHERE (receptor_id = $1 AND remitente_id = $2) OR (receptor_id = $2 and remitente_id = $1)';

client.connect();

var listar = function (perfil1, perfil2) {
	return new Promise(function (resolve, reject) {
		client.query(read_sql, [perfil1, perfil2], (err, res) => {		
			if (err) {
				console.log(err.stack) 			
				return;			
			}				
			resolve(res.rows);
		});		
	});
}

var guardar = function (texto, recibe, remite) {
	client.query(create_sql, [texto, recibe, remite], (err, res) => {		
		if (err) {
			console.log(err.stack) 			
			return;			
		}
	});
}

module.exports = {
	listar: listar,
	guardar: guardar,
}
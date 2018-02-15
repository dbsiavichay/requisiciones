var express = require('express'), 
	app     = express();

var server = require('http').createServer(app)
	io     = require('socket.io').listen(server);

var pg = require ('pg');
var pgConString = "postgres://postgres:081011@localhost:5432/requisicionesdb"
var client = new pg.Client(pgConString)
client.connect()
client.query("LISTEN addnotificacion");
client.handler = false;


var Mensaje = require('./db/mensaje');

var clientes = {}

io.sockets.on('connection', function (socket) {				
	if (!client.handler) {
		client.on('notification', function(data) {		    
		    //socket.broadcast.to('gestionadores').emit('message', {data:data.payload});		    
		    var notificacion = JSON.parse(data.payload);		    
		    var receptor = notificacion['receptor_id'];
		    if (receptor in clientes) {
		    	clientes[receptor].socket.emit('count', notificacion)		    
		    	clientes[receptor].socket.emit('notificacion', notificacion)
		    }
		});
		client.handler=true;			
	}	

	socket.emit('data', {});

	socket.on('data', function (data) {		
		var id = data['user_id']
		this['user'] = data		
		clientes[id] = {
			'socket': this,			
		}		
		socket.emit('ready-chat', {});
	});

	socket.on('chat-datos', function (data) {
		var emite = socket.user.user_id;
		var recibe = data;
		var p = Mensaje.listar(emite, recibe)
		p.then(function (datos) {
			socket.emit('chat-datos', datos);
		});
	});

	socket.on('chat', (data) => {		
		receptor = data['receptor_id'];
		Mensaje.guardar(data.texto, receptor, socket.user.user_id);
		if (receptor in clientes) { 
			data['remitente'] = socket.user;
			clientes[receptor].socket.emit('chat', data);
		}
	});

	socket.on('disconnect', function () {
		delete clientes[this['user']['user_id']];
		console.log('Usuarios conectados: ' + Object.keys(clientes).length)		
		console.log('Socket: ' + this['id'] + ' se ha desconectado.')		
	});
});







console.log('Server listen on port 8002');
server.listen(8002)
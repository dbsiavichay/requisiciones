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

var clientes = {}

io.sockets.on('connection', function (socket) {				
	if (!client.handler) {
		client.on('notification', function(data) {		    
		    //socket.broadcast.to('gestionadores').emit('message', {data:data.payload});		    
		    var notificacion = JSON.parse(data.payload);		    
		    var receptor = notificacion['receptor_id'];
		    if (receptor in clientes) 
		    	clientes[receptor].socket.emit('notificacion', notificacion)		    
		});
		client.handler=true;			
	}	

	socket.emit('data', {});

	socket.on('data', function (data) {	
		var receptor = data['user_id']	
		this['receptor'] = receptor		
		clientes[receptor] = {
			'socket': this,			
		}		
	});

	socket.on('disconnect', function () {
		delete clientes[this['receptor']];		
		console.log('Socket: ' + this['id'] + ' se ha desconectado.')		
	});
});







console.log('Server listen on port 8002');
server.listen(8002)
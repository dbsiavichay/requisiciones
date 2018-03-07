const user = process.env.DB_USER
const password = process.env.DB_PASSWORD
const host = process.env.DB_HOST
const port = process.env.DB_PORT

module.exports = {
	user: user,
	password: password,
	host: host,
	port: port,
}
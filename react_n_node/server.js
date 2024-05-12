//Import dependencies
const express = require('express');     //for HTTP requests
const bodyParser = require('body-parser');

//Initialize express
const app = express();
const port = 1987;
const cors = require('cors');       //Middleware cors

//Config middleware to analize json
app.use(bodyParser.json());

app.use(cors());

app.get('/syslog-messages', (req, res) => {
  // Leer los mensajes del archivo syslog_messages.txt
  const fs = require('fs');
  fs.readFile('syslog_messages.txt', 'utf8', (err, data) => {
    if (err) {
      console.error(err);
      res.status(500).send('Error al leer los mensajes syslog.');
      return;
    }
    // Dividir los mensajes por líneas y enviarlos como respuesta
    const messages = data.split('\n');
    res.send(messages);
  });
});


//Initialize server
app.listen(port, () => {
  console.log(`Servidor escuchando en http://localhost:${port}`);
});
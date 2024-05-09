const cors = require("cors");
const express = require("express");
const helmet = require("helmet"); // Importe o pacote helmet
const session = require('express-session');
const mongoose = require('mongoose'); // Importe o Mongoose
const app = express();
const userRoutes = require("../src/routes/userRoutes");

app.use(cors());
app.use(express.static('public'));

// Configuração da CSP usando o pacote helmet
app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"],
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      styleSrc: ["'self'"],
    },
  })
);

app.use(session({
  secret: 'sua-chave-secreta',
  resave: false,
  saveUninitialized: true
}));

app.use(express.json());
app.use("../api/users", userRoutes);

app.get('/home', function(req, res) {
  res.send('Bem-vindo à página inicial!');
});

const PORT = process.env.PORT || 3000;

// Conectando ao MongoDB
mongoose.connect('mongodb+srv://mirynhalopes:9541@cluster.dqfj2m5.mongodb.net/')
  .then(() => {
    console.log('Conectado ao MongoDB');
    // Inicie o servidor após conectar-se ao MongoDB
    app.listen(PORT, () => {
      console.log(`Servidor rodando em http://localhost:${PORT}/api/users`);
    });
  })
  .catch((error) => {
    console.error('Erro ao conectar ao MongoDB:', error);
    process.exit(1); // Encerra o processo do Node.js em caso de erro de conexão
  });

module.exports = app; // Exporta o aplicativo express em vez do servidor

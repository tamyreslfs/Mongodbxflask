const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

// Rotas para o CRUD de usuários
router.get('/users', userController.getAllUsers); // GET /api/users
router.post('/users', userController.createUser); // POST /api/users
router.patch('/users/:id', userController.updateUser); // PATCH /api/users/:id
router.delete('/users/:id', userController.deleteUser); // DELETE /api/users/:id

// Rota para login de usuário
router.post('/login', userController.login);

module.exports = router;

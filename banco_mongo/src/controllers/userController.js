const User = require("../models/User");

exports.getAllUsers = async (req, res) => {
    try {
        const users = await User.find();
        res.status(200).json(users);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

exports.createUser = async (req, res) => {
    const { name, password } = req.body;
    
    // Verifica se o nome de usuário já existe
    const existingUser = await User.findOne({ name });
    if (existingUser) {
        return res.status(400).json({ message: 'Nome de usuário já existe' });
    }

    // Cria um novo usuário
    const user = new User({ name, password });
    try {
        const savedUser = await user.save();
        res.status(201).json(savedUser);
    } catch (error) {
        res.status(400).json({ message: error.message })
    }
};

exports.updateUser = async (req, res) => {
    const { id } = req.params;
    try {
        const updatedUser = await User.findByIdAndUpdate(id, req.body, { new: true });
        res.status(200).json(updatedUser);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

exports.deleteUser = async (req, res) => {
    const { id } = req.params;
    try {
        await User.findByIdAndDelete(id);
        res.status(200).json({ message: "User deleted successfully" });
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

exports.login = async (req, res) => {
    const { name, password } = req.body;

    try {
        // Procura pelo nome de usuário na base de dados
        const user = await User.findOne({ name });
        if (!user) {
            return res.status(401).json({ message: 'Nome de usuário não encontrado' });
        }

        // Verifica se a senha corresponde à senha armazenada
        if (user.password !== password) {
            return res.status(401).json({ message: 'Senha incorreta' });
        }

        // Se as credenciais estiverem corretas, retorna uma resposta de sucesso
        res.status(200).json({ message: 'Login bem-sucedido' });
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

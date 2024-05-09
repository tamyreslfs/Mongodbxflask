const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true // Define o campo como obrigatório
    },
    password: {
        type: String,
        required: true // Define o campo como obrigatório
    }
});

module.exports = mongoose.model("User", userSchema);

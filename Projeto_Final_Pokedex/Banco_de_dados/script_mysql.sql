CREATE DATABASE IF NOT EXISTS pokedex_bd;
USE pokedex_bd;

DROP TABLE IF EXISTS pokemon;

CREATE TABLE pokemon (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero INT(11) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(70) NOT NULL,
    altura DECIMAL(3,2),
    peso DECIMAL(5,2),
    habilidade VARCHAR(200),
    img VARCHAR(255),
    ataque INT(5),
    defesa INT(5),
    foto VARCHAR(255)
);

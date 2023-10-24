-- ----------------- GESTICADO ----------------------
CREATE DATABASE IF NOT EXISTS gesticado;
USE gesticado;

-- creation de la table utilisateur 
CREATE TABLE IF NOT EXISTS utilisateur
(
	numero VARCHAR(10),
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    mdp TEXT NOT NULL,
    email VARCHAR(100) NOT NULL,
    age TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY(numero)
);

-- creation de la table tache 
CREATE TABLE IF NOT EXISTS tache
(
	nom_tache VARCHAR(100) NOT NULL UNIQUE,
    duree_tache SMALLINT UNSIGNED NOT NULL,
    temps_effectue SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    numero_tache TINYINT UNSIGNED NOT NULL,
    jour_actuel DATETIME NOT NULL,
    fin_journee TINYINT NOT NULL DEFAULT 0,
    numero VARCHAR(10),
    CONSTRAINT FOREIGN KEY(numero) REFERENCES utilisateur(numero)
);
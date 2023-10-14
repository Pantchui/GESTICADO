-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : sam. 14 oct. 2023 à 05:10
-- Version du serveur : 10.4.28-MariaDB
-- Version de PHP : 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `gestion_temps_taches`
--

-- --------------------------------------------------------

--
-- Structure de la table `taches`
--

CREATE TABLE `taches` (
  `nom_tache` varchar(100) DEFAULT NULL,
  `duree` int(11) DEFAULT NULL,
  `temps_effectue` int(11) NOT NULL,
  `numero` varchar(10) DEFAULT NULL,
  `numero_tache` int(11) NOT NULL,
  `jour` varchar(100) NOT NULL,
  `fin_journee` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `taches`
--

INSERT INTO `taches` (`nom_tache`, `duree`, `temps_effectue`, `numero`, `numero_tache`, `jour`, `fin_journee`) VALUES
('laver le sol', 60, 0, '815Xq22', 1, 'Mardi 5 Septembre 2023', 0),
('prendre les habits', 60, 0, '815Xq22', 2, 'Mardi 5 Septembre 2023', 0),
('Virer', 60, 0, '815Xq22', 3, 'Mardi 5 Septembre 2023', 0),
('Viser le caillloux', 60, 0, '815Xq22', 4, 'Mardi 5 Septembre 2023', 0),
('laver le sol', 60, 1, '815Xq22', 1, 'Samedi 9 Septembre 2023', 0),
('prendre ', 15, 1, '815Xq22', 2, 'Samedi 9 Septembre 2023', 0),
('puiser de l\'eau', 45, 1, '815Xq22', 3, 'Samedi 9 Septembre 2023', 0),
('manger', 30, 1, '815Xq22', 4, 'Samedi 9 Septembre 2023', 0),
('Laver les habits', 60, 1, '815Xq22', 1, 'Lundi 11 Septembre 2023', 0),
('Laver les habits', 60, 1, '815Xq22', 1, 'Mardi 12 Septembre 2023', 0),
('ajouter l\'eau', 15, 0, '815Xq22', 2, 'Mardi 12 Septembre 2023', 0),
('chercher l\'enfant', 45, 0, '815Xq22', 3, 'Mardi 12 Septembre 2023', 0),
('xxxv', 45, 70, '815Xq22', 4, 'Mardi 12 Septembre 2023', 0),
('vdhghj', 45, 80, '815Xq22', 5, 'Mardi 12 Septembre 2023', 0),
('Repasser les habits', 45, 1, '815Xq22', 1, 'Mercredi 13 Septembre 2023', 1),
('laver le sol', 120, 1, '815Xq22', 2, 'Mercredi 13 Septembre 2023', 1),
('puiser de l\'eau', 45, 1, '815Xq22', 3, 'Mercredi 13 Septembre 2023', 1),
('manger', 30, 2, '815Xq22', 4, 'Mercredi 13 Septembre 2023', 1),
('laver les habits', 60, 3, '915Pp93', 1, 'Jeudi 14 Septembre 2023', 1),
('preparer', 45, 1, '915Pp93', 2, 'Jeudi 14 Septembre 2023', 1),
('visionner', 30, 1, '915Pp93', 3, 'Jeudi 14 Septembre 2023', 1),
('laver les habits', 120, 2, '815Xq22', 1, 'Samedi 16 Septembre 2023', 1),
('laver le sol', 45, 1, '815Xq22', 2, 'Samedi 16 Septembre 2023', 1),
('manger', 30, 300, '815Xq22', 3, 'Samedi 16 Septembre 2023', 1),
('laver les habits', 120, 9, '915Pp93', 1, 'Samedi 16 Septembre 2023', 1),
('laver le sol', 60, 1, '773Jo76', 1, 'Samedi 16 Septembre 2023', 0),
('programmer en java', 180, 1, '773Jo76', 2, 'Samedi 16 Septembre 2023', 0),
('finir le projet python', 180, 1, '773Jo76', 3, 'Samedi 16 Septembre 2023', 0),
('laver les habits', 60, 0, '982Ms86', 1, 'Samedi 16 Septembre 2023', 0),
('puiser de l\'eau', 60, 0, '982Ms86', 2, 'Samedi 16 Septembre 2023', 0),
('manger', 30, 0, '982Ms86', 3, 'Samedi 16 Septembre 2023', 0),
('manger', 60, 1, '989Sm28', 1, 'Samedi 16 Septembre 2023', 0),
('voir serie 1', 60, 1, '989Sm28', 2, 'Samedi 16 Septembre 2023', 0),
('voir film 1', 120, 1, '989Sm28', 3, 'Samedi 16 Septembre 2023', 0),
('laver les habits', 60, 1, '815Xq22', 1, 'Lundi 18 Septembre 2023', 1),
('laver le sol', 45, 70, '815Xq22', 2, 'Lundi 18 Septembre 2023', 1),
('preparer', 120, 1, '815Xq22', 3, 'Lundi 18 Septembre 2023', 1),
('puiser l\'eau', 120, 0, '815Xq22', 4, 'Lundi 18 Septembre 2023', 1),
('Laver le sol', 60, 1, '815Xq22', 1, 'Jeudi 5 Octobre 2023', 0),
('manger', 30, 2, '815Xq22', 2, 'Jeudi 5 Octobre 2023', 0),
('prendre l\'enfant', 45, 0, '815Xq22', 3, 'Jeudi 5 Octobre 2023', 0),
('cultiver le champs', 120, 0, '815Xq22', 4, 'Jeudi 5 Octobre 2023', 0),
('laver les habits', 120, 1, '815Xq22', 1, 'Lundi 9 Octobre 2023', 1),
('laver les assiettes', 30, 0, '815Xq22', 2, 'Lundi 9 Octobre 2023', 1),
('manger', 60, 1, '815Xq22', 3, 'Lundi 9 Octobre 2023', 1),
('visioinner', 180, 1, '815Xq22', 4, 'Lundi 9 Octobre 2023', 1);

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

CREATE TABLE `utilisateur` (
  `numero` varchar(15) NOT NULL,
  `pseudo` varchar(50) NOT NULL,
  `mail` varchar(50) NOT NULL,
  `mdp` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `utilisateur` (`numero`, `pseudo`, `mail`, `mdp`) VALUES
('114Te15', 'steve', 'steve@gmail.com', '0000'),
('773Jo76', 'Armel', 'arm@gmail.com', '1234'),
('815Xq22', 'Junior', 'ju@gmail.com', '1234'),
('915Pp93', 'vincent', 'vincent@gmail.com', '9999'),
('982Ms86', 'Ben', 'ben@gmail.com', '1234'),
('989Sm28', 'romeo', 'romeo@gmail.com', 'rome');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `taches`
--
ALTER TABLE `taches`
  ADD KEY `numero` (`numero`);

--
-- Index pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  ADD PRIMARY KEY (`numero`);

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `taches`
--
ALTER TABLE `taches`
  ADD CONSTRAINT `taches_ibfk_1` FOREIGN KEY (`numero`) REFERENCES `utilisateur` (`numero`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

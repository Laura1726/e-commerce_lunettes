-- USE S2BDD;

DROP TABLE IF EXISTS ligne_panier,ligne_commande,commande,lunette,utilisateur,couleur,categorie,etat;

CREATE TABLE IF NOT EXISTS utilisateur(
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),
    nom VARCHAR(255),
    est_actif INT,
    PRIMARY KEY (id_utilisateur)
);

CREATE TABLE IF NOT EXISTS couleur (
    id_couleur INT AUTO_INCREMENT,
    libelle VARCHAR(255),
    PRIMARY KEY(id_couleur)
);



CREATE TABLE IF NOT EXISTS etat(
    id_etat INT AUTO_INCREMENT,
    libelle_etat VARCHAR(255),
    PRIMARY KEY(id_etat)
);




CREATE TABLE IF NOT EXISTS categorie(
    id_categorie INT AUTO_INCREMENT,
    libelle_categorie VARCHAR(255),
    PRIMARY KEY(id_categorie)
);






CREATE TABLE IF NOT EXISTS commande(
    id_commande INT AUTO_INCREMENT,
    date_achat DATE,
    etat_id INT,
    utilisateur_id INT,
    PRIMARY KEY (id_commande),
    CONSTRAINT Fk_commande_etat FOREIGN KEY (etat_id) REFERENCES etat(id_etat),
    CONSTRAINT Fk_commande_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur)
);





CREATE TABLE IF NOT EXISTS lunette(
    id_lunette INT AUTO_INCREMENT,
    nom_lunette VARCHAR(255),
    sexe VARCHAR(255),
    indice_protection INT,
    taille_monture INT,
    prix_lunette DECIMAL(5,2),
    image VARCHAR(255),
    stock INT,
    fournisseur INT,
    marque VARCHAR(255),
    categorie_id INT,
    couleur_id INT,
    PRIMARY KEY (id_lunette),
    CONSTRAINT Fk_lunette_categorie FOREIGN KEY (categorie_id) REFERENCES categorie(id_categorie)
    CONSTRAINT Fk_lunette_couleur FOREIGN KEY (couleur_id) REFERENCES couleur(id_couleur)
);




CREATE TABLE IF NOT EXISTS ligne_commande(
    prix DECIMAL(5,2),
    quantite INT,
    lunette_id INT,
    commande_id INT,
    PRIMARY KEY (lunette_id,commande_id),
    CONSTRAINT Fk_ligne_commande_lunette FOREIGN KEY(lunette_id) REFERENCES lunette(id_lunette),
    CONSTRAINT Fk_ligne_commande_commande FOREIGN KEY (commande_id) REFERENCES commande(id_commande)
);

CREATE TABLE IF NOT EXISTS ligne_panier(
    date_ajout DATE,
    quantite INT,
    lunette_id INT,
    utilisateur_id INT,
    PRIMARY KEY (lunette_id,utilisateur_id),
    CONSTRAINT Fk_ligne_panier_lunette FOREIGN KEY(lunette_id) REFERENCES lunette(id_lunette),
    CONSTRAINT Fk_ligne_panier_commande FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE IF NOT EXISTS detient(
    lunette_id INT,
    couleur_id INT,
    PRIMARY KEY (lunette_id,couleur_id),
    CONSTRAINT Fk_detient_lunette FOREIGN KEY (lunette_id) REFERENCES lunette(id_lunette),
    CONSTRAINT Fk_detient_couleur FOREIGN KEY (couleur_id) REFERENCES couleur(id_couleur)
);





INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(1,'admin','admin@admin.fr',
    'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988',
    'ROLE_admin','admin','1'),
(2,'client','client@client.fr',
    'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349',
    'ROLE_client','client','1'),
(3,'client2','client2@client2.fr',
    'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080',
    'ROLE_client','client2','1');


INSERT INTO couleur(id_couleur, libelle) VALUES (1,'noir'),
                                                (2,'blanc'),
                                                (3,'rouge'),
                                                (4,'jaune'),
                                                (5,'orange'),
                                                (6,'brun'),
                                                (7,'bleu'),
                                                (8,'violet'),
                                                (9,'multicolore');


INSERT INTO etat(id_etat, libelle_etat) VALUES (1,'en attente'),
                                               (2,'expédie'),
                                               (3,'valide'),
                                               (4,'confirme');

INSERT INTO categorie(id_categorie, libelle_categorie) VALUES (1,'lunette de vue'),
                                                              (2,'lunette de soleil'),
                                                              (3,'lunette de ski'),
                                                              (4,'lunette de piscine');



INSERT INTO commande(id_commande, date_achat, etat_id, utilisateur_id) VALUES (1,'2024-04-17',1,2),
                                                                              (2,'2025-01-21',2,3),
                                                                              (3,'2023-06-26',1,2),
                                                                              (4,'2024-10-11',2,2);

INSERT INTO lunette(id_lunette, nom_lunette, sexe, indice_protection, taille_monture, prix_lunette, image, stock, fournisseur, marque, categorie_id, couleur_id) VALUES (1,'mirage','h',3,4,267.98,'lunette1.webp',2,1,'Rayban',1, 1),
                                                                                                                                                                  (2,'meta','h',3,2,478.87,'lunette2.webpp',1,2,'Fendi',2, 7),
                                                                                                                                                                  (3,'infinity','f',4,5,980.67,'lunette3.webp',100,3,'Optic2000',1,2),
                                                                                                                                                                  (4,'vortex','h',1,1,750,'lunette4.webp',50,1,'KABOOM',1,3),
                                                                                                                                                                  (5,'Fendigraphy','f',4,4,375.3,'lunette5.webp',5,1,'Furet',2,4),
                                                                                                                                                                  (6,'MAG450 ','h',1,1,50.0,'lunette6.webp',589,1,'LV',1,5),
                                                                                                                                                                  (7,'Orbis-Quadrum','h',3,2,234.67,'lunette7.webp',0,2,'Liketheview',1,6),
                                                                                                                                                                  (8,'X-Fit','h',3,4,999.99,'lunette8.webp',45,3,'pipo',4,7),
                                                                                                                                                                  (9,'Cobra Competizione','f',2,3,65.0,'lunette9.webp',45,3,'Rayban',4,8),
                                                                                                                                                                  (10,'Fastskin','h',1,2,55.55,'lunette10.webp',43,2,'Fendi',4,9),
                                                                                                                                                                  (11,'Lys ','h',4,3,110.0,'lunette11.webp',23,3,'chut',1,1),
                                                                                                                                                                  (12,' GC X Speed','h',3,4,940,'lunette12.webp',20,2,'Optic2000',3,2),
                                                                                                                                                                  (13,'Flower','h',5,5,275.0,'lunette13.webp',23,1,'KABOOM',2,3),
                                                                                                                                                                  (14,'ClassicFly ','f',3,4,145.0,'lunette14.webp',2,2,'Athena',2,4),
                                                                                                                                                                  (15,' CT0092O','h',3,3,850.0,'lunette15.webp',45,1,'glow',1,5),
                                                                                                                                                                  (16,'GC Speed Max','h',5,3,130.0,'lunette16.webp',1,3,'fiou',3,6),
                                                                                                                                                                  (17,'Vintage','h',2,3,80.0,'lunette17.webp',230,1,'gru',1,7),
                                                                                                                                                                  (18,'Prisme','h',3,2,190,'lunette18.webp',34,1,'top1',2,8),
                                                                                                                                                                  (19,'Bee','f',2,3,225.0,'lunette19.webp',3,2,'Lastreet',1,9),
                                                                                                                                                                  (20,'Hot Rod','h',3,4,140,'lunette20.webp',4,1,'Lastreet',2,1);


INSERT INTO ligne_commande (prix, quantite, lunette_id, commande_id) VALUES
(267.98, 1, 1, 1),
(478.87, 1, 2, 1),

(980.67, 2, 3, 2),

(750.00, 1, 4, 3),
(375.30, 1, 5, 3),

(55.55, 2, 10, 4),
(65.00, 1, 9, 4);

INSERT INTO ligne_panier (date_ajout, quantite, lunette_id, utilisateur_id) VALUES
('2025-01-10', 1, 7, 2),
('2025-01-12', 2, 11, 2),

('2025-01-15', 1, 8, 3),
('2025-01-18', 3, 17, 3);

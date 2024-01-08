CREATE TABLE Patients(
   Id_Patients INT AUTO_INCREMENT,
   Nom VARCHAR(255) ,
   Prenom VARCHAR(255) ,
   Date_de_naissance DATE,
   Sexe VARCHAR(15) ,
   Adresse TEXT,
   Telephone VARCHAR(20) ,
   Adresse_mail VARCHAR(255) ,
   PRIMARY KEY(Id_Patients)
);

CREATE TABLE Analyses(
   Id_Analyses INT AUTO_INCREMENT,
   Nom_de_l_analyse VARCHAR(255) ,
   Description_de_l_analyse VARCHAR(255) ,
   Concentration__mg_L_ FLOAT,
   Valeur_de_reference__mg_L_ FLOAT,
   Date_analyse DATE,
   Commentaire TEXT,
   PRIMARY KEY(Id_Analyses),
   FOREIGN KEY (Id_Patients) REFERENCES Patients(Id_Patients)
);

CREATE TABLE fait(
   Id_Patients INT,
   Id_Analyses INT,
   PRIMARY KEY(Id_Patients, Id_Analyses),
   FOREIGN KEY(Id_Patients) REFERENCES Patients(Id_Patients),
   FOREIGN KEY(Id_Analyses) REFERENCES Analyses(Id_Analyses)
);

-- Insertion d'un patient

INSERT INTO Patients (Nom, Prenom, Date_de_naissance, Sexe, Adresse, Telephone, Adresse_mail)
VALUES ('Dupont', 'Jean', '1990-05-15', 'Homme', '123 Rue de la Paix, Ville', '01 23 45 67 89', 'jean.dupont@email.com');

-- Insertion d'une analyse

INSERT INTO Analyses (Nom_de_l_analyse, Description_de_l_analyse, Concentration__mg_L_, Valeur_de_reference__mg_L_, Date_analyse, Commentaire, Id_Patients)
VALUES ('Hémoglobine', 'Mesure de la concentration d hémoglobine', 11.5, 12.0, '2024-01-01', 'Normal', 1);
  
-- Implémentation automatique de la table fait à chaque ajout d'analyse pour un patient

DELIMITER //

CREATE TRIGGER tr_insert_into_fait_after_insert
AFTER INSERT ON Analyses
FOR EACH ROW
BEGIN
    INSERT INTO fait (Id_Patients, Id_Analyses) VALUES (NEW.Id_Patients, NEW.Id_Analyses);
END;
//

DELIMITER ;


import os
import pymysql
import secrets
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "MySqlMatching")
DB_NAME = os.getenv("DB_NAME", "matching2")

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = secrets.token_hex(16)

CREATE_PATIENTS_TABLE = """
CREATE TABLE IF NOT EXISTS Patients (
    Id_Patients INT AUTO_INCREMENT PRIMARY KEY,
    Nom VARCHAR(255),
    Prenom VARCHAR(255),
    Date_de_naissance DATE,
    Sexe VARCHAR(15),
    Adresse TEXT,
    Telephone VARCHAR(20),
    Adresse_mail VARCHAR(255)
);
"""

CREATE_ANALYSES_TABLE = """
CREATE TABLE IF NOT EXISTS Analyses (
   Id_Analyses INT AUTO_INCREMENT PRIMARY KEY,
   Nom_de_l_analyse VARCHAR(255),
   Description_de_l_analyse VARCHAR(255),
   Concentration__mg_L_ FLOAT,
   Valeur_de_reference__mg_L_ FLOAT,
   Date_analyse DATE,
   Commentaire TEXT,
   Id_Patients INT,
   FOREIGN KEY (Id_Patients) REFERENCES Patients(Id_Patients)
);
"""

def initialize_database():
    with app.app_context():
        connection = connect_to_database()
        with connection.cursor() as cursor:
            cursor.execute(CREATE_PATIENTS_TABLE)
            cursor.execute(CREATE_ANALYSES_TABLE)
        connection.close()

def connect_to_database():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

@app.before_request
def before_request():
    initialize_database()

# CRUD: Create (Création) - Ajouter un nouveau patient
@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    nom = data.get('Nom')
    prenom = data.get('Prenom')
    date_naissance = data.get('Date_de_naissance')
    sexe = data.get('Sexe')
    adresse = data.get('Adresse')
    telephone = data.get('Telephone')
    adresse_mail = data.get('Adresse_mail')

    with connect_to_database() as connection, connection.cursor() as cursor:
        cursor.execute("INSERT INTO Patients (Nom, Prenom, Date_de_naissance, Sexe, Adresse, Telephone, Adresse_mail) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s);",
                       (nom, prenom, date_naissance, sexe, adresse, telephone, adresse_mail))
        connection.commit()

    return jsonify({"message": "Patient ajouté avec succès"}), 201

# CRUD: Read (Lecture) - Récupérer tous les patients
@app.route('/patients', methods=['GET'])
def get_all_patients():
    connection = connect_to_database()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Patients;")
        all_patients = cursor.fetchall()
    connection.close()

    return jsonify(patients=all_patients)

# CRUD: Read (Lecture) - Récupérer un patient par ID
@app.route('/patients/<int:Id_Patients>', methods=['GET'])
def get_patient_by_id(Id_Patients):
    with connect_to_database() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Patients WHERE Id_Patients = %s;", (Id_Patients,))
        patient = cursor.fetchone()

    if patient:
        return jsonify(patient)
    else:
        return jsonify({"error": "Patient non trouvé"}), 404

# CRUD: Update (Mise à jour) - Modifier un patient par ID
@app.route('/patients/<int:Id_Patients>', methods=['PUT'])
def update_patient(Id_Patients):
    data = request.json
    nom = data.get('Nom')
    prenom = data.get('Prenom')
    date_naissance = data.get('Date_de_naissance')
    sexe = data.get('Sexe')
    adresse = data.get('Adresse')
    telephone = data.get('Telephone')
    adresse_mail = data.get('Adresse_mail')

    with connect_to_database() as connection, connection.cursor() as cursor:
        # Vérifier d'abord si le patient existe
        cursor.execute("SELECT * FROM Patients WHERE Id_Patients = %s;", (Id_Patients,))
        existing_patient = cursor.fetchone()

        if not existing_patient:
            return jsonify({"error": "Patient non trouvé"}), 404

        # Mettre à jour le patient
        cursor.execute("UPDATE Patients SET Nom=%s, Prenom=%s, Date_de_naissance=%s, Sexe=%s, Adresse=%s, "
                       "Telephone=%s, Adresse_mail=%s WHERE Id_Patients=%s;",
                       (nom, prenom, date_naissance, sexe, adresse, telephone, adresse_mail, Id_Patients))
        connection.commit()

    return jsonify({"message": "Patient mis à jour avec succès"})

# CRUD: Delete (Suppression) - Supprimer un patient par ID
@app.route('/patients/<int:Id_Patients>', methods=['DELETE'])
def delete_patient(Id_Patients):
    with connect_to_database() as connection, connection.cursor() as cursor:
        # Vérifier d'abord si le patient existe
        cursor.execute("SELECT * FROM Patients WHERE Id_Patients = %s;", (Id_Patients,))
        existing_patient = cursor.fetchone()

        if not existing_patient:
            return jsonify({"error": "Patient non trouvé"}), 404

        # Supprimer le patient
        cursor.execute("DELETE FROM Patients WHERE Id_Patients=%s;", (Id_Patients,))
        connection.commit()

    return jsonify({"message": "Patient supprimé avec succès"})

# CRUD: Create (Création) - Ajouter une nouvelle analyse
@app.route('/analyses', methods=['POST'])
def add_analysis():
    data = request.json
    nom_analyse = data.get('Nom_de_l_analyse')
    description_analyse = data.get('Description_de_l_analyse')
    concentration = data.get('Concentration__mg_L_')
    valeur_reference = data.get('Valeur_de_reference__mg_L_')
    date_analyse = data.get('Date_analyse')
    commentaire = data.get('Commentaire')
    Id_Patients = data.get('Id_Patients')  # Assurez-vous que cette clé est présente dans votre requête JSON

    with connect_to_database() as connection, connection.cursor() as cursor:
        cursor.execute("INSERT INTO Analyses (Nom_de_l_analyse, Description_de_l_analyse, Concentration__mg_L_, Valeur_de_reference__mg_L_, Date_analyse, Commentaire, Id_Patients) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s);",
                       (nom_analyse, description_analyse, concentration, valeur_reference, date_analyse, commentaire, Id_Patients))
        connection.commit()

    return jsonify({"message": "Analyse ajoutée avec succès"}), 201

# CRUD: Read (Lecture) - Récupérer toutes les analyses
@app.route('/analyses', methods=['GET'])
def get_all_analyses():
    connection = connect_to_database()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM analyses;")
        all_analyses = cursor.fetchall()
    connection.close()

    return jsonify(analyses=all_analyses)

# CRUD: Read (Lecture) - Récupérer une analyse par ID
@app.route('/analyses/<int:Id_analyses>', methods=['GET'])
def get_analysis_by_id(Id_analyses):
    with connect_to_database() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM analyses WHERE Id_analyses = %s;", (Id_analyses,))
        analysis = cursor.fetchone()

    if analysis:
        return jsonify(analysis)
    else:
        return jsonify({"error": "Analyse non trouvée"}), 404

# CRUD: Update (Mise à jour) - Modifier une analyse par ID
@app.route('/analyses/<int:Id_analyses>', methods=['PUT'])
def update_analysis(Id_analyses):
    data = request.json
    nom_analyse = data.get('Nom_de_l_analyse')
    description_analyse = data.get('Description_de_l_analyse')
    concentration = data.get('Concentration')
    valeur_reference = data.get('Valeur_de_reference')

    with connect_to_database() as connection, connection.cursor() as cursor:
        # Vérifier d'abord si l'analyse existe
        cursor.execute("SELECT * FROM analyses WHERE Id_analyses = %s;", (Id_analyses,))
        existing_analysis = cursor.fetchone()

        if not existing_analysis:
            return jsonify({"error": "Analyse non trouvée"}), 404

        # Mettre à jour l'analyse
        cursor.execute("UPDATE analyses SET Nom_de_l_analyse=%s, Description_de_l_analyse=%s, Concentration=%s, "
                       "Valeur_de_reference=%s WHERE Id_analyse=%s;",
                       (nom_analyse, description_analyse, concentration, valeur_reference, Id_analyses))
        connection.commit()

    return jsonify({"message": "Analyse mise à jour avec succès"})

# CRUD: Delete (Suppression) - Supprimer une analyse par ID
@app.route('/analyses/<int:Id_analyses>', methods=['DELETE'])
def delete_analysis(Id_analyses):
    with connect_to_database() as connection, connection.cursor() as cursor:
        # Vérifier d'abord si l'analyse existe
        cursor.execute("SELECT * FROM analyses WHERE Id_analyses = %s;", (Id_analyses,))
        existing_analysis = cursor.fetchone()

        if not existing_analysis:
            return jsonify({"error": "Analyse non trouvée"}), 404

        # Supprimer l'analyse
        cursor.execute("DELETE FROM analyses WHERE Id_analyses=%s;", (Id_analyses,))
        connection.commit()

    return jsonify({"message": "Analyse supprimée avec succès"})
                       
if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, host='localhost', port=8501)
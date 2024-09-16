
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox, \
    QTableWidget, QTableWidgetItem
import sqlite3

def creerTableCarnetAdress():
    connexion = sqlite3.connect('carnetAdress.db')
    cursor = connexion.cursor()

    # Requête SQL pour créer la table si elle n'existe pas déjà
    req = """
    CREATE TABLE IF NOT EXISTS contacts ( id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TEXT, telephone TEXT, mail TEXT )"""
    cursor.execute(req)
    connexion.commit()
    connexion.close()

    # Message pour informer que la table a été créée ou existe déjà
    print("Table 'contacts' créée ou déjà existante.")

def ajouterContact():
    nom = lineEditNom.text()
    prenom = lineEditPrenom.text()
    telephone = lineEditTelephone.text()
    mail = lineEditMail.text()

    if nom and prenom and telephone and mail:
        conn = sqlite3.connect("carnetAdress.db")
        cursor = conn.cursor()
        req = "INSERT INTO contacts (nom, prenom, telephone, mail) VALUES (?, ?, ?, ?)"
        cursor.execute(req, (nom, prenom, telephone, mail))
        conn.commit()
        conn.close()

        # Afficher un message de confirmation
        QMessageBox.information(fen, "Succès", "Le contact a été ajouté avec succès.")

        # Réinitialiser les champs
        lineEditNom.clear()
        lineEditPrenom.clear()
        lineEditTelephone.clear()
        lineEditMail.clear()

        # Recharger les contacts
        chargerContacts()
    else:
        QMessageBox.warning(fen, "Erreur", "Veuillez remplir tous les champs.")

def chargerContacts():
    contacts = []

    try:
        conn = sqlite3.connect("carnetAdress.db")
        cursor = conn.cursor()

        # Requête pour récupérer les contacts
        req = "SELECT * FROM contacts"
        cursor.execute(req)
        contacts = cursor.fetchall()

    except sqlite3.Error as e:
        print(f"Erreur lors de la connexion ou de l'exécution de la requête : {e}")
    finally:
        conn.close()

    # Vider le contenu existant dans le tableau
    tableWidget.clearContents()

    # Ajuster pour 5 colonnes : 1 pour l'ID (cachée) et 4 pour les autres champs
    tableWidget.setRowCount(len(contacts))
    tableWidget.setColumnCount(5)
    tableWidget.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Téléphone", "Mail"])

    for row_idx, contact in enumerate(contacts):
        for col_idx, data in enumerate(contact):
            item = QTableWidgetItem(str(data))

            if col_idx == 0:  # Si c'est l'ID, on le cache et on le rend non modifiable
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                tableWidget.setItem(row_idx, col_idx, item)
            else:
                tableWidget.setItem(row_idx, col_idx, item)

    # Cacher la colonne ID
    tableWidget.setColumnHidden(0, True)

def remplirChampsAvecSelection():
    selected_row = tableWidget.currentRow()

    if selected_row != -1:
        # Remplir les champs avec les données de la ligne sélectionnée
        lineEditNom.setText(tableWidget.item(selected_row, 1).text())
        lineEditPrenom.setText(tableWidget.item(selected_row, 2).text())
        lineEditTelephone.setText(tableWidget.item(selected_row, 3).text())
        lineEditMail.setText(tableWidget.item(selected_row, 4).text())
    else:
        # Réinitialiser les champs s'il n'y a pas de sélection
        lineEditNom.clear()
        lineEditPrenom.clear()
        lineEditTelephone.clear()
        lineEditMail.clear()

def modifierContact():
    selected_row = tableWidget.currentRow()
    if selected_row != -1:
        contact_id = tableWidget.item(selected_row, 0).text()
        nom = lineEditNom.text()
        prenom = lineEditPrenom.text()
        telephone = lineEditTelephone.text()
        mail = lineEditMail.text()

        if nom and prenom and telephone and mail:
            conn = sqlite3.connect("carnetAdress.db")
            cursor = conn.cursor()
            req = "UPDATE contacts SET nom = ?, prenom = ?, telephone = ?, mail = ? WHERE id = ?"
            cursor.execute(req, (nom, prenom, telephone, mail, contact_id))
            conn.commit()
            conn.close()

            QMessageBox.information(fen, "Succès", "Le contact a été modifié avec succès.")
            lineEditNom.clear()
            lineEditPrenom.clear()
            lineEditTelephone.clear()
            lineEditMail.clear()
            chargerContacts()
        else:
            QMessageBox.warning(fen, "Erreur", "Veuillez remplir tous les champs.")
    else:
        QMessageBox.warning(fen, "Erreur", "Veuillez sélectionner un contact à modifier.")

def supprimerContact():
    selected_row = tableWidget.currentRow()
    if selected_row != -1:
        contact_id = tableWidget.item(selected_row, 0).text()
        reply = QMessageBox.question(fen, 'Confirmation', 'Êtes-vous sûr de vouloir supprimer ce contact ?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect("carnetAdress.db")
            cursor = conn.cursor()
            req = "DELETE FROM contacts WHERE id = ?"
            cursor.execute(req, (contact_id,))
            conn.commit()
            conn.close()
            QMessageBox.information(fen, "Succès", "Le contact a été supprimé avec succès.")
            chargerContacts()
            lineEditNom.clear()
            lineEditPrenom.clear()
            lineEditTelephone.clear()
            lineEditMail.clear()
    else:
        QMessageBox.warning(fen, "Erreur", "Veuillez sélectionner un contact à supprimer.")

app = QApplication(sys.argv)
fen = QWidget()
fen.setWindowTitle("CARNET D'ADRESSE")
fen.setGeometry(0, 0, 800, 600)
fen.setStyleSheet("""
    QWidget {
        background-color: #f0f0f0;
        font-family: Arial, sans-serif;
    }

    QLabel {
        font-size: 14px;
        color: #333333;
        padding: 5px;
    }

    QLineEdit {
        border: 2px solid #cccccc;
        border-radius: 5px;
        padding: 5px;
        background-color: #ffffff;
    }

    QPushButton {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 8px 16px;
        font-size: 14px;
        border: none;
    }

    QPushButton:hover {
        background-color: #45a049;
    }

    QPushButton:pressed {
        background-color: #3e8e41;
    }

    QTableWidget {
        border: 1px solid #cccccc;
        background-color: #ffffff;
        gridline-color: #cccccc;
        font-size: 13px;
    }

    QHeaderView::section {
        background-color: #dddddd;
        padding: 5px;
        border: 1px solid #cccccc;
    }
""")
grid = QGridLayout(fen)
fen.setLayout(grid)

labelNom = QLabel("Nom")
labelPrenom = QLabel("Prénom")
labelTelefone = QLabel("Téléphone")
labelMail = QLabel("Mail")

lineEditNom = QLineEdit()
lineEditPrenom = QLineEdit()
lineEditTelephone = QLineEdit()
lineEditMail = QLineEdit()

# Ajouter les labels et champs de saisie à la grille
grid.addWidget(labelNom, 0, 0)
grid.addWidget(lineEditNom, 1, 0)
grid.addWidget(labelPrenom, 0, 1)
grid.addWidget(lineEditPrenom, 1, 1)
grid.addWidget(labelTelefone, 0, 2)
grid.addWidget(lineEditTelephone, 1, 2)
grid.addWidget(labelMail, 0, 3)
grid.addWidget(lineEditMail, 1, 3)

# Créer et ajouter les boutons
buttonAjouter = QPushButton("Ajouter")
grid.addWidget(buttonAjouter, 2, 0)

buttonModifier = QPushButton("Modifier")
grid.addWidget(buttonModifier, 2, 1)

buttonSupprimer = QPushButton("Supprimer")
grid.addWidget(buttonSupprimer, 2, 2)

buttonInitialiser = QPushButton("Initialiser")
grid.addWidget(buttonInitialiser, 2, 3)

# Ajouter le QTableWidget pour afficher les contacts
tableWidget = QTableWidget()
grid.addWidget(tableWidget, 3, 0, 1, 4)

# Connecter les boutons aux fonctions
buttonInitialiser.clicked.connect(creerTableCarnetAdress)
buttonAjouter.clicked.connect(ajouterContact)
buttonModifier.clicked.connect(modifierContact)
buttonSupprimer.clicked.connect(supprimerContact)
fen.show()
# Connecter la sélection de ligne à la fonction de remplissage des champs
tableWidget.itemSelectionChanged.connect(remplirChampsAvecSelection)
#Charger les contacts au démarrage
chargerContacts()
app.exec()
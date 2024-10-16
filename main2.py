from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox, \
    QTableWidget, QTableWidgetItem , QDateEdit
import sqlite3


def creerTableCarnetAdress():
    print("Créer la table")
    conn = sqlite3.connect("carnetAdress.db")
    cursor = conn.cursor()
    req = "CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT NOT NULL, prenom TEXT NOT NULL, telephone TEXT NOT NULL, mail TEXT NOT NULL , naissance TEXT NOT NULL , adresse TEXT NOT NULL)"
    cursor.execute(req)
    conn.commit()
    conn.close()
    print("La base de données et la table ont été créées avec succès.")


def ajouterContact():
    nom = lineEditNom.text()
    prenom = lineEditPrenom.text()
    telephone = lineEditTelephone.text()
    mail = lineEditMail.text()
    naissance = lineEditNaissance.text()
    adresse = lineEditAdresse.text()

    if nom and prenom and telephone and mail and naissance and adresse:
        conn = sqlite3.connect("carnetAdress.db")
        cursor = conn.cursor()
        req = "INSERT INTO contacts (nom, prenom, telephone, mail , naissance, adresse) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(req, (nom, prenom, telephone, mail , naissance, adresse))
        conn.commit()
        conn.close()

        # Afficher un message de confirmation
        QMessageBox.information(fen, "Succès", "Le contact a été ajouté avec succès.")

        # Réinitialiser les champs
        lineEditNom.clear()
        lineEditPrenom.clear()
        lineEditTelephone.clear()
        lineEditMail.clear()
        lineEditNaissance.clear()
        lineEditAdresse.clear()

        # Recharger les contacts
        chargerContacts()
    else:
        QMessageBox.warning(fen, "Erreur", "Veuillez remplir tous les champs.")
def chargerContacts():
    conn = sqlite3.connect("carnetAdress.db")
    cursor = conn.cursor()
    req = "SELECT * FROM contacts"
    cursor.execute(req)
    contacts = cursor.fetchall()
    conn.close()

    # Ajuster pour 5 colonnes : 1 pour l'ID (cachée) et 4 pour les autres champs
    tableWidget.setRowCount(len(contacts))
    tableWidget.setColumnCount(7)
    tableWidget.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Téléphone", "Mail" , "Date de naissance" , "Adresse" ])

    for row_idx, contact in enumerate(contacts):
        for col_idx, data in enumerate(contact):
            item = QTableWidgetItem(str(data))
            if col_idx == 0:  # Si c'est l'ID, on le cache
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Rendre non modifiable
                tableWidget.setColumnHidden(0, True)  # Cacher la colonne
            tableWidget.setItem(row_idx, col_idx, item)
def remplirChampsAvecSelection():
    selected_row = tableWidget.currentRow()
    if selected_row != -1:
        # Récupérer les informations de la ligne sélectionnée et les mettre dans les champs
        lineEditNom.setText(tableWidget.item(selected_row, 1).text())
        lineEditPrenom.setText(tableWidget.item(selected_row, 2).text())
        lineEditTelephone.setText(tableWidget.item(selected_row, 3).text())
        lineEditMail.setText(tableWidget.item(selected_row, 4).text())
        lineEditNaissance.setText(tableWidget.item(selected_row, 5).text())
        lineEditAdresse.setText(tableWidget.item(selected_row, 6).text())

def modifierContact():
    selected_row = tableWidget.currentRow()
    if selected_row != -1:
        contact_id = tableWidget.item(selected_row, 0).text()
        nom = lineEditNom.text()
        prenom = lineEditPrenom.text()
        telephone = lineEditTelephone.text()
        mail = lineEditMail.text()
        naissance = lineEditNaissance.text()
        adresse = lineEditAdresse.text()

        if nom and prenom and telephone and mail and naissance and adresse:
            conn = sqlite3.connect("carnetAdress.db")
            cursor = conn.cursor()
            req = "UPDATE contacts SET nom = ?, prenom = ?, telephone = ?, mail = ? , naissance = ? , adresse = ? WHERE id = ?"
            cursor.execute(req, (nom, prenom, telephone, mail, naissance , adresse ,  contact_id))
            conn.commit()
            conn.close()

            QMessageBox.information(fen, "Succès", "Le contact a été modifié avec succès.")
            lineEditNom.clear()
            lineEditPrenom.clear()
            lineEditTelephone.clear()
            lineEditMail.clear()
            lineEditNaissance.clear()
            lineEditAdresse.clear()
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
            lineEditNaissance.clear()
            lineEditAdresse.clear()
    else:
        QMessageBox.warning(fen, "Erreur", "Veuillez sélectionner un contact à supprimer.")

app = QApplication([])
fen = QWidget()
fen.setWindowTitle("CARNET D'ADRESSE")
fen.setGeometry(0, 0, 1000, 800)
fen.setStyleSheet("""
    QWidget {
        background-color: #f0f0f0;
        font-family: Arial, sans-serif;
    }

    QLabel {
        font-size: 15px;
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
        font-size: 15px;
        border: none;
    }

    QPushButton:hover {
        background-color: #45a049;
    }

    QPushButton:pressed {
        background-color: #3e8e41;
    }

    QTableWidget {
        border: 10px solid #cccccc;
        background-color: #ffffff;
        gridline-color: #cccccc;
        font-size: 15px;
    }

    QHeaderView::section {
        background-color: #dddddd;
        padding: 5px;
        border: 1px solid #cccccc;
    }
""")
grid = QGridLayout(fen)
fen.setLayout(grid)

#grid.setContentsMargins(10, 10, 10, 10)
#grid.setSpacing(10)

labelNom = QLabel("Nom")
labelPrenom = QLabel("Prénom")
labelTelefone = QLabel("Téléphone")
labelMail = QLabel("Mail")
labelNaissance = QLabel("Naissance")



labelAdresse = QLabel("Adresse")

lineEditNom = QLineEdit()
lineEditPrenom = QLineEdit()
lineEditTelephone = QLineEdit()
lineEditMail = QLineEdit()
lineEditNaissance = QLineEdit()

lineEditAdresse = QLineEdit()

# Ajouter les labels et champs de saisie à la grille
grid.addWidget(labelNom, 0, 0)
grid.addWidget(lineEditNom, 1, 0)
grid.addWidget(labelPrenom, 0, 1)
grid.addWidget(lineEditPrenom, 1, 1)
grid.addWidget(labelTelefone, 0, 2)
grid.addWidget(lineEditTelephone, 1, 2)
grid.addWidget(labelMail, 2, 0)
grid.addWidget(lineEditMail, 3, 0)
grid.addWidget(labelNaissance, 2, 1)
grid.addWidget(lineEditNaissance, 3, 1)
grid.addWidget(labelAdresse, 2, 2)
grid.addWidget(lineEditAdresse, 3, 2)

# Créer et ajouter le bouton "Ajouter"
buttonAjouter = QPushButton("Ajouter")
grid.addWidget(buttonAjouter, 4, 0)

buttonModifier = QPushButton("Modifier")
grid.addWidget(buttonModifier, 4, 1)

buttonSupprimer = QPushButton("Supprimer")
grid.addWidget(buttonSupprimer, 4, 2)
# Ajouter le QTableWidget pour afficher les contacts
tableWidget = QTableWidget()
grid.addWidget(tableWidget, 5, 0, 1, 4)

buttonInitialiser = QPushButton("Initialiser")
grid.addWidget(buttonInitialiser, 4, 3)

# Connecter le bouton "Ajouter" à la fonction ajouterContact
buttonAjouter.clicked.connect(ajouterContact)
buttonModifier.clicked.connect(modifierContact)
buttonSupprimer.clicked.connect(supprimerContact)
buttonInitialiser.clicked.connect(creerTableCarnetAdress)

fen.show()

# Créer la table au démarrage
creerTableCarnetAdress()
tableWidget.itemSelectionChanged.connect(remplirChampsAvecSelection)
# Charger les contacts au démarrage
chargerContacts()
app.exec()

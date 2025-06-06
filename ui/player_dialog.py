from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                           QLineEdit, QSpinBox, QComboBox, QPushButton,
                           QDateEdit)
from PyQt5.QtCore import Qt, QDate
from database import Player
from datetime import date

class PlayerDialog(QDialog):
    def __init__(self, parent=None, player=None):
        super().__init__(parent)
        self.player = player
        self.setWindowTitle("Add Player" if player is None else "Edit Player")
        self.setup_ui()
        if player:
            self.load_player_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Create input fields
        self.name_edit = QLineEdit()
        self.age_spin = QSpinBox()
        self.age_spin.setRange(16, 45)
        self.age_spin.setValue(20)

        self.position_combo = QComboBox()
        self.position_combo.addItems(["Forward", "Midfielder", "Defender", "Goalkeeper"])

        self.nationality_edit = QLineEdit()

        # Stats spinboxes
        self.stats_boxes = {}
        for stat in ["Attack", "Defense", "Stamina", "Speed", "Technique"]:
            spin = QSpinBox()
            spin.setRange(1, 100)
            spin.setValue(50)
            self.stats_boxes[stat.lower()] = spin
            form_layout.addRow(f"{stat}:", spin)

        # Contract details
        self.wage_spin = QSpinBox()
        self.wage_spin.setRange(1000, 1000000)
        self.wage_spin.setValue(10000)
        self.wage_spin.setSingleStep(1000)

        self.value_spin = QSpinBox()
        self.value_spin.setRange(100000, 300000000)
        self.value_spin.setValue(1000000)
        self.value_spin.setSingleStep(100000)

        self.contract_end = QDateEdit()
        self.contract_end.setDate(QDate.currentDate().addYears(3))
        self.contract_end.setCalendarPopup(True)

        # Add fields to form layout
        form_layout.addRow("Name:", self.name_edit)
        form_layout.addRow("Age:", self.age_spin)
        form_layout.addRow("Position:", self.position_combo)
        form_layout.addRow("Nationality:", self.nationality_edit)
        form_layout.addRow("Weekly Wage (£):", self.wage_spin)
        form_layout.addRow("Value (£):", self.value_spin)
        form_layout.addRow("Contract End:", self.contract_end)

        layout.addLayout(form_layout)

        # Add buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def load_player_data(self):
        """Load existing player data into the form"""
        self.name_edit.setText(self.player.name)
        self.age_spin.setValue(self.player.age)
        self.position_combo.setCurrentText(self.player.position)
        self.nationality_edit.setText(self.player.nationality)
        
        # Load stats
        self.stats_boxes["attack"].setValue(self.player.attack)
        self.stats_boxes["defense"].setValue(self.player.defense)
        self.stats_boxes["stamina"].setValue(self.player.stamina)
        self.stats_boxes["speed"].setValue(self.player.speed)
        self.stats_boxes["technique"].setValue(self.player.technique)
        
        # Load contract details
        self.wage_spin.setValue(int(self.player.wage))
        self.value_spin.setValue(int(self.player.value))
        self.contract_end.setDate(QDate.fromString(str(self.player.contract_end), Qt.ISODate))

    def get_player_data(self):
        """Get the player data from the form"""
        return {
            "name": self.name_edit.text(),
            "age": self.age_spin.value(),
            "position": self.position_combo.currentText(),
            "nationality": self.nationality_edit.text(),
            "attack": self.stats_boxes["attack"].value(),
            "defense": self.stats_boxes["defense"].value(),
            "stamina": self.stats_boxes["stamina"].value(),
            "speed": self.stats_boxes["speed"].value(),
            "technique": self.stats_boxes["technique"].value(),
            "wage": float(self.wage_spin.value()),
            "value": float(self.value_spin.value()),
            "contract_end": date.fromisoformat(self.contract_end.date().toString(Qt.ISODate))
        }

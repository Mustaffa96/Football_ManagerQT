from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                           QLineEdit, QPushButton, QFormLayout, QDoubleSpinBox)
from PyQt5.QtCore import Qt
from database import Team

class TeamDialog(QDialog):
    def __init__(self, parent=None, team=None):
        super().__init__(parent)
        self.team = team
        self.setup_ui()
        if team:
            self.load_team_data()

    def setup_ui(self):
        self.setWindowTitle("Add Team" if not self.team else "Edit Team")
        layout = QVBoxLayout(self)

        # Form layout for team details
        form_layout = QFormLayout()

        # Team name
        self.name_edit = QLineEdit()
        form_layout.addRow("Team Name:", self.name_edit)

        # Country
        self.country_edit = QLineEdit()
        form_layout.addRow("Country:", self.country_edit)

        # League
        self.league_edit = QLineEdit()
        form_layout.addRow("League:", self.league_edit)

        # Budget
        self.budget_spin = QDoubleSpinBox()
        self.budget_spin.setRange(0, 1000000000)  # 1 billion max
        self.budget_spin.setPrefix("$")
        self.budget_spin.setSingleStep(1000000)  # 1 million step
        form_layout.addRow("Budget:", self.budget_spin)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")

        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

    def load_team_data(self):
        """Load existing team data into the form"""
        self.name_edit.setText(self.team.name)
        self.country_edit.setText(self.team.country)
        self.league_edit.setText(self.team.league)
        self.budget_spin.setValue(self.team.budget)

    def get_team_data(self):
        """Get the team data from the form"""
        return {
            "name": self.name_edit.text(),
            "country": self.country_edit.text(),
            "league": self.league_edit.text(),
            "budget": self.budget_spin.value()
        }

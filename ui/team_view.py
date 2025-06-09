from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                           QTableWidgetItem, QPushButton, QLabel, QLineEdit,
                           QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from database import get_session, Team
from .team_dialog import TeamDialog

class TeamView(QWidget):
    def __init__(self):
        super().__init__()
        self.session = get_session()
        self.setup_ui()
        self.load_teams()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search Teams:")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search by name, country, or league...")
        self.search_edit.textChanged.connect(self.filter_teams)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)
        layout.addLayout(search_layout)
        
        # Teams table
        self.teams_table = QTableWidget()
        self.teams_table.setColumnCount(4)
        self.teams_table.setHorizontalHeaderLabels([
            "Team Name", "Country", "League", "Budget"
        ])
        
        # Enable sorting
        self.teams_table.setSortingEnabled(True)
        
        # Set column widths
        header = self.teams_table.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        
        # Set alternating row colors
        self.teams_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.teams_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.add_team_btn = QPushButton("Add Team")
        self.edit_team_btn = QPushButton("Edit Team")
        self.remove_team_btn = QPushButton("Remove Team")
        
        self.add_team_btn.clicked.connect(self.add_team)
        self.edit_team_btn.clicked.connect(self.edit_team)
        self.remove_team_btn.clicked.connect(self.remove_team)
        
        button_layout.addWidget(self.add_team_btn)
        button_layout.addWidget(self.edit_team_btn)
        button_layout.addWidget(self.remove_team_btn)
        
        layout.addLayout(button_layout)
        
        # Update button states
        self.teams_table.itemSelectionChanged.connect(self.update_button_states)
        self.update_button_states()

    def load_teams(self):
        """Load all teams into the table"""
        self.teams = self.session.query(Team).all()
        self.filter_teams()

    def filter_teams(self):
        """Filter teams based on search text"""
        search_text = self.search_edit.text().lower()
        
        self.teams_table.setRowCount(0)
        for team in self.teams:
            if (search_text in team.name.lower() or
                search_text in team.country.lower() or
                search_text in team.league.lower()):
                
                row = self.teams_table.rowCount()
                self.teams_table.insertRow(row)
                
                # Create items
                items = [
                    QTableWidgetItem(team.name),
                    QTableWidgetItem(team.country),
                    QTableWidgetItem(team.league),
                    QTableWidgetItem(f"${team.budget:,.2f}")
                ]
                
                # Store team ID in the first column
                items[0].setData(Qt.UserRole, team.id)
                
                # Set items
                for col, item in enumerate(items):
                    self.teams_table.setItem(row, col, item)

    def update_button_states(self):
        """Enable/disable buttons based on selection"""
        has_selection = len(self.teams_table.selectedItems()) > 0
        self.edit_team_btn.setEnabled(has_selection)
        self.remove_team_btn.setEnabled(has_selection)

    def get_selected_team(self):
        """Get the currently selected team"""
        selected_items = self.teams_table.selectedItems()
        if not selected_items:
            return None
        
        row = selected_items[0].row()
        team_id = self.teams_table.item(row, 0).data(Qt.UserRole)
        return self.session.query(Team).get(team_id)

    def add_team(self):
        """Add a new team"""
        dialog = TeamDialog(self)
        if dialog.exec_():
            team_data = dialog.get_team_data()
            team = Team(**team_data)
            
            self.session.add(team)
            self.session.commit()
            self.load_teams()

    def edit_team(self):
        """Edit the selected team"""
        team = self.get_selected_team()
        if not team:
            return
            
        dialog = TeamDialog(self, team)
        if dialog.exec_():
            team_data = dialog.get_team_data()
            for key, value in team_data.items():
                setattr(team, key, value)
            
            self.session.commit()
            self.load_teams()

    def remove_team(self):
        """Remove the selected team"""
        team = self.get_selected_team()
        if not team:
            return
            
        if team.players:
            QMessageBox.warning(
                self,
                "Cannot Remove Team",
                "This team still has players. Remove or transfer all players first.",
                QMessageBox.Ok
            )
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Are you sure you want to remove {team.name}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.session.delete(team)
            self.session.commit()
            self.load_teams()

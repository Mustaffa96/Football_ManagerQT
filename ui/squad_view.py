from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                           QTableWidgetItem, QPushButton, QLabel, QComboBox,
                           QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from database import get_session, Player, Team
from .player_dialog import PlayerDialog

class SquadView(QWidget):
    def __init__(self):
        super().__init__()
        self.session = get_session()
        self.setup_ui()
        self.load_squad_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Team selector
        team_layout = QHBoxLayout()
        team_label = QLabel("Select Team:")
        self.team_combo = QComboBox()
        self.load_teams()
        team_layout.addWidget(team_label)
        team_layout.addWidget(self.team_combo)
        team_layout.addStretch()
        layout.addLayout(team_layout)
        
        # Squad table
        self.squad_table = QTableWidget()
        self.squad_table.setColumnCount(8)
        self.squad_table.setHorizontalHeaderLabels([
            "Name", "Position", "Age", "Attack", "Defense",
            "Stamina", "Speed", "Technique"
        ])
        
        # Set column widths
        header = self.squad_table.horizontalHeader()
        for i in range(8):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        
        layout.addWidget(self.squad_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.add_player_btn = QPushButton("Add Player")
        self.edit_player_btn = QPushButton("Edit Player")
        self.remove_player_btn = QPushButton("Remove Player")
        
        button_layout.addWidget(self.add_player_btn)
        button_layout.addWidget(self.edit_player_btn)
        button_layout.addWidget(self.remove_player_btn)
        
        layout.addLayout(button_layout)
        
        # Connect signals
        self.team_combo.currentIndexChanged.connect(self.load_squad_data)
        self.add_player_btn.clicked.connect(self.add_player)
        self.edit_player_btn.clicked.connect(self.edit_player)
        self.remove_player_btn.clicked.connect(self.remove_player)
        
        # Enable/disable buttons based on selection
        self.squad_table.itemSelectionChanged.connect(self.update_button_states)
        self.update_button_states()

    def load_teams(self):
        teams = self.session.query(Team).all()
        for team in teams:
            self.team_combo.addItem(team.name, team.id)

    def load_squad_data(self):
        team_id = self.team_combo.currentData()
        if team_id is None:
            return
            
        players = self.session.query(Player).filter_by(team_id=team_id).all()
        self.squad_table.setRowCount(len(players))
        
        for row, player in enumerate(players):
            self.squad_table.setItem(row, 0, QTableWidgetItem(player.name))
            self.squad_table.setItem(row, 1, QTableWidgetItem(player.position))
            self.squad_table.setItem(row, 2, QTableWidgetItem(str(player.age)))
            self.squad_table.setItem(row, 3, QTableWidgetItem(str(player.attack)))
            self.squad_table.setItem(row, 4, QTableWidgetItem(str(player.defense)))
            self.squad_table.setItem(row, 5, QTableWidgetItem(str(player.stamina)))
            self.squad_table.setItem(row, 6, QTableWidgetItem(str(player.speed)))
            self.squad_table.setItem(row, 7, QTableWidgetItem(str(player.technique)))
            
            # Store player id in the first column for reference
            self.squad_table.item(row, 0).setData(Qt.UserRole, player.id)

    def update_button_states(self):
        has_selection = len(self.squad_table.selectedItems()) > 0
        self.edit_player_btn.setEnabled(has_selection)
        self.remove_player_btn.setEnabled(has_selection)

    def get_selected_player(self):
        selected_items = self.squad_table.selectedItems()
        if not selected_items:
            return None
        
        row = selected_items[0].row()
        player_id = self.squad_table.item(row, 0).data(Qt.UserRole)
        return self.session.query(Player).get(player_id)

    def add_player(self):
        team_id = self.team_combo.currentData()
        if team_id is None:
            return
            
        dialog = PlayerDialog(self)
        if dialog.exec_():
            player_data = dialog.get_player_data()
            player = Player(**player_data)
            player.team_id = team_id
            
            self.session.add(player)
            self.session.commit()
            self.load_squad_data()

    def edit_player(self):
        player = self.get_selected_player()
        if not player:
            return
            
        dialog = PlayerDialog(self, player)
        if dialog.exec_():
            player_data = dialog.get_player_data()
            for key, value in player_data.items():
                setattr(player, key, value)
            
            self.session.commit()
            self.load_squad_data()

    def remove_player(self):
        player = self.get_selected_player()
        if not player:
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Are you sure you want to remove {player.name} from the squad?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.session.delete(player)
            self.session.commit()
            self.load_squad_data()

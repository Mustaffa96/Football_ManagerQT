from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                           QTableWidgetItem, QPushButton, QLabel, QComboBox,
                           QHeaderView, QMessageBox, QLineEdit)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QColor
from database import get_session, Player, Team
from .player_dialog import PlayerDialog

class SortableTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        if isinstance(self.data(Qt.DisplayRole), str) and isinstance(other.data(Qt.DisplayRole), str):
            return self.data(Qt.DisplayRole).lower() < other.data(Qt.DisplayRole).lower()
        try:
            return float(self.data(Qt.DisplayRole)) < float(other.data(Qt.DisplayRole))
        except ValueError:
            return super().__lt__(other)

class SquadView(QWidget):
    def __init__(self):
        super().__init__()
        self.session = get_session()
        self.setup_ui()
        self.load_squad_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Team selector and search
        top_layout = QHBoxLayout()
        
        # Team selector
        team_layout = QHBoxLayout()
        team_label = QLabel("Select Team:")
        team_label.setProperty("class", "section-label")
        self.team_combo = QComboBox()
        self.load_teams()
        team_layout.addWidget(team_label)
        team_layout.addWidget(self.team_combo)
        top_layout.addLayout(team_layout)
        
        # Search
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_label.setProperty("class", "section-label")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search players...")
        self.search_edit.textChanged.connect(self.filter_squad_data)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)
        top_layout.addLayout(search_layout)
        
        # Position filter
        position_layout = QHBoxLayout()
        position_label = QLabel("Position:")
        position_label.setProperty("class", "section-label")
        self.position_filter = QComboBox()
        self.position_filter.addItems(["All", "Forward", "Midfielder", "Defender", "Goalkeeper"])
        self.position_filter.currentTextChanged.connect(self.filter_squad_data)
        position_layout.addWidget(position_label)
        position_layout.addWidget(self.position_filter)
        top_layout.addLayout(position_layout)
        
        layout.addLayout(top_layout)
        
        # Squad table
        self.squad_table = QTableWidget()
        self.squad_table.setColumnCount(8)
        self.squad_table.setHorizontalHeaderLabels([
            "Name", "Position", "Age", "Attack", "Defense",
            "Stamina", "Speed", "Technique"
        ])
        
        # Enable sorting
        self.squad_table.setSortingEnabled(True)
        
        # Set column widths
        header = self.squad_table.horizontalHeader()
        for i in range(8):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        
        # Set alternating row colors
        self.squad_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.squad_table)
        
        # Stats summary
        stats_layout = QHBoxLayout()
        self.squad_stats_label = QLabel()
        self.squad_stats_label.setProperty("class", "section-label")
        stats_layout.addWidget(self.squad_stats_label)
        layout.addLayout(stats_layout)
        
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
            
        self.current_players = self.session.query(Player).filter_by(team_id=team_id).all()
        self.filter_squad_data()
        self.update_squad_stats()

    def filter_squad_data(self):
        if not hasattr(self, 'current_players'):
            return
            
        search_text = self.search_edit.text().lower()
        position_filter = self.position_filter.currentText()
        
        filtered_players = []
        for player in self.current_players:
            # Apply search filter
            if search_text and search_text not in player.name.lower():
                continue
                
            # Apply position filter
            if position_filter != "All" and player.position != position_filter:
                continue
                
            filtered_players.append(player)
        
        self.squad_table.setRowCount(len(filtered_players))
        for row, player in enumerate(filtered_players):
            # Name with colored stats
            name_item = SortableTableWidgetItem(player.name)
            name_item.setData(Qt.UserRole, player.id)
            
            # Create items
            items = [
                name_item,
                SortableTableWidgetItem(player.position),
                SortableTableWidgetItem(str(player.age)),
                SortableTableWidgetItem(str(player.attack)),
                SortableTableWidgetItem(str(player.defense)),
                SortableTableWidgetItem(str(player.stamina)),
                SortableTableWidgetItem(str(player.speed)),
                SortableTableWidgetItem(str(player.technique))
            ]
            
            # Set items with color based on stats
            for col, item in enumerate(items):
                self.squad_table.setItem(row, col, item)
                if col >= 3:  # Stats columns
                    stat_value = int(item.text())
                    if stat_value >= 80:
                        item.setForeground(QColor("#27ae60"))  # Good (green)
                    elif stat_value >= 60:
                        item.setForeground(QColor("#f39c12"))  # Medium (orange)
                    else:
                        item.setForeground(QColor("#c0392b"))  # Poor (red)

    def update_squad_stats(self):
        if not hasattr(self, 'current_players') or not self.current_players:
            self.squad_stats_label.setText("")
            return
            
        avg_attack = sum(p.attack for p in self.current_players) / len(self.current_players)
        avg_defense = sum(p.defense for p in self.current_players) / len(self.current_players)
        avg_stamina = sum(p.stamina for p in self.current_players) / len(self.current_players)
        
        stats_text = (f"Squad Stats - Attack: {avg_attack:.1f} | "
                     f"Defense: {avg_defense:.1f} | "
                     f"Stamina: {avg_stamina:.1f}")
        self.squad_stats_label.setText(stats_text)

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

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QGraphicsEllipseItem,
    QGraphicsTextItem,
    QInputDialog,
    QMessageBox,
    QMenu,
)
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor
from database import get_session, Player, Team, TeamTactics


class PlayerItem(QGraphicsEllipseItem):
    # Define available roles for each position
    ROLES = {
        "GK": ["Goalkeeper", "Sweeper Keeper"],
        "D": [
            "Centre-Back",
            "Full-Back",
            "Wing-Back",
            "Ball-Playing Defender",
            "Libero",
        ],
        "M": [
            "Central Midfielder",
            "Defensive Midfielder",
            "Attacking Midfielder",
            "Box-to-Box",
            "Deep-Lying Playmaker",
            "Wide Midfielder",
            "Winger",
        ],
        "F": [
            "Target Man",
            "Poacher",
            "Complete Forward",
            "False Nine",
            "Inside Forward",
            "Advanced Forward",
        ],
    }

    def __init__(self, player, x, y, parent=None):
        super().__init__(0, 0, 30, 30, parent)
        self.player = player
        self.setPos(x, y)
        self.setBrush(QBrush(QColor("#3498db")))
        self.setPen(QPen(Qt.black))
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)

        # Add player name and role labels
        self.name_label = QGraphicsTextItem(self)
        self.name_label.setPlainText(player.name)
        self.name_label.setDefaultTextColor(Qt.white)
        # Center the name text
        br = self.name_label.boundingRect()
        self.name_label.setPos(-br.width() / 2 + 15, -br.height() / 2 + 15)

        self.role_label = QGraphicsTextItem(self)
        self.role_label.setDefaultTextColor(Qt.yellow)
        self.role_label.setPos(-br.width() / 2 + 15, br.height() / 2 + 15)

        self.current_role = None

    def set_role(self, role):
        self.current_role = role
        self.role_label.setPlainText(role if role else "")
        # Update color based on role
        if role:
            if "Attacking" in role or "Forward" in role:
                self.setBrush(QBrush(QColor("#e74c3c")))  # Red for attacking roles
            elif "Defensive" in role or "Centre-Back" in role:
                self.setBrush(QBrush(QColor("#2ecc71")))  # Green for defensive roles
            elif "Midfielder" in role:
                self.setBrush(QBrush(QColor("#3498db")))  # Blue for midfield roles
            elif "Goalkeeper" in role:
                self.setBrush(QBrush(QColor("#f1c40f")))  # Yellow for goalkeeper

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.show_role_menu(event)
        else:
            super().mousePressEvent(event)

    def show_role_menu(self, event):
        menu = QMenu()

        # Determine available roles based on player's position
        if self.player.position.startswith("GK"):
            roles = self.ROLES["GK"]
        elif self.player.position.startswith("D"):
            roles = self.ROLES["D"]
        elif self.player.position.startswith("M"):
            roles = self.ROLES["M"]
        elif self.player.position.startswith("F"):
            roles = self.ROLES["F"]
        else:
            roles = []

        # Add role options to menu
        for role in roles:
            action = menu.addAction(role)
            action.setCheckable(True)
            if self.current_role == role:
                action.setChecked(True)

        # Add a "Clear Role" option
        menu.addSeparator()
        clear_action = menu.addAction("Clear Role")

        # Show menu and handle selection
        action = menu.exec_(event.screenPos().toPoint())
        if action:
            if action == clear_action:
                self.set_role(None)
            else:
                self.set_role(action.text())

        # Notify TacticsView of role change
        self.scene().parent().parent().update_player_roles()


class PitchView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setup_pitch()

    def setup_pitch(self):
        # Set the pitch dimensions (scale to 100x60 units)
        pitch_width = 800
        pitch_height = 500
        margin = 50  # Add margin for better visibility
        
        # Set scene rect with margins
        self.setSceneRect(-margin, -margin, pitch_width + 2*margin, pitch_height + 2*margin)

        # Draw pitch outline
        self.scene.addRect(
            0, 0, pitch_width, pitch_height, QPen(Qt.white), QBrush(QColor("#27ae60"))
        )

        # Draw center line
        self.scene.addLine(
            pitch_width / 2, 0, pitch_width / 2, pitch_height, QPen(Qt.white)
        )

        # Draw center circle
        self.scene.addEllipse(
            pitch_width / 2 - 50, pitch_height / 2 - 50, 100, 100, QPen(Qt.white)
        )

        # Draw penalty areas
        # Left penalty area
        self.scene.addRect(0, pitch_height / 2 - 110, 130, 220, QPen(Qt.white))
        # Right penalty area
        self.scene.addRect(
            pitch_width - 130, pitch_height / 2 - 110, 130, 220, QPen(Qt.white)
        )


class TacticsView(QWidget):
    FORMATIONS = {
        "4-4-2": [
            # Strikers
            [(600, 150), (600, 350)],
            # Midfielders
            [(450, 100), (450, 200), (450, 300), (450, 400)],
            # Defenders
            [(200, 100), (200, 200), (200, 300), (200, 400)],
            # Goalkeeper
            [(80, 250)],
        ],
        "4-4-2 Diamond": [
            # Strikers
            [(600, 150), (600, 350)],
            # Midfielders (Diamond: CAM, 2xCM, CDM)
            [(500, 250), (450, 150), (450, 350), (400, 250)],
            # Defenders
            [(200, 100), (200, 200), (200, 300), (200, 400)],
            # Goalkeeper
            [(80, 250)],
        ],
        "4-3-3": [
            # Strikers
            [(600, 150), (600, 250), (600, 350)],
            # Midfielders
            [(450, 150), (450, 250), (450, 350)],
            # Defenders
            [(200, 100), (200, 200), (200, 300), (200, 400)],
            # Goalkeeper
            [(80, 250)],
        ],
        "4-3-3 Holding": [
            # Strikers
            [(600, 150), (600, 250), (600, 350)],
            # Midfielders (2 CM, 1 CDM)
            [(500, 175), (500, 325), (400, 250)],
            # Defenders
            [(200, 100), (200, 200), (200, 300), (200, 400)],
            # Goalkeeper
            [(80, 250)],
        ],
        "4-2-3-1": [
            # Striker
            [(600, 250)],
            # Attacking Midfielders
            [(500, 150), (500, 250), (500, 350)],
            # Defensive Midfielders
            [(400, 175), (400, 325)],
            # Defenders
            [(200, 100), (200, 200), (200, 300), (200, 400)],
            # Goalkeeper
            [(80, 250)],
        ],
        "3-5-2": [
            # Strikers
            [(600, 150), (600, 350)],
            # Midfielders
            [(450, 100), (450, 175), (450, 250), (450, 325), (450, 400)],
            # Defenders
            [(200, 150), (200, 250), (200, 350)],
            # Goalkeeper
            [(80, 250)],
        ],
        "3-4-3": [
            # Strikers
            [(600, 150), (600, 250), (600, 350)],
            # Midfielders
            [(450, 125), (450, 225), (450, 325), (450, 425)],
            # Defenders
            [(200, 150), (200, 250), (200, 350)],
            # Goalkeeper
            [(80, 250)],
        ],
        "5-3-2": [
            # Strikers
            [(600, 150), (600, 350)],
            # Midfielders
            [(450, 150), (450, 250), (450, 350)],
            # Defenders
            [(200, 50), (200, 150), (200, 250), (200, 350), (200, 450)],
            # Goalkeeper
            [(80, 250)],
        ],
        "4-5-1": [
            # Striker
            [(600, 250)],
            # Midfielders
            [(450, 50), (450, 150), (450, 250), (450, 350), (450, 450)],
            # Defenders
            [(200, 100), (200, 200), (200, 300), (200, 400)],
            # Goalkeeper
            [(80, 250)],
        ],
        "4-1-4-1": [
            # Striker
            [(600, 250)],
            # Advanced Midfielders
            [(500, 100), (500, 200), (500, 300), (500, 400)],
            # Defensive Midfielder
            [(400, 250)],
            # Defenders
            [(200, 100), (200, 200), (200, 300), (200, 400)],
            # Goalkeeper
            [(80, 250)],
        ],
    }

    def __init__(self):
        super().__init__()
        self.session = get_session()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Top controls
        controls_layout = QHBoxLayout()

        # Team selector
        team_layout = QHBoxLayout()
        team_label = QLabel("Select Team:")
        team_label.setProperty("class", "section-label")
        self.team_combo = QComboBox()
        self.load_teams()
        team_layout.addWidget(team_label)
        team_layout.addWidget(self.team_combo)
        controls_layout.addLayout(team_layout)

        # Saved tactics selector
        tactics_layout = QHBoxLayout()
        tactics_label = QLabel("Saved Tactics:")
        tactics_label.setProperty("class", "section-label")
        self.tactics_combo = QComboBox()
        self.tactics_combo.currentIndexChanged.connect(self.load_tactics)
        tactics_layout.addWidget(tactics_label)
        tactics_layout.addWidget(self.tactics_combo)
        controls_layout.addLayout(tactics_layout)

        # Formation selector with categories
        formation_layout = QVBoxLayout()
        formation_label = QLabel("Formation:")
        formation_label.setProperty("class", "section-label")
        self.formation_combo = QComboBox()

        # Group formations by style
        formations_by_style = {
            "Classic": ["4-4-2", "4-3-3", "3-5-2"],
            "Modern": ["4-2-3-1", "4-3-3 Holding", "3-4-3"],
            "Defensive": ["5-3-2", "4-5-1", "4-1-4-1"],
            "Attacking": ["4-4-2 Diamond", "4-3-3", "3-4-3"],
        }

        for style, formations in formations_by_style.items():
            self.formation_combo.addItem(f"=== {style} ===")
            for formation in formations:
                self.formation_combo.addItem(formation)

        self.formation_combo.currentTextChanged.connect(self.on_formation_changed)
        formation_layout.addWidget(formation_label)
        formation_layout.addWidget(self.formation_combo)
        controls_layout.addLayout(formation_layout)

        layout.addLayout(controls_layout)

        # Pitch view
        self.pitch_view = PitchView()
        layout.addWidget(self.pitch_view)

        # Bottom controls
        bottom_layout = QHBoxLayout()

        self.save_btn = QPushButton("Save Tactics")
        self.save_btn.clicked.connect(self.save_tactics)
        bottom_layout.addWidget(self.save_btn)

        self.delete_btn = QPushButton("Delete Tactics")
        self.delete_btn.clicked.connect(self.delete_tactics)
        self.delete_btn.setEnabled(False)
        bottom_layout.addWidget(self.delete_btn)

        layout.addLayout(bottom_layout)

        # Initial formation setup
        self.update_formation()

    def load_teams(self):
        self.team_combo.clear()
        teams = self.session.query(Team).all()
        for team in teams:
            self.team_combo.addItem(team.name, team.id)
        self.team_combo.currentIndexChanged.connect(self.load_squad)

    def load_squad(self):
        team_id = self.team_combo.currentData()
        if team_id is None:
            return

        self.current_team = self.session.query(Team).get(team_id)
        self.load_saved_tactics()
        self.update_formation()

    def load_saved_tactics(self):
        self.tactics_combo.clear()
        self.tactics_combo.addItem("New Tactics", None)

        if hasattr(self, "current_team"):
            tactics = (
                self.session.query(TeamTactics)
                .filter_by(team_id=self.current_team.id)
                .all()
            )
            for tactic in tactics:
                self.tactics_combo.addItem(tactic.name, tactic.id)

        self.delete_btn.setEnabled(self.tactics_combo.count() > 1)

    def load_tactics(self):
        tactics_id = self.tactics_combo.currentData()
        if tactics_id is None:
            return

        self.current_tactics = self.session.query(TeamTactics).get(tactics_id)
        if self.current_tactics:
            self.formation_combo.setCurrentText(self.current_tactics.formation)
            self.update_formation()

            # Load saved player positions and roles
            if self.current_tactics.player_positions:
                for item in self.pitch_view.scene.items():
                    if isinstance(item, PlayerItem):
                        player_id = str(item.player.id)
                        if player_id in self.current_tactics.player_positions:
                            pos = self.current_tactics.player_positions[player_id]
                            item.setPos(pos["x"], pos["y"])
                        if (
                            self.current_tactics.player_roles
                            and player_id in self.current_tactics.player_roles
                        ):
                            item.set_role(self.current_tactics.player_roles[player_id])

    def update_formation(self):
        # Clear existing players from the pitch
        for item in self.pitch_view.scene.items():
            if isinstance(item, PlayerItem):
                self.pitch_view.scene.removeItem(item)

        formation = self.formation_combo.currentText()
        if not formation in self.FORMATIONS or not hasattr(self, "current_team"):
            return

        # Get available players by position
        players = {"GK": [], "D": [], "M": [], "F": []}

        for player in self.current_team.players:
            # Categorize players by position
            if player.position.startswith("Goalkeeper"):
                players["GK"].append(player)
            elif player.position.startswith("Defender"):
                players["D"].append(player)
            elif player.position.startswith("Midfielder"):
                players["M"].append(player)
            elif player.position.startswith("Forward"):
                players["F"].append(player)

        # Place players according to formation
        positions = self.FORMATIONS[formation]

        # Place goalkeeper first (to ensure it's always placed)
        if players["GK"] and positions[3]:
            gk_pos = positions[3][0]
            self.add_player_to_pitch(players["GK"][0], gk_pos[0], gk_pos[1])

        # Place strikers
        for i, pos in enumerate(positions[0]):
            if i < len(players["F"]):
                self.add_player_to_pitch(players["F"][i], pos[0], pos[1])

        # Place midfielders
        for i, pos in enumerate(positions[1]):
            if i < len(players["M"]):
                self.add_player_to_pitch(players["M"][i], pos[0], pos[1])

        # Place defenders
        for i, pos in enumerate(positions[2]):
            if i < len(players["D"]):
                self.add_player_to_pitch(players["D"][i], pos[0], pos[1])

    def add_player_to_pitch(self, player, x, y):
        player_item = PlayerItem(player, x, y)
        self.pitch_view.scene.addItem(player_item)

        # Restore saved role if exists
        if hasattr(self, "current_tactics") and self.current_tactics:
            player_roles = self.current_tactics.player_roles or {}
            if str(player.id) in player_roles:
                player_item.set_role(player_roles[str(player.id)])

    def update_player_roles(self):
        """Collect all player roles and save them"""
        player_roles = {}
        for item in self.pitch_view.scene.items():
            if isinstance(item, PlayerItem):
                if item.current_role:
                    player_roles[str(item.player.id)] = item.current_role

        # If we have current tactics, update them
        if hasattr(self, "current_tactics") and self.current_tactics:
            self.current_tactics.player_roles = player_roles
            try:
                self.session.commit()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save roles: {str(e)}")

    def save_tactics(self):
        if not hasattr(self, "current_team"):
            return

        # Get tactics name from user
        name, ok = QInputDialog.getText(
            self,
            "Save Tactics",
            "Enter tactics name:",
            text=self.tactics_combo.currentText()
            if self.tactics_combo.currentData()
            else "New Tactics",
        )

        if not ok or not name:
            return

        # Collect player positions and roles
        player_positions = {}
        player_roles = {}
        for item in self.pitch_view.scene.items():
            if isinstance(item, PlayerItem):
                pos = item.pos()
                player_id = str(item.player.id)
                player_positions[player_id] = {"x": pos.x(), "y": pos.y()}
                if item.current_role:
                    player_roles[player_id] = item.current_role

        # Check if we're updating existing tactics or creating new ones
        tactics_id = self.tactics_combo.currentData()
        if tactics_id:
            tactics = self.session.query(TeamTactics).get(tactics_id)
            tactics.name = name
            tactics.formation = self.formation_combo.currentText()
            tactics.player_positions = player_positions
            tactics.player_roles = player_roles
        else:
            tactics = TeamTactics(
                team_id=self.current_team.id,
                name=name,
                formation=self.formation_combo.currentText(),
                player_positions=player_positions,
                player_roles=player_roles,
            )
            self.session.add(tactics)

        try:
            self.session.commit()
            self.current_tactics = tactics
            self.load_saved_tactics()
            # Select the saved tactics
            index = self.tactics_combo.findText(name)
            if index >= 0:
                self.tactics_combo.setCurrentIndex(index)
            QMessageBox.information(self, "Success", "Tactics saved successfully!")
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to save tactics: {str(e)}")

    def delete_tactics(self):
        tactics_id = self.tactics_combo.currentData()
        if not tactics_id:
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete these tactics?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            try:
                tactics = self.session.query(TeamTactics).get(tactics_id)
                self.session.delete(tactics)
                self.session.commit()
                self.load_saved_tactics()
                self.tactics_combo.setCurrentIndex(0)  # Select "New Tactics"
                QMessageBox.information(
                    self, "Success", "Tactics deleted successfully!"
                )
            except Exception as e:
                self.session.rollback()
                QMessageBox.critical(
                    self, "Error", f"Failed to delete tactics: {str(e)}"
                )

    def on_formation_changed(self, formation):
        # Skip category headers
        if formation.startswith("==="):
            # Find next non-header item
            index = self.formation_combo.currentIndex()
            self.formation_combo.setCurrentIndex(index + 1)
            return

        self.update_formation()

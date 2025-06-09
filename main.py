import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStatusBar,
    QStackedWidget,
    QComboBox,
    QDialog,
)
from PyQt5.QtCore import Qt
from ui import SquadView
from ui.tactics_view import TacticsView
from ui.match_view import MatchView
from ui.team_view import TeamView
from database import init_db, create_sample_data, get_session
from database.models import Team, TeamTactics
from ui.styles import MAIN_STYLE
from sqlalchemy.orm import joinedload

class FootballManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Football Manager QT")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize database and sample data if needed
        db_file = "football_manager.db"
        if not os.path.exists(db_file):
            init_db()
            create_sample_data()

        self.setup_ui()

    def setup_ui(self):
        # Apply stylesheet
        self.setStyleSheet(MAIN_STYLE)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Create header
        header = QLabel("Football Manager QT")
        header.setProperty("class", "header-label")
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # Create navigation panel
        nav_panel = QWidget()
        nav_layout = QHBoxLayout(nav_panel)
        nav_layout.setSpacing(10)

        # Add main menu buttons
        self.buttons = [
            ("Teams", self.show_teams, "Manage teams"),
            ("Squad", self.show_squad, "Manage your team's squad"),
            ("Tactics", self.show_tactics, "Set up team tactics and formation"),
            ("Match", self.show_match, "Play matches and view results"),
            ("Transfer", self.show_transfer, "Buy and sell players"),
            ("Statistics", self.show_statistics, "View detailed statistics"),
        ]

        for text, callback, tooltip in self.buttons:
            btn = QPushButton(text)
            btn.clicked.connect(callback)
            btn.setToolTip(tooltip)
            btn.setMinimumWidth(120)
            nav_layout.addWidget(btn)

        main_layout.addWidget(nav_panel)

        # Create stacked widget for different views
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Add views
        self.team_view = TeamView()
        self.stacked_widget.addWidget(self.team_view)
        
        self.squad_view = SquadView()
        self.stacked_widget.addWidget(self.squad_view)

        # Add tactics view
        self.tactics_view = TacticsView()
        self.stacked_widget.addWidget(self.tactics_view)

        # Add match view
        self.match_setup_widget = QWidget()
        match_setup_layout = QVBoxLayout(self.match_setup_widget)
        
        # Team selection
        teams_layout = QHBoxLayout()
        
        # Home team selection
        home_layout = QVBoxLayout()
        home_label = QLabel("Home Team:")
        self.home_team_combo = QComboBox()
        home_layout.addWidget(home_label)
        home_layout.addWidget(self.home_team_combo)
        
        vs_label = QLabel("VS")
        vs_label.setAlignment(Qt.AlignCenter)
        
        # Away team selection
        away_layout = QVBoxLayout()
        away_label = QLabel("Away Team:")
        self.away_team_combo = QComboBox()
        away_layout.addWidget(away_label)
        away_layout.addWidget(self.away_team_combo)
        
        teams_layout.addLayout(home_layout)
        teams_layout.addWidget(vs_label)
        teams_layout.addLayout(away_layout)
        match_setup_layout.addLayout(teams_layout)
        
        # Start match button
        start_match_btn = QPushButton("Start Match")
        start_match_btn.clicked.connect(self.start_match)
        match_setup_layout.addWidget(start_match_btn)
        
        self.stacked_widget.addWidget(self.match_setup_widget)
        
        # Load teams into combo boxes
        self.load_teams()

        # Add placeholder widgets for other views
        for _ in range(2):  # Transfer, Statistics
            placeholder = QWidget()
            placeholder_layout = QVBoxLayout(placeholder)
            label = QLabel("Coming Soon!")
            label.setProperty("class", "header-label")
            label.setAlignment(Qt.AlignCenter)
            placeholder_layout.addWidget(label)
            self.stacked_widget.addWidget(placeholder)

        # Add status bar
        self.statusBar().showMessage("Welcome to Football Manager QT!")
        self.statusBar().setStyleSheet(
            "QStatusBar { background-color: #34495e; color: white; padding: 5px; }"
        )

    def load_teams(self):
        """Load teams into combo boxes"""
        session = get_session()
        teams = session.query(Team).all()
        
        for team in teams:
            self.home_team_combo.addItem(team.name, team.id)
            self.away_team_combo.addItem(team.name, team.id)
            
        session.close()
        
    def start_match(self):
        """Start a match between selected teams"""
        session = get_session()
        
        # Get selected teams using newer SQLAlchemy API
        home_team_id = self.home_team_combo.currentData()
        away_team_id = self.away_team_combo.currentData()
        
        # Eagerly load teams with their players and tactics
        home_team = (
            session.query(Team)
            .filter_by(id=home_team_id)
            .options(joinedload(Team.players))
            .first()
        )
        away_team = (
            session.query(Team)
            .filter_by(id=away_team_id)
            .options(joinedload(Team.players))
            .first()
        )
        
        # Get default tactics for each team
        home_tactics = session.query(TeamTactics).filter_by(team_id=home_team_id).first()
        away_tactics = session.query(TeamTactics).filter_by(team_id=away_team_id).first()
        
        # Create copies of the data to avoid session issues
        home_team_data = {
            'id': home_team.id,
            'name': home_team.name,
            'players': [{
                'id': p.id,
                'name': p.name,
                'attack': p.attack,
                'defense': p.defense,
                'stamina': p.stamina,
                'speed': p.speed,
                'technique': p.technique
            } for p in home_team.players]
        }
        
        away_team_data = {
            'id': away_team.id,
            'name': away_team.name,
            'players': [{
                'id': p.id,
                'name': p.name,
                'attack': p.attack,
                'defense': p.defense,
                'stamina': p.stamina,
                'speed': p.speed,
                'technique': p.technique
            } for p in away_team.players]
        }
        
        home_tactics_data = {
            'formation': home_tactics.formation,
            'player_positions': home_tactics.player_positions,
            'player_roles': home_tactics.player_roles
        } if home_tactics else None
        
        away_tactics_data = {
            'formation': away_tactics.formation,
            'player_positions': away_tactics.player_positions,
            'player_roles': away_tactics.player_roles
        } if away_tactics else None
        
        session.close()
        
        # Create and show match dialog
        match_dialog = QDialog(self)
        match_dialog.setWindowTitle("Match View")
        match_dialog.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(match_dialog)
        match_view = MatchView(home_team_data, away_team_data, home_tactics_data, away_tactics_data)
        layout.addWidget(match_view)
        
        match_dialog.exec_()

    def show_teams(self):
        self.stacked_widget.setCurrentIndex(0)
        self.statusBar().showMessage("Team Management")

    def show_squad(self):
        self.stacked_widget.setCurrentIndex(1)
        self.statusBar().showMessage("Squad Management")

    def show_tactics(self):
        self.stacked_widget.setCurrentIndex(2)
        self.statusBar().showMessage("Team Tactics")

    def show_match(self):
        self.stacked_widget.setCurrentIndex(3)
        self.statusBar().showMessage("Match Center")

    def show_transfer(self):
        self.stacked_widget.setCurrentIndex(4)
        self.statusBar().showMessage("Transfer Market - Coming Soon!")

    def show_statistics(self):
        self.stacked_widget.setCurrentIndex(5)
        self.statusBar().showMessage("Statistics - Coming Soon!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FootballManager()
    window.show()
    sys.exit(app.exec_())

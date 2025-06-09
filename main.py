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
)
from PyQt5.QtCore import Qt
from ui import SquadView
from ui.tactics_view import TacticsView
from database import init_db, create_sample_data
from ui.styles import MAIN_STYLE


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
        self.squad_view = SquadView()
        self.stacked_widget.addWidget(self.squad_view)

        # Add tactics view
        self.tactics_view = TacticsView()
        self.stacked_widget.addWidget(self.tactics_view)

        # Add placeholder widgets for other views
        for _ in range(3):  # Match, Transfer, Statistics
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

    def show_squad(self):
        self.stacked_widget.setCurrentIndex(0)
        self.statusBar().showMessage("Squad Management")

    def show_tactics(self):
        self.stacked_widget.setCurrentIndex(1)
        self.statusBar().showMessage("Team Tactics")

    def show_match(self):
        self.stacked_widget.setCurrentIndex(2)
        self.statusBar().showMessage("Match Center - Coming Soon!")

    def show_transfer(self):
        self.stacked_widget.setCurrentIndex(3)
        self.statusBar().showMessage("Transfer Market - Coming Soon!")

    def show_statistics(self):
        self.stacked_widget.setCurrentIndex(4)
        self.statusBar().showMessage("Statistics - Coming Soon!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FootballManager()
    window.show()
    sys.exit(app.exec_())

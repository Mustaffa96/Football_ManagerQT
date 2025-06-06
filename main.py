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
from database import init_db, create_sample_data


class FootballManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Football Manager QT")
        self.setGeometry(100, 100, 1024, 768)

        # Initialize database and sample data if needed
        db_file = "football_manager.db"
        if not os.path.exists(db_file):
            init_db()
            create_sample_data()

        self.setup_ui()

    def setup_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create header
        header = QLabel("Football Manager QT")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(header)

        # Create button layout
        button_layout = QHBoxLayout()

        # Add main menu buttons
        self.buttons = [
            ("Squad", self.show_squad),
            ("Tactics", self.show_tactics),
            ("Match", self.show_match),
            ("Transfer", self.show_transfer),
            ("Statistics", self.show_statistics),
        ]

        for text, callback in self.buttons:
            btn = QPushButton(text)
            btn.clicked.connect(callback)
            btn.setMinimumWidth(120)
            button_layout.addWidget(btn)

        main_layout.addLayout(button_layout)

        # Create stacked widget for different views
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Add views
        self.squad_view = SquadView()
        self.stacked_widget.addWidget(self.squad_view)

        # Add placeholder widgets for other views
        for _ in range(4):  # Tactics, Match, Transfer, Statistics
            self.stacked_widget.addWidget(QWidget())

        # Add status bar
        self.statusBar().showMessage("Welcome to Football Manager QT!")

    def show_squad(self):
        self.stacked_widget.setCurrentIndex(0)
        self.statusBar().showMessage("Squad Management")

    def show_tactics(self):
        self.stacked_widget.setCurrentIndex(1)
        self.statusBar().showMessage("Team Tactics - Coming Soon!")

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

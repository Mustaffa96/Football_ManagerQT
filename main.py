import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStatusBar,
)
from PyQt5.QtCore import Qt


class FootballManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Football Manager QT")
        self.setGeometry(100, 100, 1024, 768)
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
        buttons = [
            ("Squad", self.show_squad),
            ("Tactics", self.show_tactics),
            ("Match", self.show_match),
            ("Transfer", self.show_transfer),
            ("Statistics", self.show_statistics),
        ]

        for text, callback in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(callback)
            btn.setMinimumWidth(120)
            button_layout.addWidget(btn)

        main_layout.addLayout(button_layout)

        # Add status bar
        self.statusBar().showMessage("Welcome to Football Manager QT!")

    def show_squad(self):
        self.statusBar().showMessage("Squad Management - Coming Soon!")

    def show_tactics(self):
        self.statusBar().showMessage("Team Tactics - Coming Soon!")

    def show_match(self):
        self.statusBar().showMessage("Match Center - Coming Soon!")

    def show_transfer(self):
        self.statusBar().showMessage("Transfer Market - Coming Soon!")

    def show_statistics(self):
        self.statusBar().showMessage("Statistics - Coming Soon!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FootballManager()
    window.show()
    sys.exit(app.exec_())

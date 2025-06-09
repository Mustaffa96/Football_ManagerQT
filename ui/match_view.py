from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QProgressBar, QListWidget)
from PyQt5.QtCore import Qt, QTimer
from logic.match_engine import MatchEngine

class MatchView(QWidget):
    def __init__(self, home_team, away_team, home_tactics, away_tactics):
        super().__init__()
        self.home_team = home_team
        self.away_team = away_team
        self.match_engine = MatchEngine(home_team, away_team, home_tactics, away_tactics)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_match)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Score and time display
        score_layout = QHBoxLayout()
        self.home_score_label = QLabel("0")
        self.away_score_label = QLabel("0")
        self.time_label = QLabel("0'")
        
        score_layout.addWidget(QLabel(self.home_team.name))
        score_layout.addWidget(self.home_score_label)
        score_layout.addWidget(QLabel("-"))
        score_layout.addWidget(self.away_score_label)
        score_layout.addWidget(QLabel(self.away_team.name))
        score_layout.addWidget(self.time_label)
        
        layout.addLayout(score_layout)
        
        # Match stats
        stats_layout = QHBoxLayout()
        
        # Possession bar
        self.possession_bar = QProgressBar()
        self.possession_bar.setTextVisible(True)
        self.possession_bar.setRange(0, 100)
        self.possession_bar.setValue(50)
        stats_layout.addWidget(QLabel("Possession"))
        stats_layout.addWidget(self.possession_bar)
        
        layout.addLayout(stats_layout)
        
        # Match events list
        self.events_list = QListWidget()
        layout.addWidget(self.events_list)
        
        # Control buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Match")
        self.start_button.clicked.connect(self.start_match)
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_match)
        self.pause_button.setEnabled(False)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def start_match(self):
        self.timer.start(1000)  # Update every second
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        
    def pause_match(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        
    def update_match(self):
        event = self.match_engine.simulate_minute()
        
        # Update time
        self.time_label.setText(f"{self.match_engine.current_minute}'")
        
        # Update score
        self.home_score_label.setText(str(self.match_engine.home_score))
        self.away_score_label.setText(str(self.match_engine.away_score))
        
        # Update possession
        home_possession = self.match_engine.possession["home"]
        self.possession_bar.setValue(int(home_possession))
        self.possession_bar.setFormat(f"{home_possession:.1f}% - {100-home_possession:.1f}%")
        
        # Add event to list if one occurred
        if event:
            if event["event_type"] == "goal":
                text = f"{event['minute']}' GOAL! {event['details']['score']}"
            else:
                text = f"{event['minute']}' Shot {event['details']['outcome']}"
            self.events_list.insertItem(0, text)
        
        # Check if match is over
        if self.match_engine.current_minute >= 90:
            self.timer.stop()
            self.events_list.insertItem(0, "Match finished!")
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(False)

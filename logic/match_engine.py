import random
from datetime import datetime
from typing import List, Dict, Tuple

class MatchEngine:
    def __init__(self, home_team, away_team, home_tactics, away_tactics):
        self.home_team = home_team
        self.away_team = away_team
        self.home_tactics = home_tactics
        self.away_tactics = away_tactics
        self.events = []
        self.home_score = 0
        self.away_score = 0
        self.current_minute = 0
        self.possession = {"home": 50, "away": 50}
        self.shots = {"home": 0, "away": 0}
        
    def calculate_team_strength(self, team, tactics) -> float:
        """Calculate overall team strength based on players and tactics"""
        total_strength = 0
        players = team['players']
        
        for player in players:
            # Basic strength calculation
            player_strength = (
                player['attack'] + 
                player['defense'] + 
                player['stamina'] + 
                player['speed'] + 
                player['technique']
            ) / 5
            total_strength += player_strength
            
        # Average team strength
        return total_strength / len(players) if players else 0
    
    def simulate_minute(self) -> Dict:
        """Simulate one minute of the match"""
        self.current_minute += 1
        
        # Calculate team strengths
        home_strength = self.calculate_team_strength(self.home_team, self.home_tactics)
        away_strength = self.calculate_team_strength(self.away_team, self.away_tactics)
        
        # Determine possession
        total_strength = home_strength + away_strength
        self.possession["home"] = (home_strength / total_strength) * 100
        self.possession["away"] = 100 - self.possession["home"]
        
        # Chance of event occurring
        if random.random() < 0.1:  # 10% chance of event per minute
            if random.random() < self.possession["home"] / 100:
                attacking_team = self.home_team
                defending_team = self.away_team
                is_home = True
            else:
                attacking_team = self.away_team
                defending_team = self.home_team
                is_home = False
                
            # Simulate shot
            self.shots["home" if is_home else "away"] += 1
            shot_quality = random.random() * (home_strength if is_home else away_strength)
            defense_quality = random.random() * (away_strength if is_home else home_strength)
            
            if shot_quality > defense_quality:
                # Goal scored!
                if is_home:
                    self.home_score += 1
                else:
                    self.away_score += 1
                    
                # Select random scorer from attacking team
                scorer = random.choice(attacking_team['players'])
                
                event = {
                    "minute": self.current_minute,
                    "event_type": "goal",
                    "player_id": scorer['id'],
                    "team_id": attacking_team['id'],
                    "player_name": scorer['name'],
                    "team_name": attacking_team['name'],
                    "details": {
                        "score": f"{self.home_score}-{self.away_score}"
                    }
                }
            else:
                # Shot saved/missed
                shooter = random.choice(attacking_team['players'])
                event = {
                    "minute": self.current_minute,
                    "event_type": "shot",
                    "player_id": shooter['id'],
                    "team_id": attacking_team['id'],
                    "player_name": shooter['name'],
                    "team_name": attacking_team['name'],
                    "details": {
                        "outcome": "saved" if shot_quality > defense_quality * 0.5 else "missed"
                    }
                }
            
            self.events.append(event)
            return event
            
        return None
    
    def simulate_match(self) -> Tuple[int, int, List[Dict]]:
        """Simulate entire 90 minute match"""
        while self.current_minute < 90:
            self.simulate_minute()
            
        return (
            self.home_score,
            self.away_score,
            self.events,
            {
                "possession": self.possession,
                "shots": self.shots
            }
        )

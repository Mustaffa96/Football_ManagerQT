from datetime import date, timedelta
from .models import init_db, get_session, Team, Player

def create_sample_data():
    session = get_session()
    
    # Create teams
    teams_data = [
        {
            "name": "Manchester United",
            "country": "England",
            "league": "Premier League",
            "budget": 200000000.0
        },
        {
            "name": "Real Madrid",
            "country": "Spain",
            "league": "La Liga",
            "budget": 250000000.0
        },
        {
            "name": "Bayern Munich",
            "country": "Germany",
            "league": "Bundesliga",
            "budget": 180000000.0
        }
    ]
    
    teams = []
    for team_data in teams_data:
        team = Team(**team_data)
        session.add(team)
        teams.append(team)
    
    # Commit teams first to get their IDs
    session.commit()
    
    # Create players for each team
    players_data = {
        "Manchester United": [
            {
                "name": "Marcus Rashford",
                "age": 25,
                "position": "Forward",
                "nationality": "England",
                "attack": 85,
                "defense": 45,
                "stamina": 80,
                "speed": 90,
                "technique": 82,
                "wage": 200000.0,
                "value": 85000000.0,
                "contract_end": date.today() + timedelta(days=1095)  # 3 years
            },
            {
                "name": "Bruno Fernandes",
                "age": 28,
                "position": "Midfielder",
                "nationality": "Portugal",
                "attack": 82,
                "defense": 65,
                "stamina": 85,
                "speed": 75,
                "technique": 88,
                "wage": 180000.0,
                "value": 75000000.0,
                "contract_end": date.today() + timedelta(days=1460)  # 4 years
            }
        ],
        "Real Madrid": [
            {
                "name": "Vinicius Jr",
                "age": 23,
                "position": "Forward",
                "nationality": "Brazil",
                "attack": 88,
                "defense": 40,
                "stamina": 85,
                "speed": 95,
                "technique": 87,
                "wage": 220000.0,
                "value": 120000000.0,
                "contract_end": date.today() + timedelta(days=1825)  # 5 years
            },
            {
                "name": "Toni Kroos",
                "age": 33,
                "position": "Midfielder",
                "nationality": "Germany",
                "attack": 78,
                "defense": 72,
                "stamina": 80,
                "speed": 65,
                "technique": 90,
                "wage": 200000.0,
                "value": 25000000.0,
                "contract_end": date.today() + timedelta(days=365)  # 1 year
            }
        ],
        "Bayern Munich": [
            {
                "name": "Harry Kane",
                "age": 30,
                "position": "Forward",
                "nationality": "England",
                "attack": 90,
                "defense": 45,
                "stamina": 82,
                "speed": 75,
                "technique": 85,
                "wage": 250000.0,
                "value": 90000000.0,
                "contract_end": date.today() + timedelta(days=1460)  # 4 years
            },
            {
                "name": "Joshua Kimmich",
                "age": 28,
                "position": "Midfielder",
                "nationality": "Germany",
                "attack": 80,
                "defense": 85,
                "stamina": 88,
                "speed": 78,
                "technique": 86,
                "wage": 180000.0,
                "value": 70000000.0,
                "contract_end": date.today() + timedelta(days=1095)  # 3 years
            }
        ]
    }
    
    for team in teams:
        for player_data in players_data[team.name]:
            player = Player(**player_data)
            player.team = team
            session.add(player)
    
    session.commit()
    session.close()

if __name__ == "__main__":
    # Initialize database
    init_db()
    # Create sample data
    create_sample_data()
    print("Sample data created successfully!")

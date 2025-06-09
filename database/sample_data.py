from datetime import date, timedelta
from .models import init_db, get_session, Team, Player, TeamTactics


def create_sample_data():
    session = get_session()

    # Create teams
    teams_data = [
        {
            "name": "Manchester United",
            "country": "England",
            "league": "Premier League",
            "budget": 200000000.0,
        },
        {
            "name": "Real Madrid",
            "country": "Spain",
            "league": "La Liga",
            "budget": 250000000.0,
        },
        {
            "name": "Bayern Munich",
            "country": "Germany",
            "league": "Bundesliga",
            "budget": 180000000.0,
        },
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
                "age": 26,
                "position": "Forward",
                "nationality": "England",
                "attack": 85,
                "defense": 45,
                "stamina": 80,
                "speed": 90,
                "technique": 82,
                "wage": 250000.0,
                "value": 85000000.0,
                "contract_end": date.today() + timedelta(days=1825),  # 5 years
            },
            {
                "name": "Bruno Fernandes",
                "age": 29,
                "position": "Midfielder",
                "nationality": "Portugal",
                "attack": 82,
                "defense": 65,
                "stamina": 85,
                "speed": 75,
                "technique": 88,
                "wage": 250000.0,
                "value": 75000000.0,
                "contract_end": date.today() + timedelta(days=1460),  # 4 years
            },
            {
                "name": "Rasmus Hojlund",
                "age": 21,
                "position": "Forward",
                "nationality": "Denmark",
                "attack": 82,
                "defense": 35,
                "stamina": 80,
                "speed": 85,
                "technique": 80,
                "wage": 150000.0,
                "value": 65000000.0,
                "contract_end": date.today() + timedelta(days=1825),  # 5 years
            },
            {
                "name": "Casemiro",
                "age": 31,
                "position": "Midfielder",
                "nationality": "Brazil",
                "attack": 75,
                "defense": 88,
                "stamina": 85,
                "speed": 70,
                "technique": 85,
                "wage": 300000.0,
                "value": 45000000.0,
                "contract_end": date.today() + timedelta(days=730),  # 2 years
            },
            {
                "name": "Andre Onana",
                "age": 27,
                "position": "Goalkeeper",
                "nationality": "Cameroon",
                "attack": 15,
                "defense": 85,
                "stamina": 75,
                "speed": 65,
                "technique": 80,
                "wage": 200000.0,
                "value": 45000000.0,
                "contract_end": date.today() + timedelta(days=1825),  # 5 years
            },
            {
                "name": "Luke Shaw",
                "age": 28,
                "position": "Defender",
                "nationality": "England",
                "attack": 75,
                "defense": 83,
                "stamina": 85,
                "speed": 82,
                "technique": 80,
                "wage": 200000.0,
                "value": 40000000.0,
                "contract_end": date.today() + timedelta(days=730),  # 2 years
            },
            {
                "name": "Raphael Varane",
                "age": 30,
                "position": "Defender",
                "nationality": "France",
                "attack": 45,
                "defense": 86,
                "stamina": 82,
                "speed": 78,
                "technique": 75,
                "wage": 250000.0,
                "value": 35000000.0,
                "contract_end": date.today() + timedelta(days=730),  # 2 years
            },
            {
                "name": "Lisandro Martinez",
                "age": 25,
                "position": "Defender",
                "nationality": "Argentina",
                "attack": 55,
                "defense": 85,
                "stamina": 83,
                "speed": 75,
                "technique": 78,
                "wage": 180000.0,
                "value": 50000000.0,
                "contract_end": date.today() + timedelta(days=1460),  # 4 years
            },
            {
                "name": "Aaron Wan-Bissaka",
                "age": 26,
                "position": "Defender",
                "nationality": "England",
                "attack": 65,
                "defense": 82,
                "stamina": 85,
                "speed": 85,
                "technique": 75,
                "wage": 120000.0,
                "value": 25000000.0,
                "contract_end": date.today() + timedelta(days=730),  # 2 years
            },
            {
                "name": "Mason Mount",
                "age": 24,
                "position": "Midfielder",
                "nationality": "England",
                "attack": 78,
                "defense": 65,
                "stamina": 82,
                "speed": 75,
                "technique": 82,
                "wage": 200000.0,
                "value": 55000000.0,
                "contract_end": date.today() + timedelta(days=1825),  # 5 years
            },
            {
                "name": "Antony",
                "age": 23,
                "position": "Forward",
                "nationality": "Brazil",
                "attack": 80,
                "defense": 45,
                "stamina": 78,
                "speed": 85,
                "technique": 85,
                "wage": 200000.0,
                "value": 50000000.0,
                "contract_end": date.today() + timedelta(days=1825),  # 5 years
            },
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
                "contract_end": date.today() + timedelta(days=1825),  # 5 years
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
                "contract_end": date.today() + timedelta(days=365),  # 1 year
            },
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
                "contract_end": date.today() + timedelta(days=1460),  # 4 years
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
                "contract_end": date.today() + timedelta(days=1095),  # 3 years
            },
        ],
    }

    for team in teams:
        for player_data in players_data[team.name]:
            player = Player(**player_data)
            player.team = team
            session.add(player)

    session.commit()

    # Create tactics for Manchester United
    man_utd = session.query(Team).filter_by(name="Manchester United").first()
    if man_utd:
        # 4-2-3-1 Formation (Default)
        tactics_4231 = TeamTactics(
            team=man_utd,
            name="Default 4-2-3-1",
            formation="4-2-3-1",
            player_positions={
                # Positions are stored as x, y coordinates on the pitch
                str(man_utd.players[4].id): {"x": 80, "y": 250},  # Onana (GK)
                str(man_utd.players[5].id): {"x": 200, "y": 100},  # Shaw (LB)
                # Other positions would be filled by players not in sample data
            },
            player_roles={
                str(man_utd.players[4].id): "Sweeper Keeper",  # Onana
                str(man_utd.players[5].id): "Wing-Back",  # Shaw
                str(man_utd.players[3].id): "Defensive Midfielder",  # Casemiro
                str(man_utd.players[1].id): "Attacking Midfielder",  # Bruno
                str(man_utd.players[0].id): "Inside Forward",  # Rashford
                str(man_utd.players[2].id): "Advanced Forward",  # Hojlund
            },
        )

        # 4-3-3 Formation (Attacking)
        tactics_433 = TeamTactics(
            team=man_utd,
            name="Attacking 4-3-3",
            formation="4-3-3",
            player_positions={
                str(man_utd.players[4].id): {"x": 80, "y": 250},  # Onana (GK)
                str(man_utd.players[5].id): {"x": 200, "y": 100},  # Shaw (LB)
                # Other positions would be filled by players not in sample data
            },
            player_roles={
                str(man_utd.players[4].id): "Sweeper Keeper",  # Onana
                str(man_utd.players[5].id): "Full-Back",  # Shaw
                str(man_utd.players[3].id): "Deep-Lying Playmaker",  # Casemiro
                str(man_utd.players[1].id): "Box-to-Box",  # Bruno
                str(man_utd.players[0].id): "Inside Forward",  # Rashford
                str(man_utd.players[2].id): "Complete Forward",  # Hojlund
            },
        )

        # 4-4-2 Diamond (Alternative)
        tactics_442_diamond = TeamTactics(
            team=man_utd,
            name="Diamond 4-4-2",
            formation="4-4-2 Diamond",
            player_positions={
                str(man_utd.players[4].id): {"x": 80, "y": 250},  # Onana (GK)
                str(man_utd.players[5].id): {"x": 200, "y": 100},  # Shaw (LB)
                # Other positions would be filled by players not in sample data
            },
            player_roles={
                str(man_utd.players[4].id): "Goalkeeper",  # Onana
                str(man_utd.players[5].id): "Full-Back",  # Shaw
                str(man_utd.players[3].id): "Defensive Midfielder",  # Casemiro
                str(man_utd.players[1].id): "Attacking Midfielder",  # Bruno
                str(man_utd.players[0].id): "Inside Forward",  # Rashford
                str(man_utd.players[2].id): "Advanced Forward",  # Hojlund
            },
        )

        session.add_all([tactics_4231, tactics_433, tactics_442_diamond])

    session.commit()
    session.close()


if __name__ == "__main__":
    # Initialize database
    init_db()
    # Create sample data
    create_sample_data()
    print("Sample data created successfully!")

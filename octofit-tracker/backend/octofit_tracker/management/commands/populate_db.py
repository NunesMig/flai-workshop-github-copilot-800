from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        self.stdout.write(self.style.WARNING('Clearing existing data...'))
        
        # Clear existing collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        self.stdout.write(self.style.SUCCESS('Creating unique index on email field...'))
        
        # Create unique index on email field
        db.users.create_index([("email", 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('Populating teams...'))
        
        # Create teams
        teams = [
            {
                '_id': 'team_marvel',
                'name': 'Team Marvel',
                'description': 'Earth\'s Mightiest Heroes',
                'created_at': datetime.now().isoformat(),
                'members': []
            },
            {
                '_id': 'team_dc',
                'name': 'Team DC',
                'description': 'Justice League United',
                'created_at': datetime.now().isoformat(),
                'members': []
            }
        ]
        db.teams.insert_many(teams)

        self.stdout.write(self.style.SUCCESS('Populating users...'))
        
        # Create Marvel superheroes
        marvel_users = [
            {
                'email': 'tony.stark@avengers.com',
                'username': 'ironman',
                'full_name': 'Tony Stark',
                'team_id': 'team_marvel',
                'role': 'hero',
                'created_at': datetime.now().isoformat(),
                'total_points': 2850
            },
            {
                'email': 'steve.rogers@avengers.com',
                'username': 'captainamerica',
                'full_name': 'Steve Rogers',
                'team_id': 'team_marvel',
                'role': 'hero',
                'created_at': datetime.now().isoformat(),
                'total_points': 3100
            },
            {
                'email': 'thor.odinson@avengers.com',
                'username': 'thor',
                'full_name': 'Thor Odinson',
                'team_id': 'team_marvel',
                'role': 'hero',
                'created_at': datetime.now().isoformat(),
                'total_points': 2950
            },
            {
                'email': 'natasha.romanoff@avengers.com',
                'username': 'blackwidow',
                'full_name': 'Natasha Romanoff',
                'team_id': 'team_marvel',
                'role': 'hero',
                'created_at': datetime.now().isoformat(),
                'total_points': 2700
            },
            {
                'email': 'bruce.banner@avengers.com',
                'username': 'hulk',
                'full_name': 'Bruce Banner',
                'team_id': 'team_marvel',
                'role': 'hero',
                'created_at': datetime.now().isoformat(),
                'total_points': 3200
            }
        ]

        # Create DC superheroes
        dc_users = [
            {
                'email': 'clark.kent@justiceleague.com',
                'username': 'superman',
                'full_name': 'Clark Kent',
                'team_id': 'team_dc',
                'role': 'hero',
                'created_at': datetime.now().isoformat(),
                'total_points': 3400
            },
            {
                'email': 'bruce.wayne@justiceleague.com',
                'username': 'batman',
                'full_name': 'Bruce Wayne',
                'team_id': 'team_dc',
                'role': 'hero',
                'created_at': datetime.now().isoformat(),
                'total_points': 3150
            },
            {
                'email': 'diana.prince@justiceleague.com',
                'username': 'wonderwoman',
                'full_name': 'Diana Prince',
                'team_id': 'team_dc',
                'role': 'hero',
                'created_at': datetime.now().isoformat(),
                'total_points': 2980
            },
            {
                'email': 'barry.allen@justiceleague.com',
                'username': 'flash',
                'full_name': 'Barry Allen',
                'team_id': 'team_dc',
                'role': 'hero',
                'created_at': datetime.now().isoformat(),
                'total_points': 2850
            },
            {
                'email': 'arthur.curry@justiceleague.com',
                'username': 'aquaman',
                'full_name': 'Arthur Curry',
                'team_id': 'team_dc',
                'role': 'hero',
                'created_at': datetime.now().isoformat(),
                'total_points': 2600
            }
        ]

        all_users = marvel_users + dc_users
        db.users.insert_many(all_users)

        self.stdout.write(self.style.SUCCESS('Populating workouts...'))
        
        # Create workout suggestions
        workouts = [
            {
                'name': 'Super Soldier Strength',
                'description': 'Build strength like Captain America',
                'category': 'strength',
                'difficulty': 'intermediate',
                'duration_minutes': 45,
                'exercises': [
                    {'name': 'Push-ups', 'sets': 4, 'reps': 20},
                    {'name': 'Pull-ups', 'sets': 4, 'reps': 12},
                    {'name': 'Squats', 'sets': 4, 'reps': 25}
                ],
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Speed Force Training',
                'description': 'Cardio workout inspired by The Flash',
                'category': 'cardio',
                'difficulty': 'advanced',
                'duration_minutes': 30,
                'exercises': [
                    {'name': 'Sprint intervals', 'duration': '10 minutes'},
                    {'name': 'High knees', 'sets': 5, 'duration': '1 minute'},
                    {'name': 'Burpees', 'sets': 4, 'reps': 15}
                ],
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Asgardian Warrior',
                'description': 'Thor\'s legendary battle training',
                'category': 'strength',
                'difficulty': 'advanced',
                'duration_minutes': 60,
                'exercises': [
                    {'name': 'Deadlifts', 'sets': 5, 'reps': 8},
                    {'name': 'Battle ropes', 'sets': 4, 'duration': '45 seconds'},
                    {'name': 'Sledgehammer swings', 'sets': 4, 'reps': 20}
                ],
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Bat-Agility Training',
                'description': 'Batman\'s stealth and agility workout',
                'category': 'flexibility',
                'difficulty': 'intermediate',
                'duration_minutes': 40,
                'exercises': [
                    {'name': 'Yoga flow', 'duration': '15 minutes'},
                    {'name': 'Dynamic stretching', 'duration': '10 minutes'},
                    {'name': 'Parkour basics', 'duration': '15 minutes'}
                ],
                'created_at': datetime.now().isoformat()
            },
            {
                'name': 'Amazon Warrior',
                'description': 'Wonder Woman\'s combat conditioning',
                'category': 'strength',
                'difficulty': 'intermediate',
                'duration_minutes': 50,
                'exercises': [
                    {'name': 'Kettlebell swings', 'sets': 4, 'reps': 20},
                    {'name': 'Box jumps', 'sets': 4, 'reps': 15},
                    {'name': 'Medicine ball slams', 'sets': 4, 'reps': 15}
                ],
                'created_at': datetime.now().isoformat()
            }
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('Populating activities...'))
        
        # Create activities for users
        activities = []
        activity_types = ['running', 'cycling', 'swimming', 'weightlifting', 'yoga', 'boxing']
        
        for user in all_users:
            for i in range(random.randint(5, 10)):
                days_ago = random.randint(1, 30)
                activity_date = datetime.now() - timedelta(days=days_ago)
                
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 90)
                calories = duration * random.randint(8, 12)
                points = int(calories / 10)
                
                activity = {
                    'user_email': user['email'],
                    'username': user['username'],
                    'team_id': user['team_id'],
                    'activity_type': activity_type,
                    'duration_minutes': duration,
                    'calories_burned': calories,
                    'points_earned': points,
                    'date': activity_date.isoformat(),
                    'notes': f'{activity_type.capitalize()} session'
                }
                activities.append(activity)
        
        db.activities.insert_many(activities)

        self.stdout.write(self.style.SUCCESS('Populating leaderboard...'))
        
        # Create leaderboard entries
        leaderboard_entries = []
        for user in all_users:
            user_activities = [a for a in activities if a['user_email'] == user['email']]
            total_points = sum(a['points_earned'] for a in user_activities)
            total_calories = sum(a['calories_burned'] for a in user_activities)
            total_duration = sum(a['duration_minutes'] for a in user_activities)
            
            entry = {
                'user_email': user['email'],
                'username': user['username'],
                'full_name': user['full_name'],
                'team_id': user['team_id'],
                'total_points': total_points,
                'total_calories': total_calories,
                'total_duration_minutes': total_duration,
                'activities_count': len(user_activities),
                'last_updated': datetime.now().isoformat()
            }
            leaderboard_entries.append(entry)
        
        # Sort by total points descending
        leaderboard_entries.sort(key=lambda x: x['total_points'], reverse=True)
        
        # Add rank
        for rank, entry in enumerate(leaderboard_entries, start=1):
            entry['rank'] = rank
        
        db.leaderboard.insert_many(leaderboard_entries)

        self.stdout.write(self.style.SUCCESS('✅ Database populated successfully!'))
        self.stdout.write(self.style.SUCCESS(f'  - Teams: {len(teams)}'))
        self.stdout.write(self.style.SUCCESS(f'  - Users: {len(all_users)}'))
        self.stdout.write(self.style.SUCCESS(f'  - Workouts: {len(workouts)}'))
        self.stdout.write(self.style.SUCCESS(f'  - Activities: {len(activities)}'))
        self.stdout.write(self.style.SUCCESS(f'  - Leaderboard entries: {len(leaderboard_entries)}'))
        
        client.close()

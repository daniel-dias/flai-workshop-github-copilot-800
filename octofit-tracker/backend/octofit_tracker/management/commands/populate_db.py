from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing data...')
        
        # Delete existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data cleared'))
        
        # Create teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            members=[],
            total_points=0
        )
        team_dc = Team.objects.create(
            name='Team DC',
            members=[],
            total_points=0
        )
        self.stdout.write(self.style.SUCCESS('Teams created'))
        
        # Create Marvel users
        self.stdout.write('Creating Marvel superheroes...')
        marvel_heroes = [
            {'name': 'Iron Man', 'email': 'tony.stark@marvel.com'},
            {'name': 'Captain America', 'email': 'steve.rogers@marvel.com'},
            {'name': 'Thor', 'email': 'thor.odinson@marvel.com'},
            {'name': 'Black Widow', 'email': 'natasha.romanoff@marvel.com'},
            {'name': 'Hulk', 'email': 'bruce.banner@marvel.com'},
            {'name': 'Spider-Man', 'email': 'peter.parker@marvel.com'},
        ]
        
        marvel_users = []
        for hero in marvel_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team='Team Marvel'
            )
            marvel_users.append(user)
        
        # Create DC users
        self.stdout.write('Creating DC superheroes...')
        dc_heroes = [
            {'name': 'Batman', 'email': 'bruce.wayne@dc.com'},
            {'name': 'Superman', 'email': 'clark.kent@dc.com'},
            {'name': 'Wonder Woman', 'email': 'diana.prince@dc.com'},
            {'name': 'The Flash', 'email': 'barry.allen@dc.com'},
            {'name': 'Aquaman', 'email': 'arthur.curry@dc.com'},
            {'name': 'Green Lantern', 'email': 'hal.jordan@dc.com'},
        ]
        
        dc_users = []
        for hero in dc_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team='Team DC'
            )
            dc_users.append(user)
        
        self.stdout.write(self.style.SUCCESS('Users created'))
        
        # Update team members
        team_marvel.members = [user.email for user in marvel_users]
        team_marvel.save()
        team_dc.members = [user.email for user in dc_users]
        team_dc.save()
        
        # Create activities
        self.stdout.write('Creating activities...')
        activity_types = [
            {'type': 'Running', 'cal_per_min': 10},
            {'type': 'Swimming', 'cal_per_min': 12},
            {'type': 'Cycling', 'cal_per_min': 8},
            {'type': 'Weightlifting', 'cal_per_min': 6},
            {'type': 'Yoga', 'cal_per_min': 4},
            {'type': 'Boxing', 'cal_per_min': 11},
        ]
        
        all_users = marvel_users + dc_users
        for user in all_users:
            # Create 5-10 activities per user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 90)
                calories = duration * activity_type['cal_per_min']
                days_ago = random.randint(0, 30)
                activity_date = datetime.now() - timedelta(days=days_ago)
                
                Activity.objects.create(
                    user_email=user.email,
                    activity_type=activity_type['type'],
                    duration=duration,
                    calories=calories,
                    date=activity_date
                )
        
        self.stdout.write(self.style.SUCCESS('Activities created'))
        
        # Create leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        for user in all_users:
            user_activities = Activity.objects.filter(user_email=user.email)
            total_calories = sum(activity.calories for activity in user_activities)
            total_activities = user_activities.count()
            
            Leaderboard.objects.create(
                user_email=user.email,
                user_name=user.name,
                team=user.team,
                total_calories=total_calories,
                total_activities=total_activities,
                rank=0  # Will be updated after all entries are created
            )
        
        # Update ranks based on total calories
        leaderboard_entries = Leaderboard.objects.all().order_by('-total_calories')
        for idx, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = idx
            entry.save()
        
        self.stdout.write(self.style.SUCCESS('Leaderboard entries created'))
        
        # Create workouts
        self.stdout.write('Creating workouts...')
        workouts = [
            {
                'name': 'Super Soldier Cardio',
                'category': 'Cardio',
                'description': 'High-intensity cardio workout inspired by Captain America training',
                'difficulty': 'Hard',
                'duration': 45,
                'calories_per_session': 450
            },
            {
                'name': 'Asgardian Strength Training',
                'category': 'Strength',
                'description': 'Heavy weightlifting routine worthy of the God of Thunder',
                'difficulty': 'Hard',
                'duration': 60,
                'calories_per_session': 360
            },
            {
                'name': 'Web-Slinger Flexibility',
                'category': 'Flexibility',
                'description': 'Dynamic stretching and mobility exercises',
                'difficulty': 'Medium',
                'duration': 30,
                'calories_per_session': 120
            },
            {
                'name': 'Bat-Training Combat',
                'category': 'Martial Arts',
                'description': 'Intensive combat training and boxing drills',
                'difficulty': 'Hard',
                'duration': 50,
                'calories_per_session': 550
            },
            {
                'name': 'Kryptonian Power Workout',
                'category': 'Full Body',
                'description': 'Complete body workout combining strength and cardio',
                'difficulty': 'Hard',
                'duration': 55,
                'calories_per_session': 500
            },
            {
                'name': 'Amazonian Warrior Training',
                'category': 'Strength',
                'description': 'Functional strength training with warrior spirit',
                'difficulty': 'Medium',
                'duration': 40,
                'calories_per_session': 320
            },
            {
                'name': 'Speed Force Sprint',
                'category': 'Cardio',
                'description': 'Sprint intervals and speed training',
                'difficulty': 'Hard',
                'duration': 35,
                'calories_per_session': 400
            },
            {
                'name': 'Atlantean Swimming',
                'category': 'Swimming',
                'description': 'Aquatic endurance and strength training',
                'difficulty': 'Medium',
                'duration': 45,
                'calories_per_session': 540
            },
            {
                'name': 'Willpower Yoga',
                'category': 'Yoga',
                'description': 'Mind and body alignment through yoga practice',
                'difficulty': 'Easy',
                'duration': 30,
                'calories_per_session': 120
            },
            {
                'name': 'Arc Reactor Core',
                'category': 'Core',
                'description': 'Core strengthening exercises for stability',
                'difficulty': 'Medium',
                'duration': 25,
                'calories_per_session': 150
            },
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data)
        
        self.stdout.write(self.style.SUCCESS('Workouts created'))
        
        # Calculate and update team points
        marvel_calories = sum(
            entry.total_calories 
            for entry in Leaderboard.objects.filter(team='Team Marvel')
        )
        dc_calories = sum(
            entry.total_calories 
            for entry in Leaderboard.objects.filter(team='Team DC')
        )
        
        team_marvel.total_points = marvel_calories
        team_marvel.save()
        team_dc.total_points = dc_calories
        team_dc.save()
        
        # Display summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
        self.stdout.write('='*50)
        self.stdout.write(f'Users created: {User.objects.count()}')
        self.stdout.write(f'Teams created: {Team.objects.count()}')
        self.stdout.write(f'Activities created: {Activity.objects.count()}')
        self.stdout.write(f'Leaderboard entries: {Leaderboard.objects.count()}')
        self.stdout.write(f'Workouts created: {Workout.objects.count()}')
        self.stdout.write('='*50)
        self.stdout.write(f'Team Marvel total points: {team_marvel.total_points}')
        self.stdout.write(f'Team DC total points: {team_dc.total_points}')
        self.stdout.write('='*50)

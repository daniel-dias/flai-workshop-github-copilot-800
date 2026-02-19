from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserModelTest(TestCase):
    def setUp(self):
        User.objects.create(name="Test User", email="test@example.com", team="Team A")
    
    def test_user_creation(self):
        user = User.objects.get(email="test@example.com")
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.team, "Team A")


class TeamModelTest(TestCase):
    def setUp(self):
        Team.objects.create(name="Team A", members=["user1@example.com"], total_points=100)
    
    def test_team_creation(self):
        team = Team.objects.get(name="Team A")
        self.assertEqual(team.total_points, 100)
        self.assertIn("user1@example.com", team.members)


class ActivityModelTest(TestCase):
    def setUp(self):
        Activity.objects.create(
            user_email="test@example.com",
            activity_type="Running",
            duration=30,
            calories=250,
            date=datetime.now()
        )
    
    def test_activity_creation(self):
        activity = Activity.objects.get(user_email="test@example.com")
        self.assertEqual(activity.activity_type, "Running")
        self.assertEqual(activity.duration, 30)
        self.assertEqual(activity.calories, 250)


class WorkoutModelTest(TestCase):
    def setUp(self):
        Workout.objects.create(
            name="Morning Jog",
            category="Cardio",
            description="A refreshing morning jog",
            difficulty="Beginner",
            duration=20,
            calories_per_session=150
        )
    
    def test_workout_creation(self):
        workout = Workout.objects.get(name="Morning Jog")
        self.assertEqual(workout.category, "Cardio")
        self.assertEqual(workout.difficulty, "Beginner")


class UserAPITest(APITestCase):
    def test_user_list(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_user(self):
        data = {"name": "New User", "email": "new@example.com", "team": "Team B"}
        response = self.client.post('/api/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TeamAPITest(APITestCase):
    def test_team_list(self):
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_team(self):
        data = {"name": "New Team", "members": [], "total_points": 0}
        response = self.client.post('/api/teams/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ActivityAPITest(APITestCase):
    def test_activity_list(self):
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LeaderboardAPITest(APITestCase):
    def test_leaderboard_list(self):
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITest(APITestCase):
    def test_workout_list(self):
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

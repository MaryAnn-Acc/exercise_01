from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Team, Activity, Workout, Leaderboard

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_user_list(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TeamTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser2', password='testpass')
        self.team = Team.objects.create(name='Test Team')
        self.team.members.add(self.user)

    def test_team_list(self):
        response = self.client.get('/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ActivityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser3', password='testpass')
        self.activity = Activity.objects.create(user=self.user, activity_type='run', duration=30, calories_burned=200, date='2024-01-01')

    def test_activity_list(self):
        response = self.client.get('/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class WorkoutTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser4', password='testpass')
        self.workout = Workout.objects.create(user=self.user, name='Morning Workout', description='Pushups', date='2024-01-01')

    def test_workout_list(self):
        response = self.client.get('/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class LeaderboardTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name='Leaderboard Team')
        self.leaderboard = Leaderboard.objects.create(team=self.team, score=100)

    def test_leaderboard_list(self):
        response = self.client.get('/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

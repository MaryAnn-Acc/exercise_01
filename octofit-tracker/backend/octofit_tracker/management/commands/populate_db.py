from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import settings

from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Clear existing data
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared users.'))

        # Teams
        Team = self.get_or_create_collection('teams')
        Team.delete_many({})
        marvel_team = {'name': 'Marvel', 'members': []}
        dc_team = {'name': 'DC', 'members': []}
        marvel_id = Team.insert_one(marvel_team).inserted_id
        dc_id = Team.insert_one(dc_team).inserted_id
        self.stdout.write(self.style.SUCCESS('Created teams.'))

        # Users
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': marvel_id},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'team': marvel_id},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': dc_id},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': dc_id},
        ]
        for user in users:
            User.objects.create_user(username=user['username'], email=user['email'], password='password')
        self.stdout.write(self.style.SUCCESS('Created users.'))

        # Activities
        Activity = self.get_or_create_collection('activities')
        Activity.delete_many({})
        Activity.insert_many([
            {'user': 'ironman', 'activity': 'run', 'distance': 5},
            {'user': 'spiderman', 'activity': 'cycle', 'distance': 10},
            {'user': 'batman', 'activity': 'swim', 'distance': 2},
            {'user': 'superman', 'activity': 'run', 'distance': 8},
        ])
        self.stdout.write(self.style.SUCCESS('Created activities.'))

        # Leaderboard
        Leaderboard = self.get_or_create_collection('leaderboard')
        Leaderboard.delete_many({})
        Leaderboard.insert_many([
            {'user': 'ironman', 'score': 100},
            {'user': 'spiderman', 'score': 90},
            {'user': 'batman', 'score': 95},
            {'user': 'superman', 'score': 110},
        ])
        self.stdout.write(self.style.SUCCESS('Created leaderboard.'))

        # Workouts
        Workouts = self.get_or_create_collection('workouts')
        Workouts.delete_many({})
        Workouts.insert_many([
            {'user': 'ironman', 'workout': 'pushups', 'count': 50},
            {'user': 'spiderman', 'workout': 'pullups', 'count': 30},
            {'user': 'batman', 'workout': 'situps', 'count': 40},
            {'user': 'superman', 'workout': 'squats', 'count': 60},
        ])
        self.stdout.write(self.style.SUCCESS('Created workouts.'))

        # Ensure unique index on email
        db = connection.cursor().db_conn.client['octofit_db']
        db['users'].create_index('email', unique=True)
        self.stdout.write(self.style.SUCCESS('Ensured unique index on user email.'))

    def get_or_create_collection(self, name):
        db = connection.cursor().db_conn.client['octofit_db']
        return db[name]

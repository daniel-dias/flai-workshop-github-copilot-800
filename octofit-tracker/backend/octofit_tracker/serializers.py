from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['_id', 'name', 'email', 'team']
        read_only_fields = ['_id']


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.ListField(child=serializers.CharField(), required=False)
    
    class Meta:
        model = Team
        fields = ['_id', 'name', 'members', 'total_points']
        read_only_fields = ['_id']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['_id', 'user_email', 'activity_type', 'duration', 'calories', 'date']
        read_only_fields = ['_id']


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = ['_id', 'user_email', 'user_name', 'team', 'total_calories', 'total_activities', 'rank']
        read_only_fields = ['_id']


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['_id', 'name', 'category', 'description', 'difficulty', 'duration', 'calories_per_session']
        read_only_fields = ['_id']

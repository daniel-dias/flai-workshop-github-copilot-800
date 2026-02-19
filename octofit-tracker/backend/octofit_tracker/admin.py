from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'team')
    search_fields = ('name', 'email')
    list_filter = ('team',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_points')
    search_fields = ('name',)
    ordering = ('-total_points',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'activity_type', 'duration', 'calories', 'date')
    search_fields = ('user_email', 'activity_type')
    list_filter = ('activity_type', 'date')
    ordering = ('-date',)
    date_hierarchy = 'date'


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('rank', 'user_name', 'team', 'total_calories', 'total_activities')
    search_fields = ('user_name', 'user_email')
    list_filter = ('team',)
    ordering = ('rank',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'difficulty', 'duration', 'calories_per_session')
    search_fields = ('name', 'category')
    list_filter = ('category', 'difficulty')

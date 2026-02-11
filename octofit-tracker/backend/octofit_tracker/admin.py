from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'fitness_level', 'total_points', 'created_at']
    list_filter = ['fitness_level', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-total_points']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model"""
    list_display = ['name', 'captain', 'total_points', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'captain__username']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['members']
    ordering = ['-total_points']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model"""
    list_display = ['user', 'activity_type', 'duration_minutes', 'points_earned', 'date', 'created_at']
    list_filter = ['activity_type', 'date', 'created_at']
    search_fields = ['user__username', 'activity_type']
    readonly_fields = ['created_at', 'points_earned']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard model"""
    list_display = ['user', 'rank', 'points', 'period', 'period_start', 'period_end', 'updated_at']
    list_filter = ['period', 'period_start', 'period_end']
    search_fields = ['user__username']
    readonly_fields = ['updated_at']
    ordering = ['period', 'rank']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout model"""
    list_display = ['name', 'fitness_level', 'activity_type', 'duration_minutes', 'created_by', 'created_at']
    list_filter = ['fitness_level', 'activity_type', 'created_at']
    search_fields = ['name', 'description', 'activity_type']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['fitness_level', 'name']

from djongo import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Extended user model for OctoFit Tracker"""
    _id = models.ObjectIdField(db_column='_id', primary_key=True)
    bio = models.TextField(blank=True, null=True)
    fitness_level = models.CharField(max_length=20, default='beginner', 
                                     choices=[('beginner', 'Beginner'), 
                                             ('intermediate', 'Intermediate'), 
                                             ('advanced', 'Advanced')])
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


class Team(models.Model):
    """Team model for group fitness challenges"""
    _id = models.ObjectIdField(db_column='_id', primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    captain = models.ForeignKey(User, on_delete=models.CASCADE, related_name='captained_teams')
    members = models.ManyToManyField(User, related_name='teams', blank=True)
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity model for logging fitness activities"""
    _id = models.ObjectIdField(db_column='_id', primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, 
                                     choices=[('running', 'Running'), 
                                             ('walking', 'Walking'), 
                                             ('cycling', 'Cycling'), 
                                             ('swimming', 'Swimming'), 
                                             ('strength', 'Strength Training'),
                                             ('yoga', 'Yoga'),
                                             ('other', 'Other')])
    duration_minutes = models.IntegerField()
    distance_km = models.FloatField(null=True, blank=True)
    calories_burned = models.IntegerField(null=True, blank=True)
    points_earned = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.date}"


class Leaderboard(models.Model):
    """Leaderboard model for tracking rankings"""
    _id = models.ObjectIdField(db_column='_id', primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
    rank = models.IntegerField()
    points = models.IntegerField()
    period = models.CharField(max_length=20, 
                             choices=[('weekly', 'Weekly'), 
                                     ('monthly', 'Monthly'), 
                                     ('all_time', 'All Time')])
    period_start = models.DateField()
    period_end = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['period', 'rank']
        unique_together = ['user', 'period', 'period_start']

    def __str__(self):
        return f"{self.user.username} - Rank {self.rank} ({self.period})"


class Workout(models.Model):
    """Workout model for personalized workout suggestions"""
    _id = models.ObjectIdField(db_column='_id', primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    fitness_level = models.CharField(max_length=20, 
                                    choices=[('beginner', 'Beginner'), 
                                            ('intermediate', 'Intermediate'), 
                                            ('advanced', 'Advanced')])
    activity_type = models.CharField(max_length=50)
    duration_minutes = models.IntegerField()
    instructions = models.TextField()
    equipment_needed = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_workouts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workouts'
        ordering = ['fitness_level', 'name']

    def __str__(self):
        return f"{self.name} ({self.fitness_level})"

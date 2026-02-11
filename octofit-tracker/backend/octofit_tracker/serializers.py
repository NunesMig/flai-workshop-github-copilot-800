from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 
                 'fitness_level', 'total_points', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'total_points']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if hasattr(obj, '_id') else None


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    id = serializers.SerializerMethodField()
    captain_name = serializers.CharField(source='captain.username', read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'captain', 'captain_name', 
                 'members', 'member_count', 'total_points', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'total_points']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if hasattr(obj, '_id') else None
    
    def get_member_count(self, obj):
        """Get the number of team members"""
        return obj.members.count()


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    id = serializers.SerializerMethodField()
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Activity
        fields = ['id', 'user', 'user_name', 'activity_type', 'duration_minutes', 
                 'distance_km', 'calories_burned', 'points_earned', 'notes', 
                 'date', 'created_at']
        read_only_fields = ['created_at', 'points_earned']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if hasattr(obj, '_id') else None
    
    def create(self, validated_data):
        """Calculate points when creating activity"""
        activity = Activity(**validated_data)
        # Simple points calculation: 10 points per 10 minutes
        activity.points_earned = (validated_data.get('duration_minutes', 0) // 10) * 10
        activity.save()
        
        # Update user's total points
        user = activity.user
        user.total_points += activity.points_earned
        user.save()
        
        return activity


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    id = serializers.SerializerMethodField()
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'user', 'user_name', 'rank', 'points', 'period', 
                 'period_start', 'period_end', 'updated_at']
        read_only_fields = ['updated_at']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if hasattr(obj, '_id') else None


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model"""
    id = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'fitness_level', 'activity_type', 
                 'duration_minutes', 'instructions', 'equipment_needed', 
                 'created_by', 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if hasattr(obj, '_id') else None

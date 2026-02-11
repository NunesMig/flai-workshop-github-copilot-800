from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from datetime import date, timedelta
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (UserSerializer, TeamSerializer, ActivitySerializer, 
                          LeaderboardSerializer, WorkoutSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get all activities for a specific user"""
        user = self.get_object()
        activities = Activity.objects.filter(user=user)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get statistics for a specific user"""
        user = self.get_object()
        total_activities = Activity.objects.filter(user=user).count()
        total_duration = Activity.objects.filter(user=user).aggregate(
            total=Sum('duration_minutes'))['total'] or 0
        
        return Response({
            'total_activities': total_activities,
            'total_duration_minutes': total_duration,
            'total_points': user.total_points,
            'fitness_level': user.fitness_level
        })


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for Team model"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(_id=user_id)
            team.members.add(user)
            team.save()
            return Response({'status': 'user joined team'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(_id=user_id)
            team.members.remove(user)
            team.save()
            return Response({'status': 'user left team'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, 
                          status=status.HTTP_404_NOT_FOUND)


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Activity model"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        """Filter activities by user if specified"""
        queryset = Activity.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        
        if user_id:
            queryset = queryset.filter(user___id=user_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent activities (last 7 days)"""
        seven_days_ago = date.today() - timedelta(days=7)
        activities = Activity.objects.filter(date__gte=seven_days_ago)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """ViewSet for Leaderboard model"""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    
    def get_queryset(self):
        """Filter leaderboard by period if specified"""
        queryset = Leaderboard.objects.all()
        period = self.request.query_params.get('period', None)
        
        if period:
            queryset = queryset.filter(period=period)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current week's leaderboard"""
        period = request.query_params.get('period', 'weekly')
        today = date.today()
        
        # Get leaderboard entries for current period
        leaderboard = Leaderboard.objects.filter(
            period=period,
            period_end__gte=today
        ).order_by('rank')
        
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    """ViewSet for Workout model"""
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    
    def get_queryset(self):
        """Filter workouts by fitness level if specified"""
        queryset = Workout.objects.all()
        fitness_level = self.request.query_params.get('fitness_level', None)
        
        if fitness_level:
            queryset = queryset.filter(fitness_level=fitness_level)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def suggested(self, request):
        """Get suggested workouts for a user based on their fitness level"""
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response({'error': 'user_id parameter required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(_id=user_id)
            workouts = Workout.objects.filter(fitness_level=user.fitness_level)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, 
                          status=status.HTTP_404_NOT_FOUND)

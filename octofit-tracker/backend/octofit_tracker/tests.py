from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import date, timedelta


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            fitness_level='beginner'
        )
    
    def test_user_creation(self):
        """Test user is created correctly"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.fitness_level, 'beginner')
        self.assertEqual(self.user.total_points, 0)
    
    def test_user_string_representation(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'testuser')


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.captain = User.objects.create_user(
            username='captain',
            email='captain@example.com',
            password='testpass123'
        )
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            captain=self.captain
        )
    
    def test_team_creation(self):
        """Test team is created correctly"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.captain, self.captain)
        self.assertEqual(self.team.total_points, 0)
    
    def test_team_string_representation(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration_minutes=30,
            distance_km=5.0,
            date=date.today()
        )
    
    def test_activity_creation(self):
        """Test activity is created correctly"""
        self.assertEqual(self.activity.user, self.user)
        self.assertEqual(self.activity.activity_type, 'running')
        self.assertEqual(self.activity.duration_minutes, 30)
    
    def test_activity_string_representation(self):
        """Test activity string representation"""
        expected = f"{self.user.username} - running - {date.today()}"
        self.assertEqual(str(self.activity), expected)


class WorkoutModelTest(TestCase):
    """Test cases for Workout model"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Beginner Running',
            description='A simple running workout',
            fitness_level='beginner',
            activity_type='running',
            duration_minutes=20,
            instructions='Run at a comfortable pace'
        )
    
    def test_workout_creation(self):
        """Test workout is created correctly"""
        self.assertEqual(self.workout.name, 'Beginner Running')
        self.assertEqual(self.workout.fitness_level, 'beginner')
        self.assertEqual(self.workout.duration_minutes, 20)
    
    def test_workout_string_representation(self):
        """Test workout string representation"""
        self.assertEqual(str(self.workout), 'Beginner Running (beginner)')


class UserAPITest(APITestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_get_users_list(self):
        """Test retrieving list of users"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_user_detail(self):
        """Test retrieving a single user"""
        url = reverse('user-detail', kwargs={'pk': self.user._id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.activity_data = {
            'user': self.user._id,
            'activity_type': 'running',
            'duration_minutes': 30,
            'distance_km': 5.0,
            'date': str(date.today())
        }
    
    def test_create_activity(self):
        """Test creating a new activity"""
        url = reverse('activity-list')
        response = self.client.post(url, self.activity_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_activities_list(self):
        """Test retrieving list of activities"""
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITest(APITestCase):
    """Test cases for Workout API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='A test workout',
            fitness_level='beginner',
            activity_type='running',
            duration_minutes=20,
            instructions='Test instructions'
        )
    
    def test_get_workouts_list(self):
        """Test retrieving list of workouts"""
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_filter_workouts_by_fitness_level(self):
        """Test filtering workouts by fitness level"""
        url = reverse('workout-list')
        response = self.client.get(url, {'fitness_level': 'beginner'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

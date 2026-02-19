from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import UserSerializer, TeamSerializer, ActivitySerializer, LeaderboardSerializer, WorkoutSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['get'])
    def by_email(self, request):
        """Get user by email"""
        email = request.query_params.get('email', None)
        if email:
            try:
                user = User.objects.get(email=email)
                serializer = self.get_serializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Email parameter required'}, status=status.HTTP_400_BAD_REQUEST)


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint for teams.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add a member to the team"""
        team = self.get_object()
        member_email = request.data.get('email')
        if member_email:
            if member_email not in team.members:
                team.members.append(member_email)
                team.save()
            return Response({'status': 'member added'})
        return Response({'error': 'Email required'}, status=status.HTTP_400_BAD_REQUEST)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for activities.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get activities by user email"""
        email = request.query_params.get('email', None)
        if email:
            activities = Activity.objects.filter(user_email=email)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({'error': 'Email parameter required'}, status=status.HTTP_400_BAD_REQUEST)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint for leaderboard.
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    
    @action(detail=False, methods=['get'])
    def top(self, request):
        """Get top users from leaderboard"""
        limit = int(request.query_params.get('limit', 10))
        top_users = Leaderboard.objects.all()[:limit]
        serializer = self.get_serializer(top_users, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    API endpoint for workouts.
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get workouts by category"""
        category = request.query_params.get('category', None)
        if category:
            workouts = Workout.objects.filter(category=category)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({'error': 'Category parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts by difficulty level"""
        difficulty = request.query_params.get('difficulty', None)
        if difficulty:
            workouts = Workout.objects.filter(difficulty=difficulty)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({'error': 'Difficulty parameter required'}, status=status.HTTP_400_BAD_REQUEST)

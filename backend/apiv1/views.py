from django.shortcuts import render
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from student.serializers import StudentRegistrationSerializer, StudentProfileSerializer
from student.models import StudentProfile


class StudentRegistrationView(generics.CreateAPIView):
    """
    Register a new student user
    POST /student/register
    """
    serializer_class = StudentRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            result = serializer.save()
            return Response(
                serializer.to_representation(result),
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {
                'message': 'Registration failed',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )






class StudentProfileDetailView(viewsets.ViewSet):
    """
    Get or update student profile
    GET /profile/{pk}
    PUT/PATCH /profile/{pk}
    """
    serializer_class = StudentProfileSerializer
    queryset = StudentProfile.objects.all()
    # lookup_field is set by the router to 'pk' by default, or you can set it here if needed

    def get_permissions(self):
        # Anyone can view, but only authenticated users can update
        if self.request.method == 'GET':
            # You need to import AllowAny
            return [AllowAny()]
        # Assuming you'll add IsAuthenticated or similar here later
        return super().get_permissions()

    # --- Router Mapped Methods ---

    def retrieve(self, request, pk=None):
        """Handles GET /profile/{pk}"""
        try:
            profile = self.queryset.get(pk=pk)
        except StudentProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(profile)
        return Response(serializer.data)
    
    def list(self, request):
        """Handles GET /profile/ (list all profiles)"""
        profiles = self.queryset.all()
        serializer = self.serializer_class(profiles, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handles PUT /profile/{pk} (Full Update)"""
        try:
            profile = self.queryset.get(pk=pk)
        except StudentProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # You would also typically implement partial_update for PATCH
    def partial_update(self, request, pk=None):
        """Handles PATCH /profile/{pk} (Partial Update)"""
        try:
            profile = self.queryset.get(pk=pk)
        except StudentProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Note: partial=True for PATCH
        serializer = self.serializer_class(profile, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
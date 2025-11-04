from django.shortcuts import render
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q, Value, IntegerField, Case, When
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
    Get or update student profile with filtering options
    
    GET /profile/ - List all profiles with optional filters:
        ?batch=56th - Filter by batch title
        ?program=bba - Filter by program name
        ?is_cr=true - Filter by CR status
        ?company=google - Fuzzy search by company name
        ?position=engineer - Fuzzy search by job position
        
    GET /profile/{pk} - Get single profile
    PUT/PATCH /profile/{pk} - Update profile
    """
    serializer_class = StudentProfileSerializer
    queryset = StudentProfile.objects.all()

    def get_permissions(self):
        # Anyone can view, but only authenticated users can update
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()

    def retrieve(self, request, pk=None):
        """Handles GET /profile/{pk}"""
        try:
            profile = self.queryset.get(pk=pk)
        except StudentProfile.DoesNotExist:
            return Response(
                {'message': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.serializer_class(profile)
        return Response(serializer.data)
    
    def list(self, request):
        """
        Handles GET /profile/ with filtering options
        
        Query Parameters:
        - batch: Filter by batch title (exact match, case-insensitive)
        - program: Filter by program name (exact match, case-insensitive)
        - is_cr: Filter by CR status (true/false)
        - company: Fuzzy search by company name (contains, case-insensitive)
        - position: Fuzzy search by job position (contains, case-insensitive)
        """
        # Start with all profiles, optimized with select_related
        profiles = self.queryset.select_related('batch', 'program')
        
        # Get filter parameters
        batch_filter = request.query_params.get('batch', None)
        program_filter = request.query_params.get('program', None)
        is_cr_filter = request.query_params.get('is_cr', None)
        company_filter = request.query_params.get('company', None)
        position_filter = request.query_params.get('position', None)
        
        # Apply filters if provided
        if batch_filter:
            profiles = profiles.filter(batch__title__iexact=batch_filter)
        
        if program_filter:
            profiles = profiles.filter(program__name__iexact=program_filter)
        
        if is_cr_filter is not None:
            # Convert string to boolean
            is_cr_bool = is_cr_filter.lower() in ('true', '1', 'yes')
            profiles = profiles.filter(is_cr=is_cr_bool)
        
        if company_filter:
            # Fuzzy match - contains search, case-insensitive
            profiles = profiles.filter(current_company__icontains=company_filter)
        
        if position_filter:
            # Fuzzy match - contains search, case-insensitive
            profiles = profiles.filter(current_job_position__icontains=position_filter)
        
        # Order by most relevant: CR first, then by name
        profiles = profiles.order_by('-is_cr', 'first_name', 'last_name')
        
        serializer = self.serializer_class(profiles, many=True)
        
        # Return with metadata about applied filters
        return Response({
            'count': len(serializer.data),
            'filters': {
                'batch': batch_filter,
                'program': program_filter,
                'is_cr': is_cr_filter,
                'company': company_filter,
                'position': position_filter,
            },
            'results': serializer.data
        })

    def update(self, request, pk=None):
        """Handles PUT /profile/{pk} (Full Update)"""
        try:
            profile = self.queryset.get(pk=pk)
        except StudentProfile.DoesNotExist:
            return Response(
                {'message': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.serializer_class(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """Handles PATCH /profile/{pk} (Partial Update)"""
        try:
            profile = self.queryset.get(pk=pk)
        except StudentProfile.DoesNotExist:
            return Response(
                {'message': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.serializer_class(profile, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def student_search(request):
    """
    Search students by name, email, phone, batch, program, company, or position
    GET /api/v1/search/?q=keyword
    
    Returns results ordered by relevance:
    1. Exact matches in name/uni_id (highest priority)
    2. Starts with matches in name
    3. Contains matches in name
    4. Matches in other fields
    """
    query = request.query_params.get('q', '').strip()
    
    if not query:
        return Response(
            {
                'message': 'Please provide a search query',
                'results': []
            },
            status=status.HTTP_200_OK
        )
    
    # Minimum length check to prevent very short queries
    if len(query) < 2:
        return Response(
            {
                'message': 'Search query must be at least 2 characters',
                'results': []
            },
            status=status.HTTP_200_OK
        )
    
    # Build the search query with Q objects for OR logic
    search_query = Q()
    
    # Search in multiple fields (case-insensitive)
    search_query |= Q(first_name__icontains=query)
    search_query |= Q(last_name__icontains=query)
    search_query |= Q(uni_id__icontains=query)
    search_query |= Q(email__icontains=query)
    search_query |= Q(phone__icontains=query)
    search_query |= Q(batch__title__icontains=query)
    search_query |= Q(batch__session__icontains=query)
    search_query |= Q(program__name__icontains=query)
    search_query |= Q(current_company__icontains=query)
    search_query |= Q(current_job_position__icontains=query)
    search_query |= Q(bio__icontains=query)
    
    # Query optimization: Use select_related to reduce database hits
    results = StudentProfile.objects.filter(search_query).select_related(
        'batch', 'program'
    ).annotate(
        # Relevance scoring for ordering
        relevance=Case(
            # Exact match in uni_id (highest priority)
            When(uni_id__iexact=query, then=Value(100)),
            # Exact match in first or last name
            When(Q(first_name__iexact=query) | Q(last_name__iexact=query), then=Value(90)),
            # Starts with in first or last name
            When(Q(first_name__istartswith=query) | Q(last_name__istartswith=query), then=Value(80)),
            # Exact match in email
            When(email__iexact=query, then=Value(70)),
            # Exact match in phone
            When(phone__iexact=query, then=Value(65)),
            # Starts with in uni_id
            When(uni_id__istartswith=query, then=Value(60)),
            # Contains in name
            When(Q(first_name__icontains=query) | Q(last_name__icontains=query), then=Value(50)),
            # Batch match
            When(batch__title__icontains=query, then=Value(40)),
            # Program match
            When(program__name__icontains=query, then=Value(35)),
            # Company or position match
            When(Q(current_company__icontains=query) | Q(current_job_position__icontains=query), then=Value(30)),
            # Email or phone contains
            When(Q(email__icontains=query) | Q(phone__icontains=query), then=Value(25)),
            # Bio match (lowest priority)
            When(bio__icontains=query, then=Value(10)),
            default=Value(1),
            output_field=IntegerField()
        )
    ).order_by('-relevance', 'first_name', 'last_name').distinct()
    
    # Limit results to prevent large response payloads
    results = results[:50]
    
    # Serialize the results
    serializer = StudentProfileSerializer(results, many=True)
    
    return Response(
        {
            'query': query,
            'count': len(serializer.data),
            'results': serializer.data
        },
        status=status.HTTP_200_OK
    )
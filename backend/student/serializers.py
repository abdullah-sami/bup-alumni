from rest_framework import serializers
from django.contrib.auth.models import User
from student.models import StudentProfile, Batch
from django.db import transaction


class StudentRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, required=False)
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)
    bio = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    profile_pic = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    batch = serializers.CharField(max_length=100, required=True)
    country = serializers.CharField(max_length=100, default='Bangladesh', allow_blank=True)
    current_position = serializers.CharField(max_length=200, required=False, allow_null=True, allow_blank=True)
    current_company = serializers.CharField(max_length=200, required=False, allow_null=True, allow_blank=True)
    is_cr = serializers.BooleanField(default=False)

    def validate_username(self, value):
        """Check if username (uni_id) already exists"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this university ID already exists.")
        if StudentProfile.objects.filter(uni_id=value).exists():
            raise serializers.ValidationError("A student profile with this university ID already exists.")
        return value

    def validate_email(self, value):
        """Check if email already exists (if provided)"""
        if value:
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("A user with this email already exists.")
            if StudentProfile.objects.filter(email=value).exists():
                raise serializers.ValidationError("A student profile with this email already exists.")
        return value

    def validate_batch(self, value):
        """Check if batch exists"""
        if not Batch.objects.filter(title=value).exists():
            raise serializers.ValidationError(f"Batch '{value}' does not exist.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        """Create User and StudentProfile"""
        
        # Extract data
        # FIXED: Properly handle uni_id vs email
        uni_id = validated_data.get('username')  # This should be the actual uni_id
        email = validated_data.get('email')
        password = validated_data.get('password')
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        bio = validated_data.get('bio')
        profile_pic = validated_data.get('profile_pic')
        batch_title = validated_data['batch']
        country = validated_data['country']
        current_position = validated_data.get('current_position')
        current_company = validated_data.get('current_company')
        is_cr = validated_data.get('is_cr', False)

        # Determine what to use as username for User model
        # If uni_id is provided, use it; otherwise fallback to email
        username_for_user = uni_id if uni_id else email

        # Get batch instance
        batch = Batch.objects.get(title=batch_title)

        # Create Django User
        user = User.objects.create_user(
            username=username_for_user,
            email=email if email else '',
            first_name=first_name,
            last_name=last_name,
            password=password  
        )

        # Create StudentProfile
        # FIXED: Always store the actual uni_id, not email
        student_profile = StudentProfile.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email if email else '',
            uni_id=uni_id if uni_id else email,  # Store actual uni_id
            bio=bio,
            profile_pic=profile_pic,
            batch=batch,
            country=country,
            current_job_position=current_position,
            current_company=current_company,
            is_cr=is_cr,
            is_verified=False  # Default to not verified
        )

        return {
            'user': user,
            'student_profile': student_profile
        }

    def to_representation(self, instance):
        """Format the response"""

        user = instance['user']
        student_profile = instance['student_profile']
        
        return {
            'message': 'Registration successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email if user.email else None,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'student_profile': {
                'uni_id': student_profile.uni_id,
                'batch': student_profile.batch.title,
                'country': student_profile.country,
                'is_cr': student_profile.is_cr,
                'is_verified': student_profile.is_verified,
                'profile_pic': student_profile.profile_pic,
            }
        }


class StudentProfileSerializer(serializers.ModelSerializer):
    batch = serializers.CharField(source='batch.title')
    
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'first_name', 'last_name', 'uni_id', 'bio', 'profile_pic',
            'batch', 'country', 'current_job_position', 'current_company',
            'email', 'phone', 'linkedin', 'facebook', 'instagram',
            'is_cr', 'is_verified'
        ]
        read_only_fields = ['is_verified']
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from student.models import StudentProfile


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'  # This can be uni_id, email, or phone
    
    role = serializers.SerializerMethodField()

    def validate(self, attrs):
        # The custom authentication backend will handle the multi-field lookup
        data = super().validate(attrs)

        # Get student profile if exists
        student_profile = None
        try:
            student_profile = StudentProfile.objects.get(uni_id=self.user.username)
        except StudentProfile.DoesNotExist:
            pass

        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.get_role(self.user),
            'student_profile': self.get_student_profile(student_profile) if student_profile else None,
        }
        return data
    
    def get_role(self, obj):
        try:
            student_profile = StudentProfile.objects.get(uni_id=obj.username)
            if student_profile.is_cr:
                return 'CR'
            return 'Student'
        except StudentProfile.DoesNotExist:
            return None
    
    def get_student_profile(self, profile):
        if not profile:
            return None
        return {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'uni_id': profile.uni_id,
            'batch': str(profile.batch),
            'is_verified': profile.is_verified,
            'is_cr': profile.is_cr,
        }
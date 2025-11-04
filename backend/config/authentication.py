from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q
from student.models import StudentProfile


class MultiFieldAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows users to login with:
    - University ID (username)
    - Email
    - Phone number
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        try:
            user = None
            
            # Try to find the user by uni_id (stored as username), email, or phone
            # First check if it's a direct username match
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # If not found by username, try to find by email in User model
                try:
                    user = User.objects.get(email=username)
                except User.DoesNotExist:
                    # If not found by email in User, search in StudentProfile
                    student_profile = StudentProfile.objects.filter(
                        Q(email=username) | Q(phone=username)
                    ).first()

                    
                    
                    if student_profile:
                        # Get the associated User by uni_id
                        try:
                            user = User.objects.get(username=student_profile.uni_id)
                        except User.DoesNotExist:
                            return None
                    else:
                        return None
            
            # Verify the password and check if user is active
            if user and user.check_password(password) and user.is_active:
                return user
                
        except Exception as e:
            # Log the exception for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Authentication error: {str(e)}")
            return None
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
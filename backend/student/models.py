from django.db import models




class Batch(models.Model):
    title = models.CharField(max_length=100)
    session =  models.CharField(max_length=20)

    def __str__(self):
        return f"{self.title} ({self.session})"
    


    

class Role(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title



class StudentProfile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    uni_id = models.CharField(max_length=20)
    bio = models.TextField(blank=True, null=True)
    profile_pic =  models.URLField(blank=True, null=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='students') 
    country = models.CharField(max_length=100, blank=True, null=True, default='Bangladesh')

    current_job_position = models.CharField(max_length=200, blank=True, null=True)
    current_company = models.CharField(max_length=200, blank=True, null=True)


    #contact
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    is_cr = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.batch.title}"
    




class StudentVerification(models.Model):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name='verification')

    def __str__(self):
        return f"Verification for {self.student.first_name} {self.student.last_name}"
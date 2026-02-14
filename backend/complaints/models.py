from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

def validate_file_size(value):
    limit = 100 * 1024 * 1024  # 100 MB
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 100 MB.')

class Project(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name='assigned_projects', blank=True)

    def __str__(self):
        return self.name

class ComplaintType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class SoftwareVersion(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='versions')
    version_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.project.name} - {self.version_number}"

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    CATEGORY_CHOICES = [
        ('software', '软件问题'),
        ('algorithm', '算法问题'),
        ('system', '系统问题'),
        ('other', '其他问题'),
    ]

    title = models.CharField(max_length=200)
    # Changed to accommodate rich text/HTML if needed, though TextField can hold HTML.
    # The requirement mentions images, which usually means storing images and referencing them in HTML 
    # OR using a specific rich text field. For simplicity in Django REST + Vue, we often use 
    # a TextField to store HTML content from a WYSIWYG editor.
    description = models.TextField() 
    
    customer_name = models.CharField(max_length=100, verbose_name="客户现场") # Mapping '客户现场' to this or creating new field? 
    # User asked for "客户现场" (Customer Site). Let's add a specific field for it or rename.
    # User also asked for "登记人员" (Registrant).
    
    site_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="客户现场")
    
    # Registrant (User who created the complaint)
    registrant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='registered_complaints')
    
    # Problem Type (Hardcoded choices as requested: 软件问题, 算法问题, 系统问题)
    # We can keep 'complaint_type' foreign key OR use a choice field. 
    # User specified specific types. Let's use a choice field for strict adherence or pre-populate ComplaintType.
    # Choice field is simpler for "软件问题, 算法问题, 系统问题".
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='software', verbose_name="问题类型")

    attachment = models.FileField(upload_to='attachments/', blank=True, null=True, validators=[validate_file_size], verbose_name="附件")

    contact_info = models.CharField(max_length=100, blank=True) # Making optional as not emphasized in new req
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    # We can keep this for backward compatibility or future dynamic types
    complaint_type = models.ForeignKey(ComplaintType, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    complaint_code = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name="问题编号")
    
    software_version = models.ForeignKey(SoftwareVersion, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="软件版本")

    def save(self, *args, **kwargs):
        if not self.complaint_code and self.project:
            # Generate code based on Project Code + Sequence
            # e.g., PROJ-001
            prefix = self.project.code
            
            # Find the last code for this project
            # Assuming format prefix-number
            last_complaint = Complaint.objects.filter(
                project=self.project,
                complaint_code__startswith=f"{prefix}-"
            ).order_by('-id').first()
            
            new_num = 1
            if last_complaint and last_complaint.complaint_code:
                try:
                    # Extract number part
                    parts = last_complaint.complaint_code.split('-')
                    if len(parts) >= 2:
                        last_num = int(parts[-1])
                        new_num = last_num + 1
                except ValueError:
                    # Fallback if parsing fails
                    pass
            
            self.complaint_code = f"{prefix}-{new_num:03d}"
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True, verbose_name="图片")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.complaint.title}'

@receiver(pre_save, sender=Project)
def track_project_code_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Project.objects.get(pk=instance.pk)
            if old_instance.code != instance.code:
                instance._old_code = old_instance.code
        except Project.DoesNotExist:
            pass

@receiver(post_save, sender=Project)
def update_complaint_codes(sender, instance, **kwargs):
    if hasattr(instance, '_old_code'):
        old_code = instance._old_code
        new_code = instance.code
        # Update all complaints for this project
        complaints = Complaint.objects.filter(project=instance, complaint_code__startswith=f"{old_code}-")
        for complaint in complaints:
            # Replace prefix
            complaint.complaint_code = complaint.complaint_code.replace(f"{old_code}-", f"{new_code}-", 1)
            complaint.save(update_fields=['complaint_code'])


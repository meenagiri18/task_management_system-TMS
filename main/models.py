from django.db import models
from django.contrib.auth.models import User
# models to Create task  
STATUS_CHOICES = [
    ('Not Started', 'Not Started'),
    ('Completed', 'Completed'),
    ('In Progress', 'In Progress'),
]

class Create_task(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='Not Started')
    start_date = models.DateField(null=True, blank=True)  
    end_date = models.DateField(null=True, blank=True) 
    isDelete = models.BooleanField(default=False)  
    is_completed = models.BooleanField(default=False)   

    def __str__(self) -> str:
        return self.title

# models to assign task 
class Assign_task(models.Model): 
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='Not Started')
    ddate = models.DateField(null=True, blank=True) 
    assign_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_tasks',
        null=True
    )
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks_assigned_by',
        null=True
    )
    is_deleted = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

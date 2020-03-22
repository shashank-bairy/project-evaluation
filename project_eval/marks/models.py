from django.db import models
from accounts.models import Student,Panel,Faculty

class Rubrics(models.Model):
    phase = models.PositiveIntegerField()
    max_marks = models.PositiveIntegerField()
    description = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Rubrics"

    def __str__(self):
        return self.description

class Marks(models.Model):
    usn = models.ForeignKey(Student,related_name='marks',on_delete=models.CASCADE)
    rubric_id = models.ForeignKey(Rubrics,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    faculty = models.ForeignKey(Faculty,blank=True,on_delete=models.CASCADE,null=True)
    date_entered = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        verbose_name_plural = "Marks"

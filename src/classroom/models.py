from django.db import models
from django.db.models.deletion import CASCADE, PROTECT


# Create your models here.
class Discipline(models.Model):
    name = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=10)
    url = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"[{self.code}] {self.name}"



class Topic(models.Model):
    discipline_fk = models.ForeignKey(Discipline, on_delete=PROTECT)
    acronym = models.CharField(max_length=4)
    name = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together = (("discipline_fk", "acronym"))

class Assignment(models.Model):
    discipline_fk = models.ForeignKey(Discipline, on_delete=PROTECT)
    topic_fk = models.ForeignKey(Topic, on_delete=PROTECT, null=True)
    acronym = models.CharField(max_length=4)
    name = models.CharField(max_length=50)
    assignment_url = models.CharField(max_length=255, unique=True)
    invitation_url = models.CharField(max_length=255, unique=True)
    deadline = models.DateTimeField(null=True)
    
    total_auto_grade = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_grade = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    class Meta:
        unique_together = (("discipline_fk", "acronym"))

    def __str__(self):
        return f"{self.discipline_fk.name} [{self.acronym}] {self.name}"

class Student(models.Model):
    name = models.CharField(max_length=100)
    class_id = models.CharField(max_length=100, unique=True)

class Handin(models.Model):
    assignment_fk = models.ForeignKey(Assignment, on_delete=PROTECT)
    student_fk = models.ForeignKey(Student, on_delete=PROTECT)
    feedback_url = models.CharField(max_length=255, null=True, blank=True)
    auto_grade = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_grade = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    complementar_grade = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        unique_together = (("assignment_fk", "student_fk"))



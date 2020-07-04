from django.db import models
from django.contrib.auth.models import User


class Program(models.Model):
    name = models.CharField(max_length=10)
    sanctioned = models.IntegerField()
    current = models.IntegerField()


class Profile(models.Model):
    user = models.OneToOneField(User)
    roll = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=10)
    cpi = models.FloatField(default=0.0)
    allotted = models.ForeignKey(Program)

    # @classmethod
    # def create(cls, user_t, roll_t, name_t, cpi_t, prog_t):
    # 	prof = cls(user=user_t, roll = roll_t, name = name_t, cpi = cpi_t, allotted=prog_t)
    # 	return prof


class ProgramProfile(models.Model):
    student = models.ForeignKey(Profile, related_name='link_to_profile')
    program = models.ForeignKey(Program, related_name='link_to_program')
    number = models.PositiveIntegerField()

    class Meta:
        ordering = ["number"]

    # @classmethod
    # def create(cls, student_t, program_t, num_t):
    #     pref =  cls(student=student_t, program=program_t, num=num_t)
    #     return pref

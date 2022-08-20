from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Employee(models.Model):
    SEX_CHOICES = (
        ('F', 'Female',),
        ('M', 'Male',),
        ('U', 'Unsure',),
    )

    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=False, blank=False)
    phone = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Configuration(models.Model):

    scheme_name = models.CharField(max_length=200, null=False, blank=False)
    is_parent = models.BooleanField(null=False, blank=False, default=False)
    parent_field = models.CharField(max_length=200, null=True, blank=True)
    field = models.CharField(max_length=200, null=False, blank=False)
    xpath = models.CharField(max_length=1000, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['scheme_name', 'field', 'parent_field'], name='unique_set')
        ]

    def __str__(self):
        if self.is_parent:
            return self.scheme_name + " -> " + "(PARENT) " + "[ Field: " + self.field + "]"
        else:
            return self.scheme_name + " -> " + "(Parent Field: " + self.parent_field + ") " + "[ Field: " + self.field + "]"





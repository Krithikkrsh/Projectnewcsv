from django.db import models

# Create your models here.
class Table(models.Model):

    Name = models.CharField(max_length=150)
    data = models.JSONField(db_index=True,null=True)
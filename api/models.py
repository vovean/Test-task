from django.db import models


# Create your models here.

class Task(models.Model):
    owner_id = models.IntegerField(null=False)
    name = models.CharField(null=False, max_length=100)
    finished = models.BooleanField(null=False, default=False)

    def change_status(self):
        self.finished = not self.finished
        self.save()

    def __repr__(self):
        return f'Task: "{self.name}" created by user #{self.owner_id}. Finished: {self.finished}'

    def __str__(self):
        return self.__repr__()

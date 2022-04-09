from datetime import datetime

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class Department(models.Model):
    name = models.CharField('Department name', max_length=120, unique=True)
    description = models.CharField('Description of department', max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    department = models.ForeignKey(Department,
                                   on_delete=models.PROTECT,
                                   verbose_name='Position department name',
                                   related_name='roles')
    name = models.CharField('Position name', max_length=30)
    is_header = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# abstract class for Task and Project
class TaskInfo(models.Model):
    STATUS_CHOICES = (
        ('In work', 'In work'),
        ('Canceled', 'Canceled'),
        ('Finished', 'Finished'),
        ('Awaiting', 'Awaiting'),
    )

    PRIORITY_CHOICES = (
        ('Very high', 'Very important'),
        ('High', 'High'),
        ('Middle', 'Middle'),
        ('Low', 'Low'),
        ('Very low', 'Very low'),
    )

    name = models.CharField('Name of task', max_length=120, unique=True)
    description = models.CharField('Description', max_length=300)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, verbose_name='Status of project/task', blank=True)
    priority = models.CharField(max_length=40, choices=PRIORITY_CHOICES, verbose_name='Priority of project/task')
    start_date = models.DateTimeField('Time when project/task was created', auto_now_add=True)
    planned_date = models.DateTimeField('Planned end date')
    finish_date = models.DateTimeField('Time when project/task was finished', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.status:
            self.status = 'In work'
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Project(TaskInfo):
    manager = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='projects',
                                verbose_name='Users hwo can delegate and update')

    def __str__(self):
        return f'Project:{self.name}, status: {self.status}'

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})

    def change_status(self, new_status):
        if new_status == 'Finished' or new_status == 'Canceled':
            self.finish_date = datetime.now()

    class Meta:
        ordering = ['-start_date']


# The task need for statistics time for every task for every executor and for link to project
class Task(TaskInfo):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    executor = models.ForeignKey(get_user_model(),
                                 on_delete=models.PROTECT,
                                 verbose_name='Executor of this task',
                                 related_name='tasks')
    # time when executor select 'task in await'
    start_await_date = models.DateTimeField(null=True, blank=True)
    # it will be calculated when task 'closed' or 'finished'
    active_time = models.DurationField(null=True, blank=True)
    passive_time = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f'Task:{self.name}, executor: {self.executor}'

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})

    # calculate time if form was changed
    def change_status(self, new_status):
        if new_status == 'Finished' or new_status == 'Canceled':
            self.finish_date = datetime.now()
            self.active_time = self.start_date - self.finish_date - self.passive_time
        if new_status == 'Awaiting':
            self.start_await_date = datetime.now()
        if new_status == 'In work' and self.status == 'Awaiting':
            self.passive_time = self.start_await_date + datetime.now()
        self.start_await_time = None

    class Meta:
        ordering = ['-start_date']

from django.shortcuts import render
from django.views.generic import ListView, DetailView

from task.models import Department


class DepartmentListView(ListView):
    model = Department


class DepartmentDetailView(DetailView):
    model = Department

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = self.object.roles.all()
        return context

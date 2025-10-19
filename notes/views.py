from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import NotesForm
from .models import Notes

def add_like_view(request,pk):
    if request.method == 'POST':
        note = get_object_or_404(Notes, pk=pk)
        note.likes += 1
        note.save()
        return HttpResponseRedirect(reverse("notes.detail", args=(pk,)))
    raise Http404

def change_visibility_view(request,pk):
    if request.method == 'POST':
        note = get_object_or_404(Notes, pk=pk)
        note.is_public = not note.is_public
        note.save()
        return HttpResponseRedirect(reverse("notes.detail", args=(pk,)))
    raise Http404

class NotesDeleteView(DeleteView):
    model = Notes
    success_url = '/smart/notes'
    template_name = 'notes/notes_delete.html'

class NotesUpdateView(UpdateView):
    model = Notes
    success_url = '/smart/notes'
    form_class = NotesForm

class NotesCreateView(CreateView):
    model = Notes
    success_url = '/smart/notes'
    form_class = NotesForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = "notes"
    template_name = "notes/notes_list.html"
    login_url = '/admin'

    def get_queryset(self):
        return self.request.user.notes.all()

class PopularNotesListView(ListView):
    model = Notes
    context_object_name = "notes"
    template_name = "notes/notes_popular.html"
    queryset = Notes.objects.filter(likes__gte=3)

class NotesDetailView(DetailView):
    model = Notes
    context_object_name = "note"

class NotesPublicDetailView(DetailView):
    model = Notes
    context_object_name = "note"
    queryset = Notes.objects.filter(is_public=True)

def detail(request, pk):
    try:
        note = Notes.objects.get(pk=pk)
    except Notes.DoesNotExist:
        raise Http404("Note does not exist")
    return render(request, 'notes/notes_detail.html',{'note':note})
# Create your views here.

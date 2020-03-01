from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.messages.storage import session
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from rest_framework import generics, renderers, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .forms import CardCreateForm, CardUpdateForm, SignUpForm
from .models import Card
from .serializers import CardSerializer, CardStatusSerializer


class SignUpView(CreateView):


    form_class = SignUpForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid

class CardCreateView(CreateView):


    model = Card
    success_url = '/'
    template_name = 'index.html'
    form_class = CardCreateForm

    def form_valid(self, form):

        card_name = form.cleaned_data.get('name')
        card_description = form.cleaned_data.get('description')
        card_assignee = form.cleaned_data.get('assignee')
        if card_assignee == None:
            Card.objects.create(name=card_name, description=card_description, creator=self.request.user)
        else:
            card_assignee = User.objects.get(username=form.cleaned_data.get('assignee'))
            Card.objects.create(name=card_name, description=card_description, creator=self.request.user, assignee=card_assignee)
        messages.success(self.request, f'The card "{card_name}" has been created and assigned to "{card_assignee}"!')
        return redirect('index')

class CardUpdateView(UpdateView):


    model = Card
    template_name = "update.html"
    success_url = '/'
    form_class = CardUpdateForm

    def get_form(self, form_class=None):

        self.object = self.get_object()
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(**self.get_form_kwargs())
        if (self.request.user.is_superuser == False) and (self.request.user != self.object.creator):
            form.fields['name'].widget.attrs['readonly'] = 'readonly'
            form.fields['name'].widget.attrs['disabled'] = 'disabled'
            form.fields['description'].widget.attrs['readonly'] = 'readonly'
            form.fields['description'].widget.attrs['disabled'] = 'disabled'
            form.fields['assignee'].widget.attrs['readonly'] = 'readonly'
            form.fields['assignee'].widget.attrs['disabled'] = 'disabled'

        return form

    def get_form_kwargs(self):

        kwargs = super(CardUpdateView, self).get_form_kwargs()

        if self.request.user.is_superuser == False:
            kwargs.update({'queryset': User.objects.filter(username=self.request.user)})
        else:
            kwargs.update({'queryset': User.objects.all()})
        return kwargs

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context['object'] = self.object
            context['card_creator'] = self.object.creator
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        return super().get_context_data(**context)

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        self.object.date_edited = timezone.now()
        self.object.save()

        if request.is_ajax():
            elm_id = request.POST['element_id']
            card_id = request.POST['card_id']
            user_object = request.POST['user_object']
            user = User.objects.get(username=user_object)
            card = Card.objects.get(id=card_id)
            if not user.is_superuser:
                if card.assignee == user:
                    if elm_id != "DN":
                        card.status = elm_id
                        card.date_edited = timezone.now()
                        card.save()
                    else:
                        messages.error(self.request, f'You are not permitted to move cards to Done column!')
                else:
                    messages.error(self.request, f'You cannot move cards assigned to other users!')
            else:
                if (card.status == "RD" or card.status == "DN") and (elm_id == "RD" or elm_id == "DN"):
                    card.status = elm_id
                    card.date_edited = timezone.now()
                    card.save()
                else:
                    messages.error(self.request, f'You can move cards only between Ready or Done columns!')

        return super().post(request, *args, **kwargs)

class CardDeleteView(DeleteView):


    model = Card
    template_name = 'index.html'
    success_url = '/'

    def delete(self, request, *args, **kwargs):

        messages.success(self.request, f'The card "{self.get_object().name}" has been successfully deleted!')
        return super(CardDeleteView, self).delete(request, *args, **kwargs)

class IndexListView(ListView):


    model = Card
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context =  super(IndexListView, self).get_context_data(**kwargs)
        context['form'] = CardCreateForm(request=self.request)
        context['new_list'] = Card.objects.filter(status="NW")
        context['in_progress_list'] = Card.objects.filter(status="INP")
        context['in_qa_list'] = Card.objects.filter(status="INQ")
        context['ready_list'] = Card.objects.filter(status="RD")
        context['done_list'] = Card.objects.filter(status="DN")
        context['users_list'] = User.objects.all()
        return context

class CardViewSet(viewsets.ModelViewSet):


    queryset = Card.objects.all()
    serializer_class = CardSerializer

class CardList(generics.ListAPIView):


    serializer_class = CardStatusSerializer

    def get_queryset(self):

        queryset = Card.objects.all()
        status = self.request.query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)
        return queryset

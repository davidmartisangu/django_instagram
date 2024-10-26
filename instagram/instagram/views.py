from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponseRedirect

from .forms import RegistrationForm, LoginForm
from profiles.models import UserProfile

# Create your views here.

class HomeView(TemplateView):
    template_name="general/home.html"


class LoginView(FormView):
    template_name="general/login.html"
    form_class = LoginForm

    def form_valid(self,form):
        usuario = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=usuario, password=password)

        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, f'Bienvenido de nuevo {user.username}')
            return HttpResponseRedirect(reverse ('home'))
        
        else:
            messages.add_message(self.request, messages.ERROR, f'Usuario no valido o contraseña incorrecta')
            return super(LoginView, self).form_invalid(form)


class RegisterView(CreateView):
    template_name="general/register.html"
    model = User
    success_url = reverse_lazy("login")
    form_class = RegistrationForm
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Usuario creado correctamente.")
        return super(RegisterView, self).form_valid(form)
    

class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = "general/profile_detail.html"
    context_object_name = "profile"


class LegalView(TemplateView):
    template_name="general/legal.html"


class ContactView(TemplateView):
    template_name="general/contact.html"


class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = "general/profile_update.html"
    context_object_name = "profile"
    fields = ['profile_picture', 'bio', 'birth_date']

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Perfil editado correctamente.")
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile_detail', args=[self.object.pk])

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Se ha cerrado la sesión correctamente")
    return HttpResponseRedirect(reverse("home"))
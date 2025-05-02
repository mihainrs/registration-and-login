from django.contrib.auth.base_user import AbstractBaseUser
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .forms import RegisterAccount, LoginForm

#vvvvv for the mail confirmation part vvvvvv

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .tokens import account_activation_token

# Create your views here.

class MainPageView(TemplateView):
    template_name = "reglog/mainpage.html"

class AccountPageView(LoginRequiredMixin, TemplateView):
    template_name = "reglog/accountpage.html"
    
class LogoutV(LogoutView):
    template_name = "reglog/logout.html"
    def get_next_page(self):
        return reverse_lazy('logout')
    
def SignUp(request):
    if request.method == "POST":
        form = RegisterAccount(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
             # Deactivate account till it is confirmed
            user.is_active = False
            user.save()
            
            #email conf
            current_site = get_current_site(request)
            subject = 'Activate Your Account!'
            message = render_to_string('reglog/activation_mail.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            send_mail(subject,message,'noreply@mydomain.com',[user.email])
            
            messages.success(request, "Account created! Please confirm your email.")
            return redirect('mainpage')
    else:
        form = RegisterAccount()
        
    return render(request, "reglog/signup.html", {'form':form})

#creating an activation view

def activate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been confirmed!')
        return redirect('mainpage')
    else:
        return render(request, 'account_activation_invalid.html')

# method for the login form
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'reglog/mainpage.html'
    #redirecting after successful login
    success_url = reverse_lazy('accountpage')
    
    #called when form is valid
    def form_valid(self, form):
        #using cleaned data to get user submitted values
        #in a safe manner, for when working with sensitive info
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Welcome back, {user.username}!")
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid username or password.")
            return self.form_invalid(form)

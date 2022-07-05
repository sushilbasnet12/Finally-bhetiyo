
# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .models import NewUser
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.core.mail import send_mail


def check_user(user):
    return not user.is_authenticated


user_logout_required = user_passes_test(check_user, '/', None)


def auth_user_should_not_access(viewfunc):
    return user_logout_required(viewfunc)


class CreateUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.fields['user_name'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Username'
        })
        self.fields['user_name'].label = ""
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'First Name'
        })
        self.fields['first_name'].label = ""

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Last Name'
        })
        self.fields['last_name'].label = ""

        self.fields['email'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Email'
        })
        self.fields['email'].label = ""

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Password'
        })
        self.fields['password1'].label = ""

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Password Confirmation'
        })
        self.fields['password2'].label = ""

        self.fields['password2'].help_text = ""
        self.fields['password1'].help_text = ""

    class Meta:
        model = NewUser
        fields = ['first_name',
                  'last_name', 'user_name', 'email',  'password1', 'password2']


@auth_user_should_not_access
def loginView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        _user = NewUser.objects.filter(
            email=request.POST.get('username')).first()
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            if(_user is not None and _user.is_active is not True):
                messages.error(request, 'Please Verify your email first')
            else:
                messages.error(request, 'Email or Password is incorrect')

    return render(request, 'login.html', {})


def logoutView(request):
    logout(request)
    return redirect('home')


@auth_user_should_not_access
def registerPage(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('email_template.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, None, [to_email])
            messages.error(
                request, 'Verification link is sent to your mail. Please verify before login')
            return redirect('login')

        else:
            context = {'form': form}
            return render(request, 'register.html', context)
    else:
        form = CreateUserForm()
        context = {'form': form}
        return render(request, 'register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = NewUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, NewUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.error(
            request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')

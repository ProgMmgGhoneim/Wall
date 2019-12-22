from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect ,get_object_or_404
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import login, authenticate
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView



from .models import Profile ,Wall
from .forms import SignForm ,WallForm
from .tokens import account_activation_token

# Create your views here.

#SingUp
def SignUp(request):
    if request.method == 'POST':
        form = SignForm(request.POST)
        if form.is_valid():
            user = form.save(commit= False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(subject, message, to=[to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
    else:
        form = SignForm()
    context ={'form':form}
    template_name= 'signup.html'
    return render(request ,template_name,context)

def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token ,backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception as e:
         print(e)
         user=None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')


# def SignIn(request):
#     msg = []
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 return redirect('home')
#     else:
#         msg.append('Invalid Login credentials, try again!')
#     return render(request, 'login.html', {'errors': msg})


class WallList(ListView):
    model = Wall
    template_name = 'home.html'
    context_object_name ='wall_list'

class WallDetailsView(DetailView):
    model = Wall
    template_name = 'wall_details.html'
    context_object_name ='wall_info'

@login_required
def YourWall(request):
    if request.user.is_authenticated:
        wall_qs = Wall.objects.filter(author=request.user)
    template_name = 'wall.html'
    return render(request , template_name , {'wall_list':wall_qs})


@login_required
def WallCreate(request):
    form = WallForm(request.POST or None ,request.FILES or None)
    if form.is_valid():
        obj = form.save(commit =False)
        obj.author = request.user
        obj.save()
        form.save()
        return redirect('home')
    template_name = 'wall_create.html'
    context ={'form':form}
    return render(request , template_name ,context)

@login_required
def WallUpdate(request ,slug):
    obj = get_object_or_404(Wall , slug=slug)
    form = WallForm(request.POST or None  ,request.FILES or None,instance=obj)
    if form.is_valid():
        form.save()
        return redirect('home')
    template_name = 'wall_update.html'
    context ={'form':form}
    return render(request , template_name ,context)

@login_required
def WallDelete(request , slug):
    obj = get_object_or_404(Wall , slug=slug)
    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    template_name = 'wall_delete.html'
    context ={
    'object':obj
    }
    return render(request , template_name ,context)

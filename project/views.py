from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse

# Create your views here.


def home(request):
    return render(request, 'project/main.html')

# def login(request):
#     return render(request, 'login.html')

# def signUp(request):
#     return render(request, 'register.html')

# def userDashboard(request):
#     return render(request, 'userDashboard.html')

# def profile(request):
#     return render(request, 'profile.html')

# def appointment(request):
#     return render(request, 'appointment.html')


# def test(request):
#     return render(request, 'test.html')

# def signup(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, 'Your account has been created successfully!')
#             return redirect('login')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'register.html', {'form': form})


# def userlogin(request):
#     if request.method == 'POST':
#         prn = request.POST.get('prn')
#         password = request.POST.get('password')
#         user = authenticate(request, prn=prn, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('project')
#         else:
#             error_message = "Invalid login credentials"
#             return render(request, 'login.html', {'error_message': error_message})
#     else:
#         return render(request, 'login.html')
        

# def userLogout(request):
#     logout(request)
#     return redirect('login')


# def Register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('login')
#     else:
#         form = UserCreationForm()
#         return render(request, 'test.html', {'form': form})

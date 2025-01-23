from django.shortcuts import redirect, render
from .models import Project
from .forms import ProjectForm, UserRegistrationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.

def proxpo(request):
     return render(request, 'proxpo.html')

def index(request, project_id):
    project = get_object_or_404(Project, pk=project_id) 
    return render(request, 'index.html', {'project': project})

def about(request):
     return render(request, 'about.html')

def services(request):
     return render(request, 'services.html')

def search_users(request):
    query = request.GET.get('q', '') 
    users = User.objects.filter(Q(username__icontains=query)) if query else [] 
    return render(request, 'search_results.html', {'query': query, 'users': users})

def project_list(request):
     projects = Project.objects.all().order_by('-created_at')
     return render(request, 'project_list.html', {'projects':projects})

@login_required
def project_create(request):
     if request.method == 'POST':
          form = ProjectForm(request.POST, request.FILES)
          if form.is_valid():
               project = form.save(commit = False)
               project.user = request.user
               project.save()
               return redirect('project_list')

     form = ProjectForm()
     return render(request, 'project_form.html', {'form':form})

@login_required
def project_edit(request, project_id):
     project = get_object_or_404(Project, pk = project_id, user = request.user)
     if request.method == 'POST':
          form = ProjectForm(request.POST, request.FILES, instance = project)
          if form.is_valid():
               project = form.save(commit=False)
               project.user = request.user
               project.save()

               return redirect('project_list')
     else:
          form = ProjectForm(instance=project)

     return render(request, 'project_form.html', {'form':form})

@login_required
def project_delete(request, project_id):
     project = get_object_or_404(Project, pk = project_id, user = request.user)
     if request.method == 'POST':
          project.delete()

          return redirect('project_list')
     
     return render(request, 'project_confirm_delete.html', {'project':project})


def register(request):
     if request.method == 'POST':
          form = UserRegistrationForm(request.POST)
          if form.is_valid():
               user = form.save(commit=False)
               user.set_password(form.cleaned_data['password1'])
               user.save()
               login(request, user)

               return redirect('project_list')
     else:
          form = UserRegistrationForm()

     return render(request, 'registration/register.html', {'form':form})
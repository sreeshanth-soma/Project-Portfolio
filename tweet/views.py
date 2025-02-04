from django.shortcuts import redirect, render, get_object_or_404
from .models import Project, Comment
from .forms import ProjectForm, UserRegistrationForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Q, Avg
from django.contrib import messages


# Create your views here.

# def chat_view(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             user_message = data.get('message', '')

#             if not user_message:
#                 return JsonResponse({'error': 'No message provided'}, status=400)

#             openai.api_key = settings.OPENAI_API_KEY  # Set your OpenAI API key

#             # Check if the OpenAI key is valid
#             if not openai.api_key:
#                 return JsonResponse({'error': 'OpenAI API Key not set'}, status=400)

#             response = openai.Completion.create(
#                 engine="text-davinci-003",
#                 prompt=user_message,
#                 max_tokens=150
#             )

#             bot_reply = response.choices[0].text.strip()  # Get the AI's response
#             return JsonResponse({'response': bot_reply})

#         except openai.error.OpenAIError as e:
#             # This will catch any OpenAI API-specific errors
#             error_message = f"OpenAI API Error: {str(e)}"
#             print(error_message)  # You can log it or print for debugging
#             return JsonResponse({'error': error_message}, status=500)

#         except Exception as e:
#             # General error handler for any other exceptions
#             error_message = f"Something went wrong: {str(e)}"
#             print(error_message)  # You can log it or print for debugging
#             return JsonResponse({'error': error_message}, status=500)

#     return JsonResponse({'error': 'Invalid request'}, status=400)


def add_comment(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Check if the user already commented on this project
    if Comment.objects.filter(user=request.user, project=project).exists():
        messages.error(request, "You have already commented on this project.")
        return redirect('project_detail', project_id=project.id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.project = project
            comment.save()
            messages.success(request, "Your comment has been added.")
            return redirect('project_detail', project_id=project.id)
    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'form': form, 'project': project})



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

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    projects = Project.objects.filter(user=user).order_by('-created_at')
    return render(request, 'profile.html', {'user': user, 'projects': projects})

def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'project_list.html', {'projects': projects})


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    comments = Comment.objects.filter(project=project).order_by('-created_at')

    if request.method == 'POST' and request.user != project.user:  # Only other users can comment
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.project = project
            comment.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = CommentForm()

    return render(request, 'project_detail.html', {
        'project': project,
        'comments': comments,
        'form': form,
    })


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'project_form.html', {'form': form})

@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, pk=project_id, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project_form.html', {'form': form})


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
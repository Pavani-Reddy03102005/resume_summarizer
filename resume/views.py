from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Resume, SkillTag
from .utils import (
    extract_text_from_pdf,
    generate_summary,
    extract_skills,
    generate_match_score
)


# 🏠 Home
def home(request):
    return render(request, 'resume/home.html')


# 📝 Register
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, 'Account created successfully')
        return redirect('login')

    return render(request, 'resume/register.html')


# 🔐 Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, 'Invalid credentials')

    return render(request, 'resume/login.html')


# 🚪 Logout
def logout_view(request):
    logout(request)
    return redirect('home')


# 📊 Dashboard
@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user)

    stats = {
        'total': resumes.count(),
        'completed': resumes.filter(status='completed').count(),
        'pending': resumes.filter(status='pending').count(),
        'failed': resumes.filter(status='failed').count(),
    }

    context = {
        'stats': stats,
        'recent_resumes': resumes.order_by('-uploaded_at')[:5],
    }

    return render(request, 'resume/dashboard.html', context)


# 📤 Upload Resume (AI Processing)
@login_required
def upload_resume(request):
    if request.method == 'POST':
        file = request.FILES.get('resumes')

        if not file:
            messages.error(request, 'Please select a file')
            return redirect('upload_resume')

        try:
            # 🔥 Extract text from PDF
            text = extract_text_from_pdf(file)

            # 🔥 Create Resume object
            resume = Resume.objects.create(
                user=request.user,
                resume_file=file,
                original_filename=file.name,
                candidate_name=file.name,
                status='completed',
                ai_summary=generate_summary(text),
                job_match_score=generate_match_score(text)
            )

            # 🔥 Extract skills
            skills = extract_skills(text)

            for skill in skills:
                SkillTag.objects.create(resume=resume, skill=skill)

            messages.success(request, 'Resume uploaded and analyzed successfully')

        except Exception as e:
            messages.error(request, f'Error processing resume: {str(e)}')

        return redirect('resume_list')

    return render(request, 'resume/upload_resume.html')


# 📋 Resume List
@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)

    context = {
        'page_obj': resumes,
        'total': resumes.count()
    }

    return render(request, 'resume/resume_list.html', context)


# 🔍 Resume Detail
@login_required
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)

    return render(request, 'resume/resume_detail.html', {
        'resume': resume
    })


# 🗑️ Delete Resume
@login_required
def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)

    resume.delete()
    messages.success(request, 'Resume deleted successfully')

    return redirect('resume_list')


# 📈 Analytics
@login_required
def analytics(request):
    resumes = Resume.objects.filter(user=request.user)

    scores = resumes.exclude(job_match_score=None)

    avg_score = 0
    if scores.exists():
        total = sum([r.job_match_score for r in scores])
        avg_score = int(total / scores.count())

    context = {
        'total': resumes.count(),
        'avg_score': avg_score,
        'status_counts': {
            'completed': resumes.filter(status='completed').count(),
            'pending': resumes.filter(status='pending').count(),
            'failed': resumes.filter(status='failed').count(),
        },
        'top_skills': SkillTag.objects.all()[:5],
    }

    return render(request, 'resume/analytics.html', context)
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import FileResponse
from .models import SiteProfile, Resume
from .forms import ContactForm
from apps.blog.models import BlogPost
from apps.portfolio.models import Project


def home(request):
    profile = SiteProfile.objects.first()
    latest_posts = BlogPost.objects.filter(
        status=BlogPost.STATUS_PUBLISHED
    ).order_by('-published_at')[:6]
    featured_projects = Project.objects.filter(featured=True)[:3]

    return render(request, 'core/home.html', {
        'profile': profile,
        'latest_posts': latest_posts,
        'featured_projects': featured_projects,
    })


def about(request):
    skills_by_category = {}
    for skill in Skill.objects.all():
        label = skill.get_category_display()
        if label not in skills_by_category:
            skills_by_category[label] = []
        skills_by_category[label].append(skill)

    interests = [
        'Backend Development', 'Django Framework', 'Open Source',
        'Clean Code', 'Database Design', 'API Design', 'DevOps', 'Tech Writing',
    ]

    return render(request, 'core/about.html', {
        'skills_by_category': skills_by_category,
        'interests': interests,
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thanks for reaching out! I'll get back to you as soon as possible."
            )
            return redirect('core:contact')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})


def resume_download(request):
    resume = Resume.objects.filter(active=True).first()
    if not resume:
        messages.error(request, 'Resume is not available right now. Check back soon!')
        return redirect('core:home')
    response = FileResponse(resume.file.open('rb'), as_attachment=True)
    filename = resume.file.name.split('/')[-1]
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

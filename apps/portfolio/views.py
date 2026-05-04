from django.shortcuts import render, get_object_or_404
from .models import Project, Skill


def project_list(request):
    projects = Project.objects.all()
    skills_by_category = {}
    for skill in Skill.objects.all():
        label = skill.get_category_display()
        if label not in skills_by_category:
            skills_by_category[label] = []
        skills_by_category[label].append(skill)

    return render(request, 'portfolio/project_list.html', {
        'projects': projects,
        'skills_by_category': skills_by_category,
    })


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related = Project.objects.exclude(pk=project.pk).order_by('-featured', 'order')[:3]

    return render(request, 'portfolio/project_detail.html', {
        'project': project,
        'related_projects': related,
    })

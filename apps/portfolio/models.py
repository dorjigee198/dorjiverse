from django.db import models
from django.utils.text import slugify


class Skill(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('devops', 'DevOps'),
        ('tools', 'Tools'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    icon = models.ImageField(
        upload_to='skills/', blank=True, null=True,
        help_text='Optional skill icon/logo image.'
    )
    level = models.CharField(
        max_length=20, choices=LEVEL_CHOICES, default='intermediate'
    )
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='other'
    )
    order = models.PositiveIntegerField(
        default=0, help_text='Lower numbers appear first.'
    )

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def level_percentage(self):
        return {
            'beginner': 25,
            'intermediate': 55,
            'advanced': 80,
            'expert': 95,
        }.get(self.level, 55)


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(
        max_length=300, blank=True,
        help_text='One-line summary shown on the project card. Auto-generated if blank.'
    )
    image = models.ImageField(
        upload_to='projects/', blank=True, null=True,
        help_text='Main project screenshot or thumbnail.'
    )
    technologies = models.CharField(
        max_length=500,
        help_text='Comma-separated list e.g. Django, PostgreSQL, Tailwind CSS'
    )
    github_link = models.URLField(blank=True)
    live_demo_link = models.URLField(blank=True)
    featured = models.BooleanField(
        default=False,
        help_text='Featured projects appear on the homepage.'
    )
    order = models.PositiveIntegerField(
        default=0, help_text='Lower numbers appear first.'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-featured', 'order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.short_description and self.description:
            self.short_description = self.description[:250]
        super().save(*args, **kwargs)

    @property
    def tech_list(self):
        """Return technologies as a Python list."""
        return [t.strip() for t in self.technologies.split(',') if t.strip()]

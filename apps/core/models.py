from django.db import models
from django.utils import timezone


class SiteProfile(models.Model):
    """
    Your personal profile — photo, name, bio, taglines.
    Only one row should exist. Edit it from admin.
    """
    name = models.CharField(max_length=100, default='Dorji Wangchuk')
    tagline = models.CharField(
        max_length=200,
        default='Code, stories, and ideas from Dorji\'s world.',
        help_text='Short line shown under your name on the homepage.'
    )
    bio = models.TextField(
        blank=True,
        help_text='A few sentences about yourself. Shown on the homepage and about page.'
    )
    profile_picture = models.ImageField(
        upload_to='profile/',
        blank=True,
        null=True,
        help_text='Your photo — shown on the homepage hero section.'
    )
    github_url = models.URLField(blank=True, default='https://github.com/dorjiwangchuk')
    linkedin_url = models.URLField(blank=True, default='https://linkedin.com/in/dorjiwangchuk')
    email = models.EmailField(blank=True, default='dorji@dorjivers.me')

    class Meta:
        verbose_name = 'Site Profile'
        verbose_name_plural = 'Site Profile'

    def __str__(self):
        return f'Profile — {self.name}'


class ContactMessage(models.Model):
    """Stores messages sent via the public contact form."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} — {self.subject}"


class Resume(models.Model):
    """Stores the uploadable resume PDF. Only one can be active at a time."""
    title = models.CharField(max_length=100, default='Dorji Wangchuk — Resume')
    file = models.FileField(upload_to='resume/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(
        default=True,
        help_text='Only the active resume will be available for download on the site.'
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Resume'
        verbose_name_plural = 'Resumes'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Deactivate all other resumes when this one becomes active
        if self.active:
            Resume.objects.filter(active=True).exclude(pk=self.pk).update(active=False)
        super().save(*args, **kwargs)

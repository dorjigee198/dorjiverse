import re
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
    ]

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True, max_length=350)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='posts'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    featured_image = models.ImageField(
        upload_to='blog/featured/', blank=True, null=True
    )
    excerpt = models.TextField(
        max_length=500, blank=True,
        help_text='Short summary shown on listing pages. Auto-generated if left blank.'
    )
    content = models.TextField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_DRAFT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == self.STATUS_PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        if not self.excerpt and self.content:
            clean_text = re.sub(r'<[^>]+>', '', self.content)
            self.excerpt = clean_text[:300].strip()
            if len(clean_text) > 300:
                self.excerpt += '...'
        super().save(*args, **kwargs)

    @property
    def reading_time(self):
        """Estimate reading time in minutes (average 200 wpm)."""
        clean_text = re.sub(r'<[^>]+>', '', self.content)
        word_count = len(clean_text.split())
        return max(1, round(word_count / 200))


class BlogImage(models.Model):
    """Additional images that can be embedded in a blog post."""
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='blog/images/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for: {self.post.title}"

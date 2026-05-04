from django import forms
from .models import ContactMessage

_field_class = (
    'w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white '
    'placeholder-slate-500 focus:outline-none focus:border-indigo-500 '
    'focus:ring-1 focus:ring-indigo-500 transition duration-200'
)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': _field_class,
                'placeholder': 'Your full name',
            }),
            'email': forms.EmailInput(attrs={
                'class': _field_class,
                'placeholder': 'your@email.com',
            }),
            'subject': forms.TextInput(attrs={
                'class': _field_class,
                'placeholder': "What's this about?",
            }),
            'message': forms.Textarea(attrs={
                'class': _field_class,
                'placeholder': 'Write your message here...',
                'rows': 6,
            }),
        }

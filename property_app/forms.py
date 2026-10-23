from django import forms
from django.utils import timezone
from .models import BookingInquiry, CondoUnit


class BookingInquiryForm(forms.ModelForm):
    preferred_unit = forms.ModelChoiceField(
        queryset=CondoUnit.objects.filter(is_available=True),
        required=False,
        empty_label="Any Available Suite (Best Recommendation)",
        widget=forms.Select(attrs={
            'class': 'w-full bg-white border border-stone-200 rounded-xl px-4 py-3 text-sm text-stone-900 focus:outline-none focus:border-stone-900 focus:ring-1 focus:ring-stone-900 transition-colors',
            'id': 'inquiry-preferred-unit'
        })
    )

    class Meta:
        model = BookingInquiry
        fields = [
            'guest_name', 
            'guest_phone', 
            'guest_email', 
            'check_in_date', 
            'check_out_date', 
            'number_of_guests', 
            'preferred_unit', 
            'special_notes'
        ]
        widgets = {
            'guest_name': forms.TextInput(attrs={
                'class': 'w-full bg-white border border-stone-200 rounded-xl px-4 py-3 text-sm text-stone-900 placeholder-stone-400 focus:outline-none focus:border-stone-900 focus:ring-1 focus:ring-stone-900 transition-colors',
                'placeholder': 'Your Full Name (e.g. John Doe)',
                'required': True
            }),
            'guest_phone': forms.TextInput(attrs={
                'class': 'w-full bg-white border border-stone-200 rounded-xl px-4 py-3 text-sm text-stone-900 placeholder-stone-400 focus:outline-none focus:border-stone-900 focus:ring-1 focus:ring-stone-900 transition-colors',
                'placeholder': 'Phone or WhatsApp Number (with country code)',
                'required': True
            }),
            'guest_email': forms.EmailInput(attrs={
                'class': 'w-full bg-white border border-stone-200 rounded-xl px-4 py-3 text-sm text-stone-900 placeholder-stone-400 focus:outline-none focus:border-stone-900 focus:ring-1 focus:ring-stone-900 transition-colors',
                'placeholder': 'Email address (optional)'
            }),
            'check_in_date': forms.DateInput(attrs={
                'class': 'w-full bg-white border border-stone-200 rounded-xl px-4 py-3 text-sm text-stone-900 focus:outline-none focus:border-stone-900 focus:ring-1 focus:ring-stone-900 transition-colors',
                'type': 'date',
                'required': True
            }),
            'check_out_date': forms.DateInput(attrs={
                'class': 'w-full bg-white border border-stone-200 rounded-xl px-4 py-3 text-sm text-stone-900 focus:outline-none focus:border-stone-900 focus:ring-1 focus:ring-stone-900 transition-colors',
                'type': 'date',
                'required': True
            }),
            'number_of_guests': forms.NumberInput(attrs={
                'class': 'w-full bg-white border border-stone-200 rounded-xl px-4 py-3 text-sm text-stone-900 focus:outline-none focus:border-stone-900 focus:ring-1 focus:ring-stone-900 transition-colors',
                'min': '1',
                'max': '10',
                'value': '2',
                'required': True
            }),
            'special_notes': forms.Textarea(attrs={
                'class': 'w-full bg-white border border-stone-200 rounded-xl px-4 py-3 text-sm text-stone-900 placeholder-stone-400 focus:outline-none focus:border-stone-900 focus:ring-1 focus:ring-stone-900 transition-colors resize-none',
                'rows': 2,
                'placeholder': 'Flight arrival time, late check-in request, extra pillows, or questions...'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')

        if check_in and check_out:
            today = timezone.localdate()
            if check_in < today:
                self.add_error('check_in_date', 'Check-in date cannot be in the past.')
            if check_out <= check_in:
                self.add_error('check_out_date', 'Check-out date must be after check-in date.')

        return cleaned_data

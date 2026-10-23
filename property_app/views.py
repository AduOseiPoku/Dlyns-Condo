from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from urllib.parse import quote
from .models import CondoUnit, Amenity, BookingInquiry, PropertySetting
from .forms import BookingInquiryForm


def home_view(request):
    """
    Main landing page showcasing suites, amenities, photo gallery, and reservation form.
    """
    settings = PropertySetting.get_settings()
    suites = CondoUnit.objects.filter(is_available=True).prefetch_related('amenities', 'gallery_images')
    amenities = Amenity.objects.filter(is_featured=True)
    form = BookingInquiryForm()

    context = {
        'suites': suites,
        'amenities': amenities,
        'form': form,
        'property': settings,
    }
    return render(request, 'home.html', context)


def suite_detail_view(request, slug):
    """
    Detailed showcase for an individual condo unit.
    """
    suite = get_object_or_404(CondoUnit, slug=slug, is_available=True)
    all_suites = CondoUnit.objects.filter(is_available=True).exclude(id=suite.id)[:3]
    form = BookingInquiryForm(initial={'preferred_unit': suite})

    context = {
        'suite': suite,
        'other_suites': all_suites,
        'form': form,
    }
    return render(request, 'suite_detail.html', context)


def inquiry_submit_view(request):
    """
    Processes the 'Request a Stay' form via AJAX or standard POST.
    """
    if request.method != 'POST':
        return redirect('home')

    form = BookingInquiryForm(request.POST)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json'

    if form.is_valid():
        inquiry = form.save()

        # You can add email notification dispatch here if desired
        success_message = (
            f"Thank you, {inquiry.guest_name}! Your stay request has been received. "
            f"Our reservations team will call you at {inquiry.guest_phone} shortly to confirm availability."
        )

        if is_ajax:
            return JsonResponse({
                'success': True,
                'message': success_message,
                'inquiry_id': inquiry.id,
            })
        
        messages.success(request, success_message)
        return redirect('home')
    else:
        if is_ajax:
            errors = {field: [str(err) for err in err_list] for field, err_list in form.errors.items()}
            return JsonResponse({
                'success': False,
                'errors': errors,
                'message': 'Please correct the highlighted fields.'
            }, status=400)

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field.replace('_', ' ').capitalize()}: {error}")
        return redirect('home')


def quick_whatsapp_redirect(request):
    """
    Generates a pre-filled WhatsApp message URL from query parameters.
    """
    settings = PropertySetting.get_settings()
    phone = settings.whatsapp_number.replace('+', '').replace(' ', '').replace('-', '')
    
    suite_name = request.GET.get('suite', 'a suite')
    check_in = request.GET.get('check_in', 'upcoming dates')
    check_out = request.GET.get('check_out', '')
    guests = request.GET.get('guests', '2')

    date_str = f"from {check_in} to {check_out}" if check_out else f"for {check_in}"
    text = (
        f"Hello {settings.name}, I would like to inquire about reserving {suite_name} "
        f"{date_str} for {guests} guest(s). Is this available?"
    )
    encoded_text = quote(text)
    return redirect(f"https://wa.me/{phone}?text={encoded_text}")


def health_check_view(request):
    """
    Lightweight health check endpoint for Dokploy / Docker health checks.
    """
    return JsonResponse({"status": "ok", "app": "dlyns_condo"})

from django.db import models
from django.utils.text import slugify


class PropertySetting(models.Model):
    """
    Singleton model to manage global condo hotel settings and contact info.
    """
    name = models.CharField(max_length=150, default="Dlyns Condo")
    tagline = models.CharField(
        max_length=255, 
        default="Modern Comfort, Prime Location & Unmatched Hospitality"
    )
    phone_number = models.CharField(max_length=50, default="+1 (555) 019-2834")
    whatsapp_number = models.CharField(
        max_length=50, 
        default="15550192834",
        help_text="Format with country code without spaces or symbols (e.g. 15550192834)"
    )
    email = models.EmailField(default="reservations@dlynscondo.com")
    address = models.CharField(max_length=255, default="Apenkwa")
    city = models.CharField(max_length=100, default="Koforidua, Eastern Region")
    check_in_time = models.CharField(max_length=50, default="3:00 PM")
    check_out_time = models.CharField(max_length=50, default="11:00 AM")
    hero_title = models.CharField(
        max_length=200, 
        default="Tranquil Living, Mountain Vistas & Personalized Hospitality"
    )
    hero_subtitle = models.TextField(
        default="Handcrafted living spaces in scenic Koforidua-Apenkwa featuring breathtaking views, 24/7 dedicated concierge, and bespoke comfort. Call or WhatsApp our reservation desk to secure your dates directly."
    )
    hero_image = models.URLField(
        default="https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1920&q=80"
    )

    class Meta:
        verbose_name = "Property Setting"
        verbose_name_plural = "Property Settings"

    def __str__(self):
        return self.name

    @classmethod
    def get_settings(cls):
        settings, created = cls.objects.get_or_create(id=1)
        return settings


class Amenity(models.Model):
    CATEGORY_CHOICES = [
        ("IN_ROOM", "In-Suite Comfort"),
        ("BUILDING", "Building & Services"),
        ("WELLNESS", "Wellness & Leisure"),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="IN_ROOM")
    icon_name = models.CharField(
        max_length=50, 
        default="wifi", 
        help_text="Name of icon (e.g. wifi, pool, tv, snowflake, shield, car, coffee, bed)"
    )
    description = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Amenities"
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class CondoUnit(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    unit_type = models.CharField(
        max_length=100, 
        help_text="e.g. 1-Bedroom Suite, Executive Penthouse"
    )
    badge = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Optional badge e.g. 'Most Popular', 'Best Mountain View'"
    )
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    nightly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    max_guests = models.PositiveIntegerField(default=2)
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    size_sqm = models.PositiveIntegerField(default=55, help_text="Size in square meters")
    cover_image = models.URLField(
        default="https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80"
    )
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="condos")
    is_featured = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "nightly_rate"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} (GH₵{self.nightly_rate}/night)"


class UnitGalleryImage(models.Model):
    unit = models.ForeignKey(CondoUnit, on_delete=models.CASCADE, related_name="gallery_images")
    image_url = models.URLField()
    caption = models.CharField(max_length=150, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Gallery image for {self.unit.title} ({self.caption or 'Photo'})"


class BookingInquiry(models.Model):
    STATUS_CHOICES = [
        ("NEW", "🟡 New Lead (Call Pending)"),
        ("CALLED", "🔵 Host Called / In Contact"),
        ("CONFIRMED", "🟢 Reservation Confirmed"),
        ("CANCELLED", "⚪ Cancelled / Unavailable"),
        ("COMPLETED", "🟣 Stay Completed"),
    ]

    guest_name = models.CharField(max_length=150, verbose_name="Guest Name")
    guest_phone = models.CharField(max_length=50, verbose_name="Phone / WhatsApp")
    guest_email = models.EmailField(blank=True, verbose_name="Guest Email")
    check_in_date = models.DateField(verbose_name="Check-in Date")
    check_out_date = models.DateField(verbose_name="Check-out Date")
    number_of_guests = models.PositiveIntegerField(default=2, verbose_name="Guests")
    preferred_unit = models.ForeignKey(
        CondoUnit, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="inquiries"
    )
    special_notes = models.TextField(blank=True, verbose_name="Notes / Requests")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NEW")
    admin_notes = models.TextField(
        blank=True, 
        help_text="Internal notes about phone conversations, negotiated rates, deposit arrangements, etc."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reservation Inquiry"
        verbose_name_plural = "Reservation Inquiries"
        ordering = ["-created_at"]

    def __str__(self):
        unit_name = self.preferred_unit.title if self.preferred_unit else "Any Suite"
        return f"{self.guest_name} - {unit_name} ({self.check_in_date} to {self.check_out_date})"

    @property
    def nights_count(self):
        if self.check_in_date and self.check_out_date:
            delta = self.check_out_date - self.check_in_date
            return max(delta.days, 1)
        return 1

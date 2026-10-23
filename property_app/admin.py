from django.contrib import admin
from django.utils.html import format_html
from .models import PropertySetting, Amenity, CondoUnit, UnitGalleryImage, BookingInquiry


@admin.register(PropertySetting)
class PropertySettingAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Branding & Hotel Info", {
            "fields": ("name", "tagline", "hero_title", "hero_subtitle", "hero_image")
        }),
        ("Direct Booking Contacts (Call-to-Book)", {
            "fields": ("phone_number", "whatsapp_number", "email", "address", "city")
        }),
        ("Check-In & Stay Times", {
            "fields": ("check_in_time", "check_out_time")
        }),
    )

    def has_add_permission(self, request):
        # Prevent creating multiple setting instances
        if PropertySetting.objects.exists():
            return False
        return super().has_add_permission(request)


class UnitGalleryImageInline(admin.TabularInline):
    model = UnitGalleryImage
    extra = 2
    fields = ("image_url", "caption", "order")


@admin.register(CondoUnit)
class CondoUnitAdmin(admin.ModelAdmin):
    list_display = ("title", "unit_type", "nightly_rate", "max_guests", "bedrooms", "bathrooms", "is_available", "is_featured", "order")
    list_filter = ("is_available", "is_featured", "unit_type")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("amenities",)
    inlines = [UnitGalleryImageInline]


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "icon_name", "is_featured")
    list_filter = ("category", "is_featured")
    search_fields = ("name", "description")


@admin.register(BookingInquiry)
class BookingInquiryAdmin(admin.ModelAdmin):
    list_display = (
        "guest_name", 
        "quick_call_link", 
        "quick_whatsapp_link", 
        "stay_dates", 
        "number_of_guests", 
        "preferred_unit", 
        "colored_status", 
        "created_at"
    )
    list_filter = ("status", "check_in_date", "preferred_unit")
    search_fields = ("guest_name", "guest_phone", "guest_email", "admin_notes", "special_notes")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "check_in_date"
    actions = ["mark_as_called", "mark_as_confirmed", "mark_as_cancelled"]

    fieldsets = (
        ("Guest & Contact Info", {
            "fields": ("guest_name", "guest_phone", "guest_email")
        }),
        ("Stay Details", {
            "fields": ("preferred_unit", "check_in_date", "check_out_date", "number_of_guests", "special_notes")
        }),
        ("Reservation Management", {
            "fields": ("status", "admin_notes", "created_at", "updated_at")
        }),
    )

    def quick_call_link(self, obj):
        clean_phone = obj.guest_phone.replace(" ", "").replace("-", "")
        return format_html(
            '<a href="tel:{}" class="button" style="background:#0284c7; color:white; padding:3px 8px; border-radius:5px; text-decoration:none; font-weight:bold;">📞 Call</a> {}',
            clean_phone,
            obj.guest_phone
        )
    quick_call_link.short_description = "Direct Call"

    def quick_whatsapp_link(self, obj):
        clean_phone = obj.guest_phone.replace("+", "").replace(" ", "").replace("-", "")
        unit_name = obj.preferred_unit.title if obj.preferred_unit else "our suites"
        msg = f"Hello {obj.guest_name}, this is Dlyns Condo reservations following up regarding your inquiry for {unit_name}."
        return format_html(
            '<a href="https://wa.me/{}?text={}" target="_blank" style="background:#16a34a; color:white; padding:3px 8px; border-radius:5px; text-decoration:none; font-weight:bold;">💬 Chat</a>',
            clean_phone,
            msg
        )
    quick_whatsapp_link.short_description = "WhatsApp"

    def stay_dates(self, obj):
        return f"{obj.check_in_date.strftime('%b %d')} → {obj.check_out_date.strftime('%b %d, %Y')} ({obj.nights_count} nights)"
    stay_dates.short_description = "Dates & Duration"

    def colored_status(self, obj):
        colors = {
            "NEW": ("#fef3c7", "#b45309", "🟡 NEW LEAD"),
            "CALLED": ("#e0f2fe", "#0369a1", "🔵 CALLED / CONTACTED"),
            "CONFIRMED": ("#dcfce7", "#15803d", "🟢 CONFIRMED"),
            "CANCELLED": ("#f1f5f9", "#64748b", "⚪ CANCELLED"),
            "COMPLETED": ("#f3e8ff", "#7e22ce", "🟣 COMPLETED"),
        }
        bg, text_col, label = colors.get(obj.status, ("#f1f5f9", "#334155", obj.status))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 4px 10px; border-radius: 9999px; font-weight: bold; font-size: 11px;">{}</span>',
            bg, text_col, label
        )
    colored_status.short_description = "Status"

    @admin.action(description="Mark selected leads as 'Called / In Contact'")
    def mark_as_called(self, request, queryset):
        queryset.update(status="CALLED")

    @admin.action(description="Mark selected leads as 'Reservation Confirmed'")
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status="CONFIRMED")

    @admin.action(description="Mark selected leads as 'Cancelled'")
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status="CANCELLED")

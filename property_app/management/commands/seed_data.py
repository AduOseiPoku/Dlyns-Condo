from django.core.management.base import BaseCommand
from datetime import date, timedelta
from property_app.models import PropertySetting, Amenity, CondoUnit, UnitGalleryImage, BookingInquiry


class Command(BaseCommand):
    help = "Seeds initial luxury condo suites, amenities, gallery images, and sample inquiry leads"

    def handle(self, *args, **options):
        self.stdout.write("Seeding Dlyns Condo database...")

        # 1. Property Settings
        prop, _ = PropertySetting.objects.get_or_create(id=1)
        prop.name = "Dlyns Condo"
        prop.tagline = "Modern Luxury, Hillside Serenity & Personalized Hospitality"
        prop.phone_number = "+233 (0) 55 000 0000"
        prop.whatsapp_number = "233550000000"
        prop.email = "reservations@dlynscondo.com"
        prop.address = "Apenkwa"
        prop.city = "Koforidua, Eastern Region"
        prop.check_in_time = "3:00 PM"
        prop.check_out_time = "11:00 AM"
        prop.hero_title = "Tranquil Living, Mountain Vistas & Personalized Hospitality"
        prop.hero_subtitle = (
            "Experience refined serviced accommodations in the peaceful hills of Koforidua-Apenkwa. "
            "Direct host booking with zero middleman fees. Call or message us on WhatsApp to secure your stay."
        )
        prop.hero_image = "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1920&q=80"
        prop.save()

        # 2. Amenities
        amenities_data = [
            ("Rooftop Terrace & Lounge", "WELLNESS", "sun", "Panoramic mountain and hillside skyline views"),
            ("High-Speed Fiber Wi-Fi", "IN_ROOM", "wifi", "Dedicated high-speed fiber line for remote work"),
            ("Split Air Conditioning", "IN_ROOM", "snowflake", "Quiet multi-zone climate control"),
            ("24/7 Monitored Security", "BUILDING", "shield", "Gated access, CCTV & on-site security"),
            ("Free Secure Parking", "BUILDING", "car", "Dedicated reserved space per suite"),
            ("Chef-Grade Kitchen", "IN_ROOM", "kitchen", "Cooktop, espresso maker, microwave & cookware"),
            ("Smart 4K TV & Sound", "IN_ROOM", "tv", "Netflix, YouTube & streaming ready"),
            ("Private Balcony", "IN_ROOM", "sun", "Outdoor seating with peaceful hill and garden views"),
        ]

        amenity_objs = {}
        for name, category, icon_name, desc in amenities_data:
            am, _ = Amenity.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "icon_name": icon_name,
                    "description": desc,
                    "is_featured": True,
                }
            )
            amenity_objs[name] = am

        # 3. Suites / Condos - Clear old demo units to keep database pristine
        CondoUnit.objects.all().delete()

        suites_data = [
            {
                "title": "Deluxe Mountain-View Suite",
                "unit_type": "1-Bedroom Suite",
                "badge": "Scenic Hill Views",
                "short_description": "A stylish hillside sanctuary featuring panoramic views of Obuo Tabri, plush queen bedding, workstation, and a private balcony.",
                "description": (
                    "Designed with refined modern aesthetics, the Deluxe Mountain-View Suite features an open-concept living area, "
                    "a plush queen-sized bed with Egyptian cotton linens, a dedicated executive workspace with high-speed fiber Wi-Fi, and a spa-style bathroom.\n\n"
                    "Enjoy morning coffee on your private balcony savoring the cool Koforidua mountain air, or unwind after exploring the Eastern Region with your 55\" Smart 4K TV."
                ),
                "nightly_rate": 95.00,
                "max_guests": 2,
                "bedrooms": 1,
                "bathrooms": 1,
                "size_sqm": 48,
                "cover_image": "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=1200&q=80",
                "order": 1,
                "gallery": [
                    ("https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1000&q=80", "Living Area"),
                    ("https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=1000&q=80", "Designer Bathroom"),
                    ("https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=1000&q=80", "Kitchenette"),
                ]
            },
            {
                "title": "Executive Apenkwa Residence",
                "unit_type": "2-Bedroom Deluxe",
                "badge": "Most Popular",
                "short_description": "Generously proportioned 2-bedroom residence featuring a full chef kitchen, expansive dining room, and peaceful private terrace.",
                "description": (
                    "The Executive Apenkwa Residence is our most requested accommodation for families, executive travelers, and weekend getaways. Spanning 85 square meters, it provides two private master bedrooms, "
                    "two en-suite bathrooms, an elegant dining space, and a chef-grade kitchen outfitted with modern appliances.\n\n"
                    "Step onto the expansive terrace for tranquil sunset views across the Eastern Region hills. Perfect for staycations, business retreats, and family holidays."
                ),
                "nightly_rate": 165.00,
                "max_guests": 4,
                "bedrooms": 2,
                "bathrooms": 2,
                "size_sqm": 85,
                "cover_image": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1200&q=80",
                "order": 2,
                "gallery": [
                    ("https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1000&q=80", "Main Bedroom"),
                    ("https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=1000&q=80", "Chef Kitchen"),
                    ("https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1000&q=80", "Terrace Lounge"),
                ]
            },
            {
                "title": "Skyline Hilltop Penthouse",
                "unit_type": "3-Bedroom Penthouse",
                "badge": "Top Mountain View",
                "short_description": "Our crowning residence with 360-degree top-floor views of the Koforidua ridges, private terrace jacuzzi, custom wet bar, and master suite.",
                "description": (
                    "Occupying the top floor of Dlyns Condo, the Skyline Hilltop Penthouse represents the pinnacle of serenity and hospitality in Koforidua. "
                    "Features include soaring ceilings, three plush master suites, a designer kitchen, and private rooftop jacuzzi overlooking the lush green ridges of the Akwapim-Togo range.\n\n"
                    "Includes VIP concierge service, priority housekeeping, and two reserved secure parking spaces."
                ),
                "nightly_rate": 250.00,
                "max_guests": 6,
                "bedrooms": 3,
                "bathrooms": 3,
                "size_sqm": 135,
                "cover_image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80",
                "order": 3,
                "gallery": [
                    ("https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1000&q=80", "Penthouse View"),
                    ("https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=1000&q=80", "Master En-Suite"),
                    ("https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?auto=format&fit=crop&w=1000&q=80", "Private Jacuzzi"),
                ]
            },
        ]

        created_suites = []
        for s_data in suites_data:
            gallery = s_data.pop("gallery")
            suite, created = CondoUnit.objects.get_or_create(
                title=s_data["title"],
                defaults=s_data
            )
            # Add all amenities
            suite.amenities.set(amenity_objs.values())
            suite.save()
            created_suites.append(suite)

            # Add gallery images
            for order, (img_url, cap) in enumerate(gallery):
                UnitGalleryImage.objects.get_or_create(
                    unit=suite,
                    image_url=img_url,
                    defaults={"caption": cap, "order": order}
                )

        # 4. Sample Booking Inquiries to demo the admin lead manager
        today = date.today()
        sample_inquiries = [
            {
                "guest_name": "Marcus Vance",
                "guest_phone": "+1 555-234-8901",
                "guest_email": "marcus.v@example.com",
                "check_in_date": today + timedelta(days=3),
                "check_out_date": today + timedelta(days=7),
                "number_of_guests": 2,
                "preferred_unit": created_suites[1],
                "special_notes": "Celebrating anniversary. Would appreciate a quiet high floor.",
                "status": "NEW",
                "admin_notes": "Needs immediate callback. Guest is interested in 4 nights."
            },
            {
                "guest_name": "Elena Rostova",
                "guest_phone": "+1 555-891-4432",
                "guest_email": "elena.r@example.com",
                "check_in_date": today + timedelta(days=10),
                "check_out_date": today + timedelta(days=14),
                "number_of_guests": 4,
                "preferred_unit": created_suites[0],
                "special_notes": "Arriving on 6 PM flight. Late check-in required.",
                "status": "CALLED",
                "admin_notes": "Called Elena on WhatsApp. Confirmed arrival time, sent location pin."
            }
        ]

        for inq_data in sample_inquiries:
            BookingInquiry.objects.get_or_create(
                guest_name=inq_data["guest_name"],
                check_in_date=inq_data["check_in_date"],
                defaults=inq_data
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded Dlyns Condo demo data!"))

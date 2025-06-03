from django.core.management.base import BaseCommand
from restaurant.models import Booking
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Populate the database with sample bookings'

    def handle(self, *args, **options):
        # Clear existing bookings
        Booking.objects.all().delete()
        
        # Create sample bookings for the next few days
        today = date.today()
        
        sample_bookings = [
            {
                'first_name': 'John Smith',
                'reservation_date': today + timedelta(days=1),
                'reservation_slot': 18
            },
            {
                'first_name': 'Mary Johnson',
                'reservation_date': today + timedelta(days=1),
                'reservation_slot': 19
            },
            {
                'first_name': 'David Wilson',
                'reservation_date': today + timedelta(days=2),
                'reservation_slot': 17
            },
            {
                'first_name': 'Sarah Davis',
                'reservation_date': today + timedelta(days=2),
                'reservation_slot': 20
            },
            {
                'first_name': 'Michael Brown',
                'reservation_date': today + timedelta(days=3),
                'reservation_slot': 18
            }
        ]
        
        for booking_data in sample_bookings:
            Booking.objects.create(**booking_data)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created booking for: {booking_data["first_name"]} '
                    f'on {booking_data["reservation_date"]} at {booking_data["reservation_slot"]}:00'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(sample_bookings)} sample bookings')
        )

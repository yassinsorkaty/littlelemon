from django.core.management.base import BaseCommand
from restaurant.models import Menu


class Command(BaseCommand):
    help = 'Populate the database with sample menu items'

    def handle(self, *args, **options):
        # Clear existing menu items
        Menu.objects.all().delete()
        
        # Create sample menu items
        menu_items = [
            {
                'name': 'Greek Salad',
                'price': 12,
                'menu_item_description': 'The famous greek salad of crispy lettuce, peppers, olives and our Chicago style feta cheese, garnished with crunchy garlic and rosemary croutons.'
            },
            {
                'name': 'Lemon Dessert',
                'price': 5,
                'menu_item_description': 'Traditional homemade Italian Lemon Ricotta Cake.'
            },
            {
                'name': 'Grilled Fish',
                'price': 20,
                'menu_item_description': 'Our Bruschetta is made from grilled bread that has been smeared with garlic and seasoned with salt and olive oil.'
            },
            {
                'name': 'Pasta',
                'price': 18,
                'menu_item_description': 'Penne with fried aubergines, cherry tomatoes, tomato sauce, fresh chili, garlic, basil & salted ricotta cheese.'
            },
            {
                'name': 'Bruschetta',
                'price': 8,
                'menu_item_description': 'Our Bruschetta is made from grilled bread that has been smeared with garlic and seasoned with salt and olive oil.'
            }
        ]
          for item_data in menu_items:
            Menu.objects.create(**item_data)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created menu item: {item_data["name"]}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully populated {len(menu_items)} menu items')
        )

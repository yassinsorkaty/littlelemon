#!/usr/bin/env python
"""
Little Lemon Restaurant Setup Script
This script automates the initial setup of the Django project
"""
import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e.stderr.strip()}")
        return False


def main():
    """Main setup function"""
    print("=" * 70)
    print("🍋 LITTLE LEMON RESTAURANT - PROJECT SETUP")
    print("=" * 70)
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print("❌ Error: manage.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    setup_steps = [
        ("pipenv install", "Installing Python dependencies"),
        ("pipenv run python manage.py migrate", "Setting up database"),
        ("pipenv run python manage.py populate_menu", "Adding sample menu items"),
        ("pipenv run python manage.py populate_bookings", "Adding sample bookings"),
    ]
    
    print("Starting automated setup process...\n")
    
    all_success = True
    for command, description in setup_steps:
        if not run_command(command, description):
            all_success = False
            break
    
    if all_success:
        print("\n" + "=" * 70)
        print("🎉 SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Create a superuser: pipenv run python manage.py createsuperuser")
        print("2. Run the server: pipenv run python manage.py runserver")
        print("3. Visit: http://localhost:8000/restaurant/")
        print("4. Admin panel: http://localhost:8000/admin/")
        print("5. API endpoints: http://localhost:8000/restaurant/api/")
        print("\nFor testing:")
        print("• Run tests: pipenv run python manage.py test tests")
        print("• Custom test runner: pipenv run python run_tests.py")
        print("\nAPI Testing with Insomnia:")
        print("• Register: POST /auth/users/")
        print("• Login: POST /auth/token/login/")
        print("• Menu API: /restaurant/api/menu-items/")
        print("• Booking API: /restaurant/api/tables/")
    else:
        print("\n❌ Setup failed. Please check the errors above and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
Comprehensive test runner for Little Lemon Restaurant Project
This script runs all tests and provides detailed reporting
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner


def run_tests():
    """Run all tests with comprehensive reporting"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'littlelemon.settings')
    django.setup()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=True)
    
    print("=" * 70)
    print("LITTLE LEMON RESTAURANT - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    
    # Test categories
    test_modules = [
        'tests.test_models',
        'tests.test_views', 
        'tests.test_static_templates',
        'tests.test_integration'
    ]
    
    all_passed = True
    
    for module in test_modules:
        print(f"\n{'-' * 50}")
        print(f"Running {module.replace('tests.test_', '').upper()} TESTS")
        print(f"{'-' * 50}")
        
        failures = test_runner.run_tests([module])
        if failures:
            all_passed = False
            print(f"❌ {module} had {failures} failure(s)")
        else:
            print(f"✅ {module} passed all tests")
    
    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Your Little Lemon app is working perfectly!")
    else:
        print("⚠️  Some tests failed. Please review the output above.")
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(run_tests())

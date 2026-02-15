#!/usr/bin/env python3
"""
Verify NEWCO system setup
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def check_directory_structure():
    """Check if all required directories exist"""
    required_dirs = [
        'data',
        'templates/email',
        'templates/meeting',
        'templates/follow_up',
        'scripts',
        'config',
        'docs',
        'reports/weekly'
    ]

    print("Checking directory structure...")
    all_good = True
    for dir_path in required_dirs:
        full_path = BASE_DIR / dir_path
        if full_path.exists():
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ✗ {dir_path} - MISSING")
            all_good = False

    return all_good

def check_config_files():
    """Check if configuration files exist"""
    required_files = [
        'config/config.yaml',
        'config/personas.yaml'
    ]

    print("\nChecking configuration files...")
    all_good = True
    for file_path in required_files:
        full_path = BASE_DIR / file_path
        if full_path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING")
            all_good = False

    return all_good

def check_data_files():
    """Check if data files exist"""
    required_files = [
        'data/contacts.csv',
        'data/interactions.csv',
        'data/pipeline.csv',
        'data/targets.csv'
    ]

    print("\nChecking data files...")
    all_good = True
    for file_path in required_files:
        full_path = BASE_DIR / file_path
        if full_path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING")
            all_good = False

    return all_good

def check_templates():
    """Check if email templates exist"""
    required_templates = [
        'templates/email/platform_gatekeeper.md',
        'templates/email/family_office_cio.md',
        'templates/email/vc_partner.md',
        'templates/email/foundation_leader.md',
        'templates/email/network_multiplier.md'
    ]

    print("\nChecking email templates...")
    all_good = True
    for file_path in required_templates:
        full_path = BASE_DIR / file_path
        if full_path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING")
            all_good = False

    return all_good

def check_scripts():
    """Check if core scripts exist"""
    required_scripts = [
        'scripts/newco_cli.py',
        'scripts/email_generator.py',
        'scripts/pipeline_manager.py',
        'scripts/reports.py',
        'scripts/automation.py'
    ]

    print("\nChecking core scripts...")
    all_good = True
    for file_path in required_scripts:
        full_path = BASE_DIR / file_path
        if full_path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING")
            all_good = False

    return all_good

def check_docs():
    """Check if documentation exists"""
    required_docs = [
        'docs/PLAYBOOK.md',
        'docs/90_Day_Plan.md',
        'docs/NEWCO_One_Pager.md',
        'README.md'
    ]

    print("\nChecking documentation...")
    all_good = True
    for file_path in required_docs:
        full_path = BASE_DIR / file_path
        if full_path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING")
            all_good = False

    return all_good

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\nChecking Python dependencies...")

    try:
        import yaml
        print("  ✓ pyyaml installed")
        return True
    except ImportError:
        print("  ✗ pyyaml - NOT INSTALLED")
        print("    Run: pip install -r requirements.txt")
        return False

def main():
    """Main verification"""
    print("="*60)
    print("NEWCO System Verification")
    print("="*60)
    print()

    checks = [
        check_directory_structure(),
        check_config_files(),
        check_data_files(),
        check_templates(),
        check_scripts(),
        check_docs(),
        check_dependencies()
    ]

    print("\n" + "="*60)
    if all(checks):
        print("✓ ALL CHECKS PASSED")
        print("="*60)
        print("\nYour NEWCO system is properly set up!")
        print("\nNext steps:")
        print("  1. Import contacts: ./scripts/import_contacts.py")
        print("  2. View dashboard: ./scripts/newco_cli.py report dashboard")
        print("  3. Read playbook: cat docs/PLAYBOOK.md")
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        print("="*60)
        print("\nPlease fix the missing files/directories above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

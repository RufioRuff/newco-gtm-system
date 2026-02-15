#!/usr/bin/env python3
"""
NEWCO Integration Validation Script

Comprehensive validation of all system components:
- Python dependencies
- LinkedIn scraping infrastructure
- Network analysis engine
- CLI functionality
- Data files and directories
- Documentation
"""

import sys
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
END = '\033[0m'


class ValidationReport:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []

    def add_pass(self, test: str, detail: str = ""):
        self.passed.append((test, detail))
        print(f"{GREEN}✅ {test}{END}")
        if detail:
            print(f"   {detail}")

    def add_fail(self, test: str, detail: str = ""):
        self.failed.append((test, detail))
        print(f"{RED}❌ {test}{END}")
        if detail:
            print(f"   {detail}")

    def add_warning(self, test: str, detail: str = ""):
        self.warnings.append((test, detail))
        print(f"{YELLOW}⚠️  {test}{END}")
        if detail:
            print(f"   {detail}")

    def summary(self):
        print(f"\n{BOLD}{'='*70}{END}")
        print(f"{BOLD}VALIDATION SUMMARY{END}")
        print(f"{'='*70}")
        print(f"{GREEN}✅ Passed: {len(self.passed)}{END}")
        print(f"{YELLOW}⚠️  Warnings: {len(self.warnings)}{END}")
        print(f"{RED}❌ Failed: {len(self.failed)}{END}")

        if len(self.failed) == 0:
            print(f"\n{GREEN}{BOLD}🎉 ALL VALIDATIONS PASSED!{END}")
            print(f"{GREEN}System is ready to execute.{END}")
            return True
        else:
            print(f"\n{RED}{BOLD}⚠️  SOME VALIDATIONS FAILED{END}")
            print(f"\n{RED}Failed checks:{END}")
            for test, detail in self.failed:
                print(f"  • {test}")
                if detail:
                    print(f"    {detail}")
            return False


def check_python_version(report: ValidationReport):
    """Check Python version is 3.10+"""
    if sys.version_info >= (3, 10):
        report.add_pass(f"Python {sys.version.split()[0]}")
    else:
        report.add_fail(f"Python version too old: {sys.version.split()[0]}",
                       "Requires Python 3.10+")


def check_python_dependencies(report: ValidationReport):
    """Check all required Python packages"""
    required_packages = {
        'yaml': 'pyyaml',
        'playwright': 'playwright',
        'bs4': 'beautifulsoup4',
        'lxml': 'lxml',
    }

    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            report.add_pass(f"Python package: {package_name}")
        except ImportError:
            report.add_fail(f"Python package: {package_name}",
                           f"Install with: pip install {package_name}")


def check_playwright_browsers(report: ValidationReport):
    """Check if Playwright browsers are installed"""
    try:
        result = subprocess.run(
            ['playwright', 'install', '--dry-run'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if 'chromium' in result.stdout.lower() or result.returncode == 0:
            report.add_pass("Playwright browsers (chromium)")
        else:
            report.add_warning("Playwright browsers",
                             "Run: playwright install chromium")
    except Exception as e:
        report.add_warning("Playwright browser check",
                          "Unable to verify: run 'playwright install chromium'")


def check_directories(report: ValidationReport):
    """Check all required directories exist"""
    base_path = Path.cwd()
    required_dirs = [
        'scripts',
        'data',
        'data/linkedin_networks',
        'data/linkedin_cache',
        'templates',
        'templates/email',
        'docs',
        'reports',
        'newco-unified-platform',
    ]

    for dir_path in required_dirs:
        full_path = base_path / dir_path
        if full_path.exists():
            report.add_pass(f"Directory: {dir_path}")
        else:
            report.add_warning(f"Directory: {dir_path}",
                             f"Creating: {full_path}")
            full_path.mkdir(parents=True, exist_ok=True)


def check_data_files(report: ValidationReport):
    """Check critical data files"""
    base_path = Path.cwd()
    data_files = {
        'data/contacts.csv': False,  # Optional
        'data/relationships.csv': False,
        'data/interactions.csv': False,
    }

    for file_path, required in data_files.items():
        full_path = base_path / file_path
        if full_path.exists():
            # Check if file has content
            if full_path.stat().st_size > 100:
                report.add_pass(f"Data file: {file_path}")
            else:
                report.add_warning(f"Data file: {file_path}", "File is empty")
        elif required:
            report.add_fail(f"Data file: {file_path}", "Required file missing")
        else:
            report.add_warning(f"Data file: {file_path}", "Will be created when needed")


def check_python_scripts(report: ValidationReport):
    """Check all Python scripts can be imported"""
    sys.path.insert(0, 'scripts')

    scripts_to_test = [
        ('linkedin_scraper', 'LinkedInScraper'),
        ('linkedin_network_crawler', 'LinkedInNetworkCrawler'),
        ('import_linkedin_network', 'LinkedInNetworkImporter'),
        ('network_analysis', 'NetworkAnalysisEngine'),
        ('relationship_manager', 'RelationshipManager'),
    ]

    for module_name, class_name in scripts_to_test:
        try:
            module = __import__(module_name)
            if hasattr(module, class_name):
                report.add_pass(f"Python script: {module_name}.py")
            else:
                report.add_warning(f"Python script: {module_name}.py",
                                 f"Class {class_name} not found")
        except Exception as e:
            report.add_fail(f"Python script: {module_name}.py",
                           f"Import error: {str(e)}")


def check_cli(report: ValidationReport):
    """Check CLI functionality"""
    try:
        result = subprocess.run(
            ['python3', 'scripts/newco_cli.py', '--help'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and 'NEWCO' in result.stdout:
            report.add_pass("NEWCO CLI")
        else:
            report.add_fail("NEWCO CLI", "CLI not working properly")
    except Exception as e:
        report.add_fail("NEWCO CLI", f"Error: {str(e)}")


def check_shell_scripts(report: ValidationReport):
    """Check shell scripts are executable"""
    base_path = Path.cwd()
    scripts = [
        'scripts/run_full_network_analysis.sh',
        'EXECUTE_NOW.sh',
        'PARTNER_SETUP.sh',
    ]

    for script_path in scripts:
        full_path = base_path / script_path
        if full_path.exists():
            if os.access(full_path, os.X_OK):
                report.add_pass(f"Shell script: {script_path}")
            else:
                report.add_warning(f"Shell script: {script_path}",
                                 "Not executable, fixing...")
                full_path.chmod(0o755)
                report.add_pass(f"Fixed permissions: {script_path}")
        else:
            report.add_fail(f"Shell script: {script_path}", "File not found")


def check_documentation(report: ValidationReport):
    """Check key documentation files exist"""
    base_path = Path.cwd()
    docs = [
        'README.md',
        'LINKEDIN_NETWORK_ANALYSIS_GUIDE.md',
        'CO_FOUNDER_QUICK_START.md',
        'START_HERE.md',
        'CLAUDE.md',
        'MASTER_INTEGRATION_PLAN.md',
    ]

    for doc in docs:
        full_path = base_path / doc
        if full_path.exists():
            if full_path.stat().st_size > 1000:
                report.add_pass(f"Documentation: {doc}")
            else:
                report.add_warning(f"Documentation: {doc}", "File seems incomplete")
        else:
            report.add_warning(f"Documentation: {doc}", "File not found")


def check_unified_platform(report: ValidationReport):
    """Check unified platform setup"""
    base_path = Path.cwd() / 'newco-unified-platform'

    if not base_path.exists():
        report.add_fail("Unified Platform", "Directory not found")
        return

    # Check package.json
    package_json = base_path / 'package.json'
    if package_json.exists():
        report.add_pass("Unified Platform: package.json")
    else:
        report.add_fail("Unified Platform: package.json", "File not found")

    # Check node_modules
    node_modules = base_path / 'node_modules'
    if node_modules.exists():
        report.add_pass("Unified Platform: node_modules")
    else:
        report.add_warning("Unified Platform: node_modules",
                          "Run: cd newco-unified-platform && yarn install")

    # Check API
    api_dir = base_path / 'api'
    if api_dir.exists():
        report.add_pass("Unified Platform: API directory")
    else:
        report.add_fail("Unified Platform: API directory", "Not found")

    # Check Web
    web_dir = base_path / 'web'
    if web_dir.exists():
        report.add_pass("Unified Platform: Web directory")
    else:
        report.add_fail("Unified Platform: Web directory", "Not found")


def check_environment(report: ValidationReport):
    """Check environment variables"""

    # LinkedIn credentials (optional but recommended)
    if os.getenv('LINKEDIN_EMAIL') and os.getenv('LINKEDIN_PASSWORD'):
        report.add_pass("LinkedIn credentials set")
    else:
        report.add_warning("LinkedIn credentials not set",
                          "Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD for scraping")

    # Database (optional for now)
    if os.getenv('DATABASE_URL'):
        report.add_pass("Database URL configured")
    elif os.getenv('SUPABASE_URL'):
        report.add_pass("Supabase configured")
    else:
        report.add_warning("Database not configured",
                          "Optional: Set DATABASE_URL or SUPABASE_URL")


def main():
    print(f"{BOLD}{'='*70}{END}")
    print(f"{BOLD}NEWCO INTEGRATION VALIDATION{END}")
    print(f"{'='*70}\n")

    report = ValidationReport()

    print(f"{BLUE}{BOLD}1. Python Environment{END}")
    check_python_version(report)
    check_python_dependencies(report)
    check_playwright_browsers(report)

    print(f"\n{BLUE}{BOLD}2. File System{END}")
    check_directories(report)
    check_data_files(report)
    check_shell_scripts(report)
    check_documentation(report)

    print(f"\n{BLUE}{BOLD}3. Python Scripts{END}")
    check_python_scripts(report)
    check_cli(report)

    print(f"\n{BLUE}{BOLD}4. Unified Platform{END}")
    check_unified_platform(report)

    print(f"\n{BLUE}{BOLD}5. Environment{END}")
    check_environment(report)

    # Print summary
    success = report.summary()

    # Next steps
    if success:
        print(f"\n{BOLD}🚀 NEXT STEPS:{END}")
        print("1. Set LinkedIn credentials (optional):")
        print("   export LINKEDIN_EMAIL='your@email.com'")
        print("   export LINKEDIN_PASSWORD='yourpassword'")
        print("\n2. Run full system:")
        print("   ./EXECUTE_NOW.sh")
        print("\n3. Or run LinkedIn analysis:")
        print("   ./scripts/run_full_network_analysis.sh")

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

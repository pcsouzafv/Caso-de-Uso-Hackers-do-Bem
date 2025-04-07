import subprocess
import os

def run_test(test_file, test_name):
    print(f"\nRunning test: {test_name}")
    result = subprocess.run(
        ['python', '-m', 'pytest', test_file, '-v', '--tb=long'],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("\nError output:")
        print(result.stderr)

tests = [
    ("tests/test_app.py", "test_home_page"),
    ("tests/test_app.py", "test_login"),
    ("tests/test_models.py", "test_user_model"),
    ("tests/test_models.py", "test_task_model"),
    ("tests/test_models.py", "test_system_log_model"),
    ("tests/test_routes.py", "test_login_route"),
    ("tests/test_routes.py", "test_login_user"),
    ("tests/test_routes.py", "test_logout_route"),
    ("tests/test_routes.py", "test_add_task"),
    ("tests/test_routes.py", "test_admin_dashboard")
]

for test_file, test_name in tests:
    run_test(test_file, test_name)

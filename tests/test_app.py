# tests/test_app.py
def test_app_creation():
    from task_manager import create_app
    app = create_app()
    assert app is not None
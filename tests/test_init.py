def test_app_import():
    """Testa a importação do módulo app"""
    import app
    assert app is not None

def test_models_import():
    """Testa a importação dos modelos"""
    from models_manager import MainUser, MainTask, MainSystemLog
    assert MainUser is not None
    assert MainTask is not None
    assert MainSystemLog is not None

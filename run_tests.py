import os
import pytest

def main():
    os.environ['PYTHONPATH'] = os.pathsep.join([os.environ.get('PYTHONPATH', ''), os.getcwd()])
    pytest.main(['-v', '--tb=short', '--show-capture=all', '-s', 'tests/'])

if __name__ == '__main__':
    main()

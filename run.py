import os
import sys

# Adiciona o diretório pai ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from task_manager import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

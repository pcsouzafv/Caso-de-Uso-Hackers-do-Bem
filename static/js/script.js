// Configurações da API
const API_URL = 'http://localhost:8000';

// Funções auxiliares
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    if (toast) {
        toast.textContent = message;
        toast.className = `toast ${type} show`;
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
}

// Gerenciamento de tema
document.addEventListener('DOMContentLoaded', function() {
    // Inicializa o tema
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);

    // Botão de alternar tema
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });
    }

    // Inicializa os contadores de tarefas
    updateTaskCounters();

    // Adiciona event listeners para os botões de filtro
    const filterButtons = document.querySelectorAll('.tab-btn[data-filter]');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.getAttribute('data-filter');
            filterTasks(filter);
            
            // Atualiza a classe active
            document.querySelectorAll('.tab-btn[data-filter]').forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
        });
    });

    // Adiciona event listeners para as abas do admin
    const tabButtons = document.querySelectorAll('.tab-btn[data-tab]');
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tab = this.getAttribute('data-tab');
            switchTab(tab);
            
            // Atualiza a classe active
            document.querySelectorAll('.tab-btn[data-tab]').forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
        });
    });
});

// Atualiza o ícone do tema
function updateThemeIcon(theme) {
    const icon = document.querySelector('.theme-toggle i');
    if (icon) {
        icon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
    }
}

// Filtra as tarefas
function filterTasks(filter) {
    const tasks = document.querySelectorAll('.task-item');
    tasks.forEach(task => {
        const isCompleted = task.classList.contains('completed');
        switch (filter) {
            case 'completed':
                task.style.display = isCompleted ? 'flex' : 'none';
                break;
            case 'pending':
                task.style.display = !isCompleted ? 'flex' : 'none';
                break;
            default: // 'all'
                task.style.display = 'flex';
        }
    });
}

// Alterna entre as abas do admin
function switchTab(tabName) {
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.style.display = content.id === tabName ? 'block' : 'none';
    });
}

// Atualiza os contadores de tarefas
function updateTaskCounters() {
    const tasks = document.querySelectorAll('.task-item');
    const completedTasks = document.querySelectorAll('.task-item.completed');
    
    const totalCounter = document.getElementById('total-tasks');
    const completedCounter = document.getElementById('completed-tasks');
    const pendingCounter = document.getElementById('pending-tasks');
    
    if (totalCounter) totalCounter.textContent = tasks.length;
    if (completedCounter) completedCounter.textContent = completedTasks.length;
    if (pendingCounter) pendingCounter.textContent = tasks.length - completedTasks.length;
}

// Toggle status da tarefa
async function toggleTaskStatus(taskId) {
    try {
        const response = await fetch(`/toggle_task/${taskId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const taskElement = document.querySelector(`[data-task-id="${taskId}"]`);
            if (taskElement) {
                taskElement.classList.toggle('completed');
                const icon = taskElement.querySelector('.task-actions .btn-success i');
                if (icon) {
                    icon.className = taskElement.classList.contains('completed') ? 
                        'fas fa-undo' : 'fas fa-check';
                }
                updateTaskCounters();
                showToast('Status da tarefa atualizado!', 'success');
            }
        } else {
            throw new Error('Erro ao atualizar tarefa');
        }
    } catch (error) {
        showToast('Erro ao atualizar tarefa', 'error');
        console.error('Erro:', error);
    }
}

// Deleta uma tarefa
async function deleteTask(taskId) {
    if (!confirm('Tem certeza que deseja excluir esta tarefa?')) return;

    try {
        const response = await fetch(`/delete_task/${taskId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const taskElement = document.querySelector(`[data-task-id="${taskId}"]`);
            if (taskElement) {
                taskElement.remove();
                updateTaskCounters();
                showToast('Tarefa excluída com sucesso!', 'success');
            }
        } else {
            throw new Error('Erro ao excluir tarefa');
        }
    } catch (error) {
        showToast('Erro ao excluir tarefa', 'error');
        console.error('Erro:', error);
    }
}

// Deleta um usuário
async function deleteUser(userId) {
    if (!confirm('Tem certeza que deseja excluir este usuário?')) return;

    try {
        const response = await fetch(`/delete_user/${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const userElement = document.querySelector(`[data-user-id="${userId}"]`);
            if (userElement) {
                userElement.remove();
                showToast('Usuário excluído com sucesso!', 'success');
            }
        } else {
            throw new Error('Erro ao excluir usuário');
        }
    } catch (error) {
        showToast('Erro ao excluir usuário', 'error');
        console.error('Erro:', error);
    }
}

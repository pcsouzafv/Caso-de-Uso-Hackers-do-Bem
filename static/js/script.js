// Configurações da API
const API_URL = 'http://localhost:8000';

// Elementos DOM
const loginTab = document.getElementById('login-tab');
const registerTab = document.getElementById('register-tab');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const loginFormElement = document.getElementById('login-form-element');
const registerFormElement = document.getElementById('register-form-element');
const authSection = document.getElementById('auth-section');
const taskDashboard = document.getElementById('task-dashboard');
const adminPanel = document.getElementById('admin-panel');
const usernameDisplay = document.getElementById('username-display');
const logoutBtn = document.getElementById('logout-btn');
const taskList = document.getElementById('task-list');
const addTaskForm = document.getElementById('add-task-form');
const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');
const allTasksBtn = document.getElementById('all-tasks-btn');
const pendingTasksBtn = document.getElementById('pending-tasks-btn');
const usersTab = document.getElementById('users-tab');
const logsTab = document.getElementById('logs-tab');
const usersPanel = document.getElementById('users-panel');
const logsPanel = document.getElementById('logs-panel');
const usersList = document.getElementById('users-list');
const systemLogs = document.getElementById('system-logs');
const adminBackBtn = document.getElementById('admin-back-btn');
const toast = document.getElementById('toast');

// Funções auxiliares
function showToast(message, isError = false) {
    toast.textContent = message;
    toast.className = 'toast' + (isError ? ' error' : '');
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function removeToken() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('is_admin');
}

async function fetchWithAuth(url, options = {}) {
    const token = getToken();
    if (!token) {
        showAuth();
        return null;
    }
    
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers
    };
    
    try {
        const response = await fetch(`${API_URL}${url}`, {
            ...options,
            headers
        });
        
        if (response.status === 401) {
            showToast('Sessão expirada. Por favor, faça login novamente.', true);
            removeToken();
            showAuth();
            return null;
        }
        
        return response;
    } catch (error) {
        console.error('Erro na requisição:', error);
        showToast('Erro ao conectar com o servidor', true);
        return null;
    }
}

function showAuth() {
    authSection.style.display = 'block';
    taskDashboard.style.display = 'none';
    adminPanel.style.display = 'none';
}

function showDashboard() {
    authSection.style.display = 'none';
    taskDashboard.style.display = 'block';
    adminPanel.style.display = 'none';
    loadTasks();
}

function showAdminPanel() {
    authSection.style.display = 'none';
    taskDashboard.style.display = 'none';
    adminPanel.style.display = 'block';
    loadUsers();
    loadLogs();
}

// Lógica de autenticação
loginTab.addEventListener('click', () => {
    loginTab.classList.add('active');
    registerTab.classList.remove('active');
    loginForm.style.display = 'block';
    registerForm.style.display = 'none';
});

registerTab.addEventListener('click', () => {
    registerTab.classList.add('active');
    loginTab.classList.remove('active');
    registerForm.style.display = 'block';
    loginForm.style.display = 'none';
});

loginFormElement.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    try {
        const response = await fetch(`${API_URL}/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            setToken(data.access_token);
            localStorage.setItem('username', username);
            
            // Verificar se o usuário é admin
            const userResponse = await fetchWithAuth('/tasks/');
            if (userResponse && userResponse.ok) {
                // Se conseguir acessar tarefas, está autenticado
                usernameDisplay.textContent = `Olá, ${username}`;
                showToast(`Bem-vindo(a), ${username}!`);
                
                // Tentar acessar endpoint de admin para verificar permissões
                const adminResponse = await fetchWithAuth('/admin/users/');
                if (adminResponse && adminResponse.ok) {
                    localStorage.setItem('is_admin', 'true');
                    const adminBtn = document.createElement('button');
                    adminBtn.className = 'btn btn-outline';
                    adminBtn.innerHTML = '<i class="fas fa-shield-alt"></i> Admin';
                    adminBtn.addEventListener('click', showAdminPanel);
                    document.querySelector('.user-info').insertBefore(adminBtn, logoutBtn);
                }
                
                showDashboard();
            }
        } else {
            showToast('Usuário ou senha incorretos', true);
        }
    } catch (error) {
        console.error('Erro no login:', error);
        showToast('Erro ao conectar com o servidor', true);
    }
});

registerFormElement.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    
    try {
        const response = await fetch(`${API_URL}/users/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            showToast('Usuário registrado com sucesso! Faça login.');
            loginTab.click();
            document.getElementById('login-username').value = username;
        } else {
            const error = await response.json();
            showToast(error.detail || 'Erro ao registrar usuário', true);
        }
    } catch (error) {
        console.error('Erro no registro:', error);
        showToast('Erro ao conectar com o servidor', true);
    }
});

logoutBtn.addEventListener('click', () => {
    removeToken();
    showToast('Logout realizado com sucesso');
    showAuth();
});

// Gestão de tarefas
async function loadTasks(filter = '') {
    let url = '/tasks/';
    if (filter === 'pending') {
        url = '/tasks/pending/';
    } else if (filter.startsWith('search:')) {
        const keyword = filter.split(':')[1];
        url = `/tasks/search/?keyword=${encodeURIComponent(keyword)}`;
    }
    
    const response = await fetchWithAuth(url);
    if (!response || !response.ok) return;
    
    const tasks = await response.json();
    renderTasks(tasks);
}

function renderTasks(tasks) {
    taskList.innerHTML = '';
    
    if (tasks.length === 0) {
        const emptyMessage = document.createElement('li');
        emptyMessage.className = 'task-item empty-message';
        emptyMessage.textContent = 'Nenhuma tarefa encontrada';
        taskList.appendChild(emptyMessage);
        return;
    }
    
    tasks.forEach(task => {
        const li = document.createElement('li');
        li.className = `task-item ${task.is_completed ? 'completed' : ''}`;
        li.dataset.id = task.id;
        
        const taskContent = document.createElement('div');
        taskContent.className = 'task-content';
        
        const taskTitle = document.createElement('div');
        taskTitle.className = 'task-title';
        taskTitle.textContent = task.title;
        
        const taskDescription = document.createElement('div');
        taskDescription.className = 'task-description';
        taskDescription.textContent = task.description || 'Sem descrição';
        
        taskContent.appendChild(taskTitle);
        taskContent.appendChild(taskDescription);
        
        const taskActions = document.createElement('div');
        taskActions.className = 'task-actions';
        
        const toggleBtn = document.createElement('button');
        toggleBtn.className = `btn ${task.is_completed ? 'btn-outline' : 'btn-success'}`;
        toggleBtn.innerHTML = task.is_completed ? 
            '<i class="fas fa-times"></i> Desmarcar' : 
            '<i class="fas fa-check"></i> Concluir';
        
        toggleBtn.addEventListener('click', () => toggleTaskStatus(task.id, !task.is_completed));
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'btn btn-danger';
        deleteBtn.innerHTML = '<i class="fas fa-trash"></i> Excluir';
        deleteBtn.addEventListener('click', () => deleteTask(task.id));
        
        taskActions.appendChild(toggleBtn);
        taskActions.appendChild(deleteBtn);
        
        li.appendChild(taskContent);
        li.appendChild(taskActions);
        
        taskList.appendChild(li);
    });
}

addTaskForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const title = document.getElementById('task-title').value;
    const description = document.getElementById('task-description').value;
    
    const response = await fetchWithAuth('/tasks/', {
        method: 'POST',
        body: JSON.stringify({ title, description })
    });
    
    if (response && response.ok) {
        showToast('Tarefa adicionada com sucesso');
        document.getElementById('task-title').value = '';
        document.getElementById('task-description').value = '';
        loadTasks();
    }
});

async function toggleTaskStatus(taskId, isCompleted) {
    const response = await fetchWithAuth(`/tasks/${taskId}`, {
        method: 'PUT',
        body: JSON.stringify({ is_completed: isCompleted })
    });
    
    if (response && response.ok) {
        showToast(`Tarefa ${isCompleted ? 'concluída' : 'reaberta'} com sucesso`);
        loadTasks();
    }
}

async function deleteTask(taskId) {
    if (!confirm('Tem certeza que deseja excluir esta tarefa?')) return;
    
    const response = await fetchWithAuth(`/tasks/${taskId}`, {
        method: 'DELETE'
    });
    
    if (response && response.ok) {
        showToast('Tarefa excluída com sucesso');
        loadTasks();
    }
}

searchBtn.addEventListener('click', () => {
    const keyword = searchInput.value.trim();
    if (keyword) {
        loadTasks(`search:${keyword}`);
    }
});

searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        searchBtn.click();
    }
});

allTasksBtn.addEventListener('click', () => {
    allTasksBtn.classList.add('active');
    pendingTasksBtn.classList.remove('active');
    loadTasks();
});

pendingTasksBtn.addEventListener('click', () => {
    pendingTasksBtn.classList.add('active');
    allTasksBtn.classList.remove('active');
    loadTasks('pending');
});

// Funções de administração
async function loadUsers() {
    const response = await fetchWithAuth('/admin/users/');
    if (!response || !response.ok) return;
    
    const users = await response.json();
    
    usersList.innerHTML = '';
    
    users.forEach(user => {
        const li = document.createElement('li');
        li.className = 'user-item';
        li.dataset.id = user.id;
        
        const userInfo = document.createElement('div');
        userInfo.textContent = `${user.username} ${user.is_admin ? '(Admin)' : ''}`;
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'btn btn-danger';
        deleteBtn.innerHTML = '<i class="fas fa-trash"></i> Remover';
        deleteBtn.disabled = user.is_admin; // Não permitir excluir admins
        deleteBtn.addEventListener('click', () => deleteUser(user.id, user.username));
        
        li.appendChild(userInfo);
        li.appendChild(deleteBtn);
        
        usersList.appendChild(li);
    });
}

async function loadLogs() {
    const response = await fetchWithAuth('/admin/logs/');
    if (!response || !response.ok) return;
    
    const data = await response.json();
    
    systemLogs.innerHTML = '';
    
    data.logs.forEach(log => {
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        logEntry.textContent = log;
        systemLogs.appendChild(logEntry);
    });
}

async function deleteUser(userId, username) {
    if (!confirm(`Tem certeza que deseja excluir o usuário ${username}?`)) return;
    
    const response = await fetchWithAuth(`/admin/users/${userId}`, {
        method: 'DELETE'
    });
    
    if (response && response.ok) {
        showToast(`Usuário ${username} excluído com sucesso`);
        loadUsers();
    }
}

usersTab.addEventListener('click', () => {
    usersTab.classList.add('active');
    logsTab.classList.remove('active');
    usersPanel.style.display = 'block';
    logsPanel.style.display = 'none';
});

logsTab.addEventListener('click', () => {
    logsTab.classList.add('active');
    usersTab.classList.remove('active');
    logsPanel.style.display = 'block';
    usersPanel.style.display = 'none';
});

adminBackBtn.addEventListener('click', showDashboard);

// Verificar autenticação no carregamento
document.addEventListener('DOMContentLoaded', async () => {
    const token = getToken();
    const username = localStorage.getItem('username');
    const isAdmin = localStorage.getItem('is_admin') === 'true';
    
    if (token && username) {
        // Verificar se o token ainda é válido
        const response = await fetchWithAuth('/tasks/');
        
        if (response && response.ok) {
            usernameDisplay.textContent = `Olá, ${username}`;
            
            if (isAdmin) {
                const adminBtn = document.createElement('button');
                adminBtn.className = 'btn btn-outline';
                adminBtn.innerHTML = '<i class="fas fa-shield-alt"></i> Admin';
                adminBtn.addEventListener('click', showAdminPanel);
                document.querySelector('.user-info').insertBefore(adminBtn, logoutBtn);
            }
            
            showDashboard();
            return;
        }
    }
    
    showAuth();
});

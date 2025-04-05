document.addEventListener('DOMContentLoaded', function() {
    // Elementos do formulário
    const taskForm = document.getElementById('task-form');
    const cancelButton = taskForm.querySelector('.btn-secondary');

    // Função para carregar e exibir o contador de tarefas
    async function loadTaskCounts() {
        try {
            const response = await fetch('/api/tasks');
            const tasks = await response.json();
            
            const pendentes = tasks.filter(t => t.status === 'pendente').length;
            const emAndamento = tasks.filter(t => t.status === 'em_andamento').length;
            const concluidas = tasks.filter(t => t.status === 'concluida').length;

            document.querySelector('.status li:nth-child(1) .badge').textContent = pendentes;
            document.querySelector('.status li:nth-child(2) .badge').textContent = emAndamento;
            document.querySelector('.status li:nth-child(3) .badge').textContent = concluidas;
        } catch (error) {
            console.error('Erro ao carregar contadores:', error);
        }
    }

    // Handler para submissão do formulário
    taskForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = {
            title: document.getElementById('title').value,
            description: document.getElementById('description').value,
            priority: document.getElementById('priority').value,
            status: document.getElementById('status').value
        };

        try {
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                alert('Tarefa criada com sucesso!');
                taskForm.reset();
                loadTaskCounts(); // Atualiza os contadores
            } else {
                alert('Erro ao criar tarefa');
            }
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao criar tarefa');
        }
    });

    // Handler para o botão cancelar
    cancelButton.addEventListener('click', function() {
        taskForm.reset();
    });

    // Handlers para itens do menu
    document.querySelectorAll('.menu li').forEach(item => {
        item.addEventListener('click', function() {
            // Remove a classe active de todos os itens
            document.querySelectorAll('.menu li').forEach(i => i.classList.remove('active'));
            // Adiciona a classe active ao item clicado
            this.classList.add('active');
        });
    });

    // Carrega os contadores inicialmente
    loadTaskCounts();
});

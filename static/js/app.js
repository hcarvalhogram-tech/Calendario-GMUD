// API Configuration
const API_BASE = 'http://127.0.0.1:8000/api/gmuds';

// DOM Elements
const navItems = document.querySelectorAll('.nav-item');
const pages = document.querySelectorAll('.page');
const modal = document.getElementById('modal');
const toast = document.getElementById('toast');

// Global state
let currentPage = 'dashboard';
let gmuds = [];
let currentDate = new Date();

// ============ Initialization ============
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadDashboard();
});

// ============ Navigation ============
function initializeEventListeners() {
    // Navigation items
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const page = item.dataset.page;
            navigateTo(page);
        });
    });

    // Modal close
    document.querySelector('.modal-close').addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });

    // Form submission
    document.getElementById('form-nova-gmud').addEventListener('submit', handleCreateGMUD);

    // Filters
    document.getElementById('btn-refresh').addEventListener('click', loadGMUDs);
    document.getElementById('filter-equipamento').addEventListener('input', filterGMUDs);
    document.getElementById('filter-status').addEventListener('change', filterGMUDs);

    // Calendar navigation
    document.getElementById('prev-month').addEventListener('click', previousMonth);
    document.getElementById('next-month').addEventListener('click', nextMonth);
}

function navigateTo(page) {
    // Update active nav item
    navItems.forEach(item => {
        item.classList.remove('active');
        if (item.dataset.page === page) {
            item.classList.add('active');
        }
    });

    // Show page
    pages.forEach(p => p.classList.remove('active'));
    document.getElementById(page).classList.add('active');
    currentPage = page;

    // Load page data
    if (page === 'dashboard') {
        loadDashboard();
    } else if (page === 'calendario') {
        renderCalendar();
    } else if (page === 'gmuds') {
        loadGMUDs();
    }
}

// ============ Dashboard ============
async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE}/dashboard/resumo`);
        const data = await response.json();

        // Update stats
        document.getElementById('total-gmuds').textContent = data.total;
        document.getElementById('agendadas-count').textContent = data.agendadas;
        document.getElementById('em-progresso-count').textContent = data.em_progresso;
        document.getElementById('concluidas-count').textContent = data.concluidas;

        // Update progress
        const percent = Math.round(data.taxa_conclusao);
        document.getElementById('progress-fill').style.width = percent + '%';
        document.getElementById('progress-percent').textContent = percent + '%';

        // Load recent
        await loadRecentGMUDs();
    } catch (error) {
        console.error('Erro ao carregar dashboard:', error);
        showToast('Erro ao carregar dashboard', 'error');
    }
}

async function loadRecentGMUDs() {
    try {
        const response = await fetch(API_BASE);
        gmuds = await response.json();

        const recent = gmuds.slice(-5).reverse();
        const recentList = document.getElementById('recent-list');
        recentList.innerHTML = '';

        if (recent.length === 0) {
            recentList.innerHTML = '<p style="text-align: center; color: var(--gray-500);">Nenhuma manutenção registrada</p>';
            return;
        }

        recent.forEach(gmud => {
            const item = document.createElement('div');
            item.className = 'recent-item';
            item.innerHTML = `
                <div class="recent-item-info">
                    <h4>${gmud.equipamento}</h4>
                    <p>${formatDate(gmud.data)}</p>
                </div>
                <div class="recent-item-status badge badge-${gmud.status.toLowerCase()}">
                    ${getStatusText(gmud.status)}
                </div>
            `;
            item.addEventListener('click', () => showGMUDDetails(gmud));
            recentList.appendChild(item);
        });
    } catch (error) {
        console.error('Erro ao carregar recentes:', error);
    }
}

// ============ GMUDs Management ============
async function loadGMUDs() {
    try {
        const response = await fetch(API_BASE);
        gmuds = await response.json();
        filterGMUDs();
    } catch (error) {
        console.error('Erro ao carregar GMUDs:', error);
        showToast('Erro ao carregar manutenções', 'error');
    }
}

function filterGMUDs() {
    const equipamento = document.getElementById('filter-equipamento').value.toLowerCase();
    const status = document.getElementById('filter-status').value;

    const filtered = gmuds.filter(gmud => {
        const matchEquipamento = gmud.equipamento.toLowerCase().includes(equipamento);
        const matchStatus = !status || gmud.status === status;
        return matchEquipamento && matchStatus;
    });

    renderGMUDsTable(filtered);
}

function renderGMUDsTable(list) {
    const tbody = document.getElementById('gmuds-list');
    const emptyState = document.getElementById('empty-state');

    if (list.length === 0) {
        tbody.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }

    emptyState.style.display = 'none';
    tbody.innerHTML = list.map(gmud => `
        <tr>
            <td>#${gmud.id}</td>
            <td>${formatDate(gmud.data)}</td>
            <td>${gmud.equipamento}</td>
            <td>${gmud.descricao || '-'}</td>
            <td>
                <span class="badge badge-${gmud.risco?.toLowerCase() || 'baixo'}">
                    ${gmud.risco || 'BAIXO'}
                </span>
            </td>
            <td>
                <span class="badge badge-${gmud.status.toLowerCase()}">
                    ${getStatusText(gmud.status)}
                </span>
            </td>
            <td>
                <button class="btn-sm btn-primary" onclick="showGMUDDetails(${JSON.stringify(gmud).replace(/"/g, '&quot;')})">
                    <i class="fas fa-eye"></i> Ver
                </button>
                <button class="btn-sm btn-danger" onclick="deleteGMUD(${gmud.id})">
                    <i class="fas fa-trash"></i> Deletar
                </button>
            </td>
        </tr>
    `).join('');
}

async function handleCreateGMUD(e) {
    e.preventDefault();

    const data = {
        data: document.getElementById('form-data').value,
        equipamento: document.getElementById('form-equipamento').value,
        descricao: document.getElementById('form-descricao').value,
        justificativa: document.getElementById('form-justificativa').value,
        risco: document.getElementById('form-risco').value
    };

    try {
        const response = await fetch(API_BASE + '/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao criar GMUD');
        }

        showToast('GMUD criada com sucesso!', 'success');
        document.getElementById('form-nova-gmud').reset();
        
        // Atualizar dashboard
        setTimeout(() => {
            loadDashboard();
            navigateTo('gmuds');
        }, 1000);
    } catch (error) {
        console.error('Erro ao criar GMUD:', error);
        showToast(error.message, 'error');
    }
}

async function deleteGMUD(id) {
    if (!confirm('Tem certeza que deseja deletar esta GMUD?')) return;

    try {
        const response = await fetch(`${API_BASE}/${id}`, { method: 'DELETE' });
        
        if (response.ok) {
            showToast('GMUD deletada com sucesso', 'success');
            loadGMUDs();
            loadDashboard();
        }
    } catch (error) {
        console.error('Erro ao deletar:', error);
        showToast('Erro ao deletar GMUD', 'error');
    }
}

function showGMUDDetails(gmud) {
    if (typeof gmud === 'string') {
        gmud = JSON.parse(gmud);
    }

    const modalBody = document.getElementById('modal-body');
    modalBody.innerHTML = `
        <div class="modal-item">
            <span class="modal-label">ID:</span>
            <span class="modal-value">#${gmud.id}</span>
        </div>
        <div class="modal-item">
            <span class="modal-label">Equipamento:</span>
            <span class="modal-value">${gmud.equipamento}</span>
        </div>
        <div class="modal-item">
            <span class="modal-label">Data:</span>
            <span class="modal-value">${formatDate(gmud.data)}</span>
        </div>
        <div class="modal-item">
            <span class="modal-label">Status:</span>
            <span class="badge badge-${gmud.status.toLowerCase()}">${getStatusText(gmud.status)}</span>
        </div>
        <div class="modal-item">
            <span class="modal-label">Risco:</span>
            <span class="modal-value">${gmud.risco || 'BAIXO'}</span>
        </div>
        <div class="modal-item">
            <span class="modal-label">Descrição:</span>
            <span class="modal-value">${gmud.descricao || '-'}</span>
        </div>
        <div class="modal-item">
            <span class="modal-label">Justificativa:</span>
            <span class="modal-value">${gmud.justificativa || '-'}</span>
        </div>
        <div class="modal-item">
            <span class="modal-label">Criado em:</span>
            <span class="modal-value">${formatDateTime(gmud.criado_em)}</span>
        </div>
        <div style="margin-top: 1.5rem; display: flex; gap: 1rem;">
            <button class="btn-primary" onclick="updateGMUDStatus(${gmud.id}, 'CONCLUIDO')">
                <i class="fas fa-check"></i> Marcar como Concluído
            </button>
            <button class="btn-secondary" onclick="closeModal()">Fechar</button>
        </div>
    `;
    openModal();
}

async function updateGMUDStatus(id, status) {
    try {
        const response = await fetch(`${API_BASE}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status })
        });

        if (response.ok) {
            showToast('Status atualizado com sucesso', 'success');
            closeModal();
            loadGMUDs();
            loadDashboard();
        }
    } catch (error) {
        console.error('Erro ao atualizar:', error);
        showToast('Erro ao atualizar status', 'error');
    }
}

// ============ Calendar ============
function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    // Update title
    const monthNames = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ];
    document.getElementById('calendar-month').textContent = 
        `${monthNames[month]} ${year}`;

    // Get calendar data
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();

    // Create calendar grid
    const calendarDiv = document.getElementById('calendar');
    calendarDiv.innerHTML = '';

    // Day headers
    const dayHeaders = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab'];
    dayHeaders.forEach(day => {
        const header = document.createElement('div');
        header.className = 'calendar-day-header';
        header.textContent = day;
        calendarDiv.appendChild(header);
    });

    // Previous month days
    const prevMonth = new Date(year, month, 0);
    const daysInPrevMonth = prevMonth.getDate();
    for (let i = startingDayOfWeek - 1; i >= 0; i--) {
        const day = document.createElement('div');
        day.className = 'calendar-day other-month';
        day.textContent = daysInPrevMonth - i;
        calendarDiv.appendChild(day);
    }

    // Current month days
    for (let i = 1; i <= daysInMonth; i++) {
        const day = document.createElement('div');
        day.className = 'calendar-day';
        day.textContent = i;

        // Check if has maintenance
        const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
        const hasMaintenance = gmuds.some(g => g.data === dateStr);
        
        if (hasMaintenance) {
            day.classList.add('has-maintenance');
        }

        day.addEventListener('click', () => {
            const dayGMUDs = gmuds.filter(g => g.data === dateStr);
            if (dayGMUDs.length > 0) {
                showDayGMUDs(dateStr, dayGMUDs);
            }
        });

        calendarDiv.appendChild(day);
    }

    // Next month days
    const totalCells = calendarDiv.querySelectorAll('.calendar-day, .calendar-day-header').length - 7;
    const remainingCells = 42 - totalCells;
    for (let i = 1; i <= remainingCells; i++) {
        const day = document.createElement('div');
        day.className = 'calendar-day other-month';
        day.textContent = i;
        calendarDiv.appendChild(day);
    }

    // Load GMUDs if not loaded
    if (gmuds.length === 0) {
        loadGMUDs();
    }
}

function previousMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
}

function nextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
}

function showDayGMUDs(dateStr, dayGMUDs) {
    const modalBody = document.getElementById('modal-body');
    const title = document.getElementById('modal-title');
    
    title.textContent = `Manutenções de ${formatDate(dateStr)}`;
    
    modalBody.innerHTML = dayGMUDs.map(gmud => `
        <div class="modal-item" style="flex-direction: column; align-items: flex-start;">
            <h4 style="margin-bottom: 0.5rem;">${gmud.equipamento}</h4>
            <div style="display: flex; gap: 1rem; width: 100%;">
                <span class="badge badge-${gmud.status.toLowerCase()}">${getStatusText(gmud.status)}</span>
                <span class="badge badge-${gmud.risco?.toLowerCase() || 'baixo'}">${gmud.risco || 'BAIXO'}</span>
            </div>
            <p style="margin-top: 0.5rem; color: var(--gray-600); font-size: 0.875rem;">
                ${gmud.descricao || '-'}
            </p>
        </div>
    `).join('');
    
    modalBody.innerHTML += `
        <div style="margin-top: 1.5rem;">
            <button class="btn-secondary" onclick="closeModal()" style="width: 100%;">Fechar</button>
        </div>
    `;
    
    openModal();
}

// ============ Modal ============
function openModal() {
    modal.classList.add('active');
}

function closeModal() {
    modal.classList.remove('active');
}

// ============ Toast ============
function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = `toast ${type} active`;
    
    setTimeout(() => {
        toast.classList.remove('active');
    }, 3000);
}

// ============ Utilities ============
function formatDate(dateStr) {
    if (!dateStr) return '-';
    const date = new Date(dateStr + 'T00:00:00');
    return date.toLocaleDateString('pt-BR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
}

function formatDateTime(dateStr) {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toLocaleDateString('pt-BR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function getStatusText(status) {
    const statusMap = {
        'AGENDADO': 'Agendada',
        'EM_PROGRESSO': 'Em Progresso',
        'CONCLUIDO': 'Concluída',
        'CANCELADO': 'Cancelada'
    };
    return statusMap[status] || status;
}

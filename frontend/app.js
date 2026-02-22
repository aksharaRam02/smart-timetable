// ✅ LIVE BACKEND (Render)
const API_BASE_URL = 'https://smart-timetable-899l.onrender.com/api';

// Utility to handle API requests
async function apiRequest(endpoint, method = 'GET', body = null) {
    const headers = {
        'Content-Type': 'application/json',
    };

    const config = {
        method,
        headers,
    };

    if (body) {
        config.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

        if (!response.ok) {
            const text = await response.text();
            throw new Error(text || 'API request failed');
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showToast(error.message || 'Server error', 'error');
        throw error;
    }
}

// ✅ Toast system (unchanged — your nice UI stays)
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg text-white font-medium transform transition-all duration-300 translate-y-10 opacity-0 z-50 ${
        type === 'success' ? 'bg-green-600' : 'bg-red-600'
    }`;

    toast.innerHTML = `
        <div class="flex items-center space-x-2">
            <i class="fa-solid ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
            <span>${message}</span>
        </div>
    `;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.remove('translate-y-10', 'opacity-0');
    }, 10);

    setTimeout(() => {
        toast.classList.add('translate-y-10', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// timetable.js

let currentTimetable = null;
let allSubjects = {};
let allFaculties = {};
let allClassrooms = {};
let allSemesters = {};

const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
const START_HOUR = 9;
const END_HOUR = 17;

document.addEventListener('DOMContentLoaded', async () => {
    // Check URL for ID
    const urlParams = new URLSearchParams(window.location.search);
    const ttId = urlParams.get('id');

    if (!ttId) {
        showToast('No timetable ID provided in URL', 'error');
        return;
    }

    try {
        toggleSpinner(true);
        // Load metadata
        const [subs, facs, rooms, sems] = await Promise.all([
            apiRequest('/subjects/'),
            apiRequest('/faculties/'),
            apiRequest('/classrooms/'),
            apiRequest('/semesters/')
        ]);

        subs.forEach(s => allSubjects[s.id] = s);
        facs.forEach(f => allFaculties[f.id] = f);
        rooms.forEach(r => allClassrooms[r.id] = r);
        sems.forEach(s => allSemesters[s.id] = s);

        // Load specific timetable
        currentTimetable = await apiRequest(`/timetables/${ttId}`);

        document.getElementById('tt-fitness').textContent = currentTimetable.fitness_score;

        setupFilters();

    } catch (e) {
        showToast(e.message, 'error');
    } finally {
        toggleSpinner(false);
    }
});

function toggleSpinner(show) {
    const s = document.getElementById('loading-spinner');
    if (show) s.classList.remove('hidden'); else s.classList.add('hidden');
}

function setupFilters() {
    const fType = document.getElementById('filter-type');
    const fEntity = document.getElementById('filter-entity');
    const btn = document.getElementById('btn-apply-filter');

    const updateEntityDropdown = () => {
        const type = fType.value;
        fEntity.innerHTML = '';
        let dataMap = {};
        if (type === 'semester') dataMap = allSemesters;
        else if (type === 'faculty') dataMap = allFaculties;
        else if (type === 'classroom') dataMap = allClassrooms;

        Object.values(dataMap).forEach(item => {
            fEntity.innerHTML += `<option value="${item.id}">${item.name || item.id}</option>`;
        });
    };

    fType.addEventListener('change', updateEntityDropdown);
    updateEntityDropdown(); // initial population

    btn.addEventListener('click', () => {
        renderGrid(fType.value, parseInt(fEntity.value));
    });

    // Render first available automatically
    if (Object.values(allSemesters).length > 0) {
        fEntity.value = Object.values(allSemesters)[0].id;
        renderGrid('semester', parseInt(fEntity.value));
    }
}

function renderGrid(filterType, entityId) {
    const tbody = document.getElementById('grid-body');
    tbody.innerHTML = '';

    // Filter sessions
    let filteredSessions = [];
    if (currentTimetable.sessions) {
        filteredSessions = currentTimetable.sessions.filter(s => {
            const sub = allSubjects[s.subject_id];
            if (!sub) return false;
            if (filterType === 'semester') return sub.semester_id === entityId;
            if (filterType === 'faculty') return s.faculty_id === entityId;
            if (filterType === 'classroom') return s.classroom_id === entityId;
            return false;
        });
    }

    if (filteredSessions.length === 0) {
        document.getElementById('empty-state').classList.remove('hidden');
    } else {
        document.getElementById('empty-state').classList.add('hidden');
    }

    // Initialize Grid structure
    let grid = {};
    for (let h = START_HOUR; h < END_HOUR; h++) {
        grid[h] = { "Monday": null, "Tuesday": null, "Wednesday": null, "Thursday": null, "Friday": null };
    }

    // Populate grid
    filteredSessions.forEach(session => {
        if (grid[session.start_time]) {
            grid[session.start_time][session.day_of_week] = session;
        }
    });

    // Render HTML
    for (let h = START_HOUR; h < END_HOUR; h++) {
        const tr = document.createElement('tr');

        // Time Label
        const timeHeader = document.createElement('td');
        timeHeader.className = "py-3 px-2 border-r border-gray-200 bg-gray-50 font-medium text-gray-700 align-middle";
        const ampm = h >= 12 ? 'PM' : 'AM';
        const displayH = h > 12 ? h - 12 : h;
        const displayNext = (h + 1) > 12 ? (h + 1) - 12 : (h + 1);
        const ampmNext = (h + 1) >= 12 ? 'PM' : 'AM';

        timeHeader.innerHTML = `${displayH}:00 ${ampm} - ${displayNext}:00 ${ampmNext}`;
        tr.appendChild(timeHeader);

        // Days
        DAYS.forEach(day => {
            const td = document.createElement('td');
            td.className = "p-2 border-r border-gray-200 h-24 align-top w-1/5 transition-colors hover:bg-gray-50";

            const session = grid[h][day];
            if (session) {
                const sub = allSubjects[session.subject_id] || { name: 'Unknown' };
                const fac = allFaculties[session.faculty_id] || { name: 'TBD' };
                const room = allClassrooms[session.classroom_id] || { name: 'Unknown' };

                // Card for class
                td.innerHTML = `
                    <div class="h-full w-full bg-indigo-50 border-l-4 border-indigo-500 rounded px-2 py-1 text-left flex flex-col justify-center shadow-sm relative group">
                        <div class="font-bold text-indigo-900 text-sm truncate" title="${sub.name}">${sub.name}</div>
                        ${filterType !== 'faculty' ? `<div class="text-xs text-indigo-700 truncate"><i class="fa-solid fa-user-tie mr-1"></i>${fac.name}</div>` : ''}
                        ${filterType !== 'classroom' ? `<div class="text-xs text-indigo-700 truncate"><i class="fa-solid fa-door-open mr-1"></i>${room.name}</div>` : ''}
                        
                        <!-- Mini Edit btn -->
                        <div class="absolute top-1 right-1 opacity-0 group-hover:opacity-100 transition-opacity">
                            <button class="text-indigo-400 hover:text-indigo-800" title="Manual Override (Coming Soon)"><i class="fa-solid fa-pen-to-square"></i></button>
                        </div>
                    </div>
                `;
            } else {
                td.innerHTML = `<div class="h-full w-full border-2 border-dashed border-gray-100 rounded text-gray-300 flex items-center justify-center text-xs opacity-0 hover:opacity-100 transition-opacity">Free Slot</div>`;
            }

            tr.appendChild(td);
        });

        tbody.appendChild(tr);
    }
}
async function apiRequest(path) {
    const BASE_URL = "https://smart-timetable-899l.onrender.com/api";

    const res = await fetch(BASE_URL + path);

    if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "API error");
    }

    return res.json();
}

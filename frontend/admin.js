// admin.js - Admin dashboard logic

// Navigation functionality
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(el => {
        el.classList.add('hidden');
    });

    // Un-highlight all tabs
    document.querySelectorAll('#sidebar-nav button').forEach(el => {
        el.classList.remove('bg-indigo-50', 'text-indigo-700');
        el.classList.add('text-gray-600');
    });

    // Handle Generation page exceptions which hides sidebar
    if (sectionId === 'generate') {
        document.getElementById('sec-generate').classList.remove('hidden');
        return;
    }

    // Show selected section
    document.getElementById(`sec-${sectionId}`).classList.remove('hidden');

    // Highlight selected tab
    const activeTab = document.getElementById(`tab-${sectionId}`);
    if (activeTab) {
        activeTab.classList.remove('text-gray-600');
        activeTab.classList.add('bg-indigo-50', 'text-indigo-700');
    }

    // Fetch relevant data
    fetchData(sectionId);
}

function switchTab(tab) {
    if (tab === 'data') {
        document.getElementById('nav-btn-data').classList.replace('text-indigo-200', 'text-white');
        document.getElementById('nav-btn-data').classList.replace('border-transparent', 'border-white');

        document.getElementById('nav-btn-generate').classList.replace('text-white', 'text-indigo-200');
        document.getElementById('nav-btn-generate').classList.replace('border-white', 'border-transparent');

        document.getElementById('sidebar-nav').classList.remove('hidden');
        showSection('departments');
    } else {
        document.getElementById('nav-btn-generate').classList.replace('text-indigo-200', 'text-white');
        document.getElementById('nav-btn-generate').classList.replace('border-transparent', 'border-white');

        document.getElementById('nav-btn-data').classList.replace('text-white', 'text-indigo-200');
        document.getElementById('nav-btn-data').classList.replace('border-white', 'border-transparent');

        document.getElementById('sidebar-nav').classList.add('hidden');
        showSection('generate');
    }
}

// Global state arrays for dropdowns
let _departments = [];
let _courses = [];
let _semesters = [];
let _faculties = [];

// CRUD Operations setup
async function fetchData(type) {
    const listBody = document.getElementById(`list-${type}`);
    if (!listBody) return;

    try {
        const data = await apiRequest(`/${type}/`);
        listBody.innerHTML = '';

        if (data.length === 0) {
            listBody.innerHTML = `<tr><td colspan="6" class="px-6 py-4 text-center text-sm text-gray-500">No records found.</td></tr>`;
        }

        data.forEach(item => {
            const tr = document.createElement('tr');

            if (type === 'departments') {
                tr.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.id}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${item.name}</td>
                `;
                // update cache
                _departments = data;
                fillDropdowns();
            } else if (type === 'courses') {
                tr.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.id}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${item.name}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.department_id}</td>
                `;
                _courses = data; fillDropdowns();
            } else if (type === 'semesters') {
                tr.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.id}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${item.name}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.course_id}</td>
                `;
                _semesters = data; fillDropdowns();
            } else if (type === 'classrooms') {
                tr.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.id}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${item.name}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.capacity}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"><span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">${item.room_type}</span></td>
                `;
            } else if (type === 'faculties') {
                tr.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.id}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${item.name}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.department_id}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.max_hours_per_week}h/week</td>
                `;
                _faculties = data; fillDropdowns();
            } else if (type === 'subjects') {
                tr.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.id}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${item.name}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">${item.code}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${item.credit_hours} cr / ${item.weekly_frequency}x wk</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Sem: ${item.semester_id} | Fac: ${item.faculty_id || 'TBD'}</td>
                `;
            }
            listBody.appendChild(tr);
        });
    } catch (e) {
        listBody.innerHTML = `<tr><td colspan="6" class="px-6 py-4 text-center text-sm text-red-500">Error loading data</td></tr>`;
    }
}

// Prefetch data for dropdowns
async function prefetchAllRelations() {
    try {
        _departments = await apiRequest('/departments/');
        _courses = await apiRequest('/courses/');
        _semesters = await apiRequest('/semesters/');
        _faculties = await apiRequest('/faculties/');
        fillDropdowns();
    } catch (e) { console.error('Prefetch error', e); }
}

function fillDropdowns() {
    // Fill course dept and faculty dept
    const selCDept = document.getElementById('course-dept');
    const selFDept = document.getElementById('fac-dept');
    if (selCDept) selCDept.innerHTML = '<option value="">Select Department</option>' + _departments.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
    if (selFDept) selFDept.innerHTML = '<option value="">Select Dept</option>' + _departments.map(d => `<option value="${d.id}">${d.name}</option>`).join('');

    // Fill semester course
    const selSCourse = document.getElementById('sem-course');
    if (selSCourse) selSCourse.innerHTML = '<option value="">Select Course</option>' + _courses.map(c => `<option value="${c.id}">${c.name}</option>`).join('');

    // Fill subject semester and faculty
    const selSubSem = document.getElementById('sub-sem');
    const selSubFac = document.getElementById('sub-fac');
    if (selSubSem) selSubSem.innerHTML = '<option value="">Select Semester</option>' + _semesters.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
    if (selSubFac) selSubFac.innerHTML = '<option value="">None / TBD</option>' + _faculties.map(f => `<option value="${f.id}">${f.name}</option>`).join('');
}

// Submit Handlers
document.addEventListener('DOMContentLoaded', () => {

    prefetchAllRelations().then(() => {
        showSection('departments'); // Initialize view
    });

    // Handle Department submit
    document.getElementById('form-department').addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            await apiRequest('/departments/', 'POST', { name: document.getElementById('dept-name').value });
            showToast('Department added successfully');
            document.getElementById('form-department').reset();
            fetchData('departments');
        } catch (err) { showToast(err.message, 'error'); }
    });

    // Handle Course submit
    document.getElementById('form-course').addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            await apiRequest('/courses/', 'POST', {
                name: document.getElementById('course-name').value,
                department_id: parseInt(document.getElementById('course-dept').value)
            });
            showToast('Course added successfully');
            document.getElementById('form-course').reset();
            fetchData('courses');
        } catch (err) { showToast(err.message, 'error'); }
    });

    // Handle Semester submit
    document.getElementById('form-semester').addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            await apiRequest('/semesters/', 'POST', {
                name: document.getElementById('sem-name').value,
                course_id: parseInt(document.getElementById('sem-course').value)
            });
            showToast('Semester added successfully');
            document.getElementById('form-semester').reset();
            fetchData('semesters');
        } catch (err) { showToast(err.message, 'error'); }
    });

    // Handle Faculty submit
    document.getElementById('form-faculty').addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            await apiRequest('/faculties/', 'POST', {
                name: document.getElementById('fac-name').value,
                department_id: parseInt(document.getElementById('fac-dept').value),
                max_hours_per_week: parseInt(document.getElementById('fac-hours').value)
            });
            showToast('Faculty added successfully');
            document.getElementById('form-faculty').reset();
            fetchData('faculties');
        } catch (err) { showToast(err.message, 'error'); }
    });

    // Handle Classroom submit
    document.getElementById('form-classroom').addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            await apiRequest('/classrooms/', 'POST', {
                name: document.getElementById('room-name').value,
                capacity: parseInt(document.getElementById('room-cap').value),
                room_type: document.getElementById('room-type').value
            });
            showToast('Classroom added successfully');
            document.getElementById('form-classroom').reset();
            fetchData('classrooms');
        } catch (err) { showToast(err.message, 'error'); }
    });

    // Handle Subject submit
    document.getElementById('form-subject').addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            const facId = document.getElementById('sub-fac').value;
            await apiRequest('/subjects/', 'POST', {
                name: document.getElementById('sub-name').value,
                code: document.getElementById('sub-code').value,
                credit_hours: parseInt(document.getElementById('sub-credits').value),
                weekly_frequency: parseInt(document.getElementById('sub-freq').value),
                semester_id: parseInt(document.getElementById('sub-sem').value),
                faculty_id: facId ? parseInt(facId) : null
            });
            showToast('Subject added successfully');
            document.getElementById('form-subject').reset();
            fetchData('subjects');
        } catch (err) { showToast(err.message, 'error'); }
    });

    // Handle Timetable Generation
    const genBtn = document.querySelector('#sec-generate button');
    if (genBtn) {
        genBtn.addEventListener('click', async () => {
            const originalText = genBtn.innerHTML;
            try {
                genBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i> Generating...';
                genBtn.disabled = true;

                const response = await apiRequest('/generate/', 'POST');
                showToast(response.message);

                // Redirect to timetable logic
                window.location.href = `timetable.html?id=${response.timetable_id}`;

            } catch (err) {
                showToast(err.message || 'Error generating timetable', 'error');
            } finally {
                genBtn.innerHTML = originalText;
                genBtn.disabled = false;
            }
        });
    }

});

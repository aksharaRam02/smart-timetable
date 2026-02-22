// timetable.js

const BASE_URL = "https://smart-timetable-899l.onrender.com/api";

let currentTimetable = null;
let allSubjects = {};
let allFaculties = {};
let allClassrooms = {};
let allSemesters = {};

const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
const START_HOUR = 9;
const END_HOUR = 17;

document.addEventListener("DOMContentLoaded", async () => {
    try {
        toggleSpinner(true);

        // 1️⃣ Get timetable ID or load latest
        const urlParams = new URLSearchParams(window.location.search);
        let ttId = urlParams.get("id");

        if (!ttId) {
            const all = await apiRequest("/timetables/");
            if (!all.length) {
                throw new Error("No timetables found in database");
            }
            ttId = all[0].id;
        }

        // 2️⃣ Load metadata
        const [subs, facs, rooms, sems] = await Promise.all([
            apiRequest("/subjects/"),
            apiRequest("/faculties/"),
            apiRequest("/classrooms/"),
            apiRequest("/semesters/")
        ]);

        subs.forEach(s => allSubjects[s.id] = s);
        facs.forEach(f => allFaculties[f.id] = f);
        rooms.forEach(r => allClassrooms[r.id] = r);
        sems.forEach(s => allSemesters[s.id] = s);

        // 3️⃣ Load timetable
        currentTimetable = await apiRequest(`/timetables/${ttId}`);
        document.getElementById("tt-fitness").textContent = currentTimetable.fitness_score;

        setupFilters();

    } catch (e) {
        console.error(e);
        alert("Frontend is connected, but backend returned an error:\n\n" + e.message);
    } finally {
        toggleSpinner(false);
    }
});

/* ------------------ API ------------------ */

async function apiRequest(path) {
    const res = await fetch(BASE_URL + path);

    if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `API error at ${path}`);
    }

    return res.json();
}

/* ------------------ UI ------------------ */

function toggleSpinner(show) {
    const s = document.getElementById("loading-spinner");
    if (!s) return;
    show ? s.classList.remove("hidden") : s.classList.add("hidden");
}

function setupFilters() {
    const fType = document.getElementById("filter-type");
    const fEntity = document.getElementById("filter-entity");
    const btn = document.getElementById("btn-apply-filter");

    const updateEntityDropdown = () => {
        fEntity.innerHTML = "";
        let dataMap = {};

        if (fType.value === "semester") dataMap = allSemesters;
        else if (fType.value === "faculty") dataMap = allFaculties;
        else if (fType.value === "classroom") dataMap = allClassrooms;

        Object.values(dataMap).forEach(item => {
            fEntity.innerHTML += `<option value="${item.id}">${item.name || item.id}</option>`;
        });
    };

    fType.addEventListener("change", updateEntityDropdown);
    updateEntityDropdown();

    btn.addEventListener("click", () => {
        renderGrid(fType.value, Number(fEntity.value));
    });

    if (Object.values(allSemesters).length) {
        fEntity.value = Object.values(allSemesters)[0].id;
        renderGrid("semester", Number(fEntity.value));
    }
}

function renderGrid(filterType, entityId) {
    const tbody = document.getElementById("grid-body");
    tbody.innerHTML = "";

    let filteredSessions = (currentTimetable.sessions || []).filter(s => {
        const sub = allSubjects[s.subject_id];
        if (!sub) return false;
        if (filterType === "semester") return sub.semester_id === entityId;
        if (filterType === "faculty") return s.faculty_id === entityId;
        if (filterType === "classroom") return s.classroom_id === entityId;
        return false;
    });

    document.getElementById("empty-state")
        .classList.toggle("hidden", filteredSessions.length > 0);

    let grid = {};
    for (let h = START_HOUR; h < END_HOUR; h++) {
        grid[h] = Object.fromEntries(DAYS.map(d => [d, null]));
    }

    filteredSessions.forEach(s => {
        if (grid[s.start_time]) {
            grid[s.start_time][s.day_of_week] = s;
        }
    });

    for (let h = START_HOUR; h < END_HOUR; h++) {
        const tr = document.createElement("tr");

        const timeCell = document.createElement("td");
        timeCell.className = "py-3 px-2 border-r bg-gray-50 font-medium";
        timeCell.textContent = `${h}:00 - ${h + 1}:00`;
        tr.appendChild(timeCell);

        DAYS.forEach(day => {
            const td = document.createElement("td");
            td.className = "p-2 border-r h-24";

            const s = grid[h][day];
            if (s) {
                td.innerHTML = `<strong>${allSubjects[s.subject_id]?.name}</strong>`;
            }

            tr.appendChild(td);
        });

        tbody.appendChild(tr);
    }
}

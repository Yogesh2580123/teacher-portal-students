document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById("searchBtn");
    const searchInput = document.getElementById("searchInput");
    const tableBody = document.querySelector("#studentsTable tbody");

    // Search functionality
    searchBtn.addEventListener("click", () => {
        const q = searchInput.value.trim();

        fetch(`/students/search?q=${encodeURIComponent(q)}`)
            .then(res => res.json())
            .then(data => {
                tableBody.innerHTML = "";

                if (!data.length) {
                    tableBody.innerHTML = "<tr><td colspan='4'>No records found</td></tr>";
                    return;
                }

                data.forEach(student => {
                    const row = document.createElement("tr");
                    row.setAttribute("data-id", student.id);
                    row.innerHTML = `
                        <td class="name">${student.name}</td>
                        <td class="subject">${student.subject}</td>
                        <td class="marks">${student.marks}</td>
                        <td>
                            <button class="editBtn">Edit</button>
                            <button class="deleteBtn">Delete</button>
                            <button class="saveBtn" style="display:none;">Save</button>
                            <button class="cancelBtn" style="display:none;">Cancel</button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });

                attachEventListeners(); // re-attach to new rows
            })
            .catch(() => alert("Error fetching search results."));
    });

    // Attach button actions
    function attachEventListeners() {
        document.querySelectorAll('.editBtn').forEach(btn =>
            btn.onclick = () => toggleEditMode(btn.closest('tr'), true)
        );

        document.querySelectorAll('.cancelBtn').forEach(btn =>
            btn.onclick = () => toggleEditMode(btn.closest('tr'), false)
        );

        document.querySelectorAll('.saveBtn').forEach(btn =>
            btn.onclick = () => saveRow(btn.closest('tr'))
        );

        document.querySelectorAll('.deleteBtn').forEach(btn =>
            btn.onclick = () => deleteRow(btn.closest('tr'))
        );
    }

    function toggleEditMode(row, editing) {
        ['name', 'subject', 'marks'].forEach(cls => {
            const cell = row.querySelector('.' + cls);
            if (editing) {
                const val = cell.textContent;
                cell.innerHTML = `<input type="${cls === 'marks' ? 'number' : 'text'}" value="${val}" />`;
            } else {
                const input = cell.querySelector('input');
                if (input) cell.textContent = input.defaultValue || input.value;
            }
        });

        row.querySelector('.editBtn').style.display = editing ? 'none' : 'inline-block';
        row.querySelector('.deleteBtn').style.display = editing ? 'none' : 'inline-block';
        row.querySelector('.saveBtn').style.display = editing ? 'inline-block' : 'none';
        row.querySelector('.cancelBtn').style.display = editing ? 'inline-block' : 'none';
    }

    function saveRow(row) {
        const id = row.dataset.id;
        const name = row.querySelector('.name input').value.trim();
        const subject = row.querySelector('.subject input').value.trim();
        const marks = row.querySelector('.marks input').value.trim();

        if (!name || !subject || isNaN(marks)) {
            alert('Please enter valid data.');
            return;
        }

        fetch(`/students/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, subject, marks: parseInt(marks) })
        })
        .then(res => {
            if (res.ok) {
                row.querySelector('.name').textContent = name;
                row.querySelector('.subject').textContent = subject;
                row.querySelector('.marks').textContent = marks;
                toggleEditMode(row, false);
            } else {
                alert('Failed to update student.');
            }
        })
        .catch(() => alert('Failed to update student.'));
    }

    function deleteRow(row) {
        const id = row.dataset.id;
        if (!confirm('Are you sure you want to delete this student?')) return;

        fetch(`/students/${id}`, {
            method: 'DELETE'
        })
        .then(res => {
            if (res.ok) {
                row.remove();
            } else {
                alert('Failed to delete student.');
            }
        })
        .catch(() => alert('Failed to delete student.'));
    }

    // Modal for Add Student
    window.openModal = function () {
        document.getElementById('studentModal').style.display = 'block';
        document.getElementById('overlay').style.display = 'block';
        document.getElementById('message').textContent = '';
        document.getElementById('name').value = '';
        document.getElementById('subject').value = '';
        document.getElementById('marks').value = '';
    };

    window.closeModal = function () {
        document.getElementById('studentModal').style.display = 'none';
        document.getElementById('overlay').style.display = 'none';
    };

    window.submitStudent = async function (event) {
        event.preventDefault();

        const name = document.getElementById('name').value.trim();
        const subject = document.getElementById('subject').value.trim();
        const marks = parseInt(document.getElementById('marks').value);

        if (!name || !subject || isNaN(marks)) {
            document.getElementById('message').textContent = "All fields are required.";
            return;
        }

        try {
            const res = await fetch('/students', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, subject, marks })
            });

            const data = await res.json();

            if (res.ok) {
                document.getElementById('message').style.color = 'green';
                document.getElementById('message').textContent = data.message;
                setTimeout(() => {
                    closeModal();
                    location.reload();
                }, 800);
            } else {
                document.getElementById('message').style.color = 'red';
                document.getElementById('message').textContent = data.error || 'Error occurred';
            }
        } catch {
            document.getElementById('message').style.color = 'red';
            document.getElementById('message').textContent = 'Network error';
        }
    };

    attachEventListeners(); // initial
});

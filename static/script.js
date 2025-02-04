function toggleEdit(noteId) {
    const modal = document.getElementById('edit-modal');
    const form = document.getElementById('modal-edit-form');
    const titleInput = document.getElementById('modal_note_title');
    const contentInput = document.getElementById('modal_note_content');

    // Set the form action to the correct note edit URL
    form.action = '/edit_note/' + noteId;

    // Populate the modal inputs with the current note data
    titleInput.value = document.querySelector('#edit-form-' + noteId + ' input[name="note_title"]').value;
    contentInput.value = document.querySelector('#edit-form-' + noteId + ' textarea[name="note_content"]').value;

    // Display the modal
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('edit-modal');
    modal.style.display = 'none';
}

function deleteNote(noteId) {
    if (confirm('Are you sure you want to delete this note?')) {
        // Send a POST request to delete the note
        fetch('/delete_note/' + noteId, {
            method: 'POST',
        }).then(response => {
            if (response.ok) {
                // Reload the page to reflect changes
                window.location.reload();
            } else {
                alert('Failed to delete the note.');
            }
        });
    }
}

function toggleCreateForm() {
    const form = document.getElementById('new-note-form');
    if (form.style.display === 'none' || form.style.display === '') {
        form.style.display = 'block';
    } else {
        form.style.display = 'none';
    }
}

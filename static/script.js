function toggleEdit(noteId) {
    const form = document.getElementById('edit-form-' + noteId);
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
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

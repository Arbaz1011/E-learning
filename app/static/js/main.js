// Enable Bootstrap tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add loading state to forms when submitting
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
            }
        });
    });

    // Enable Bootstrap validation styles
    document.querySelectorAll('.needs-validation').forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Course progress tracking
    const progressElements = document.querySelectorAll('.lesson-progress');
    progressElements.forEach(element => {
        element.addEventListener('click', async function(e) {
            if (e.target.matches('.complete-lesson')) {
                e.preventDefault();
                const lessonId = e.target.dataset.lessonId;
                try {
                    const response = await fetch(`/lesson/${lessonId}/complete`);
                    if (response.ok) {
                        window.location.reload();
                    }
                } catch (error) {
                    console.error('Error updating lesson progress:', error);
                }
            }
        });
    });

    // Dynamic search functionality
    const searchInput = document.querySelector('#courseSearch');
    if (searchInput) {
        let timeout = null;
        searchInput.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                const searchForm = this.closest('form');
                if (searchForm) {
                    searchForm.submit();
                }
            }, 500);
        });
    }

    // Confirmation dialogs
    document.querySelectorAll('[data-confirm]').forEach(element => {
        element.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

    // File upload preview
    const fileInput = document.querySelector('.custom-file-input');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const fileName = this.files[0].name;
            const label = this.nextElementSibling;
            label.textContent = fileName;
        });
    }

    // Notification handling
    const notificationBell = document.querySelector('.notification-bell');
    if (notificationBell) {
        notificationBell.addEventListener('click', async function() {
            try {
                await fetch('/notifications/mark-read', { method: 'POST' });
                const badge = this.querySelector('.notification-badge');
                if (badge) {
                    badge.style.display = 'none';
                }
            } catch (error) {
                console.error('Error marking notifications as read:', error);
            }
        });
    }
});

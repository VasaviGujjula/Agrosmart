// Auto-hide Flash Messages
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// Confirmation for critical actions
function confirmAction(message) {
    return confirm(message || "Are you sure you want to proceed?");
}
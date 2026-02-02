// Main JS interactions

document.addEventListener('DOMContentLoaded', () => {
    // Flash message auto-dismiss
    const flashes = document.querySelectorAll('.flash-message');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.opacity = '0';
            setTimeout(() => flash.remove(), 500);
        }, 4000);
    });

    // File Upload Preview (Simple Name Display)
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            const fileName = e.target.files[0]?.name;
            const label = document.querySelector('.file-label-text');
            if (label && fileName) {
                label.textContent = fileName;
            }
        });
    }
});

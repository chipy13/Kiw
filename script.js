// Form validation and interactive elements
document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Dynamic form interactions
    const diagnosisForm = document.querySelector('.skin-diagnosis-form');
    if (diagnosisForm) {
        diagnosisForm.addEventListener('submit', function(e) {
            // Add any client-side validation here
        });
    }
    
    // Skin type visualization in results page
    const skinTypeElement = document.getElementById('skin-type-result');
    if (skinTypeElement) {
        const skinType = skinTypeElement.textContent.trim();
        let badgeClass = 'bg-secondary';
        
        switch(skinType) {
            case 'Oily':
                badgeClass = 'bg-success';
                break;
            case 'Dry':
                badgeClass = 'bg-warning text-dark';
                break;
            case 'Combination':
                badgeClass = 'bg-info text-dark';
                break;
            case 'Normal':
                badgeClass = 'bg-primary';
                break;
            case 'Sensitive':
                badgeClass = 'bg-danger';
                break;
        }
        
        skinTypeElement.className = `skin-type-badge badge ${badgeClass}`;
    }
});

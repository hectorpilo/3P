document.addEventListener('DOMContentLoaded', function() {
    // Establecer la fecha actual en el campo de fecha
    const fechaInput = document.getElementById('fecha');
    if (fechaInput) {
        const today = new Date().toISOString().split('T')[0];
        fechaInput.value = today;
    }
    
    // Hacer que los mensajes flash desaparezcan después de 3 segundos
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.display = 'none';
        }, 3000);
    });
}); 
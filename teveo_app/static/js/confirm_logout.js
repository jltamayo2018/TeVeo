document.getElementById('delete-account-btn').addEventListener('click', function(event) {
    console.log('delete-account-btn clicked');
    event.preventDefault(); // Evitar el envío del formulario por defecto

    // Mostrar el cuadro de diálogo de confirmación
    if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
        // Si el usuario confirma, enviar el formulario
        document.querySelector('form').submit();
    } else {
        // Si el usuario cancela, no hacer nada
        return false;
    }
});
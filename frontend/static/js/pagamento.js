document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('alerta-container');

    if (container) {
        const alertas = container.querySelectorAll('.alerta-card');

        alertas.forEach(alerta => {
            const tempoExibicao = 6000;

            setTimeout(() => {
                alerta.classList.add('alerta-sumir');

                setTimeout(() => {
                    alerta.remove();
                }, 500);

            }, tempoExibicao);  
        });
    }
});


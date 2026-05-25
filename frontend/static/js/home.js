document.addEventListener('DOMContentLoaded', () => {
    // ===== CONTROLE DOS FAVORITOS VISUAL =====
    const botoesFavoritos = document.querySelectorAll('.heart-link');

    botoesFavoritos.forEach(botao => {
        botao.addEventListener('click', function(e) {
            // Nota: O link ainda vai disparar para o Django salvar no banco,
            // mas este código muda o ícone instantaneamente para melhorar a experiência.
            const icone = this.querySelector('.heart-icon');
            if (icone.textContent === '🤍') {
                icone.textContent = '❤️';
                showToast('Adicionado aos favoritos! ❤️');
            } else {
                icone.textContent = '🤍';
            }
        });
    });
});

/* ===== TOAST (SISTEMA DE NOTIFICAÇÃO) ===== */
function showToast(msg) {
    // Cria o Toast dinamicamente caso ele não exista no HTML
    let toast = document.getElementById('toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast';
        toast.style.position = 'fixed';
        toast.style.bottom = '20px';
        toast.style.right = '20px';
        toast.style.background = '#00e5ff';
        toast.style.color = '#111';
        toast.style.padding = '12px 25px';
        toast.style.borderRadius = '8px';
        toast.style.fontFamily = "'Audiowide', sans-serif";
        toast.style.fontWeight = 'bold';
        toast.style.zIndex = '1000';
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        toast.style.transform = 'translateY(20px)';
        toast.style.boxShadow = '0 0 15px rgba(0, 229, 255, 0.5)';
        document.body.appendChild(toast);
    }

    toast.textContent = msg;
    toast.style.opacity = '1';
    toast.style.transform = 'translateY(0)';

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(20px)';
    }, 3000);
}

/* ===== FUNÇÕES DOS SLIDERS (CARROSSEIS) ===== */
function scrollBanner(direction) {
    const slider = document.getElementById('bannerSlider');
    if (slider) {
        const width = slider.clientWidth;
        slider.scrollBy({ left: direction * width, behavior: 'smooth' });
    }
}

function scrollCategorias(direction) {
    const slider = document.getElementById('categoriasSlider');
    if (slider) {
        slider.scrollBy({ left: direction * 200, behavior: 'smooth' });
    }
}

function scrollProdutos(direction) {
    const slider = document.getElementById('produtosSlider');
    if (slider) {
        slider.scrollBy({ left: direction * 280, behavior: 'smooth' });
    }
}

// ===== AUTOPLAY DO BANNER PRINCIPAL =====
document.addEventListener('DOMContentLoaded', () => {
    const bannerSlider = document.getElementById('bannerSlider');
    
    // Configura para passar o banner a cada 4 segundos (4000 milissegundos)
    const tempoAutoPlay = 4000; 
    
    if (bannerSlider) {
        setInterval(() => {
            const larguraBanner = bannerSlider.clientWidth;
            // Se chegou ao fim do scroll, volta para o início (0)
            if (bannerSlider.scrollLeft + larguraBanner >= bannerSlider.scrollWidth - 10) {
                bannerSlider.scrollTo({ left: 0, behavior: 'smooth' });
            } else {
                // Caso contrário, avança para o próximo banner
                bannerSlider.scrollBy({ left: larguraBanner, behavior: 'smooth' });
            }
        }, tempoAutoPlay);
    }
});
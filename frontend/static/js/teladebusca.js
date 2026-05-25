function filtrarProdutosHome() {
    // 1. Pega o texto digitado e converte para minúsculo
    let input = document.getElementById('searchInput').value.toLowerCase();
    
    // 2. Seleciona todos os cards de produtos que estão no carrossel
    let produtos = document.querySelectorAll('#produtosSlider .produto-card');

    // 3. Percorre cada produto para verificar se o nome combina com a pesquisa
    produtos.forEach(function(card) {
        // Pega o título do produto dentro deste card específico
        let titulo = card.querySelector('.produto-titulo').textContent.toLowerCase();
        
        // Se o título incluir o que foi digitado, mostra o card. Senão, esconde.
        if (titulo.includes(input)) {
            card.style.display = ''; // Volta à exibição normal
        } else {
            card.style.display = 'none'; // Oculta o produto
        }
    });
}
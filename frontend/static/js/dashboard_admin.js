function filtrarProdutos() {
    // 1. Pega o texto digitado e converte para minúsculo
    let input = document.getElementById("searchInputAdmin");
    let filtro = input.value.toLowerCase();
    
    // 2. Pega todas as linhas (tr) dentro do corpo da tabela (tbody)
    let tabela = document.querySelector(".responsive-table tbody");
    let linhas = tabela.getElementsByTagName("tr");

    // 3. Percorre cada linha da tabela
    for (let i = 0; i < linhas.length; i++) {
        // Encontra o parágrafo que contém o nome do produto
        let nomeProdutoTag = linhas[i].querySelector(".product-info p");
        
        if (nomeProdutoTag) {
            // Pega o texto do nome do produto
            let nomeProduto = nomeProdutoTag.textContent || nomeProdutoTag.innerText;
            
            // Se o nome do produto incluir o que foi digitado (ignorando maiúsculas/minúsculas)
            if (nomeProduto.toLowerCase().indexOf(filtro) > -1) {
                linhas[i].style.display = ""; // Mostra a linha
            } else {
                linhas[i].style.display = "none"; // Esconde a linha
            }
        }
    }
}

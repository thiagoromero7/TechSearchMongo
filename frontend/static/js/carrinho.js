const botoesMais = document.querySelectorAll(".qtd-mais");
const botoesMenos = document.querySelectorAll(".qtd-menos");

botoesMais.forEach(botao => {
    botao.addEventListener("click", () => {

        const quantidade = botao.parentElement.querySelector(".qtd-numero");

        let valor = parseInt(quantidade.innerText);

        quantidade.innerText = valor + 1;
    });
});

botoesMenos.forEach(botao => {
    botao.addEventListener("click", () => {

        const quantidade = botao.parentElement.querySelector(".qtd-numero");

        let valor = parseInt(quantidade.innerText);

        if (valor > 1) {
            quantidade.innerText = valor - 1;
        }
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const cepInput = document.getElementById('cep');
    const ruaInput = document.getElementById('rua');
    const numeroInput = document.getElementById('numero');
    const bairroInput = document.getElementById('bairro');
    const cidadeInput = document.getElementById('cidade');
    const estadoInput = document.getElementById('estado');

    // Escuta o evento quando o utilizador sai do campo de texto (blur)
    cepInput.addEventListener('blur', function() {
        // Remove traços ou espaços, deixando apenas números
        let cep = this.value.replace(/\D/g, '');

        // Valida se o CEP tem o tamanho padrão de 8 dígitos
        if (cep.length === 8) {
            // Coloca um feedback visual temporário nos campos
            ruaInput.value = '...';
            bairroInput.value = '...';
            cidadeInput.value = '...';
            estadoInput.value = '...';

            // Consulta a API do ViaCEP
            fetch(`https://viacep.com.br/ws/${cep}/json/`)
                .then(response => response.json())
                .then(dados => {
                    if (!("erro" in dados)) {
                        // Preenche os campos de forma automática
                        ruaInput.value = dados.logradouro;
                        bairroInput.value = dados.bairro;
                        cidadeInput.value = dados.localidade;
                        estadoInput.value = dados.uf;
                        
                        // Passa o foco automaticamente para o número para poupar cliques
                        numeroInput.focus();
                    } else {
                        alert("CEP não encontrado no sistema postal.");
                        limparFormulario();
                    }
                })
                .catch(() => {
                    alert("Erro ao conectar ao serviço de CEP. Digite os dados manualmente.");
                    limparFormulario();
                });
        }
    });

    function limparFormulario() {
        cepInput.value = '';
        ruaInput.value = '';
        bairroInput.value = '';
        cidadeInput.value = '';
        estadoInput.value = '';
    }
});
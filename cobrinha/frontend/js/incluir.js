$(function () {

    $(document).on("click", "#btIncluir", function () {

        var dados_foto = new FormData($('#meuform')[0]);

        $.ajax({
            url: 'http://localhost:5000/save_image',
            method: 'POST',
            //dataType: 'json',
            data: dados_foto, // dados serão enviados em formato normal, para upload da foto
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                alert("enviou a foto direitinho!");
                insereJogadorNoBanco();
            },
            error: function (data) {
                alert("deu ruim na foto");
            }
        });





        function insereJogadorNoBanco() {

            //pegar dados da tela
            nome = $("#campoNome").val();
            pontuacao = $("#campoPontuacao").val();

            // C:\\fakepath\\olho.jpg"
            // esse fakepath vem de algum lugar da biblioteca utilizada
            // só conta a contrabarra uma vez, inicia do zero
            nome_foto = $("#campoFoto").val().substr(12);

            // preparar dados no formato json
            var dados = JSON.stringify({ nome: nome, pontuacao: pontuacao, nome_foto: nome_foto });
            // fazer requisição para o back-end
            $.ajax({
                url: 'http://localhost:5000/incluir_jogador',
                method: 'POST',
                dataType: 'json', // os dados são recebidos no formato json
                //contentType: 'application/json', // dados enviados em json
                data: dados, // estes são os dados enviados
                success: jogador_incluido, // chama a função listar para processar o resultado
                error: erroAoIncluirJogador
            });
            function jogador_incluido(retorno) {
                if (retorno.resultado == "ok") { // a operação deu certo?
                    // informar resultado de sucesso
                    alert("jogador cadastrado com sucesso!");
                    $("#campoNome").val();
                    $("#campoPontuacao").val();
                } else {
                    // informar mensagem de erro
                    alert(retorno.resultado + ":" + retorno.detalhes);
                }
            }
            function erroAoIncluirJogador(retorno) {
                // informar mensagem de erro
                alert("ERRO: " + retorno.resultado + ":" + retorno.detalhes);
            }
        }

    });
});
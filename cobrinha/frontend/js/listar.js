$(function () {

    $(document).on("click", "#btListar", function () {

        // chamada ao backend
        $.ajax({
            url: 'http://localhost:5000/retornar_jogadores',
            method: 'GET',
            dataType: 'json', // os dados são recebidos no formato json
            success: listar_jogadores, // chama a função listar para processar o resultado
            error: function () {
                alert("erro ao ler dados, verifique o backend");
            }
        });

        // função executada quando tudo dá certo
        function listar_jogadores(retorno) {
            if (retorno.resultado == 'ok') {
                $('#corpoTabelaJogadore').empty();
                jogadores = retorno.detalhes;
                for (var i in jogadores) { 
                    lin = `<tr>
                           <td>${jogadores[i].nome}</td>
                           <td>${jogadores[i].pontuacao}</td>
                           <td><img src="http://localhost:5000/get_image/${jogadores[i].id}" height=100 width=100></td>
                           </tr>`;
                    // adiciona a linha no corpo da tabela
                    $('#corpoTabelaJogadores').append(lin);
                }
            } else {
                alert("erro no retorno: " + retorno.detalhes);
            }
        }

    });
});
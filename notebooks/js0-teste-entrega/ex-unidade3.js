function metodosVetor(vetor) {
    vetor.sort();
    vetor.pop();
    vetor.unshift('abacate');
    escreva(0.6, 'metodos do vetor', vetor);
    return vetor;
}

metodosVetor([4, 0, 9]);
metodosVetor(['doritos', 'cavalo', 'filme']);

function metodosString(str) {
    str = str.toUpperCase();
    str = str.replaceAll('O', 'A');
    escreva(0.7, 'string', str);
    return str;
}

metodosString('calvo');
metodosString('tome');

function escreveDataPorExtenso(data) {
    data = data.split('/');
    return data[0] + ' de ' + obtemNomeDoMes(data[1]) + ' de ' + data[2];
}

escreva(9, 'data por extenso', escreveDataPorExtenso('15/7/2006'));
escreva(9, 'data por extenso', escreveDataPorExtenso('15/4/1974'));
escreva(9, 'data por extenso', escreveDataPorExtenso('12/9/2014'));

function eliminaCaracteres(texto, caracteresParaEliminar) {
    for (let caractere of caracteresParaEliminar) {
        texto = texto.replaceAll(caractere, '');
    }
    

    return texto;
}

escreva(10, 'elimina', eliminaCaracteres('voce', 'oe'));


function substituiCaracteres(texto, caracteresProcura, caracteresSubstituirPor) {
    for(let i = 0; i < caracteresProcura.length; i++) {
        let caractereProcura = caracteresProcura[i];
        let caractereSubstituirPor = caracteresSubstituirPor[i];
        texto = texto.replaceAll(caractereProcura, caractereSubstituirPor);
    }
    

    return texto;
}

escreva(10, 'substitui', substituiCaracteres('cava', 'ac', 'ov'));

function inverteTexto(texto) {
    let textoInvertido = [];
    for (let i = 0; i < texto.length; i++) {
        textoInvertido[texto.length - i] = texto[i];
    }
    textoInvertido = textoInvertido.join('');
        
    return textoInvertido;
}

escreva(10, 'inverte', inverteTexto('salta'));

function verificaPalindromo(texto) {
    texto = texto.toLowerCase();
    texto = eliminaCaracteres(texto, ',-!?; ');
    texto = substituiCaracteres(texto, 'áéíóúãõâêîôûç', 'aeiouaoaeiouc');
    return texto === inverteTexto(texto);
}

escreva(11, 'rapar é palíndromo', verificaPalindromo('rapar'));
escreva(11, 'rAp?á,r é palíndromo', verificaPalindromo('rAp?á,r'));
escreva(11, 'comer é palíndromo', verificaPalindromo('comer'));

function dizOiPara(funcaoDeDarOi, nomeDaPessoa) {
    
    // veja que aqui, independente do nome da função
    // externa, invocamos ela como funcaoDeDarOi
    textoDoOi = funcaoDeDarOi(nomeDaPessoa);
    
    escrevaMensagem(12, '=========== Início do chat ===========');
    escrevaMensagem(12, textoDoOi);
    escrevaMensagem(12, '======================================');
    escrevaMensagem(12, '<br>');
}


function oiEmPortuguesFormal(nome) {
    return 'Oi Sr(a). ' + nome + ', como vai?';
}

let oiEmPortugues = function(nome) {
    return 'Oi ' + nome + ', blza?';
};


// dá oi para 'Daniel' de várias formas diferentes
dizOiPara(oiEmPortuguesFormal, 'Daniel');
dizOiPara(oiEmPortugues, 'Daniel');
dizOiPara(function(nome) {
    return 'Hi ' + nome + ', how are you?';
}, 'Daniel');

function oiEmPortuguesInformal(nome) {
    return 'Fala ' + nome + ', de boa?';
}

let oiEmPortuguesSms = function(nome) {
    return 'Oii ' + nome + ', trql?';
};

dizOiPara(oiEmPortuguesInformal, 'Eduardo');
dizOiPara(oiEmPortuguesSms, 'Eduardo');
dizOiPara(function(nome) {
    return 'Hello ' + nome + ', my confederate adventurer, how can I serve you today?';
}, 'Eduardo');

function aplicaOperacaoEmCadaElemento(operacao, vetor1, vetor2) {
    let vetor = [];
    vetor1.forEach((num, i) => {
        vetor[i] = operacao(num, vetor2[i])
    });
    escreva(13, operacao + '<br><br>vetor 1 [' + vetor1 + '] vetor 2 [' + vetor2 + ']', vetor1.length === vetor2.length ? vetor : null);
    return vetor1.length === vetor2.length ? vetor : null;
}

let multiplica = function(a, b) {
    return a * b;
};

function subtracao(a, b) {
    return a - b;
}

aplicaOperacaoEmCadaElemento(function(a, b) {
    return a + b;
}, [10, 21], [3, 1]);
aplicaOperacaoEmCadaElemento(multiplica, [13, 44], [22, 69]);
aplicaOperacaoEmCadaElemento(subtracao, [35, 35], [13, 22]);

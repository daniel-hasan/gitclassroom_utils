function contandoElementosDoVetor(elementos, elementoSendoProcurado) {
    let quantidade = 0;
    elementos.forEach(function (elemento) {
        if (elemento === elementoSendoProcurado) {
            quantidade++;
        }
    });
    
    escreva(0.4, 'Quantidade', quantidade);
    return quantidade;
}

contandoElementosDoVetor([543, 345, 2, 0, 666, 3, 655, 666, 666], 666);
contandoElementosDoVetor(['cavalo', 'tome', 'que isso meu filho calme', 'cavalo'], 'cavalo');

function obtemNomeDoMes(numero) {
    if (numero < 1 || numero > 12) {
        escrevaMensagem(0.5, 'Mês inválido: ' + numero);
        return null;
    }

    let meses = [
        'janeiro',
        'fevereiro',
        'março',
        'abril',
        'maio',
        'junho',
        'julho',
        'agosto',
        'setembro',
        'outubro',
        'novembro',
        'dezembro'
    ];

    return meses[numero - 1];
}

escreva(0.5, 'mes', obtemNomeDoMes(4));

function calculaVelocidadeAlturaBola(velocidadeInicial, gravidade, n) {
    for ( ; n > 0; n--) {
        escreva(3, 'h(' + n + ')', calculaAlturaBola(n, velocidadeInicial, gravidade));
        escreva(3, 'v(' + n + ')', calculaVelocidadeBola(n, velocidadeInicial, gravidade));
    }
}

calculaVelocidadeAlturaBola(50, 9.81, 20);

function somatorio(n) {
    let s = 0;
    for (n -= n % 2; n > 1; n -= 2) {
        s += 1 / n;
    }

    escreva(4, 'somatorio', s);
    return s;
}

somatorio(1);
somatorio(10);
somatorio(100);

function obtemPosicaoDoElemento(elements, wantedElement) {
    let i = 0;
    for (let element of elements) {
        if (wantedElement === element)
            return i;
        i++;
    }
    
    return null;
}

escreva(5, 'Posição', obtemPosicaoDoElemento([1234, 432, 234, 5, 324], 234));

function calculaMediaEntreExtremos(numbs) {
    let min, max;
    max = min = numbs[0];
    for (num of numbs) {
        if (num < min)
            min = num;
        if (num > max)
            max = num;
    }

    return (max + min) / 2;
}

escreva(6, 'Média', calculaMediaEntreExtremos([2, 3, 90, 32453452, -23476450]));

//Max before 'Infinity': 1476
function fibonacci(tamanhoSequencia) {
    let sequencia = []
    switch (tamanhoSequencia) {
        case 0:
            break
        case 1:
            sequencia = [0]
            break
        default:
            sequencia = [0, 1]
            for (let i = 2; i < tamanhoSequencia; i++)
                sequencia[i] = sequencia[i - 1] + sequencia[i - 2]
    }

    escreva(7, 'Fib(' + tamanhoSequencia + ')', sequencia)
    return sequencia
}

fibonacci(1);
fibonacci(2);
fibonacci(3);
fibonacci(5);
fibonacci(8);
fibonacci(13);

function exibeAmigos(pessoas, amizades, x) {
    let amigos = [], numPessoa = obtemPosicaoDoElemento(pessoas, x);

    for (let i = 0, a = 0; i < pessoas.length; i++) {
        if (amizades[numPessoa][i] === 1)
            amigos[a++] = pessoas[i];
    }

    return amigos;
}

escreva(8, 'pessoas = [\'Alice\', \'Bob\', \'Carol\', \'Daniele\']<br>amizades = [<br>[0, 0, 0, 1],<br>[1, 0, 1, 1],<br>[0, 0, 0, 1],<br>[1, 1, 0, 0]<br>]<br>x = \'Bob\'', exibeAmigos(['Alice', 'Bob', 'Carol', 'Daniele'], [[0, 0, 0, 1], [1, 0, 1, 1], [0, 0, 0, 1], [1, 1, 0, 0]],'Bob'));
escreva(8, 'pessoas = [\'noob noob\', \'talarico\', \'faro\']<br>amizades = [<br>[0, 0, 1],<br>[1, 0, 0],<br> [1, 1, 0]<br>]<br>x = \'faro\'', exibeAmigos(['noob noob', 'talarico', 'faro'], [[0, 0, 1], [1, 0, 0], [1, 1, 0]], 'faro'));

function exibeAmigosEmComum(pessoas, amizades, x, y) {
    let pessoaX = exibeAmigos(pessoas, amizades, x), pessoaY = exibeAmigos(pessoas, amizades, y), comum = [], i = 0;

    for (let pessoa of pessoaX) {
        pessoaY.forEach(element => {
            if (element === pessoa) comum[i++] = pessoa;
        });
    }

    return comum;
}

escreva(8, 'pessoas = [\'Alice\', \'Bob\', \'Carol\', \'Daniele\']<br>amizades = [<br>[0, 0, 0, 1],<br>[1, 0, 1, 1],<br>[0, 0, 0, 1],<br>[1, 1, 0, 0]<br>]<br>x = \'Bob\'<br>y = \'Daniele\'', exibeAmigosEmComum(['Alice', 'Bob', 'Carol', 'Daniele'], [[0, 0, 0, 1], [1, 0, 1, 1], [0, 0, 0, 1], [1, 1, 0, 0]],'Bob', 'Daniele'));
escreva(8, 'pessoas = [\'noob noob\', \'talarico\', \'faro\']<br>amizades = [<br>[0, 0, 1],<br>[1, 0, 0],<br> [1, 1, 0]<br>]<br>x = \'faro\'<br>y = \'noob noob\'', exibeAmigosEmComum(['noob noob', 'talarico', 'faro'], [[0, 0, 1], [1, 0, 0], [1, 1, 0]], 'faro', 'noob noob'));

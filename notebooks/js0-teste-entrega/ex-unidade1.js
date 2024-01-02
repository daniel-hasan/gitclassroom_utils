// Exercício 0.1: entendo a saída dos testes
function testeSaidas() {
    escrevaMensagem(0.1, 'Exercício 0.1');
    let a = 1;
    let b = 2;
    let c = [1, 3, 2, 123, 2321, 32, 1];
    let d = [
        [12, 21, 21, 1, 2],
        [12,  1,  2, 3, 1, 1],
        [1,   1,  2, 3, 1, 4]
    ];
    let m = [
        [0, 0, 0, 1],
        [1, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 1, 0, 0]
    ]
    let pessoas = ['Alice', 'Bob', 'Carol', 'Daniele'];
    let e = true;
    
    escreva(0.1, 'Variável a', a); // < variável
    //      ^ nº exerc. ^ rótulo (descrição)     

    // escrever também (i) b, (ii) soma de a e b, (iii) d, (iv) e   (≃ 4 linhas)




}

// invocar testeSaidas e ver o resultado na página                  (≃ 1 linha)





// ----------------------------------------------------------------------------
// Exercício 0.2: função soma                                    (≃ 4-5 linhas)

function soma(a, b) {
    escreva(0.2, 'soma', a + b);
    return a + b;
}

soma(5, -2);

// ----------------------------------------------------------------------------
// Exercício 0.3: fazendo cálculos matemáticos                  (≃ 7-10 linhas)

function calculaValoresDoNumero(x) {
    escreva(0.3, 'quadrado', x ** 2)
    escreva(0.3, 'metade', x / 2);
    escreva(0.3, 'raiz', Math.sqrt(x));
}

calculaValoresDoNumero(13);
calculaValoresDoNumero(17);

// ----------------------------------------------------------------------------
// Exercício 1: altura da bola no instante                      (≃ 5-10 linhas)

function calculaAlturaBola(tempo, velocidadeInicial, gravidade) {
    let altura = velocidadeInicial * tempo - gravidade * tempo ** 2 / 2;
    return altura;
}

escreva(1, 'h(1.5)', calculaAlturaBola(1.5, 50, 9.81));
escreva(1, 'h(10)', calculaAlturaBola(10, 50, 9.81));

// ----------------------------------------------------------------------------
// Exercício 2: velocidade da bola no instante                  (≃ 6-12 linhas)


function calculaVelocidadeBola(tempo, velocidadeInicial, gravidade) {
    return velocidadeInicial - gravidade * tempo;
}

escreva(2, 'h(1.5)', calculaVelocidadeBola(1.5, 50, 9.81));
escreva(2, 'h(10)', calculaVelocidadeBola(10, 50, 9.81));

class Pokemon:
    def __init__(self, numero, nome, tipo, altura, peso,habilidade, ataque, defesa, imagem=None):
        self.numero = numero
        self.nome = nome
        self.tipo = tipo
        self.altura = altura
        self.peso = peso
        self.habilidade = habilidade
        self.ataque = ataque
        self.defesa = defesa
        self.imagem = imagem

    def atualizar(self, nome, tipo, altura, peso,habilidade, ataque, defesa):
        self.nome = nome
        self.tipo = tipo
        self.altura = altura
        self.peso = peso
        self.habilidade = habilidade
        self.ataque = ataque
        self.defesa = defesa

    def dados(self):
        return (
            self.numero,
            self.nome,
            self.tipo,
            self.altura,
            self.peso,
            self.habilidade,
            self.imagem,
            self.ataque,
            self.defesa
        )

from pokemon import Pokemon
from imagem_pokemon import baixar_imagem
from pokemonDAO import pokemonDAO


class ControlePokemon:
    def __init__(self):
        self.dao = pokemonDAO()

    def _dados_validos(self, nome, tipo):
        return bool(nome.strip() and tipo.strip())

    def _pokemon_existe(self, id_pokemon):
        return any(p[0] == id_pokemon for p in self.dao.listar_todos())

    def cadastrar(self, numero, nome, tipo, altura, peso, habilidade, ataque, defesa):
        if not self._dados_validos(nome, tipo):
            return False

        imagem = baixar_imagem(numero)
        if not imagem:
            return False

        pokemon = Pokemon(numero, nome, tipo, altura, peso, habilidade, ataque, defesa, imagem)
        return self.dao.inserir(*pokemon.dados())

    def listar(self):
        return self.dao.listar_todos()

    def consultar(self, nome):
        if not nome.strip():
            return []
        return self.dao.buscar_nome(nome)

    def atualizar(self, id_pokemon, numero, nome, tipo, altura, peso, habilidade, ataque, defesa):
        if not self._dados_validos(nome, tipo) or not self._pokemon_existe(id_pokemon):
            return False

        imagem = baixar_imagem(numero)
        if not imagem:
            return False

        return self.dao.atualizar(
            id_pokemon, numero, nome, tipo, altura, peso, habilidade, imagem, ataque, defesa
        )

    def excluir(self, id_pokemon):
        if not self._pokemon_existe(id_pokemon):
            return False
        return self.dao.deletar(id_pokemon)
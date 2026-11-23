from conexaosql import criar_conexao
from mysql.connector import Error
class pokemonDAO:
    def inserir(self,numero,nome,tipo,altura=None,peso=None,habilidade=None,img=None,ataque=None,defesa=None):
        conexao = criar_conexao()
        if conexao:
            cursor = None
            try:
                cursor = conexao.cursor()
                sql=('INSERT INTO pokemon(numero,nome,tipo,altura,peso,habilidade,img,ataque,defesa)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)')
                valores=(numero,nome,tipo,altura,peso,habilidade,img,ataque,defesa)
                cursor.execute(sql,valores)
                conexao.commit()
                return True
            except Error as e:
                print(f"erro ao inserir: {e}")
                return False
            finally:
                if cursor:
                    cursor.close()
                conexao.close()
        return False
    def listar_todos(self):
        conexao = criar_conexao()
        if conexao:
            cursor=None
            try:
                cursor=conexao.cursor()
                cursor.execute('SELECT id, numero,nome,tipo,altura,peso,habilidade,img,ataque,defesa FROM pokemon ORDER BY numero')
                return cursor.fetchall()
            except Error as e:
                print(f"erro ao listar painho: {e}")
                return[]
            finally:
                if cursor:
                    cursor.close()
                conexao.close()
        return[]
    def buscar_nome(self,nome):
        conexao=criar_conexao()
        if conexao:
            cursor=None
            try:
                cursor=conexao.cursor()
                cursor.execute("SELECT id, numero,nome,tipo,altura,peso,habilidade,img,ataque,defesa FROM pokemon WHERE nome LIKE %s ORDER BY numero",(f'%{nome}%',))
                return cursor.fetchall()
            except Error as e:
                print(f'Erro ao buscar ze: {e}')
                return[]
            finally:
                if cursor:
                    cursor.close()
                conexao.close()
        return[]
    def atualizar(self,id_pokemon,numero,nome,tipo,altura=None,peso=None,habilidade=None,img=None,ataque=None,defesa=None):
        conexao=criar_conexao()
        if conexao:
            cursor=None
            try:
                cursor=conexao.cursor()
                sql=('UPDATE pokemon SET numero=%s,nome=%s,tipo=%s,altura=%s,peso=%s,habilidade=%s,img=%s,ataque=%s,defesa=%s WHERE id=%s')
                valores=(numero,nome,tipo,altura,peso,habilidade,img,ataque,defesa,id_pokemon)
                cursor.execute(sql,valores)
                conexao.commit()
                return True
            except Error as e:
                print(f'nn deu pra atualizar fi: {e}')
                return False
            finally:
                if cursor:
                    cursor.close()
                conexao.close()
        return False
    def deletar(self,id_pokemon):
        conexao=criar_conexao()
        if conexao:
            cursor=None
            try:
                cursor=conexao.cursor()
                cursor.execute('DELETE FROM pokemon WHERE id=%s',(id_pokemon,))
                conexao.commit()
                return True
            except Error as e:
                print(f'nn deu pra deletar ze: {e}')
                return False
            finally:
                if cursor:
                    cursor.close()
                conexao.close()
        return False
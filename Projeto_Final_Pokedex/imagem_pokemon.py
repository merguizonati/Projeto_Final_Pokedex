import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def baixar_imagem(numero):
    try:
        num_limpo = int(str(numero).strip())
        dominio = "https://raw.githubusercontent.com"
        caminho = "/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/"
        url = f"{dominio}{caminho}{num_limpo}.png"
        
        headers = {"User-Agent": "Mozilla/5.0"}
        resposta = requests.get(url, headers=headers, timeout=10, verify=False)
        
        if resposta.status_code == 200:
            return resposta.content
        else:
            print(f"Imagem não encontrada na API (Status {resposta.status_code})")
            return None
    except Exception as e:
        print(f"Erro ao baixar imagem: {e}")
        return None
import requests

# Defina a chave de API do Hunter
HUNTER_API_KEY = "SUA_API_KEY_HUNTER"

def buscar_emails_por_dominio(dominio):
    """
    Função para buscar os e-mails associados a um domínio utilizando a API do Hunter.

    Parâmetros:
    - dominio (str): O domínio para o qual os e-mails serão pesquisados.

    Retorna:
    - List[str]: Uma lista de e-mails encontrados para o domínio fornecido.
    """
    # Construção da URL da API do Hunter para buscar os e-mails pelo domínio
    url = f"https://api.hunter.io/v2/domain-search?domain={dominio}&api_key={HUNTER_API_KEY}"

    try:
        # Realizando a requisição GET à API
        response = requests.get(url)
        
        # Verificando se a resposta foi bem-sucedida
        if response.status_code == 200:
            # Se a resposta for bem-sucedida, parse o JSON e extrai os e-mails
            data = response.json()
            return [item["value"] for item in data.get("data", {}).get("emails", [])]
        else:
            # Caso o status code não seja 200, retornamos uma lista vazia
            print(f"Erro ao acessar a API: Status Code {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        # Caso ocorra algum erro na requisição, loga o erro
        print(f"Erro de requisição: {e}")
        return []

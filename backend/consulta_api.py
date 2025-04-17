import requests
import time

def consultar_cnpj(cnpj):
    """
    Função que consulta informações sobre uma empresa usando a API da ReceitaWS.
    Retorna um dicionário com o nome e o domínio do site da empresa.

    :param cnpj: CNPJ da empresa a ser consultada
    :return: Dicionário com o nome da empresa e domínio do site
    """
    try:
        # URL da API da ReceitaWS para consulta de CNPJ
        url = f"https://receitaws.com.br/v1/cnpj/{cnpj}"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        # Envia a requisição para a API
        response = requests.get(url, headers=headers)

        # Se o limite de requisições foi atingido (status 429)
        if response.status_code == 429:
            print(f"Limite atingido para o CNPJ: {cnpj}")
            time.sleep(1)  # Atraso para respeitar o limite da API
            return {"empresa": "Desconhecida", "site": "empresa.com.br"}

        # Se a consulta foi bem-sucedida (status 200)
        if response.status_code == 200:
            dados = response.json()
            nome = dados.get("nome", "Desconhecida")  # Nome da empresa
            email = dados.get("email", "")  # Email da empresa, se disponível
            site = dados.get("site", "")  # Site da empresa, se disponível
            
            # Limpeza do site para extrair o domínio
            dominio = site.replace("http://", "").replace("https://", "").replace("www.", "").strip().split("/")[0]

            # Se o domínio estiver vazio, tenta obter do email
            if not dominio:
                dominio = email.split("@")[-1] if "@" in email else "empresa.com.br"

            # Retorna o nome da empresa e o domínio do site
            return {
                "empresa": nome or "Desconhecida",
                "site": dominio or "empresa.com.br"
            }
        else:
            # Se houve erro na consulta (qualquer status diferente de 200)
            print(f"Erro na consulta do CNPJ {cnpj}: {response.status_code}")
            return {"empresa": "Desconhecida", "site": "empresa.com.br"}

    except Exception as e:
        # Em caso de erro inesperado
        print(f"Erro ao consultar CNPJ {cnpj}: {e}")
        return {"empresa": "Desconhecida", "site": "empresa.com.br"}

def consultar_varios_cnpjs(lista_cnpjs):
    """
    Função que consulta vários CNPJs e retorna os resultados de forma agrupada.

    :param lista_cnpjs: Lista contendo os CNPJs a serem consultados
    :return: Lista de resultados com nome e site de cada empresa
    """
    resultados = []
    for cnpj in lista_cnpjs:
        # Chama a função de consulta para cada CNPJ
        resultado = consultar_cnpj(cnpj)
        resultados.append(resultado)
        time.sleep(1)  # Respeita o limite da API gratuita entre as requisições
    return resultados

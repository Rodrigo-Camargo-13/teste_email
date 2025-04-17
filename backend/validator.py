from difflib import SequenceMatcher

def validar_emails(emails):
    """
    Função responsável por validar a correspondência entre os e-mails gerados e os esperados, além de comparar
    a validação real do SMTP.

    Parâmetros:
        emails (list): Lista de dicionários com os dados dos e-mails a serem validados. Cada dicionário deve 
                       conter as chaves 'nome', 'sobrenome', 'email', 'dominio' e 'smtp_valido'.

    Retorna:
        list: Lista de dicionários com a validação simulada e real do e-mail, além da comparação entre o 
              e-mail gerado e o esperado.
    """
    resultados = []

    # Iteração sobre a lista de e-mails para validação
    for item in emails:
        nome = item["nome"]
        sobrenome = item["sobrenome"]
        email_gerado = item["email"]
        dominio = item["dominio"]

        # Gerar o e-mail esperado no formato nome.sobrenome@dominio
        esperado = f"{nome}.{sobrenome}@{dominio}"

        # Calcular a similaridade entre o e-mail gerado e o esperado
        similaridade = SequenceMatcher(None, email_gerado, esperado).ratio()

        # Definir a validade simulada com base no limiar de similaridade
        valido_simulado = similaridade > 0.85

        # Adicionar os resultados de cada validação na lista de resultados
        resultados.append({
            "email": email_gerado,
            "valido_simulado": valido_simulado,
            "valido_real": item.get("smtp_valido", False),
            "esperado": valido_simulado,  # Se o e-mail gerado for válido, o esperado será True
            "real": item.get("smtp_valido", False)  # Validade real do e-mail
        })

    return resultados

# Lista de domínios reais conhecidos para validação de e-mails
REAL_DOMAINS = [
    "magazineluiza.com.br",
    "vale.com",
    "bb.com.br",
    "petrobras.com.br"
]

def verificar_email_smtp(email):
    """
    Função para verificar se o e-mail é válido com base em seu domínio e formato.
    O e-mail é considerado válido se:
    - Contiver um '@' e o nome antes do domínio tiver um ponto (nome.sobrenome).
    - O domínio do e-mail estiver na lista de domínios conhecidos.

    Args:
        email (str): O e-mail a ser verificado.

    Returns:
        bool: Retorna True se o e-mail for válido, caso contrário, False.
    """
    # Verifica se o e-mail contém o caractere '@'
    if "@" not in email:
        return False

    # Divide o e-mail em nome e domínio
    nome, dominio = email.split("@")

    # Valida se o domínio do e-mail está na lista de domínios reais conhecidos
    # E também verifica se o nome antes do '@' contém um ponto (indicando um formato nome.sobrenome)
    if dominio in REAL_DOMAINS and "." in nome:
        return True

    return False

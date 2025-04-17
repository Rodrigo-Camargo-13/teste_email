def gerar_possiveis_emails(nomes, dominio):
    """
    Gera uma lista de possíveis e-mails com base em uma lista de nomes e um domínio fornecido.
    
    Args:
        nomes (list of dicts): Lista de dicionários contendo 'nome' e 'sobrenome' de pessoas.
        dominio (str): O domínio de e-mail a ser utilizado.
        
    Returns:
        list of dicts: Lista de dicionários contendo os e-mails gerados, nome, sobrenome e domínio.
    """

    # Lista de formatos de e-mail possíveis
    formatos = [
        "{nome}.{sobrenome}", "{nome}", "{sobrenome}", "c.{sobrenome}",
        "{nome}.s", "c.s", "csilva", "{sobrenome}{nome}", "{nome}_{sobrenome}",
        "{nome}-{sobrenome}", "{nome}.{sobrenome}1", "{nome}1", "c.{sobrenome}1",
        "{nome}99", "{nome}{sobrenome}2024", "c_{sobrenome}", "{sobrenome}.c",
        "{sobrenome}{nome[0]}", "{sobrenome}.{nome}", "{nome}.{sobrenome}s"
    ]
    
    # Lista de cargos institucionais
    cargos = ["diretoria", "financeiro", "contato", "rh", "ti", "suporte"]

    emails = []

    # Gerar e-mails baseados nos nomes fornecidos
    for pessoa in nomes:
        nome = pessoa["nome"].lower()
        sobrenome = pessoa["sobrenome"].lower()

        # Gerar e-mails com base nos formatos
        for formato in formatos:
            try:
                # Formatar o e-mail
                local = formato.format(nome=nome, sobrenome=sobrenome)
                email = f"{local}@{dominio}"
                emails.append({
                    "email": email,
                    "dominio": dominio,
                    "nome": nome,
                    "sobrenome": sobrenome
                })
            except Exception as e:
                # Logar erro sem interromper o processo
                print(f"Erro ao formatar: {formato} - {e}")

    # Gerar e-mails institucionais para cargos
    for cargo in cargos:
        emails.append({
            "email": f"{cargo}@{dominio}",
            "dominio": dominio,
            "nome": cargo,
            "sobrenome": "",
            "tipo": "cargo"
        })

    return emails

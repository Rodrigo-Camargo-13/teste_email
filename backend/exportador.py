import csv
import os

def exportar_emails_para_csv(emails_validos, empresa, dominio):
    """
    Função para exportar a lista de e-mails validados para um arquivo CSV.

    Parâmetros:
    emails_validos (list): Lista de dicionários com os e-mails e seu status de validação.
    empresa (str): Nome da empresa associada aos e-mails.
    dominio (str): Domínio dos e-mails que serão exportados.

    Retorna:
    None
    """
    
    # Criação do nome do arquivo de exportação
    nome_arquivo = f"resultado_{empresa.lower().replace(' ', '_')}.csv"
    
    # Garantir que o diretório 'exportados' existe
    os.makedirs("exportados", exist_ok=True)
    
    # Caminho completo onde o arquivo será salvo
    caminho = os.path.join("exportados", nome_arquivo)

    try:
        # Abrir o arquivo para escrita, criando o arquivo se necessário
        with open(caminho, mode="w", newline="", encoding="utf-8") as arquivo_saida:
            writer = csv.DictWriter(arquivo_saida, fieldnames=["empresa", "dominio", "email", "smtp_valido"])
            
            # Escrever o cabeçalho no CSV
            writer.writeheader()
            
            # Escrever cada e-mail validado no arquivo
            for item in emails_validos:
                writer.writerow({
                    "empresa": empresa,
                    "dominio": dominio,
                    "email": item["email"],
                    "smtp_valido": item["smtp_valido"]
                })
        
        # Mensagem de sucesso na exportação
        print(f"Arquivo exportado com sucesso para: {caminho}")
    
    except Exception as e:
        # Em caso de erro, mostrar uma mensagem de falha
        print(f"Erro ao exportar o arquivo: {e}")

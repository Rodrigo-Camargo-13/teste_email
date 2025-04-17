from email_generator import gerar_possiveis_emails
from validator import validar_emails
from confusion_matrix import gerar_matriz_confusao
from smtp_checker import verificar_email_smtp
from exportador import exportar_emails_para_csv

def gerar_e_validar_emails():
    # Empresas com domínios reais
    empresas = [
        {"empresa": "Magazine Luiza", "site": "magazineluiza.com.br"},
        {"empresa": "Banco do Brasil", "site": "bb.com.br"},
        {"empresa": "Petrobras", "site": "petrobras.com.br"},
        {"empresa": "Vale S.A.", "site": "vale.com"},
    ]

    # Funcionários simulados
    nomes = [
        {"nome": "Carlos", "sobrenome": "Silva"},
        {"nome": "Ana", "sobrenome": "Souza"},
        {"nome": "João", "sobrenome": "Pereira"}
    ]

    for empresa in empresas:
        print(f"\nEmpresa: {empresa['empresa']}")
        print(f"Domínio: {empresa['site']}\n")

        # Geração de e-mails possíveis
        emails_gerados = gerar_possiveis_emails(nomes, empresa["site"])

        # Validação via SMTP
        print("Verificando e-mails com SMTP real...")
        for item in emails_gerados:
            item["smtp_valido"] = verificar_email_smtp(item["email"])
            status = "Válido" if item["smtp_valido"] else "Inválido"
            print(f"{item['email']} => {status}")

        # Validação do formato de e-mail
        resultados = validar_emails(emails_gerados)

        # Geração da matriz de confusão
        gerar_matriz_confusao(resultados)

        # Exportar os dados para CSV
        exportar_emails_para_csv(emails_gerados, empresa["empresa"], empresa["site"])

if __name__ == "__main__":
    gerar_e_validar_emails()

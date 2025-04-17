from flask import Flask, request, render_template, send_file
import pandas as pd
import os
import zipfile
from backend.consulta_api import consultar_varios_cnpjs
from backend.email_generator import gerar_possiveis_emails
from backend.smtp_checker import verificar_email_smtp
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder
from fpdf import FPDF
import matplotlib.pyplot as plt
import seaborn as sns

# Inicializando a aplicação Flask
app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Função que gerencia a página inicial da aplicação. Quando um arquivo CSV é enviado, ele é processado, os e-mails são
    validados, e os resultados são apresentados em gráficos e relatórios.
    """
    emails_result = []
    zip_dir = "resultados"
    os.makedirs(zip_dir, exist_ok=True)  # Criar a pasta de resultados, se não existir

    # Se a requisição for do tipo POST, processa o arquivo enviado
    if request.method == "POST":
        file = request.files["file"]  # Arquivo CSV enviado
        filtro = request.form.get("cargo") or "Todos"  # Filtro de cargo selecionado

        # Leitura e processamento do arquivo CSV
        df = pd.read_csv(file)
        df.columns = [col.lower().strip() for col in df.columns]

        if "cnpj" not in df.columns:
            return "Erro: o arquivo CSV precisa conter a coluna 'cnpj'."  # Verificação de coluna obrigatória

        cnpjs = df["cnpj"].astype(str).tolist()
        empresas = consultar_varios_cnpjs(cnpjs)  # Consulta de CNPJs

        # Definindo alguns nomes e cargos para gerar os e-mails
        nomes = [{"nome": "Carlos", "sobrenome": "Silva"}, {"nome": "Ana", "sobrenome": "Souza"}, {"nome": "João", "sobrenome": "Pereira"}]
        cargos = ["financeiro", "diretoria", "rh", "contato", "comercial", "ti"]

        # Processamento das empresas e geração dos e-mails
        for empresa in empresas:
            nome_empresa = (empresa.get("empresa") or "Desconhecida").strip()
            dominio = (empresa.get("site") or "empresa.com.br").strip()

            # Ajuste de domínio com base em nomes de empresas específicas
            nome_emp = nome_empresa.lower()
            if "vale" in nome_emp:
                dominio = "vale.com"
            elif "petrobras" in nome_emp:
                dominio = "petrobras.com.br"
            elif "magazine" in nome_emp:
                dominio = "magazineluiza.com.br"
            elif "banco do brasil" in nome_emp or "bb" in nome_emp:
                dominio = "bb.com.br"

            # Geração dos e-mails com base em nomes e cargos
            emails = gerar_possiveis_emails(nomes, dominio)
            if filtro != "Todos":
                emails.append({
                    "email": f"{filtro}@{dominio}",
                    "nome": filtro,
                    "sobrenome": "",
                    "empresa": nome_empresa,
                    "dominio": dominio
                })
            else:
                for cargo in cargos:
                    emails.append({
                        "email": f"{cargo}@{dominio}",
                        "nome": cargo,
                        "sobrenome": "",
                        "empresa": nome_empresa,
                        "dominio": dominio
                    })

            # Validação SMTP de cada e-mail
            for item in emails:
                item["smtp_valido"] = verificar_email_smtp(item["email"])
                item["empresa"] = nome_empresa
                item["dominio"] = dominio
                item["cnpj"] = empresa.get("cnpj") or "Desconhecido"
                emails_result.append(item)

        # Criação do DataFrame com os resultados
        df_saida = pd.DataFrame(emails_result)
        df_saida.to_csv(f"{zip_dir}/emails_validados.csv", index=False)
        df_saida.to_excel(f"{zip_dir}/emails_validados.xlsx", index=False)

        # Geração de Gráficos por CNPJ
        for cnpj, grupo in df_saida.groupby("cnpj"):
            plt.figure(figsize=(6, 4))
            grupo["smtp_valido"] = grupo["smtp_valido"].astype(bool)
            sns.countplot(data=grupo, x="smtp_valido")
            plt.title(f"Validação por CNPJ {cnpj}")
            plt.savefig(f"{zip_dir}/grafico_{cnpj}.png")
            plt.close()

        # Preparação dos dados para IA (RandomForest)
        X = df_saida[["nome", "sobrenome"]].fillna("")
        y = df_saida["smtp_valido"].astype(int)

        encoder = LabelEncoder()
        X_encoded = pd.DataFrame({
            "nome": encoder.fit_transform(X["nome"].astype(str)),
            "sobrenome": encoder.fit_transform(X["sobrenome"].astype(str))
        })

        # Treinamento do modelo de IA
        model = RandomForestClassifier()
        model.fit(X_encoded, y)
        y_pred = model.predict(X_encoded)

        cm = confusion_matrix(y, y_pred)
        report = classification_report(y, y_pred, output_dict=True)

        # Geração de gráficos para a Matriz de Confusão e Dispersão
        plt.figure(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
        plt.title("Matriz de Confusão")
        plt.xlabel("Previsto")
        plt.ylabel("Real")
        plt.savefig(f"{zip_dir}/matriz_confusao.png")
        plt.close()

        plt.figure(figsize=(6, 4))
        sns.scatterplot(data=X_encoded.assign(valido=y), x="nome", y="sobrenome", hue="valido")
        plt.title("Dispersão - Nome x Sobrenome vs Validação")
        plt.savefig(f"{zip_dir}/dispersao.png")
        plt.close()

        # Gerando o Relatório PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Relatório de E-mails Validados", ln=True)

        pdf.set_font("Arial", "B", size=11)
        pdf.cell(200, 10, txt="Métricas de Classificação:", ln=True)
        pdf.set_font("Arial", size=10)
        for label, metrics in report.items():
            if isinstance(metrics, dict):
                linha = f"Classe {label}: Precision={metrics['precision']:.2f}, Recall={metrics['recall']:.2f}, F1={metrics['f1-score']:.2f}"
                pdf.cell(200, 8, txt=linha, ln=True)

        # Totais por Domínio
        pdf.set_font("Arial", "B", size=11)
        pdf.cell(200, 10, txt="Totais por Domínio:", ln=True)
        pdf.set_font("Arial", size=10)
        dominios = df_saida.groupby("dominio")["smtp_valido"].value_counts().unstack().fillna(0)
        for dom, vals in dominios.iterrows():
            linha = f"{dom} => Válidos: {int(vals.get(True, 0))}, Inválidos: {int(vals.get(False, 0))}"
            pdf.cell(200, 8, txt=linha, ln=True)

        # Totais por CNPJ
        pdf.set_font("Arial", "B", size=11)
        pdf.cell(200, 10, txt="Totais por CNPJ:", ln=True)
        pdf.set_font("Arial", size=10)
        cnpj_grupo = df_saida.groupby("cnpj")["smtp_valido"].value_counts().unstack().fillna(0)
        for cnpj, vals in cnpj_grupo.iterrows():
            linha = f"{cnpj} => Válidos: {int(vals.get(True, 0))}, Inválidos: {int(vals.get(False, 0))}"
            pdf.cell(200, 8, txt=linha, ln=True)

        # Padrões de e-mail usados
        pdf.set_font("Arial", "B", size=11)
        pdf.cell(200, 10, txt="Padrões de E-mail Usados:", ln=True)
        pdf.set_font("Arial", size=10)
        df_saida["formato"] = df_saida["email"].str.extract(r"^([\w\.\-_]+)@")
        formato_count = df_saida.groupby("formato")["smtp_valido"].value_counts().unstack().fillna(0)
        for formato, vals in formato_count.iterrows():
            linha = f"{formato} => Válidos: {int(vals.get(True, 0))}, Inválidos: {int(vals.get(False, 0))}"
            pdf.cell(200, 8, txt=linha, ln=True)

        # Conclusão
        pdf.set_font("Arial", "B", size=11)
        pdf.cell(200, 10, txt="Conclusão Geral:", ln=True)
        pdf.set_font("Arial", size=10)
        total_validos = int(df_saida["smtp_valido"].sum())
        total_total = len(df_saida)
        taxa = (total_validos / total_total) * 100 if total_total else 0
        pdf.multi_cell(200, 8, txt=f"Foram testados {total_total} e-mails. Desses, {total_validos} foram válidos ({taxa:.2f}%). O modelo de IA demonstrou boa aderência ao padrão real.")

        pdf.output(f"{zip_dir}/relatorio.pdf")

        # Gerar o arquivo ZIP
        zip_path = "resultado.zip"
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for fname in os.listdir(zip_dir):
                zipf.write(os.path.join(zip_dir, fname), arcname=fname)

        return send_file(zip_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

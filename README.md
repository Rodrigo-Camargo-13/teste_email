```markdown
Teste de Validação de E-mails e CNPJs

Este projeto é uma solução automatizada para validação de e-mails empresariais, baseada em CNPJs, com funcionalidades adicionais de análise e relatórios detalhados. Ele utiliza inteligência artificial para prever a probabilidade de um e-mail ser válido ou não, integrando diferentes fontes de dados como a Receita Federal, além de fornecer gráficos e relatórios completos para análise.

---

Funcionalidades

- Validação de E-mails: Verifica a validade dos e-mails com base no padrão de domínios conhecidos e formatos específicos.
- Consultas Automáticas: Realiza consultas aos CNPJs fornecidos para obter as informações da empresa e gerar os e-mails.
- Inteligência Artificial: Utiliza um modelo de aprendizado de máquina (Random Forest) para classificar e-mails com base em nome e sobrenome.
- Análise Completa: Gera gráficos e uma matriz de confusão para analisar a precisão do modelo.
- Relatórios: Geração de relatórios detalhados em PDF, CSV e Excel, incluindo métricas de classificação, totais por domínio e CNPJ, padrões de e-mail e muito mais.

---

Como Funciona

1. Input de Dados: O usuário carrega um arquivo CSV com os CNPJs das empresas que deseja validar os e-mails.
2. Validação e Geração de E-mails: O sistema gera os e-mails com base nos CNPJs e valida esses e-mails através de um serviço SMTP.
3. Modelagem de IA: A validação é aprimorada com a utilização de um modelo de inteligência artificial, treinado para prever a validade de e-mails com base em nome e sobrenome.
4. Relatório e Exportação: O sistema gera gráficos e relatórios detalhados, que podem ser exportados em formato PDF, CSV e Excel.
5. Download de Resultados: O usuário pode baixar um arquivo ZIP contendo os resultados completos, incluindo os relatórios e gráficos gerados.

---

Tecnologias Utilizadas

- Flask: Framework web em Python para desenvolvimento do backend.
- pandas: Biblioteca para manipulação e análise de dados.
- matplotlib & seaborn: Bibliotecas para criação de gráficos e visualizações.
- FPDF: Biblioteca para gerar PDFs com relatórios detalhados.
- scikit-learn: Para a criação do modelo de aprendizado de máquina (Random Forest).
- zipfile: Para criar arquivos ZIP contendo os resultados.
- openpyxl: Para manipulação de arquivos Excel.

---

Como Rodar o Projeto

Requisitos

1. [Python 3.8+](https://www.python.org/downloads/)
2. Dependências do projeto listadas em `requirements.txt`.

Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/Rodrigo-Camargo-13/teste_email.git
   cd teste_email
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute o aplicativo:

   ```bash
   python app.py
   ```

5. Acesse a aplicação no navegador: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

Estrutura do Projeto

```plaintext
teste_email/
├── backend/                    # Código do backend
│   ├── consulta_api.py         # Consulta de CNPJs
│   ├── email_generator.py      # Geração de e-mails
│   ├── smtp_checker.py         # Validação SMTP
│   ├── ia_model.py             # Modelo de predição
│   ├── exportador.py           # Exportações (CSV, Excel)
│   ├── confusion_matrix.py     # Matriz de Confusão
│   ├── validator.py            # Validação geral
│   └── main.py                 # Função principal para rodar a aplicação Flask
├── frontend/                   # Código do frontend
│   ├── static/                 # Arquivos estáticos (CSS, imagens, vídeos)
│   └── templates/              # Arquivos HTML
│       └── index.html          # Página principal
├── requirements.txt            # Dependências do projeto
├── app.py                      # Roteador principal Flask
└── .gitignore                  # Arquivos ignorados no git
```

---

Contribuindo

Contribuições são bem-vindas! Para contribuir, siga as etapas abaixo:

1. Faça o fork deste repositório.
2. Crie uma nova branch (`git checkout -b feature-branch`).
3. Faça as alterações e commit com mensagens claras.
4. Envie um pull request.

---

Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

Contato

Para mais informações ou dúvidas, entre em contato com o criador do projeto:

- [Rodrigo Camargo](https://github.com/Rodrigo-Camargo-13)
- Email: rodrigopimentelcamargo@yahoo.com.br

---

**Divirta-se validando e-mails e melhorando a experiência de dados!**
```

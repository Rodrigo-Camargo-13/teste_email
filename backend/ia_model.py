from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

def treinar_modelo_formatos():
    """
    Função responsável pelo treinamento do modelo de classificação de formatos de e-mail.

    O modelo é treinado com exemplos simples de combinações de nome e sobrenome, 
    juntamente com a informação de e-mail válido ou não. Utiliza o algoritmo RandomForest.

    Retorna o classificador treinado e o vetor de contagem.
    """
    # Exemplos de dados de treinamento: nomes, sobrenomes e e-mails válidos
    nomes = ["Carlos", "Ana", "João", "Maria", "Pedro", "Lara"]
    sobrenomes = ["Silva", "Souza", "Pereira", "Rocha", "Dias", "Alves"]
    e_mails_validos = [True, False, True, False, True, True]

    # Criação da lista de combinações de nome e sobrenome
    X = [f"{nome} {sobrenome}" for nome, sobrenome in zip(nomes, sobrenomes)]
    y = e_mails_validos

    # Vetorização dos textos (nomes + sobrenomes)
    vetor = CountVectorizer()
    X_vetorizado = vetor.fit_transform(X)

    # Criação e treinamento do modelo RandomForest
    classificador = RandomForestClassifier()
    classificador.fit(X_vetorizado, y)

    return classificador, vetor

def prever_formato(classificador, vetor, nome, sobrenome):
    """
    Função para prever se o formato de e-mail de uma combinação de nome e sobrenome
    é válido, com base no modelo treinado.

    Args:
    - classificador: Modelo RandomForest treinado
    - vetor: Vetor de contagem (CountVectorizer) para transformação do texto
    - nome: Nome para previsão
    - sobrenome: Sobrenome para previsão

    Retorna:
    - True se o formato de e-mail for válido, False caso contrário.
    """
    texto = f"{nome} {sobrenome}"
    X_input = vetor.transform([texto])
    return bool(classificador.predict(X_input)[0])

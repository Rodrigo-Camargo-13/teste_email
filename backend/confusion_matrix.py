from sklearn.metrics import confusion_matrix, classification_report

def gerar_matriz_confusao(resultados):
    """
    Gera a matriz de confusão e o relatório de classificação para os resultados 
    do modelo de previsão de e-mails válidos.
    
    Args:
    resultados (list of dict): Lista de dicionários contendo os resultados de previsão, 
                               onde 'valido_real' é o valor real e 'valido_simulado' é o valor previsto.
    
    Prints:
    - Matriz de Confusão: Comparação entre os valores reais e previstos.
    - Relatório de Classificação: Avaliação de métricas como precision, recall e F1-score.
    """

    # Extrai os valores reais e previstos
    y_true = [r['valido_real'] for r in resultados]       # Valores reais: SMTP válido?
    y_pred = [r['valido_simulado'] for r in resultados]   # Valores previstos: Adivinhação correta?

    # Imprime a Matriz de Confusão
    print("\nMatriz de Confusão:")
    print(confusion_matrix(y_true, y_pred))

    # Imprime o Relatório de Classificação
    print("\nRelatório de Classificação:")
    print(classification_report(y_true, y_pred))



def inputs_validacao():
    import pandas
    import statsmodels.api
    from scipy.stats import probplot
    from sklearn.exceptions import NotFittedError
    from sklearn.inspection import permutation_importance
    from sklearn.model_selection import cross_val_score, cross_val_predict
    from sklearn.metrics import (r2_score, mean_squared_error, mean_absolute_error, 
                                 mean_absolute_percentage_error, mean_squared_log_error, 
                                 make_scorer, roc_curve, accuracy_score, balanced_accuracy_score, 
                                 precision_score, recall_score, f1_score, roc_auc_score, 
                                 average_precision_score, confusion_matrix, auc, 
                                 precision_recall_curve)
    from sklearn.calibration import calibration_curve
    import matplotlib.pyplot
    import plotly.express
    import plotly.graph_objects
    import seaborn
    from IPython.display import display, Markdown
    import ipywidgets
    import numpy

    
    descricoes = {
        'model': 'Este é o modelo já treinado, compatível com o framework do Scikit-Learn. Pode ser uma pipeline do Scikit-Learn com um modelo como último passo. Este modelo já aprendeu os padrões dos dados e está pronto para fazer previsões. Para problemas de regressão, é necessário que o modelo tenha o método .predict. Em problemas de classificação, além do .predict, também é necessário o método .predict_proba.',
        'X_train': 'Estes são os dados usados para treinar o modelo. São informações estruturadas em observações e variáveis que o modelo usou para aprender.',
        'y_train': 'Estes são os rótulos ou valores-alvo associados aos dados de treinamento. Serviram como resposta para o modelo durante a fase de treinamento.',
        'X_test': 'Estes são novos dados, que o modelo ainda não viu. Serão utilizados para avaliar o desempenho do modelo, simulando uma situação real.',
        'y_test': 'Estes são os rótulos ou valores-alvo dos dados de teste. Servirão como referência para comparar as previsões do modelo e avaliar seu desempenho.',
        'cv': 'Este parâmetro é utilizado como o número de divisões (folds) para a validação cruzada ao usar a função cross_val_score do Scikit-Learn. É fundamental para calcular a pontuação CV (Cross Validation Score) do modelo. Um valor mais alto implica que a estimativa da capacidade de generalização do modelo é mais robusta, pois utiliza mais divisões para a validação. No entanto, isso também pode aumentar o tempo computacional.',
        'nbinbs': 'O número de bins no histograma dos dados. Este valor pode afetar a interpretação dos resultados, ao determinar o nível de detalhamento na visualização dos dados.',
        'n_repeats': 'Este é o número de vezes que repetimos a avaliação da importância dos recursos, por permutação. Mais repetições podem dar uma visão mais precisa de quais recursos são mais relevantes para as previsões do modelo.'
    }

    def exibir_descricao(input):
        display(Markdown(f"<div style='background: #ffffff; color: #000000; padding: 0.5em; margin: 0.5em 0; font-family: Arial, sans-serif;'><h2 style='background: #c0c0c0; display: inline-block; padding: 0.2em 0.5em;'>{input}</h2><p>{descricoes[input]}</p></div>"))

    dropdown = ipywidgets.Dropdown(options=list(descricoes.keys()))
    ipywidgets.interact(exibir_descricao, input=dropdown)

#################### VALIDAR REGRESSÃO ##################################    
    
    
def validar_regressao(model, X_train, y_train, X_test, y_test, cv, nbins, n_repeats):
    import pandas
    import statsmodels.api
    from scipy.stats import probplot
    from sklearn.exceptions import NotFittedError
    from sklearn.inspection import permutation_importance
    from sklearn.model_selection import cross_val_score, cross_val_predict
    from sklearn.metrics import (r2_score, mean_squared_error, mean_absolute_error, 
                                 mean_absolute_percentage_error, mean_squared_log_error, 
                                 make_scorer, roc_curve, accuracy_score, balanced_accuracy_score, 
                                 precision_score, recall_score, f1_score, roc_auc_score, 
                                 average_precision_score, confusion_matrix, auc, 
                                 precision_recall_curve)
    from sklearn.calibration import calibration_curve
    import matplotlib.pyplot
    import plotly.express
    import plotly.graph_objects
    import seaborn
    from IPython.display import display, Markdown
    import ipywidgets
    import numpy

### Transformando y_test e y_train em numpy.array caso não estejam nesse formato ainda.

    if not isinstance(y_test, numpy.ndarray):
         y_test = numpy.array(y_test)

    if not isinstance(y_train, numpy.ndarray):
         y_train = numpy.array(y_train)

    
### Testando se o modelo já está treinado, caso contrário o modelo ou pipeline é treinada com os parâmetros padrões 

    try:
        
        
        y_pred = model.predict(X_test)
        y_train_pred = model.predict(X_train)
        
        
    except NotFittedError:
        
        
        print("Pipeline Aka Modelo Não Treinado Ainda.....    treinando......... modelo com Pipeline Padrão Já deu Set_PARAMS?")
        
        model.fit(X_train, y_train)        
        y_pred = model.predict(X_test)
        y_train_pred = model.predict(X_train)
    

### Definição de Métricas e função para avaliar as métricas 
    
    
    def mean_absolute_percentage_error(y_true, y_pred): 
        
        
        
        return numpy.mean(numpy.abs((y_true - y_pred) / y_true)) * 100   
    
    ###### Veio olhar o código né?? :D     
    def evaluation_metrics():

        y_train_pred = model.predict(X_train)
        y_pred = model.predict(X_test)

        r2_train = r2_score(y_train, y_train_pred)
        r2_test = r2_score(y_test, y_pred)

        rmse_train = numpy.sqrt(mean_squared_error(y_train, y_train_pred))
        rmse_test = numpy.sqrt(mean_squared_error(y_test, y_pred))

        mae_train = mean_absolute_error(y_train, y_train_pred)
        mae_test = mean_absolute_error(y_test, y_pred)

        mape_train = mean_absolute_percentage_error(y_train, y_train_pred) * 100
        mape_test = mean_absolute_percentage_error(y_test, y_pred) * 100

        scoring_dict = {
            'r2': 'r2',
            'rmse': make_scorer(mean_squared_error, greater_is_better=False, squared=False),
            'mae': 'neg_mean_absolute_error',
            'mape': make_scorer(mean_absolute_percentage_error, greater_is_better=False),
        }
        ##### BRAZILIAN BEAST &&&&&&&&&&&&&&&&& UNTOUCHABLE PRESENTS 
        cv_scores = {}
        for metric_name, scorer in scoring_dict.items():
            cv_score = cross_val_score(model, X_train, y_train, cv=cv, scoring=scorer)
            cv_scores[metric_name] = cv_score.mean()

        metrics = pandas.DataFrame({
            'Metric': ['R2', 'RMSE', 'MAE', 'MAPE'],
            'Train Value': [r2_train, rmse_train, mae_train, mape_train],
            'Test Value': [r2_test, rmse_test, mae_test, mape_test],
            'CV Score': [cv_scores['r2'], -cv_scores['rmse'], -cv_scores['mae'], -cv_scores['mape']]
        })

        fig = plotly.graph_objects.Figure(data=[plotly.graph_objects.Table(header=dict(values=['Metrica', 'Valor Dados Treino', 'Valor Dados Teste', 'Score Validação Cruzada']),
                                       cells=dict(values=[metrics['Metric'], metrics['Train Value'], metrics['Test Value'], metrics['CV Score']]))])
        fig.show()  

    ### Função para Valor Real Versus Previsto 


    from plotly.subplots import make_subplots

    def grafico_previsto_vs_real():
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Previsto vs Real - Treino", "Previsto vs Real - Teste"))

        fig.add_trace(
            plotly.graph_objects.Scatter(x=y_train, y=y_train_pred, mode='markers'),
            row=1, col=1
        )

        fig.add_trace(
            plotly.graph_objects.Scatter(x=[y_train.min(), y_train.max()], y=[y_train.min(), y_train.max()], mode='lines'),
            row=1, col=1
        )

        fig.add_trace(
            plotly.graph_objects.Scatter(x=y_test, y=y_pred, mode='markers'),
            row=1, col=2
        )

        fig.add_trace(
            plotly.graph_objects.Scatter(x=[y_test.min(), y_test.max()], y=[y_test.min(), y_test.max()], mode='lines'),
            row=1, col=2
        )

        fig.update_layout(height=600, width=1200, title_text="Previsto vs Real")
        fig.show()

    def grafico_residuos():
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Gráfico Resíduos - Treino", "Gráfico Resíduos - Teste"))

        residuos_treino = y_train - y_train_pred
        fig.add_trace(
            plotly.graph_objects.Scatter(x=y_train_pred, y=residuos_treino, mode='markers'),
            row=1, col=1
        )

        fig.add_trace(
            plotly.graph_objects.Scatter(x=[y_train_pred.min(), y_train_pred.max()], y=[0, 0], mode='lines'),
            row=1, col=1
        )

        residuos_teste = y_test - y_pred
        fig.add_trace(
            plotly.graph_objects.Scatter(x=y_pred, y=residuos_teste, mode='markers'),
            row=1, col=2
        )

        fig.add_trace(
            plotly.graph_objects.Scatter(x=[y_pred.min(), y_pred.max()], y=[0, 0], mode='lines'),
            row=1, col=2
        )

        fig.update_layout(height=600, width=1200, title_text="Gráfico de Resíduos")
        fig.show()


    def histograma_residuos():
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Histograma Resíduos - Treino", "Histograma Resíduos - Teste"))

        residuos_treino = y_train - y_train_pred
        fig.add_trace(
            plotly.graph_objects.Histogram(x=residuos_treino, nbinsx=nbins),
            row=1, col=1
        )

        residuos_teste = y_test - y_pred
        fig.add_trace(
            plotly.graph_objects.Histogram(x=residuos_teste, nbinsx=nbins),
            row=1, col=2
        )

        fig.update_layout(height=600, width=1200, title_text="Histograma de Resíduos")
        fig.show()

    def qq_plot():
        fig, ax = matplotlib.pyplot.subplots(1, 2, figsize=(15, 5))

        residuos_treino = y_train - y_train_pred
        statsmodels.api.qqplot(residuos_treino, line ='45', ax=ax[0])
        ax[0].set_title('QQ Plot Resíduos - Treino')

        residuos_teste = y_test - y_pred
        statsmodels.api.qqplot(residuos_teste, line ='45', ax=ax[1])
        ax[1].set_title('QQ Plot Resíduos - Teste')

        matplotlib.pyplot.show()
            

    def qq_plot():
        fig, ax = matplotlib.pyplot.subplots(1, 2, figsize=(15, 5))

        residuos_treino = y_train - y_train_pred
        statsmodels.api.qqplot(residuos_treino, line ='45', ax=ax[0])
        ax[0].set_title('QQ Plot Resíduos - Treino')

        residuos_teste = y_test - y_pred
        statsmodels.api.qqplot(residuos_teste, line ='45', ax=ax[1])
        ax[1].set_title('QQ Plot Resíduos - Teste')

        matplotlib.pyplot.show()
            
            
        
    def permutation_feature_importance():
        
        scoring_dict = {
            'r2': 'r2',
            'rmse': make_scorer(mean_squared_error, greater_is_better=False, squared=False),
            'mae': 'neg_mean_absolute_error',
            'mape': make_scorer(mean_absolute_percentage_error, greater_is_better=False),
        }

        results_train = {}
        results_test = {}
        for metric_name, scorer in scoring_dict.items():
            result_train = permutation_importance(model, X_train, y_train_pred, scoring=scorer, n_repeats=10, random_state=42)
            result_test = permutation_importance(model, X_test, y_test, scoring=scorer, n_repeats=10, random_state=42)
            
            importance_df_train = pandas.DataFrame({'Variável': X_train.columns,
                                           'Importância Treino': result_train.importances_mean,
                                           'Importância Desvio Padrão Treino': result_train.importances_std})
            
            importance_df_test = pandas.DataFrame({'Variável': X_test.columns,
                                           'Importância Teste': result_test.importances_mean,
                                           'Importância Desvio Padrão Teste': result_test.importances_std})
                                           
            importance_df_train.sort_values(by='Importância Treino', ascending=False, inplace=True)
            importance_df_test.sort_values(by='Importância Teste', ascending=False, inplace=True)
            
            results_train[metric_name] = importance_df_train
            results_test[metric_name] = importance_df_test
            
            importance_difference = pandas.merge(importance_df_train, importance_df_test, on="Variável", suffixes=('_train', '_test'))
            importance_difference["Diferença"] = abs(importance_difference['Importância Treino'] - importance_difference['Importância Teste'])

            fig = plotly.graph_objects.Figure()
            fig.add_trace(plotly.graph_objects.Bar(name='Treino', 
                                 x=importance_df_train['Variável'], 
                                 y=importance_df_train['Importância Treino'], 
                                 error_y=dict(array=importance_df_train['Importância Desvio Padrão Treino'])))

            fig.add_trace(plotly.graph_objects.Bar(name='Teste', 
                                 x=importance_df_test['Variável'], 
                                 y=importance_df_test['Importância Teste'], 
                                 error_y=dict(array=importance_df_test['Importância Desvio Padrão Teste'])))
            fig.update_layout(barmode='group', title=f'Permutation Feature Importance ({metric_name.upper()})')
            fig.show()


            fig_diff = plotly.graph_objects.Figure(data=[plotly.graph_objects.Table(header=dict(values=['Variável', 'Diferença']),
                                                cells=dict(values=[importance_difference['Variável'], importance_difference['Diferença']]))])
            fig_diff.show()
        
    
    

    def plot_explanation(plot_type):
        
        explanations = {
            'Métricas de Avaliação': 
            '''
            As métricas de avaliação são como um "boletim" do nosso modelo de previsão. Quatro dessas métricas que merecem destaque são R2, RMSE, MAE e MAPE.

            1- R2 (R-squared ou Coeficiente de Determinação): Imagine que você tem uma lupa que lhe permite ver o quão bem a nossa "linha de previsão" se encaixa nos pontos de dados. Esse é o R2. Ele nos diz a proporção da variância nos dados que é explicada pelo modelo. Seu valor varia de 0 a 1, onde 1 é a nota máxima, indicando que nosso modelo prevê perfeitamente os dados.

            2- RMSE (Root Mean Square Error): Aqui medimos a diferença entre o que o modelo previu e o que realmente aconteceu. Quanto menor o RMSE, melhor. É como se estivéssemos medindo a distância entre os pontos e a nossa "linha de previsão".

            3- MAE (Mean Absolute Error): Similar ao RMSE, o MAE também mede a diferença entre as previsões e a realidade. Só que ele não dá tanto peso aos erros grandes. É como se estivéssemos medindo a distância entre os pontos e a nossa "linha de previsão" sem levar tanto em conta os pontos muito distantes.

            4-MAPE (Mean Absolute Percentage Error): O MAPE nos dá o erro médio em termos percentuais. É como se estivéssemos calculando em média quantos por cento o modelo erra nas previsões.

            5-CV Score (Cross-Validation Score): Imagine que queremos testar o quanto nosso modelo é bom em situações diferentes. Para isso, dividimos os dados em várias partes e treinamos o modelo várias vezes, cada vez com partes diferentes dos dados. A média desses testes é o CV Score. Ele nos ajuda a ter uma visão mais robusta do desempenho do nosso modelo.

            6-TRAIN_SCORE e TEST_SCORE: Estes são como testes finais que fazemos no nosso modelo. O TRAIN_SCORE é como uma prova feita com a matéria que o aluno estudou, e o TEST_SCORE é uma prova surpresa, com perguntas que o aluno nunca viu. Se a nota na prova surpresa for muito mais baixa, pode ser que o aluno (ou seja, nosso modelo) tenha decorado a matéria em vez de realmente ter aprendido.
            
            ''',
            'Plot do Valor Real vs Previsto':
            '''
            Este gráfico é como uma competição entre o que o nosso modelo previu e o que realmente aconteceu. Se nosso modelo fosse perfeito, todos os pontos estariam alinhados na linha diagonal.
            ''',

            'Plot Residuos':
            '''
            Imagine que pudéssemos olhar a "cara" dos erros do nosso modelo. É isso que o gráfico dos resíduos mostra. Se os erros parecerem "bagunçados" e distribuídos ao acaso em torno do zero, é um bom sinal. Se parecerem "organizados" ou formando um padrão, o modelo pode estar errando de maneira sistemática.
            ''',

            'Histograma Residuos':
            '''
            Imagine que os erros do nosso modelo fossem alunos de uma escola e nós quiséssemos saber como estão distribuídas as notas deles. Esse histograma nos mostra isso. Se as notas (ou seja, os erros) seguirem uma curva de sino (distribuição normal), centrada no zero, é um bom sinal. Significa que os erros são equilibrados e o nosso modelo não está errando mais para um lado ou outro.
            ''',

            'Q-Q Plot':
            '''
            O Q-Q Plot é outra maneira de verificar se os erros do nosso modelo estão bem distribuídos. É como se estivéssemos verificando se as notas dos alunos estão equilibradas. Se as notas estiverem bem distribuídas, os pontos estarão na linha diagonal.
            ''',

            'Importancia das Features Permutadas':
            '''
            Imagine que queremos saber qual é a "matéria" (ou feature) que mais "pesa" na nota final do nosso modelo. E ainda queremos saber se o modelo está "colando" (overfitting) dessa matéria. Para isso, permutamos as features e vemos como isso afeta o resultado. Se uma matéria tem um peso muito grande na nota final e o modelo vai mal quando essa matéria é alterada, pode ser que o modelo esteja "colando" dessa matéria. É como se estivéssemos tentando entender melhor o "processo de aprendizagem" do nosso modelo, para garantir que ele será capaz de responder bem a novas perguntas.
            '''
        }
    
        text_widget = ipywidgets.Textarea(
            value=explanations[plot_type],
            layout=ipywidgets.Layout(width="100%", height="200px")
        )

        display(text_widget)

        plot_selected(plot_type)
        
    def plot_selected(plot_type):
        
        if plot_type ==    'Métricas de Avaliação':
            evaluation_metrics()
        elif plot_type ==  'Plot do Valor Real vs Previsto':
            grafico_previsto_vs_real()
        elif plot_type ==  'Plot Residuos':
            grafico_residuos()
        elif plot_type ==  'Histograma Residuos':
            histograma_residuos()
        elif plot_type ==  'Q-Q Plot':
            qq_plot()
        elif plot_type ==  'Importancia das Features Permutadas':
            permutation_feature_importance()
        
    dropdown = ipywidgets.Dropdown(options=['Métricas de Avaliação','Plot do Valor Real vs Previsto', 'Plot Residuos', 'Histograma Residuos', 'Q-Q Plot','Importancia das Features Permutadas'])
    ipywidgets.interact(plot_explanation, plot_type=dropdown)
    
    
    
def validar_classificacao_binaria(model, X_train, y_train, X_test, y_test, cv, nbins, n_repeats):
    import numpy

    
    import pandas
    import statsmodels.api
    from scipy.stats import probplot
    from sklearn.exceptions import NotFittedError
    from sklearn.inspection import permutation_importance
    from sklearn.model_selection import cross_val_score, cross_val_predict
    from sklearn.metrics import (r2_score, mean_squared_error, mean_absolute_error, 
                                 mean_absolute_percentage_error, mean_squared_log_error, 
                                 make_scorer, roc_curve, accuracy_score, balanced_accuracy_score, 
                                 precision_score, recall_score, f1_score, roc_auc_score, 
                                 average_precision_score, confusion_matrix, auc, 
                                 precision_recall_curve)
    from sklearn.calibration import calibration_curve
    import matplotlib.pyplot
    import plotly.express
    import plotly.graph_objects
    import seaborn
    from IPython.display import display, Markdown
    import ipywidgets


    if not isinstance(y_test, numpy.ndarray):
         y_test = numpy.array(y_test)

    if not isinstance(y_train, numpy.ndarray):
         y_train = numpy.array(y_train)

    
    
    try:
        
        
        y_pred = model.predict(X_test)
        y_train_pred = model.predict(X_train)
        y_train_prob = model.predict_proba(X_train)[:, 1]
        y_test_prob = model.predict_proba(X_test)[:, 1]      
        
    except NotFittedError:
        
        
        print("Pipeline Aka Modelo Não Treinado Ainda.....    treinando......... modelo com Pipeline Padrão Já deu Set_PARAMS?")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_train_pred = model.predict(X_train)
        y_train_prob = model.predict_proba(X_train)[:, 1]
        y_test_prob = model.predict_proba(X_test)[:, 1]
        
        
    def evaluation_metrics():
        y_train_pred = model.predict(X_train)
        y_pred = model.predict(X_test)

        y_train_prob = model.predict_proba(X_train)[:, 1]
        y_test_prob = model.predict_proba(X_test)[:, 1]

        acc_train = accuracy_score(y_train, y_train_pred)
        acc_test = accuracy_score(y_test, y_pred)
        
        b_acc_train=balanced_accuracy_score(y_train, y_train_pred)
        b_acc_test=accuracy_score(y_test, y_pred)
        
        prec_train = precision_score(y_train, y_train_pred)
        prec_test = precision_score(y_test, y_pred)

        rec_train = recall_score(y_train, y_train_pred)
        rec_test = recall_score(y_test, y_pred)

        f1_train = f1_score(y_train, y_train_pred)
        f1_test = f1_score(y_test, y_pred)

        auc_train = roc_auc_score(y_train, y_train_prob)
        auc_test = roc_auc_score(y_test, y_test_prob)

        pr_auc_train = average_precision_score(y_train, y_train_prob)
        pr_auc_test = average_precision_score(y_test, y_test_prob)

        scoring_dict = {
            'Acurácia': make_scorer(accuracy_score),
            'Acurácia Balanceada': make_scorer(balanced_accuracy_score),
            'Precisão': make_scorer(precision_score),
            'Recall': make_scorer(recall_score),
            'F1-Score': make_scorer(f1_score),
            'AUC-ROC': make_scorer(roc_auc_score, needs_proba=True),
            'PR AUC Score': make_scorer(average_precision_score, needs_proba=True),
        }

        cv_scores = {}
        for metric_name, scorer in scoring_dict.items():
            cv_score = cross_val_score(model, X_train, y_train, cv=cv, scoring=scorer,n_jobs=-1)
            cv_scores[metric_name] = cv_score.mean()

        metrics = pandas.DataFrame({
            'Métrica': ['Acurácia','Acurácia Balanceada','Precisão','Recall', 'F1-Score', 'AUC-ROC', 'PR AUC Score'],
            'Valor Treino': [acc_train, b_acc_train,prec_train, rec_train, f1_train, auc_train, pr_auc_train],
            'Valor Teste': [acc_test, b_acc_test,prec_test, rec_test, f1_test, auc_test, pr_auc_test],
            'Score Validação Cruzada': [cv_scores['Acurácia'],cv_scores['Acurácia Balanceada'],cv_scores['Precisão'], cv_scores['Recall'], cv_scores['F1-Score'], cv_scores['AUC-ROC'], cv_scores['PR AUC Score']]
        })

        fig = plotly.graph_objects.Figure(data=[plotly.graph_objects.Table(header=dict(values=['Métrica', 'Valor Treino', 'Valor Teste', 'Score Validação Cruzada']),
                                       cells=dict(values=[metrics['Métrica'], metrics['Valor Treino'], metrics['Valor Teste'], metrics['Score Validação Cruzada']]))])
        fig.show() 

    def matriz_confusao():
        fig, ax = matplotlib.pyplot.subplots(1, 2, figsize=(15, 5))

        cm_train = confusion_matrix(y_train, y_train_pred)
        acc_train = accuracy_score(y_train, y_train_pred)
        b_acc_train = balanced_accuracy_score(y_train, y_train_pred)
        prec_train = precision_score(y_train, y_train_pred)
        rec_train = recall_score(y_train, y_train_pred)

        plotly.seaborn.heatmap(cm_train, annot=True, fmt="d", ax=ax[0], cmap='Blues', cbar=False, xticklabels=[0, 1], yticklabels=[0, 1])
        ax[0].set_title(f'Treino\nAcurácia: {acc_train:.2f}\nAcurácia Balanceada: {b_acc_train:.2f}\nPrecisão: {prec_train:.2f}\nRecall: {rec_train:.2f}')
        ax[0].set_xlabel('Predito')
        ax[0].set_ylabel('Real')

        cm_test = confusion_matrix(y_test, y_pred)
        acc_test = accuracy_score(y_test, y_pred)
        b_acc_test = balanced_accuracy_score(y_test, y_pred)
        prec_test = precision_score(y_test, y_pred)
        rec_test = recall_score(y_test, y_pred)

        plotly.seaborn.heatmap(cm_test, annot=True, fmt="d", ax=ax[1], cmap='Blues', cbar=False, xticklabels=[0, 1], yticklabels=[0, 1])
        ax[1].set_title(f'Teste\nAcurácia: {acc_test:.2f}\nAcurácia Balanceada: {b_acc_test:.2f}\nPrecisão: {prec_test:.2f}\nRecall: {rec_test:.2f}')
        ax[1].set_xlabel('Predito')
        ax[1].set_ylabel('Real')

        matplotlib.pyplot.show()

    def roc_auc_curve():
        fig, ax = matplotlib.pyplot.subplots(1, 2, figsize=(15, 5))

        fpr_train, tpr_train, _ = roc_curve(y_train, y_train_prob)
        roc_auc_train = auc(fpr_train, tpr_train)

        ax[0].plot(fpr_train, tpr_train, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc_train:.2f})')
        ax[0].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        ax[0].set_xlim([0.0, 1.0])
        ax[0].set_ylim([0.0, 1.05])
        ax[0].set_xlabel('Taxa de Falso Positivo')
        ax[0].set_ylabel('Taxa de Verdadeiro Positivo')
        ax[0].set_title('Curva ROC - Treino')
        ax[0].legend(loc="lower right")

        # ROC-AUC para os dados de teste
        fpr_test, tpr_test, _ = roc_curve(y_test, y_test_prob)
        roc_auc_test = auc(fpr_test, tpr_test)

        ax[1].plot(fpr_test, tpr_test, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc_test:.2f})')
        ax[1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        ax[1].set_xlim([0.0, 1.0])
        ax[1].set_ylim([0.0, 1.05])
        ax[1].set_xlabel('Taxa de Falso Positivo')
        ax[1].set_ylabel('Taxa de Verdadeiro Positivo')
        ax[1].set_title('Curva ROC - Teste')
        ax[1].legend(loc="lower right")

        matplotlib.pyplot.show()
        
        
        
    def precision_recall():
        fig, ax = matplotlib.pyplot.subplots(1, 2, figsize=(15, 5))

        precision_train, recall_train, _ = precision_recall_curve(y_train, y_train_prob)
        average_precision_train = average_precision_score(y_train, y_train_prob)

        ax[0].step(recall_train, precision_train, color='b', alpha=0.2, where='post')
        ax[0].fill_between(recall_train, precision_train, step='post', alpha=0.2, color='b')
        ax[0].set_xlabel('Recall')
        ax[0].set_ylabel('Precision')
        ax[0].set_ylim([0.0, 1.05])
        ax[0].set_xlim([0.0, 1.0])
        ax[0].set_title('Curva de Precisão-Recall: AP={0:0.2f}'.format(average_precision_train))

        
########### As perguntas --- Os questionamentos sobre a verdade são os impulsionadores das respostas que a humanidade busca, faça perguntas coerentes e sempre busque por suas respostas......
        
        
        precision_test, recall_test, _ = precision_recall_curve(y_test, y_test_prob)
        average_precision_test = average_precision_score(y_test, y_test_prob)

        ax[1].step(recall_test, precision_test, color='b', alpha=0.2, where='post')
        ax[1].fill_between(recall_test, precision_test, step='post', alpha=0.2, color='b')
        ax[1].set_xlabel('Recall')
        ax[1].set_ylabel('Precision')
        ax[1].set_ylim([0.0, 1.05])
        ax[1].set_xlim([0.0, 1.0])
        ax[1].set_title('Curva de Precisão-Recall: AP={0:0.2f}'.format(average_precision_test))

        matplotlib.pyplot.show()
        
    def histograma_probabilidade():
        df_treino = pandas.DataFrame({'Probabilidade Prevista': y_train_prob, 'Rótulo Verdadeiro': y_train, 'Dados': 'Treino'})
        df_teste = pandas.DataFrame({'Probabilidade Prevista': y_test_prob, 'Rótulo Verdadeiro': y_test, 'Dados': 'Teste'})

        df = pandas.concat([df_treino, df_teste])

        fig = plotly.express.histogram(df, x='Probabilidade Prevista', color='Rótulo Verdadeiro', facet_col='Dados', nbins=50, opacity=0.7,
                           labels={'Probabilidade Prevista': 'Probabilidade Prevista', 'Rótulo Verdadeiro': 'Rótulo Verdadeiro'},
                           title='Histograma de Probabilidade Prevista')
        fig.show()

    def plot_densidade_probabilidade():
        df_treino = pandas.DataFrame({'Probabilidade Prevista': y_train_prob, 'Rótulo Verdadeiro': y_train, 'Dados': 'Treino'})
        df_teste = pandas.DataFrame({'Probabilidade Prevista': y_test_prob, 'Rótulo Verdadeiro': y_test, 'Dados': 'Teste'})

        df = pandas.concat([df_treino, df_teste])

        fig = plotly.express.histogram(df, x='Probabilidade Prevista', color='Rótulo Verdadeiro', facet_col='Dados', nbins=50, opacity=0.7,
                           marginal='box', histnorm='density', barmode='overlay',
                           labels={'Probabilidade Prevista': 'Probabilidade Prevista', 'Rótulo Verdadeiro': 'Rótulo Verdadeiro'},
                           title='Densidade de Probabilidade Prevista')
        fig.show()

        
##### Esse aqui é perigoso, cuidado , só grave.        
        
    def plot_calibracao_probabilidade():
        prob_verdadeira_treino, prob_prevista_treino = calibration_curve(y_train, y_train_prob, n_bins=10)
        prob_verdadeira_teste, prob_prevista_teste = calibration_curve(y_test, y_test_prob, n_bins=10)

        fig = plotly.graph_objects.Figure()

        fig.add_trace(plotly.graph_objects.Scatter(x=prob_prevista_treino, y=prob_verdadeira_treino, mode='lines+markers', name='Treino'))
        fig.add_trace(plotly.graph_objects.Scatter(x=prob_prevista_teste, y=prob_verdadeira_teste, mode='lines+markers', name='Teste'))
        fig.add_shape(type='line', x0=0, x1=1, y0=0, y1=1, yref='y', xref='x', line=dict(color='Black', dash='dash'))

        fig.update_layout(title='Plot de Calibração de Probabilidade', xaxis_title='Probabilidade Prevista', yaxis_title='Probabilidade Verdadeira')

        fig.show()
        
        
    def permutation_feature_importance():
        scoring_dict = {
            'Acurácia': make_scorer(accuracy_score),
            'Acurácia Balanceada': make_scorer(balanced_accuracy_score),
            'Precisão': make_scorer(precision_score),
            'Recall': make_scorer(recall_score),
            'F1-Score': make_scorer(f1_score),
            'AUC-ROC': make_scorer(roc_auc_score, needs_proba=True),
            'PR AUC Score': make_scorer(average_precision_score, needs_proba=True),
        }

        results_train = {}
        results_test = {}
        for metric_name, scorer in scoring_dict.items():
            result_train = permutation_importance(model, X_train, y_train, scoring=scorer, n_repeats=10, random_state=42)
            result_test = permutation_importance(model, X_test, y_test, scoring=scorer, n_repeats=10, random_state=42)

            importance_df_train = pandas.DataFrame({'Variável': X_train.columns,
                                               'Importância Treino': result_train.importances_mean,
                                               'Importância Desvio Padrão Treino': result_train.importances_std})

            importance_df_test = pandas.DataFrame({'Variável': X_test.columns,
                                               'Importância Teste': result_test.importances_mean,
                                               'Importância Desvio Padrão Teste': result_test.importances_std})

            importance_df_train.sort_values(by='Importância Treino', ascending=False, inplace=True)
            importance_df_test.sort_values(by='Importância Teste', ascending=False, inplace=True)

            results_train[metric_name] = importance_df_train
            results_test[metric_name] = importance_df_test

            importance_difference = pandas.merge(importance_df_train, importance_df_test, on="Variável", suffixes=('_train', '_test'))
            importance_difference["Diferença"] = abs(importance_difference['Importância Treino'] - importance_difference['Importância Teste'])

            fig = plotly.graph_objects.Figure()
            fig.add_trace(plotly.graph_objects.Bar(name='Treino', 
                                 x=importance_df_train['Variável'], 
                                 y=importance_df_train['Importância Treino'], 
                                 error_y=dict(array=importance_df_train['Importância Desvio Padrão Treino'])))

            fig.add_trace(plotly.graph_objects.Bar(name='Teste', 
                                 x=importance_df_test['Variável'], 
                                 y=importance_df_test['Importância Teste'], 
                                 error_y=dict(array=importance_df_test['Importância Desvio Padrão Teste'])))
            fig.update_layout(barmode='group', title=f'Permutation Feature Importance ({metric_name.upper()})')
            fig.show()


            fig_diff = plotly.graph_objects.Figure(data=[plotly.graph_objects.Table(header=dict(values=['Variável', 'Diferença']),
                                                cells=dict(values=[importance_difference['Variável'], importance_difference['Diferença']]))])
            fig_diff.show()

    
    

    def plot_explanation(plot_type):

        explanations = {
            'Métricas de Avaliação': 
            '''
            A tabela de métricas de avaliação é uma ferramenta crucial que agrega várias métricas essenciais para determinar a eficiência de um modelo de classificação binária. Nela, encontramos medidas como Acurácia, Acurácia Balanceada, Precisão, Sensibilidade (Recall), F1-Score, Área Sob a Curva (AUC) da Característica Operacional do Receptor (ROC) e Área Sob a Curva (AUC) do Score de Precisão-Recall.

            Acurácia: Esta é a proporção de previsões corretas feitas pelo modelo em relação a todos os tipos de previsões feitas.

            Acurácia Balanceada: Esta é a média das acurácias obtidas em cada classe individualmente. É útil para lidar com situações onde as classes são desbalanceadas. Esta métrica varia de 0 a 1, onde 1 indica desempenho perfeito.

            Precisão: Esta é a proporção de previsões verdadeiras positivas (TP) feitas em relação ao total de previsões positivas, ou seja, a soma de verdadeiras positivas (TP) e falsas positivas (FP).

            Sensibilidade (Recall): Esta é a proporção de previsões verdadeiras positivas (TP) feitas em relação ao total de amostras que realmente eram positivas, ou seja, a soma de verdadeiras positivas (TP) e falsas negativas (FN).

            F1-Score: Esta é uma medida harmônica da precisão e sensibilidade e busca um equilíbrio entre ambos.

            AUC-ROC: Esta é a área sob a curva da Característica Operacional do Receptor (ROC). Uma ROC é uma curva de probabilidade para diferentes classes. AUC é a medida da capacidade do modelo de distinguir entre classes.

            AUC-PR: Esta é a área sob a curva do Score de Precisão-Recall. Essa curva é uma plotagem da precisão contra a sensibilidade. A AUC fornece uma avaliação agregada do desempenho em todos os limiares de classificação possíveis.
           
            CV Score (Cross-Validation Score):
            
            A pontuação de validação cruzada é uma técnica para avaliar a capacidade do modelo de generalizar para novos dados. Na validação cruzada, o conjunto de dados é dividido em várias partes, e o modelo é treinado e testado várias vezes, cada vez em diferentes partes dos dados. Isso fornece uma estimativa robusta do desempenho do modelo em dados não vistos.

            TRAIN_SCORE: Esta é a pontuação obtida ao avaliar o modelo no mesmo conjunto de dados usado para treinamento. Se essa pontuação for muito mais alta do que as outras duas, pode indicar um problema de sobreajuste, onde o modelo aprendeu os dados de treinamento "de cor", mas não é capaz de generalizar bem para dados novos.

            TEST_SCORE: Esta é a pontuação obtida ao avaliar o modelo em um conjunto de dados de teste separado, que não foi usado durante o treinamento. Se essa pontuação for significativamente mais baixa do que o TRAIN_SCORE, novamente pode indicar um problema de sobreajuste.

            Analisando a diferença entre o TRAIN_SCORE, TEST_SCORE e CV_SCORE, podemos ter uma ideia de como nosso modelo está se saindo em diferentes conjuntos de dados.
            ''',
            'Matriz de Confusão':
            '''
            A matriz de confusão é uma tabela que facilita a avaliação do desempenho de um algoritmo de aprendizado supervisionado. Nela, cada linha representa as instâncias de uma classe que o algoritmo previu, enquanto cada coluna representa as instâncias de uma classe real. Essa apresentação clara de verdadeiros e falsos positivos e negativos nos permite entender como o modelo está classificando as informações.
            ''',

            'Curva AUC-ROC':
            '''
            A curva ROC-AUC é uma representação visual que nos mostra o quão bem o modelo de classificação binária está diferenciando as classes. O gráfico traça a taxa de verdadeiros positivos contra a taxa de falsos positivos para diferentes pontos de corte de classificação (Acima de qual valor de probabilidade prevista é considerado classe 1). Quanto mais o modelo se aproxima do canto superior esquerdo do gráfico (taxa de verdadeiros positivos alta e taxa de falsos positivos baixa), mais eficiente ele é.
            ''',

            'Curva de Precisão-Recall':
            '''
            A curva de precisão-recall é um gráfico que mostra o equilíbrio entre a precisão (a proporção de verdadeiros positivos entre todas as previsões positivas) e a sensibilidade (a proporção de verdadeiros positivos entre todas as instâncias positivas). Um modelo cuja curva de precisão-recall se aproxima do canto superior direito do gráfico demonstra um alto nível de precisão e sensibilidade.
            ''',

            'Histograma de Probabilidade':
            '''
            O histograma de probabilidade é um gráfico que mostra a distribuição das previsões de um modelo de classificação em termos de probabilidade. Ele permite uma análise mais detalhada das previsões do modelo, oferecendo uma representação visual da probabilidade associada a cada previsão, o que pode ajudar a entender melhor a capacidade de classificação do modelo.
            ''',

            'Plot de Densidade de Probabilidade':
            '''
            A densidade de probabilidade é um gráfico que mostra a distribuição das previsões de um modelo de classificação de uma maneira mais suave em comparação ao histograma de probabilidade. Essa visualização facilita a identificação de padrões e tendências na distribuição das previsões do modelo.
            ''',

            'Plot de Calibração de Probabilidade':
            '''
            A calibração de probabilidade é um gráfico que compara as probabilidades previstas pelo modelo com as frequências observadas. Esta visualização é útil para avaliar se as previsões de probabilidade do modelo estão bem calibradas, ou seja, se a probabilidade prevista corresponde à frequência observada dos eventos.
            ''',
            'Importância das Features Permutadas': 
            '''
            
           Além da identificação das características mais relevantes para as previsões do modelo, a permutação de características também permite analisar a possibilidade de overfitting de variáveis. O gráfico resultante dessa análise não apenas destaca a importância das características, mas também compara essa importância nos dados de treinamento e teste.

           Essa comparação desempenha um papel crucial na avaliação do ajuste excessivo do modelo, também conhecido como overfitting. Se uma característica tem uma importância alta nos dados de treinamento, mas não mostra a mesma relevância nos dados de teste, isso pode ser um indicador de overfitting. Nesse caso, o modelo pode estar excessivamente ajustado aos dados de treinamento, tornando-se incapaz de generalizar bem para os dados de teste. Isso pode levar a previsões imprecisas ou falhas quando o modelo é exposto a novos dados.

           Portanto, a permutação de características e sua subsequente análise visual em um gráfico fornecem uma perspectiva crucial sobre a robustez e a generalidade do modelo, bem como a capacidade do modelo de fazer previsões confiáveis ao ser confrontado com novos dados.
                        
            '''            
            
        }


    

        text_widget = ipywidgets.Textarea(
            value=explanations[plot_type],
            layout=ipywidgets.Layout(width="100%", height="200px")
        )
        display(text_widget)

        plot_selected(plot_type)
        
    def plot_selected(plot_type):

        if plot_type == 'Métricas de Avaliação':

            evaluation_metrics()

        elif plot_type == 'Matriz de Confusão':

            matriz_confusao()

        elif plot_type == 'Curva AUC-ROC':

            roc_auc_curve()

        elif plot_type == 'Curva de Precisão-Recall':

            precision_recall()

        elif plot_type == 'Histograma de Probabilidade':

            histograma_probabilidade()

        elif plot_type == 'Plot de Densidade de Probabilidade':

            plot_densidade_probabilidade()

        elif plot_type == 'Plot de Calibração de Probabilidade':

            plot_calibracao_probabilidade()

        elif plot_type == 'Importância das Features Permutadas':

            permutation_feature_importance()

    dropdown = ipywidgets.Dropdown(options=['Métricas de Avaliação', 'Matriz de Confusão', 'Curva AUC-ROC', 'Curva de Precisão-Recall', 'Histograma de Probabilidade', 'Plot de Densidade de Probabilidade', 'Plot de Calibração de Probabilidade', 'Importância das Features Permutadas'])

    ipywidgets.interact(plot_explanation, plot_type=dropdown)
# Validar Modelos

![Python versions](https://img.shields.io/pypi/pyversions/validar_modelos)
[![GitHub Issues](https://img.shields.io/github/issues/Alexandre-Papandrea/validar_modelos)](https://github.com/Alexandre-Papandrea/validar_modelos/issues)
[![License](https://img.shields.io/github/license/Alexandre-Papandrea/validar_modelos)](https://github.com/Alexandre-Papandrea/validar_modelos/blob/main/LICENSE)

`validar_modelos` é uma biblioteca Python projetada para tornar a validação de modelos de Machine Learning mais acessível e eficiente. Com um conjunto abrangente de gráficos e métricas, esta biblioteca ajuda a simplificar e acelerar a etapa de validação do pipeline de Machine Learning.

## 🛠️ Instalação

Você pode instalar a biblioteca `validar_modelos` via pip:

```shell
pip install validar_modelos
```

## 🚀 Uso

Primeiro, importe a função `validar_regressao` ou `validar_classificacao_binaria` de `validar_modelos`:

```python
from validar_modelos import validar_regressao
from validar_modelos import validar_classificacao_binaria
```

Depois, chame a função `validar_regressao` ou `validar_classificacao_binaria` passando os argumentos adequados. Por exemplo:

```python
validar_regressao(model, X_train, y_train, X_test, y_test, cv)
validar_classificacao_binaria(model, X_train, y_train, X_test, y_test, cv, nbins, n_repeats)
```

## 🧪 Testes

Para rodar os testes, use o seguinte comando:

```shell
pytest
```

## 🤝 Contribuição

Agradecemos todas as contribuições, seja corrigindo bugs, adicionando novos recursos ou melhorando a documentação. Aqui estão algumas diretrizes:

1. Faça um fork do repositório e crie uma nova branch.
2. Faça suas alterações na nova branch.
3. Rode os testes para garantir que suas alterações não quebrem nada.
4. Faça um pull request descrevendo suas alterações. 

Se você tiver alguma dúvida ou sugestão, sinta-se à vontade para abrir uma issue.

## 👥 Mantenedores

- [Alexandre Papandrea](https://github.com/Alexandre-Papandrea)

## 📜 Licença

`validar_modelos` é licenciado sob os termos da [MIT License](LICENSE).


Leia a publicação completa sobre `validar_modelos` no [Medium](https://medium.com/@Alexandre-Papandrea/validando-modelos-de-machine-learning-com-a-biblioteca-em-python-validar_modelos-2fe64a6d1ae5).
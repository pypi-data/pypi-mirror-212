from setuptools import setup, find_packages

setup(
    name="validar_modelos",
    version="0.0.4",
    description="Ferramentas e Instruções para Validação de Modelos Clássicos",
    url="http://github.com/Alexandre-Papandrea/validar_modelos",
    author="Alexandre Papandrea",
    author_email="alexandre@dadosinteligentes.com",
    packages=find_packages(),
    install_requires=[
        "ipywidgets",
        "pandas",
        "numpy",
        "plotly",
        "scikit-learn",
        "scipy",
        "statsmodels",
        "matplotlib",
        "seaborn",
        "ipython"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
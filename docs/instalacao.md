# Instalação

## Pré-requisitos

- [pyenv](https://github.com/pyenv/pyenv) (ou [pyenv-win](https://github.com/pyenv-win/pyenv-win) no Windows).
- [Poetry](https://python-poetry.org/) (`curl -sSL https://install.python-poetry.org | python3 -`, ou via pipx).

## Passo a passo

```bash
# 1. Instalar a versão de Python exigida pelo projeto (requires-python >= 3.14)
pyenv install 3.14.5

# 2. Fixar a versão local do projeto (gera/atualiza .python-version)
pyenv local 3.14.5

# 3. Garantir que o Poetry crie o ambiente virtual dentro do projeto (.venv/)
poetry config virtualenvs.in-project true --local

# 4. Apontar o Poetry para o interpretador do pyenv
poetry env use "$(pyenv which python)"

# 5. Instalar as dependências (runtime + dev) e materializar o .venv/
poetry install

# 6. Validar o ambiente
poetry env info
```

Todo comando do projeto (executar a aplicação, testes, lint, format, docs)
deve ser executado através de `poetry run ...` — nunca com um interpretador
Python global, para garantir que as versões e dependências corretas sejam
usadas.

!!! note
    Não é necessário criar um `venv` manualmente: o Poetry cuida disso no
    passo 5, a partir da configuração do passo 3.

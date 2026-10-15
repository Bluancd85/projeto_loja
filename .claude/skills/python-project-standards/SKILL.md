---
name: python-project-standards
description: Padroniza a criação, configuração, manutenção e documentação de projetos Python usando pyenv, Poetry, Ruff, Pytest/pytest-cov (cobertura mínima 75%) e MkDocs Material. Use ao iniciar um novo projeto Python, ao auditar/corrigir a configuração de um projeto existente, ou quando o usuário pedir lint, testes, cobertura ou documentação padronizados.
---

# Padronização de Projetos Python

Manual operacional para criar, configurar, manter e documentar projetos Python profissionais com um stack fixo: **pyenv** (versão local do Python), **Poetry** (dependências, empacotamento, ambiente virtual), **venv** gerenciada pelo Poetry, **Ruff** (lint + format), **Poe the Poet** (tasks), **Pytest + pytest-cov** (testes e cobertura ≥75%) e **MkDocs Material** (documentação).

Esta skill não é uma lista de tecnologias — é um procedimento. Cada seção abaixo deve ser **executada**, não apenas descrita.

## 1. Objetivo e escopo

Aplicar este padrão sempre que você for:
- Criar um projeto Python novo do zero.
- Auditar ou corrigir a configuração de um projeto Python existente que deveria seguir este padrão.
- Adicionar lint, testes, cobertura ou documentação a um projeto que não os tem.
- Revisar se um projeto está em conformidade antes de uma entrega.

Fora de escopo: escolha de frameworks de aplicação (web, CLI, dados etc.) — esta skill cobre apenas a infraestrutura de engenharia (ambiente, qualidade, testes, docs), não a lógica de negócio do projeto.

## 2. Pré-requisitos

Antes de qualquer alteração, verifique se as ferramentas existem no ambiente:

```bash
pyenv --version
poetry --version
```

- Se `pyenv` não estiver instalado: informe o usuário e oriente a instalação (ex.: `curl https://pyenv.run | bash` em Linux/macOS, ou o instalador equivalente da plataforma). Não prossiga silenciosamente sem pyenv — a seleção de versão local depende dele.
- Se `poetry` não estiver instalado: oriente a instalação oficial (`curl -sSL https://install.python-poetry.org | python3 -`) ou via pipx. Não use `pip install poetry` dentro de um ambiente de projeto.
- Se alguma ferramenta não puder ser instalada por limitação do ambiente de execução, **registre essa limitação explicitamente** no relato final — nunca finja que a etapa foi concluída.

## 3. Regras de execução (não-negociáveis)

1. O Poetry administra o `.venv/`. **Nunca** execute `python -m venv` manualmente nem crie um ambiente concorrente.
2. O `pyenv` define a versão local via `.python-version`. Essa versão deve satisfazer o `requires-python` declarado no `pyproject.toml`; se houver conflito, corrija um dos dois — não ignore.
3. O Ruff é a **única** ferramenta de lint e formatação. Lint e format são operações distintas, cada uma com sua própria task (`poetry run task lint` e `poetry run task format`) — não as combine em um único comando.
4. A cobertura mínima de testes é **75%** medida sobre o código real em `src/<pacote>`, nunca apenas sobre os arquivos de teste. Não reduza esse número artificialmente via exclusões injustificadas, testes triviais (que não afirmam nada relevante) ou remoção de código da medição.
5. O MkDocs Material deve ser executável via `poetry run mkdocs ...`, sem depender de instalação global.
6. Nunca declare uma validação como bem-sucedida sem ter executado o comando correspondente e observado a saída real.
7. Em projetos preexistentes: inspecione a estrutura e as configurações atuais antes de alterar qualquer arquivo. Preserve o que já funciona; não sobrescreva configurações úteis sem justificativa técnica registrada.

## 4. Procedimento — configuração do ambiente

Execute nesta ordem (substitua `<VERSAO_PYTHON>` por uma versão estável e compatível, ex. `3.12.7`):

```bash
# 1. Instalar a versão escolhida (se ainda não disponível)
pyenv install <VERSAO_PYTHON>

# 2. Fixar a versão local do projeto (cria/atualiza .python-version)
pyenv local <VERSAO_PYTHON>

# 3. Garantir que o Poetry crie o venv dentro do projeto
poetry config virtualenvs.in-project true --local

# 4. Apontar o Poetry para o interpretador do pyenv
poetry env use "$(pyenv which python)"

# 5. Instalar dependências e materializar o .venv/
poetry install

# 6. Validar
poetry env info
```

Esclarecimentos:
- `.python-version` (gerado pelo pyenv) define a versão **local** selecionada para este diretório.
- `requires-python` no `pyproject.toml` define a **faixa de compatibilidade** exigida pelo projeto — a versão do pyenv deve estar dentro dessa faixa.
- O Poetry cria ou reutiliza o ambiente em `.venv/` na raiz do projeto (graças ao passo 3). Todo comando de execução, lint, teste ou doc deve passar por `poetry run ...` (ou pelo shell do Poetry), nunca por um interpretador global.

## 5. Estrutura padronizada do projeto

```text
projeto/
├── .venv/                      # ambiente virtual, criado e gerenciado pelo Poetry — não versionar
├── docs/                        # fonte da documentação (MkDocs)
│   └── index.md
├── src/
│   └── projeto/                # código da aplicação (layout src/)
│       ├── __init__.py
│       └── ...
├── tests/                       # testes automatizados (pytest)
│   ├── conftest.py
│   └── ...
├── .python-version              # versão local fixada pelo pyenv
├── .gitignore                    # exclui .venv/, caches, builds, artefatos
├── mkdocs.yml                    # configuração do MkDocs Material
├── pyproject.toml                # metadados, dependências, config de todas as ferramentas
├── poetry.lock                    # versionar em projetos de aplicação (instalações reprodutíveis)
└── SKILL.md
```

Regras de estrutura:
- Use sempre o layout `src/` — nunca coloque o pacote importável na raiz do repositório.
- Configure `[tool.poetry] packages = [{include = "projeto", from = "src"}]` (ou equivalente) para que o empacotamento encontre o pacote em `src/`.
- Mantenha todo teste em `tests/`, espelhando a estrutura de `src/projeto` quando fizer sentido.
- `.gitignore` deve excluir no mínimo: `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.ruff_cache/`, `htmlcov/`, `.coverage`, `dist/`, `build/`, `site/` (saída do `mkdocs build`).
- Versione `poetry.lock` em projetos de aplicação (não bibliotecas publicadas de forma solta) para garantir que todos instalem exatamente as mesmas versões.
- Não crie arquivos, pastas ou configurações extras sem uma razão técnica — se um diretório do template não se aplica ao projeto, omita-o e justifique.

## 6. Ruff — lint e formatação

Adicione o Ruff e o Poe the Poet como dependências de desenvolvimento:

```bash
poetry add --group dev ruff poethepoet
```

Configure no `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py312"
line-length = 100
exclude = ["dist", "build", "site", ".venv"]

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.poe.tasks]
lint = "ruff check ."
format = "ruff format ."
```

- `lint` (`ruff check .`) identifica erros, importações não utilizadas e problemas de qualidade — não reformata o código.
- `format` (`ruff format .`) aplica a formatação padronizada — não substitui a análise de lint.
- Sempre execute as duas tasks via Poetry:

```bash
poetry run task lint
poetry run task format
```

- Se `poetry run task lint` falhar com "task not found", confirme que `[tool.poe.tasks]` está no `pyproject.toml` e que `poethepoet` foi instalado como dev dependency (o plugin é descoberto automaticamente pelo Poetry 1.2+ via `poetry-plugin` ou executado como `poe` dentro do venv — valide com `poetry run poe lint` se `task` não for reconhecido no ambiente do usuário).

## 7. Pytest — testes automatizados e cobertura

Adicione as dependências de teste:

```bash
poetry add --group dev pytest pytest-cov
```

Configure no `pyproject.toml` (ajuste `projeto` para o nome real do pacote em `src/`):

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "--cov=projeto",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=75",
]
```

Regras de teste:
- Arquivos `test_*.py`, funções `test_*`, dentro de `tests/`.
- Use fixtures (`conftest.py`) para setup compartilhado.
- Isole dependências externas (rede, banco, serviços de terceiros) com dublês de teste — não dependa de serviços reais em testes unitários, salvo quando isso for explicitamente o objetivo (ex.: teste de integração marcado como tal).
- Cubra casos normais, de limite, entradas inválidas e exceções relevantes — não apenas o caminho feliz.
- Teste comportamento observável, não detalhes internos de implementação.

Execução:

```bash
poetry run pytest
# ou, explicitamente:
poetry run pytest --cov=projeto --cov-report=term-missing --cov-report=html
```

A cobertura de 75% é medida sobre `src/projeto`, não sobre os testes. Se a cobertura reportada parecer artificialmente alta ou baixa, verifique se o pytest está de fato importando o pacote instalado pelo Poetry a partir de `src/` (um `poetry install` ausente ou um `pyproject.toml` com `packages` mal configurado causa isso).

## 8. MkDocs Material — documentação

Adicione as dependências de documentação:

```bash
poetry add --group dev mkdocs mkdocs-material
```

Estrutura inicial de `docs/`:

```text
docs/
├── index.md            # propósito do projeto, visão geral
├── instalacao.md       # pyenv + Poetry, passo a passo de setup
├── uso.md               # como executar a aplicação
├── arquitetura.md       # decisões arquiteturais relevantes, quando houver
├── desenvolvimento.md   # como contribuir, lint, format, testes
└── testes.md            # como executar e interpretar os testes/cobertura
```

Exemplo de `mkdocs.yml`:

```yaml
site_name: Projeto
site_description: Descrição real do projeto
theme:
  name: material
  language: pt-BR
  features:
    - navigation.tabs
    - content.code.copy

nav:
  - Início: index.md
  - Instalação: instalacao.md
  - Uso: uso.md
  - Arquitetura: arquitetura.md
  - Desenvolvimento: desenvolvimento.md
  - Testes: testes.md

markdown_extensions:
  - admonition
  - pymdownx.highlight
  - pymdownx.superfences
  - toc:
      permalink: true
```

Cada página deve conter conteúdo real e específico do projeto — propósito, instalação/configuração do ambiente, como executar a aplicação, como rodar testes e cobertura, como executar lint/format, como gerar/visualizar a documentação, como contribuir, e decisões arquiteturais quando aplicável. Não deixe páginas vazias ou genéricas.

Comandos (sempre via Poetry, nunca com MkDocs instalado globalmente):

```bash
poetry run mkdocs serve   # preview local
poetry run mkdocs build   # build estático, falha em erros de nav/links quebrados
```

## 9. `pyproject.toml` consolidado (referência)

```toml
[project]
name = "projeto"
version = "0.1.0"
description = "Descrição real do projeto"
authors = [{name = "Nome", email = "email@exemplo.com"}]
readme = "README.md"
requires-python = ">=3.12,<3.13"
dependencies = []

[tool.poetry]
packages = [{include = "projeto", from = "src"}]

[tool.poetry.group.dev.dependencies]
ruff = "*"
poethepoet = "*"
pytest = "*"
pytest-cov = "*"
mkdocs = "*"
mkdocs-material = "*"

[tool.ruff]
target-version = "py312"
line-length = 100
exclude = ["dist", "build", "site", ".venv"]

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "--cov=projeto",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=75",
]

[tool.poe.tasks]
lint = "ruff check ."
format = "ruff format ."

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

Ajuste `requires-python` para uma faixa compatível com a versão fixada pelo pyenv, e `projeto` para o nome real do pacote em todos os lugares em que aparece.

## 10. Fluxo obrigatório de validação

Execute **sempre**, nesta ordem, após criar ou modificar o projeto. Corrija e re-execute qualquer etapa que falhar antes de seguir para a próxima.

```bash
# 1-3. Ambiente
python --version
pyenv version
poetry env info

# 4. Dependências
poetry install

# 5-7. Qualidade (lint -> format -> lint de novo, para ver o que restou)
poetry run task lint
poetry run task format
poetry run task lint

# 8-9. Testes e cobertura (a task pytest já falha automaticamente se < 75%)
poetry run pytest

# 10. Documentação
poetry run mkdocs build
```

- Se qualquer comando falhar: leia a causa real do erro, corrija o problema na configuração ou no código, e execute novamente a(s) etapa(s) afetada(s) — não pule para a etapa seguinte com uma falha pendente.
- Não declare uma etapa como "concluída" ou "passou" sem ter rodado o comando e visto a saída. Se o ambiente de execução não permitir rodar algum comando, diga isso explicitamente no relato, em vez de assumir sucesso.

## 11. Boas práticas de engenharia

- Código simples, modular, legível e testável; responsabilidade única, baixo acoplamento.
- Type hints nas interfaces relevantes (assinaturas públicas, contratos entre módulos).
- Sem duplicação de código; sem abstrações prematuras ou complexidade sem necessidade atual.
- Tratamento de erros explícito nos pontos em que falhas são esperadas.
- Nenhuma dependência nova sem necessidade real.
- Nenhum segredo ou credencial no código-fonte — use variáveis de ambiente para configuração sensível.
- Testes validam comportamento observável, não a implementação interna.
- Atualize a documentação sempre que o comportamento público mudar.
- Em projetos existentes, preserve configurações e funcionalidades já presentes; não sobrescreva sem justificativa.

## 12. Regras operacionais da IA ao aplicar esta skill

1. Inspecionar a estrutura existente antes de alterar qualquer arquivo.
2. Identificar a versão de Python compatível com o projeto (pyenv local vs. `requires-python`).
3. Verificar quais ferramentas e dependências já estão disponíveis antes de assumir que faltam.
4. Criar ou ajustar apenas a estrutura necessária — sem excesso.
5. Implementar configurações funcionais de fato (arquivos reais, comandos que rodam), não apenas descrever o que "deveria" existir.
6. Executar as verificações automatizadas da Seção 10.
7. Corrigir erros e regressões introduzidos pelas próprias alterações antes de encerrar.
8. Documentar decisões técnicas relevantes (ex.: por que uma versão de Python ou uma exceção de lint foi escolhida).
9. Relatar claramente ao usuário: o que foi executado, o que passou, o que falhou e o que ficou pendente.

Nunca inventar resultados de execução, arquivos existentes, métricas de cobertura ou funcionalidades implementadas. Quando não for possível executar um comando por limitação do ambiente, registrar essa limitação explicitamente em vez de presumir um resultado.

## 13. Diagnóstico de problemas comuns

| Sintoma | Causa provável | Correção |
|---|---|---|
| `poetry env use "$(pyenv which python)"` falha ou usa interpretador errado | pyenv não tem a versão instalada, ou shims do pyenv não estão no `PATH` | `pyenv install <versão>`; confirmar `pyenv which python` aponta para o shim correto antes de rodar o comando |
| Poetry ignora `.python-version` / usa outra versão | `requires-python` no `pyproject.toml` não inclui a versão fixada pelo pyenv | Alinhar a faixa de `requires-python` com a versão local, ou trocar a versão local para uma dentro da faixa |
| `poetry run task lint` ou `task format` não encontrado | `poethepoet` não instalado como dev dependency, ou `[tool.poe.tasks]` ausente/mal formatado no `pyproject.toml` | `poetry add --group dev poethepoet`; validar a seção `[tool.poe.tasks]`; testar com `poetry run poe lint` como alternativa |
| `ruff format` e `ruff check` entram em conflito (format desfaz o que o lint pediu) | Regras de lint incompatíveis com o formatador (ex.: regras de estilo que o formatter já controla) | Remover do `select` regras de estilo puro já cobertas pelo formatter (ex. `E501` quando `line-length` já é respeitado pelo format); manter `format` e `lint` como operações complementares, não concorrentes |
| Cobertura reportada muito abaixo (ou acima) do esperado | `--cov=projeto` não corresponde ao nome real do pacote em `src/`, ou o pacote não foi instalado via `poetry install` | Confirmar que `--cov` usa o nome exato do pacote em `src/<pacote>`; rodar `poetry install` antes dos testes; confirmar `[tool.poetry] packages` aponta para `src/` |
| `mkdocs build` falha com erro de navegação | `nav` em `mkdocs.yml` referencia um arquivo `.md` que não existe em `docs/` | Criar o arquivo faltante ou remover a entrada da `nav`; rodar `poetry run mkdocs build` novamente para confirmar |

## 14. Checklist final de validação

- [ ] `pyenv` seleciona a versão local do Python (`.python-version` presente e coerente com `requires-python`).
- [ ] Poetry gerencia dependências e ambiente virtual (nenhum `venv`/`virtualenv` manual concorrente).
- [ ] `.venv/` está em uso dentro do projeto (`poetry config virtualenvs.in-project true --local` aplicado).
- [ ] Tasks `poetry run task lint` e `poetry run task format` existem e executam sem erro de configuração.
- [ ] Ruff configurado em `[tool.ruff]`/`[tool.ruff.lint]` no `pyproject.toml`.
- [ ] Pytest configurado em `[tool.pytest.ini_options]`, testes em `tests/`, nomenclatura `test_*`.
- [ ] Cobertura mínima de 75% atingida sobre `src/<projeto>` real, sem exclusões artificiais, com `--cov-fail-under=75` ativo.
- [ ] MkDocs Material configurado (`mkdocs.yml` + `docs/`) e `poetry run mkdocs build` executa sem erro.
- [ ] Todas as configurações (`pyproject.toml`, `mkdocs.yml`, tasks) são coerentes entre si (nomes de pacote, caminhos).
- [ ] O fluxo de validação da Seção 10 foi executado nesta sessão, nesta ordem, com resultados reais observados.
- [ ] Nenhuma etapa foi declarada como concluída sem evidência de execução; limitações de ambiente foram registradas explicitamente quando houve.

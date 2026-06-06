# Dodo Starter Pack - Manifesto Anti-Vibe Coding

> Esse arquivo e lido pelo Claude no inicio de toda conversa.
> **Mantenha curto e direto.** Para regras deterministicas, use `.claude/settings.json`.
> Para conhecimento sob demanda e guias operacionais, consulte `.claude/skills/`.

## Regras Globais

**Este projeto segue as regras GSD definidas em `C:\Users\Admin\.claude\CLAUDE.md`:**
- Caveman Mode full
- RTK obrigatorio em terminal
- Fluxo GSD 4-D (Discuss -> Plan -> Execute -> Verify)
- Memoria ID-based (`resumo-de-trabalho.md`)
- Subagentes para tarefas complexas

**O que esta abaixo sao regras ESPECIFICAS deste projeto.**

---

## Stack do Projeto

- **Frontend:** HTML5, CSS3 Vanilla, JavaScript Moderno (ES6+)
- **Backend/Scripting:** Python 3.10+
- **Quality & Linting:** Ruff (Python), ESLint/Prettier (JS/HTML/CSS)
- **Testing:** Pytest (Python)

## Comandos Essenciais

```bash
# Setup de Ambiente
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Qualidade (RTK Mindset)
ruff check .
ruff format .
npx prettier --write .
pytest
```

## Regras Inegociaveis (Anti-Vibe Coding)

1.  **Codigo Sem Testes Nao Entra**: Cada nova logica publica ou funcionalidade deve ser acompanhada por testes equivalentes.
2.  **Nao Simule Execucoes**: Proibido fingir que um comando ou linter funcionou sem de fato roda-lo e obter o resultado real.
3.  **Auditoria Paginada (ID-Based)**: Qualquer mutacao ou decisao arquitetural deve ser registrada no `resumo-de-trabalho.md` sob um ID de observacao estruturado `[OBS-YYYYMMDD-NN]`.
4.  **Uso de Proxy RTK**: Toda interacao de terminal de desenvolvimento deve ser realizada de forma otimizada para tokens.

## Estrutura de Dominio Recomendada

```
dodo-project/
|-- .claude/                   # Configuracoes do Claude Code
|   |-- settings.json          # Permissoes deterministicas e hooks wired
|   +-- skills/                # progressive disclosure de conhecimentos
|-- .githooks/                 # Hooks de git integrados para seguranca
|-- docs/                      # Documentacao tecnica do GSD Flow e RTK
|-- tests/                     # Suite de testes automatizados
|-- resumo-de-trabalho.md      # Historico linear de auditoria tecnica (GSD)
+-- CLAUDE.md                  # Esse manifesto
```

## Referencia Cruzada

> Regras globais de orquestracao, subagentes, auto-aperfeicoamento e correcao autonoma estao definidas em `C:\Users\Admin\.claude\CLAUDE.md`. Este manifesto contem apenas regras especificas do projeto.

## Setup Obrigatorio (Primeira Execucao)

Ao iniciar neste projeto pela primeira vez, execute:
- Windows: `.\setup.ps1`
- Linux/macOS: `bash setup.sh`

Isso ativa os hooks de seguranca e qualidade (.githooks). Sem isso, commits nao serao validados.

# Graph Report - mediaDownloader (2026-06-02)

## Corpus Check

- 17 files · ~6,035 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary

- 130 nodes · 130 edges · 14 communities (12 shown, 2 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness

- Built from commit: `c20ae273`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)

- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]

## God Nodes (most connected - your core abstractions)

1. `Kwai Downloader` - 15 edges
2. `get_kwai_info()` - 10 edges
3. `download_mp3()` - 8 edges
4. `sanitize_filename()` - 8 edges
5. `rules` - 7 edges
6. `download_mp4()` - 7 edges
7. `extract_url()` - 6 edges
8. `Design do Projeto: dwKwai Downloader` - 6 edges
9. `cleanup_file()` - 5 edges
10. `🦤 Dodo Starter Pack - Manifesto Anti-Vibe Coding` - 5 edges

## Surprising Connections (you probably didn't know these)

- `info()` --calls--> `get_kwai_info()` [INFERRED]
  main.py → scraper.py
- `download_mp4()` --calls--> `extract_url()` [INFERRED]
  main.py → scraper.py
- `download_mp4()` --calls--> `get_kwai_info()` [INFERRED]
  main.py → scraper.py
- `download_mp4()` --calls--> `sanitize_filename()` [INFERRED]
  main.py → scraper.py
- `download_mp3()` --calls--> `extract_url()` [INFERRED]
  main.py → scraper.py

## Communities (14 total, 2 thin omitted)

### Community 0 - "Community 0"

Cohesion: 0.10
Nodes (25): AppState, cleanup_file(), download_mp3(), download_mp4(), info(), Remove arquivo temporário., Remove arquivo temporário., Remove arquivo temporário. (+17 more)

### Community 1 - "Community 1"

Cohesion: 0.11
Nodes (18): 🏗️ Arquitetura, 📦 Build e Deploy, 🚀 Como rodar localmente, 🔗 Demo, 📂 Estrutura do projeto, 🔄 Fluxo principal da aplicação, ⚙️ Highlights técnicos, Kwai Downloader (+10 more)

### Community 2 - "Community 2"

Cohesion: 0.20
Nodes (8): crypto, diretorioBase, diretoriosIgnorados, extensoesAlvo, fs, gerarHash(), path, processarUrl()

### Community 3 - "Community 3"

Cohesion: 0.12
Nodes (15): env, browser, es2021, node, extends, parserOptions, ecmaVersion, sourceType (+7 more)

### Community 4 - "Community 4"

Cohesion: 0.20
Nodes (9): 🧠 A Lei da Memória Virtual (ID-Based), Fase 1: Discuss & Diagnose (A Regra do Mago Acadêmico), Fase 2: Plan & Develop (O Planejamento Checklist), Fase 3: Execute & Deliver (Execução Atômica e Testabilidade), Fase 4: Verify & Commit (UAT e Auditoria de Mutação), 🚀 Fluxo GSD (Get Shit Done) 4-D & Protocolo de Memória, O Arquivo `resumo-de-trabalho.md`, 🏛️ O Fluxo GSD 4-D em Quatro Etapas (+1 more)

### Community 5 - "Community 5"

Cohesion: 0.25
Nodes (7): 1. Camada de Filtro (Precision Search), 2. Camada de Scan (Linhas Imediatas), 3. Camada de Deep Dive (Leitura Seletiva), 🏎️ O Protocolo de Busca Cirúrgica em 3 Camadas, 🛡️ Prefixo RTK Obrigatório no Terminal, ⚡ RTK (Rust Token Killer) Mindset — Eficiência de Tokens, 🔇 Supressão de Ruído no Terminal

### Community 6 - "Community 6"

Cohesion: 0.29
Nodes (6): 🏗️ Arquitetura do Sistema, Design do Projeto: dwKwai Downloader, 🚀 Estratégia de Deploy, 🔄 Fluxo de Dados, 📋 Registro de Decisões (Decision Log), 🛠️ Stack Tecnológica

### Community 7 - "Community 7"

Cohesion: 0.29
Nodes (6): Garante que segredos reais sejam casados pelas regexes de segurança., Valida se caminhos protegidos e secretos são interceptados de forma correta., Valida se o formato Conventional Commit + ID de Observação é rigidamente exigido, test_commit_msg_validation(), test_pre_commit_protected_paths(), test_pre_commit_secret_detection()

### Community 8 - "Community 8"

Cohesion: 0.33
Nodes (5): 🚀 Comandos Essenciais, 🦤 Dodo Starter Pack - Manifesto Anti-Vibe Coding, 📁 Estrutura de Domínio Recomendada, 🔒 Regras Inegociáveis (Anti-Vibe Coding), 🛠️ Stack do Projeto

### Community 9 - "Community 9"

Cohesion: 0.47
Nodes (5): get_staged_files(), main(), Retorna a lista de arquivos no stage (staged)., Varre um arquivo em busca de segredos e caminhos protegidos., scan_file()

### Community 10 - "Community 10"

Cohesion: 0.40
Nodes (4): Meta Commands, RTK - Rust Token Killer (Google Antigravity), Rule, Why

## Knowledge Gaps

- **60 isolated node(s):** `browser`, `es2021`, `node`, `extends`, `ecmaVersion` (+55 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions

_Questions this graph is uniquely positioned to answer:_

- **Are the 3 inferred relationships involving `get_kwai_info()` (e.g. with `download_mp3()` and `download_mp4()`) actually correct?**
  _`get_kwai_info()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `download_mp3()` (e.g. with `extract_url()` and `get_kwai_info()`) actually correct?**
  _`download_mp3()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `sanitize_filename()` (e.g. with `download_mp3()` and `download_mp4()`) actually correct?**
  _`sanitize_filename()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `browser`, `es2021`, `node` to the rest of the system?**
  _82 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.0960591133004926 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._

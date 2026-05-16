# Graph Report - kwaiDownloader  (2026-05-16)

## Corpus Check
- 3 files · ~3,713 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 21 nodes · 27 edges · 4 communities (3 shown, 1 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7b994930`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]

## God Nodes (most connected - your core abstractions)
1. `get_kwai_info()` - 7 edges
2. `download_mp3()` - 5 edges
3. `extract_url()` - 5 edges
4. `download_mp4()` - 4 edges
5. `cleanup_file()` - 3 edges
6. `sanitize_filename()` - 3 edges
7. `info()` - 2 edges
8. `gerarHash()` - 2 edges
9. `processarUrl()` - 2 edges
10. `Remove arquivo temporário.` - 1 edges

## Surprising Connections (you probably didn't know these)
- `info()` --calls--> `get_kwai_info()`  [INFERRED]
  main.py → scraper.py
- `download_mp4()` --calls--> `get_kwai_info()`  [INFERRED]
  main.py → scraper.py
- `download_mp3()` --calls--> `extract_url()`  [INFERRED]
  main.py → scraper.py
- `download_mp3()` --calls--> `get_kwai_info()`  [INFERRED]
  main.py → scraper.py
- `download_mp4()` --calls--> `extract_url()`  [INFERRED]
  main.py → scraper.py

## Communities (4 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.33
Nodes (5): cleanup_file(), download_mp3(), info(), Remove arquivo temporário., Gera MP3 via FFmpeg e envia.

### Community 1 - "Community 1"
Cohesion: 0.5
Nodes (4): get_kwai_info(), Limpa nome do arquivo: letras, números e espaços (Opção 1)., Extrai metadados do vídeo Kwai usando yt-dlp., sanitize_filename()

### Community 3 - "Community 3"
Cohesion: 0.5
Nodes (4): download_mp4(), Proxy para download do MP4 com nome personalizado., extract_url(), Extrai link do Kwai de um texto usando Regex.

## Knowledge Gaps
- **6 isolated node(s):** `Remove arquivo temporário.`, `Proxy para download do MP4 com nome personalizado.`, `Gera MP3 via FFmpeg e envia.`, `Extrai link do Kwai de um texto usando Regex.`, `Limpa nome do arquivo: letras, números e espaços (Opção 1).` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_kwai_info()` connect `Community 1` to `Community 0`, `Community 3`?**
  _High betweenness centrality (0.234) - this node is a cross-community bridge._
- **Why does `download_mp3()` connect `Community 0` to `Community 1`, `Community 3`?**
  _High betweenness centrality (0.176) - this node is a cross-community bridge._
- **Why does `download_mp4()` connect `Community 3` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `get_kwai_info()` (e.g. with `info()` and `download_mp4()`) actually correct?**
  _`get_kwai_info()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `download_mp3()` (e.g. with `extract_url()` and `get_kwai_info()`) actually correct?**
  _`download_mp3()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `extract_url()` (e.g. with `download_mp4()` and `download_mp3()`) actually correct?**
  _`extract_url()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `download_mp4()` (e.g. with `extract_url()` and `get_kwai_info()`) actually correct?**
  _`download_mp4()` has 2 INFERRED edges - model-reasoned connections that need verification._
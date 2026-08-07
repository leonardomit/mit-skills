# SETUP — Instalação única do fluxo

> Fazer 1 vez no Mac. Tempo estimado: 30–45 min.
> Comandos validados contra a doc oficial em 06/08/2026. Onde houver ⚠️, conferir a doc viva antes.

## 0. Pré-requisitos

```bash
git --version                 # git instalado
brew install gh && gh auth login   # GitHub CLI (workers abrem PR com ele)
node --version                # Node p/ npx (instalar via brew se faltar)
```

## 1. Instalar o Orca

```bash
brew install --cask stablyai/orca/orca
```

Abrir o app → adicionar seu(s) repositório(s). Gratuito, open source (MIT).

## 2. Configurar os agentes

**Settings → Agents:**

- **Claude Code** — login com sua conta Max na primeira sessão. É o agente padrão de tudo.
- **Codex** — ⚠️ requer assinatura ChatGPT (Plus/Pro) ou API key OpenAI, que você ainda não tem.
  Quando contratar: `npm install -g @openai/codex`, depois `codex` → sign in with ChatGPT (conferir comando atual na doc do Codex).
- **Grok** — conferir **x.ai/cli**: o acesso ao CLI muda com frequência e pode estar incluso no SuperGrok/X Premium+. Senão, API xAI à parte.

> O fluxo funciona 100% só com Claude. Codex/Grok são opcionais e plugáveis depois, sem refazer nada.

## 3. Permissões — LER ANTES DE LIGAR YOLO

O Orca vem em **Yolo por padrão** (Claude roda com `--dangerously-skip-permissions`).

Regra deste fluxo:

- **Yolo:** só em repos isolados, sem segredos, sem acesso a dados de produção.
- **Manual:** repos com credenciais, integrações reais (ERP, NF-e, financeiro) ou qualquer coisa irreversível.
- Trocar em **Settings → Agents → Agent Permissions** (global ou por agente).
- **Nunca** deixar `.env`/segredos versionados no repo — todo worktree herda o conteúdo.

## 4. Habilitar o CLI

**Settings → Experimental → CLI**, depois verificar:

```bash
command -v orca
orca status --json
```

## 5. Instalar as skills oficiais do Orca

```bash
npx skills add https://github.com/stablyai/orca --skill orca-cli --global
npx skills add https://github.com/stablyai/orca --skill orchestration --global
npx skills add https://github.com/stablyai/orca --skill orca-linear --global   # só p/ modo Linear
```

## 6. Instalar as skills deste kit (Claude Code global)

```bash
cp -R "/Users/Mitsuo/Documents/Obsidian Vault/orca-workflow/skills/plan-tickets" ~/.claude/skills/
cp -R "/Users/Mitsuo/Documents/Obsidian Vault/orca-workflow/skills/orchestrate-tickets" ~/.claude/skills/
```

Ficam disponíveis como `/plan-tickets` e `/orchestrate-tickets` em qualquer repo. (O Orca escaneia os diretórios de skills de Claude, Codex, Agent Skills e OMP.)

## 7. Linear (opcional — modo híbrido)

**Settings → Integrations → Linear** → colar API token pessoal (Linear → Settings → API) → escolher teams.
Com isso: criar worktree a partir de uma issue preenche nome/branch e injeta descrição, comentários e imagens no contexto do agente.

## 8. Teste de fumaça (5 min)

```bash
orca worktree create --name teste-fluxo --agent claude \
  --prompt "Crie um arquivo HELLO.md com a data de hoje e nada mais." --json
orca worktree list --json
```

Ver o diff no Orca, descartar o worktree. Se funcionou, o fluxo está pronto — seguir para o `PLAYBOOK.md`.

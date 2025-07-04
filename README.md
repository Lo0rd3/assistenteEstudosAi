
# 🧠 Assistente de Estudos AI

**Assistente de Estudos AI** é uma aplicação interativa em Python que utiliza a API do Gemini da Google para ajudar estudantes e profissionais de IT a estudarem de forma mais eficaz. A aplicação gera automaticamente:

- ✅ **Resumos técnicos**
- 🧾 **CheatSheets práticos**
- 🎯 **Quizzes interativos com correção automática**
- 🧠 **Flashcards para memorização ativa**
- 📚 **Sessões de prática com feedback**

Tudo em **português europeu**, com foco em **tecnologia, informática, redes, DevOps, sysadmin e cloud**.

---

## ✨ Funcionalidades

| Módulo | Descrição |
|--------|-----------|
| 📄 Resumos | Geração automática de resumos técnicos exaustivos e académicos sobre qualquer tema |
| 🧾 Cheatsheets | Geração de cheatsheets limpos e estruturados (Markdown ou texto) para referência rápida |
| 🧠 Flashcards | Criação de flashcards personalizados e prática interativa com feedback e pontuação |
| 🎯 Quizzes | Criação de quizzes de escolha múltipla com diferentes níveis de dificuldade e correção gerada automaticamente |
| 📂 Armazenamento | Os conteúdos são guardados localmente em pastas por tipo: `resumos/`, `cheatsheets/`, `flashcards/`, `quizzes/` |

---

## ⚙️ Requisitos

- Python 3.8+
- Chave de API do Gemini da Google

### Instalação

```bash
git clone https://github.com/Lo0rd3/assistenteEstudosAi.git
cd assistenteEstudosAi
pip install -r requirements.txt
```

Crie um ficheiro `.env` com a sua chave de API:

```
GeminiApiKey=SUA_CHAVE_AQUI
```

---

## 🚀 Como usar

Execute o programa principal:

```bash
python main.py
```

Escolha entre as opções:

```
==== Assistente de Estudos ====
[1] Gerar Resumos
[2] Gerar CheatSheets
[3] Fazer Quiz Interativo
[4] Gerar Flashcards
[5] Praticar Flashcards
[0] Sair
```

---

## 📁 Estrutura do Projeto

```
assistenteEstudosAi/
├── cheatsheet.py           # Geração de cheatsheets
├── flashcards.py           # Geração e prática de flashcards
├── resumo.py               # Geração de resumos técnicos
├── quiz.py                 # Criação e correção de quizzes
├── utils.py                # Funções auxiliares (ex: API key)
├── main.py                 # Menu principal da aplicação
├── requirements.txt        # Dependências
├── SumaryPrompt.txt        # Prompt base para resumos
├── CheatsheetPrompt.txt    # Prompt base para cheatsheets
└── ...
```

---

## 🧪 Exemplos

- Flashcards gerados são exportados em `.csv` e compatíveis com Anki, Quizlet e RemNote.
- Quizzes podem ser salvos como `.md` ou `.txt`, com correção completa.
- Resumos são formatados para Markdown (ex: Obsidian) ou texto simples.

---

## 📜 Licença

Este projeto é distribuído sob a licença MIT.

---

## 🙋‍♂️ Contribuição

Pull requests são bem-vindos! Sinta-se à vontade para sugerir melhorias, funcionalidades ou corrigir bugs.

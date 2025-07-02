from utils import getApiKey
import os
from openai import OpenAI
import openai

def generateSumary():
    openai.api_key = getApiKey()
    client = OpenAI(api_key=openai.api_key)

    while True:
        theme = input("Tema do resumo: ").strip()
        if not theme:
            print("Tema não pode estar vazio.")
        else:
            break
    while True:
        print("\nEm que formato deseja guardar o resumo?")
        print("[1] Markdown (.md, para Obsidian)")
        print("[2] Texto Simples (.txt)")
        choice = input("Escolha: ").strip()
    
        if choice == "1":
            sumaryFormat = "Markdown para Obsidian, com sintaxe adequada."
            extension = ".md"
            break
        elif choice == "2":
            sumaryFormat = ".txt, texto simples."
            extension = ".txt"
            break
        else:
            print("Opção inválida.")
            

    promptBase = readPrompt()
    if promptBase is None: return

    prompt = promptBase.replace("{theme}", theme).replace("{sumaryFormat}", sumaryFormat)
    msg = [{"role": "system", "content": prompt}]

    while True:
        print("\nConsultando GPT...\n")
        answer = client.chat.completions.create(
            model="gpt-4.1-mini-2025-04-14",
            messages=msg,
            temperature=0.3,
            max_tokens=2000
        )
        sumary = answer.choices[0].message.content

        print("\n=== RESUMO GERADO ===\n")
        print(sumary)
        print("\nO que deseja fazer?")
        print("[1] Guardar este resumo")
        print("[2] Pedir alteraçoes ao GPT")
        print("[0] Voltar ao menu")
        op = input("Escolha: ").strip()

        if op == "1":
            if not os.path.exists("resumos"):
                os.makedirs("resumos")
            outputPath = os.path.join("resumos", theme.replace(" ", "_") + extension)
            with open(outputPath, "w", encoding="utf-8") as f:
                f.write(sumary)
            print(f"Resumo guardado em: {outputPath}")
            break
        elif op == "2":
            while True:
                    newQuestion = input("Digite o seu comentário: ").strip()
                    if newQuestion:
                        msg.append({"role": "user", "content": newQuestion})
                        break
                    else:
                        print("Entrada vazia — voltando ao menu.")
        elif op == "0":
            break
        else:
            print("Opção inválida.")

def readPrompt():
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    filePath = os.path.join(scriptDir, "SumaryPrompt.txt")
    try:
        with open(filePath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Arquivo SumaryPrompt.txt não encontrado em {filePath}!")
        return None

import os
from openai import OpenAI
import openai

def ler_prompt_base():
    try:
        with open("promptResumo.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("Arquivo promptResumo.txt não encontrado!")
        return None

def obter_api_key():
    caminho = "chatgptKey.txt"
    if os.path.exists(caminho):
        chave = open(caminho, "r", encoding="utf-8").read().strip()
        if chave:
            return chave
    # pedir se não existir ou estiver vazio
    return input("Cole a sua OpenAI API Key: ").strip()

def gerar_resumo():
    openai.api_key = obter_api_key()
    client = OpenAI(api_key=openai.api_key)

    tema = input("Tema do resumo: ").strip()
    if not tema:
        print("Tema não pode ser vazio.")
        return

    print("\nEm que formato deseja o resumo?")
    print("[1] Markdown (.md, para Obsidian)")
    print("[2] Texto Simples (.txt)")
    escolha = input("Escolha: ").strip()

    if escolha == "1":
        formato_texto = "Markdown para Obsidian, com sintaxe adequada."
        extensao = ".md"
    elif escolha == "2":
        formato_texto = "texto simples, sem qualquer sintaxe Markdown."
        extensao = ".txt"
    else:
        print("Opção inválida.")
        return

    prompt_base = ler_prompt_base()
    if prompt_base is None: return

    prompt = prompt_base.replace("{tema}", tema).replace("{formato}", formato_texto)
    mensagens = [{"role": "system", "content": prompt}]

    while True:
        print("\nConsultando GPT...\n")
        resposta = client.chat.completions.create(
            model="gpt-4.1-mini-2025-04-14",
            messages=mensagens,
            temperature=0.3,
            max_tokens=2000
        )
        resumo = resposta.choices[0].message.content

        print("\n=== RESUMO GERADO ===\n")
        print(resumo)
        print("\nO que deseja fazer?")
        print("[1] Guardar este resumo")
        print("[2] Fazer nova pergunta ao GPT")
        print("[0] Voltar ao menu")
        op = input("Escolha: ").strip()

        if op == "1":
            if not os.path.exists("resumos"):
                os.makedirs("resumos")
            caminho_saida = os.path.join("resumos", tema.replace(" ", "_") + extensao)
            with open(caminho_saida, "w", encoding="utf-8") as f:
                f.write(resumo)
            print(f"Resumo guardado em: {caminho_saida}")
            break
        elif op == "2":
            nova = input("Digite sua pergunta/comentário: ").strip()
            if nova:
                mensagens.append({"role": "user", "content": nova})
            else:
                print("Entrada vazia — voltando ao menu.")
        elif op == "0":
            break
        else:
            print("Opção inválida.")

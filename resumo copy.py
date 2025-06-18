import openai
import os

def ler_prompt_base():
    try:
        with open("promptResumo.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("Arquivo promptResumo.txt não encontrado!")
        return None

def gerar_resumo():
    openai.api_key = obter_api_key()
    
    tema = input("Tema do resumo: ").strip()
    if not tema:
        print("Tema não pode ser vazio.")
        return

    # Pergunta o formato do resumo antes de gerar
    print("\nEm que formato deseja o resumo?")
    print("[1] Markdown (.md, para Obsidian)")
    print("[2] Texto Simples (.txt)")
    formato_escolhido = input("Escolha: ").strip()

    if formato_escolhido == "1":
        formato_output = "Markdown para Obsidian, com sintaxe adequada."
        extensao = ".md"
    elif formato_escolhido == "2":
        formato_output = "texto simples, para ficheiro de texto."
        extensao = ".txt"
    else:
        print("Opção inválida. Saindo.")
        return

    # Lê o prompt base do ficheiro e faz substituição de variáveis
    prompt_base = ler_prompt_base()
    if prompt_base is None:
        return

    prompt_usuario = (
        prompt_base
        .replace("{tema}", tema)
        .replace("{formato}", formato_output)
    )

    # Inicia histórico de mensagens para manter contexto se necessário
    mensagens = [
        {"role": "system", "content": prompt_usuario}
    ]

    while True:
        print("\nConsultando ChatGPT, aguarde...\n")
        resposta = openai.ChatCompletion.create(
            model="gpt-4.1-mini-2025-04-14",  # Confirme o nome do modelo na sua conta OpenAI
            messages=mensagens,
            temperature=0.4,
            max_tokens=2000,
        )
        resumo = resposta['choices'][0]['message']['content']

        print("\n=== RESUMO GERADO ===\n")
        print(resumo)
        print("\nO que deseja fazer?")
        print("[1] Guardar este resumo")
        print("[2] Perguntar/comentar ao ChatGPT sobre este tema")
        print("[0] Voltar ao menu principal")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            if not os.path.exists("resumos"):
                os.makedirs("resumos")
            nome_arquivo = f"resumos/{tema.replace(' ', '_')}{extensao}"
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.write(resumo)
            print(f"Resumo guardado em: {nome_arquivo}")
            break
        elif opcao == "2":
            user_input = input("Digite a sua pergunta ou comentário adicional: ").strip()
            if user_input:
                mensagens.append({"role": "user", "content": user_input})
            else:
                print("Nada digitado. Retornando ao menu de opções.")
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

def obter_api_key():
    caminho_key = "chatgptKey.txt"
    api_key = None
    if os.path.exists(caminho_key):
        with open(caminho_key, "r", encoding="utf-8") as f:
            api_key = f.read().strip()
    if not api_key:
        api_key = input("Cole a sua OpenAI API Key: ").strip()
    return api_key

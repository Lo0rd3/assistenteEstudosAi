

while True:
    print("\n==== Assistente de Estudos ====")
    print("[1] Gerar resumo (.md para Obsidian)")
    print("[2] Gerar flashcards (.csv para Anki/Quizlet)")
    print("[3] Fazer quiz interativo")
    print("[0] Sair")
    escolha = input("Escolha uma opção: ").strip()

    if escolha == "1":
        gerar_resumo()
    elif escolha == "2":
        gerar_flashcards()
    elif escolha == "3":
        quiz_interativo()
    elif escolha == "0":
        print("Até logo!")
        break
    else:
        print("Opção inválida. Tente novamente.")

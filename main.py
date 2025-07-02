from utils import getApiKey
from resumo import generateSumary
from quiz import interactiveQuiz

api_key = getApiKey()
try:
    while True:
        print("\n==== Assistente de Estudos ====")
        print("[1] Gerar resumo")
        print("[2] Fazer quiz interativo")
        print("[3] Gerar flashcards")
        print("[0] Sair")
        choice = input("Escolha uma opção: ").strip()

        if choice == "1":
            generateSumary()
        elif choice == "2":
          interactiveQuiz()
#       elif choice == "3":
#            generateflashcards()
        elif choice == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")
except KeyboardInterrupt:
    print("\nPrograma encerrado pelo user.")


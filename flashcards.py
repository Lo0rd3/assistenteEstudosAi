import os
import csv
import google.generativeai as genai
from utils import getApiKey
from datetime import datetime
import random

def genFlashcards():
    genai.configure(api_key=getApiKey())
    model = genai.GenerativeModel('gemini-2.5-flash')


    # Pergunta o tema
    while True:
        Theme = input("Tema dos flashcards: ").strip()
        if Theme and len(Theme) >= 3:
            break
        print("O tema deve ter pelo menos 3 caracteres.")

    # Pergunta quantos flashcards
    while True:
        Num = input("Quantos flashcards quer gerar? ").strip()
        if Num.isdigit() and int(Num) > 0:
            NumCards = int(Num)
            break
        print("Por favor, insira um número válido.")

    # Gera os flashcards
    genPrompt = (
            "Você é um especialista em educação e técnicas de estudo, altamente capacitado em criar flashcards perfeitos que facilitam a memorização ativa e a recuperação eficiente da informação. "
            "Seu objetivo é elaborar flashcards claros, diretos, e altamente eficazes, que sigam rigorosamente estas instruções:\n\n"
            f"Tema: {Theme}\n"
            f"Quantidade: {NumCards}\n\n"
            "Melhores Práticas para os Flashcards:\n"
            "1. Clareza e objetividade: Cada flashcard deve conter apenas uma ideia ou conceito central claramente formulado.\n"
            "2. Perguntas diretas: As perguntas devem estimular ativamente o raciocínio ou a recuperação ativa do conhecimento.\n"
            "3. Respostas concisas: As respostas devem ser diretas, precisas, curtas e fáceis de memorizar.\n"
            "4. Variedade e Relevância: Distribua diferentes níveis de dificuldade e aborde aspectos essenciais, importantes e interessantes sobre o tema.\n"
            "5. Exemplos práticos: Sempre que possível, inclua exemplos, casos práticos, ou informações complementares curtas que facilitem a compreensão.\n"
            "6. Facilidade de memorização: Use técnicas como associação, analogias ou mnemônicos breves nas respostas para auxiliar a retenção sempre que aplicável.\n\n"
            "Gere APENAS flashcards no seguinte formato:\n\n"
            "Pergunta: <pergunta>\n"
            "Resposta: <resposta>\n\n"
            "Observações importantes:\n"
            "- Não adicione nenhum texto introdutório ou explicações adicionais além dos flashcards.\n"
            "- Não repita ideias semelhantes entre os flashcards; cada um deve ser único e independente.\n"
            "- Os flashcards devem estar perfeitamente adaptados para estudo eficaz e otimizado.\n\n"
            "Agora, crie os flashcards solicitados!"
            )
    print("\nA gerar flashcards... aguarde!\n")
    response = model.generate_content(genPrompt)
    FlashText = response.text


    # Parsing para pares pergunta-resposta
    Flashcards = []
    bloc = [l.strip() for l in FlashText.splitlines() if l.strip()]
    q = None
    for line in bloc:
        if line.lower().startswith("pergunta:"):
            q = line.split(":", 1)[1].strip()
        elif line.lower().startswith("resposta:") and q:
            a = line.split(":", 1)[1].strip()
            Flashcards.append((q, a))
            q = None

    if not Flashcards:
        print("Não foi possível gerar flashcards válidos.")
        return

    print(f"\nGerados {len(Flashcards)} flashcards:")
    for idx, (q, a) in enumerate(Flashcards, start=1):
        print(f"{idx}. P: {q}\n   R: {a}")

    # Pergunta se quer guardar
    SaveChoice = ""
    while SaveChoice not in ("1", "2"):
        print("\nDeseja guardar estes flashcards?")
        print("[1] Sim")
        print("[2] Não")
        SaveChoice = input("Escolha: ").strip()
        if SaveChoice not in ("1", "2"):
            print("Opção inválida! Tente novamente.")
    if SaveChoice == "2":
        print("Flashcards não guardados.")
        return 

    # Salvar em CSV 
    if not os.path.exists("flashcards"):
        os.makedirs("flashcards")
    now = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"flashcards/{Theme.replace(' ', '_')}_flashcards_{now}.csv"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Pergunta;Resposta\n")
        for q, a in Flashcards:
            f.write(f"{q};{a}\n")
    print(f"Flashcards guardados em: {filename}")
    print("\nPara importar no Anki, Quizlet ou RemNote, escolha importar CSV, separador ponto e vírgula.")
    return 













def interactFlashcards():
    
    # Listar ficheiros disponíveis
    if not os.path.exists("flashcards"):
        os.makedirs("flashcards")

    files = [f for f in os.listdir("flashcards") if f.endswith(".csv")]
        
    if not files:
        while True:
            print("Nenhum ficheiro de flashcards (.csv) encontrado.")
            createChoice = input("Pretende criar novos flashcards?\nEscolha [s/n]: ").strip().lower()
            
            if createChoice == "s":
                genFlashcards()
                praticar = input("Deseja praticar os flashcards criados? [s/n]: ").strip().lower()
                if praticar == "s":
                    return interactFlashcards()
                else:
                    print("A voltar ao menu principal.")
                    return
            elif createChoice == "n":
                print("A voltar ao menu principal.")
                return
            else:
                print("Opção invalida. Tente Novamente.")
                   

    print("\nFicheiros de flashcards disponíveis:")
    for idx, name in enumerate(files, start=1):
        print(f"[{idx}] {name}")
    
    print("[Q] Voltar ao menu principal")
    
    while True:
        choice = input("\nEscolhe o número do ficheiro para praticar: ").strip().lower()
        if choice== "q":
            print("\nA voltar ao menu principal.")
            return
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            fileToRun = files[int(choice)-1]
            break
        print("Opção inválida. Tenta novamente.")
    
    


    
    path = os.path.join("flashcards", fileToRun)
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)  # Salta o cabeçalho
            cards = list(reader)

    except Exception as e:
        print(f"\nErro ao ler o ficheiro: {e}")
        return
    
    if not cards:
        print("\nO ficheiro selecionado está vazio.")
        return

    random.shuffle(cards)  # Baralhar os cartões

    while True:
        print("\nPretende contar as respostas corretas durante a prática?")
        print("[1] Sim")
        print("[2] Não")
        countChoice = input("Escolha: ").strip()
        if countChoice == "1":
            countCorrect = True
            break
        elif countChoice == "2":
            countCorrect = False
            break
        else:
            print("Opção inválida. Tente novamente.")




    print(f"\nA praticar flashcards de: {fileToRun}\n")
    correct = 0
    answered= 0
    for idx, (question, answer) in enumerate(cards, start=1):
        print("=" * 40)
        print(f"Cartão {idx}: {question}")

        userInput = input("Carregue ENTER para ver a resposta\n(Q para sair)").strip().lower()
        if userInput == 'q':
            print("A sair da prática de flashcards.")
            break
        answered += 1 
        print(f"Resposta: {answer}")
              
        if countCorrect:
            while True:
                gotIt = input("Resposta correta? (s/n): ").strip().lower()
                if gotIt in ("s", "n"):
                    if gotIt == "s":
                        correct += 1
                    break
                print("Entrada inválida. Responde com 's' ou 'n'.")
        input("Pressiona ENTER para continuar para o proximo flashcard.'Q'-sair")




    print("=" * 40)
    print(f"\nCartões praticados: {answered}/{len(cards)}")
    if countCorrect and answered > 0:
        print(f"Respostas corretas: {correct}/{answered}")
        percentage = (correct / answered) * 100
        print(f"Taxa de acerto: {percentage:.1f}%")
    
        if correct == answered:
            print("\nExcelente! Acertaste todos os cartões!")
        elif percentage >= 70:
            print("\nBom trabalho! Estás no bom caminho.")
        elif percentage >= 50:
            print("\nContinuas a aprender! Revê os cartões que falhaste.")
        else:
            print("\nNão desanimes! Praticar é a chave para aprender.")

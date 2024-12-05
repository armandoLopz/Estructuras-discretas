import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trivias dinamicas")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

font = pygame.font.Font(None, 32)
large_font = pygame.font.Font(None, 48)

questions = [
    {
        "question": "¿Cuántas permutaciones hay de 5 elementos distintos?",
        "answer": "120",
        "explanation": "Se calcula como 5! (5 factorial) = 5 x 4 x 3 x 2 x 1 = 120"
    },
    {
        "question": "En una carrera con 8 corredores, ¿de cuántas formas se pueden asignar el oro, plata y bronce?",
        "answer": "336",
        "explanation": "Se calcula como P(8,3) = 8 x 7 x 6 = 336"
    },
    {
        "question": "¿Cuántos números de 4 dígitos se pueden formar con los dígitos 1, 2, 3, 4, 5 sin repetición?",
        "answer": "120",
        "explanation": "Es una permutación de 5 elementos tomados de 4 en 4: P(5,4) = 5 x 4 x 3 x 2 = 120"
    },
    {
        "question": "¿Cuántas formas hay de seleccionar 3 libros de una estantería con 10 libros?",
        "answer": "120",
        "explanation": "Es una combinación de 10 elementos tomados de 3 en 3: C(10,3) = 10! / (3! * 7!) = 120"
    },
    {
        "question": "¿Cuántas palabras de 3 letras (con o sin sentido) se pueden formar con las letras de 'PYTHON'?",
        "answer": "216",
        "explanation": "Hay 6 opciones para la primera letra, 6 para la segunda y 6 para la tercera: 6 x 6 x 6 = 216"
    }
]

def draw_button(text, x, y, width, height, active_color, inactive_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x + width/2, y + height/2))
    screen.blit(text_surf, text_rect)
    return False

def draw_text_box(text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_lines = []
    words = text.split()
    current_line = words[0]
    for word in words[1:]:
        test_line = current_line + " " + word
        if font.size(test_line)[0] <= width - 20:
            current_line = test_line
        else:
            text_lines.append(current_line)
            current_line = word
    text_lines.append(current_line)
    
    start_y = y + 10
    for line in text_lines:
        text_surf = font.render(line, True, BLACK)
        text_rect = text_surf.get_rect(x=x+10, y=start_y)
        screen.blit(text_surf, text_rect)
        start_y += font.get_linesize()

def main_menu():
    while True:
        screen.fill(WHITE)
        title = large_font.render("Trivias dinamicas", True, BLACK)
        screen.blit(title, (WIDTH/2 - title.get_width()/2, 100))

        if draw_button("Jugar", WIDTH/2 - 100, 250, 200, 50, GRAY, WHITE):
            return "play"
        if draw_button("Instrucciones", WIDTH/2 - 100, 320, 200, 50, GRAY, WHITE):
            return "instructions"
        if draw_button("Salir", WIDTH/2 - 100, 390, 200, 50, GRAY, WHITE):
            return "quit"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        pygame.display.flip()

def show_instructions():
    while True:
        screen.fill(WHITE)
        title = large_font.render("Instrucciones", True, BLACK)
        screen.blit(title, (WIDTH/2 - title.get_width()/2, 50))

        instructions = [
            "1. Lee cuidadosamente cada pregunta.",
            "2. Escribe tu respuesta y presiona Enter.",
            "3. Gana puntos por responder correctamente.",
            "4. Aprende de las explicaciones proporcionadas.",
            "5. ¡Diviértete y mejora tus conocimientos!"
        ]

        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, BLACK)
            screen.blit(text, (50, 150 + i * 50))

        if draw_button("Volver", WIDTH/2 - 100, 500, 200, 50, GRAY, WHITE):
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

def game():
    score = 0
    question_index = 0
    user_answer = ""
    message = ""
    show_explanation = False
    
    while question_index < len(questions):
        current_question = questions[question_index]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not show_explanation:
                        if user_answer == current_question["answer"]:
                            score += 1
                            message = "¡Correcto!"
                        else:
                            message = f"Incorrecto. La respuesta correcta era {current_question['answer']}"
                        show_explanation = True
                    else:
                        question_index += 1
                        user_answer = ""
                        message = ""
                        show_explanation = False
                elif event.key == pygame.K_BACKSPACE:
                    user_answer = user_answer[:-1]
                else:
                    user_answer += event.unicode

        screen.fill(WHITE)

        draw_text_box(current_question["question"], 20, 50, WIDTH - 40, 100, GRAY)

        answer_text = font.render(f"Tu respuesta: {user_answer}", True, BLACK)
        screen.blit(answer_text, (20, 160))

        score_text = font.render(f"Puntaje: {score}/{question_index}", True, BLACK)
        screen.blit(score_text, (WIDTH - 150, 10))

        message_color = GREEN if message == "¡Correcto!" else RED
        message_text = font.render(message, True, message_color)
        screen.blit(message_text, (WIDTH/2 - message_text.get_width()/2, 200))

        if show_explanation:
            draw_text_box(f"Explicación: {current_question['explanation']}", 20, 240, WIDTH - 40, 200, GRAY)

            next_text = font.render("Presiona Enter para la siguiente pregunta", True, BLACK)
            screen.blit(next_text, (WIDTH/2 - next_text.get_width()/2, HEIGHT - 50))

        pygame.display.flip()

    screen.fill(WHITE)
    final_score_text = large_font.render(f"Puntaje Final: {score}/{len(questions)}", True, BLACK)
    screen.blit(final_score_text, (WIDTH/2 - final_score_text.get_width()/2, HEIGHT/2 - 50))
    
    if draw_button("Volver al Menú", WIDTH/2 - 100, HEIGHT/2 + 50, 200, 50, GRAY, WHITE):
        return

    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def main():
    while True:
        choice = main_menu()
        if choice == "play":
            game()
        elif choice == "instructions":
            show_instructions()
        elif choice == "quit":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()

print("Quiz game code executed successfully. Run this script with Pygame installed to play the game.")
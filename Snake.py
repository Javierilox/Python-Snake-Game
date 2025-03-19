import sys
import pygame
import random
import tkinter as tk
from tkinter import messagebox as mBox

imagen_inicio = pygame.image.load("Images/Snake.jpg")
imagen_pausa = pygame.image.load("Images/Snake_Pausa.jpg")

HEIGHT = 700
WIDTH = 700
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
GRIND_SIZE = 20


# clase de la serpiente
class Snake:
    def __init__(self):
        self.velocity = 20
        self.length = 0  # Cambia la longitud inicial a 0
        self.snake_body = [[220, 200]]
        self.actual_movement = random.choice(["right", "left", "up", "down"])
        self.incorrect_movements = {"right": "left", "left": "right", "up": "down", "down": "up"}
        self.best_score = 0

    # Movimientos de la serpiente
    def move_snake(self, window):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                new_direction = None
                if event.key == pygame.K_UP:
                    new_direction = "up"
                elif event.key == pygame.K_DOWN:
                    new_direction = "down"
                elif event.key == pygame.K_LEFT:
                    new_direction = "left"
                elif event.key == pygame.K_RIGHT:
                    new_direction = "right"

                if new_direction and new_direction != self.incorrect_movements[self.actual_movement]:
                    self.actual_movement = new_direction

                if event.key == pygame.K_p:
                    menu_pausa(window)

        self.snake_movements(window)

    # chequear los movimientos de la serpiente
    def snake_movements(self, window):
        head_x, head_y = self.snake_body[0]
        if self.actual_movement == "right":
            head_x += self.velocity
        elif self.actual_movement == "left":
            head_x -= self.velocity
        elif self.actual_movement == "up":
            head_y -= self.velocity
        elif self.actual_movement == "down":
            head_y += self.velocity

        head_x, head_y = self.chequear_bounds(head_x, head_y)
        self.snake_body.insert(0, [head_x, head_y])
        self.draw_snake(window)
        if len(self.snake_body) > self.length:
            self.snake_body.pop()
        self.revisar_choque()

    # chequear los limites de la serpiente
    def chequear_bounds(self, x, y):
        return (x % WIDTH, y % HEIGHT)

    # dibujar la serpiente
    def draw_snake(self, window):
        for idx, segment in enumerate(self.snake_body):
            color = YELLOW if idx == 0 else BLUE
            pygame.draw.rect(window, color, (segment[0], segment[1], 20, 20))

    # cabeza de la serpiente
    def cabeza_serpiente(self):
        return self.snake_body[0]

    # revisar si la serpiente choca
    def revisar_choque(self):
        if self.cabeza_serpiente() in self.snake_body[1:]:
            self.reset()

    # resetear la serpiente
    def reset(self):
        mensaje(self.length)  # Se muestra la puntuación real
        self.snake_body = [[220, 200]]
        self.actual_movement = random.choice(["right", "left", "up", "down"])
        self.best_score = max(self.best_score, self.length)  # No restamos 1
        self.length = 0  # Reiniciamos a 0 en vez de 1


# mensaje de game over
def mensaje(puntuacion):
    root = tk.Tk()
    root.withdraw()
    mBox.showinfo("Perdiste , Game Over", f"Tu puntuación fue: {puntuacion}")
    try:
        root.destroy()
    except:
        pass


# clase de la comida de la serpiente
class Food:
    def __init__(self):
        self.food_position = (0, 0)
        self.posicion_random()

    # posicion random de la comida
    def posicion_random(self):
        self.food_position = [random.randrange(0, WIDTH, 20), random.randrange(0, HEIGHT, 20)]

    # dibujar la comida
    def dibujar_comida(self, window):
        pygame.draw.rect(window, RED, (*self.food_position, 20, 20))


# chequear la comida aparezca de forma random y actualice marcador
def chequear_comida(snake, food, bloque):
    if tuple(snake.cabeza_serpiente()) == tuple(food.food_position):
        food.posicion_random()  # Reubica la comida
        snake.length += 1  # Aumenta correctamente
        snake.best_score = max(snake.best_score, snake.length)  # Actualiza el mejor puntaje
        bloque.bloque_random()


# clase donde crearemos los obstaculos
class Bloque:
    def __init__(self):
        self.bloque_position = []
        self.bloque_random()

    # posicion random de los bloques
    def bloque_random(self):
        # Genera 8 obstáculos en posiciones aleatorias
        self.bloque_position = [(random.randrange(0, 680, 20), random.randrange(0, 680, 20)) for i in range(8)]

    # dibujar los bloques
    def dibujar_bloque(self, window):
        for i, value in enumerate(self.bloque_position):
            pygame.draw.rect(window, BLACK, [value[0], value[1], 20, 20])


def check_block(snake, bloque):
    if tuple(snake.cabeza_serpiente()) in bloque.bloque_position:
        bloque.bloque_random()  # Reubica los bloques cuando la serpiente choca
        snake.reset()  # Reinicia la serpiente


# dibujar la cuadricula
def drawGrid(window):
    window.fill(GREEN)
    for x in range(0, WIDTH, GRIND_SIZE):
        pygame.draw.line(window, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRIND_SIZE):
        pygame.draw.line(window, BLACK, (0, y), (WIDTH, y))


# menu de inicio
def menu_inicio(start, window):
    window.blit(imagen_inicio, (0, 0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key:
                return False
    return True


# menu de pausa
def menu_pausa(window):
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    paused = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        window.blit(imagen_pausa, (0, 0))
        pygame.display.update()


# funcion principal
def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Juego de la Culebrita")
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    font = pygame.font.SysFont("avenir", 28)
    obstaculos = Bloque()
    start = True
    while True:
        clock.tick(12)
        drawGrid(window)
        snake.move_snake(window)
        chequear_comida(snake, food, obstaculos)  # Ahora se pasa el bloque aquí
        check_block(snake, obstaculos)

        score_text = font.render(f"Puntuación: {snake.length}", True, BLACK)  # No restamos 1
        best_score_text = font.render(f"Mejor Puntuación: {snake.best_score}", True, BLACK)
        window.blit(score_text, (5, 10))
        window.blit(best_score_text, (5, 30))
        food.dibujar_comida(window)
        obstaculos.dibujar_bloque(window)

        # Si la variable start = True, Mostraremos la imagen de inicio
        while start:
            start = menu_inicio(start, window)
        # si la comida aparece en un bloque, la comida se mueve a otra posicion
        while True:
            if food.food_position in obstaculos.bloque_position:
                food.posicion_random()  # Mueve la comida si está en un bloque
            break
        pygame.display.update()


# ejecutar el juego
if __name__ == "__main__":
    main()

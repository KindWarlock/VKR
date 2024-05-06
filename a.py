import pygame
import sys

pygame.init()

width, height = 400, 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


def create_alpha_gradient(width, height):
    gradient_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(height):
        alpha = int((y / height) * 255)  # Alpha value ranges from 0 to 255
        pygame.draw.line(gradient_surface, (255, 255,
                         255, alpha), (0, y), (width, y))
    return gradient_surface


def render_text_with_gradient(text, font, gradient_surface):
    # Render text without alpha
    text_surface = font.render(text, True, (255, 255, 255))
    gradient_surface = pygame.transform.scale(
        gradient_surface, text_surface.get_size())
    text_surface.blit(gradient_surface, (0, 0),
                      special_flags=pygame.BLEND_RGBA_MULT)  # Apply gradient
    return text_surface


gradient = create_alpha_gradient(width, height)
font = pygame.font.Font(None, 36)
text = "Alpha Gradient Text"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((80, 100, 25))
    text_surface = render_text_with_gradient(text, font, gradient)
    screen.blit(text_surface, (50, 50))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

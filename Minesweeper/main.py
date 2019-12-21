import minesweeper
import pygame

pygame.init()


def render():

    screen.fill((220, 220, 220))

    for r in range(num_rows):
        for c in range(num_cols):

            cell = field.get_at_pos(r, c)

            if cell != 0:
                if cell != -1:
                    cell_surf = num_surfs[cell-1]
                else:
                    cell_surf = mine_surf

                screen.blit(
                    cell_surf,
                    (int((c+0.5)*cell_size-cell_surf.get_width()/2),
                     int((r+0.5)*cell_size-cell_surf.get_height()/2))
                )

            if (r, c) not in unconvered_cells or (win and cell == -1):
                pygame.draw.rect(screen, (240, 240, 240), (c*cell_size, r*cell_size, cell_size, cell_size))

            if (r, c) in flagged_cells:
                screen.blit(flag_surf, (int((c+0.5)*cell_size-flag_surf.get_width()/2),int((r+0.5)*cell_size-flag_surf.get_height()/2)))

    for r in range(num_rows):
        pygame.draw.line(screen, (200, 200, 200), (0, r*cell_size), (num_cols*cell_size, r*cell_size))

    for c in range(num_cols):
        pygame.draw.line(screen, (200, 200, 200), (c*cell_size, 0), (c*cell_size, num_rows*cell_size))

    pygame.display.flip()


def uncover(r, c):
    global unconvered_cells, alive

    newly_visible = field.uncover_from(r, c)

    if newly_visible == -1:
        unconvered_cells.extend(field.get_mines())
        alive = False
        print("You lose!")

    else:
        newly_visible = list(set(newly_visible).difference(flagged_cells))
        unconvered_cells.extend(newly_visible)


num_rows = 12
num_cols = 20
num_mines = 33
cell_size = 25
font_size = 25


field = minesweeper.MineField((num_rows, num_cols))
#field.place_mines(num_mines)
#field.place_hints()

unconvered_cells = []
flagged_cells = []
initialized = False


# Graphics
screen = pygame.display.set_mode((num_cols*cell_size, num_rows*cell_size))

theme_font = pygame.font.Font(None, font_size)
num_surfs = [theme_font.render(str(i), True, (0, 0, 0)) for i in range(1, 9)]
mine_surf = pygame.image.load("src/images/mine.png").convert_alpha()
mine_surf = pygame.transform.smoothscale(mine_surf, (cell_size-4, cell_size-4))
flag_surf = pygame.image.load("src/images/flag.png").convert_alpha()
flag_surf = pygame.transform.smoothscale(flag_surf, (cell_size-4, cell_size-4))


running = True
alive = True
win = False


while running:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        elif e.type == pygame.MOUSEBUTTONDOWN and alive:

            x, y = pygame.mouse.get_pos()
            r = y // cell_size
            c = x // cell_size

            if e.button == 1:

                if (r, c) not in unconvered_cells and (r, c) not in flagged_cells:

                    if not initialized:
                        field.place_mines(num_mines, restrictions=[[r, c]])
                        field.place_hints()

                        initialized = True

                    uncover(r, c)

            elif e.button == 2:

                if (r, c) in unconvered_cells:

                    nearby = [
                        (r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
                        (r, c - 1), (r, c + 1),
                        (r + 1, c - 1), (r + 1, c), (r + 1, c + 1),
                    ]

                    for cell in nearby:
                        if cell not in flagged_cells and cell not in unconvered_cells and field.in_bounds(*cell):

                            uncover(*cell)


            elif e.button == 3:

                if (r, c) not in unconvered_cells:

                    if (r, c) not in flagged_cells:
                        flagged_cells.append((r, c))
                    else:
                        flagged_cells.remove((r, c))

    if alive and len(set(unconvered_cells)) + num_mines == num_rows * num_cols:
        win = True
        alive = False

        print("You win!")

    render()

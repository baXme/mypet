import pygame as pg

# Инициализация pg
pg.init()

# Размеры окна
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
icon_size = 80
pad = 5
font = pg.font.Font(None, 40)
mini_font = pg.font.Font(None, 15)


def load1(file, width, hidth):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image, (width, hidth))
    return image


def text_render(text):
    return font.render(str(text), True, "black")


def text_render1(text):
    return mini_font.render(str(text), True, "black")


class Button:
    def __init__(self, text, x, y, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text_font=font, func=None):
        self.func = func
        self.idle_image = load1("images/button.png", width, height)
        self.pressed_image = load1("images/button_clicked.png", width, height)
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.is_pressed = False
        self.text_font = text_font
        self.text = font.render(str(text), True, "Black")
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.is_pressed:
                self.image = self.pressed_image
            else:
                self.image = self.idle_image

    def is_clck(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                self.func()
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.is_pressed = False


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Виртуальный питомец")
        self.background = load1("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.happines_image = load1("images/happiness.png", icon_size, icon_size)
        self.dog_image = load1("images/dog.png", 310, 500)
        self.satiety_image = load1("images/satiety.png", icon_size, icon_size)
        self.health_image = load1("images/health.png", icon_size, icon_size)
        self.money_image = load1("images/money.png", icon_size, icon_size)
        self.happines = 100
        self.satiety = 100
        self.health = 100
        self.money = 10
        self.coins_per_second = 1
        self.costs_of_upgrade = {100: False, 1000: False, 5000: False, 10000: False}
        self.button_x = SCREEN_WIDTH - pad - BUTTON_WIDTH
        self.eat = Button("Поесть", self.button_x, 100, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, func=self.food_menu_on)
        self.clouth = Button("Одежда", self.button_x, 175, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, func=self.clouth_menu_on)
        self.play = Button("Игры", self.button_x, 250, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, func=self.game_menu_on)
        self.upgrade_button = Button("Улучшить", self.button_x + 130, 3,
                                     width=BUTTON_WIDTH // 3, height=BUTTON_HEIGHT // 3,
                                     text_font=mini_font,
                                     func=self.increase_money)

        self.INCREASE_COINS = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREASE_COINS, 1000)
        self.run()
    def food_menu_on(self):
        self.mode = "Food menu"
    def game_menu_on(self):
        self.mode = "Game menu"
    def clouth_menu_on(self):
        self.mode = "Clouth menu"
    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == self.INCREASE_COINS:
                self.money += self.coins_per_second
            self.eat.is_clck(event)
            self.clouth.is_clck(event)
            self.play.is_clck(event)
            self.upgrade_button.is_clck(event)
            if event.type == pg.MOUSEBUTTONDOWN:
                self.money += 1

    def increase_money(self):
        for key, value in self.costs_of_upgrade.items():
            if self.costs_of_upgrade[key] == False and self.costs_of_upgrade[key] == self.money:
                self.costs_of_upgrade[key] = True
                self.coins_per_second += 1
                self.money -= self.costs_of_upgrade[key]

    def update(self):
        self.eat.update()
        self.clouth.update()
        self.play.update()
        self.upgrade_button.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.happines_image, (pad, pad))
        self.screen.blit(self.dog_image, (275, 100))
        self.screen.blit(self.health_image, (pad, 70))
        self.screen.blit(self.satiety_image, (pad, 140))
        self.screen.blit(self.money_image, (SCREEN_WIDTH - icon_size - pad * 9, pad))
        self.screen.blit(text_render(self.happines), (pad + icon_size, pad * 6))
        self.screen.blit(text_render(self.health), (pad + icon_size, 95))
        self.screen.blit(text_render(self.satiety), (pad + icon_size, 165))
        self.screen.blit(text_render(self.money), (SCREEN_WIDTH - icon_size + 35, pad * 6))

        self.eat.draw(self.screen)
        self.clouth.draw(self.screen)
        self.play.draw(self.screen)
        self.upgrade_button.draw(self.screen)
        self.screen.blit(text_render("Поесть"), (self.button_x + 55, 120))
        self.screen.blit(text_render("Одежда"), (self.button_x + 44, 195))
        self.screen.blit(text_render("Игры"), (self.button_x + 65, 270))
        self.screen.blit(text_render1("улучшить"), (self.button_x + 140, 7))
        pg.display.flip()


if __name__ == "__main__":
    Game()
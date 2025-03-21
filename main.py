import pygame as pg

# Инициализация pg
pg.init()
print("21312312312312")
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
class Item:
    def __init__(self, name, price, file):
        self.price = price
        self.name = name
        self.is_bought = False
        self.is_using = False
        self.image = load1(file, 310 // 1.7, 500 // 1.7)
        self.full_image = load1(file, 310, 500)
class Cmenu:
    def __init__(self, game):
        self.game = game
        self.menu = load1("images/menu/menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.botton_label_off = load1("images/menu/bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.botton_label_on = load1("images/menu/bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load1("images/menu/top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load1("images/menu/top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items =[Item("Cиния футболка", 10, "images/items/blue t-shirt.png"),
                     Item("Ботинки", 50, "images/items/boots.png")


        ]
        self.current_item = 0
        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.next_button = Button("Вперёд", SCREEN_WIDTH - 90 - SCREEN_WIDTH, SCREEN_HEIGHT - 130,
                                  width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2),
                                  func=self.to_next)

        def draw(self, screen):
            screen.blit(self.menu_page, (0, 0))
            screen.blit(self.items[self.current_item].image, self.item_rect)
            if self.items[self.current_item].is_bought:
                screen.blit(self.botton_label_on, (0, 0))
            else:
                screen.blit(self.botton_label_off, (0, 0))
            if self.items[self.current_item].is_using:
                screen.blit(self.top_label_on, (0, 0))
            else:
                screen.blit(self.top_label_off, (0, 0))

        def to_next(self):
            if self.current_item != len(self.items) - 1:
                self.current_item += 1

        def update(self):
            self.next_button.update()

        def is_clcked(self, event):
            self.next_button.is_clcked(event)


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
        self.mode = "Main"
        self.coins_per_second = 1

        self.costs_of_upgrade = {100: False, 1000: False, 5000: False, 10000: False}
        self.button_x = SCREEN_WIDTH - pad - BUTTON_WIDTH
        self.eat = Button("Поесть", self.button_x, 100, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                          func=self.food_menu_on)
        self.clouth = Button("Одежда", self.button_x, 175, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                             func=self.clouth_menu_on)
        self.play = Button("Игры", self.button_x, 250, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                           func=self.game_menu_on)
        self.upgrade_button = Button("Улучшить", self.button_x + 130, 3,
                                     width=BUTTON_WIDTH // 3, height=BUTTON_HEIGHT // 3,
                                     text_font=mini_font,
                                     func=self.increase_money)
        self.buttons = [self.upgrade_button, self.play, self.clouth, self.eat]
        self.clouthes_menu = Cmenu(self)
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
            if event.type == pg.KEYDOWN:
                if event.type == self.INCREASE_COINS:
                    self.money += self.coins_per_second
            self.eat.is_clck(event)
            self.clouth.is_clck(event)
            self.play.is_clck(event)
            self.upgrade_button.is_clck(event)
            if event.type == pg.MOUSEBUTTONDOWN:
                self.money += 1
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.mode = "Main"
            for button in self.buttons:
                button.is_clck(event)
    def increase_money(self):
        for cost, check in self.costs_of_upgrade.items():
            if check == False and cost <= self.money:
                self.costs_of_upgrade[cost] = True
                self.coins_per_second += 1
                self.money -= cost

    def update(self):
        self.eat.update()
        self.clouth.update()
        self.play.update()
        self.upgrade_button.update()
        self.clouthes_menu.update()
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
        if self.mode == "Clouth menu":
            self.clouthes_menu.draw(self.screen)

if __name__ == "__main__":
    Game()
import json
import random

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
font_maxi = pg.font.Font(None, 200)
fps = 600


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
        self.text = self.text_font.render(str(text), True, "Black")
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

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
    def __init__(self, name, price, file, is_bought, is_using ):
        self.price = price
        self.name = name
        self.file = file
        self.is_bought = is_bought
        self.is_using = is_using
        self.image = load1(file, 310 // 1.7, 500 // 1.7)
        self.full_image = load1(file, 310, 500)
class Cmenu:
    def __init__(self, game, data):
        self.game = game
        self.menu = load1("images/menu/menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.botton_label_off = load1("images/menu/bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.botton_label_on = load1("images/menu/bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load1("images/menu/top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load1("images/menu/top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items =[]
        for item in data:
            self.items.append(Item(*item.values()))

        self.current_item = 0
        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.next_button = Button("Вперёд", 125, 425,
                                  width=int(BUTTON_WIDTH // 2), height=int(BUTTON_HEIGHT // 2),
                                  func=self.to_next)
        self.end_button = Button("назад", 675, 425,
                                  width=int(BUTTON_WIDTH // 2), height=int(BUTTON_HEIGHT // 2),
                                  func=self.to_end)
        self.use_button = Button("Надеть", 125, 350,
                                  width=int(BUTTON_WIDTH // 2), height=int(BUTTON_HEIGHT // 2),
                                  func=self.use)
        self.buy_button = Button("купить", 400, 375,
                                  width=int(BUTTON_WIDTH // 2), height=int(BUTTON_HEIGHT // 2),
                                  func=self.buy)
        self.bought = text_render("Куплено")
        self.used = text_render("Надето")
    def draw(self, screen):
        screen.blit(self.menu, (0, 0))
        screen.blit(self.items[self.current_item].image, self.item_rect)
        if self.items[self.current_item].is_bought:
            screen.blit(self.botton_label_on, (0, 0))
            screen.blit(self.bought, (645, 185))

        else:
            screen.blit(self.botton_label_off, (0, 0))
        if self.items[self.current_item].is_using:
            screen.blit(self.top_label_on, (0, 0))
            screen.blit(self.used, (650, 115))
        else:
            screen.blit(self.top_label_off, (0, 0))

    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1
    def to_end(self):
        if self.current_item != len(self.items) + 1:
            self.current_item -= 1
    def buy (self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.items[self.current_item].is_bought = True
    def use (self):
        if self.items[self.current_item].is_bought == True:
            self.items[self.current_item].is_using = True
    def update(self):
        self.next_button.update()


    def is_clck(self, event):
        self.next_button.is_clck(event)
        self.buy_button.is_clck(event)
        self.use_button.is_clck(event)
        self.end_button.is_clck(event)

class Food:
    def __init__(self, name, file, satiety, price, medicene=0):
        self.name = name
        self.satiety = satiety
        self.price = price
        self.medicene = medicene
        self.image = load1(file, 200, 200)
class Fmenu:
    def __init__(self, game):
        self.game = game
        self.menu = load1("images/menu/menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.botton_label_off = load1("images/menu/bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.botton_label_on = load1("images/menu/bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load1("images/menu/top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load1("images/menu/top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items =[Food("Мясо", "images/food/dog food.png", 10, 10),
                     Food("Корм", "images/food/meat.png", 15, 20),
                     Food("Элит", "images/food/dog food elite.png", 15, 40, medicene=40),
                     Food("Мед", "images/food/medicine.png", 0, 50, medicene=40)


        ]


        self.current_item = 0
        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (250, 250)
        self.next_button = Button("Вперёд", 125, 425,
                                  width=int(BUTTON_WIDTH // 2), height=int(BUTTON_HEIGHT // 2),
                                  func=self.to_next)
        self.end_button = Button("назад", 675, 425,
                                  width=int(BUTTON_WIDTH // 2), height=int(BUTTON_HEIGHT // 2),
                                  func=self.to_end)

        self.eat_button = Button("Сьесть", 400, 375,
                                  width=int(BUTTON_WIDTH // 2), height=int(BUTTON_HEIGHT // 2),
                                  func=self.buy)

    def draw(self, screen):
        screen.blit(self.menu, (0, 0))
        screen.blit(self.items[self.current_item].image, self.item_rect)


    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1
    def to_end(self):
        if self.current_item != len(self.items) + 1:
            self.current_item -= 1
    def buy (self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.game.satiety += self.items[self.current_item].satiety
            if self.game.satiety > 100:
                self.game.satiety = 100
            self.game.health += self.items[self.current_item].medicene
            if self.game.health > 100:
                self.game.health = 100


    def update(self):
        self.next_button.update()
        self.end_button.update()
        self.eat_button.update()


    def is_clck(self, event):
        self.next_button.is_clck(event)
        self.eat_button.is_clck(event)
        self.end_button.is_clck(event)
class Toy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.dog = Dog
        self.ball = load1("images/toys/ball.png", 100, 100)
        self.bone1 = load1("images/toys/blue bone.png", 100, 100)
        self.bone2 = load1("images/toys/red bone.png", 100, 100)
        self.mini = Mini_game
        self.image = None
        self.pic = random.randint(1,3)
        if self.pic == 1:
            self.image = self.ball
        elif self.pic == 2:
            self.image = self.bone1
        elif self.pic == 3:
            self.image = self.bone2
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 10) * SCREEN_WIDTH // 20
        self.rect.y = 30

    def update(self):
        self.rect.y += 1
        if self.rect.y >= SCREEN_HEIGHT:
            self.kill()
class Dog(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = load1("images/dog.png",310 // 2, 500 //2)
        self.rect = self.image.get_rect()
        self.rect.centerx = 450
        self.rect.centery = 550 - 140
    def update(self):
        self.keys = pg.key.get_pressed()
        if self.keys[pg.K_a]:
            self.rect.x -= 1
        if self.keys[pg.K_d]:
            self.rect.x += 1


class Mini_game:
    def __init__(self, game):
        self.game = game
        self.dog = Dog()
        self.background = load1("images/game_background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.dog_image = self.dog.image
        self.toys = pg.sprite.Group()
        self.score = 0
        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 5
    def new_game(self):
        self.background = load1("images/game_background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.dog_image = load1("images/dog.png", 310 // 2, 500 //2)
        self.dog = Dog()
        self.toys = pg.sprite.Group()
        self.score = 0
        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 15



    def update(self):
        self.dog.update()
        self.toys.update()
        if random.randint(0, 1000) == 0:
            self.toys.add(Toy())
        hits = pg.sprite.spritecollide(self.dog, self.toys, True, pg.sprite.collide_rect_ratio(0.6))
        self.score += len(hits)
        if pg.time.get_ticks() - self.start_time > self.interval:
            self.game.happiness += int(self.score)
            self.game.mode = "Main"

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        screen.blit(text_render(self.score), (105, 90))
        screen.blit(self.dog.image, self.dog.rect)
        self.toys.draw(screen)
class Game:
    def __init__(self):
        with open("save.json", encoding="utf-8") as f:
            data = json.load(f)
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Виртуальный питомец")
        self.clock = pg.time.Clock()
        self.background = load1("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.happiness_image = load1("images/happiness.png", icon_size, icon_size)
        self.dog_image = load1("images/dog.png", 310, 500)
        self.satiety_image = load1("images/satiety.png", icon_size, icon_size)
        self.health_image = load1("images/health.png", icon_size, icon_size)
        self.money_image = load1("images/money.png", icon_size, icon_size)
        self.happiness = data["happiness"]
        self.satiety = data["satiety"]
        self.health = data["health"]
        self.money = data["money"]
        self.mode = "Main"
        print(self.mode)
        self.coins_per_second = data["coins_per_second"]
        self.mini_game = Mini_game(self)
        self.fps = 100
        self.clock = pg.time.Clock()

        self.costs_of_upgrade = {}
        for key, value in data["costs_of_upgrade"].items():
            self.costs_of_upgrade[int(key)] = value
        self.button_x = SCREEN_WIDTH - pad - BUTTON_WIDTH
        self.eat = Button("Поесть", self.button_x, 100, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                          func=self.food_menu_on)
        self.clouth = Button("Одежда", self.button_x, 175, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                             func=self.clouth_menu_on)
        self.play = Button("Игры", self.button_x, 250, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                           func=self.game_on)
        self.upgrade_button = Button("Улучшить", self.button_x + 130, 3,
                                     width=BUTTON_WIDTH // 3, height=BUTTON_HEIGHT // 3,
                                     text_font=mini_font,
                                     func=self.increase_money)
        self.clouthes_menu = Cmenu(self, data["clothes"])
        self.food_menu = Fmenu(self)

        self.buttons = [self.upgrade_button, self.play, self.clouth, self.eat]
        self.INCREASE_COINS = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREASE_COINS, 1000)
        self.DECRIASE = pg.USEREVENT + 1
        pg.time.set_timer(self.DECRIASE, 500)
        self.run()
    def food_menu_on(self):
        self.mode = "Food menu"
    def game_on(self):
        self.mode = "Mini game"
        self.mini_game.new_game()
    def clouth_menu_on(self):
        self.mode = "Clouth_menu"
    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(fps)

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.mode == "Game over":
                   data = {"happiness": 100,
                    "satiety": 100,
                    "health": 100,
                    "money": 1000,
                    "coins_per_second": 1,
                    "costs_of_upgrade": {
                        "100": False,
                        "1000": False,
                        "5000": False,
                        "10000": False
                    },
                    "clothes": [
                            {
                            "name": "синия футболка",
                            "price": 10,
                            "image": "images/items/blue t-shirt.png",
                            "is_bought": False,
                            "is_using": False
                            },
                            {"name": "Ботинки",
                             "price": 50,
                             "image": "images/items/boots.png",
                             "is_bought": False,
                             "is_using": False

                             }

                        ]

                    }
                else:
                    data = {"happiness" : self.happiness,
                            "satiety": self.satiety,
                            "health": self.health,
                            "money": self.money,
                            "coins_per_second": self.coins_per_second,
                            "costs_of_upgrade": {
                                "100": self.costs_of_upgrade[100],
                                "1000":self.costs_of_upgrade[1000],
                                "5000": self.costs_of_upgrade[5000],
                                "10000": self.costs_of_upgrade[10000]
                            },
                    'clothes' : []

                    }
                    for item in self.clouthes_menu.items:
                        data["clothes"].append({'name' : item.name,
                                                'price' : item.price,
                                                'image' : item.file,
                                                'is_using' : item.is_using,
                                                'is_bought': item.is_bought



                    })
                with open("save.json", 'w', encoding='utf-8') as  f:
                    json.dump(data, f, ensure_ascii=False)
                pg.quit()
                exit()

            if event.type == self.INCREASE_COINS:
                self.money += self.coins_per_second
            if event.type == self.DECRIASE:
                chance = random.randint(1, 10)
                if chance <= 5:
                    self.satiety -= 1
                elif 5 < chance <= 9:
                    self.happiness -= 1
                else:
                    self.health -= 1
            if self.mode == "Main":
                for button in self.buttons:
                    button.is_clck(event)
            elif self.mode == "Clouth_menu":
                self.clouthes_menu.is_clck(event)
            elif self.mode == "Food menu":
                self.food_menu.is_clck(event)
            if event.type == pg.MOUSEBUTTONDOWN:
                self.money += 1
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.mode = "Main"





    def increase_money(self):
        for cost, check in self.costs_of_upgrade.items():
            if check == False and cost <= self.money:
                self.costs_of_upgrade[cost] = True
                self.coins_per_second += 1
                self.money -= cost

    def update(self):
        if self.happiness == 0 or self.satiety == 0 or self.health == 0:
            self.mode = "Game over"
        elif self.mode == "Clouth_menu":
            self.clouthes_menu.update()
        elif self.mode == "Food menu":
            self.food_menu.update()
        elif self.mode == "Mini game":
            self.mini_game.update()
        else:
            for button in self.buttons:
                button.update()

    def draw(self):
        for button in self.buttons:
            button.draw(self.screen)
        if self.mode == "Clouth_menu":
            self.clouthes_menu.draw(self.screen)
        if self.mode == "Food menu":
            self.food_menu.draw(self.screen)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.happiness_image, (pad, pad))
        self.screen.blit(self.dog_image, (275, 100))
        self.screen.blit(self.health_image, (pad, 70))
        self.screen.blit(self.satiety_image, (pad, 140))
        self.screen.blit(self.money_image, (SCREEN_WIDTH - icon_size - pad * 9, pad))
        self.screen.blit(text_render(self.happiness), (pad + icon_size, pad * 6))
        self.screen.blit(text_render(self.health), (pad + icon_size, 95))
        self.screen.blit(text_render(self.satiety), (pad + icon_size, 165))
        self.screen.blit(text_render(self.money), (SCREEN_WIDTH - icon_size + 35, pad * 6))


        for item in  self.clouthes_menu.items:
            if item.is_using:
                self.screen.blit(item.full_image, (SCREEN_WIDTH // 2 - 350 // 2,100))

        for button in self.buttons:
            button.draw(self.screen)
        if self.mode == "Clouth_menu":
            self.clouthes_menu.draw(self.screen)
            self.clouthes_menu.next_button.draw(self.screen)
            self.clouthes_menu.use_button.draw(self.screen)
            self.clouthes_menu.buy_button.draw(self.screen)
            self.clouthes_menu.end_button.draw(self.screen)
        if self.mode == "Food menu":
            self.food_menu.draw(self.screen)
            self.food_menu.next_button.draw(self.screen)
            self.food_menu.eat_button.draw(self.screen)
            self.food_menu.end_button.draw(self.screen)
        if self.mode == "Mini game":
            self.mini_game.draw(self.screen)
        if self.mode == "Game over":
            text = font_maxi.render("YOU DIED", True, "red")
            text_rect = text.get_rect(center=(SCREEN_WIDTH //2, SCREEN_HEIGHT //2))
            self.screen.blit(text, text_rect)



        pg.display.flip()

if __name__ == "__main__":
    Game()
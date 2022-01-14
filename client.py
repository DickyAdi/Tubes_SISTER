import pygame as spg
from network import Network
spg.font.init()

width = 700
height = 700
win = spg.display.set_mode((width, height))
spg.display.set_caption("Client")

# GUI BUTTON #
class Button:
    def __init__(self, text, x, y, color, img):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 100
        self.height = 100
        self.img = img
        

    def draw(self, win):
        spg.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        win.blit(self.img,(self.x, self.y))
        font = spg.font.SysFont("comicsans", 32)
        text = font.render(self.text, 1, (0,0,0))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

# GUI WINDOW #
def redrawWindow(win, game, p):
    win.fill((148,0,211))

    if not(game.connected()):
        font = spg.font.SysFont("comicsans", 60)
        text = font.render("Menunggu Pemain Lain...", 1, (255,255,255))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = spg.font.SysFont("comicsans", 60)
        text = font.render("Pilihanmu", 1, (0, 255,255))
        win.blit(text, (80, 100))

        text = font.render("Lawan", 1, (0, 255, 255))
        win.blit(text, (420, 100))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothMove():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Move and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Move:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting", 1, (0, 0, 0))

            if game.p2Move and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Move:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 300))
            win.blit(text1, (400, 300))
        else:
            win.blit(text1, (100, 300))
            win.blit(text2, (400, 300))

        for btn in btns:
            btn.draw(win)

    spg.display.update()


image1 = spg.image.load(r".\img\batu.png")
image2 = spg.image.load(r".\img\gunting.png")
image3 = spg.image.load(r".\img\kertas.png")
btns = [Button("Batu", 100, 500, (148,0,211),image1), Button("Gunting", 300, 500, (148,0,211),image2), Button("Kertas", 500, 500, (148,0,211), image3)]

# FUNGSI MAIN #
def main():
    run = True
    clock = spg.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothMove():
            redrawWindow(win, game, player)
            spg.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = spg.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("Kamu Menang!", 1, (0,255,0), True)
            elif game.winner() == -1:
                text = font.render("Game Seimbang!", 1, (255,255,255), True)
            else:
                text = font.render("Kamu kalah...", 1, (255, 0, 0), True)

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            spg.display.update()
            spg.time.delay(2000)

        for event in spg.event.get():
            if event.type == spg.QUIT:
                run = False
                spg.quit()

            if event.type == spg.MOUSEBUTTONDOWN:
                pos = spg.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Move:
                                n.send(btn.text)
                        else:
                            if not game.p2Move:
                                n.send(btn.text)

        redrawWindow(win, game, player)

# FUNGSI UNTUK MENAMPILKAN WINDOW MAIN MENU (SAAT PERTAMA KALI MAIN GAME) #
def menu_screen():
    run = True
    clock = spg.time.Clock()
    image = spg.image.load(r".\img\500.png")

    while run:
        clock.tick(60)
        win.fill((148,0,211))
        font = spg.font.SysFont("comicsans", 60)
        text = font.render("Click Untuk Bermain!", 1, (255,255,255))
        win.blit(text, (65,300))
        win.blit(image, (65,50))
        spg.display.update()

        for event in spg.event.get():
            if event.type == spg.QUIT:
                spg.quit()
                run = False
            if event.type == spg.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()

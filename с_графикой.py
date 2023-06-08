import pygame
from random import randint
pygame.init()
# Определяем размеры окна и кол-во кадров в секунду
WIDTH, HEIGHT = 800, 600
FPS = 60
# Размер картинок
TILE = 32

# Создаем окно
window = pygame.display.set_mode((WIDTH, HEIGHT))
# Создаем таймер времени
clock = pygame.time.Clock()

# Шрифт для интерфейса
fontUI = pygame.font.Font(None, 30)

# Загружаем изображения блоков, танков и взрывов
imgBrick = pygame.image.load('images/block_brick.png')
imgTanks = [
    pygame.image.load('images/tank1.png'),
    pygame.image.load('images/tank2.png'),
    pygame.image.load('images/tank3.png'),
    pygame.image.load('images/tank4.png'),
    pygame.image.load('images/tank5.png'),
    pygame.image.load('images/tank6.png'),
    pygame.image.load('images/tank7.png'),
    pygame.image.load('images/tank8.png'),
    ]
imgBangs = [
    pygame.image.load('images/bang1.png'),
    pygame.image.load('images/bang2.png'),
    pygame.image.load('images/bang3.png'),
    ]

# Создаем список возможных направлений
DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]

# Класс для работы с интерфейсом
class UI:
    def __init__(self): # инициализация
        pass

    def update(self): # метод для обновления
        pass

    def draw(self): #отрисовка
        i = 0 #номер танка
        for obj in objects: # проходим про объектам на экране
            if obj.type == 'tank': #отрисовка UI для каждого танка
                pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))

#отрисовка жизней танков в виде квадрата их цвета и числа жизней
                text = fontUI.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center = (5 + i * 70 + 32, 5 + 11))
                window.blit(text, rect)
                i += 1

#класс для работы с танком
class Tank:
    #инициализируем танк и добавляем в список объектов, задаем тип объекта
    def __init__(self, color, px, py, direct, keyList):
        objects.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE) #задаем квадрат танка
        self.direct = direct #направление
        self.moveSpeed = 2 #скорость движения
        self.hp = 5 #кол-во жизней

        self.shotTimer = 0 #таймер выстрела
        self.shotDelay = 60 #задержка между выстрелами
        self.bulletSpeed = 5 #скорость пули
        self.bulletDamage = 1 #урон

        #кнопки управления танком
        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]

        self.rank = 0 #ранг танка
        #загружаем изображение танка и попорачиваем его на 90 градусов, умножая на -1 (вращение против часовой стрелки)
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        #задаем прямоугольник танка
        self.rect = self.image.get_rect(center = self.rect.center)


    def update(self): #метод обновления танка
        #поворачиваем танк в нужном направлении
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        #уменьшаем размеры изображения
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        #задаем прямоугольник танка
        self.rect = self.image.get_rect(center = self.rect.center)

        #запоминаем старые координаты танка
        oldX, oldY = self.rect.topleft
        #проверяем, нажата ли кнопка управления
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed #двигаем влево
            self.direct = 3 #задаем направление влево
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed #двигаем вверх
            self.direct = 0 #направление вверх
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2

        #проверяем столкновение танка с блоком
        for obj in objects:
            #если объект не является текущим танком и является блоком и есть пересечение прямоугольников
            if obj != self and obj.type == 'block' and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY #возвращаем танк на старые координаты

        #проверяем, нажата ли кнопка выстрела и прошло ли достаточно времени с последнего выстрела
        if keys[self.keySHOT] and self.shotTimer == 0:
            #вычисляем скорость пули по его направлению
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            #создаем пулю
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay #задаем таймер для следующего выстрела

        if self.shotTimer > 0: self.shotTimer -= 1 #если таймер до след. выстрела не истек, то уменьшаем его

    def draw(self): #делаем отрисовку танка
        window.blit(self.image, self.rect) #отрисовка изобр. танка на его прямоугольнике

    def damage(self, value): #функция для получения урона
        self.hp -= value
        if self.hp <= 0: #если жизни закончились, то танк удаляется
            objects.remove(self)
            print(self.color, 'dead') #выводи сообщение о смерти танка

class Bullet: #класс для работы с пулями
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self) #добавляем снаряд в список всех снарядов
        self.parent = parent #запоминаем родительский объект - танк
        #задаем координаты и направление пули и урон
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self): #обновление состояния пули
        #двигаем пулю
        self.px += self.dx
        self.py += self.dy

        #проверяем, вышла ли пуля за пределы окна
        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self) #если да, то удаляем её из списка пуль
        else:
            for obj in objects: #если нет, то проверяем ее столкновение с другими объектами
                #проверяем, что объект не явл. родителем пули и не явл. об. взрыва и что пуля столкнулась с объектом
                if obj != self.parent and obj.type != 'bang' and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage) #наносим урон объекту
                    bullets.remove(self) #удаляем пулю из списка
                    Bang(self.px, self.py) #создаем объект взрыва на месте столкновения
                    break #выходим из цикла проверки столкновения

    def draw(self): #отрисовка пули
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)

class Bang: #класс объекта взрыва
    def __init__(self, px, py):
        objects.append(self) #добавляем в список игровых объектов
        self.type = 'bang' #устанавливаем тип объекта

        self.px, self.py = px, py #устан. коорд. объекта взрыва
        self.frame = 0 #устан. текущий фрейм анимации взрыва

    def update(self): #обновляем состояние об. взрыва
        self.frame += 0.2 #увелич. тек. фрейм анимации взрыва
        if self.frame >= 3: objects.remove(self) #если произошло более 3 фреймов, удаляем об. из списка об.

    def draw(self): #отрисовка об. взрыва
        image = imgBangs[int(self.frame)] #получаем картинку тек. фр. аним. взрыва
        rect = image.get_rect(center = (self.px, self.py)) #получ. прямоуг., в который необход. нарис. картинку
        window.blit(image, rect) #рис. картинку в прямоуг.
    
class Block: #класс блока
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1 #кол-во жизней блока

    def update(self):
        pass

    def draw(self):
        window.blit(imgBrick, self.rect)

    def damage(self, value): #нанесение урона блоку
        self.hp -= value #уменьш. кол-во жизней
        if self.hp <= 0: objects.remove(self) #удал. блок, если его жизни закончились

#создаем список пуль и объектов
bullets = []
objects = []
#создаем синий и красный танки с изначальными координатами и параметрами управления клавишами клавиатуры
Tank('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
Tank('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER))
ui = UI() #создаем объект интерфейса

for _ in range(50): #создаем 50 блоков на поле с помощью рандома
    while True:
        x = randint(0, WIDTH // TILE - 1) * TILE #генерация случайных координат
        y = randint(1, HEIGHT // TILE - 1) * TILE
        rect = pygame.Rect(x, y, TILE, TILE) #создание прямоугольника блока по координатам
        fined = False #поиск пересечения с другими объектами на игровом поле
        for obj in objects:
            if rect.colliderect(obj.rect): fined = True

        if not fined: break #если пересечений нет, то поиск прекращается

    Block(x, y, TILE) #создаем и добавляем объект блок в список объектов

play = True #основной игровой цикл
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    keys = pygame.key.get_pressed() #получение нажатых клавиш

    #обновление состояний всех объектов в игре
    for bullet in bullets: bullet.update()
    for obj in objects: obj.update()
    ui.update()

    window.fill('black') #очистка экрана
    #отрисовка всех объектов в игре
    for bullet in bullets: bullet.draw()
    for obj in objects: obj.draw()
    ui.draw()
    
    pygame.display.update() #обновление экрана
    clock.tick(FPS) #установка задержки
    
pygame.quit()
"""
Kласс Car який має атрибути fuel(паливо, задається за допомогою random.randrange(0, 9)),
trip_distance(Відстань яку проїхав автомобіль),
model (модель авто) та color(колір)
реалізовано в класі метод move() який приймає distance як аргумент.

Клас Race який мєє атрибути race_cars(список авто для гонки) та winner(перможець)

Мотод add_car_on_race для додавання автомобілів нв гонку

Реалізовано метод race() який приймає парамер laps(кількість кругів для гонки)
в якому цикл for переввіряє чи достатньо учасників для проведення заїзду поточного та виводить номер круга
також всередині якого є вкладений цикл for який викликає метод move() для кожного учасника і зберігає його у новому
списку remaining_cars якщо вони можуть продовжити гонку. Наступним кроком визначаємо переможця і виводимо його або
виводимо повідомлення про нічию якщо переможців декілька

"""

import random


# створюємо клас Car
class Car:
    # ініціалізуємо атрибути класу
    def __init__(self, model, color):
        self.model = model  # модель авто
        self.color = color  # колір авто
        self.fuel = random.randrange(0, 9)  # паливо, задається випадково від 0 до 8
        self.trip_distance = 0  # відстань, яку проїхав авто

    # створюємо метод move, який приймає distance як аргумент
    def move(self, distance):
        # перевіряємо, чи достатньо палива для руху
        if self.fuel >= distance:
            # зменшуємо паливо на відстань руху
            self.fuel -= distance
            # збільшуємо відстань, яку проїхав авто, на відстань руху
            self.trip_distance += distance
            # повертаємо True, якщо авто змогло рухатися
            return True
        else:
            # повертаємо False, якщо авто не має достатньо палива
            return False


# створюємо клас Race
class Race:
    # ініціалізуємо атрибути класу
    def __init__(self):
        self.race_cars = []  # Список Учасників
        self.winner = None

    # Метод додавання авто для гонки
    def add_car_on_race(self, car):
        self.race_cars.append(car)

    # Функція яка приймає кількість кругів та визначає переможця
    def race(self, laps):
        for lap in range(1, laps + 1):
            if len(self.race_cars) < 2:  # Виходимо із гонки якщо залишилось менше 2х учасників
                print('Недостатньо учасників для проведення гонки')
                break
            print(f"=== Круг {lap} ===")
            remaining_cars = []  # Зберігаємо гонщиків, які ще можуть продовжувати гонку
            for car in self.race_cars:
                moved = car.move(1)  # Припустимо, що в кожен круг рухається на 1 одиницю відстані
                if moved:
                    if car.fuel > 0:  # Якщо в баку є топливо додаємо їх на наступний круг
                        remaining_cars.append(car)
                    print(
                        f"{car.model} ({car.color}): Пройдено {lap}-ий круг. Залишилося пального: {car.fuel}")

            self.race_cars = remaining_cars  # Оновлюємо гонщиків, які можуть продовжувати гонку

        if len(self.race_cars) > 0:  # визначаємо переможця
            self.winner = max(self.race_cars, key=lambda x: x.trip_distance)
            #  Виводимо модель та колір пкреможця а також кількісь кругів яку міг би зробити з його запасом ходу
            print(f'Переможець {self.winner.model} ({self.winner.color}) проїхавши'
                  f' {self.winner.trip_distance + self.winner.fuel} кругів')
        else:
            print('Гонка завершилась, нічиєю')


# Створюємо автомобілі
car_a = Car('BMW', "red")
car_b = Car('Audi', "blue")
car_c = Car('Mercedes', "white")
car_d = Car('Renault', "black")
car_e = Car('Porch', "yellow")
car_f = Car('Lamborghini', "gray")

# Створюємо гонку
race = Race()

# Добавляємо учасників гонки
race.add_car_on_race(car_a)
race.add_car_on_race(car_b)
race.add_car_on_race(car_c)
race.add_car_on_race(car_d)
race.add_car_on_race(car_e)
race.add_car_on_race(car_f)

# Проводимо гонку на 9 кругів
race.race(9)

"""
Kласс Car який має атрибути fuel(паливо, задається за допомогою random.randrange(0, 9)),
trip_distance(Відстань яку проїхав автомобіль),
model (модель авто) та color(колір)
реалізовано в класі метод move який приймає distance як аргумент.

Цикл while race_dist < desired_dist: викликає для кожного екземпляру класу метод move та передає йому значення
random.randrange(0, 9). Метод move  додає до trip_distance значення, яке було повернуто методом randomrange
та зменшує кількість палива на це ж значення

Як тільки один із автомобілів проїхав відстань більшу або яка дорівнює desired_dist - виводиться  повідомлення
про те що автомобіль переміг, вказано марку та дистанцію яку проїхав цей автомобіль.
Цикл у такому випадку переривається

Після циклу виводимо повідомлення про те скільки і який автомобіль проїхав, та який у нього запас палива
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


# створюємо 3 екземпляри класу Car
car1 = Car("Tesla", "червоний")
car2 = Car("BMW", "синій")
car3 = Car("Toyota", "зелений")

# для того щоб цикл while не був бескінечним у випадку коли у жодному авто недостатньо палива для проходження гонки
# і вмходу із циклу,- встановлюємо дистанцію на максимальне значення палива із всіх учасників
desired_dist = max(car1.fuel, car2.fuel, car3.fuel)

# задаємо поточну відстань гонки
race_dist = 0

# використовуємо цикл while для симуляції гонки
while race_dist < desired_dist:
    # для кожного авто викликаємо метод move з випадковою відстанню від 0 до 8
    car1.move(random.randrange(0, 9))
    car2.move(random.randrange(0, 9))
    car3.move(random.randrange(0, 9))
    # знаходимо максимальну відстань, яку проїхав один з авто
    race_dist = max(car1.trip_distance, car2.trip_distance, car3.trip_distance)
    # якщо один з авто проїхав бажану відстань або більше, то виводимо повідомлення про перемогу
    if race_dist >= desired_dist:
        # визначаємо, який авто переміг
        if car1.trip_distance == race_dist:
            winner = car1
        elif car2.trip_distance == race_dist:
            winner = car2
        else:
            winner = car3
        # виводимо повідомлення про перемогу, вказавши марку та відстань переможця
        print(f"Автомобіль {winner.model} {winner.color} переміг, проїхавши {winner.trip_distance} км.")
        # перериваємо цикл
        break

# після циклу виводимо повідомлення про те, скільки і який автомобіль проїхав, та який у нього запас палива
print(f"Автомобіль {car1.model} {car1.color} проїхав {car1.trip_distance} км, у нього залишилося {car1.fuel} л палива.")
print(f"Автомобіль {car2.model} {car2.color} проїхав {car2.trip_distance} км, у нього залишилося {car2.fuel} л палива.")
print(f"Автомобіль {car3.model} {car3.color} проїхав {car3.trip_distance} км, у нього залишилося {car3.fuel} л палива.")

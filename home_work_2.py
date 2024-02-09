def length_of_string(input_string: str):
    """
    Функція, яка приймає рядок і повертає його довжину.

    Параметри:
    - input_string (str): Вхідний рядок.

    Повертає:
    - int: Довжина вхідного рядка.
    """
    return len(input_string)


def concatenate_strings(string_1: str, string_2: str):
    """
    Функція, яка приймає два рядки і повертає об'єднаний рядок.

    Параметри:
    - string_1 (str): 1-й рядок.
    - string_2 (str): 2-й рядок.

    Повертає:
    - str: Об'єднаний рядок.
    """
    return string_1 + string_2


def square_of_number(number):
    """
    Функція, яка повертає квадрат переданого числа.

    Параметри:
    - number (float або int): Число, квадрат якого потрібно знайти.

    Повертає:
    - float або int: Квадрат введеного числа.
    """
    return number ** 2


def sum_of_number(num1, num2):
    """
    Функція, яка повертає суму переданих чисел.

    Параметри:
    - num1 (float або int): Перше число.
    - num2 (float або int): Друге число.

    Повертає:
    - float або int: Суму переданих чисел.
    """
    return num1 + num2


def division_of_number(num1: int, num2: int):
    """
    Функція, яка приймає 2 числа типу int, виконує операцію ділення та повертає цілу частину і залишок.

    Параметри:
    - num1: Перше число.
    - num2: Друге число.

    Повертає:
    - int:  Цілу частину і залишокл.
    """
    return num1 // num2, num1 % num2


def calculate_average(numbers):
    """
    Функція, яка обчислює середнє значення списку чисел.

    Параметри:
    - numbers (list): Список чисел.

    Повертає:
    - float: Середнє значення чисел у списку.
    """
    return sum(numbers) / len(numbers)


def find_common_elements(list1, list2):
    """
    Функція, яка приймає два списки і повертає список, який містить спільні елементи обох списків.

    Параметри:
    - list1 (list): Перший список чисел.
    - list2 (list): Другий список чисел.

    Повертає:
    - list: Спільні елементи обох списків.
    """
    return list(set(list1).intersection(set(list2)))


def keys_dictionary(my_dict):
    """
    Функція, яка приймає словник і виводить всі ключі цього словника.

    Параметри:
    - my_dict (dict): Словник.

   Повертає:
    - None: Виводить ключі цього словника.
    """
    print(my_dict.keys())


def merge_dictionaries(dict1, dict2):
    """
    Функція, яка об'єднує два словники.

    Параметри:
    - dict1 (dict): Перший словник.
    - dict2 (dict): Другий словник.

    Повертає:
    - dict: Об'єднаний словник.
    """
    return {**dict1, **dict2}


def union_sets(set1, set2):
    """
    Функція, яка приймає дві множини і повертає їхнє об'єднання.

    Параметри:
    - set1 (set): Перша множина.
    - set2 (set): Друга мгожина.

    Повертає:
    - set: Об'єднання обох множин.
    """
    return set1.union(set2)


def is_subset(set1, set2):
    """
    Функція, яка перевіряє, чи є одна множина підмножиною іншої.

    Параметри:
    - set1 (set): Перша множина.
    - set2 (set): Друга множина.

    Повертає:
    - bool: True, якщо set1 є підмножиною set2, інакше False.
    """
    return set1.issubset(set2)


def check_parity(number):
    """
    Функція, яка визначає парність чи непарність числа та виводить відповідне повідомлення.

    Параметри:
    - number (int): Вхідне число.

    Повертає:
    - None: Функція виводить результат, але не повертає значення.
    """
    if number % 2 == 0:
        print("Парне")
    else:
        print("Непарне")


def even_number_list(list_num):
    """
    Функція, яка приймає список чисел і повертає новий список, що містить тільки парні числа.

    Параметри:
    - list_num (list): Вхідний список чисел.

    Повертає:
    - list: Cписок, що містить тільки парні числа.
    """
    return [num for num in list_num if num % 2 == 0]

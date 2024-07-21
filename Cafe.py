# Моделирование работы сети кафе с несколькими столиками и потоком посетителей, прибывающих для заказа пищи и
# уходящих после завершения приема.
#
# Есть сеть кафе с несколькими столиками. Посетители приходят, заказывают еду, занимают столик, употребляют еду и уходят.
# Если столик свободен, новый посетитель принимается к обслуживанию, иначе он становится в очередь на ожидание.
#
# Создайте 3 класса:
# Table - класс для столов, который будет содержать следующие атрибуты: number(int) - номер стола,
# is_busy(bool) - занят стол или нет.
#
# Cafe - класс для симуляции процессов в кафе. Должен содержать следующие атрибуты и методы:
# Атрибуты queue - очередь посетителей (создаётся внутри init), tables список столов (поступает из вне).
# Метод customer_arrival(self) - моделирует приход посетителя(каждую секунду).
# Метод serve_customer(self, customer) - моделирует обслуживание посетителя. Проверяет наличие свободных столов,
# в случае наличия стола - начинает обслуживание посетителя (запуск потока), в противном случае - посетитель поступает
# в очередь. Время обслуживания 5 секунд.
# Customer - класс (поток) посетителя. Запускается, если есть свободные столы.
#
# Так же должны выводиться текстовые сообщения соответствующие событиям:
# Посетитель номер <номер посетителя> прибыл.
# Посетитель номер <номер посетителя> сел за стол <номер стола>. (начало обслуживания)
# Посетитель номер <номер посетителя> покушал и ушёл. (конец обслуживания)
# Посетитель номер <номер посетителя> ожидает свободный стол. (помещение в очередь
# Пример работы:
# # Создаем столики в кафе
# table1 = Table(1)
# table2 = Table(2)
# table3 = Table(3)
# tables = [table1, table2, table3]
#
# # Инициализируем кафе
# cafe = Cafe(tables)
#
# # Запускаем поток для прибытия посетителей
# customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
# customer_arrival_thread.start()
#
# # Ожидаем завершения работы прибытия посетителей
# customer_arrival_thread.join()
#

import time
from threading import Thread
import queue

class Table:                 # Создаем словарь столов, где ключ - номер стола, значение - занят (True) или свободен (False)
    def __init__(self, number):
        self.number = number
        self.tables = {}

    def add_dict_tables(self):
        is_busy = False
        self.tables[self.number] = is_busy
        return self.tables

class Cafe:
    def __init__(self, tables):
        self.tables = tables
        self.queue = queue.Queue()

    def customer_arrival(self):
        customer = 0
        for i in range(1, 21):
            customer += 1
            print(f'Посетитель номер {customer} прибыл.')
            self.serve_customer(customer)
            time.sleep(1)
        return customer
    def serve_customer(self, customer):
        for key in self.tables:                             # Получаем список номеров столов из словаря
            if not self.tables[key]:
                self.tables[key] = True
                customer = Customer(key, customer, self)
                customer.start()
                return
        print(f"Посетитель номер {customer} ожидает свободный стол")
        self.queue.put(customer)

    def table_check(self, table):
        if not self.queue.empty():
            get_customer = self.queue.get()
            customer = Customer(table, get_customer, self)
            customer.start()
        else:
            self.tables[table] = False

class Customer(Thread):
    def __init__(self, table, customer, cafe):
        super().__init__()
        self.table = table
        self.customer = customer
        self.cafe = cafe

    def run(self):
        print(f'Посетитель {self.customer} сел за стол номер {self.table}')
        time.sleep(5)
        print(f"Посетитель номер {self.customer} покушал и ушёл")
        self.cafe.table_check(self.table)



table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
table4 = Table(4)

table_1 = table1.add_dict_tables()
table_2 = table2.add_dict_tables()
table_3 = table3.add_dict_tables()
table_4 = table4.add_dict_tables()

tables = {**table_1, **table_2, **table_3, **table_4}


cafe = Cafe(tables)

customer_arrival_thread = Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

customer_arrival_thread.join()


class Counter:
    current=0
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end
        # print(self.current) # --> 0
        # print(self.start) # --> 0
        # print(self.end) # --> 20

    def increase(self):
        # Функция по умолчанию возвращает None т.е. не чего не возвращает 
        if self.current < self.end: 
            self.current += 1
            return self.current # Что-бы ваш счётчик заработал нужно возвращать значение   
        else: 
            return 'Out of range'

my_count=Counter(start=0, end=3)
print(my_count.increase()) # --> 1
print(my_count.increase()) # --> 2
print(my_count.increase()) # --> 3
print(my_count.increase()) # --> 'Out of range'
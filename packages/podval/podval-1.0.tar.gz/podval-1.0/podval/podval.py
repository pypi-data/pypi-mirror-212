def Stack():
    print('''class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        if self.is_empty():
            return None
        else:
            popped_item = self.head.data
            self.head = self.head.next
            return popped_item

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.head.data

    def __str__(self):
        current = self.head
        stack_str = ""
        while current:
            stack_str += str(current.data) + " → "
            current = current.next
        return stack_str.rstrip(" → ")''')
    
def Stack1():
    print('''#Дан стек и число  k . Необходимо найти  k -й по счету элемент в стеке.
    def find(s, i):
    current = s.head
    k=1
    while current and k<=i:
        if k==i:
            return f'Элемент под номером {i}: {current.data}'
        current = current.next
        k+=1
    return 'Элемента с таким номером в данном стеке нет'
    ''')
    
def Stack2():
    print('''#Дан стек и значение  A . Необходимо удалить из стека все элементы, которые больше  A .
    stack2 = Stack()

while not stack1.is_empty():
    temp = stack1.pop()
    if temp <= A:
        stack2.push(temp)

while not stack2.is_empty():
    stack1.push(stack2.pop())
''')

def Stack3():
    print('''#Дан стек и два элемента  A  и  B . Необходимо удалить из стека все элементы, которые находятся между  A  и  B  (включая сами  A  и  B
    A = int(input())
B = int(input())
bf_stack = Stack()
while not(stack.is_empty()):
  if stack.peek() == A:
    while stack.peek() != B:
      stack.pop()
    if stack.peek() == B:
      stack.pop()
  bf_stack.push(stack.peek())
  stack.pop()
while not(bf_stack.is_empty()):
  stack.push(bf_stack.peek())
  bf_stack.pop()
print(stack)''')
    
def Stack4():
    print('''#Дан стек. Необходимо найти среднее арифметическое всех его элементов.
    from random import randint

for i in range(10):
    a.push(randint(1,20))
cnt = 0
s = 0
while a.is_empty() ^ 1:
    cnt += 1
    s += a.peek()
    a.pop()
s/cnt''')
    
def Stack5():
    print('''#Дан стек. Необходимо проверить, есть ли в нем повторяющиеся элементы. Вывести повторяющиеся элементы, если они есть.
    def find_dup(stack):
    seen = set()
    dup = set()
    current = stack.top
    while current is not None:
        if current.data in seen:
            dup.add(current.data)
        else:
            seen.add(current.data)
        current = current.next
    return dup''')
    
def Stack6():
    print('''#Дан стек. Необходимо удалить из него все отрицательные элементы.
    stack = Stack()
for i in range(10):
    stack.add(random.randint(-10,10))
    def del_negative(stack):
    val = stack.head
    basket = []
    while val:
        if 0 > val.data:
            pp = stack.pop()
            while pp != val.data:
                basket.append(pp)
                pp = stack.pop()
        val = val.next
    for i in reversed(basket):
        stack.add(i)
    return stack
print(del_negative(stack)) ''')
           
def Queue():
    print('''
   class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return not bool(self.head)

    def enqueue(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return data

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        current = self.head
        queue_str = ""
        while current:
            queue_str += " → " + str(current.data)
            current = current.next
        return queue_str.lstrip(" → ")  ''')

def Queue1():
    print('''# функция для нахождения первого нечетного элемента очереди
def find_first_odd(queue):
    current = queue.head
    while current:
        if current.data % 2 != 0:
            return current.data
        current = current.next
    return None''')

def Queue2():
    print('''# функция для добавления нового элемента в очередь перед первым четным элементом
def add_before_first_even(queue, item):
    new_node = Node(item)
    if not queue.head:
        queue.head = new_node
        queue.tail = new_node
    elif queue.head.data % 2 == 0:
        new_node.next = queue.head
        queue.head = new_node
    else:
        prev_node = queue.head
        current = prev_node.next
        while current:
            if current.data % 2 == 0:
                prev_node.next = new_node
                new_node.next = current
                return
            prev_node = current
            current = current.next
        queue.tail.next = new_node
        queue.tail = new_node''')

def Queue3():
    print('''# альтернативная функция для добавления нового элемента в очередь перед первым четным элементом
def add_before_first_even(queue, data):
    temp_queue = Queue()
    even_found = False

    while not queue.is_empty():
        item = queue.dequeue()
        if item % 2 == 0 and not even_found:
            temp_queue.enqueue(data)
            even_found = True
        temp_queue.enqueue(item)

    while not temp_queue.is_empty():
        queue.enqueue(temp_queue.dequeue())''')

def Queue4():
    print('''Создать класс очереди, который будет поддерживать операции добавления элемента в конец очереди и удаления всех элементов из очереди, которые меньше заданного значения.
    class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return not bool(self.head)

    def enqueue(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node


    def dequeue_less(self, par):
        current = self.head
        previous = None

        while current:
            if current.data < par:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next

                if current == self.tail:
                    self.tail = previous
            else:
                previous = current
            current = current.next


    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        current = self.head
        queue_str = ""
        while current:
            queue_str += " → " + str(current.data)
            current = current.next
        return queue_str.lstrip(" → ")''')

def Queue5():
    print('''Сортировка значений очереди по возрастанию
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return not bool(self.head)

    def enqueue(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return data
    
    def listed(self):
        current = self.head
        queue_str = []
        while current:
            queue_str.append(current.data)
            current = current.next
        return queue_str

    def sorting(queue):
      temp_queue = sorted(Queue.listed(queue))
      queue = Queue()
      for i in temp_queue:
          queue.enqueue(i)
      return queue                       

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        current = self.head
        queue_str = ""
        while current:
            queue_str += " → " + str(current.data)
            current = current.next
        return queue_str.lstrip(" → ")  ''')

def Queue6():
    print('''Создать класс очереди, который будет поддерживать операции добавления элемента в конец очереди и удаления всех повторяющихся элементов из очереди.
    class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return not bool(self.head)

    def enqueue(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return data

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    
    def del_repeats(self):
        new_data = []
        while self.head:
            if self.head.data not in new_data:
                new_data.append(self.head.data)
            self.head = self.head.next
        self.tail = None
        for i in new_data:
            self.enqueue(i)

    def __str__(self):
        current = self.head
        queue_str = ""
        while current:
            queue_str += " → " + str(current.data)
            current = current.next
        return queue_str.lstrip(" → ")  ''')

def Queue7():
    print('''Создать класс очереди с ограниченной емкостью. Если при добавлении элемента очередь уже заполнена, то новый элемент должен заменить первый элемент в очереди.

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue5:
    def __init__(self, capacity):
        self.head = None
        self.tail = None
        self.capacity = capacity

    def is_empty(self):
        return not bool(self.head)

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    
    def enqueue(self, data):
        new_node = Node(data)
        
        if self.__len__() < self.capacity:
            print('место в очереди еще есть')
            if not self.head:
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next = new_node
                self.tail = new_node
        else:
            print('места в очереди уже нет')
            self.head.data = new_node.data
            

    def dequeue(self):
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return data

    def __str__(self):
        current = self.head
        queue_str = ""
        while current:
            queue_str += " → " + str(current.data)
            current = current.next
        return queue_str.lstrip(" → ") ''')
    
def DoublyLinkedList():
    print('''
    class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            new_node.prev = current

    def delete_node(self, data):
        if self.head is None:
            return
        elif self.head.data == data:
            if self.head.next is not None:
                self.head = self.head.next
                self.head.prev = None
            else:
                self.head = None
        else:
            current = self.head
            while current.next is not None and current.next.data != data:
                current = current.next
            if current.next is None:
                return
            else:
                current.next = current.next.next
                if current.next is not None:
                    current.next.prev = current

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        if self.head == None:
            return f"Двусвязный список пустой"
        current = self.head
        dllist_str = ""
        while current:
            dllist_str += " ⇄ " + str(current.data)
            current = current.next
        return dllist_str.lstrip(" ⇄ ") ''')
    
def CircularDoublyLinkedList():
    print('''class Data:
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None

class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Data(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            new_node.prev = self.tail
            new_node.next = self.head
        else:
            new_node.prev = self.tail
            new_node.next = self.head
            self.tail.next = new_node
            self.head.prev = new_node
            self.tail = new_node

    def prepend(self, data):
        new_node = Data(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            new_node.prev = self.tail
            new_node.next = self.head
        else:
            new_node.prev = self.tail
            new_node.next = self.head
            self.head.prev = new_node
            self.tail.next = new_node
            self.head = new_node

    def delete(self, key):
        current_node = self.head
        while current_node:
            if current_node.data == key:
                if current_node == self.head:
                    self.head = current_node.next
                    self.tail.next = self.head
                    self.head.prev = self.tail
                elif current_node == self.tail:
                    self.tail = current_node.prev
                    self.head.prev = self.tail
                    self.tail.next = self.head
                else:
                    current_node.prev.next = current_node.next
                    current_node.next.prev = current_node.prev
                return
            current_node = current_node.next

    def __len__(self):
        count = 0
        current_node = self.head
        while current_node:
            count += 1
            current_node = current_node.next
            if current_node == self.head:
                break
        return count

    def __str__(self):
        cdllist_str = ""
        current_node = self.head
        while current_node:
            cdllist_str += str(current_node.data) + " ⇄ "
            current_node = current_node.next
            if current_node == self.head:
                break
        return " ⇄ " + cdllist_str''')


def Sorting():
    print('''import time

class Sorting:

    # простая обменная сортировка
    @staticmethod
    def bubble_sort(arr, reverse=False):
        n = len(arr)
        for i in range(n):
            for j in range(n - i - 1):
                if not reverse:
                    if arr[j] > arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
                else:
                    if arr[j] < arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    # шейкерная сортировка
    @staticmethod
    def cocktail_sort(arr, reverse=False):
        n = len(arr)
        start = 0
        end = n - 1
        swapped = True
        while swapped:
            swapped = False
            for i in range(start, end):
                if (not reverse and arr[i] > arr[i + 1]) or (reverse and arr[i] < arr[i + 1]):
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    swapped = True
            if not swapped:
                break
            swapped = False
            end = end - 1
            for i in range(end - 1, start - 1, -1):
                if (not reverse and arr[i] > arr[i + 1]) or (reverse and arr[i] < arr[i + 1]):
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    swapped = True
            start = start + 1
        return arr

    # сортировка расчёской
    @staticmethod
    def comb_sort(arr, reverse=False):
        n = len(arr)
        gap = n
        shrink = 1.3
        swapped = True
        while swapped:
            gap = int(gap/shrink)
            if gap < 1:
                gap = 1
            i = 0
            swapped = False
            while i+gap < n:
                if (not reverse and arr[i] > arr[i+gap]) or (reverse and arr[i] < arr[i+gap]):
                    arr[i], arr[i+gap] = arr[i+gap], arr[i]
                    swapped = True
                i += 1
        return arr

    # сортировка выбором
    @staticmethod
    def selection_sort(arr, reverse=False):
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if reverse:
                    if arr[j] > arr[min_idx]:
                        min_idx = j
                else:
                    if arr[j] < arr[min_idx]:
                        min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

    # сортировка включением
    @staticmethod
    def insertion_sort(arr, reverse=False):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and ((not reverse and arr[j] > key) or (reverse and arr[j] < key)):
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    # быстрая сортировка
    @staticmethod
    def quick_sort(arr, reverse=False):
        if len(arr) <= 1:
            return arr
        else:
            pivot = arr[0]
            left = []
            right = []
            for i in range(1, len(arr)):
                if arr[i] < pivot:
                    left.append(arr[i])
                else:
                    right.append(arr[i])
            if reverse:
                return Sorting.quick_sort(right, reverse=True) + [pivot] + Sorting.quick_sort(left, reverse=True)
            else:
                return Sorting.quick_sort(left) + [pivot] + Sorting.quick_sort(right)

    # сортировка Шелла
    @staticmethod
    def shell_sort(arr, reverse=False):
        gap = len(arr) // 2
        while gap > 0:
            for i in range(gap, len(arr)):
                temp = arr[i]
                j = i
                while j >= gap and ((not reverse and arr[j - gap] > temp) or (reverse and arr[j - gap] < temp)):
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = temp
            gap //= 2
        return arr

    # сортировка слиянием
    @staticmethod
    def merge_sort(arr, reverse=False):
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        
        left_half = Sorting.merge_sort(left_half, reverse=reverse)
        right_half = Sorting.merge_sort(right_half, reverse=reverse)
        
        return Sorting.merge(left_half, right_half, reverse=reverse)

    # вспомогательная функция для сортировки слиянием
    @staticmethod
    def merge(left_half, right_half, reverse=False):
        result = []
        i = 0
        j = 0
        while i < len(left_half) and j < len(right_half):
            if not reverse:
                if left_half[i] <= right_half[j]:
                    result.append(left_half[i])
                    i += 1
                else:
                    result.append(right_half[j])
                    j += 1
            elif reverse:
                if left_half[i] >= right_half[j]:
                    result.append(left_half[i])
                    i += 1
                else:
                    result.append(right_half[j])
                    j += 1
        result += left_half[i:]
        result += right_half[j:]
        return result

    # декоратор, вычисляющий время выполнения функции и выводящий его на экран
    def measure_time(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()            
            print(f"\nВремя выполнения {tuple(kwargs.items())[0][1]}_sort: {end - start:.6f} сек.")
            return result
        return wrapper

    @staticmethod
    @measure_time
    def sort(arr, method='bubble', reverse=False):
        if method == 'bubble':
            return Sorting.bubble_sort(arr, reverse)
        elif method == 'cocktail':
            return Sorting.cocktail_sort(arr, reverse)
        elif method == 'comb':
            return Sorting.comb_sort(arr, reverse)
        elif method == 'selection':
            return Sorting.selection_sort(arr, reverse)
        elif method == 'insertion':
            return Sorting.insertion_sort(arr, reverse)
        elif method == 'quick':
            return Sorting.quick_sort(arr, reverse)
        elif method == 'shell':
            return Sorting.shell_sort(arr, reverse)
        elif method == 'merge':
            return Sorting.merge_sort(arr, reverse)''')
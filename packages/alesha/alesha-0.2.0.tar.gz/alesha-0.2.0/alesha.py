'''
Здарова дружище, пользуйся реализациям на здоровье
За код структур данных и сортировок поблагодарим Виталия Игоревича
За то что ты сейчас видишь это сообщение благодари твоего скромного слугу - Rekzi
'''

def get_stack():
    'Возвращает реализацию стека'
    return("""
class Node:
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
        return stack_str.rstrip(" → ")
    """)


def get_queue():
    'Возвращает реализацию очереди'
    return("""
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
        return queue_str.lstrip(" → ")  
    """)

def get_double_linked_list():
    'Возвращает реализацию двусвязного списка'
    return("""
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
        return dllist_str.lstrip(" ⇄ ")   
    """)

def get_circular_doubly_linked_list():
    'Возвращает циклический двусвязный список'
    return("""
class Node:
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None

class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
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
        new_node = Node(data)
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
        return " ⇄ " + cdllist_str
    """)
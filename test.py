class A:
    def __init__(self, num):
        self.num = num

    def get_num(self):
        return self.num

    def draw(self):
        print("drawing!!!")

A(3).draw()

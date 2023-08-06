class Generate:
    def _square(self, i):
        result = i * i
        print("-------------------")
        print(f'Square of {i}: {result}')
        print("-------------------")

    def _cube(self, i):
        result = i * i * i
        print("-------------------")
        print(f'Cube of {i}: {result}')
        print("-------------------")

    def square(self, i):
        self._square(i)

    def cube(self, i):
        self._cube(i)

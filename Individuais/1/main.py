class KaratsubaMultiplier:
    def multiply(self, x: int, y: int) -> int:
        if x < 10 or y < 10:
            return x * y
        n = max(len(str(x)), len(str(y)))
        m = n // 2
        high_x, low_x = divmod(x, 10 ** m)
        high_y, low_y = divmod(y, 10 ** m)
        z0 = self.multiply(low_x, low_y)
        z1 = self.multiply(low_x + high_x, low_y + high_y)
        z2 = self.multiply(high_x, high_y)
        return (z2 * 10 ** (2 * m)) + ((z1 - z2 - z0) * 10 ** m) + z0

class InputHandler:
    def get_numbers(self) -> tuple[int, int]:
        x = int(input("Enter the first integer: "))
        y = int(input("Enter the second integer: "))
        return x, y

class OutputHandler:
    def show_result(self, result: int) -> None:
        print(f"Result: {result}")

class KaratsubaApp:
    def __init__(self):
        self.input_handler = InputHandler()
        self.output_handler = OutputHandler()
        self.multiplier = KaratsubaMultiplier()

    def run(self):
        x, y = self.input_handler.get_numbers()
        result = self.multiplier.multiply(x, y)
        self.output_handler.show_result(result)

if __name__ == "__main__":
    app = KaratsubaApp()
    app.run()

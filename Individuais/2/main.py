from typing import List, Tuple
from abc import ABC, abstractmethod


class MaxMinResult:
    def __init__(self, minimum: int, maximum: int):
        self.minimum = minimum
        self.maximum = maximum
    
    def __str__(self):
        return f"Min: {self.minimum}, Max: {self.maximum}"


class MaxMinSelector(ABC):
    @abstractmethod
    def find_max_min(self, numbers: List[int]) -> MaxMinResult:
        pass


class DivideConquerMaxMinSelector(MaxMinSelector):
    def __init__(self):
        self.comparison_count = 0
    
    def find_max_min(self, numbers: List[int]) -> MaxMinResult:
        if not numbers:
            raise ValueError("List cannot be empty")
        
        self.comparison_count = 0
        result = self._max_min_recursive(numbers, 0, len(numbers) - 1)
        return result
    
    def _max_min_recursive(self, numbers: List[int], low: int, high: int) -> MaxMinResult:
        if low == high:
            return MaxMinResult(numbers[low], numbers[high])
        
        if high == low + 1:
            self.comparison_count += 1
            if numbers[low] > numbers[high]:
                return MaxMinResult(numbers[high], numbers[low])
            else:
                return MaxMinResult(numbers[low], numbers[high])
        
        mid = (low + high) // 2
        left_result = self._max_min_recursive(numbers, low, mid)
        right_result = self._max_min_recursive(numbers, mid + 1, high)
        
        self.comparison_count += 2
        final_min = min(left_result.minimum, right_result.minimum)
        final_max = max(left_result.maximum, right_result.maximum)
        
        return MaxMinResult(final_min, final_max)
    
    def get_comparison_count(self) -> int:
        return self.comparison_count


class InputHandler:
    @staticmethod
    def get_numbers() -> List[int]:
        try:
            input_str = input("Enter numbers separated by spaces: ")
            numbers = [int(x.strip()) for x in input_str.split()]
            
            if not numbers:
                raise ValueError("No numbers provided")
            
            return numbers
        except ValueError as e:
            print(f"Error: {e}")
            return InputHandler.get_numbers()


class OutputHandler:
    @staticmethod
    def show_result(result: MaxMinResult, comparison_count: int):
        print(f"\nResult: {result}")
        print(f"Number of comparisons: {comparison_count}")


class MaxMinApp:
    def __init__(self, selector: MaxMinSelector):
        self.selector = selector
    
    def run(self):
        print("MaxMin Select Algorithm - Divide and Conquer")
        print("=" * 50)
        
        numbers = InputHandler.get_numbers()
        result = self.selector.find_max_min(numbers)
        
        comparison_count = 0
        if isinstance(self.selector, DivideConquerMaxMinSelector):
            comparison_count = self.selector.get_comparison_count()
        
        OutputHandler.show_result(result, comparison_count)


if __name__ == "__main__":
    selector = DivideConquerMaxMinSelector()
    app = MaxMinApp(selector)
    app.run()

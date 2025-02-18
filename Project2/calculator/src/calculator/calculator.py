class Calculator:
    def add(self, x: float, y: float) -> float:
        """Add two numbers."""
        return x + y
    
    def subtract(self, x: float, y: float) -> float:
        """Subtract y from x."""
        return x - y
    
    def multiply(self, x: float, y: float) -> float:
        """Multiply two numbers."""
        return x * y
    
    def divide(self, x: float, y: float) -> float:
        """Divide x by y."""
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y

def main() -> None:
    calc = Calculator()
    
    # Example calculations
    print("2 + 3 =", calc.add(2, 3))
    print("5 - 2 =", calc.subtract(5, 2))
    print("4 * 6 =", calc.multiply(4, 6))
    print("10 / 2 =", calc.divide(10, 2))

if __name__ == "__main__":
    main()

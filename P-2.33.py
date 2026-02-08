# [P-2.33] Write a Python program that inputs a polynomial in standard algebraic
# notation and outputs the first derivative of that polynomial.

from typing import Self
import re

class Polynomial:
  """
  Represents a polynomial and provides methods for differentiation and string formatting.
  """
  
  def __init__(self, polynomial_input: str | list[int | float]) -> None:
    """
    Initialize the Polynomial object.

    Args:
      polynomial_input: Either a string representing the polynomial 
                        (example: "x^2 + 2x + 4") or a list of coefficients 
                        where the index corresponds to the exponent 
                        (example: [4, 2, 1] for x^2 + 2x + 4).
    
    Raises:
      ValueError: If the string format is invalid.
      TypeError: If the input is neither a string nor a list.
    """
    if isinstance(polynomial_input, list):
      self._polynomial_list = polynomial_input
    elif isinstance(polynomial_input, str):
      try:
        self._polynomial_list = self._convert_polynomial_str_to_list(polynomial_input)
      except Exception as e:
        raise ValueError(f"Invalid polynomial string: {polynomial_input}") from e
    else:
      raise TypeError("Polynomial must be initialized with a string or a list of numbers.")

  def _convert_polynomial_str_to_list(self, polynomial_str: str) -> list[int | float]:
    """
    Parses a string representation of a polynomial into a list of coefficients.

    This method uses regular expressions to tokenize the input string, 
    identifying coefficients and exponents for each term.

    Args:
      polynomial_str: The algebraic string to parse.

    Returns:
      A list of floats/ints where index i holds the coefficient for x^i.
    """
    polynomial_str = polynomial_str.replace(" ", "")

    if not polynomial_str or polynomial_str == "0":
      return [0]

    coefficients = {}

    # Parse terms - find all matches
    # Pattern explanation:
    # [+-]?                : optional sign
    # (?:\d*\.?\d*)        : coefficient (optional, can be float)
    # x                    : literal 'x'
    # (?:\^(\d+))?         : optional exponent
    # |                    : OR
    # [+-]?\d+\.?\d* : constant term (with optional decimal)
    pattern = r'([+-]?(?:\d*\.?\d*))x(?:\^(\d+))?|([+-]?\d+\.?\d*)'
    position = 0

    while position < len(polynomial_str):
      match = re.match(pattern, polynomial_str[position:])
      if not match:
        raise ValueError(f"Invalid polynomial format at position {position}")

      full_match = match.group(0)

      if 'x' in full_match:
        coeff_str = match.group(1) or ''
        exp_str = match.group(2)

        if not coeff_str or coeff_str == '+':
          coeff = 1.0
        elif coeff_str == '-':
          coeff = -1.0
        else:
          coeff = float(coeff_str)

        exp = int(exp_str) if exp_str else 1

      else:
        coeff = float(match.group(3))
        exp = 0

      coefficients[exp] = coefficients.get(exp, 0) + coeff

      position += len(full_match)

    if not coefficients:
      return [0]

    max_degree = max(coefficients.keys())

    result = [0.0] * (max_degree + 1)
    for exp, coeff in coefficients.items():
      result[exp] = coeff

    return result

  def degree(self) -> int:
    """
    Returns the degree of the polynomial.
    
    The degree is defined as the highest exponent of x with a non-zero coefficient.
    """
    return len(self._polynomial_list) - 1

  def calculate_derivative(self) -> Self:
    """
    Computes the first derivative of the polynomial.

    Returns:
      A new Polynomial instance representing the first derivative.
    """
    if len(self._polynomial_list) <= 1:
      return Polynomial([0])

    derivative_list = [
      self._polynomial_list[i] * i 
      for i in range(1, len(self._polynomial_list))
    ]

    return Polynomial(derivative_list)

  def __str__(self) -> str:
    """
    Returns the string representation of the polynomial in standard algebraic form.
    """
    if not self._polynomial_list or all(coeff == 0 for coeff in self._polynomial_list):
      return "0"

    terms = []

    for degree in range(len(self._polynomial_list) - 1, -1, -1):
      coeff = self._polynomial_list[degree]
      if coeff == 0:
        continue

      sign = "-" if coeff < 0 else "+"
      abs_coeff = abs(coeff)

      if degree == 0:
        term = f"{abs_coeff}"
      elif degree == 1:
        term = "x" if abs_coeff == 1 else f"{abs_coeff}x"
      else:
        term = f"x^{degree}" if abs_coeff == 1 else f"{abs_coeff}x^{degree}"

      terms.append((sign, term))

    if not terms:
      return "0"

    first_sign, first_term = terms[0]
    result = f"-{first_term}" if first_sign == "-" else first_term

    for sign, term in terms[1:]:
      result += f" {sign} {term}"

    return result


test_cases = [
  "3x^2 - 2x + 4",
  "4 + 3x^2 - 2x",
  "x^2 + x",
  "3.5x^2 + 2.1x - 1",
  "0",
  "5",
  "x",
  " -x^3 + 2x",
  "0.5x^2",
  "-x +"
]

for test_str in test_cases:
  try:
    print(f"f(x) = {test_str}")
    polynomial = Polynomial(test_str)
    derivative = polynomial.calculate_derivative()
    print(f"f'(x) = {derivative}")
  except Exception as e:
    print(f"Exception: {e}")
  print()
  
polynomial_str = input(f'polynomial_str: ')
try:
  polynomial = Polynomial(polynomial_str)
  print(f"Derivative: {polynomial.calculate_derivative()}")
except Exception as e:
  print(f'Exception: {e}')
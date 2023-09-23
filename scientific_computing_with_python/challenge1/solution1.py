def format_single_problem(problem):
    """Returns a list containing: the first operand; the operator and the second operand; and the calculation result
       All numbers are right justified and the operand is left justified"""

    (operand1, operator, operand2) = problem.split()

    output_chars = max(len(operand1), len(operand2)) + 2

    if output_chars > 6:
        raise OperandTooLongError("Numbers cannot be more than four digits.")

    try:
        number1 = int(operand1)
        number2 = int(operand2)
    except ValueError:
        raise BadOperandError("Numbers must only contain digits.")
  
    if operator == '+':
        calculation_result = str(number1 + number2)
    elif operator == '-':
        calculation_result = str(number1 - number2)
    else:
        raise BadOperatorError("Operator must be '+' or '-'.")

    return [
             (output_chars - len(operand1)) * ' ' + operand1,
             operator + (output_chars - len(operand2) - 1) * ' ' + operand2,
             '-' * output_chars,
             (output_chars - len(calculation_result)) * ' ' + calculation_result,
    ]

def arithmetic_arranger(problems, show_solution=False):
    """Concatenates the results of format_single_problem into a nicely formatted string
       and returns error messages for exceptions"""

    if len(problems) > 5:
        return "Error: Too many problems."

    solution_elements = [[], [], [], []]

    for problem in problems:
        try:
            formatted_problem = format_single_problem(problem)
        except Exception as e:
            return "Error: " + e.msg
        for i in range(4):
            solution_elements[i].append(formatted_problem[i])

    lines = ["    ".join(elem) for elem in solution_elements]

    if show_solution:
        return " \n".join(lines)
    else:
        return " \n".join(lines[:3])

class BadOperatorError(SyntaxError):
   pass

class BadOperandError(SyntaxError):
   pass

class OperandTooLongError(SyntaxError):
   pass

if __name__ == "__main__":
    print(arithmetic_arranger(["2 + 2"], True))

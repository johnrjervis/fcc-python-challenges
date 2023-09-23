class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        padding = '*' * int((30 - len(self.name)) / 2)
        transactions = ""
        for transaction in self.ledger:
            transactions += f'{transaction["description"][:23]}{(23 - len(transaction["description"][:23])) * " "}'
            amt = f'{transaction["amount"]:.2f}'
            transactions += f'{(7 - len(amt[:7])) * " "}{amt[:7]}\n'
        return f'{padding}{self.name}{padding}\n{transactions}Total: {self.get_balance():.2f}'

    def deposit(self, amount, description=""):
        """Credit the acount with the supplied amount, which is logged in the ledger with the optional description"""
        self.ledger.append({"amount": amount, "description": description})

    def get_balance(self):
        """Returns current balance, which is calculated as the sum of the amounts of the transactions in the ledger """
        result = 0

        for entry in self.ledger:
            result += entry["amount"]

        return result

    def check_funds(self, amount):
        """Returns true if the current balance is sufficient for a withdrawal of the amount argument"""
        return amount <= self.get_balance()

    def withdraw(self, amount, description=""):
        """Makes a withdrawal of amount if the required funds are available and returns true if the withdrawal is successful"""
        if self.check_funds(amount):
            self.deposit(-amount, description)
            return True
        else:
            return False

    def transfer(self, amount, destinationCategory):
        """Transfers amount to another category if the required funds are available and returns true if the transfer is successful""" 
        is_successful_transfer = self.withdraw(amount, "Transfer to " + destinationCategory.name)

        if is_successful_transfer:
            destinationCategory.deposit(amount, "Transfer from " + self.name)

        return is_successful_transfer

def create_spend_chart(categories):
    """Creates an ASCII-style bar chart from the withdrawals of each of the category objects in the supplied categories list.
       The data is rounded down the the nearest 10%.
       To the left of the bar data is a vertical axis comprised of pipe characters with labels at intervals of 10%.
       The data is followed by a horizontal axis made of dashes, beneath which the name property of each category appears vertically"""

    category_withdrawals = []

    horizontal_axis = "    "
    for category in categories:
        horizontal_axis += "---"
        withdrawals_this_category = 0

        for entry in category.ledger:
            if entry["amount"] < 0 and entry["description"][:11] != "Transfer to":
               withdrawals_this_category += -entry["amount"]

        category_withdrawals.append(withdrawals_this_category)
    
    percentage_withdrawals = [value * 100 / sum(category_withdrawals) for value in category_withdrawals]

    result_lines = ["Percentage spent by category"]

    for i in range(100, -10, -10):
        if i == 100:
           vertical_axis_label = str(i)
        elif i < 100 and i > 0:
           vertical_axis_label = f' {i}'
        else:
           vertical_axis_label = f'  {i}'

        data = ''
        for percentage in percentage_withdrawals:

            if percentage >= i:
                data += " o "
            else:
                data += "   "

        result_lines.append(f'{vertical_axis_label}|{data} ')

    result_lines.append(f'{horizontal_axis}-')

    for i in range(max([len(category.name) for category in categories])):
        label_row = "    "
        for cat in categories:
            label_row += ' ' + get_letter_or_space(cat.name, i) + ' '
        result_lines.append(f'{label_row} ')

    return '\n'.join(result_lines)

get_letter_or_space = lambda word, index : word[index] if index < len(word) else ' '

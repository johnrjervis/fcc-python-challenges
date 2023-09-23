import unittest as ut
from unittest.mock import patch, call
from io import StringIO
from solution3 import *
import sys

def create_category_objects(name_list):
    """Turns a list of names into a list of category objects with the corresponding names"""
    return (Category(name) for name in name_list)

def create_two_categories():
    """Creates two arbitrarily-named categories"""
    return create_category_objects(["Cheese", "Biscuits"])

class CategoryTests(ut.TestCase):
    """Tests for the Category class"""

    def test_category_object_sets_name_property_from_initialisation_argument(self):
        newCategory = Category("test")

        self.assertEqual(newCategory.name, "test")

    def test_a_category_is_initialised_with_a_ledger_property_that_is_an_empty_list(self):
        newCategory = Category("test")

        self.assertEqual(newCategory.ledger, [])

    def test_deposit_method_enters_a_dict_with_an_amount_into_the_ledger_list_of_a_category_instance(self):
        newCategory = Category("test")

        newCategory.deposit(200)

        self.assertEqual(newCategory.ledger[0]["amount"], 200)

    def test_if_only_an_amount_is_passed_to_deposit_the_corresponding_description_in_the_ledger_is_empty(self):
        newCategory = Category("test")

        newCategory.deposit(200)

        self.assertEqual(newCategory.ledger[0]["description"], "")

    def test_a_description_that_is_passed_to_deposit_will_appear_in_the_corresponding_ledger_entry(self):
        newCategory = Category("test")

        newCategory.deposit(200, "Funds for testing")

        self.assertEqual(newCategory.ledger[0]["description"], "Funds for testing")

    def test_get_balance_returns_zero_if_no_transactions_have_been_made(self):
        newCategory = Category("test")

        self.assertEqual(newCategory.get_balance(), 0)

    def test_get_balance_returns_deposit_amount_if_only_transaction_is_a_single_deposit(self):
        newCategory = Category("test")

        newCategory.deposit(200, "Funds for testing")

        self.assertEqual(newCategory.get_balance(), 200)

    def test_get_balance_returns_total_deposit_amount_if_all_transactions_are_deposits(self):
        newCategory = Category("test")

        newCategory.deposit(200, "Funds for testing")
        newCategory.deposit(100, "Extra funds for more testing")

        self.assertEqual(newCategory.get_balance(), 300)

    def test_the_check_funds_method_returns_true_if_the_amount_argument_is_less_than_or_equal_to_the_available_balance(self):
        newCategory = Category("test")

        newCategory.deposit(200, "Funds for testing")

        self.assertTrue(newCategory.check_funds(199))
        self.assertTrue(newCategory.check_funds(200))

    def test_the_check_funds_method_returns_false_if_the_amount_argument_is_more_than_the_available_balance(self):
        newCategory = Category("test")

        newCategory.deposit(200, "Funds for testing")

        self.assertFalse(newCategory.check_funds(201))

    def test_the_withdraw_method_enters_a_the_negative_value_of_the_amount_argument_into_the_ledger(self):
        newCategory = Category("test")

        newCategory.deposit(200)
        newCategory.withdraw(100)

        self.assertEqual(newCategory.ledger[1]["amount"], -100)

    def test_the_withdraw_method_enters_an_empty_description_into_the_ledger_if_no_description_is_supplied(self):
        newCategory = Category("test")

        newCategory.deposit(200)
        newCategory.withdraw(100)

        self.assertEqual(newCategory.ledger[1]["description"], "")

    def test_the_withdraw_method_enters_a_description_into_the_ledger_if_one_is_supplied(self):
        newCategory = Category("Cheese")

        newCategory.deposit(200)
        newCategory.withdraw(100, "Purchase of Limburger")

        self.assertEqual(newCategory.ledger[1]["description"], "Purchase of Limburger")

    def test_get_balance_returns_correct_balance_for_a_combination_of_deposits_and_withdrawals(self):
        newCategory = Category("test")

        newCategory.deposit(200)
        newCategory.withdraw(50) 
        newCategory.withdraw(500) 
        newCategory.deposit(100)
        newCategory.withdraw(25) 
        newCategory.withdraw(10) 

        self.assertEqual(newCategory.get_balance(), 215)

    def test_the_withdraw_method_returns_true_if_the_transaction_is_successful(self):
        newCategory = Category("test")

        newCategory.deposit(200)

        self.assertTrue(newCategory.withdraw(100))

    @patch('solution3.Category.check_funds')
    def test_withdraw_calls_check_funds__with_the_supplied_amount_argument_to_ensure_transaction_is_possible(self, mock_check_funds):
        newCategory = Category("test")

        newCategory.withdraw(50)

        self.assertTrue(mock_check_funds.called)
        self.assertEqual(mock_check_funds.call_args, call(50))

    def test_the_withdraw_method_does_not_update_the_ledger_if_there_are_insufficient_funds_for_a_transaction(self):
        newCategory = Category("test")

        newCategory.withdraw(200)

        self.assertEqual(newCategory.ledger, [])

    def test_the_withdraw_method_returns_false_if_there_are_insuffient_funds_for_the_transaction(self):
        newCategory = Category("test")

        self.assertFalse(newCategory.withdraw(100))

    @patch('solution3.Category.withdraw')
    def test_the_transfer_method_calls_the_withdraw_method_with_the_supplied_amount_argument_and_a_description_of_the_transfer(self, mock_category_withdraw):
        (fromCategory, toCategory) = create_two_categories()
        fromCategory.deposit(200)
        toCategory.deposit(75)

        fromCategory.transfer(50, toCategory)

        self.assertTrue(mock_category_withdraw.called)
        """If withdraw is called with the correct arguments, the transfer should only take place if there are sufficient funds
           and the transaction amount and description should be correctly logged in the fromCategory's ledger"""
        self.assertEqual(mock_category_withdraw.call_args, call(50, "Transfer to Biscuits"))

    # Technically this is covered by the mock withdraw test above, but I wrote the test below first and have kept it as back up for the mock test
    def test_transfer_method_subtracts_transferred_funds_from_the_available_balance(self):
        (fromCategory, toCategory) = create_two_categories()
        fromCategory.deposit(200)

        fromCategory.transfer(75, toCategory)

        self.assertEqual(fromCategory.get_balance(), 125)

    def test_transferred_funds_are_added_to_the_balance_of_the_destination_Category(self):
        (fromCategory, toCategory) = create_two_categories()
        fromCategory.deposit(200)
        toCategory.deposit(75)

        fromCategory.transfer(50, toCategory)

        self.assertEqual(toCategory.get_balance(), 125)

    def test_transferred_funds_are_not_received_by_the_destination_Category_if_the_withdrawal_fails(self):
        (fromCategory, toCategory) = create_two_categories()
        fromCategory.deposit(100)
        toCategory.deposit(75)

        fromCategory.transfer(150, toCategory)

        self.assertEqual(toCategory.get_balance(), 75)

    def test_transfer_method_returns_true_if_transfer_takes_place(self):
        (fromCategory, toCategory) = create_two_categories()
        fromCategory.deposit(200)

        self.assertTrue(fromCategory.transfer(50, toCategory))

    def test_transfer_method_returns_false_if_transfer_does_not_take_place(self):
        (fromCategory, toCategory) = create_two_categories()
        fromCategory.deposit(25)

        self.assertFalse(fromCategory.transfer(50, toCategory))

    # Could replace this if mocks are used
    def test_transfer_is_described_in_source_ledger_as_transfer_to_destination_Category_name(self):
        (fromCategory, toCategory) = create_two_categories()
        fromCategory.deposit(200)

        fromCategory.transfer(75, toCategory)
        
        self.assertEqual(fromCategory.ledger[1]["description"], "Transfer to Biscuits") 

    def test_transfer_is_described_in_destination_ledger_as_transfer_from_source_Category_name(self):
        (fromCategory, toCategory) = create_two_categories()
        fromCategory.deposit(200)

        fromCategory.transfer(75, toCategory)
        
        self.assertEqual(toCategory.ledger[0]["description"], "Transfer from Cheese")

    def test_printing_a_category_with_no_transactions_outputs_a_heading_padded_with_asterisks_and_a_total(self):
        newCategory = Category("test")
        captured_output = StringIO()
        sys.stdout = captured_output

        print(newCategory)

        self.assertEqual(captured_output.getvalue(), "*************test*************\nTotal: 0.00\n")

    def test_printing_a_category_with_transactions_outputs_a_header_followed_by_a_list_of_its_transactions_and_a_total(self):
        (newCategory, toCategory) = create_two_categories()
        newCategory.deposit(200, "Cheese money")
        newCategory.withdraw(80, "Purchase of Edam")
        newCategory.transfer(75, toCategory)
        captured_output = StringIO()
        sys.stdout = captured_output

        print(newCategory)

        sys.stdout = sys.__stdout__

        self.assertEqual(captured_output.getvalue(), "************Cheese************\nCheese money            200.00\nPurchase of Edam        -80.00\nTransfer to Biscuits    -75.00\nTotal: 45.00\n")

class SpendChartTests(ut.TestCase):
    """Tests for the create_spend_chart function"""

    def test_the_first_line_returned_by_create_spend_chart_is_heading_text(self):
        newCategory = Category("test")
        newCategory.deposit(20)
        newCategory.withdraw(5)

        first_line_of_chart = create_spend_chart([newCategory]).split('\n')[0]

        self.assertEqual(first_line_of_chart, "Percentage spent by category")

    def test_all_text_lines_in_the_chart_have_three_characters_per_input_dataset_plus_five_extra_characters(self):
        (newCategory1, newCategory2) = create_two_categories()
        newCategory1.deposit(20)
        newCategory1.withdraw(5)

        # Use [1:] to remove the heading
        for line in create_spend_chart([newCategory1]).split('\n')[1:]:
            self.assertEqual(len(line), 8)
        for line in create_spend_chart([newCategory1, newCategory2]).split('\n')[1:]:
            self.assertEqual(len(line), 11)

    def test_the_eleven_rows_of_data_start_with_numbers_100_to_0_followed_by_a_pipe(self):
        newCategory = Category("Test")
        newCategory.deposit(20)
        newCategory.withdraw(5)

        spend_chart_lines = create_spend_chart([newCategory]).split('\n')

        # Data rows are 1 (=100%) to 11 (=0%)
        for i in range(1, 12):
            label_value = f'{(110 - (i * 10))}|'
            if i == 11:
                label_value = "  " + label_value
            elif i > 1:
                label_value = ' ' + label_value
            self.assertEqual(spend_chart_lines[i][:4], label_value)

    def test_create_spend_chart_returns_chart_with_one_bar_at_100_per_cent_when_supplied_with_one_category(self):
        newCategory = Category("Test")
        newCategory.deposit(20)
        newCategory.withdraw(5)

        spend_chart_lines = create_spend_chart([newCategory]).split('\n')

        for i in range(1, 12):
            self.assertEqual(spend_chart_lines[i][4:7], ' o ')

    def test_create_spend_chart_returns_two_bars_at_50_per_cent_for_two_categories_with_equal_withdrawals(self):
        # Helper function for creating bar charts?
        (newCategory1, newCategory2) = create_two_categories()
        newCategory1.deposit(20)
        newCategory1.withdraw(5)
        newCategory2.deposit(10)
        newCategory2.withdraw(3)
        newCategory2.withdraw(2)

        spend_chart_lines = create_spend_chart([newCategory1, newCategory2]).split('\n')

        for i in range(1, 12):
            if i < 6:
                self.assertEqual(spend_chart_lines[i][4:10], '      ')
            else:
                self.assertEqual(spend_chart_lines[i][4:10], ' o  o ')

    def test_bars_in_spend_chart_are_rounded_down_to_the_nearest_ten_percent(self):
        # Total withdrawals = 100, percentages should be a little over 50%, 30% and 10%
        (newCategory1, newCategory2, newCategory3) = create_category_objects(["Cheese", "Biscuits", "Wine"])
        newCategory1.deposit(80)
        newCategory1.withdraw(52)
        newCategory2.deposit(50)
        newCategory2.withdraw(33)
        newCategory3.deposit(20)
        newCategory3.withdraw(15)

        spend_chart_lines = create_spend_chart([newCategory1, newCategory2, newCategory3]).split('\n')

        for i in range(1, 6):
            self.assertEqual(spend_chart_lines[i][4:13], "         ")
        for j in range(6, 8):
            self.assertEqual(spend_chart_lines[j][4:13], " o       ")
        for k in range(9, 10):
            self.assertEqual(spend_chart_lines[k][4:13], " o  o    ")
        for l in range(10, 12):
            self.assertEqual(spend_chart_lines[l][4:13], " o  o  o ")

    def test_create_spend_chart_produces_chart_based_only_on_withdrawals_and_ignores_transfers(self):
        (newCategory1, newCategory2) = create_two_categories()
        newCategory1.deposit(20)
        newCategory1.withdraw(5)
        newCategory2.deposit(10)
        newCategory1.transfer(5, newCategory2)
        newCategory2.withdraw(3)
        newCategory2.withdraw(2)

        spend_chart_lines = create_spend_chart([newCategory1, newCategory2]).split('\n')

        for i in range(1, 12):
            if i < 6:
                self.assertEqual(spend_chart_lines[i][4:10], '      ')
            else:
                self.assertEqual(spend_chart_lines[i][4:10], ' o  o ')

    def test_a_horizontal_axis_that_consists_of_four_spaces_and_then_dashes_to_the_end_of_the_line_appears_beneath_the_bar_data(self):
        (newCategory1, newCategory2) = create_two_categories()
        newCategory1.deposit(20)
        newCategory1.withdraw(5)

        single_bar_chart_axis = create_spend_chart([newCategory1]).split('\n')[12]
        self.assertEqual(single_bar_chart_axis, "    ----")
        double_bar_chart_axis = create_spend_chart([newCategory1, newCategory2]).split('\n')[12]
        self.assertEqual(double_bar_chart_axis, "    -------")

    def test_get_letter_or_space_returns_the_correct_letter_for_an_index_less_than_the_word_length(self):
        self.assertEqual(get_letter_or_space("test", 1), 'e')

    def test_get_letter_or_space_returns_a_space_for_an_index_greater_than_or_equal_to_the_word_length(self):
        self.assertEqual(get_letter_or_space("test", 4), ' ')
        self.assertEqual(get_letter_or_space("test", 5), ' ')

    def test_category_names_should_be_displayed_beneath_graph_as_labels(self):
        (newCategory1, newCategory2, newCategory3) = create_category_objects(["Cheese", "Biscuits", "Wine"])
        newCategory1.deposit(80)
        newCategory1.withdraw(52)
        newCategory2.deposit(50)
        newCategory2.withdraw(33)
        newCategory3.deposit(20)
        newCategory3.withdraw(15)

        spend_chart_lines = create_spend_chart([newCategory1, newCategory2, newCategory3]).split('\n')

        expected_labels = [
            "     C  B  W  ",
            "     h  i  i  ",
            "     e  s  n  ",
            "     e  c  e  ",
            "     s  u     ",
            "     e  i     ",
            "        t     ",
            "        s     ",
        ]

        for i in range(len(expected_labels)):
            self.assertEqual(spend_chart_lines[i+13], expected_labels[i])

if __name__ == "__main__":
    ut.main()

import unittest
from service.Service import Service
from service.ServiceExceptions import *
from domain.BoardExceptions import *

class TestService(unittest.TestCase):

    def execute(self):
        
        '''
        test_service = Service(5, 5)

        #self.assertEqual(test_service.printable_board(), '+---+---+---+---+---+\n| 1 | 2 | 3 | 4 | 5 |\n+===+===+===+===+===+\n| \x00  | \x00  | \x00  | \x00  | \x00  |\n+---+---+---+---+---+\n| \x00  | \x00  | \x00  | \x00  | \x00  |\n+---+---+---+---+---+\n| \x00  | \x00  | \x00  | \x00  | \x00  |\n+---+---+---+---+---+\n| \x00  | \x00  | \x00  | \x00  | \x00  |\n+---+---+---+---+---+\n| \x00  | \x00  | \x00  | \x00  | \x00  |\n+---+---+---+---+---+')
        
        test_service.push_to_col(1)
        test_service.push_to_col(2)
        test_service.push_to_col(4)
        test_service.computer_push_to_col()

        test_service.check_draw()
        self.assertEqual(test_service.check_winner(), None)

        test_service.push_to_col(1)
        test_service.push_to_col(1)
        test_service.computer_push_to_col()

        self.assertEqual(test_service.check_winner(), None)

        test_service.push_to_col(5)
        test_service.push_to_col(5)
        test_service.push_to_col(5)
        test_service.computer_push_to_col()

        self.assertEqual(test_service.check_winner(), None)

        test_service.push_to_col(3)
        test_service.push_to_col(3)
        test_service.push_to_col(3)
        test_service.push_to_col(3)

        self.assertEqual(test_service.check_winner(), '\u26A1')

        test_service.push_to_col(2)
        test_service.push_to_col(2)
        test_service.push_to_col(2)
        test_service.push_to_col(2)
        test_service.push_to_col(4)
        test_service.push_to_col(4)
        test_service.push_to_col(4)
        test_service.push_to_col(4)
        test_service.push_to_col(1)
        test_service.push_to_col(5)

        with self.assertRaisesRegex(ColumnOverflowException, 'This column is full!'):
            test_service.push_to_col(5)
        
        with self.assertRaisesRegex(InvalidColumnException, 'Entered column is out of bounds!'):
            test_service.push_to_col(6)

        with self.assertRaisesRegex(DrawException, 'Draw!'):
            test_service.check_draw()

            '''

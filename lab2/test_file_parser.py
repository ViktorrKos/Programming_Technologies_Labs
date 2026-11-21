# test_file_parser.py
"""
Ізолювання логіки коду модульних тестів за допомогою підставних (фіктивних) об'єктів (mock).
Розділ 1: Моки для читання/запису файлів (unittest.mock.mock_open, patch).
"""

import unittest
from unittest.mock import patch, mock_open

def file_parser(*args):
    """
    Функція, яку тестуємо. Вона відкриває файл, рахує або замінює один текст у
    файлі на інший та записує дані знову у файл (залежно від параметрів).
    """
    cnt = 0
    data = None
    if len(args) >= 2:
        file_name, expr = args[0], args[1]
        with open(file_name, "r") as f:
            data = f.readlines()
        cnt = sum([el.count(expr) for el in data])
    if len(args) == 3 and data and cnt != 0:
        new_expr = args[2]
        new_data = [el.replace(expr, new_expr) for el in data]
        with open(file_name, "w") as f:
            f.writelines(new_data)
    return f'Found {cnt} strings'


class ParserTest(unittest.TestCase):
    def setUp(self):
        # Попередні присвоєння значень змінним, що далі буде використано у тестах
        self.file_content_mock = """Hello World!!
Hello World is in a file.
A mocked file.
He is not real mocked.
But he thinks he is.
Mocked File is here.
"""
        self.fake_file_path = "file/path/mock"
        self.input_values = ['mocked', 'Mocked File', 'is not there']
        self.output_values = [2, 1, 0]

    def test_count_expressions(self):
        """Тест підрахунку входжень підрядків у файл за допомогою mock_open"""
        # target динамічно враховує спосіб запуску (прямий або через test runner)
        target = f"{__name__}.open" if __name__ != '__main__' else '__main__.open'
        with patch(target, new=mock_open(read_data=self.file_content_mock)) as _file:
            for i in range(0, len(self.input_values)):
                with self.subTest(el=self.input_values[i]):
                    actual = file_parser(self.fake_file_path, self.input_values[i])
                    self.assertEqual(f'Found {self.output_values[i]} strings', actual)
                    _file.assert_called_with(self.fake_file_path, 'r')

    def test_count_replacings(self):
        """Тест заміни рядків у файлі та перевірка виклику запису writelines"""
        target = f"{__name__}.open" if __name__ != '__main__' else '__main__.open'
        with patch(target, new=mock_open(read_data="replace test place to place")) as _file:
            old_expr = "place"
            new_expr = "union"
            # Примітка: у рядку 'replace test place to place' підрядок 'place' зустрічається 3 рази
            # (1 раз у 'replace' та 2 рази окремо). Тому count('place') == 3.
            expected = 3
            actual = file_parser(self.fake_file_path, old_expr, new_expr)
            self.assertEqual(f'Found {expected} strings', actual)
            _file.assert_called_with(self.fake_file_path, 'w')
            _file().writelines.assert_called_once_with(["replace test place to place".replace(old_expr, new_expr)])

    def test_empty_file(self):
        """Тест обробки порожнього файлу"""
        target = f"{__name__}.open" if __name__ != '__main__' else '__main__.open'
        with patch(target, new=mock_open(read_data="")) as _file:
            old_expr = 'some expr'
            new_expr = 'new expr'
            expected = 0
            actual = file_parser(self.fake_file_path, old_expr, new_expr)
            self.assertEqual(f'Found {expected} strings', actual)
            _file.assert_called_with(self.fake_file_path, 'r')

    @unittest.expectedFailure
    def test_manual_bug_expected_failure_demo(self):
        target = f"{__name__}.open" if __name__ != '__main__' else '__main__.open'
        with patch(target, new=mock_open(read_data="replace test place to place")) as _file:
            # Тут очікуємо 2 (помилкове значення з методички), тому тест гарантовано зазнає невдачі
            actual = file_parser(self.fake_file_path, "place", "union")
            self.assertEqual("Found 2 strings", actual)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

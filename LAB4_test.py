import unittest
from unittest.mock import patch, mock_open
from LAB4_Master import NotesStackApp
from junit_xml import TestSuite, TestCase
import os

class TestNotesStackApp(unittest.TestCase):

    def setUp(self):
        self.app = NotesStackApp()

    def test_add_note_success(self):
        # Тест на успішне додавання нотатки
        with patch("builtins.input", return_value="Test note"):
            self.app.add_note()
        self.assertIn("Test note", self.app.stack)

    def test_add_empty_note(self):
        # Тест на додавання порожньої нотатки
        with patch("builtins.input", return_value=""):
            with patch("builtins.print") as mock_print:
                self.app.add_note()
                mock_print.assert_any_call("Помилка: Нотатка не може бути порожньою!")
        self.assertEqual(len(self.app.stack), 0)

    def test_remove_note_success(self):
        # Тест на успішне видалення нотатки
        self.app.stack = ["Test note 1", "Test note 2"]
        with patch("builtins.print") as mock_print:
            self.app.remove_note()
            mock_print.assert_any_call("Видалено: Test note 2")
        self.assertNotIn("Test note 2", self.app.stack)

    def test_remove_note_empty_stack(self):
        # Тест на спробу видалити нотатку з порожнього стеку
        self.app.stack = []
        with patch("builtins.print") as mock_print:
            self.app.remove_note()
            mock_print.assert_any_call("Помилка: Стек порожній, нічого видаляти!")

    def test_view_notes(self):
        # Тест на перегляд нотаток
        self.app.stack = ["Test note 1", "Test note 2"]
        with patch("builtins.print") as mock_print:
            self.app.view_notes()
            mock_print.assert_any_call("Ваші нотатки:")
            mock_print.assert_any_call("Test note 2")
            mock_print.assert_any_call("Test note 1")

    def test_view_notes_empty_stack(self):
        # Тест на перегляд порожнього стеку
        self.app.stack = []
        with patch("builtins.print") as mock_print:
            self.app.view_notes()
            mock_print.assert_any_call("Стек порожній!")

    def test_clear_notes(self):
        # Тест на очищення нотаток
        self.app.stack = ["Test note 1", "Test note 2"]
        with patch("builtins.print") as mock_print:
            self.app.clear_notes()
            mock_print.assert_any_call("Всі нотатки очищено.")
        self.assertEqual(len(self.app.stack), 0)

    def test_save_notes_success(self):
        # Тест на успішне збереження нотаток у файл
        self.app.stack = ["Test note 1", "Test note 2"]
        with patch("builtins.open", mock_open()) as mock_file:
            with patch("builtins.print") as mock_print:
                self.app.save_notes()
                mock_file.assert_called_once_with("notes.txt", "w")
                mock_file().write.assert_any_call("Test note 1\n")
                mock_file().write.assert_any_call("Test note 2\n")
                mock_print.assert_any_call("Нотатки успішно збережені у файл notes.txt!")

    def test_save_notes_empty_stack(self):
        # Тест на спробу збереження порожнього стеку
        self.app.stack = []
        with patch("builtins.print") as mock_print:
            self.app.save_notes()
            mock_print.assert_any_call("Немає нотаток для збереження!")

if __name__ == '__main__':
    # Створюємо директорію для звітів, якщо вона не існує
    if not os.path.exists('test-reports'):
        os.makedirs('test-reports')

    # Запускаємо тести і створюємо звіт у форматі XML
    test_cases = []
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestNotesStackApp)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Додаємо результати тестів у XML-звіт
    for test, outcome in zip(suite, result.failures + result.errors + result.skipped):
        test_case = TestCase(test[0].id())
        if outcome in result.failures:
            test_case.add_failure_info(outcome[1])
        elif outcome in result.errors:
            test_case.add_error_info(outcome[1])
        test_cases.append(test_case)

    ts = TestSuite("my test suite", test_cases)
    with open('test-reports/results.xml', 'w') as f:
        TestSuite.to_file(f, [ts], prettyprint=True)

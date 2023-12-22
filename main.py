import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit

s = '''
zéro
un deux trois quatre cinq six sept huit neuf dix
onze douze treize quatorze quinze seize dixsept dixhuit dixneuf
'''
d = {
    'vingt': 20,
    'trente': 30,
    'quarante': 40,
    'cinquante': 50,
    'soixante': 60,
    'soixante-dix': 70,
    'quatre-vingt': 80,
    'quatre-vingt-dix': 90,
    'cent': 100,
    'cents': 100,
    'mille': 1000,
}
DIGITS = {k: v for v, k in enumerate(s.strip().split())}
DIGITS.update(d)


def number_to_name(number, case=False):
    if number < 11:
        return 'единичного формата' if case else 'единичный формат'
    elif 10 < number < 20:
        return 'формата 11-19' if case else 'формат 11-19'
    elif 19 < number < 100:
        return 'десятичного формата' if case else 'десятичный формат'
    elif number > 99:
        return 'числа формата сотен' if case else 'число формата сотен'


def get_error_for_incorrect_order(prev_number, number):
    return f'{number_to_name(number)} следует после {number_to_name(prev_number, True)}'


def convert_text(number_text):
    number_text = ' '.join(number_text.split())
    segments = number_text.replace(' et un', '-un').replace(' et onze', '-onze').replace('dix-', 'dix').split()
    print(segments)
    numbers = []
    for segment in segments:
        number = DIGITS.get(segment, segment)
        print('  number:', number)
        if not isinstance(number, int):
            parts = number.split('-')
            if len(parts) > 1:
                if segment.startswith('quatre-vingt'):
                    parts = ['quatre-vingt', parts[2]]

                number = DIGITS.get(parts[0]) + DIGITS.get(parts[1])

        if not isinstance(number, int):
            return f'Неизвестное слово: {number}'

        numbers.append(number)

    for index, number in enumerate(numbers):
        if number in [100] and index > 0:
            prev_number = numbers[index - 1]
            if number == 100 and (prev_number > 9 or prev_number == 0):
                return get_error_for_incorrect_order(prev_number, number)

            numbers[index] *= prev_number
            numbers[index - 1] = 0
        elif index > 0:
            prev_number = numbers[index - 1]
            if prev_number < 10:
                return get_error_for_incorrect_order(prev_number, number)
            elif prev_number < 20:
                return get_error_for_incorrect_order(prev_number, number)
            elif prev_number < 100 and number > 9:
                return get_error_for_incorrect_order(prev_number, number)


    print(numbers)
    return sum(numbers)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Конвертация французских числительных в число')
        button = QPushButton('Конвертировать')
        button.clicked.connect(self.convert_and_show_text)

        layout = QVBoxLayout()
        input_field = QLineEdit()
        self.input_field = input_field
        input_field.setPlaceholderText('Введите числительное текстом')

        output_label = QLabel()
        self.output_label = output_label
        layout.addWidget(input_field)
        layout.addWidget(QLabel('Результат:'))
        layout.addWidget(output_label)
        layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def convert_and_show_text(self):
        number_text = self.input_field.text().strip()
        try:
            number = convert_text(number_text) if number_text else 'не указан ввод'
        except Exception:
            number = 'неизвестная ошибка'

        self.output_label.setText(str(number) if isinstance(number, int) else f'Ввод некорректен из-за "{number}"')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()

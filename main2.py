from bs4 import BeautifulSoup
import re

def typograph(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')

    def is_word_char(c):
        return c.isalnum() or c in '_'

    def replace_quotes(text):
        result = ''
        stack = []
        i = 0
        length = len(text)

        while i < length:
            char = text[i]
            if char == '"':
                prev_char = text[i - 1] if i > 0 else ''
                next_char = text[i + 1] if i + 1 < length else ''

                # Определяем, является ли кавычка открывающей или закрывающей
                if not stack or (not is_word_char(prev_char) and is_word_char(next_char)):
                    # Открывающая кавычка
                    if len(stack) % 2 == 0:
                        # Внешняя кавычка
                        result += '«'
                        stack.append('«')
                    else:
                        # Внутренняя кавычка
                        result += '„'
                        stack.append('„')
                else:
                    # Закрывающая кавычка
                    if stack:
                        open_quote = stack.pop()
                        if open_quote == '«':
                            result += '»'
                        elif open_quote == '„':
                            result += '”'
                        else:
                            result += '»'
                    else:
                        # Нет открывающей кавычки, считаем как открывающую
                        result += '«'
                        stack.append('«')
                i += 1
            else:
                result += char
                i += 1

        # Закрываем незакрытые кавычки
        while stack:
            open_quote = stack.pop()
            if open_quote == '«':
                result += '»'
            elif open_quote == '„':
                result += '”'

        return result

    def process_text(text):
        text = re.sub(r' - ', ' — ', text)
        text = replace_quotes(text)
        return text

    for element in soup.find_all(string=True):
        if element.parent.name not in ['script', 'style']:
            element.replace_with(process_text(element))

    return str(soup)

html_input = '"d" "d" "d" "d "d"" "d" "d" "d"' * 1000
html_output = typograph(html_input)
print(html_output)

html_input = '<h1>"Стоимость такого решения на 30-40% дешевле покупки в рознице", - сказал Шестаков.</h1><p class="kek" style="color: red">""Победа", "Аэрофлот" и "Россия" останется или уйдет? Ценник Norwind в два раза выше", - написала в группе аэропорта Кургана пользователь Юлия Зинченко.</p>'
html_output = typograph(html_input)
print(html_output)

from bs4 import BeautifulSoup
import re

QUOTE_CHAR = '"'

def replace_quotes(text):
    # Флаг для чередования кавычек
    open_quote = True

    # Функция для замены кавычек поочередно
    def replace(match):
        nonlocal open_quote
        if open_quote:
            open_quote = False
            return '„'  # Открывающая кавычка
        else:
            open_quote = True
            return '“'  # Закрывающая кавычка

    # Заменяем каждую кавычку " поочередно
    return re.sub(r'"', replace, text)


def typograph(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')

    def process_text(text):
        # Замена дефисов на длинные тире
        text = re.sub(r'(?<=\s)-(?=\s)', '—', text)

        # Поиск первой и последней кавычки
        r_quote = text.find(QUOTE_CHAR)  # индекс первой кавычки
        l_quote = text.rfind(QUOTE_CHAR)  # индекс последней кавычки

        # Проверяем, есть ли кавычки
        if r_quote != -1 and l_quote != -1 and r_quote != l_quote:
            # свапаем на «»
            text = text[:r_quote] + '«' + text[r_quote + 1:]
            text = text[:l_quote] + '»' + text[l_quote + 1:]

            # Выделяем текст между первой и последней кавычкой
            quote_section = text[r_quote + 1:l_quote + 1]

            # Применяем функцию замены кавычек только к этому фрагменту
            replaced_section = replace_quotes(quote_section)

            # Собираем строку заново с изменённой частью
            text = text[:r_quote + 1] + replaced_section + text[l_quote + 1:]

        return text

    # Применяем типограф ко всем текстовым узлам
    for element in soup.find_all(string=True):
        if element.parent.name not in ['script', 'style']:  # Игнорируем <script> и <style>
            # Преобразование только текстовых полей
            new_text = process_text(element)
            # print(new_text)
            element.replace_with(new_text)

    return str(soup)

html_input = '''<h1>"Стоимость такого решения на 30-40% дешевле покупки в рознице", - сказал Шестаков.</h1><p class="kek" style="color: red">""Победа" останется или уйдет? Ценник Norwind в два раза выше", - написала в группе аэропорта Кургана пользователь Юлия Зинченко.</p>'''


result = typograph(html_input)
print(result)

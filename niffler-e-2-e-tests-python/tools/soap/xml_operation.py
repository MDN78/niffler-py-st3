from xml.etree import ElementTree

# Определение пространств имен
namespaces = {
    'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
    'ns2': 'niffler-userdata'
}


def safe_find_text(element, path, namespaces=None, default=None):
    """
    Функция извлечения текста из XML-элемента.
    - Ищет элемент по указанному пути (path)
    - Если элемент найден, возвращает его текст
    - Если элемент не найден, возвращает значение по умолчанию (default)
    """
    elem = element.find(path, namespaces)
    return elem.text if elem is not None else default


def current_user_result_operation(xml_str: str):
    """
    Функция для парсинга XML-данных, полученных из SOAP-сервиса
    :param xml_str: xml строка
    :return: словарь с данными пользователя
    """
    root = ElementTree.fromstring(xml_str)
    user = root.find('.//ns2:user', namespaces)
    user_data = {
        'id': safe_find_text(user, 'ns2:id', namespaces),
        'username': safe_find_text(user, 'ns2:username', namespaces),
        'fullname': safe_find_text(user, 'ns2:fullname', namespaces),
        'currency': safe_find_text(user, 'ns2:currency', namespaces),
        'friendshipStatus': safe_find_text(user, 'ns2:friendshipStatus', namespaces)
    }
    return user_data

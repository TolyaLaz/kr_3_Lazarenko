import json
import os
import datetime as dt


def json_read(filename):
    """читает json файл"""
    with open(filename) as file:
        return json.load(file)


def filter_operation(operation_list):
    """функция отсеивает в json файле операции без EXECUTED"""
    filtered_list = []
    for operation in operation_list:
        if operation.get('state') == 'EXECUTED':
            filtered_list.append(operation)
    return filtered_list


def sort_operation(operation_list):
    """функция сортирует список по дате с ближайшего к последнему"""
    sorted_list = sorted(operation_list, key=lambda x: x['date'], reverse=True)
    return sorted_list


def mask_operation_from(operation):
    """функция маскирует номер карты или счета отправителя"""
    operation_from = operation.get('from')
    if operation_from:
        parts = operation_from.split(' ')
        last_number = parts[-1]
        if len(last_number) == 16:
            masked_number = f"{last_number[:4]} {last_number[4:6]}** **** {last_number[-4:]} ->"
            return f"{' '.join(parts[:-1])} {masked_number}"
        else:
            return f"Счет **{last_number[-4:]} ->"
    return "Без номера ->"


def mask_operation_to(operation):
    """функция маскирует номер счета получателя"""
    operation_to = operation.get('to')
    if operation_to:
        parts = operation_to.split(' ')
        last_number = parts[-1]
        return f"Счет **{last_number[-4:]}"


def format_date(operation):
    """функция форматирует строку в json файле в формат datetime и выводит в нужный формат строкой"""
    date = operation['date']
    # dt_time = dt.datetime.strptime(date, __format="%Y-%m-%dT%H:%M:%S.%f")
    dt_time = dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
    return dt_time.strftime("%d.%m.%Y")



absolute_path = os.path.abspath('/home/anatoliy/PycharmProjects/kr_3_Lazarenko/operations.json')
reading = json_read(absolute_path)
filter_json = filter_operation(reading)
sorting = sort_operation(filter_json)
for i in sorting[:5]:
    print(f'{format_date(i)} {i["description"]}')
    print(f'{mask_operation_from(i)} {mask_operation_to(i)}')
    print(f'{i["operationAmount"]["amount"]} {i["operationAmount"]["currency"]["name"]}\n')

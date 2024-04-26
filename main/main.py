import os, json

l = []  # Создание временного листа
files = os.listdir('transactions')  #
for i in files:  # Цикл по всем файлам
    f = open(f"{'transactions'}/{i}")  # Открытие и считывание файлов из директории
    l.append(json.loads(f.read()))  # Добавление файлов во временной хранилиище
blocks = l.copy()  # Для удобства меняем название
for i in l:  # Цикл по всем "блокам"
    if i['hash'].startswith('000') and i['hash'].endswith('000'):  # Первое задание
        print(f"№1. блок: {i['hash']}", f"номер: {i['index']}", f"автор: {i['transactions'][-1]['to']}",
              sep='\n')  # Вывод результата первого задания
        break
blocks = sorted(blocks, key=lambda x: x['index'])  # Сортируем все блоки по индексу
forks = []  # создаём массив для форков
for block in range(len(blocks) - 1):  # Идём циклом по всем блокам, кроме последнего
    if blocks[block]['index'] - blocks[block + 1][f'index'] == 0:  # Сравнение каждого элемента со следующим
        forks.append(blocks[block])  # Если два элемента подряд имеют одинаковые индексы, то добавляем в массив форков
start_fork = forks[0]  # Первый форк
next_fork = None  # Следующий форк
forks_info = []  # Массив с краткой информацией по форкам
for fork in range(len(forks) - 1):  # Считываем все форки циклом
    if forks[fork]['index'] - forks[fork + 1]['index'] != -1:  # Если индекс форка не равен индексу форк следующего
        forks_info.append((start_fork['index'], forks[fork]['index']))  # Добавляем информацию о "цепочке" в массив
        start_fork = forks[fork + 1]  # Меняем положение начального форка
else:
    forks_info.append((start_fork['index'], forks[-1]['index']))

len_of_forks = map(lambda x: x[1] - x[0] + 1, forks_info)  # вычисление длины "цепочки" форка
len_of_forks = sorted(len_of_forks)  # сортировка
naim = 0  # наименьшее
naib = ''  # наибольшее
for i in forks_info:
    if (i[1] - i[0] + 1) == 2:  # ищем минимальный элемент
        naim = i[0]  # меняем значение наименьшего
    if i[1] - i[0] + 1 == len_of_forks[-1]:  # ищем максимальный элемент
        naib = i  # меняем зачение наибольшего

print("№2. Длина наименьшего форка: ", len_of_forks[0])
print("№3. Номер первого блока в форке наименьшей длины: ", naim)
print("№4. Длина наибольшего форка: ", len_of_forks[-1])
l = []  # временый массив
for i in blocks:  # цикл по блокам
    if naib[0] <= i['index'] <= naib[1]:  # Ищем самую длинную "цепочку" форка
        l.append(i)  # добавляем во временый массив
# sorted by timestamp
for_five_info = sorted(forks_info, key=lambda x: x[1] - x[0])
for_five_forks = list(filter(lambda x: for_five_info[-1][0] <= x['index'] <= for_five_info[-1][1], blocks))
max_hash_temp = sorted(for_five_forks, key=lambda x: x['timestamp'])[-1]
print("№5. Хэш последнего блока в отброшенной ветке форка наибольшей длины: ",
      max_hash_temp['pre_hash'])  # Исходя из задания и шаблона
print("№6. Количество форков: ", len(len_of_forks))
for i in blocks:
    if i['index'] == 71:
        print("№7. Размер вознаграждения за создание блока #71: ", i['transactions'][-1]['value'])

only_indexes = []
for_values = []
dict_values = dict()
for i in blocks:
    if i['index'] not in only_indexes:
        only_indexes.append(i['index'])  # Добавляем индексы всех блоков, кроме форков
        for_values.append(i)  # Добавляем все значения, кроме форков

for i in for_values:
    value = i['transactions'][-1]['value']  # для упрощения работы со словарём
    if value not in dict_values:  # стандартный счётчик элементов для вычисления награждения
        dict_values[value] = 1
    else:
        dict_values[value] += 1

nums = list(dict_values.values())[2:-1]  # срез для вычисления "правильного" периода
print("№8. Период сокращения размера вознаграждения за создание блока (каждые n блоков):", nums[0])

list_for_coef = (list(dict_values.keys())[2:-1])  # массив значений (для вычисления коэффциента)
kd = round(list_for_coef[1] / list_for_coef[0], 2)  # вычисления коэффициента
val = list_for_coef[-1]
schet = len(list_for_coef)
while (round(val, 2) != round(0.09, 2)):
    val *= kd
    schet += 1

print("№9. Коэффициент сокращения вознаграждения за выработку блока:", kd)
print("№10. № блока, в котором в будущем размер вознаграждения впервые окажется равен 0,09:", schet * 17)

secret_info_list = []
temp_ind = []
temp_secret = []
for i in blocks:
    if len(i['secret_info']) != 0:  # Если существует секретная информация
        secret_info_list.append(str(i['secret_info']))  # Добавляем секретную информаицю
        temp_ind.append(i['index'])  # Добавляем индекс
print("№11. Блоки, в которых в поле secret_info встречается дополнительная информация: ", *temp_ind)
print("№12. Secret info в порядке её появления: ", " ".join(secret_info_list))
print("№13. Шестнадцатеричная форма представления ключевой строки: ", bytes.fromhex("".join(secret_info_list)).decode('utf-8'))


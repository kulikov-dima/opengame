# OpenGame-OpenFork 
### Open-source парсер stopgame.ru
<img src="assets/stopgame-logo.png" width="150">

# Возможности
 * Выводить список игр по жанру/категории и экспортировать в CSV
 * Сохранять списки платформ в CSV
 * Сохранять списки жанров в CSV
# Библиотеки
 * Requests
 * BeautifulSoup4
 * ArgParse
 * logging
 * dataclasses
# Установка и проверка
 1. Для установки зависимостей необходимо выполнить
    ```shell
    pip install -r requirements.txt 
    ```
 2. Готово! Теперь можно вызвать справку.
      ```shell
      python main.py --help 
      ```
# Использование
 * Для вызова справки необходимо запустить программу с флагом -h или --help
     ```shell
    python main.py --help
     ```
 * Чтобы обновить списки тегов и платформ необходимо выполнить
     ```shell
     python main.py update
     ```
 * Чтобы показать списки игр с первой страницы необходимо сделать
     ```shell
     python main.py -v games
     ```
   #### Важно, перед выводом/экспортом списка игр необходимо сделать `python main.py update`
 * Чтобы отфильтровать списки игр по платформе надо добавить флаг --platforms
     ```shell
     python main.py -v games --platforms "Linux"
     ```
   Также можно совмещать несколько платформ, например
   ```shell
   python main.py -v games --platforms "Linux" "Sony PlayStation 5"
   ```
 * Чтобы отфильтровать по жанру нужно сделать сделать
   ```shell
   python main.py -v games --genres "Мод"
   ```
 *  Также можно объединять как в случае с platforms
    ```shell
    python main.py -v games --genres "Мод" "Стратегия"
    ```
 * Флаги можно комбинировать
   ```shell
   python main.py -v games --genres "Мод" "Стратегия" --platforms "Linux" "Sony PlayStation 5"
   ```
 * Чтобы экспортировать в csv нужно сделать
   ```shell
   python main.py -v games --out "output.csv"
   ```
# Ограничения 
   Чтобы не ложить сервера stopgame при каждой попытке распарсить сайт, в программе есть ограничения на скорость отправки запросов
   При каждой отправке запроса перед отправкой мы ждём 0.5 секунд из-за этого программа долго работает
   
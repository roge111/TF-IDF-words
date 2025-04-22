# TF-IDF-words

Привет. В данном репозитории представлено решение задачи на тему "TF-IDF". Надеюсь, будет интересно! 😉

# Задание

Начнем по постановки самой задачи

```
Реализовать веб-приложение. В качестве интерфейса сделать страницу с формой для загрузки текстового файла, после загрузки и обработки файла отображается таблица с 50 словами с колонками:

слово
tf, сколько раз это слово встречается в тексте
idf, обратная частота документа
Вывод упорядочить по уменьшению idf.


Задание необходимо опубликовать на github.com, либо gitlab.com.

Если увлечётесь тестовым заданием, то можно сделать постраничный вывод и любые улучшения на ваше усмотрение.
```
Касемо термино:
`tf` - это частота слова к количесву слов
`idf` - это логорифм от частоного деления количесвта документов на количество документов с определнным словом
 На изображении ниже можно увидеть формулы 

![](https://myslide.ru/documents_7/c49b05d8f35511b2b7111dadc1e79a8a/img13.jpg)

Однако формулировка задачи говорит то, что пользователь загружает один файл. А значит у всех `idf` будет одинаковым. Но нам надо слова в первую очередь сортировать по `idf`. Представим, что одна строка = один абзец. Сооттвественно, `количество документов` = `количество абзацев`. 

### Алгоритм
---
1) Front принимает файл, отправляет его post-запросом.
2) Файл принимается Backend и отправляет на обработку.
3) Считываем всё из файла, разделяя текст по `\n`, чтобы разделить абзацы.
4) Перебираем абзацы.
5) В каждом абзаце удаляем все символы, кроме английских и российских букв и цифр.
6) Разбиваем абзац на слова по пробелам.
7) Перебираем слова, считая количество слов в абзаце и количество абзацев с этим словом.
8) Считаем tf и idf по отдельности.
9) Объединяем всё в одну структуру и отдаём в HTML.
10) Выводим всё в таблице.
Ну теперь давай посомтрим на каод. И начнем мы с frontend. Но важно, посомотри в конце инструкцию по запуску из `VS Code` на `Windows`.

### index.html
---

`index.html` - файл с оформлением страницы, на которой будет кнопка выбора файла, отправки, а потом и таблица

```
    <div class="container">
        <h2>Анализ TF-IDF</h2>
        <form id="upload-form">
            <div class="form-group">
                <label for="file-input">Выберите текстовый файл:</label>
                <input type="file" id="file-input" name="file" required>
            </div>
            <button type="submit" class="btn">Анализировать</button>
        </form>

        <table id="results-table" style="display: none;">
            <thead>
                <tr>
                    <th>Слово</th>
                    <th>TF</th>
                    <th>IDF</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>
    </div>
```

Это основной код для отображения кнопок «Все» и приема файла. Затем к типу `submit` будет привязана функция JS для отправки все на серверную часть и приема результата обратно. Также в этом участке содержится оформление таблицы. Теперь перейдем к скрипту, отвечающему за обработку и отправку запроса.
```
document.getElementById('upload-form').addEventListener('submit', async function (e) {
            e.preventDefault();

            const fileInput = document.getElementById('file-input');
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);

            const response = await fetch('http://127.0.0.1:8000/tf_idf', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                alert("Ошибка при анализе файла");
                return;
            }

            const data = await response.json();

            const table = document.getElementById('results-table');
            const tbody = table.querySelector('tbody');
            tbody.innerHTML = '';

            for (const [word, stats] of Object.entries(data)) {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${word}</td>
                    <td>${stats.tf.toFixed(4)}</td>
                    <td>${stats.idf.toFixed(4)}</td>
                `;
                tbody.appendChild(row);
            }

            table.style.display = 'table';
        });
```

`fileInput` — тут мы получаем файл с элемента с `id` = `file-input`.
`fromData` — массив, в который мы кладем наш файл.
```
const response = await fetch('http://127.0.0.1:8000/tf_idf', {
                method: 'POST',
                body: formData
            });
```

Тут мы передаем запрос по адресу `http://127.0.0.1:8000/tf_idf`, где `http://127.0.0.1:8000` — это адрес, по которому запускается файл FastAPI с портом `8000`, а `/tf_idf` — это уже адрес самой функции, которая принимает запрос.

```
if (!response.ok) {
                alert("Ошибка при анализе файла");
                return;
            }
```
Здесь мы обрабатываем ошибку, если возникла ошибка, то выведет сообщение. Это может быть связано с соединением или некорректной работой функции.

```const data = await response.json();

            const table = document.getElementById('results-table');
            const tbody = table.querySelector('tbody');
            tbody.innerHTML = '';
```
Тут мы получаем ответ программы на Python и парсим его. 
`table` - ищет элемент с `id` = `results-table`. Это и есть наша таблица. Колонки там записаны в таком порядке: `word`, `tf`, `idf`.
`tbody` - тело таблицы, куда будут подставляться значения

```
for (const [word, stats] of Object.entries(data)) {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${word}</td>
                    <td>${stats.tf.toFixed(4)}</td>
                    <td>${stats.idf.toFixed(4)}</td>
                `;
                tbody.appendChild(row);
            }
```

Тут мы уже заполняем данными. `toFixed(4)` — округление значения до 4-х знаков после запятой. 

За саму подстановку отвечает код ниже:

```
<td>${word}</td>
<td>${stats.tf.toFixed(4)}</td>
<td>${stats.idf.toFixed(4)}</td>
```

Ну а за стили у нас отвечает файл `index.css`, который располагается в `/frontend/styles`.

### Серверная часть
---

Теперь, после разбора Frontend части, перейдем к основной программе. Она располагается в папке `/backend` и разделена на два файла: `FileUp` — программа, которая принимает запрос, `FileProcessing` — файл с классом `FileProcessing`, который содержит реализацию алгоритма вычисления параметров для каждого из слов.

И пройдем по порядку. Начнем с программы, которая принимает у нас запрос

## FileUp
---

Как я сказал, тут реализована функция, что принимает запрос. Для работы с запросами я использую `FastAPI`

Посмотрим на то, что мы ипортируем

```
from FileProcessing import FileProcessing
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
```

`FileProcessing` — класс, который содержит функцию для вычисления параметров для каждого из слов.
`FastAPI` — класс для приема запросов.
`UploadFile` — инструмент, который позволяет принять файл из запроса.
`FileResponse` — класс, который позволяет указать, из какого файла мы принимаем запрос.
`CORSMiddleware` — класс, который позволяет дать разрешение для портов, с которых мы будем принимать запрос.

```
app = FastAPI()

file_process = FileProcessing()
```

Тут мы создаем объекты классов `FastAPI` и `FileProcessing`.

```
@app.get("/")
def root():
    return FileResponse('frontend/index.html')
```

Тут мы указываем, откуда мы принимаем запрос. 
`@app.get("/")` — мы устанавливаем точку, начиная с какой папки мы можем принимать проекты. В данном случае `"/"` — мы принимаем запросы из всех файлов корневой папки проекта и файлов из дочерних папок. 

```
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)
```
Тут мы даем разарешения на запросы с портов `5500` по адресам: `http://127.0.0.1` и `http://localhost`. Почему так? Я запускаю проект из `Visual Studio Code`, который использует `Live Server`,  который в свою очередь делает запуск по умолчанию с порта `5500`, а так как файл с программой запускается с порта `8000`, то мыдолжны дать разрешение для порта `5500`. 

```
@app.post("/tf_idf")
async def file_processing(file: UploadFile = File(...)):
    # Передаем файл напрямую в функцию tfidf
    tf, idf = file_process.tfidf(file)
    
    word_info = {}
    for key in tf:
        word_info[key] = {
            'tf': tf[key],
            'idf': idf[key]
        }
    return dict(list(sorted(word_info.items(), key=lambda x: x[1]['idf'], reverse=True))[:50])

```

Тут мы принимаем сам запрос, отправляем на обработку и возвращаем единую хеш-таблицу. `@app.post("/tf_idf")` — это метка для функции, что она принимает запросы метода `POST` и находится по адресу `tf_idf`. Конечно, полный адрес — `http://127.0.0.1:8000/tf_idf`. С помощью `tfidf` из класса `FileResponse` мы обрабатываем файл. В итоге функция возвращает две хеш-таблицы: первая с колонками `word` и `tf`, а вторая — `word` и `idf`. И эти таблицы подставляются в `tf` и `idf`. А в `word_info` мы объединяем в одну хеш-таблицы типа `word: {'tf': значение, 'idf': значение}`. 

```
return dict(list(sorted(word_info.items(), key=lambda x: x[1]['idf'], reverse=True))[:50])
```

А тут мы возвращаем таблицу, отсортированную по значению `idf` в порядке убывания. И из отсортированного набора мы оставляем только первые 50 слов (согласно ТЗ).

## FileProcessing

Это класс для основной обработки файла.

```
def _clean_text(self, text: str) -> list[str]:
        text = re.sub(r'[^a-zA-Z0-9 \u0400-\u04FF]', '', text).lower().split()
        return text
```
Данная функция `_clean_text` является приватной для данного класса и принимает текст. Затем она удаляет из него все символы, кроме пробелов, цифр, английских и русских букв, а также разделеяем текст на список слов.
```
 def tfidf(self, upload_file):
        content = upload_file.file.read().decode('utf-8')
        #content = upload_file.read()
        document = content.split("\n")

        count_files = {}
        count_doc = 0
        tf_hash = {}
        idf_hash ={}
        for text in document:
            count_doc += 1
            words = self._clean_text(text)
            hash_count_word = {}
            
            for word in words:

                if word not in hash_count_word:
                    hash_count_word[word] = 1
                else:
                    hash_count_word[word] += 1

                if word not in count_files:
                    count_files[word] = 1
                elif hash_count_word[word] < 2:
                    count_files[word] += 1
            
            for key in hash_count_word:
                if key in tf_hash:
                    tf_hash[key] += hash_count_word[key]/len(text)
                else:
                    tf_hash[key] = hash_count_word[key]/len(text)
        
        for key in count_files:
            idf_hash[key] = math.log(count_doc/count_files[key])
        
        return tf_hash, idf_hash
```

Эта функция и обарабтывает текст

```
content = upload_file.file.read().decode('utf-8')
document = content.split("\n")

```

Тут мы чистаем текст, применяя кодировку `utf-8`, чтобы корректно считывать русские символы. `content` — содержит всё содержимое файла. `document` — содержит список из абзацев, которые разделены переносом на следующую строку `\n`.

```
        count_files = {}
        count_doc = 0
        tf_hash = {}
        idf_hash ={}
```

`count_files` — содержит таблицу, где ключ — это слово, а значение — количество документов, в котором данное слово встречается (документ = абзац).
`count_doc` — считает количество документов, но у нас документ = абзац.
`tf_hash` — таблица, где ключ — слово, а значение — это вычисленный `tf`.
`idf_hash` — то же самое, что и `tf_hash`, но тут значение — это `idf`.


```
        for text in document:
            count_doc += 1
            words = self._clean_text(text)
            hash_count_word = {}
```

Запускаем цикл, где `text` — это абзац из `document`. Тут мы увеличиваем `count_doc`, чистим текст от лишних символов и сохраняем в `word`. `hash_count_word` — таблица, где ключ — слово, а значение — количество данного слова в текущем абзаце. 

```
for word in words:
```
Запускаем цикл, `word` — это слово из списка слов `words`.

```
if word not in hash_count_word:
    hash_count_word[word] = 1
else:
    hash_count_word[word] += 1
```

Данная часть позволяет добавлять слова как ключи, если их нет, или увеличивать в них значение, если имеется. Это надо, так как если мы сделаем `+=` к ключу, которого еще нет, то мы получим в лоб ошибку. 😂

Тут я проверяю, если нет слова как ключа в `hash_count_word`, то добавляем со значением 1, в противном случае увеличиваем значение на 1, то есть это счетчик слов.

```
if word not in count_files:
    count_files[word] = 1
elif hash_count_word[word] < 2:
    count_files[word] += 1
```

Тут тоже самое, но мы увеличиваем на 1 только один раз, то есть если мы слово встретили меньше 2 раз (то есть 1-й раз), то увеличиваем. Все это в одном цикле `for word ...`.
```
for key in hash_count_word:
if key in tf_hash:
    tf_hash[key] += hash_count_word[key]/len(text)
else:
    tf_hash[key] = hash_count_word[key]/len(text)
```

Закончив цикл `for word...`, но не закончив `for text...`, мы обрабатываем данные по слову и записываем как значение частотное деления количества данного слова в абзаце на количество слов. Это и есть `tf`. Но общий параметр `tf` я сделал как сумму `tf` из каждого абзаца.

```
for key in count_files:
    idf_hash[key] = math.log(count_doc / count_files[key])
```

Закончив перебор абзацев, вычисляем `idf`. Для каждого слова мы берем логарифм частного от деления количества документов `count_doc` на количество документов, в которых данное слово встречается `count_files[key]`. 

Ну и возвращаем таблицы с `tf` и `idf`:
```
return tf_hash, idf_hash

```

Вот и весь алгоритм, который решает данную задачу. Давай узнаем, как запускать.

# Инструкция по запуску из Visual Studio Code на Windows

Чтобы запустить `html`, то мы открываем сам файл и в правом нижнем углу жмём `Go Live`.
Чтобы запустить файл программ на Python с `fastapi`, мы открываем командную строку. В Пуске вводим `cmd` и запускаем `Командная строка`. Используя `cd`, доходим до папки с программой. Например, `cd backend` зайдет в папку backend. Далее, дойдя до папки с программой, запускаем так: `python -m uvicorn FileUp:app --host 127.0.0.1 --port 8000`, где `--port 8000` мы и устанавливаем порт 8000, а хост — `--host 127.0.0.1`.

### Пример



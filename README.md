<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Запуск проекта</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
        }
        h1 {
            color: #333;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            font-family: Consolas, monospace;
            overflow-x: auto;
        }
        a {
            color: #007bff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Запуск проекта</h1>

    <p>Перед началом работы необходимо перейти в папку проекта:</p>
    <pre><code>cd ...\kirovenergo\kirovenergo_project</code></pre>

    <p>Запустите сервер разработки Django:</p>
    <pre><code>python manage.py runserver</code></pre>

    <p>После успешного запуска сервера интерфейс будет доступен по адресу:</p>
    <p><a href="http://127.0.0.1:8000/" target="_blank">http://127.0.0.1:8000/</a></p>
</body>
</html>

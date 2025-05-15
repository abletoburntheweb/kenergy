import os

# Путь к проекту
project_dir = r"C:\Users\79127\Desktop\pyprojects\kenergy"

# Поиск файлов с нулевыми байтами
for root, dirs, files in os.walk(project_dir):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                content = f.read()
                if b"\x00" in content:
                    print(f"Найден файл с нулевыми байтами: {file_path}")
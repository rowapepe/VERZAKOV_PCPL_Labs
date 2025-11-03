class Catalog:
    def __init__(self, id_catalog, name):
        self.id_catalog = id_catalog
        self.name = name

class File:
    def __init__(self, id_file, name, size, id_catalog):
        self.id_file = id_file
        self.name = name
        self.size = size
        self.id_catalog = id_catalog

class CatalogFile:
    def __init__(self, id_file, id_catalog):
        self.id_file = id_file
        self.id_catalog = id_catalog

catalogs = [
    Catalog(1, "Документы"),
    Catalog(2, "Изображения"),
    Catalog(3, "Видео")
]

files = [
    File(1, "Анализ.txt", 1250, 1),
    File(2, "Архив.zip", 8500, 1),
    File(3, "Фото.png", 3200, 2),
    File(4, "Видео.mp4", 7000, 3),
    File(5, "Приложение.apk", 900, 1)
]

catalog_files = [
    CatalogFile(1, 1),
    CatalogFile(2, 1),
    CatalogFile(3, 2),
    CatalogFile(3, 1),
    CatalogFile(4, 3),
    CatalogFile(5, 1),
]

def Task_1():
    result = []
    for f in files:
        if f.name.startswith("А"):
            for c in catalogs:
                if f.id_catalog == c.id_catalog:
                    result.append((f.name, c.name))
    return result

def Task_2():
    result = []
    for c in catalogs:
        file_sizes = [f.size for f in files if f.id_catalog == c.id_catalog]
        if file_sizes:
            result.append((c.name, min(file_sizes)))
    return sorted(result, key=lambda x: x[1])

def Task_3():
    result = []
    for cf in catalog_files:
        for f in files:
            for c in catalogs:
                if cf.id_file == f.id_file and cf.id_catalog == c.id_catalog:
                    result.append((f.name, c.name))
    return sorted(result, key=lambda x: x[0])

def main():
    print("Предметная область: Файл, Каталог файлов\n")

    res1 = Task_1()
    
    print("Задание В1. Файлы, начинающиеся с 'А':")
    for name, cat in res1:
        print(f"{name} — {cat}")
    
    res2 = Task_2()

    print("\nЗадание В2. Каталоги с минимальным размером файла:")
    for cat, size in res2:
        print(f"{cat}: {size} КБ")

    res3 = Task_3()

    print("\nЗадание В3. Файлы и каталоги (многие-ко-многим):")
    for file_name, cat_name in res3:
        print(f"{file_name} — {cat_name}")

if __name__ == "__main__":
    main()
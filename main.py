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

def get_files_starting_with(letter, files, catalogs):
    result = []
    for f in files:
        if f.name.startswith(letter):
            for c in catalogs:
                if f.id_catalog == c.id_catalog:
                    result.append((f.name, c.name))
    return result


def get_catalogs_with_min_file_size(files, catalogs):
    result = []
    for c in catalogs:
        sizes = [f.size for f in files if f.id_catalog == c.id_catalog]
        if sizes:
            result.append((c.name, min(sizes)))
    return sorted(result, key=lambda x: x[1])


def get_files_and_catalogs_many_to_many(files, catalogs, catalog_files):
    result = []
    for cf in catalog_files:
        for f in files:
            for c in catalogs:
                if cf.id_file == f.id_file and cf.id_catalog == c.id_catalog:
                    result.append((f.name, c.name))
    return sorted(result, key=lambda x: x[0])
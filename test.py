import unittest
from main import (Catalog, File, CatalogFile, get_files_starting_with,
    get_catalogs_with_min_file_size,
    get_files_and_catalogs_many_to_many)


class TestFileCatalogLogic(unittest.TestCase):
    def setUp(self):
        self.catalogs = [
            Catalog(1, "Документы"),
            Catalog(2, "Изображения"),
            Catalog(3, "Видео")
        ]

        self.files = [
            File(1, "Анализ.txt", 1250, 1),
            File(2, "Архив.zip", 8500, 1),
            File(3, "Фото.png", 3200, 2),
            File(4, "Видео.mp4", 7000, 3),
            File(5, "Приложение.apk", 900, 1)
        ]

        self.catalog_files = [
            CatalogFile(1, 1),
            CatalogFile(2, 1),
            CatalogFile(3, 2),
            CatalogFile(3, 1),
            CatalogFile(4, 3),
            CatalogFile(5, 1),
        ]

    def test_files_starting_with_A(self):
        result = get_files_starting_with("А", self.files, self.catalogs)
        expected = [
            ("Анализ.txt", "Документы"),
            ("Архив.zip", "Документы")
        ]
        self.assertEqual(result, expected)

    def test_min_file_size_by_catalog(self):
        result = get_catalogs_with_min_file_size(self.files, self.catalogs)
        expected = [
            ("Документы", 900),
            ("Изображения", 3200),
            ("Видео", 7000)
        ]
        self.assertEqual(result, expected)

    def test_many_to_many_relationship(self):
        result = get_files_and_catalogs_many_to_many(
            self.files, self.catalogs, self.catalog_files
        )
        expected = [
            ("Анализ.txt", "Документы"),
            ("Архив.zip", "Документы"),
            ("Видео.mp4", "Видео"),
            ("Фото.png", "Документы"),
            ("Фото.png", "Изображения"),
            ("Приложение.apk", "Документы")
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
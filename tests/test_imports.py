import unittest

import pyrulo.class_imports


class TestImports(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_whenImportClassesByDir_resultIsTheExpected(self):
        # arrange
        path = "test_classes"

        # act
        classes = pyrulo.class_imports.import_classes_by_dir(path, object, False)
        names = [cls.__name__ for cls in classes]
        counts = {}
        for name in names:
            counts.setdefault(name, 0)
            counts[name] += 1

        # assert
        self.assertIn("A", names)
        self.assertIn("B", names)
        self.assertIn("C", names)
        self.assertEqual(counts["A"], 1)
        self.assertEqual(counts["B"], 1)
        self.assertEqual(counts["C"], 1)

    def test_whenImportClassesByExternalDir_resultIsTheExpected(self):
        # arrange
        path = "C:/_cosas/Desarrollo/Proyectos/Python/propsettings/propsettings"

        # act
        classes = pyrulo.class_imports.import_classes_by_dir(path, object, False)
        names = [cls.__name__ for cls in classes]

        # assert
        self.assertIn("Setting", names)

    def test_whenImportClassFromFile_resultsIsTheExpected(self):
        # arrange
        path = "C:/_cosas/Desarrollo/Proyectos/Python/propsettings/propsettings/setting.py"

        # act
        classes = pyrulo.class_imports.import_classes_in_specific_script(path, object)
        names = [cls.__name__ for cls in classes]

        # assert
        self.assertIn("Setting", names)

    def test_whenImportClassFromFileByKey_resultsIsTheExpected(self):
        # arrange
        path = "C:/_cosas/Desarrollo/Proyectos/Python/propsettings/propsettings/setting.py"

        # act
        classes = pyrulo.class_imports.import_classes_in_specific_script(path, object)
        names = [cls.__name__ for cls in classes]

        # assert
        self.assertIn("Setting", names)


if __name__ == '__main__':
    unittest.main()

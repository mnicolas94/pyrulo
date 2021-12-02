import importlib
import inspect
import logging
import os
import pkgutil

import pyrulo.class_imports


if __name__ == '__main__':
    # path = "C:/_cosas/Desarrollo/Proyectos/Python/propsettings/propsettings/setting.py"
    # classes = pyrulo.class_imports.import_classes_in_specific_script(path, object)

    path = "test_classes"
    classes = pyrulo.class_imports.import_classes_in_dir(path, object)

    print(classes)

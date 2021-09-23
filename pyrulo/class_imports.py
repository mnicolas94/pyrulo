import importlib
import importlib.util
import inspect
import logging
import os.path
import pkgutil


_registered_classes = {}


def register_classes_dir_by_key(key, classes_dir: str, base_class: type, recursive: bool):
    if key in _registered_classes:
        logging.warning("Classes were registered with the same key already.")
    _registered_classes.setdefault(key, []).append((classes_dir, base_class, recursive))


def import_classes_by_key(key):
    classes = []
    if key in _registered_classes:
        registered_list = _registered_classes[key]

        for classes_dir, base_class, recursive in registered_list:
            imported_classes = import_classes_by_dir(classes_dir, base_class, recursive)
            for cls in imported_classes:
                if cls not in classes:
                    classes.append(cls)
    else:
        logging.warning(f"There are no classes registered with that key: {key}")
    return classes


def import_classes_in_specific_script_by_key(module_path: str, key):
    classes = []
    if key in _registered_classes:
        registered_list = _registered_classes[key]

        for _, base_class, _ in registered_list:
            imported_classes = import_classes_in_file(module_path, base_class)
            for cls in imported_classes:
                if cls not in classes:
                    classes.append(cls)
    else:
        logging.warning(f"There are no classes registered with that key: {key}")
    return classes


def import_classes_in_specific_script(module_path: str, base_class: type):
    classes = []
    imported_classes = import_classes_in_file(module_path, base_class)
    for cls in imported_classes:
        if cls not in classes:
            classes.append(cls)
    return classes


def import_classes_in_file(file_path, base_class):
    imported_module = importlib.util.spec_from_file_location("", file_path).loader.load_module()
    mod_classes = _import_module_classes(imported_module, base_class)
    classes = []
    for cls in mod_classes:
        _add_class_if_not_exists(classes, cls)

    return classes


def import_classes_by_dir(dir_path, base_class, recursive=True):
    """
    Importar las clases de los scripts que estén en un directorio.
    :param dir_path: directorio de los scripts.
    :param base_class: clase base de las clases que se desean importar.
    :param recursive: si se desea buscar también en los subdirectorios.
    :return:
    """
    classes = []

    absolute = os.path.abspath(dir_path)

    if '.' in absolute:
        logging.warning(f"Can't import modules from a directory with dot/s in it's path: {absolute}.")
        return classes

    for (modinfo, name, ispkg) in pkgutil.iter_modules([dir_path]):
        if not ispkg:
            imported_module = modinfo.find_spec(name).loader.load_module()
            mod_classes = _import_module_classes(imported_module, base_class)
            for cls in mod_classes:
                _add_class_if_not_exists(classes, cls)

    if recursive:
        for d in os.listdir(dir_path):
            subdir = os.path.join(dir_path, d)
            if os.path.isdir(subdir) and not subdir.endswith('__pycache__'):
                mod_classes = import_classes_by_dir(subdir, base_class, recursive)
                for cls in mod_classes:
                    _add_class_if_not_exists(classes, cls)
    return classes


def _import_module_classes(module, base_class):
    """
    Importar las clases de un módulo que hereden de una clase específica.
    :param module: dirección del módulo en string. e.g. mymodule.functions
    :param base_class: clase base de las clases que se desean importar.
    :return:
    """
    classes = set()
    for i in dir(module):
        attribute = getattr(module, i)
        if inspect.isclass(attribute) \
                and not inspect.isabstract(attribute) \
                and issubclass(attribute, base_class) \
                and attribute != base_class \
                and not issubclass(attribute, NotImport):
            classes.add(attribute)

    return classes


def _classes_are_equal(cls_A, cls_B):
    module1 = cls_A.__module__
    module2 = cls_B.__module__
    if module1.endswith(module2) or module2.endswith(module1):
        source1 = inspect.getsource(cls_A)
        source2 = inspect.getsource(cls_B)
        if source1 == source2:
            return True
    return False


def _add_class_if_not_exists(classes, new_class):
    exists = False
    for klass in classes:
        if _classes_are_equal(new_class, klass):
            exists = True
            break
    if not exists:
        classes.append(new_class)


class NotImport:
    """
    Esta clase es solo para "marcar" otras clases como no importables. Es decir, las clases que hereden de NotImport
    no serán importadas de manera dinámica por el método import_module_classes.
    """

    @staticmethod
    def notimport(clazz):
        """
        Este método funciona como decorador de clases para añadir a NotImport como clase base a una clase.

        Uso:

        @notimport
        class A(object):
            pass

        :param clazz:
        :return:
        """
        if inspect.isclass(clazz):
            clazz.__bases__ += (NotImport, )
        return clazz

import sys

from generalfile import Path
from generallibrary import EnvVar, VerInfo, join_with_str, deco_cache
from generallibrary.values import Crud


class Crud_EnvVar_PATH(Crud):
    delimiter = VerInfo().env_var_path_delimiter

    def set(self):
        self.obj.value = f"{self.instance.scripts_path()}{self.delimiter}{self.obj}"

    def unset(self):
        paths = [Path(path=path_str) for path_str in self.obj.value.split(self.delimiter)]
        paths.remove(self.instance.scripts_path())
        self.obj.value = join_with_str(delimiter=self.delimiter, obj=paths)


class Crud_EnvVar_VENV(Crud):
    def set(self):
        self.obj.value = self.instance.path

    def unset(self):
        self.obj.remove()


class Crud_sys_path(Crud):
    def set(self):
        self.obj.insert(0, str(self.value))

    def unset(self):
        value = str(self.value)
        if value in sys.path:
            sys.path.remove(value)


class Crud_Path_Lines(Crud):
    def _get_path_strings(self):
        return self.obj.text.read().splitlines()

    def _set_path_strings(self, path_strings):
        self.obj.text.write("\n".join(path_strings), overwrite=True)

    @staticmethod
    def _value_to_path(value):
        return str(Path(value).absolute()).lower()

    def set_value(self, value):
        path_str = self._value_to_path(value=value)
        path_strings = self._get_path_strings()
        if path_str in path_strings:
            return
        path_strings.append(path_str)
        self._set_path_strings(path_strings=path_strings)

    def unset_value(self, value):
        path_str = self._value_to_path(value=value)
        path_strings = self._get_path_strings()
        if path_str not in path_strings:
            return
        path_strings.remove(path_str)
        self._set_path_strings(path_strings=path_strings)


class _Venv_Cruds:
    @property
    @deco_cache()
    def cruds(self):
        """ :param generalpackager.Venv self: """
        class VenvCruds:
            EnvVar_PATH = Crud_EnvVar_PATH(obj=EnvVar("PATH"), value=self.scripts_path(), instance=self)
            EnvVar_VENV = Crud_EnvVar_VENV(obj=EnvVar("VIRTUAL_ENV"), value=self.path, instance=self)
            sys_path_scripts = Crud_sys_path(obj=sys.path, value=self.scripts_path(), instance=self)
            sys_path_site = Crud_sys_path(obj=sys.path, value=self.site_packages_path(), instance=self)
            Path_easy_install = Crud_Path_Lines(obj=self.easy_install_path(), instance=self)
        return VenvCruds



























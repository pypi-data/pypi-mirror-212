from generalpackager.api.localrepo.base.metadata import _Metadata
from generalpackager.api.shared.target import Targets, _SharedTarget, _TARGETS_LITERAL


class _LocalRepo_Target(_SharedTarget):
    """ Target of None is only for packages without a metadata.json file. """
    _cls_metadata = _Metadata
    _cls_target_classes = {}

    def __init_subclass__(cls, **kwargs):
        """ :param generalpackager.LocalRepo cls: """
        super().__init_subclass__(**kwargs)
        if cls.__name__ != cls._BASE_CLS_NAME:
            assert cls.target in Targets.field_values_defaults()
            assert cls._cls_metadata is not None
        cls._cls_target_classes[cls.target] = cls

    def targetted(self, target: _TARGETS_LITERAL):
        """ :param generalpackager.LocalRepo self: """
        return self._cls_target_classes[target](name=self.name, path=self.path)






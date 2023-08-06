class _SharedOwner:
    """ Shared by GitHub, PyPI and NPM. """
    DEFAULT_OWNER = ...

    # _recycle_keys = {"owner": lambda owner: _SharedOwner._scrub_owner(owner=owner)}
    _recycle_keys = {"owner": lambda cls, owner: cls._scrub_owner(owner=owner)}

    def __init__(self, owner=None):
        self.owner = self._scrub_owner(owner=owner)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        assert cls.DEFAULT_OWNER is not Ellipsis

    @classmethod
    def _scrub_owner(cls, owner):
        return owner or cls.DEFAULT_OWNER

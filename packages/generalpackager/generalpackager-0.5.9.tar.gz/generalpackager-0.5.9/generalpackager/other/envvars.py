
from generallibrary import EnvVar

GH_TOKEN = EnvVar("GH_TOKEN", "secrets.PACKAGER_GITHUB_API", skip_test_on_missing=True)
TWINE_USERNAME = EnvVar("TWINE_USERNAME", "secrets.TWINE_USERNAME", skip_test_on_missing=True)
TWINE_PASSWORD = EnvVar("TWINE_PASSWORD", "secrets.TWINE_PASSWORD", skip_test_on_missing=True)


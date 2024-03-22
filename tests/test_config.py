from pathlib import Path

from invoicetool.config import Config


def test_default_working_directory(config: Config):
    assert config.base_output_directory == Path.home() / ".invoicetool"


# def test_env_var_working_directory(monkeypatch, tmp_path):
#     monkeypatch.setenv("INVOICETOOL_WORKING_DIR", str(tmp_path))
#     assert get_working_directory() == tmp_path


# def test_config_overrides_default(config):
#     assert get_working_directory(config) == config.working_directory


# def test_env_var_overrides_config(monkeypatch, tmp_path, config):
#     monkeypatch.setenv("INVOICETOOL_WORKING_DIR", str(tmp_path))
#     assert get_working_directory(config) == tmp_path

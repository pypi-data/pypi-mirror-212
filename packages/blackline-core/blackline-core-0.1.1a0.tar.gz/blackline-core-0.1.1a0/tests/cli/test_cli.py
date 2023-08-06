from datetime import datetime
from pathlib import Path

from blackline.cli.cli import cli, echo_validation
from blackline.constants import DEFAULT_PROFILE
from blackline.models.validation import (
    CollectionValidation,
    DatasetCollectionValidation,
    FieldValidation,
)
from click.testing import CliRunner


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0


def test_cli_init(monkeypatch, tmp_path):
    def __init__(
        self, path, name, default_profile, catalogue, adapters, *args, **kwargs
    ):
        assert path == tmp_path
        assert name == "blackline"
        assert default_profile == DEFAULT_PROFILE
        assert catalogue == Path("catalogue")
        assert adapters == Path("adapters")

    monkeypatch.setattr("blackline.cli.cli.InitProject.__init__", __init__)
    monkeypatch.setattr("blackline.cli.cli.InitProject.init_project", lambda self: None)
    runner = CliRunner()
    result = runner.invoke(cli, ["init", "--project-dir", str(tmp_path)])
    assert result.exit_code == 0


def test_run(monkeypatch):
    def _deidentify(path, profile, start_date):
        assert path == Path("project")
        assert profile == "default"
        assert start_date == datetime(2023, 1, 1)

    monkeypatch.setattr("blackline.cli.cli.deidentify", _deidentify)
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "run",
            "--project-dir",
            "project",
            "--profile",
            "default",
            "--start-date",
            "2023-01-01",
        ],
    )
    assert result.exit_code == 0


def test_debug(monkeypatch, project_root, profile):
    def __init__(self, path, profile):
        self.path = path
        self.profile = profile

    def debug(self):
        assert self.path == project_root
        assert self.profile == profile
        return {"test_store_0": True, "test_store_1": False}

    monkeypatch.setattr("blackline.cli.cli.Debug.__init__", __init__)
    monkeypatch.setattr("blackline.cli.cli.Debug.debug", debug)

    def Validate__init__(self, *args, **kwargs):
        pass

    def validate_catalogue_dataset(self):
        return {
            "test_dataset": DatasetCollectionValidation(
                collections={
                    "test_collection": CollectionValidation(
                        name="test_collection",
                        fields={"test_field": FieldValidation(name="test_field")},
                    )
                },
            )
        }

    monkeypatch.setattr(
        "blackline.cli.cli.Validate.__init__",
        Validate__init__,
    )
    monkeypatch.setattr(
        "blackline.cli.cli.Validate.validate_catalogue_dataset",
        validate_catalogue_dataset,
    )
    runner = CliRunner()
    result = runner.invoke(
        cli, ["debug", "--project-dir", str(project_root), "--profile", profile]
    )

    assert result.exit_code == 0


def test_sample_run(project_root, monkeypatch, start_date):
    # Setup
    profile = "sample_profile"
    runner = CliRunner()

    # Run
    sample_result = runner.invoke(
        cli,
        [
            "sample",
            "--project-dir",
            str(project_root),
            "--default-profile",
            profile,
        ],
    )
    # Change directoy to project root
    monkeypatch.chdir(project_root)
    run_result = runner.invoke(
        cli,
        [
            "run",
            "--project-dir",
            str(project_root),
            "--profile",
            profile,
            "--start-date",
            start_date.strftime("%Y-%m-%d"),
        ],
    )
    assert sample_result.exit_code == 0
    assert run_result.exit_code == 0


def test_report(project_root, monkeypatch, start_date):
    # Setup
    profile = "sample_profile"
    runner = CliRunner()

    runner.invoke(
        cli,
        [
            "sample",
            "--project-dir",
            str(project_root),
            "--default-profile",
            profile,
        ],
    )

    result = runner.invoke(
        cli,
        [
            "report",
            "--project-dir",
            str(project_root),
        ],
    )
    assert result.exit_code == 0


def test_echo_validation():
    # Setup
    excs = {
        "test_dataset": DatasetCollectionValidation(
            name="test_dataset",
            collections={
                "test_collection": CollectionValidation(
                    name="test_collection",
                    fields={"test_field": FieldValidation(name="test_field")},
                )
            },
        )
    }

    # Run
    echo_validation(excs)

    # Assert
    assert True

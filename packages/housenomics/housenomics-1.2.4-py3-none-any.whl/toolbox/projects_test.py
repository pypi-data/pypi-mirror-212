import pytest
import toml

from toolbox.project import update_version_in_pyproject_toml


@pytest.fixture
def pyproject_toml_path(tmp_path):
    """
    Fixture to create a temporary pyproject.toml file for testing.
    """
    pyproject_toml_path = tmp_path / "pyproject.toml"
    pyproject_toml_path.touch()
    return pyproject_toml_path


def test_update_version_in_pyproject_toml(pyproject_toml_path):
    """
    Test updating the version in pyproject.toml file.
    """
    # Define a sample version
    version = "1.2.3"

    # Create a sample pyproject.toml content
    sample_toml_content = """
    [build-system]
    requires = ["poetry-core>=1.0.0"]
    build-backend = "poetry.core.masonry.api"

    [tool.poetry]
    name = "your-project"
    version = "0.1.0"
    description = "Your project description."
    authors = ["Your Name <youremail@example.com>"]
    license = "MIT"

    [tool.poetry.dependencies]
    python = "^3.9"

    [tool.poetry.dev-dependencies]
    pytest = "^6.2.2"
    """

    # Write the sample pyproject.toml content to the temporary file
    with open(pyproject_toml_path, "w") as f:
        f.write(sample_toml_content)

    # Call the function
    update_version_in_pyproject_toml(version, pyproject_toml_path)

    # Read the modified pyproject.toml file
    pyproject_toml = toml.load(pyproject_toml_path)

    # Check if the version has been updated correctly
    assert pyproject_toml["tool"]["poetry"]["version"] == version  # nosec

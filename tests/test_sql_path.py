from src.utilities import _render_sql_with_args
import pytest
def test_sql_render_happy(tmp_path):

    project = "test_project"
    dataset = "test_dataset"
    sql_file = tmp_path / "test.sql"
    sql_file.write_text("SELECT * FROM `${PROJECT}.${DATASET}.table`")
    result = _render_sql_with_args(sql_file, project, dataset)
    assert "test_project.test_dataset" in result
    assert result.startswith("SELECT * FROM")

def test_sql_render_raise():
    project = "test_project"
    dataset = "test_dataset"

    with pytest.raises(FileNotFoundError, match="SQL file not found"):
        _render_sql_with_args("raise_test/test.sql", project, dataset)

    
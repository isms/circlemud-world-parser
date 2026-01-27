import json
import shutil
import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from circlemud_world_parser import parse
from circlemud_world_parser.parse import app
from circlemud_world_parser.utils import parse_from_file


ASSETS_DIR = Path('assets').resolve()


@pytest.fixture
def assets_dir():
    """Fixture providing the path to the assets directory."""
    return ASSETS_DIR


@pytest.fixture
def cli_runner():
    """Fixture providing a Typer CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_assets_dir():
    """Fixture that copies all assets to a temp directory for CLI testing."""
    temp_dir = Path(tempfile.mkdtemp())
    shutil.copytree(ASSETS_DIR, temp_dir / 'assets')
    yield temp_dir / 'assets'
    shutil.rmtree(temp_dir)


def get_all_test_files():
    """Collect all test files grouped by type for parametrization."""
    test_files = []
    for file_type in parse.PARSER_LOOKUP:
        for filepath in (ASSETS_DIR / file_type).glob(f'*.{file_type}'):
            test_files.append((file_type, filepath))
    return test_files


def generate_test_ids():
    """Generate readable test IDs from file paths."""
    test_files = get_all_test_files()
    return [f"{file_type}/{Path(filepath).name}" for file_type, filepath in test_files]


@pytest.mark.parametrize("file_type,filepath", get_all_test_files(), ids=generate_test_ids())
def test_parse_individual_file(file_type, filepath):
    """Parse each tinyworld file individually and verify no unexpected errors."""
    parser_func, splitter = parse.PARSER_LOOKUP[file_type]
    payload, errors = parse_from_file(filepath, parser_func, splitter)

    filename = Path(filepath).name
    if filename == '0.obj':
        # This file has a known intentional error (bug object)
        assert len(errors) == 1
        expected = '0\nbug~\na bug~\nThis object is BAD!'
        assert expected in errors[0]['text']
    else:
        assert errors == [], f"Unexpected errors parsing {filepath}: {errors}"

    # Verify we got parseable results
    assert isinstance(payload, list)


@pytest.mark.parametrize("file_type", list(parse.PARSER_LOOKUP.keys()))
def test_parse_all_files_of_type(file_type, assets_dir):
    """Parse all files of a given type and verify aggregate behavior."""
    filenames = list((assets_dir / file_type).glob(f'*.{file_type}'))

    assert len(filenames) > 0, f"No files found for type {file_type}"

    total_parsed = 0
    for filepath in filenames:
        parser_func, splitter = parse.PARSER_LOOKUP[file_type]
        payload, errors = parse_from_file(filepath, parser_func, splitter)
        total_parsed += len(payload)

    assert total_parsed > 0, f"No items parsed for type {file_type}"


class TestCLIIntegration:
    """Integration tests for the CLI interface."""

    def test_cli_parse_mob_file(self, cli_runner, temp_assets_dir):
        """Test CLI parsing of a mob file outputs valid JSON."""
        mob_file = temp_assets_dir / 'mob' / '30.mob'
        result = cli_runner.invoke(app, [str(mob_file)])

        assert result.exit_code == 0, f"CLI failed: {result.output}"

        # Verify output is valid JSON
        output_data = json.loads(result.output)
        assert isinstance(output_data, list)
        assert len(output_data) > 0

        # Verify mob structure
        first_mob = output_data[0]
        assert 'id' in first_mob
        assert 'aliases' in first_mob

    def test_cli_parse_obj_file(self, cli_runner, temp_assets_dir):
        """Test CLI parsing of an object file outputs valid JSON."""
        obj_file = temp_assets_dir / 'obj' / '30.obj'
        result = cli_runner.invoke(app, [str(obj_file)])

        assert result.exit_code == 0, f"CLI failed: {result.output}"

        output_data = json.loads(result.output)
        assert isinstance(output_data, list)
        assert len(output_data) > 0

    def test_cli_parse_wld_file(self, cli_runner, temp_assets_dir):
        """Test CLI parsing of a world file outputs valid JSON."""
        wld_file = temp_assets_dir / 'wld' / '30.wld'
        result = cli_runner.invoke(app, [str(wld_file)])

        assert result.exit_code == 0, f"CLI failed: {result.output}"

        output_data = json.loads(result.output)
        assert isinstance(output_data, list)
        assert len(output_data) > 0

    def test_cli_parse_shp_file(self, cli_runner, temp_assets_dir):
        """Test CLI parsing of a shop file outputs valid JSON."""
        shp_file = temp_assets_dir / 'shp' / '30.shp'
        result = cli_runner.invoke(app, [str(shp_file)])

        assert result.exit_code == 0, f"CLI failed: {result.output}"

        output_data = json.loads(result.output)
        assert isinstance(output_data, list)
        assert len(output_data) > 0

    def test_cli_parse_zon_file(self, cli_runner, temp_assets_dir):
        """Test CLI parsing of a zone file outputs valid JSON."""
        zon_file = temp_assets_dir / 'zon' / '30.zon'
        result = cli_runner.invoke(app, [str(zon_file)])

        assert result.exit_code == 0, f"CLI failed: {result.output}"

        output_data = json.loads(result.output)
        assert isinstance(output_data, list)
        assert len(output_data) > 0

    def test_cli_output_to_file(self, cli_runner, temp_assets_dir):
        """Test CLI can write output to a file."""
        mob_file = temp_assets_dir / 'mob' / '30.mob'
        output_file = temp_assets_dir / 'output.json'

        result = cli_runner.invoke(app, [str(mob_file), '--dest', str(output_file)])

        assert result.exit_code == 0, f"CLI failed: {result.output}"

        # Verify file was created and contains valid JSON
        assert output_file.exists()
        with open(output_file) as f:
            output_data = json.load(f)
        assert isinstance(output_data, list)
        assert len(output_data) > 0

    def test_cli_invalid_file_type(self, cli_runner, temp_assets_dir):
        """Test CLI handles unknown file types gracefully."""
        # Create a file with unknown extension
        bad_file = temp_assets_dir / 'test.xyz'
        bad_file.write_text('test content')

        result = cli_runner.invoke(app, [str(bad_file)])

        assert result.exit_code != 0

    @pytest.mark.parametrize("file_type", list(parse.PARSER_LOOKUP.keys()))
    def test_cli_parse_all_files_of_type(self, cli_runner, temp_assets_dir, file_type):
        """Test CLI can parse all files of each type."""
        filenames = list((temp_assets_dir / file_type).glob(f'*.{file_type}'))

        for filepath in filenames:
            filename = filepath.name

            # Skip the known bad file
            if filename == '0.obj':
                continue

            result = cli_runner.invoke(app, [str(filepath)])

            assert result.exit_code == 0, f"CLI failed for {filepath}: {result.output}"

            # Verify valid JSON output
            output_data = json.loads(result.output)
            assert isinstance(output_data, list)

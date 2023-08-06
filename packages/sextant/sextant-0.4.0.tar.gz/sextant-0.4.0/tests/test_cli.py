"""Tests for the ChartsCollection and Chart classes"""
import shutil
import tempfile

from contextlib import contextmanager

import pytest
import yaml

from sextant import cli

from . import fixtures


def _get_chartscollection(basedir) -> cli.ChartsCollection:
    return cli.ChartsCollection(basedir, f"{basedir}/charts")


@pytest.fixture(name="collection")
def chartscollection() -> cli.ChartsCollection:
    """Get the test chartscollection."""
    return _get_chartscollection(fixtures)


@contextmanager
def chart_in_temp_dir(chartname):
    tmp = tempfile.mkdtemp()
    new_fixtures = f"{tmp}/fixtures"
    try:
        shutil.copytree(fixtures, new_fixtures)
        collection = _get_chartscollection(new_fixtures)
        yield collection.chart(chartname)
    finally:
        shutil.rmtree(tmp)


def test_collection(collection: cli.ChartsCollection):
    """Test that collection works."""
    # All charts should've been loaded
    assert len(list(collection.charts())) == 3
    assert isinstance(collection.chart("good"), cli.Chart)


def test_query(collection: cli.ChartsCollection):
    """Test that querying works."""
    assert collection.query("bar.beer:1.0.0")[0].chart_dir == collection.chart("good").chart_dir
    assert collection.query("some.other:1.1.1") == []
    # only exact matches
    assert collection.query("bar.beer:1.0") == []
    # bad charts cannot be loaded
    assert collection.query("baz.drunk-unicorn:1.0") == []


def test_lock():
    """Test that a lockfile is created"""
    with chart_in_temp_dir("good") as good:
        good.create_lock(force=False)
        assert good.package.lockfile.exists()
        good.package.lockfile.unlink()


def test_vendor():
    """Test that we can create the vendor directory and fill it"""
    with chart_in_temp_dir("good") as good:
        assert not good.vendor_dir.exists()
        good.vendor(force=False)
        assert good.vendor_dir.is_dir()
        assert_chart_version(good, "0.0.2")


def assert_chart_version(chart, desired_version):
    """Verify version of a chart."""
    chart_data = yaml.safe_load(chart.chart_yaml.read_text())
    assert chart_data["version"] == desired_version


def test_vendor_chart_bump():
    """Test that no change to vendoring means no version bump in the chart."""
    with chart_in_temp_dir("good") as good:
        assert not good.vendor_dir.exists()
        good.vendor(force=False)
        assert_chart_version(good, "0.0.2")
        good.vendor(force=False)
        assert_chart_version(good, "0.0.2")
        good.vendor(force=True)
        assert_chart_version(good, "0.0.2")
        # Now we truncate a vendored file.
        tampered = good.chart_dir / good.BUNDLE_DIR / "bar" / "beer_1.0.0.tpl"
        tampered.write_text("some garbage")
        good.vendor(force=True)
        # Vendoring with force=True recreated the file.
        # Sextant should've detected it and bumped chart version.
        assert_chart_version(good, "0.0.3")


def test_set_arbitrary_version():
    """Test we can set an arbitrary version."""
    with chart_in_temp_dir("good") as good:
        good.bump_chart_version("1.0.0")
        assert_chart_version(good, "1.0.0")
        with pytest.raises(ValueError):
            good.bump_chart_version("0.8.1")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
from pathlib import Path

import pytest

from clickgen.packagers import WindowsPackager, XPackager
from tests.utils import create_test_cursor


def test_XPackger(image_dir: Path) -> None:
    """Test the ``clickgen.packagers.XPackager`` functionality."""
    XPackager(image_dir, theme_name="test", comment="testing")

    cur_theme = image_dir / "cursor.theme"
    idx_theme = image_dir / "index.theme"

    assert cur_theme.exists() is True
    assert idx_theme.exists() is True

    with cur_theme.open() as f:
        assert f.readlines() == ["[Icon Theme]\n", "Name=test\n", 'Inherits="test"']

    with idx_theme.open() as f:
        assert f.readlines() == [
            "[Icon Theme]\n",
            "Name=test\n",
            "Comment=testing\n",
            'Inherits="hicolor"',
        ]


def test_WindowsPackager_empty_dir_exception(image_dir: Path) -> None:
    """Testing ``clickgen.packagers.WindowsPackager`` raise the empty directory \
    exception with exception type **FileNotFoundError**.
    """
    with pytest.raises(FileNotFoundError) as excinfo:
        WindowsPackager(
            image_dir, theme_name="test", comment="testing", author="Unknown"
        )

    assert (
        str(excinfo.value)
        == f"Windows cursors '*.cur' or '*.ani' not found in '{image_dir}'"
    )


def test_WindowsPackager_missing_cur_exception(image_dir: Path) -> None:
    """Testing ``clickgen.packagers.WindowsPackager`` raise the missing cursors \
    exception with exception type **FileNotFoundError**.
    """
    create_test_cursor(image_dir, "Work.ani")
    create_test_cursor(image_dir, "Busy.ani")
    create_test_cursor(image_dir, "Default.cur")
    create_test_cursor(image_dir, "Help.cur")
    create_test_cursor(image_dir, "Link.cur")
    create_test_cursor(image_dir, "Move.cur")
    create_test_cursor(image_dir, "Diagonal_2.cur")
    create_test_cursor(image_dir, "Vertical.cur")
    create_test_cursor(image_dir, "Horizontal.cur")
    create_test_cursor(image_dir, "Diagonal_1.cur")
    create_test_cursor(image_dir, "Handwriting.cur")
    create_test_cursor(image_dir, "Cross.cur")
    create_test_cursor(image_dir, "IBeam.cur")
    with pytest.raises(FileNotFoundError) as excinfo:
        WindowsPackager(
            image_dir, theme_name="test", comment="testing", author="Unknown"
        )

    assert (
        str(excinfo.value)
        == "Windows cursors are missing ['Alternate', 'Unavailiable']"
    )


def test_WindowsPackager_with_semi_animated_cursors(
    tmpdir_factory: pytest.TempdirFactory,
) -> None:
    """Testing ``clickgen.packagers.WindowsPackager`` supports 'semi-animated' \
    cursors.

    This test generates all .ani (animated) cursors and passed them to \
    **WindowsPackager**. And checks, It generates valid ``install.inf`` file \
    with appropriate cursor-type or not.
    """

    d = Path(tmpdir_factory.mktemp("test_image"))
    create_test_cursor(d, "Work.ani")
    create_test_cursor(d, "Busy.ani")
    create_test_cursor(d, "Default.ani")
    create_test_cursor(d, "Help.ani")
    create_test_cursor(d, "Link.ani")
    create_test_cursor(d, "Move.ani")
    create_test_cursor(d, "Diagonal_2.ani")
    create_test_cursor(d, "Vertical.ani")
    create_test_cursor(d, "Horizontal.ani")
    create_test_cursor(d, "Diagonal_1.ani")
    create_test_cursor(d, "Handwriting.ani")
    create_test_cursor(d, "Cross.ani")
    create_test_cursor(d, "IBeam.ani")
    create_test_cursor(d, "Unavailiable.ani")
    create_test_cursor(d, "Alternate.ani")

    WindowsPackager(d, theme_name="test", comment="testing", author="Unknown")

    install_file = d / "install.inf"

    assert install_file.exists() is True
    data = install_file.read_text()

    assert "Work.ani" in data
    assert "Busy.ani" in data
    assert "Default.ani" in data
    assert "Help.ani" in data
    assert "Link.ani" in data
    assert "Move.ani" in data
    assert "Diagonal_2.ani" in data
    assert "Vertical.ani" in data
    assert "Horizontal.ani" in data
    assert "Diagonal_1.ani" in data
    assert "Handwriting.ani" in data
    assert "Cross.ani" in data
    assert "IBeam.ani" in data
    assert "Unavailiable.ani" in data
    assert "Alternate.ani" in data

    shutil.rmtree(d)


def test_WindowsPackager_without_website_url(
    tmpdir_factory: pytest.TempdirFactory,
) -> None:
    """Testing ``clickgen.packagers.WindowsPackager`` parameters default value."""
    d = Path(tmpdir_factory.mktemp("test_image"))
    create_test_cursor(d, "Work.ani")
    create_test_cursor(d, "Busy.ani")
    create_test_cursor(d, "Default.cur")
    create_test_cursor(d, "Help.cur")
    create_test_cursor(d, "Link.cur")
    create_test_cursor(d, "Move.cur")
    create_test_cursor(d, "Diagonal_2.cur")
    create_test_cursor(d, "Vertical.cur")
    create_test_cursor(d, "Horizontal.cur")
    create_test_cursor(d, "Diagonal_1.cur")
    create_test_cursor(d, "Handwriting.cur")
    create_test_cursor(d, "Cross.cur")
    create_test_cursor(d, "IBeam.cur")
    create_test_cursor(d, "Unavailiable.cur")
    create_test_cursor(d, "Alternate.cur")

    WindowsPackager(d, theme_name="test", comment="testing", author="Unknown")

    install_file = d / "install.inf"

    assert install_file.exists() is True
    data = install_file.read_text()

    assert "Work.ani" in data
    assert "Busy.ani" in data
    assert "Default.cur" in data
    assert "Help.cur" in data
    assert "Link.cur" in data
    assert "Move.cur" in data
    assert "Diagonal_2.cur" in data
    assert "Vertical.cur" in data
    assert "Horizontal.cur" in data
    assert "Diagonal_1.cur" in data
    assert "Handwriting.cur" in data
    assert "Cross.cur" in data
    assert "IBeam.cur" in data
    assert "Unavailiable.cur" in data
    assert "Alternate.cur" in data

    shutil.rmtree(d)


def test_WindowsPackager_with_website_url(
    tmpdir_factory: pytest.TempdirFactory,
) -> None:
    """Testing ``clickgen.packagers.WindowsPackager`` default parameters \
            with custom value."""
    d = Path(tmpdir_factory.mktemp("test_image"))
    create_test_cursor(d, "Work.ani")
    create_test_cursor(d, "Busy.ani")
    create_test_cursor(d, "Default.cur")
    create_test_cursor(d, "Help.cur")
    create_test_cursor(d, "Link.cur")
    create_test_cursor(d, "Move.cur")
    create_test_cursor(d, "Diagonal_2.cur")
    create_test_cursor(d, "Vertical.cur")
    create_test_cursor(d, "Horizontal.cur")
    create_test_cursor(d, "Diagonal_1.cur")
    create_test_cursor(d, "Handwriting.cur")
    create_test_cursor(d, "Cross.cur")
    create_test_cursor(d, "IBeam.cur")
    create_test_cursor(d, "Unavailiable.cur")
    create_test_cursor(d, "Alternate.cur")

    WindowsPackager(
        d,
        theme_name="test",
        comment="testing",
        author="Unknown",
        website_url="testing.test",
    )

    install_file = d / "install.inf"

    assert install_file.exists() is True
    data = install_file.read_text()

    assert "Work.ani" in data
    assert "Busy.ani" in data
    assert "Default.cur" in data
    assert "Help.cur" in data
    assert "Link.cur" in data
    assert "Move.cur" in data
    assert "Diagonal_2.cur" in data
    assert "Vertical.cur" in data
    assert "Horizontal.cur" in data
    assert "Diagonal_1.cur" in data
    assert "Handwriting.cur" in data
    assert "Cross.cur" in data
    assert "IBeam.cur" in data
    assert "Unavailiable.cur" in data
    assert "Alternate.cur" in data

    # assert "testing.test" in data

    shutil.rmtree(d)


def test_WindowsPackger_install_and_uninstall_scripts(
    tmpdir_factory: pytest.TempdirFactory,
) -> None:
    """Test the ``clickgen.packagers.WindowsPackager`` functionality."""

    d = Path(tmpdir_factory.mktemp("test_image"))
    create_test_cursor(d, "Work.ani")
    create_test_cursor(d, "Busy.ani")
    create_test_cursor(d, "Default.cur")
    create_test_cursor(d, "Help.cur")
    create_test_cursor(d, "Link.cur")
    create_test_cursor(d, "Move.cur")
    create_test_cursor(d, "Diagonal_2.cur")
    create_test_cursor(d, "Vertical.cur")
    create_test_cursor(d, "Horizontal.cur")
    create_test_cursor(d, "Diagonal_1.cur")
    create_test_cursor(d, "Handwriting.cur")
    create_test_cursor(d, "Cross.cur")
    create_test_cursor(d, "IBeam.cur")
    create_test_cursor(d, "Unavailiable.cur")
    create_test_cursor(d, "Alternate.cur")
    WindowsPackager(d, theme_name="test", comment="testing", author="Unknown")

    install_script = d / "install.inf"
    assert install_script.exists() is True
    install_data = install_script.read_text()
    assert "test Cursors" in install_data
    assert "Work.ani" in install_data
    assert "Busy.ani" in install_data
    assert "Default.cur" in install_data
    assert "Help.cur" in install_data
    assert "Link.cur" in install_data
    assert "Move.cur" in install_data
    assert "Diagonal_2.cur" in install_data
    assert "Vertical.cur" in install_data
    assert "Horizontal.cur" in install_data
    assert "Diagonal_1.cur" in install_data
    assert "Handwriting.cur" in install_data
    assert "Cross.cur" in install_data
    assert "IBeam.cur" in install_data
    assert "Unavailiable.cur" in install_data
    assert "Alternate.cur" in install_data

    uninstall_script = d / "uninstall.bat"
    assert uninstall_script.exists() is True
    uninstall_data = uninstall_script.read_text()
    assert "test Cursors" in uninstall_data

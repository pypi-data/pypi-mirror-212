from django.test import TestCase
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from django_icons.core import (
    _get_setting,
    get_icon_kwargs,
    get_icon_kwargs_from_settings,
    get_icon_renderer,
    icon,
    render_icon,
)
from django_icons.renderers import Bootstrap3Renderer, FontAwesome4Renderer, IconRenderer, ImageRenderer


class VersionTest(TestCase):
    """Test the package version."""

    def test_version(self):
        from django_icons import __version__

        parts = __version__.split(".")
        self.assertEqual(len(parts), 2)


class RenderIconFunctionTest(TestCase):
    """Test the `render_icon` function."""

    def test_render_icon(self):
        self.assertEqual(
            render_icon("user", title=_("user"), renderer=IconRenderer),
            '<i class="user" title="user"></i>',
        )

    def test_laziness(self):
        user_icon = render_icon("user", title=_("user"), renderer=IconRenderer)
        with translation.override("nl"):
            self.assertEqual(user_icon, '<i class="user" title="gebruiker"></i>')


class IconFunctionTest(TestCase):
    """Test the `icon` function."""

    def test_icon(self):
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(
                icon("user", title=_("user"), renderer=IconRenderer),
                '<i class="user" title="user"></i>',
            )


class UtilsTest(TestCase):
    """Test the utility functions."""

    def test_get_setting(self):
        with self.settings(DJANGO_ICONS=None):
            self.assertEqual(_get_setting("SECTION", "name"), None)
            self.assertEqual(_get_setting("SECTION", "name", "foo"), "foo")
        with self.settings(DJANGO_ICONS={"SECTION": {"name": "bar"}}):
            self.assertEqual(_get_setting("SECTION", "name"), "bar")
            self.assertEqual(_get_setting("SECTION", "name", "foo"), "bar")

    def test_get_icon_kwargs_from_settings(self):
        with self.settings(DJANGO_ICONS=None):
            self.assertEqual(get_icon_kwargs_from_settings("info"), {"name": "info"})
        with self.settings(DJANGO_ICONS={"ICONS": {"info": "info-sign"}}):
            self.assertEqual(get_icon_kwargs_from_settings("info"), {"name": "info-sign"})
        with self.settings(DJANGO_ICONS={"ICONS": {"info": {"name": "info-sign"}}}):
            self.assertEqual(get_icon_kwargs_from_settings("info"), {"name": "info-sign"})
        with self.settings(DJANGO_ICONS={"ICONS": {"info": {"title": "Information"}}}):
            self.assertEqual(
                get_icon_kwargs_from_settings("info"),
                {"name": "info", "title": "Information"},
            )

    def test_get_icon_kwargs(self):
        with self.settings(DJANGO_ICONS=None):
            self.assertEqual(
                get_icon_kwargs("info", "size-lg color-red"),
                {"name": "info", "extra_classes": ["size-lg", "color-red"]},
            )
        with self.settings(DJANGO_ICONS={"ICONS": {"info": "info-sign"}}):
            self.assertEqual(get_icon_kwargs("info"), {"name": "info-sign"})
        with self.settings(DJANGO_ICONS={"ICONS": {"info": {"name": "info-sign"}}}):
            self.assertEqual(get_icon_kwargs("info"), {"name": "info-sign"})
        with self.settings(DJANGO_ICONS={"ICONS": {"info": {"title": "Information"}}}):
            self.assertEqual(get_icon_kwargs("info"), {"name": "info", "title": "Information"})

    def test_get_icon_renderer(self):
        with self.settings(DJANGO_ICONS=None):
            self.assertEqual(get_icon_renderer(), IconRenderer)
            self.assertEqual(get_icon_renderer("icon"), IconRenderer)
            self.assertEqual(get_icon_renderer("fontawesome4"), FontAwesome4Renderer)
            self.assertEqual(get_icon_renderer("bootstrap3"), Bootstrap3Renderer)
            self.assertEqual(get_icon_renderer("image"), ImageRenderer)
            self.assertEqual(
                get_icon_renderer("django_icons.renderers.Bootstrap3Renderer"),
                Bootstrap3Renderer,
            )
            self.assertEqual(
                get_icon_renderer("Bootstrap3Renderer"),
                Bootstrap3Renderer,
            )

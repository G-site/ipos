import asyncio

from app.main import app, create_app
from app.parser import parse_inline_markup, parse_popup_target, render_sections
from app.services import get_chapter_by_slug, get_chapters


def test_bold_markup_is_rendered():
    result = parse_inline_markup("Это #важный текст# для службы.")
    assert "<strong>важный текст</strong>" in result


def test_comment_link_is_transformed_to_popup_button():
    result = parse_inline_markup(
        "[[памятка_рядом|comment:Не спеши и держи внимание на службе.]]"
    )
    assert "inline-popup-trigger" in result
    assert 'data-popup-type="comment"' in result


def test_italic_light_markup_is_rendered():
    result = parse_inline_markup("Это ~спокойное пояснение~ для ученика.")
    assert '<em class="text-lean">спокойное пояснение</em>' in result


def test_important_markup_is_rendered():
    result = parse_inline_markup("Это !!важное предупреждение!! для службы.")
    assert '<strong class="text-important">важное предупреждение</strong>' in result


def test_youtube_target_normalizes_to_embed():
    popup_type, popup_value = parse_popup_target(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=43s"
    )
    assert popup_type == "youtube"
    assert popup_value.endswith("dQw4w9WgXcQ?start=43")


def test_render_sections_builds_toc():
    sections, toc = render_sections(
        [{"id": "one", "title": "Первый раздел", "body": ["Текст"]}]
    )
    assert sections[0]["id"] == "one"
    assert toc == [{"id": "one", "title": "Первый раздел"}]


def test_services_return_chapters():
    chapters = asyncio.run(get_chapters())
    chapter = asyncio.run(get_chapter_by_slug("prizvanie-i-vnimanie"))
    assert len(chapters) >= 3
    assert chapter is not None
    assert chapter["toc"]


def test_app_is_configured_with_expected_routes():
    local_app = create_app()
    paths = {route.path for route in local_app.routes}
    assert "/" in paths
    assert "/chapters/{slug}" in paths
    assert app.title == "Школа юного иподьякона"

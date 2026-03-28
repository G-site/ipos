from __future__ import annotations

import html
import re
from urllib.parse import parse_qs, urlparse


LINK_PATTERN = re.compile(r"\[\[(.+?)\|(.+?)\]\]")
BOLD_IMPORTANT_PATTERN = re.compile(r"!!(.*?)!!")
BOLD_PATTERN = re.compile(r"#(.*?)#")
ITALIC_LIGHT_PATTERN = re.compile(r"~(.*?)~")
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif")


def _format_link_label(label: str) -> str:
    parts = [html.escape(part.strip()) for part in label.split("_") if part.strip()]
    if not parts:
        return html.escape(label)

    decorated = "".join(
        f'<span class="link-word">{part}</span>' for part in parts
    )
    return f'<span class="link-label">{decorated}</span>'


def _extract_youtube_id(parsed_url) -> str | None:
    if "youtu.be" in parsed_url.netloc:
        return parsed_url.path.lstrip("/") or None
    if "youtube.com" in parsed_url.netloc:
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]
        if parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/embed/", 1)[1] or None
        if parsed_url.path.startswith("/shorts/"):
            return parsed_url.path.split("/shorts/", 1)[1] or None
    return None


def _extract_youtube_start(parsed_url) -> int:
    params = parse_qs(parsed_url.query)
    raw_value = params.get("t", params.get("start", ["0"]))[0]
    if raw_value.isdigit():
        return int(raw_value)

    match = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?", raw_value)
    if not match:
        return 0

    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds


def parse_popup_target(raw_target: str) -> tuple[str, str]:
    target = raw_target.strip()
    if target.lower().startswith("comment:"):
        return "comment", target.split(":", 1)[1].strip()

    parsed = urlparse(target)
    youtube_id = _extract_youtube_id(parsed)
    if youtube_id:
        start = _extract_youtube_start(parsed)
        embed_url = f"https://www.youtube.com/embed/{youtube_id}"
        if start:
            embed_url += f"?start={start}"
        return "youtube", embed_url

    if parsed.path.lower().endswith(IMAGE_EXTENSIONS):
        return "image", target

    if parsed.scheme in {"http", "https"}:
        return "comment", f"Посилання: {target}"

    return "comment", target


def parse_inline_markup(text: str) -> str:
    escaped = html.escape(text)

    def replace_important(match: re.Match[str]) -> str:
        return f'<strong class="text-important">{html.escape(match.group(1))}</strong>'

    def replace_bold(match: re.Match[str]) -> str:
        return f"<strong>{html.escape(match.group(1))}</strong>"

    def replace_italic_light(match: re.Match[str]) -> str:
        return f'<em class="text-lean">{html.escape(match.group(1))}</em>'

    escaped = BOLD_IMPORTANT_PATTERN.sub(replace_important, escaped)
    escaped = BOLD_PATTERN.sub(replace_bold, escaped)
    escaped = ITALIC_LIGHT_PATTERN.sub(replace_italic_light, escaped)

    def replace_link(match: re.Match[str]) -> str:
        label = match.group(1).strip()
        target = html.unescape(match.group(2).strip())
        popup_type, popup_value = parse_popup_target(target)
        return (
            '<button type="button" class="inline-popup-trigger" '
            f'data-popup-type="{html.escape(popup_type, quote=True)}" '
            f'data-popup-value="{html.escape(popup_value, quote=True)}" '
            f'aria-label="Открыть материал: {html.escape(label, quote=True)}">'
            f"{_format_link_label(label)}"
            "</button>"
        )

    escaped = LINK_PATTERN.sub(replace_link, escaped)
    return escaped


def render_sections(sections: list[dict]) -> tuple[list[dict], list[dict]]:
    rendered_sections = []
    toc = []

    for section in sections:
        rendered_sections.append(
            {
                "id": section["id"],
                "title": section["title"],
                "body": [parse_inline_markup(paragraph) for paragraph in section["body"]],
            }
        )
        toc.append({"id": section["id"], "title": section["title"]})

    return rendered_sections, toc

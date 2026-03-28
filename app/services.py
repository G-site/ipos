import asyncio

from app.data import chapters
from app.parser import render_sections


async def get_chapters() -> list[dict]:
    await asyncio.sleep(0)
    return chapters


async def get_chapter_by_slug(slug: str) -> dict | None:
    await asyncio.sleep(0)
    for chapter in chapters:
        if chapter["slug"] == slug:
            rendered_sections, toc = render_sections(chapter["sections"])
            return {
                **chapter,
                "rendered_sections": rendered_sections,
                "toc": toc,
            }
    return None

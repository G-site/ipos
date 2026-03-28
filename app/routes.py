from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.services import get_chapter_by_slug, get_chapters


router = APIRouter()
templates = Jinja2Templates(directory=settings.template_dir)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    chapters = await get_chapters()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "chapters": chapters,
            "page_title": settings.app_title,
            "hero_title": "Навчання юних іпод'яконів",
            "hero_text": (
                "Тихий, красивий і сучасний простір для знайомства зі служінням, "
                "дисципліною та увагою у храмі."
            ),
            "footer_note": "Матеріал підготовлений для спокійного та послідовного навчання.",
        },
    )


@router.get("/chapters/{slug}", response_class=HTMLResponse)
async def chapter_detail(request: Request, slug: str) -> HTMLResponse:
    chapter = await get_chapter_by_slug(slug)
    if chapter is None:
        raise HTTPException(status_code=404, detail="Главу не знайдено")

    return templates.TemplateResponse(
        request=request,
        name="chapter.html",
        context={
            "chapter": chapter,
            "page_title": chapter["title"],
            "footer_note": "Усі спливаючі матеріали закриваються на кліку поза вікном або під час прокручування.",
        },
    )

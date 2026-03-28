from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_title: str = "Школа юного іподьякона"
    app_description: str = (
        "Мінімалістичний навчальний сайт для юних іподьяконів з інтерактивними матеріалами."
    )
    template_dir: str = "app/templates"
    static_dir: str = "app/static"


settings = Settings()

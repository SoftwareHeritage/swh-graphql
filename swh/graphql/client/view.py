from starlette.templating import Jinja2Templates


async def explorer_page(request):
    templates = Jinja2Templates(directory="swh/graphql/client")
    return templates.TemplateResponse("explorer.html", {"request": request})

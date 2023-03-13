# Copyright (C) 2023 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import os

from starlette.templating import Jinja2Templates


async def explorer_page(request):
    templates = Jinja2Templates(directory=os.path.dirname(__file__))
    return templates.TemplateResponse("explorer.html", {"request": request})

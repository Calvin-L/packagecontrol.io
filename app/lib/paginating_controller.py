import math
from urllib.parse import urlencode

from bottle import route, request


def get_page():
    try:
        page = request.query.page or 1
        page = int(page)
    except (ValueError):
        page = 1
    return page


def build_data(results, page, per_page, list_key='packages', other_params=None):
    total = results['total']

    count = len(results[list_key])
    begin = (page - 1) * per_page
    end = begin + count

    pages = math.ceil(total / per_page)

    if other_params is None:
        other_params = {}

    links = []
    if pages > 1:
        for num in range(1, pages + 1):
            params = {'page': str(num)}
            params.update(other_params)
            link = {
                'number': num,
                'href': '?' if num == 1 else '?' + urlencode(params),
                'selected': num == page
            }
            links.append(link)

    return {
        list_key: results[list_key],
        'page': page,
        'count': count,
        'begin': begin,
        'end': end,
        'total': total,
        'pages': pages,
        'links': links
    }

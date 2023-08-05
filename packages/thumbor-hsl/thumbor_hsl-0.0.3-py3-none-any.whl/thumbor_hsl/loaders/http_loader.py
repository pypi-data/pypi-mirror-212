import datetime
import re
from thumbor.loaders import http_loader
from urllib.parse import urlparse


def return_contents(response, url, context, req_start=None):
    regex_match = context.config.HSL_REGEX_MATCH_URL

    def callback():
        return http_loader.return_contents(response, url, context, req_start)

    if req_start:
        res = urlparse(url)
        netloc = res.netloc
        code = response.code

        has_width_and_height = bool(context.request.width) and bool(context.request.height)

        if not has_width_and_height and regex_match is None:
            return callback()

        parsed_match = ''

        if regex_match:
            parsed_match = re.search(regex_match, url)
            parsed_match = parsed_match.group(1) if parsed_match and parsed_match.group(1) else ''

        finish = datetime.datetime.now()

        # make sure to have placeholders in case the values are empty. This way we can parse it easier later
        extra = f"{context.request.width}x{context.request.height}%{parsed_match}" \
            if has_width_and_height else f"%{parsed_match}"

        context.metrics.timing(
            f"original_image_with_size.fetch.{code}%{netloc}%{extra}",
            (finish - req_start).total_seconds() * 1000,
        )
        context.metrics.incr(
            f"original_image_with_size.fetch.{code}%{netloc}%{extra}",
        )

    return callback()


async def load(context, url):
    return await http_loader.load(context, url, return_contents_fn=return_contents)

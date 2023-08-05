thumbor-http-stats-loader
--------------------------------

An extended `http` loader for thumbor which introduces an additional statd
counter `original_image_with_size_fetch.$code.$host.$widthx$height.$parsedUrl`

## Configuration

    LOADER="thumbor_hsl.loaders.http_loader"

### Optional query parsing

If you specify the `HSL_REGEX_MATCH_URL` option, you can provide a regex with a group which value will be appended
in `$parsedUrl`

Example:

    HSL_REGEX_MATCH_URL="someQuery=(\d+)"

For a given url, e.g. `https://my-image?someQuery=10` the result of `10` will be appended to the counter.


## Install

    pip install https://github.com/BowlingX/thumbor-http-header-stats-loader/archive/1.0.0.zip  
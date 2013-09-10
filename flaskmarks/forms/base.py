from flask_wtf import (
    Form,
)

strip_filter = lambda x: x.strip() if x else None

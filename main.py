
from pydantic import BaseModel
import string
import random

app = FastAPI()

# In-memory store: {short_code: original_url}
url_mapping = {}

# Characters for short code
SHORT_CODE_LENGTH = 6
CHARACTERS = string.ascii_letters + string.digits


def generate_short_code(length=SHORT_CODE_LENGTH):
    """Generate a unique short code."""
    while True:
        code = ''.join(random.choices(CHARACTERS, k=length))
        if code not in url_mapping:
            return code


class URLRequest(BaseModel):
    url: str


class URLResponse(BaseModel):
    short_url: str
    original_url: str


@app.post("/shorten", response_model=URLResponse)
def create_short_url(request: URLRequest):
    original_url = request.url
    # Generate a unique short code
    short_code = generate_short_code()
    url_mapping[short_code] = original_url
    short_url = f"https://{YOUR_VERCEL_DOMAIN}/{short_code}"
    return URLResponse(short_url=short_url, original_url=original_url)


@app.get("/{short_code}")
def redirect(short_code: str):
    original_url = url_mapping.get(short_code)
    if not original_url:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"redirect_url": original_url}

# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.scrape import scrape_single_url
from app.extract import process_and_extract_tables_single
from app.models import BankResponse
from mangum import Mangum  # Import Mangum for AWS Lambda integration
import logging
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

class ExtractionRequest(BaseModel):
    url: str

    @classmethod
    def validate_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if not all([parsed.scheme, parsed.netloc]):
            raise ValueError('Invalid URL format.')
        if parsed.scheme not in ('http', 'https'):
            raise ValueError('URL must start with http or https.')
        return v

class ExtractionResponse(BaseModel):
    bank_response: Optional[BankResponse]
    error: Optional[str] = None

@app.post("/extract", response_model=ExtractionResponse)
def extract_bank_data(request: ExtractionRequest):
    url = request.url  # str
    logger.info(f"Received request to scrape URL: {url}")
    
    csv_tables, error = scrape_single_url(url)

    if error:
        logger.error(f"Error scraping URL {url}: {error}")
        raise HTTPException(status_code=400, detail=error)

    bank_response = process_and_extract_tables_single(csv_tables, chunk_size=5000)

    if not bank_response:
        logger.error(f"Failed to process scraped data for URL {url}")
        raise HTTPException(status_code=500, detail="Failed to process the scraped data.")

    logger.info(f"Successfully processed data for URL {url}")
    return ExtractionResponse(bank_response=bank_response)

# Create Mangum handler for AWS Lambda
handler = Mangum(app, lifespan="off")

# Add a root route for health checks
@app.get("/")
def read_root():
    return {"status": "ok"}

# When using API Gateway with Lambda proxy integration, 
# add this route to handle OPTIONS requests
@app.options("/{rest_of_path:path}")
async def preflight_handler(rest_of_path: str):
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

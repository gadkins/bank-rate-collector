# Bank Rate Collector

An AI-powered API that extracts bank interest rates from a given URL.  

The API uses OpenAI's GPT-4o to extract the interest rates from a given URL. The API is built using FastAPI and deployed to AWS Lambda using the Serverless Framework.

## Project Structure

```
bank-rate-collector/
│
├── app/
│ ├── main.py # FastAPI application with Mangum handler
│ ├── extract.py # 'extract' function and related utilities
│ ├── merge.py # Functions for merging rates by URL and root domain
│ ├── models.py # Pydantic models (BankResponse and others)
│ └── scrape.py # Functions for scraping URLs
│
├── template.yaml # AWS SAM template for Lambda configuration
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── .gitignore # Git ignore file

```

## Prerequisites

- Python 3.10 or higher
- AWS CLI configured with appropriate credentials
- AWS SAM CLI installed
- An OpenAI API key stored in AWS Secrets Manager

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/gadkins/bank-rate-collector.git
   cd bank-rate-collector
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Store your OpenAI API key in AWS Secrets Manager:
   - Go to AWS Secrets Manager console
   - Create a new secret named `bank-rate-collector/openai-api-key`
   - Store your OpenAI API key as the secret value

## Deploy to AWS Lambda using AWS SAM

1. Build the SAM application:
   ```
   sam build
   ```

2. Deploy the application:
   ```
   sam deploy --guided
   ```
   Follow the prompts to configure your deployment. Make sure to allow the creation of IAM roles when asked.

3. Note the API endpoint URL provided in the deployment output.

## Usage

To use the API, send a POST request to the `/extract` endpoint with a JSON body containing the URL to scrape:

```
curl -X POST "https://wvceiydmh4.execute-api.us-east-2.amazonaws.com/Prod/extract" \
    -H "Content-Type: application/json" \
    -d '{"url": "https://www.simplicity.coop/rates"}'
```

## Local Development

To run the application locally for development:

1. Set the following environment variables in the `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key
- `AWS_REGION`: The AWS region where the Lambda function will be deployed
- `AWS_ACCESS_KEY_ID`: Your AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key

Alternatively, you can set the environment variables in your shell, for example: `

```bash
export OPENAI_API_KEY='your-openai-api-key'
```

2. Configure a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI application:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`.

## How It Works

The following components are used in the Bank Rate Collector API:

- [x] The web scraper BeautifulSoup is used to scrape HTML tags from a list of websites.
- [x] From the collected tags, we filter for `<table>`, `<h1>`, and `<h2>` tags, discarding the rest.
- [x] These tables are converted into CSV to clean them up and reduce their character count using custom functions.  
- [x] The CSV tables are then chunked to prepare them for sending to a large language model (LLM).
- [x] Along with the table chunks, a structured schema (Pydantic object) is provided to the LLM to instruct it on how the data should be formatted in it's response.
- [x] Special instructions can be provided to the LLM to handle edge cases or other behavior not well defined in the Pydantic object schema.
- [x] Once the LLM receives the table chunks, structured schema response format, and special instructions, it responds with a list of JSON objects containing the banking rates, per the schema (OpenAI Python SDK now supports enfocing a `response_format` such as a Pydantic object. The SDK handles converting the data type to a supported JSON schema, deserializing the JSON response into the typed data structure automatically, and parsing refusals if they arise. See [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)).
- [x] After all JSON objects are returned from the LLM, a post-processing script aggregates and deduplicates the data.

### Structured Outputs

The application passes a Pydantic object to the LLM to enforce a structured response format. The Pydantic object is a schema that defines the structure of the response data. The OpenAI API will return a JSON object that conforms to this schema. The Pydantic object is defined in the `models.py` file.

<details>
  <summary>Show JSON schema</summary>

```json
{
  "type": "object",
  "properties": {
    "bankRootDomain": {
      "type": "string",
      "description": "The root domain of the bank."
    },
    "checkingAccounts": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/CheckingAccountResponse"
      },
      "default": []
    },
    "savingsAccounts": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/SavingsAccountResponse"
      },
      "default": []
    },
    "moneyMarketAccounts": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/MoneyMarketAccountResponse"
      },
      "default": []
    },
    "certificatesOfDeposit": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/CertificateOfDepositResponse"
      },
      "default": []
    },
    "individualRetirementAccounts": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/IndividualRetirementAccountResponse"
      },
      "default": []
    },
    "loans": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/LoanResponse"
      },
      "default": []
    },
    "creditCards": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/CreditCardResponse"
      },
      "default": []
    },
    "fees": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/FeeResponse"
      },
      "default": []
    }
  },
  "required": ["bankRootDomain"],
  "definitions": {
    "CheckingAccountResponse": {
      "$ref": "#/definitions/CheckingAccountResponse"
    },
    "SavingsAccountResponse": {
      "$ref": "#/definitions/SavingsAccountResponse"
    },
    "MoneyMarketAccountResponse": {
      "$ref": "#/definitions/MoneyMarketAccountResponse"
    },
    "CertificateOfDepositResponse": {
      "$ref": "#/definitions/CertificateOfDepositResponse"
    },
    "IndividualRetirementAccountResponse": {
      "$ref": "#/definitions/IndividualRetirementAccountResponse"
    },
    "LoanResponse": {
      "$ref": "#/definitions/LoanResponse"
    },
    "CreditCardResponse": {
      "$ref": "#/definitions/CreditCardResponse"
    },
    "FeeResponse": {
      "$ref": "#/definitions/FeeResponse"
    }
  }
}
```
</details>
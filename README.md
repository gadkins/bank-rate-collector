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

1. Rename the `.env.example` file to `.env`:
    ```bash
    mv .env.example .env
    ```

2. set the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key. You can get an API key from the [OpenAI platform](https://platform.openai.com/api-keys).
- `AWS_REGION`: The AWS region where the Lambda function will be deployed
- `AWS_ACCESS_KEY_ID`: Your AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key

Alternatively, you can set the environment variables in your shell, for example: `

    ```bash
    export OPENAI_API_KEY='your-openai-api-key'
    ```

3. Configure a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install the development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the FastAPI application:
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
        "bankDomain": {
            "type": "string",
            "description": "The domain of the bank to which these account types belong."
        },
        "checkingAccounts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the checking account, e.g. Interest Checking, Senior Advantage Checking, etc."
                    },
                    "interestRate": {
                        "type": "number",
                        "description": "The interest rate of the checking account, if any."
                    },
                    "annualPercentageYield": {
                        "type": "number",
                        "description": "The annual percentage yield (APY) of the checking account."
                    },
                    "minimumBalanceToObtainAPY": {
                        "type": "number",
                        "description": "The minimum balance to obtain the annual percentage yield (APY)."
                    },
                    "minimumBalanceToOpen": {
                        "type": "number",
                        "description": "The minimum balance to open the checking account."
                    },
                    "minimumDailyBalance": {
                        "type": "number",
                        "description": "The minimum daily balance of the checking account to obtain APY or avoid fees."
                    },
                    "dividendRate": {
                        "type": "number",
                        "description": "The dividend rate of the checking account, if any."
                    },
                    "dividendFrequency": {
                        "type": "string",
                        "description": "The frequency at which dividends are paid, if at all, e.g. monthly, quarterly, annually, etc."
                    }
                },
                "required": [
                    "name",
                    "annualPercentageYield"
                ]
            }
        },
        "savingsAccounts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the savings account, e.g. Partnership Savings, Statement Savings, etc."
                    },
                    "interestRate": {
                        "type": "number",
                        "description": "The interest rate of the savings account, if any."
                    },
                    "annualPercentageYield": {
                        "type": "number",
                        "description": "The annual percentage yield (APY) of the savings account."
                    },
                    "minimumBalanceToObtainAPY": {
                        "type": "number",
                        "description": "The minimum balance to obtain the annual percentage yield (APY)."
                    },
                    "minimumBalanceToOpen": {
                        "type": "number",
                        "description": "The minimum balance to open the savings account."
                    },
                    "minimumDailyBalance": {
                        "type": "number",
                        "description": "The minimum daily balance of the savings account to obtain APY or avoid fees."
                    },
                    "dividendRate": {
                        "type": "number",
                        "description": "The dividend rate of the checking account, if any."
                    },
                    "dividendFrequency": {
                        "type": "string",
                        "description": "The frequency at which dividends are paid, if at all, e.g. monthly, quarterly, annually, etc."
                    },
                    "required": [
                        "name",
                        "annualPercentageYield"
                    ]
                }
            },
            "moneyMarketAccounts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name or tier of money market account, e.g. Tier 1 ($0.01 - $9,999.99), etc."
                        },
                        "interestRate": {
                            "type": "number",
                            "description": "The interest rate of the savings account, if any."
                        },
                        "annualPercentageYield": {
                            "type": "number",
                            "description": "The annual percentage yield (APY) of the savings account."
                        },
                        "minimumBalanceToObtainAPY": {
                            "type": "number",
                            "description": "The minimum balance to obtain the annual percentage yield (APY)."
                        },
                        "dividendRate": {
                            "type": "number",
                            "description": "The dividend rate of the checking account, if any."
                        },
                        "dividendFrequency": {
                            "type": "string",
                            "description": "The frequency at which dividends are paid, if at all, e.g. monthly, quarterly, annually, etc."
                        },
                        "minimumBalanceToOpen": {
                            "type": "number",
                            "description": "The minimum balance to open the savings account."
                        },
                        "minimumDailyBalance": {
                            "type": "number",
                            "description": "The minimum daily balance of the savings account to obtain APY or avoid fees."
                        }
                    },
                    "required": [
                        "name",
                        "annualPercentageYield"
                    ]
                }
            },
            "certificatesOfDeposit": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "term": {
                            "type": "string",
                            "description": "The term of the certificate of deposit, e.g. 6 months, 12 months, etc."
                        },
                        "interestRate": {
                            "type": "number",
                            "description": "The interest rate of the certificate of deposit, if any."
                        },
                        "annualPercentageYield": {
                            "type": "number",
                            "description": "The annual percentage yield (APY) of the certificate of deposit."
                        },
                        "minimumBalanceToObtainAPY": {
                            "type": "number",
                            "description": "The minimum balance to obtain the annual percentage yield (APY)."
                        },
                        "minimumBalanceToOpen": {
                            "type": "number",
                            "description": "The minimum balance to open the certificate of deposit."
                        },
                        "minimumDailyBalance": {
                            "type": "number",
                            "description": "The minimum daily balance of the certificate of deposit to obtain APY or avoid fees."
                        }
                    },
                    "required": [
                        "term",
                        "annualPercentageYield"
                    ]
                }
            },
            "individualRetirementAccounts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "term": {
                            "type": "string",
                            "description": "The term of the individual retirement account, e.g. 7 months, 12 months, etc."
                        },
                        "interestRate": {
                            "type": "number",
                            "description": "The interest rate of the individual retirement account, if any."
                        },
                        "annualPercentageYield": {
                            "type": "number",
                            "description": "The annual percentage yield (APY) of the individual retirement account."
                        },
                        "minimumBalanceToObtainAPY": {
                            "type": "number",
                            "description": "The minimum balance to obtain the annual percentage yield (APY)."
                        },
                        "minimumBalanceToOpen": {
                            "type": "number",
                            "description": "The minimum balance to open the individual retirement account."
                        },
                        "minimumDailyBalance": {
                            "type": "number",
                            "description": "The minimum daily balance of the individual retirement account to obtain APY or avoid fees."
                        }
                    },
                    "required": [
                        "term",
                        "annualPercentageYield"
                    ]
                }
            },
            "loans": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the loan, e.g. Auto Loan, Student Loan, 30-Year Fixed Rate Mortgage, etc."
                        },
                        "term": {
                            "anyOf": [
                                {
                                    "type": "integer"
                                },
                                {
                                    "type": "string"
                                }
                            ],
                            "description": "The term of the loan, e.g. 1-3 years, 7 years, etc."
                        },
                        "annualPercentageRate": {
                            "type": "number",
                            "description": "The Annual Percentage Rate (APR) of the loan. APR is the interest rate plus additional fees charged by the lender."
                        },
                        "minimumPayment": {
                            "type": "number",
                            "description": "The required minimum monthly payment for the loan."
                        },
                        "maximumLoanAmount": {
                            "type": "number",
                            "description": "The maximum loan amount that can be borrowed as a percentage of the collateral value."
                        },
                        "paymentPer1000Dollars": {
                            "type": "number",
                            "description": "The amount the borrower would pay per month for every $1,000 borrowed."
                        }
                    },
                    "required": [
                        "name",
                        "annualPercentageRate"
                    ]
                }
            },
            "creditCards": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the credit card, if applicable, e.g. Visa Platinum, Mastercard Gold, etc."
                        },
                        "annualPercentageRate": {
                            "type": "number",
                            "description": "The Annual Percentage Rate (APR) of the loan. APR is the interest rate plus additional fees charged by the lender."
                        },
                        "annualFee": {
                            "type": "number",
                            "description": "The annual fee charged by the credit card provider."
                        },
                        "doesEarnRewards": {
                            "type": "boolean",
                            "description": "Indicates whether the credit card earns rewards or not."
                        }
                    },
                    "required": [
                        "annualPercentageRate",
                        "annualFee"
                    ]
                }
            },
            "fees": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the fee, e.g. Overdraft Fee, Wire Transfer Fee, etc."
                        },
                        "feeAmount": {
                            "type": "number",
                            "description": "The fee amount."
                        },
                        "feeUnit": {
                            "type": "string",
                            "description": "The unit of the fee amount, e.g. 'per hour', 'per month', 'per ten', '%', etc."
                        },
                        "oneTime": {
                            "type": "boolean",
                            "description": "Indicates if the fee is a one-time fee."
                        },
                        "recurringInterval": {
                            "type": "string",
                            "description": "The interval for recurring fees, e.g. 'monthly', 'annually', etc. (if applicable).",
                            "enum": ["daily", "weekly", "monthly", "annually"]
                        }
                    },
                    "required": [
                        "name",
                        "feeAmount",
                        "feeUnit"
                    ],
                    "anyOf": [
                        {
                            "required": ["oneTime"]
                        },
                        {
                            "required": ["recurringInterval"]
                        }
                    ]
                }
            }
        }
    }
}
```
</details>
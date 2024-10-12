# Bank Rate Collector

An AI-powered API that extracts bank interest rates from a given URL.  

The API uses OpenAI's GPT-4o to extract the interest rates from a given URL. The API is built using FastAPI and deployed to AWS Lambda using the Serverless Framework.

## Project Structure

```
bank-rate-collector/
│
├── app/
│   ├── main.py          # FastAPI application with Mangum handler
│   ├── extract.py       # 'extract' function and related utilities
│   ├── merge.py         # Functions for merging rates by URL and root domain
│   ├── models.py        # Pydantic models (BankResponse and others)
│   └── scrape.py        # Functions for scraping URLs
│
├── template.yaml        # AWS SAM template for Lambda configuration
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .gitignore           # Git ignore file

```
## Deploy to AWS Lambda using AWS SAM

AWS Serverless Application Model (SAM) is a framework for building serverless applications, primarily targeted for Amazon API Gateway APIs, AWS Lambda functions, and Amazon DynamoDB.

To deploy the FastAPI application to AWS Lambda using AWS SAM, follow these steps:

1. Set the `OPENAI_API_KEY` variable

    ```bash
    export OPENAI_API_KEY='your-openai-api-key'
    ```

    Add this line to your shell configuration (`~/.bashrc` or `~/.zshrc`) to persist the variable across sessions. To add this line to your shell configuration, run:
    
    ```bash
    echo "export OPENAI_API_KEY='your-openai-api-key'" >> ~/.bashrc
    ```

    Then reolad your shell:
    
        ```bash
        source ~/.bashrc
        ```

2. Install SAM CLI:
    
    Download and run the SAM [CLI installer](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).

    Then complete the setup wizard.

    To verify the installation, run:
    
    ```bash
    which sam
    sam --version
    ```

3. Build the project:
    
    ```bash
    sam build
    ```

    The SAM CLI will build the FastAPI application and create a `.aws-sam` directory.

4. Deploy

    ```bash
   sam deploy --guided
    ```

    During deployment, you'll be asked to set up various configurations, including the API Gateway.

5. Test the API
    
    ```bash
    curl -X GET https://ifj2zfoza5.execute-api.us-east-1.amazonaws.com/Prod/bank-rates?url=https://www.simplicity.coop/rates
    ```

## Deploy to AWS Lambda using Serverless Framework 

Alternately, you can deploy the FastAPI application to AWS Lambda using the Serverless Framework. The advantage of using the Serverless Framework is it's multi-cloud compatibility with other cloud providers like Azure and Google Cloud.

To deploy the FastAPI application to AWS Lambda using the Serverless Framework, follow these steps:

1. Set the `OPENAI_API_KEY` variable

    ```bash
    export OPENAI_API_KEY='your-openai-api-key'
    ```

    Add this line to your shell configuration (`~/.bashrc` or `~/.zshrc`) to persist the variable across sessions. To add this line to your shell configuration, run:
    
    ```bash
    echo "export OPENAI_API_KEY='your-openai-api-key'" >> ~/.bashrc
    ```

    Then reolad your shell:
    
        ```bash
        source ~/.bashrc
        ```

2. Install Serverless Framework:
    
    ```bash
    npm install -g serverless
    ```
    
    The Serverless Framework configuration is defined in the `serverless.yml` file and state information is stored in `.serverless` directory.

3. Set Up Your AWS Credentials:
    
    ```bash
    serverless config credentials --provider aws --key YOUR_ACCESS_KEY --secret YOUR_SECRET_KEY
    ```

    Be sure to replace `YOUR_ACCESS_KEY` and `YOUR_SECRET_KEY` with your own AWS credentials.

4. Install the Serverless Python Requirements Plugin:
    
    ```bash
    npm install serverless-python-requirements
    ```

    The Serverless Python Requirements plugin will package the Python dependencies and deploy them to AWS Lambda.

5. Deploy

    ```bash
    serverless deploy
    ```

    This will deploy the FastAPI application to AWS Lambda and create an API Gateway endpoint.

6. Test the API
    
    ```bash
    curl -X GET https://ip8qnpxns8.execute-api.us-east-1.amazonaws.com/bank-rates?url=https://www.simplicity.coop/rates
    ```
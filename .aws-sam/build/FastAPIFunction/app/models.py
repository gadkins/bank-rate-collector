from typing import List, Union
from pydantic import BaseModel, Field

class CheckingAccountResponse(BaseModel):
    """
    Pydantic model representing a checking account.
    """

    name: str = Field(description="The name of the checking account.")
    interestRate: float = Field(description="The interest rate of the checking account, if any.")
    annualPercentageYield: Union[float, None] = Field(description="The annual percentage yield of the checking account.")
    minimumBalanceToObtainAPY: Union[float, None] = Field(description="The minimum balance to obtain the annual percentage yield of the checking account, if any.")
    minimumBalanceToOpen: Union[float, None] = Field(description="The minimum balance to open the checking account, if any.")
    minimumDailyBalance: Union[float, None] = Field(description="The minimum daily balance of the checking account, if any.")
    dividendRate: Union[float, None] = Field(description="The dividend rate of the checking account, if any.")
    dividendFrequency: Union[str, None] = Field(description="The dividend frequency of the checking account, if any.")

class SavingsAccountResponse(BaseModel):
    """
    Pydantic model representing a savings account.
    """

    name: str = Field(description="The name of the savings account.")
    interestRate: Union[float, None] = Field(description="The interest rate of the savings account, if any.")
    annualPercentageYield: float = Field(description="The annual percentage yield of the savings account.")
    minimumBalanceToObtainAPY: Union[float, None] = Field(description="The minimum balance to obtain the annual percentage yield of the savings account, if any.")
    minimumBalanceToOpen: Union[float, None] = Field(description="The minimum balance to open the savings account, if any.")
    minimumDailyBalance: Union[float, None] = Field(description="The minimum daily balance of the savings account, if any. Alternatively, the balance requirement for interest.")
    dividendRate: Union[float, None] = Field(description="The dividend rate of the savings account, if any.")
    dividendFrequency: Union[str, None] = Field(description="The dividend frequency of the savings account, if any.")

class MoneyMarketAccountResponse(BaseModel):
    """
    Pydantic model representing a money market account.
    """

    name: str = Field(description="The name of the money market account.")
    interestRate: Union[float, None] = Field(description="The interest rate of the money market account, if any.")
    annualPercentageYield: float = Field(description="The annual percentage yield of the money market account.")
    minimumBalanceToObtainAPY: Union[float, None] = Field(description="The minimum balance to obtain the annual percentage yield of the money market account, if any.")
    dividendRate: Union[float, None] = Field(description="The dividend rate of the money market account, if any.")
    dividendFrequency: Union[str, None] = Field(description="The dividend frequency of the money market account, if any.")
    minimumBalanceToOpen: Union[float, None] = Field(description="The minimum balance to open the money market account, if any.")
    minimumDailyBalance: Union[float, None] = Field(description="The minimum daily balance of the money market account, if any.")

class CertificateOfDepositResponse(BaseModel):
    """
    Pydantic model representing a certificate of deposit.
    """

    term: str = Field(description="The term of the certificate of deposit.")
    interestRate: Union[float, None] = Field(description="The interest rate of the certificate of deposit, if any.")
    annualPercentageYield: float = Field(description="The annual percentage yield of the certificate of deposit.")
    minimumBalanceToObtainAPY: Union[float, None] = Field(description="The minimum balance to obtain the annual percentage yield of the certificate of deposit, if any.")
    minimumBalanceToOpen: Union[float, None] = Field(description="The minimum balance to open the certificate of deposit, if any.")
    minimumDailyBalance: Union[float, None] = Field(description="The minimum daily balance of the certificate of deposit, if any.")

class IndividualRetirementAccountResponse(BaseModel):
    """
    Pydantic model representing an individual retirement account.
    """

    term: str = Field(description="The term of the individual retirement account.")
    interestRate: Union[float, None] = Field(description="The interest rate of the individual retirement account, if any.") 
    annualPercentageYield: float = Field(description="The annual percentage yield of the individual retirement account.")
    minimumBalanceToObtainAPY: Union[float, None] = Field(description="The minimum balance to obtain the annual percentage yield of the individual retirement account, if any.")
    minimumBalanceToOpen: Union[float, None] = Field(description="The minimum balance to open the individual retirement account, if any.")
    minimumDailyBalance: Union[float, None] = Field(description="The minimum daily balance of the individual retirement account, if any.")

class LoanResponse(BaseModel):
    """
    Pydantic model representing a loan.
    """

    name: str = Field(description="The name of the loan.")
    term: Union[Union[int, str], None] = Field(description="The term of the loan, if any.")
    annualPercentageRate: float = Field(description="The annual percentage rate of the loan.")
    minimumPayment: Union[float, None] = Field(description="The minimum payment of the loan, if any.")
    maximumLoanAmount: Union[float, None] = Field(description="The maximum loan amount of the loan, if any.") 
    paymentPer1000Dollars: Union[float, None] = Field(description="The payment per 1000 dollars of the loan, if any.")
    interestRate: Union[float, None] = Field(description="The interest rate of the loan, if any.")

class CreditCardResponse(BaseModel):
    """
    Pydantic model representing a credit card.
    """

    name: Union[str, None] = Field(description="The name of the credit card, if any.")
    annualPercentageRate: float = Field(description="The annual percentage rate of the credit card.")
    annualFee: Union[float, None] = Field(description="The annual fee of the credit card, if any.")
    doesEarnRewards: Union[bool, None] = Field(description="Whether the credit card earns rewards, if any.")

class FeeResponse(BaseModel):
    """
    Pydantic model representing a fee.
    """

    name: str = Field(description="The name of the fee.")
    feeAmount: float = Field(description="The amount of the fee.")
    feeUnit: str = Field(description="The unit of the fee.")
    oneTime: Union[bool, None] = Field(description="Whether the fee is one-time, if any.")
    recurringInterval: Union[str, None] = Field(description="The recurring interval of the fee, if any.")

class BankResponse(BaseModel):
    """
    Pydantic model representing a bank.
    """

    bankRootDomain: str = Field(description="The root domain of the bank.")
    checkingAccounts: Union[List[CheckingAccountResponse], None] = Field(default_factory=list)
    savingsAccounts: Union[List[SavingsAccountResponse], None] = Field(default_factory=list)
    moneyMarketAccounts: Union[List[MoneyMarketAccountResponse], None] = Field(default_factory=list)
    certificatesOfDeposit: Union[List[CertificateOfDepositResponse], None] = Field(default_factory=list)
    individualRetirementAccounts: Union[List[IndividualRetirementAccountResponse], None] = Field(default_factory=list)
    loans: Union[List[LoanResponse], None] = Field(default_factory=list)
    creditCards: Union[List[CreditCardResponse], None] = Field(default_factory=list)
    fees: Union[List[FeeResponse], None] = Field(default_factory=list)
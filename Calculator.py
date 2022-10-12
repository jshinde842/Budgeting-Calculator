"""
This Python script uses the 50/30/20 rule in Financial Budgeting to help give the user rough guidance as to what to budget and how much.
Author: Jay Shinde 

Tax Data Source: https://taxfoundation.org/2022-tax-brackets/ 
50/30/20 Rule Source: https://n26.com/en-eu/blog/50-30-20-rule
"""
class Calc:
    """
    Main Calculator Class 
    """

    #Helper Functions


    def cleanInput(dollarAmount: str) -> (float | None):
        """
        Input: dirty string that may contain non-numerical chars
        Output: float representation of cleaned dirty string, none if non-castable
        """
        dollarAmount = dollarAmount.replace("$", "")
        dollarAmount = dollarAmount.replace(",", "")
        digitsAmount = dollarAmount.replace(".", "")
        if digitsAmount.isdigit():
            res = float(dollarAmount)
        else:
            res = None
        return res
    

    def formatDollar(dollarFloat: float) -> str:
        """
        Input: float representation for dollar amount
        Output: formatted string with $ and ,
        """
        return "${:,.2f}".format(dollarFloat)


    def getTaxAmount(preTaxIncome: float) -> int:
        """
        Input: income of the user
        Output: tax percentage of the income 
        """
        if preTaxIncome >= 0:
            taxPercentage = 10
            if preTaxIncome > 10275:
                taxPercentage = 12
                if preTaxIncome > 41775:
                    taxPercentage = 22
                    if preTaxIncome > 89075:
                        taxPercentage = 24
                        if preTaxIncome > 170050:
                            taxPercentage = 32
                            if preTaxIncome > 215950:
                                taxPercentage = 35
                                if preTaxIncome > 539900:
                                    taxPercentage = 37
        return taxPercentage


    def getMonthlyFromYearly(yearlyIncome: float) -> float:
        """
        Input: Yearly Income
        Output: Monthly Income
        """
        return yearlyIncome / 12


    def getHourlyFromYearly(yearlyIncome: float) -> float:
        """
        Input: Yearly Income
        Output: Hourly Income
        """
        return yearlyIncome / 40 / 52


    def getYearlyFromMonthly(monthlyIncome: float) -> float:
        """
        Input: Monthly Income
        Output: Yearly Income
        """
        return monthlyIncome * 12


    def getHourlyFromMonthly(monthlyIncome: float) -> float:
        """
        Input: Monthly Income
        Output: Hourly Income
        """
        return monthlyIncome * 12 / 40 / 52


    def getYearlyFromHourly(hourlyIncome: float) -> float:
        """
        Input: Hourly Income
        Output: Yearly Income
        """
        return hourlyIncome * 40 * 52


    def getMonthlyFromHourly(hourlyIncome: float) -> float:
        """
        Input: Monthly Income
        Output: Yearly Income
        """
        return hourlyIncome * 40 * 52 / 12
    

    #Initialize variables
    preTaxIncome = inputIncome = taxPercentage = incomeType = incomeMinus401k = 0
    hourlyWage = None

    #Let user choose what income to use for the calculation.
    print("================================================")
    print("Welcome, use this tool to give you a rough idea of how you should be spending your paychecks.")
    print("================================================\n")
    print("How would you like to enter your income?\n")
    print("1 : Hourly Income")
    print("2 : Monthly Income")
    print("3 : Annual Income\n")
    while incomeType == 0:
        incomeSelect = input("Enter 1, 2, or 3: ")
        if incomeSelect == "1":
            incomeType = 1
        elif incomeSelect == "2":
            incomeType = 2
        elif incomeSelect == "3":
            incomeType = 3
        else:
            print("Please enter a valid option.\n")

    #Prompt user for their income
    if incomeType == 1:             #Hourly
        hourlyIncome = cleanInput(input("What is your Hourly Income? Enter: "))
        while hourlyIncome == None: 
            print("Sorry, that's not a valid income. Try Again.")
            hourlyIncome = cleanInput(input("What is your Hourly Income? Enter: "))
        preTaxIncome = inputIncome = getYearlyFromHourly(hourlyIncome)
        monthlyIncome = getMonthlyFromHourly(hourlyIncome)
    elif incomeType == 2:           #Monthly
        monthlyIncome = cleanInput(input("What is your Monthly Income? Enter: "))
        while monthlyIncome == None:
            print("Sorry, that's not a valid income. Try Again.")
            monthlyIncome = cleanInput(input("What is your Monthly Income? Enter: "))
        preTaxIncome = inputIncome = getYearlyFromMonthly(monthlyIncome)
        hourlyIncome = getHourlyFromMonthly(monthlyIncome)
    elif incomeType == 3:           #Annually
        preTaxIncome = inputIncome = cleanInput(input("What is your Annual Income? Enter: "))
        while preTaxIncome == None:
            print("Sorry, that's not a valid income. Try Again.")
            preTaxIncome = inputIncome = cleanInput(input("What is your Annual Income? Enter: "))
        hourlyIncome = getHourlyFromYearly(preTaxIncome)
        monthlyIncome = getMonthlyFromYearly(preTaxIncome)

    # Does the user have a 401k? If so calculate contribution and deduct from pre-tax income
    user401k = input("Do you have a 401(k) Account? Enter Y or N : ").lower()
    if user401k == "y" or user401k == "yes":
        percentMatch401kSalary = float(input("What percent does your company maximally match your salary? Example: 6 Percent = 6. Enter : "))
        percentMatch401kCompany = float(input("What percent does your company maximally match your contribution? Example: 100 Percent = 100. Enter : "))
        companyMatchingPercentage = percentMatch401kCompany/100
        user401kContribution = company401kContribution = preTaxIncome * (percentMatch401kSalary/100)
        company401kContribution *= companyMatchingPercentage
        yearly401kIn = user401kContribution + company401kContribution  #calculate amount to go into 401k yearly
        preTaxIncome -= yearly401kIn                                   #update income
    else:
        yearly401kIn = 0

    #Calculate Post-Tax Income 
    incomeMinus401k = preTaxIncome  
    taxPercentage = getTaxAmount(preTaxIncome)
    postTaxIncome = preTaxIncome - (preTaxIncome * taxPercentage / 100)

    # Use 50/20/30 Rule for Income Split
    yearlyNeeds = postTaxIncome * 0.5                       # 50% : Needs
    monthlyNeeds = getMonthlyFromYearly(yearlyNeeds)        #
    yearlyWants = postTaxIncome * 0.3                       # 30% : Wants
    monthlyWants = getMonthlyFromYearly(yearlyWants)        #
    yearlySavings = postTaxIncome * 0.2                     # 20% : Savings
    monthlySavings = getMonthlyFromYearly(yearlySavings)    #

    #print results in format
    print(
        "========================RESULTS========================\n",
        "Annual Income : ",formatDollar(inputIncome),"\n",
        "Monthly Income : ",formatDollar(monthlyIncome),"\n",
        "Hourly Income : ",formatDollar(hourlyIncome),"\n\n",
        "Now let's deduct your 401(k) contributions.","\n",
        "Annual 401(k) Contributions : ",formatDollar(yearly401kIn),"\n",
        "Annual Income after 401(k) deductions : ", formatDollar(incomeMinus401k),"\n\n",
        "Now let's tax your income.","\n",
        "Your tax bracket gets you taxed at ",taxPercentage,"%\n",
        "Annual Income after Tax and 401(k) deductions : ",formatDollar(postTaxIncome),"\n",
        "Monthly Income after Tax and 401(k) deductions : ",formatDollar(getMonthlyFromYearly(postTaxIncome)),"\n",
        "Hourly Income after Tax and 401(k) deductions : ",formatDollar(getHourlyFromYearly(postTaxIncome)),"\n\n",
        "Let's calculate how you should be spending your money according to the 50/30/20 Rule\n\n",
        "'NEEDS' are those bills that you absolutely must pay and are the things necessary for survival. Examples are Rent, Utilities, Car payments, Groceries, and more.\n",
        "Your 'needs' category has a annual budget of ",formatDollar(yearlyNeeds), " or ",formatDollar(monthlyNeeds), " monthly.\n\n",
        "'WANTS' Wants are all the things you spend money on that are not absolutely essential. Examples are Dinner Out, Weekends out, Concerts, and more.\n",
        "Your 'wants' category has a annual budget of ",formatDollar(yearlyWants), " or ",formatDollar(monthlyWants), " monthly.\n\n",
        "'SAVINGS' is a category where you put this money towards High-Yield Savings Accounts or Retirement/Investment Accounts. Examples are HYSA with APY of 2.15% or an Investment Account that trades ETFs.\n",
        "Your 'savings' category has a annual budget of ",formatDollar(yearlySavings), " or ",formatDollar(monthlySavings), " monthly.\n",
        "======================================================="
    )
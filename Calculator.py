"""
This Program takes returns a plan to divvy up income into buckets pre-set by the user.
Input: Pre-Tax Yearly Income
Output: Income Plan

Author: Jay Shinde 2022
"""
class Calc:

    #Helper Functions

    """
    Input: dirty string containing chars that cannot be casted to type float
    Output: float type representing a cleaned version of string
    """
    def cleanInput(dollarAmount):
        dollarAmount = dollarAmount.replace("$", "")
        dollarAmount = dollarAmount.replace(",", "")
        if dollarAmount.isdigit():
            res = float(dollarAmount)
        else:
            res = None
        return res
    """
    Input: float representation for dollar amount
    Output: formatted string with $ and ,
    """
    def formatDollar(dollarFloat):
        return "${:,.2f}".format(dollarFloat)

    """
    Input: Income of the user of type float
    Output: tax percentage of the income by bracket of type int
    Tax Data Source: https://taxfoundation.org/2022-tax-brackets/
    """
    def getTaxAmount(preTaxIncome):
        if preTaxIncome > 0:
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

    """
    Input: Yearly Income of type float
    Output: Monthly Income of type float
    """
    def getMonthlyFromYearly(yearlyIncome):
        return yearlyIncome / 12

    """
    Input: Yearly Income of type float
    Output: Hourly Income of type float
    """
    def getHourlyFromYearly(yearlyIncome):
        return yearlyIncome / 40 / 52

    """
    Input: Monthly Income of type float
    Output: Yearly Income of type float
    """
    def getYearlyFromMonthly(monthlyIncome):
        return monthlyIncome * 12

    """
    Input: Monthly Income of type float
    Output: Hourly Income of type float
    """
    def getHourlyFromMonthly(monthlyIncome):
        return monthlyIncome * 12 / 40 / 52

    """
    Input: Hourly Income of type float
    Output: Yearly Income of type float
    """
    def getYearlyFromHourly(hourlyIncome):
        return hourlyIncome * 40 * 52

    """
    Input: Monthly Income of type float
    Output: Yearly Income of type float
    """
    def getMonthlyFromHourly(hourlyIncome):
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
            print("Please pick a valid option.\n")

    #Prompt user for their income

    if incomeType == 1: #Hourly
        hourlyIncome = cleanInput(input("What is your Hourly Income? Enter: "))
        while hourlyIncome == None: 
            print("Sorry, that's not a valid income. Try Again.")
            hourlyIncome = cleanInput(input("What is your Hourly Income? Enter: "))
        preTaxIncome = inputIncome = getYearlyFromHourly(hourlyIncome)
        monthlyIncome = getMonthlyFromHourly(hourlyIncome)
    elif incomeType == 2: #Monthly
        monthlyIncome = cleanInput(input("What is your Monthly Income? Enter: "))
        while monthlyIncome == None:
            print("Sorry, that's not a valid income. Try Again.")
            monthlyIncome = cleanInput(input("What is your Monthly Income? Enter: "))
        preTaxIncome = inputIncome = getYearlyFromMonthly(monthlyIncome)
        hourlyIncome = getHourlyFromMonthly(monthlyIncome)
    elif incomeType == 3: #Annually
        preTaxIncome = inputIncome = cleanInput(input("What is your Annual Income? Enter: "))
        while preTaxIncome == None:
            print("Sorry, that's not a valid income. Try Again.")
            preTaxIncome = inputIncome = cleanInput(input("What is your Annual Income? Enter: "))
        hourlyIncome = getHourlyFromYearly(preTaxIncome)
        monthlyIncome = getMonthlyFromYearly(preTaxIncome)

    # Does the user have a 401k? If so calculate contribution

    user401k = input("Do you have a 401(k) Account? Enter Y or N : ")
    if user401k == "Y":
        percentMatch401kSalary = float(input("What percent does your company maximally match of your salary? Example: 6 Percent = 6. Enter : "))
        percentMatch401kCompany = float(input("What percent does your company maximally match of your contribution? Example: 100 Percent = 100. Enter : "))
        companyMatchingPercentage = percentMatch401kCompany/100
        user401kContribution = company401kContribution = preTaxIncome * (percentMatch401kSalary/100)
        company401kContribution *= companyMatchingPercentage

        #calculate amount to go into 401k yearly
        yearly401kIn = user401kContribution + company401kContribution  

        #update income
        preTaxIncome -= yearly401kIn     
    else:
        yearly401kIn = 0


    #Calculate Post-Tax Income 
    incomeMinus401k = preTaxIncome  
    taxPercentage = getTaxAmount(preTaxIncome)
    postTaxIncome = preTaxIncome - (preTaxIncome * taxPercentage / 100)
    postTaxMonthlyIncome = postTaxIncome / 12

    # Use 50/20/30 Rule for Income Split

    # 50% : Needs
    yearlyNeeds = postTaxIncome * 0.5
    monthlyNeeds = postTaxMonthlyIncome * 0.5
    # 30% : Wants
    yearlyWants = postTaxIncome * 0.3
    monthlyWants = postTaxMonthlyIncome * 0.3
    # 20% : Savings
    yearlySavings = postTaxIncome * 0.2
    monthlySavings = postTaxMonthlyIncome * 0.2


    #print results
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
        "Let's calculate how you should be spending your money according to the 50/20/30 Rule\n\n",
        "'NEEDS' are those bills that you absolutely must pay and are the things necessary for survival. Examples are Rent, Utilities, Car payments, Groceries, and more.\n",
        "Your 'needs' category has a annual budget of ",formatDollar(yearlyNeeds), " or ",formatDollar(monthlyNeeds), " monthly.\n\n",
        "'WANTS' Wants are all the things you spend money on that are not absolutely essential. Examples are Dinner Out, Weekends out, Concerts, and more.\n",
        "Your 'wants' category has a annual budget of ",formatDollar(yearlyWants), " or ",formatDollar(monthlyWants), " monthly.\n\n",
        "'SAVINGS' is a category where you put this money towards High-Yield Savings Accounts or Retirement/Investment Accounts. Examples are HYSA with APY of 2.15% or an Investment Account that trades ETFs.\n",
        "Your 'savings' category has a annual budget of ",formatDollar(yearlySavings), " or ",formatDollar(monthlySavings), " monthly.\n",
        "======================================================="
    )
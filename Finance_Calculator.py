import math, sys, argparse

def NumMonths(cred_prin, payment, inter):
    nom_rate = (inter / 100) / 12
    return math.ceil(math.log(payment / (payment - nom_rate * cred_prin), (1 + nom_rate)))

def AnnuityPayment(cred_prin, months, inter):
    nom_rate = (inter / 100) / 12
    return math.ceil(cred_prin * ((nom_rate * (1 + nom_rate)**months) / ((1 + nom_rate)**months - 1)))

def Credit_Principal(payment, months, inter):
    nom_rate = (inter / 100) / 12
    return math.ceil(payment / ((nom_rate * (1 + nom_rate)**months) / ((1 + nom_rate)**months - 1)))

def DiffPayment(cred_prin, months, inter):
    nom_rate = (inter / 100) / 12
    for n in range(1, months + 1):
        dict_diffpayments[n] = math.ceil(cred_prin / months + nom_rate * (cred_prin - cred_prin * ( n - 1) / months))

# Start of the Final Version using command line arguements:

# Set up arguement parser:
parser = argparse.ArgumentParser()

# Set up supportive arguments for --diff and --annuity
# Required arguments:
parser.add_argument("--interest", type=float, help="Interest rate")
parser.add_argument("--type", choices=["diff", "annuity"], help="--type=diff or --type=annuity calculations")

# Optional args, depending on the calculation (thus the default=0)
parser.add_argument("--principal", type=int, help="Total Principal", default=0)
parser.add_argument("--periods", type=int, help="Number of months", default=0)
parser.add_argument("--payment", type=int, help="Monthly payment", default=0)

# Get all arguments:
args = parser.parse_args()

# Initialize the dictionary to hold differential payment info
dict_diffpayments = {}

# check for 4 arguments and if any of the int/floats are negative:
if len(sys.argv) < 4:
    print("Incorrect parameters")
    sys.exit()
elif args.interest == None:
    print('Incorrect parameters')
    sys.exit()
elif args.principal < 0 or args.periods < 0 or args.payment < 0 or args.interest < 0.0:
    print("Incorrect Parameters")
    sys.exit()

if args.type == 'diff':
    DiffPayment(args.principal, args.periods, args.interest)
    total_paid = 0
    for k in sorted(dict_diffpayments.keys()):
        total_paid += dict_diffpayments[k]
        print('Month {}: paid out {}'.format(k, dict_diffpayments[k]))
    print('Overpayment = {}'.format(total_paid - args.principal))
elif args.type == 'annuity':
    if not args.payment:
        period_payment = AnnuityPayment(args.principal, args.periods, args.interest)
        print('Your annuity payment = {}!'.format(period_payment))
        print('Overpayment = {}'.format(period_payment * args.periods - args.principal))
    elif not args.periods:
        total_months = NumMonths(args.principal, args.payment, args.interest)
        years = int(total_months / 12)
        months = math.ceil((round(total_months / 12, 2) - years) * 12)
        if total_months < 12:
            print('You need {} months to repay this credit!'.format(total_months))
        elif total_months % 12 == 0:
            print('You need {} year(s) to repay this credit!'.format(years))
        else:
            print('You  need {} year(s) and {} month(s) to repay this credit!'.format(years, months))
        print('Overpayment = {}'.format(total_months * args.payment - args.principal))
    elif not args.principal:
        principal = Credit_Principal(args.payment, args.periods, args.interest)
        print('Your credit principal = {}!'.format(principal))
        print('Overpayment = {}'.format(principal - args.principal))

'''
Previous Versions of challenge worked this way:

calculation = input('What do you want to calculate?\n'\
                'type "n" - for count of months\n'\
                'type "a" - for annuity monthly payment,\n'\
                'type "p" - for credit principal')

if calculation == 'n':
    principal = int(input('Enter credit principal: '))
    monthly_payment = float(input('Enter monthly payment: '))
    interest_rate = float(input('Enter credit interest: '))
    total_months = NumMonths(principal, monthly_payment, interest_rate)
    years = int(total_months / 12)
    months = math.ceil((round(total_months / 12, 2) - years) * 12)
    if total_months < 12:
        print('You need {} months to repay this credit!'.format(total_months))
    elif total_months % 12 == 0:
        print('You need {} year(s) to repay this credit!'.format(years))
    else:
        print('You  need {} year(s) and {} month(s) to repay this credit!'.format(years, months))

elif calculation == 'a':
    principal = int(input('Enter credit principal: '))
    periods = int(input('Enter count of periods: '))
    interest_rate = float(input('Enter credit interest: '))
    print('Your annuity payment = {}'.format(AnnuityPayment(principal, periods, interest_rate)))

elif calculation == 'p':
    monthly_payment = float(input('Enter monthly payment: '))
    periods = int(input('Enter count of periods: '))
    interest_rate = float(input('Enter credit interest: '))
    print('Your credit principal = {}'.format(Credit_Principal(monthly_payment, periods, interest_rate)))
'''

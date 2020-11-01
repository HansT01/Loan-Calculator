import sys
from math import log, ceil, floor

# Make a list of arguments for easier use
args = []


def die():
    print('Incorrect parameters')
    sys.exit()


if len(sys.argv) == 5:
    for i in sys.argv[1:5]:
        args.append(i)
else:
    die()

# Create variables
var = {'payment_type': None, 'payment': None,
       'principal': None, 'periods': None, 'interest': None}

# Check the list for arguments and append them to the corresponding variables
for i in args:
    if '--type' in i:
        var['payment_type'] = i[(i.index('=') + 1):]
    if '--payment' in i:
        var['payment'] = float(i[(i.index('=') + 1):])
    if '--principal' in i:
        var['principal'] = float(i[(i.index('=') + 1):])
    if '--periods' in i:
        var['periods'] = float(i[(i.index('=') + 1):])
    if '--interest' in i:
        var['interest'] = float(i[(i.index('=') + 1):])

empty_var = []

for i in var:
    if var[i] == None:
        empty_var.append(i)
    if type(var[i]) == float:
        if var[i] <= 0:
            die()

# D = P/n + i*(P - P*(m-1)/n)
# D = mth differentiated payment
# i = nominal interest rate
# n = number of payments
# m = current repayment month

if len(empty_var) != 1 or empty_var[0] == 'interest':
    die()
else:
    P = var['principal']
    D = var['payment']
    n = var['periods']
    i = var['interest'] / 1200


if var['payment_type'] == 'annuity':
    if empty_var[0] == 'payment':
        D = ceil(((P * i * pow(1 + i, n)) / (pow(1 + i, n) - 1)))
        print(f'Your annuity payment = {D}!')

        overpayment = D * n - P
        print(f'Overpayment = {ceil(overpayment)}')

    elif empty_var[0] == 'principal':
        P = D / ((i * pow(1 + i, n)) / (pow(1 + i, n) - 1))
        print(f'Your loan principal = {P:.0f}!')

        overpayment = D * n - P
        print(f'Overpayment = {ceil(overpayment)}')

    elif empty_var[0] == 'periods':
        n = log(D / (D - i * P), 1 + i)
        rounded_n = ceil(n)

        years = floor(rounded_n / 12)
        months = rounded_n % 12

        print(
            f'It will take {years} year' + 's' * (years != 1) + f' and {months} month' * (months != 0) + 's' * (months != 1 & months != 0) + ' to repay this loan!')

        overpayment = D * rounded_n - P
        print(f'Overpayment = {ceil(overpayment)}')

elif var['payment_type'] == 'diff':
    if empty_var[0] == 'payment':
        payment_list = []

        for m in range(1, int(n)+1):
            D = P/n + i*(P - P*(m-1)/n)
            payment_list.append(ceil(D))
            print(f'Month {m}: payment is {ceil(D)}')

        overpayment = sum(payment_list) - P
        print(f'Overpayment = {ceil(overpayment)}')

    else:
        die()
else:
    die()

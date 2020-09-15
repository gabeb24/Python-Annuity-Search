"""P4: Data Translator I project, CPSC 5061, Seattle University
This is the second program that finds the amount of the monthly annuity payment using bisection search.
"""
from math import e

# Which test case are we running?
test_case = 1

def annuity_value(initial_monthly_payment):
    # First figure out the bracket: low can be $0, high can be total which we know is too high
    # While we're at it we can calculate the npv of the cash flows, since this won't change during the search
    total = 0.0
    cf_npv = 0.0
    cf_file = open(dense_cf_filename, 'r')
    rates_file = open(dense_rates_filename, 'r')
    months = 1
    for cf_line, rate_line in zip(cf_file, rates_file):
        rate = float(rate_line) / 12.0 / 100.0
        cash_flow = float(cf_line)
        total += cash_flow
        disc = e ** (-rate * months)
        curr_npv = cash_flow * disc
        cf_npv += curr_npv
        #if cash_flow != 0.0:
        #    print('months:', months, 'cashflow:', cash_flow, 'discount:', disc, 'npv:', curr_npv)
        months += 1
    cf_file.close()
    rates_file.close()
    #print('NPV of customer-provided cash flows: $%.2f' % cf_npv)
    #print('Total customer-provided cash flows: $%.2f' % total)

    rates_file = open(dense_rates_filename, 'r')
    months = 1
    npv = cf_npv
    payment = initial_monthly_payment
    for rate_line in rates_file:
        rate = float(rate_line) / 12.0 / 100.0
        disc = e**(-rate * months)
        pmtnpv = payment * disc
        npv -=  pmtnpv
        #print('months: {:2d}, rate: {:.8f}, disc: {:.8f}, pmt: {:.2f}, pmt_npv: {:.2f}, ttl_npv: {:.2f}'.format(
        #    months, rate, disc, payment, pmtnpv, npv))
        if months % 12 == 0:
            payment += round(payment * inflation, 2)
        months += 1
    rates_file.close()
    return npv


# Following are instructor-provided file:
#   p4_testN_terms.csv:
#     line 1 column titles: term,inflation
#     line 2 values: term is number of months of annuity payments, inflation is annual inflation adjustment
annuity_terms_filename = 'p4_test%d_terms.csv' % test_case

# Following are the output files created by the p4_create_dense_files program. These have one line for every month
dense_cf_filename = 'p4_test%d_dense_cf.txt' % test_case
dense_rates_filename = 'p4_test%d_dense_rates.txt' % test_case

# Get the annuity terms
terms_file = open(annuity_terms_filename, 'r')
terms_file.readline()  # skip the first line of column titles
line = terms_file.readline()  # this is the line with the numbers, e.g., '120,3.0'
annuity_term, inflation = line.split(',')  # split into our two values (as strings), e.g., '120', '3.0'
annuity_term = int(annuity_term)  # convert to an integer from a string
inflation = float(inflation) / 100.0  # convert to a float and ratio from a string with percent number
terms_file.close()

lo, hi = 0.0, 1_000_000.0

# Now we have a low that is too low and a high that is too high, so we can use bisection search
#print('\nSearching for correct beginning monthly annuity payment:')
last_guess = lo
guess = hi
while abs(guess - last_guess) > 0.01:
    last_guess = guess
    guess = round((lo + hi) / 2, 2)
    npv = annuity_value(guess)
    if npv < 0.0:
        hi = guess
    else:
        lo = guess

# Print out the details of the payments
payment = guess
print('\nFirst year pay $%.2f per month' % payment)
total_payments = 0
months = 0
for months in range(12, annuity_term, 12):
    total_payments += 12 * payment
    payment += payment * inflation
    print('Next year pay $%.2f per month' % payment)
total_payments += (annuity_term - months) * payment
print('For a total of $%.2f' % total_payments)
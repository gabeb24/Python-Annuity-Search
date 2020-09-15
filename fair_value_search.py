# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 14:32:37 2020

@author: Gabe

"""



test_case = 1

annuity_terms_file  = '/Users/Gabe/Desktop/P4/p4_test%d_terms.csv' % test_case

annuity_file = open(annuity_terms_file, 'r')
annuity_file.readline()  # skip the first line of column titles
line = annuity_file.readline()  # this is the line with the numbers
annuity_term, inflation = line.split(',')  # split into our two values (as strings), e.g., '120', '3.0'
annuity_term = int(annuity_term)  # convert to an integer from a string
inflation = float(inflation) / 100.0  # convert to a float and ratio from a string with percent number
annuity_file.close()




from math import e

total = 0.0
cf_npv = 0.0

months = 1

cf_file = open('/Users/Gabe/Desktop/P4/dense_cf.txt', 'r')
rate_file = open('/Users/Gabe/Desktop/P4/dense_rates.txt', 'r')


#iterating through all 26 cash flows and rates to calculate the NPV of all cash flows and total cash flows
for line_cf, line_rate in zip(cf_file, rate_file):
    cash_flow = float(line_cf)
    rate = float(line_rate) 
    total += cash_flow #totaling all cash flows
    cf_npv += cash_flow * e ** (-rate / 100 / 12 * months) #calculating the npv of each cash flow
    months += 1
    
cf_file.close()

print('NPV customer-provided cash flows: $%.2f' % cf_npv)
print('Total customer-provided cash flows: $%.2f' % total)

months = 1
low = 0.0
high = total
iter_count = 1

#pretend last guess is low and first guess is high
last_guess = low
guess = high

rate2 = (rate / 100 / 12)
disc = e ** (-rate2 * months)


print('Finding correct beginning monthly annuity payment:')





while abs(guess - last_guess) > 0.01:
    last_guess = guess
    guess = round((low + high) / 2, 2)
    npv = cf_npv - guess * disc
    print('With annuity of', (low, '+' ,high), '/', 2, '=', guess, ',' 'NPV is', npv)
   
    
    
#this is our annuity value function. npv = annuity(value(guess))
    rates_file = open(rate_file, 'r') #read in all the interest rates into the function
    months = 1
    payment = guess
    #every month has a payment, so we keep track of the NPV for all months
    npv = cf_npv
    for rate_line in rate_file:
        rate = float(rate) / 12.0 / 100/0
        disc = e** (-rate * months)
        payment_npv = payment * disc #The npv each month for a specific payment
        npv -= payment_npv #accumulation of npv as a negative cash flow since we pay it out
    
    #inflation
    if months % 12 == 0:
        payment += round(payment * inflation, 2)
        months += 1
        


    if npv < 0.0:
        high = guess
    else:
        low = guess
        guess = round((low + high) / 2, 2)

    

   
    
    

    
   
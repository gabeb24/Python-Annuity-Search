# -*- coding: utf-8 -*-


#OSMBA 5061

#P4 Data Translator 1

#Gabe Boucaud



test_case = 1

annuity_terms_file  = '/Users/Gabe/Desktop/P4/p4_test%d_terms.csv' % test_case
cash_flows_file = '/Users/Gabe/Desktop/P4/p4_test%d_cash_flows.csv' % test_case
rates_file = '/Users/Gabe/Desktop/P4/p4_test%d_interest_rates.csv' % test_case

annuity_file = open(annuity_terms_file, 'r')
annuity_file.readline()  # skip the first line of column titles
line = annuity_file.readline()  # this is the line with the numbers
annuity_term, inflation = line.split(',')  # split into our two values (as strings), e.g., '120', '3.0'
annuity_term = int(annuity_term)  # convert to an integer from a string
inflation = float(inflation) / 100.0  # convert to a float and ratio from a string with percent number
annuity_file.close()


cf_input_file = open(cash_flows_file, 'r') #opens the cash flow csv file
cf_file = open('dense_cf', 'w') #opens our txt file

month = 1

for line in cf_input_file:
    #for each line in the original file:
    #separate the columns with a commma
    #turn the month into an int and amount into a float
    cf_month, cf_amount = line.split(',')
    cf_month = int(cf_month)
    cf_amount = float(cf_amount)
    #if you come across a month value where cf_month is greater than month
    #write in 0.0 for the cf_amount of that month and increment month
    while month < cf_month:
        cf_file.write(str(0.0) + '\n')
        month += 1
    #write in the cf_amount and increment month by 1
    cf_file.write(str(cf_amount) + '\n')
    month += 1
while month <= annuity_term:
    cf_file.write(str(0.0) + '\n')
    month += 1
cf_input_file.close()
cf_file.close()

#Continue to fill in the month where the cash flow is 0 until we get to the annuity term(26)

rates_input_file = open(rates_file, 'r')
rates_dense_file = open('dense_rates', 'w')

no_rate = ' '
no_month = ' '
prev_line = " "
last_line = " "
month_r = 1
for line_r in rates_input_file:
    rates_month, rate = line_r.split(',')
    rates_month = int(rates_month)
    rate = float(rate)
    line_r = line_r[:-1]
    
    while month_r < rates_month:
        rates_dense_file.write(str(no_rate) + '\n')
        month_r += 1
  
    prev_line = line_r
    no_month, no_rate = prev_line.split(',')
    no_month = int(no_month)
    no_rate = float(no_rate)
        
    rates_dense_file.write(str(rate) + '\n')
    month_r += 1
        
while month_r <= annuity_term:
    last_line = rate
    rates_dense_file.write(str(last_line) + '\n')
    month_r += 1
   
    
rates_input_file.close()
rates_dense_file.close()
    
    
    
    
    
        
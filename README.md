Date: December 15th, 2021
Author: Alejandro Avella

This program reads a series of transactions from a CSV file, handles deposits, withdrawals, disputes, resolves and chargebacks, and then outputs the state of clients accounts.

# Usage
python3 payment_engine.py transactions.csv > client_accounts.csv

# Requirements
Python 3.4+
No specific packages. It uses sys and csv standard libraries.

# Input file
The input file has four fields: type, client, tx, amount

# Output file
The output file has five fields: client, available, held, total, locked

# Testing
The program was tested with input transactions of the type deposit, withdrawal, dispute, resolve and chargeback. Positive and negative scenarios were considered.  See transactions.csv file.

# About the program
It has 3 main parts:
1. Reads input csv file.
2. Process transactions with payment_engine function. The output is maintained in a dictionary of dictionaries where the key is the client id.
3. Writes output to standard output so that the results can be redirected to an output csv file.
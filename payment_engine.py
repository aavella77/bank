import sys
import csv

""" Global variables """
input_headers = [
    "type",
    "client",
    "tx",
    "amount"
]

output_headers = [
    "client",
    "available",
    "held",
    "total",
    "locked"
]


def read_input_file(filename):
    with open(filename) as f:
        reader = csv.DictReader(f, fieldnames=input_headers)
        header = next(reader)
        # Check file as empty
        if header is not None:
            output = payment_engine(reader)
    return output


def intiatialze_client(client, output):
    """output is a dictionary of dictionaries with client as the key"""
    output[client] = {}
    output[client]["available"] = 0
    output[client]["held"] = 0
    output[client]["total"] = 0
    output[client]["locked"] = "false"
    return output


def payment_engine(reader):
    output = {}
    """ Process on transaction at a time """
    for row in reader:
        if row["client"] not in output:
            output = intiatialze_client(row["client"], output)
        if row["type"] == "deposit":
            if float(row["amount"]) >= 0.0:
                output[row["client"]]["available"] += float(row["amount"])
                output[row["client"]]["total"] += float(row["amount"])
        elif row["type"] == "withdrawal":
            """ if client does not have sufficient available funds it should fail """
            if (output[row["client"]]["available"] - float(row["amount"])) >= 0:
                output[row["client"]]["available"] -= float(row["amount"])
                output[row["client"]]["total"] -= float(row["amount"])
        elif row["type"] == "dispute":
            tx_disputed = row["tx"]
            tx_disputed_amount = find_tx(tx_disputed)
            output[row["client"]]["available"] -= float(tx_disputed_amount)
            output[row["client"]]["held"] += float(tx_disputed_amount)
        elif row["type"] == "resolve":
            tx_resolved = row["tx"]
            tx_resolved_amount = find_tx(tx_resolved)
            output[row["client"]]["available"] += float(tx_resolved_amount)
            output[row["client"]]["held"] -= float(tx_resolved_amount)
        elif row["type"] == "chargeback":
            tx_chargeback = row["tx"]
            tx_chargeback_amount = find_tx(tx_chargeback)
            output[row["client"]]["total"] -= float(tx_chargeback_amount)
            output[row["client"]]["held"] -= float(tx_chargeback_amount)
            output[row["client"]]["locked"] = "true"
    return output


def find_tx(transaction):
    with open(filename) as f:
        reader = csv.DictReader(f, fieldnames=input_headers)
        header = next(reader)
        # Check file as empty
        if header is not None:
            for row in reader:
                if row["tx"] == transaction:
                    return row["amount"]
        """ TODO: if transaction does not exist assuming an error on partner """


def write_to_standard_out(output):
    writer = csv.DictWriter(
        sys.stdout, fieldnames=output_headers)
    writer.writeheader()
    for client, data in output.items():
        client_output = {
            "client": client,
            "available": round(output[client]["available"], 4),
            "held": round(output[client]["held"], 4),
            "total": round(output[client]["total"], 4),
            "locked": output[client]["locked"]
        }
        writer.writerow(client_output)


if __name__ == "__main__":
    """ Validate input command and display usage """
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 payment_engine.py transactions.csv > client_accounts.csv\n")
    filename = sys.argv[1]
    output = read_input_file(filename)
    write_to_standard_out(output)

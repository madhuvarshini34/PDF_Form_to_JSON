from datetime import datetime
from checkbox_parser import CheckboxParser
import re

def parse_text_to_json(text, pdf_path):
    lines = text.split("\n")
    
    data = {
        "alert_type": "N/A",
        "status": "N/A",
        "custom_data": {
            "Name": "N/A",
            "Last four digits of card": "N/A",
            "Amount": "N/A",
            "Transaction date": "N/A",
            "Merchant name": "N/A",
            "Transaction was not authorized": "N/A",
            "At the time of the transaction the card was:": "N/A",
            "Have you always had possession of your ATM/Debit card?": "N/A",
            "Are you aware of the transaction?": "N/A",
            "date you lost your card": "N/A",
            "Time you lost your card": "N/A",
            "Date you realised card was stolen": "N/A",
            "Time you realised card was stolen": "N/A",
            "Do you know who made the transaction": "N/A",
            "When was the last time you used your card": "N/A",
            "Last transaction amount": "N/A",
            "Where do you normally store your card": "N/A",
            "where do you normally store your PIN": "N/A",
            "Other items that were stolen": "N/A",
            "Have you filed police report": "N/A",
            "Officer name": "N/A",
            "Report number": "N/A",
            "Suspect name": "N/A",
            "Date": "N/A",
            "contact number": "N/A",
            "Reason for dispute": "N/A"
        },
        "instruments": [],
        "entities": [{"entity_id": "N/A"}],
        "events": [],
        "title": "N/A",
        "created_at": "N/A",
        "alert_id": "N/A"
    }

    # Extract checkbox selection
    checkbox_parser = CheckboxParser(pdf_path)
    checkbox_value = checkbox_parser.extract_ticked_checkbox()
    data["custom_data"]["At the time of the transaction the card was:"] = checkbox_value

    for line in lines:
        if "Transaction was not authorized" in line:
            data["custom_data"]["Transaction was not authorized"] = lines[lines.index(line) + 1].strip()

        if "Have you always had possession of your ATM/Debit card?" in line:
            data["custom_data"]["Have you always had possession of your ATM/Debit card?"] = lines[lines.index(line) + 1].strip()
            
        if "Are you aware of the transaction?" in line:
            data["custom_data"]["Are you aware of the transaction?"] = lines[lines.index(line) + 1].strip()
            
        if "Where do you normally store your card?" in line:
            data["custom_data"]["Where do you normally store your card"] = lines[lines.index(line) + 1].strip()

        if "Where do you normally store your PIN?" in line:
            data["custom_data"]["where do you normally store your PIN"] = lines[lines.index(line) + 1].strip()

        if "Why are you disputing the transaction(s)?" in line:
            data["custom_data"]["Reason for dispute"] = lines[lines.index(line) + 1].strip()

        if "Date the error was first noticed" in line:
            raw_date = lines[lines.index(line) + 1].strip()

            try:
                # Convert raw date to MM/DD/YYYY format
                formatted_date = datetime.strptime(raw_date, "%m.%d.%y").strftime("%m/%d/%Y")
            except ValueError:
                formatted_date = raw_date  # Keep original if conversion fails

            data["custom_data"]["Date"] = formatted_date

        card_match = re.search(r"(\d+\s\d+\s\d+\s\d+)", line)
        if card_match:
            last_four = int(card_match.group(1)[-4:])
            data["custom_data"]["Last four digits of card"] = last_four

        acc_match = re.search(r"Account Number:\s*([\dX*]+)", line)
        if acc_match:
            account_number = acc_match.group(1)
            data["instruments"].append(account_number)

        if "$" in line:
            parts = line.split()
            if len(parts) >= 4:
                date, amount, merchant_info = parts[0], parts[1], " ".join(parts[2:])
        
                try:
                    # Convert amount to float after removing "$" and "," (for thousands)
                    numeric_amount = float(amount.replace('$', '').replace(',', ''))
                except ValueError:
                    numeric_amount = None  # If conversion fails, store None

                data["events"].append({
                    "event_type": "N/A",
                    "event_id": "N/A",
                    "date": date,
                    "amount": numeric_amount,  # Stored as float
                    "merchant_description": merchant_info
            })

    return data

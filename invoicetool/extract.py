import re
from datetime import datetime

INVOICE_TO_REGEX_PATTERN = r"Invoice(?:\s+To)?[:]?\s*(.+)"
# DATE_REGEX_PATTERN = r"Date:?\s*(\w+ \d{4})"  # 43
# DATE_REGEX_PATTERN = r"Date\s*:?\s+(\w+ \d{4})"  # 34
# DATE_REGEX_PATTERN = r"Date:? ?(\w+ ?\d{4})"  # 21
# DATE_REGEX_PATTERN = r"Date:? ?(\w+(?:\s+)?\d{4})"  # 19
# DATE_REGEX_PATTERN = r"Date:? ?(\w+(?:\s+)?\d{2,4})"  # 18
# DATE_REGEX_PATTERN = r"Date:? ?((?:(\d{1,2}\s+)?)\w+(?:\s+)?\d{2,4})"  # 12
# DATE_REGEX_PATTERN = r"Date:? ?((?:(\d{1,2}\s+)?)\w+(?:[\s/–-]+)?(?:\w+)?(?:[\s/–-]+)?\d{2,4})"  # 4
DATE_REGEX_PATTERN = r"Date:? ?((?:(\d{1,2}\s+)?)\w+(?:[\s/–-]+)?(?:\w+)?(?:[\s/–-]+)?(?:\w+)?\s*\d{2,4})"  # 2
INVOICE_NUMBER_REGEX_PATTERN = r"Inv\s*:?\s+(\d+)"
ADDRESS_REGEX_PATTERN = (
    r"^Invoice(?:\s+To)?[:]?\s*.+((?:\n.*)*)(?=(job\s+ref|description))"
)


def extract_customer_name(text):
    if match := re.search(INVOICE_TO_REGEX_PATTERN, text, re.IGNORECASE):
        return match.group(1).strip()


def extract_customer_address(text):
    if match := re.search(ADDRESS_REGEX_PATTERN, text, re.IGNORECASE):
        return match.group(1).strip()


def extract_invoice_number(text: str) -> int:
    if match := re.search(INVOICE_NUMBER_REGEX_PATTERN, text, re.IGNORECASE):
        return int(match.group(1))


def extract_date(text: str) -> str:
    if match := re.search(DATE_REGEX_PATTERN, text, re.IGNORECASE):
        return match.group(1).strip()


def extract_date_as_datetime(text: str) -> datetime:
    if date_str := extract_date(text):
        month, year = date_str.split()
        try:
            # full date format e.g., December 2021
            return datetime.strptime(f"{month} {year}", "%B %Y")
        except ValueError:
            try:
                # abbreviated date format e.g., Dec 2021
                return datetime.strptime(f"{month[:3]} {year}", "%b %Y")
            except ValueError:
                raise ValueError("Invalid date format")


def extract_job_ref(text: str) -> str:
    if match := re.search(r"job\s+ref\s*:?\s*(.+)", text, re.IGNORECASE):
        return match.group(1).strip()

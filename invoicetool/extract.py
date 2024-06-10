import re
from datetime import datetime

INVOICE_TO_REGEX_PATTERN = r"Invoice(?:\s+To)?[:]?\s*(.+)"
DATE_REGEX_PATTERN = (
    r"Date:? ?((?:(\d{1,2}\s+)?)\w+(?:[\s/–-]+)?(?:\w+)?(?:[\s/–-]+)?(?:\w+)?\s*\d{2,4})"
)
INVOICE_NUMBER_REGEX_PATTERN = r"Inv\s*:?\s+(\d+)"
ADDRESS_REGEX_PATTERN = r"^Invoice(?:\s+To)?[:]?\s*.+((?:\n.*)*)(?=(job\s+ref|description))"
NAME_AND_ADDRESS_REGEX_PATTERN = (
    r"^Invoice(?:\s+To)?\s*[:]?\s*(.+)((?:\n(?!(job\s+ref|description)).*)*)"
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


def extract_customer_name_and_address(text: str) -> tuple[str, str | None, None]:
    name, address = None, None
    if match := re.search(NAME_AND_ADDRESS_REGEX_PATTERN, text, re.IGNORECASE | re.MULTILINE):
        name = match.group(1).strip()
        address = match.group(2).strip()
    return name, address

from dataclasses import asdict, dataclass

from invoicetool.extract import (
    extract_customer_name_and_address,
    extract_date,
    extract_invoice_number,
    extract_job_ref,
)
from invoicetool.word import WordDocument, split_invoice_on_divide


@dataclass
class Customer:
    name: str
    address: str

    def __str__(self) -> str:
        return f"Name: {self.name}\nAddress:\n({self.address})"

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)


@dataclass
class Invoice:
    invoice_number: int
    date: str
    customer: "Customer"
    description: str
    _word_document: "WordDocument"
    job_ref: str | None = None

    def __str__(self) -> str:
        return f"Invoice #{self.invoice_number}: {self.customer.name} ({self.date})"

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    @classmethod
    def from_word_document(cls, doc: WordDocument) -> "Invoice":
        text = doc.text
        header, footer = split_invoice_on_divide(text)
        name, address = extract_customer_name_and_address(footer)
        customer = Customer(
            name=name,
            address=address,
        )
        return cls(
            invoice_number=extract_invoice_number(header),
            date=extract_date(header),
            customer=customer,
            description=footer,
            _word_document=doc,
            job_ref=extract_job_ref(footer),
        )

    @property
    def raw_text(self) -> str:
        return self._word_document.text

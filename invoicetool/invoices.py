from dataclasses import asdict, dataclass


@dataclass
class Customer:
    name: str
    address: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)


@dataclass
class Invoice:
    customer: "Customer"
    invoice_number: int
    date: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

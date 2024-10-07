import strawberry

@strawberry.type
class InvoiceType:
    id: int
    owner_id: int
    amount: float
    currency: str
    metadata: str

@strawberry.input
class InvoiceCreate:
    owner_id: int
    amount: float
    currency: str
    metadata: str
import enum


class CartStatus(enum.Enum):
    OPEN = "Open"
    PENDING = "Pending"
    COMPLETED = "Completed"
    REJECTED = "Rejected"

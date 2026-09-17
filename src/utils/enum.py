from enum import Enum

class UserRole(str, Enum):
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    USER = "user"

class TicketStatus(str, Enum):
    TODO = "ToDo"
    OPEN = "Open"
    INPROGRESS = "InProgress"
    WAITING = "Waiting"
    BLOCKED = "Blocked"
    OEM = "OEM"
    CANCELLED = "Cancelled"
    DONE = "Done"
    CLOSED = "Closed"
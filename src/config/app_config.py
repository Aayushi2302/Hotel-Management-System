class AppConfig:
    DATABASE_PATH = "hotel_management.db"
    LOG_FILE_PATH = "logs.log"
    MAXIMUM_LOGIN_ATTEMPTS = 3

    # role specific constants
    ADMIN_ROLE = "admin"
    STAFF_ROLE = "staff"
    RECEPTION_ROLE = "reception"

    # password types
    DEFAULT_PASSWORD = "default"
    PERMANENT_PASSWORD = "permanent"

    # status specific constants
    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"

    # room status
    ROOM_STATUS_AVAILABLE = "available"
    ROOM_STATUS_BOOKED = "booked"
    ROOM_STATUS_INACTIVE = "inactive"
    
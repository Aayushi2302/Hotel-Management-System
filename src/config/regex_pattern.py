class RegexPattern:
    EMAIL_REGEX = r"^[a-z0-9]+@[a-z]+\.[a-z]{2,3}"
    MOBILE_NO_REGEX = r"[6-9][0-9]{9}$"
    NAME_REGEX = r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$"
    PASSWORD_PATTERN = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[@#$%&]).{8,}$"
    ROLE_REGEX = r"^([a-z]){5,}$"
    USERNAME_REGEX = r"(^user@)([a-z]{5,})"
    AGE_REGEX = r"(^[1][4-9]$)|(^[2-5][0-9]$)|60"
    ROOM_ID_REGEX = r"^ROOM[a-zA-Z0-9]+$"
from enum import Enum


class AllureTags(str, Enum):
    USER_LOGIN = "USER_LOGIN"
    ACTIONS_UI = "ACTIONS_UI"
    ACTIONS_DB = "ACTIONS_DB"


class AllureFeature(str, Enum):
    DATABASE = "Database"
    AUTHENTICATION = "Authentication"
    CATEGORY = "Category"
    SPENDS = "Spends"
    PROFILE = "Profile"


class AllureStory(str, Enum):
    CATEGORY = "Category"
    SPEND = "Spend"
    REGISTRATION = "Registration"
    AUTHENTICATION = "Authentication"
    WRONG_AUTHENTICATION = "Wrong Authentication"
    NAVIGATION = "Navigation"

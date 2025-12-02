from enum import Enum


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

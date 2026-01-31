from enum import Enum


class AllureTags(str, Enum):
    USER_LOGIN = "USER_LOGIN"
    ACTIONS_UI = "ACTIONS_UI"
    ACTIONS_DB = "ACTIONS_DB"
    ACTIONS_API = "ACTIONS_API"
    KAFKA = "Паблишинг сообщений в кафку"
    SOAP = "SOAP"


class AllureEpic(str, Enum):
    NIFFLER = "Niffler app"


class AllureFeature(str, Enum):
    DATABASE = "Database"
    AUTHENTICATION = "Authentication"
    CATEGORY = "Category"
    SPENDS = "Spends"
    PROFILE = "Profile"
    KAFKA = "Publishing messages to Kafka"
    SOAP = "Sending messages to Soap"


class AllureStory(str, Enum):
    CATEGORY = "Category"
    SPEND = "Spend"
    REGISTRATION = "Registration"
    AUTHENTICATION = "Authentication"
    WRONG_AUTHENTICATION = "Wrong Authentication"
    NAVIGATION = "Navigation"
    KAFKA_MESSAGE = "Message with User publishing to Kafka after successful registration"
    KAFKA_PRODUCING = "Filling userdata exclude auth"
    SOAP_GET_USER_INFO = 'Getting info about existing user by username'

from enum import Enum


class Days(Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class TrainType(Enum):
    SUPERFAST = "Superfast"
    FAST = "Fast"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class JourneyStatus(Enum):
    CONFIRMED = "Confirmed"
    WAITING = "Waiting"
    CANCELLED = "Cancelled"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class BirthPreference(Enum):
    LOWER = "Lower"
    MIDDLE = "Middle"
    UPPER = "Upper"
    SIDEUPPER = 'Sideupper'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHERS = "Others"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Coaches(Enum):
    AC1 = "First AC"
    AC2 = "Second AC"
    AC3 = "Third AC"
    SLEEPER = "Sleeper"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

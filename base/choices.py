from enum import Enum


class Constants:
    BOOKING_FOR_NEXT_DAYS = 10
    TOTAL_SEATS = 150


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
        return tuple((day.name, day.value) for day in cls)


class TrainType(Enum):
    SUPERFAST = "Superfast"
    FAST = "Fast"

    @classmethod
    def choices(cls):
        return tuple((train_type.name, train_type.value) for train_type in cls)


class JourneyStatus(Enum):
    CONFIRMED = "Confirmed"
    WAITING = "Waiting"
    CANCELLED = "Cancelled"

    @classmethod
    def choices(cls):
        return tuple((j_status.name, j_status.value) for j_status in cls)


class BirthPreference(Enum):
    LOWER = "Lower"
    MIDDLE = "Middle"
    UPPER = "Upper"
    SIDEUPPER = 'Sideupper'

    @classmethod
    def choices(cls):
        return tuple((birth_pref.name, birth_pref.value) for birth_pref in cls)


class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHERS = "Others"

    @classmethod
    def choices(cls):
        return tuple((gender.name, gender.value) for gender in cls)


class Coaches(Enum):
    AC1 = "First AC"
    AC2 = "Second AC"
    AC3 = "Third AC"
    SLEEPER = "Sleeper"

    @classmethod
    def choices(cls):
        return tuple((coach.name, coach.value) for coach in cls)


class Fare(Enum):
    AC1_SUPERFAST = 2080
    AC1_FAST = 1880
    AC2_SUPERFAST = 1500
    AC2_FAST = 1200
    AC3_SUPERFAST = 1200
    AC3_FAST = 800
    SLEEPER_SUPERFAST = 800
    SLEEPER_FAST = 400

    @classmethod
    def choices(cls):
        return tuple((fare.name, fare.value) for fare in cls)

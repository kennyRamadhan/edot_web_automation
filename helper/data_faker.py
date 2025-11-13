# utils/faker_data.py
from faker import Faker

class FakerData:
    fake = Faker('id_ID') 

    @classmethod
    def get_full_name(cls):
        return cls.fake.name()

    @classmethod
    def get_email(cls):
        return cls.fake.email()

    @classmethod
    def get_phone(cls):
        return cls.fake.phone_number()

    @classmethod
    def get_company(cls):
        return cls.fake.company()

    @classmethod
    def get_address(cls):
        return cls.fake.address()

    @classmethod
    def get_sentence(cls):
        return cls.fake.sentence()

    @classmethod
    def get_random_number(cls, min=1000, max=9999):
        return cls.fake.random_int(min=min, max=max)

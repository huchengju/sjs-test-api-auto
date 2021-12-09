# -*- coding: utf-8 -*-

from faker import Factory


class Data():

    def __init__(self):
        self.fake = Factory.create("zh_cn")

    def email(self):
        return self.fake.free_email()

    def phone(self):
        p = self.fake.phone_number()
        return p

    def identity(self):
        return self.fake.ssn()

    def city(self):
        return self.fake.city()

    def name(self):
        return self.fake.name()

    def bankcard(self):
        return self.fake.credit_card_number()


if __name__ == '__main__':
    D = Data()
    print(D.phone())

import hashlib
from passlib.hash import argon2
from hashids import Hashids
from flask import current_app as app

from app.model.db import DBConnection

class User:

    def __init__(self, email = None, password = None, public_id = None):
        self.db = DBConnection()

        #Pull User Data
        if public_id:
            user_info = self.db.query("""
                SELECT user_id,public_id,first_name,last_name,email,password_hash,is_verified,
                user_subscription.subscription_id IS NOT NULL AS is_premium
                FROM user_account
                LEFT JOIN user_subscription
                ON user_account.user_id = user_subscription.user_id
                WHERE public_id = %s
                GROUP BY user_account.user_id
                """,
                [User.decode_public_id(public_id)]
            )
        elif email:
            user_info = self.db.query("""
                SELECT user_id,public_id,first_name,last_name,email,password_hash,is_verified,
                user_subscription.subscription_id IS NOT NULL AS is_premium
                FROM user_account
                LEFT JOIN user_subscription
                ON user_account.user_id = user_subscription.user_id
                WHERE email = %s
                GROUP BY user_account.user_id
                """,
                [email]
            )
        else:
            raise AssertionError("Missing user credentials")

        assert len(user_info), "User not found"
        user_record = user_info[0]
        self.internal_id = user_record['user_id']
        self.public_id = User.encode_id(user_record['public_id'])
        self.full_name = user_record['first_name'] + " " + user_record['last_name']
        self.email = user_record['email']
        self.is_verified = bool(user_record['is_verified'])
        self.is_premium = user_record['is_premium']
        self.integrity = (argon2.verify(password, user_record['password_hash'])) if password else False

    def to_dict(self):
        user_dict = {
            'public_id': self.public_id,
            'full_name': self.full_name,
            'email': self.email,
            'is_verified': self.is_verified,
            'is_premium': self.is_premium,
        }

        return user_dict

    @staticmethod
    def encode_id(id):
        hashids = Hashids(salt=app.config['SECRET_KEY'], min_length=9)
        return hashids.encode(int(id))

    @staticmethod
    def decode_public_id(id):
        hashids = Hashids(salt=app.config['SECRET_KEY'], min_length=9)
        return hashids.decode(int(id))

    @staticmethod
    def new_user(first_name, last_name, email, password):
        assert first_name, "Missing User first_name"
        assert last_name, "Missing User last_name"
        assert email, "Missing User email"
        assert password, "Missing User password"

        db = DBConnection()

        #Generate Account ID
        acct_hash_obj = hashlib.sha256(email.encode())
        acct_hash = acct_hash_obj.hexdigest()

        #Generate Password Hash
        pass_hash = argon2.hash(password)

        #Save User to DB
        db.query(
            "INSERT INTO user_account(user_id,first_name,last_name,email,password_hash) \
            VALUES (%s,%s,%s,%s,%s)",
            [acct_hash,first_name,last_name,email,pass_hash]
        )
        db.save()
        db.close()
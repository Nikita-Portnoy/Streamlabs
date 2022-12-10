import braintree
from flask import current_app as app

from app.model.user.user import User

class Checkout(User):

    def __init__(self, user_id):

        super().__init__(public_id=user_id)
        
        self.braintree_gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                braintree.Environment.Sandbox,
                merchant_id=app.config['BT_MERCHANT_ID'],
                public_key=app.config['BT_PUBLIC_KEY'],
                private_key=app.config['BT_PRIVATE_KEY']
            )
        )

    def generate_client_token(self):
        return self.braintree_gateway.client_token.generate(customer_id=self.internal_id)

    def get_subscriptions(self):
        user_subscriptions = self.db.query(
            "SELECT subscription_id,created_at,price,subscription_status,updated_at \
            FROM user_subscription \
            WHERE user_id = %s",
            [self.internal_id]
        )

        return user_subscriptions

    def new_subscription(self, sub_type, payment_nonce):

        assert self.is_premium, "Subscription exists"

        plan_id = ""
        for plan in Checkout.get_subscription_plans():
            if plan.nane == sub_type:
                plan_id = plan.id

        assert plan_id, "Plan not found"

        subscription = self.braintree_gateway.subscription.create({
            'plan_id': plan_id,
            'payment_method_nonce': payment_nonce
        })

        # TODO Check if successful

        self.db.query(
            "INSERT INTO user_subscription(subscription_id,user_id,created_at,price,subscription_status,updated_at) \
            VALUES (%s,%s,%s,%s,%s,%s)",
            [subscription.id,self.internal_id,subscription.created_at,subscription.price,subscription.status,subscription.updated_at]
        )
        self.db.save()
        self.db.close()

    def cancel_subscription(self, subscription_id):
        # TODO Check subscription exists in db

        self.braintree_gateway.subscription.cancel(subscription_id)

        self.db.query(
            "DELETE FROM user_subscription \
            WHERE subscription_id = %s",
            [subscription_id]
        )
        self.db.save()
        self.db.close()


    @staticmethod
    def get_subscription_plans():
        braintree_gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                braintree.Environment.Sandbox,
                merchant_id=app.config['BT_MERCHANT_ID'],
                public_key=app.config['BT_PUBLIC_KEY'],
                private_key=app.config['BT_PRIVATE_KEY']
            )
        )

        return braintree_gateway.plan.all()
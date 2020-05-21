import hashlib
import hmac
import sys

from razorpay.errors import SignatureVerificationError
from razorpay.utility import Utility


def verify_payment_signature(self, parameters):
    order_id = str(parameters['razorpay_order_id'])
    payment_id = str(parameters['razorpay_payment_id'])
    razorpay_signature = str(parameters['razorpay_signature'])
    msg = "{}|{}".format(order_id, payment_id)

    secret = str(self.client.auth[1])

    return self.verify_signature(msg, razorpay_signature, secret)


def verify_webhook_signature(self, body, signature, secret):
    self.verify_signature(body, signature, secret)
    return self.verify_signature(body, signature, secret)


def verify_signature(self, body, signature, key):
    if sys.version_info[0] == 3:  # pragma: no cover
        key = bytes(key, 'utf-8')
        body = bytes(body, 'utf-8')
    dig = hmac.new(key=key,
                   msg=body,
                   digestmod=hashlib.sha256)
    generated_signature = dig.hexdigest()
    if sys.version_info[0:3] < (2, 7, 7):
        result = self.compare_string(generated_signature, signature)
    else:
        result = hmac.compare_digest(generated_signature, signature)
    if not result:
        raise SignatureVerificationError(
            'Razorpay Signature Verification Failed')
    return result


Utility.verify_payment_signature = verify_payment_signature
Utility.verify_webhook_signature = verify_webhook_signature
Utility.verify_signature = verify_signature


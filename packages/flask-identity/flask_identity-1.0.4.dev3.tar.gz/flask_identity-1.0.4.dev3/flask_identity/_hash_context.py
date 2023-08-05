# -*- coding: utf-8 -*-

"""
    identity._hash_context
    ~~~~~~~~~~~~~~~~~~~
    Hash Context of Flask-Identity

    :author: solardiax <solardiax@hotmail.com>
    :copyright: (c) 2020 by DreamEx Works.
    :license: MIT, see LICENSE for more details.
"""


from passlib.context import CryptContext


class HashContext(object):
    """
    | Class to generate/verify hash securitied string.
    | Hashed string can be used to store context or any unencrypt context.
    """

    def __init__(self, app) -> None:
        secret_key = app.config.get("IDENTITY_HASH_SALT", None)

        if secret_key is None:
            secret_key = app.config.get("SECRET_KEY", None)

        if secret_key is None:
            raise SystemError("Config setting SECRET_KEY or IDENTITY_HASH_SALT is missing.")

        schemes = app.config.get("IDENTITY_HASH_SCHEMES", ["bcrypt"])
        schemes_keywords = app.config.get("IDENTITY_HASH_OPTIONS", {})

        # Create a passlib CryptContext
        self.crypt_context = CryptContext(schemes, **schemes_keywords)

    def hash_context(self, context: str) -> str:
        """
        Hash plaintext ``context`` using the ``IDENTITY_HASH_SCHEMES`` specified in the app config.
        :param context: Plaintext string that the user types in.
        :return: hashed context.

        Example:
            ``user.context = hash_context("mycontext")``
        """

        # Use passlib's CryptContext to hash a context
        context_hash = self.crypt_context.encrypt(context)

        return context_hash

    def verify_context(self, context: str, context_hash: str) -> bool:
        """
        Verify plaintext ``context`` against ``hashed context``.
        :param context: Plaintext context that the user types in.
        :param context_hash: context hash generated by a previous call to ``hash_context()``.
        :return:
            | True when ``context`` matches ``context_hash``.
            | False otherwise.

        Example:
            ::
                if verify_context("mycontext", user.context):
                    login_user(user)
        """
        # Use passlib's CryptContext to verify a context
        return self.crypt_context.verify(context, context_hash)

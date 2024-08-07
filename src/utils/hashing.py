from passlib.context import CryptContext

# get the crypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    @classmethod
    def bcrypt_hash(cls, password: str) -> str:
        """
        Hash the password using bcrypt algorithm
        :param password: the password to hash
        :return: the hashed password
        """
        return pwd_context.hash(password)

    @classmethod
    def verify(cls, plain_password: str, hashed_password: str) -> bool:
        """
        Verify the plain password against the hashed password
        :param plain_password: the plain password to verify
        :param hashed_password: the hashed password to verify against
        :return: True if the plain password matches the hashed password, False otherwise
        """
        return pwd_context.verify(secret=plain_password, hash=hashed_password)

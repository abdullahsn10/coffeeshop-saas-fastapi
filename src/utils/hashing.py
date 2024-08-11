from passlib.context import CryptContext

# get the crypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    @classmethod
    def bcrypt_hash(cls, password: str) -> str:
        """
        Hash the password using bcrypt algorithm
        *Args:
            password: <PASSWORD> to be hashed
        *Returns:
            The hashed password using BCrypt algorithm
        """
        return pwd_context.hash(password)

    @classmethod
    def verify(cls, plain_password: str, hashed_password: str) -> bool:
        """
        Verify the plain password against the hashed password\n
        *Args:
            plain_password: plain text password to be verified\n
            hashed_password: hashed password to compare against and verify\n
        *Returns:
            True if the hashed password matches the plain password, False otherwise
        """
        return pwd_context.verify(secret=plain_password, hash=hashed_password)

class CoinNotFound(Exception):
    """ Raise when a coin is not found """
    def __init__(self, coin: str):
        super().__init__(f"'{coin}' coin is not found")

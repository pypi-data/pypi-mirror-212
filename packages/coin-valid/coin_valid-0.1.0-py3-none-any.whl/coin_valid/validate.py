import re

from coin_valid.coins import network_coin_regex
from coin_valid.exceptions.address_exceptions import InvalidAddress
class Validate:

    @staticmethod
    def validate(address: str, coin: str, network: str = 'mainnet') -> bool:
        """
        Check if address is valid for that coin and network

        :param str address: address
        :param str coin: acronym or full name
        :param str network: mainnet, stagenet, testnet
        :return bool: true if valid and raise InvalidAddress error if invalid
        """
        regex = network_coin_regex(coin, network)
        if not re.match(regex, address):
            raise InvalidAddress(address, coin, network)
        return True



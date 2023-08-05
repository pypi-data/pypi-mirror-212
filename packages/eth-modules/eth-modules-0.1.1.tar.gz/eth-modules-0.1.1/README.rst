

To checksum address
===============
This project helps you generate correct checksum address for EVM blockchains

Installing
============

.. code-block:: bash

    pip install web3-checksum

Usage
=====

.. code-block:: bash

    >>> from web3_checksum.get_checksum_address import get_checksum_address
    >>> get_checksum_address(private_key='YOUr PRIVATE KEY')
    >>> get_checksum_address(address='YOUR ADDRESS')
    >>> get_checksum_address(account='YOUR ACCOUNT')


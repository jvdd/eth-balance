# eth-balance
Fetches the real-time balance of 1 or multiple eth addresses

## Run the code

1. Add your [etherscan.io](https://etherscan.io/) api key in the `keys.txt` file.
2. Add your addresses as separate lines in the `addresses.txt` file.
3. Run the code
   ```
   $ python eth-balance.get_balance.py
   ```

Example output:

```txt
Address: 0xb8C9b9d2b033AcBf130873e93F2f208eA2782b37
ETH Balance: 0.134175 - $558.70

Address: 0xaE781204D4050ae3544dB2AAc8926da262537dC1
ETH Balance: 0.864965 - $3601.67
Tokens:
      BUNNY: 7125222359.175408 - $0.01
      GRUMPY: 1025.708824 - $0.00
      SHIB : 48668408.040837 - $3544.03
      eRise: 19462997.155228 - $0.00
      POODL: 37.709654 - $0.00

Address: 0xBDF05E45143d65139978C46aD5C3e2a7c3Dd1AEA
ETH Balance: 0.421284 - $1754.21

Address: 0x8BB7867Ba0173A9bCc761b617Be60621C69356f2
ETH Balance: 0.789285 - $3286.54

Combined
ETH Balance: 2.209709 - $9201.12
Tokens:
      BUNNY: 7125222359.175408 - $0.01
      GRUMPY: 1025.708824 - $0.00
      SHIB : 48668408.040837 - $3544.03
      eRise: 19462997.155228 - $0.00
      POODL: 37.709654 - $0.00

TOTAL: $12745.17
```
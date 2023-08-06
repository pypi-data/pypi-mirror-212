# vap - [Verify Apple Postback](https://developer.apple.com/documentation/storekit/skadnetwork/verifying_an_install-validation_postback#3599761)

#### How to install:
```bash
$ pip install vap
```

#### How to use:
```bash
$ vap verify '{"version": "4.0", "ad-network-id": "com.example", "source-identifier": "39", "app-id": 525463029, "transaction-id": "6aafb7a5-0170-41b5-bbe4-fe71dedf1e31", "redownload": false, "source-domain": "example.com", "fidelity-type": 1, "did-win": true, "coarse-conversion-value": "high", "postback-sequence-index": 0, "attribution-signature": "MEUCIQD4rX6eh38qEhuUKHdap345UbmlzA7KEZ1bhWZuYM8MJwIgMnyiiZe6heabDkGwOaKBYrUXQhKtF3P/ERHqkR/XpuA="}'
# 1
```

```python
from vap.verifier import verify_postback

# supported versions below:
items = [
    {
        'version': '2.1',
        'ad-network-id': 'com.example',
        'campaign-id': 42,
        'transaction-id': '6aafb7a5-0170-41b5-bbe4-fe71dedf1e28',
        'app-id': 525463029,
        'attribution-signature': 'MEUCID6rbq3qt4GvFaAaynh5/LAcvn1d8CQTRhrZhLIxLKntAiEAo7IrvoMw6u2qDg6Tr5vIsEHXj'
                                 'lLkPlCOL0ojJcEh3Qw=',
        'redownload': True,
        'source-app-id': 1234567891,
        'conversion-value': 20,
    },
    {
        'version': '3.0',
        'ad-network-id': 'example123.skadnetwork',
        'campaign-id': 42,
        'transaction-id': '6aafb7a5-0170-41b5-bbe4-fe71dedf1e28',
        'app-id': 525463029,
        'attribution-signature': 'MEYCIQD5eq3AUlamORiGovqFiHWI4RZT/PrM3VEiXUrsC+M51wIhAPMANZA9c07raZJ64gVaXhB9'
                                 '+9yZj/X6DcNxONdccQij',
        'redownload': True,
        'source-app-id': 1234567891,
        'fidelity-type': 1,
        'conversion-value': 20,
        'did-win': True,
    },
    {
        'version': '3.0',
        'ad-network-id': 'example123.skadnetwork',
        'campaign-id': 42,
        'transaction-id': 'f9ac267a-a889-44ce-b5f7-0166d11461f0',
        'app-id': 525463029,
        'attribution-signature': 'MEUCIQDDetUtkyc/MiQvVJ5I6HIO1E7l598572Wljot2Onzd4wIgVJLzVcyAV+TXksGNoa0DTMXEP'
                                 'gNPeHCmD4fw1ABXX0g=',
        'redownload': True,
        'fidelity-type': 1,
        'did-win': False,
    },
    {
        'version': '4.0',
        'ad-network-id': 'com.example',
        'source-identifier': '39',
        'app-id': 525463029,
        'transaction-id': '6aafb7a5-0170-41b5-bbe4-fe71dedf1e31',
        'redownload': False,
        'source-domain': 'example.com',
        'fidelity-type': 1,
        'did-win': True,
        'coarse-conversion-value': 'high',
        'postback-sequence-index': 0,
        'attribution-signature': 'MEUCIQD4rX6eh38qEhuUKHdap345UbmlzA7KEZ1bhWZuYM8MJwIgMnyiiZe6heabDkGwOaKBYrUXQ'
                                 'hKtF3P/ERHqkR/XpuA=',
    },
    {
        'version': '4.0',
        'ad-network-id': 'com.example',
        'source-identifier': '5239',
        'app-id': 525463029,
        'transaction-id': '6aafb7a5-0170-41b5-bbe4-fe71dedf1e30',
        'redownload': False,
        'source-domain': 'example.com',
        'fidelity-type': 1,
        'did-win': True,
        'conversion-value': 63,
        'postback-sequence-index': 0,
        'attribution-signature': 'MEUCIGRmSMrqedNu6uaHyhVcifs118R5z/AB6cvRaKrRRHWRAiEAv96ne3dKQ5kJpbsfk4eYiePmr'
                                 'ZUU6sQmo+7zfP/1Bxo=',
    },
]

for postback in items:
    print(verify_postback(postback))

# True
# True
# True
# True
# True
```
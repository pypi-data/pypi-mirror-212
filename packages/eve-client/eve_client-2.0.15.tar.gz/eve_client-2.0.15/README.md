The EVE API Client is a python class that allows interaction with the [Exodus Vulnerability Enrichment (EVE):](<https://eve.exodusintel.com>) platform.

Welcome to the EVE API Client's documentation. Please get started by reading about how to use it and add it to your projects.

What's new
==========

Patch
==========
- Fixes bug with HTTP proxy target.


Pre-requisites
==============
- An Exodus Intelligence account is required if you want to take advantage of the ful EVE platform.
- [Python](https://www.python.org/downloads/) 3.8 or newer is required.
- The EVE platform provides an endpoint to deliver essential information about Common Vulnerabilities and Exposures CVE anonymously.

Getting started
===============
**Install EVE Client using pip:**

``` bash
   $ pip install eve-client
```

**Using EVE Client Anonymously:**

```python

   import json
   from eve_client import eve
   exodus_api = eve.EVEClientAnonymous()
   cve = exodus_api.get_cve("CVE-2021-44228")
   print(json.dumps(cve, indent=3))
```

**Output:**

```json

   {
      "data": {
         "attack_vector": "network",
         "product": "Apache Log4j2,Log4j2",
         ...
         "vendor": "Apache Software Foundation,Apache"
      },
      "ok": true
   }
```

**Using EVE Client with Authentication:**

```python
   import json
   from eve_client import eve
   exodus_api = eve.EVEClient('abc@def.com', 'MyPassword', 'MYPRIVATEKEY')
   cve = exodus_api.get_vuln("CVE-2021-44228")
   print(json.dumps(cve, indent=3))
```

**Output:**
```json

   {
      "data": {
         "attack_vector": "network",
         "product": "Apache Log4j2,Log4j2",
         ...
         "vendor": "Apache Software Foundation,Apache"
      },
      "ok": true
   }
```

*You receive the anonymous fields, plus the fields in your account tier.*


Classes and Methods Available
=============================

### _class_ eve.EVEClient(email, password, key, url, api_version, proxy_protocol, proxy_address, proxy_port)
Bases: `object`

Class EVEClient allows communication with the Exodus API.

Module to connect and interact with the Exodus Intelligence API.


* **Parameters**
    * **email** (*str*) -- Email address registered with Exodus Intelligence.
    * **password** (*str*) -- User password
    * **key** (*str**, **optional*) -- Exodus Intelligence API key, defaults to None
    * **url** (*_type_**, **optional*) -- Exodus Intelligence API domain, defaults to "[https://eve.exodusintel.com](https://eve.exodusintel.com)"
    * **api_version** (*str**, **optional*) -- Version number ie: v1 or v2, defaults to "v1"
    * **proxy_protocol** (*str**, **optional*) -- Proxy protocol type, defaults to "http"
    * **proxy_url** (*str**, **optional*) -- Proxy Url, defaults to None
    * **proxy_port** (*int**, **optional*) -- Proxy Port, defaults to 3128


#### decrypt_bronco_in_report(report, bronco_public_key)
Decrypt the content of a report using a private and public key.
* **Parameters**
    * **report** (*object*) -- The encrypted message.
    * **bronco_public_key** (*str*) -- The public key
* **Raises**
    **KeyError** -- When Bronco Key is wrong.
* **Returns**
    A dictionary object representing the report.
* **Return type**
    dict



#### generate_key_pair()
Generate a public key pair .
* **Raises**
    * **exceptions.InvalidStateError** -- Could not set the public key.
    * **exceptions.InvalidStateError** -- Could not confirm the public key.
* **Returns**
    A key pair (sk, pk)
* **Return type**
    tuple

#### get_access_token()
Obtain access token.
* **Raises**
    **requests.exceptions.ConnectionError** -- API is Unavailable.
* **Returns**
    A token
* **Return type**
    str

#### get_bronco_public_key()
Get server public key.
* **Returns**
    A string representation of a public key.
* **Return type**
    str



#### get_recent_reports(reset: Optional[Union[int, datetime]] = None)
Get recent reports.
* **Parameters**
    **reset** (*int**, **datetime**, **optional*) -- A number of days in the past to reset, defaults to 0
* **Returns**
    Recent reports.
* **Return type**
    dict


#### get_recent_vulns(reset: int = 0)
Get all vulnerabilities within 60 days of the user's stream marker;             limit of 500 vulnerabilities can be returned.
* **Parameters**
    **reset** (*int**, **optional*) -- Reset the stream maker to a number of days in the
    past, defaults to 0
* **Returns**
    Returns recent vulnerabilities.
* **Return type**
    dict

#### get_report(identifier: str)
Get a report by identifier .
* **Parameters**
    **identifier** (*str*) -- String representation of report id.
* **Returns**
    Returns report
* **Return type**
    dict

#### get_vuln(identifier: str)
Get a Vulnerability by identifier or cve.

* **Parameters**
    **identifier** (*str*) -- String representation of vulnerability id.
* **Returns**
    A Vulnerability
* **Return type**

    dict

#### get_vulns_by_day()
Get vulnerabilities by day .
* **Returns**
    The number of vulnerabilities by day.
* **Return type**
    dict

#### handle_reset_option(reset: Optional[Union[int, datetime]] = None)
Reset number of days.
* **Parameters**
    **reset** (*int*) -- Number of days in the past to reset
* **Returns**
    A date in ISO8601
* **Return type**
    datetime

#### search(search_term: str)
Search specific term
* **Parameters**
    **search_term** (*str*) -- Term to search for.
* **Returns**
    Vulnerabilities containing search term
* **Return type**
    dict

### _class_ eve.EVEClientAnonymous()
Bases: `object`
This class allows to retrieve cve information anonymously from
Exodus Intelligence API.
* **Returns:**
    JSON Object: CVE information available to the anonymous user.

#### get_cve(identifier: str)
Retrieve a Common Vulnerabilities and Exposures identifier.
* **Parameters**
    **identifier** (*str*) -- CVE identifier
* **Returns**
    A dictionary containing fields for the anonymous tier.
* **Return type**
    dict

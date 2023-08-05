# Sonatype: Nexus IQ Server - Python SDK

## Installation

If the python package is hosted on Github, you can install directly from Github

```sh
pip install nexus_iq_sdk
```

Then import the package:

```python
import nexus_iq_sdk
```

Then import the package:

```python
import nexus_iq_sdk
```

## Getting Started

```python
from __future__ import print_function
import time
import nexus_iq_sdk
from nexus_iq_sdk.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = nexus_iq_sdk.ApplicationCategoriesApi(nexus_iq_sdk.ApiClient(configuration))
organization_id = 'organization_id_example' # str |
body = nexus_iq_sdk.ApiApplicationCategoryDTO() # ApiApplicationCategoryDTO |  (optional)

try:
    api_response = api_instance.add_tag(organization_id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ApplicationCategoriesApi->add_tag: %s\n" % e)

# create an instance of the API class
api_instance = nexus_iq_sdk.ApplicationCategoriesApi(nexus_iq_sdk.ApiClient(configuration))
organization_id = 'organization_id_example' # str |
tag_id = 'tag_id_example' # str |

try:
    api_instance.delete_tag(organization_id, tag_id)
except ApiException as e:
    print("Exception when calling ApplicationCategoriesApi->delete_tag: %s\n" % e)

# create an instance of the API class
api_instance = nexus_iq_sdk.ApplicationCategoriesApi(nexus_iq_sdk.ApiClient(configuration))
organization_id = 'organization_id_example' # str |

try:
    api_response = api_instance.get_applicable_tags(organization_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ApplicationCategoriesApi->get_applicable_tags: %s\n" % e)

# create an instance of the API class
api_instance = nexus_iq_sdk.ApplicationCategoriesApi(nexus_iq_sdk.ApiClient(configuration))
application_public_id = 'application_public_id_example' # str |

try:
    api_response = api_instance.get_applicable_tags_by_application_public_id(application_public_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ApplicationCategoriesApi->get_applicable_tags_by_application_public_id: %s\n" % e)

# create an instance of the API class
api_instance = nexus_iq_sdk.ApplicationCategoriesApi(nexus_iq_sdk.ApiClient(configuration))
application_public_id = 'application_public_id_example' # str |

try:
    api_response = api_instance.get_application_applicable_tags(application_public_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ApplicationCategoriesApi->get_application_applicable_tags: %s\n" % e)

# create an instance of the API class
api_instance = nexus_iq_sdk.ApplicationCategoriesApi(nexus_iq_sdk.ApiClient(configuration))
organization_id = 'organization_id_example' # str |

try:
    api_response = api_instance.get_applied_policy_tags(organization_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ApplicationCategoriesApi->get_applied_policy_tags: %s\n" % e)

# create an instance of the API class
api_instance = nexus_iq_sdk.ApplicationCategoriesApi(nexus_iq_sdk.ApiClient(configuration))
organization_id = 'organization_id_example' # str |

try:
    api_response = api_instance.get_applied_tags(organization_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ApplicationCategoriesApi->get_applied_tags: %s\n" % e)

# create an instance of the API class
api_instance = nexus_iq_sdk.ApplicationCategoriesApi(nexus_iq_sdk.ApiClient(configuration))
organization_id = 'organization_id_example' # str |

try:
    api_response = api_instance.get_tags(organization_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ApplicationCategoriesApi->get_tags: %s\n" % e)

# create an instance of the API class
api_instance = nexus_iq_sdk.ApplicationCategoriesApi(nexus_iq_sdk.ApiClient(configuration))

try:
    api_response = api_instance.get_tags_used_by_applications()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ApplicationCategoriesApi->get_tags_used_by_applications: %s\n" % e)

# create an instance of the API class
api_instance = nexus_iq_sdk.ApplicationCategoriesApi(nexus_iq_sdk.ApiClient(configuration))
organization_id = 'organization_id_example' # str |
body = nexus_iq_sdk.ApiApplicationCategoryDTO() # ApiApplicationCategoryDTO |  (optional)

try:
    api_response = api_instance.update_tag(organization_id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ApplicationCategoriesApi->update_tag: %s\n" % e)
```

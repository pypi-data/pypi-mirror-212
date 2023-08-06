ORGANIZATION = """
organization:
  key: organization_key
  tags:
  - foo
  - bar
  name: organization_foo
  description: organization description
  controller:
    name: Bob
    address: Museumplein 10, 1071 DJ Amsterdam, Netherlands
    email: bob@organization.com
    phone: 020 573 2911
  data_protection_officer:
    name: Alice
    address: Museumplein 10, 1071 DJ Amsterdam, Netherlands
    email: alice@organization.com
    phone: 020 573 2911
  representative:
    name: Carol [optional]
    address: Museumplein 10, 1071 DJ Amsterdam, Netherlands
    email: carol@organization.com
    phone: 020 573 2911
"""

SYSTEM = """
system:
  key: system_key
  tags:
  - foo
  - bar
  name: system_foo
  description: <system description> [optional]

"""


RESOURCE = """
resource:
  key: foo_key
  tags:
  - foo
  - bar
  name: <resource name>
  description: <resource description>
  resource_type: Service
  data_responsibility_title: Processor
  privacy_declarations:
  - name: Privacy Policy
    data_categories:
    - user.device.cookie_id
    - user.contact
    data_use: improve.system
    data_subjects:
    - Customer
    data_qualifier: Aggregated
  dependencies:
  - system_key
  joint_controller:
    name: Dave
    address: Museumplein 10, 1071 DJ Amsterdam, Netherlands
    email: dave@organization.com
    phone: 020 573 2911
  third_country_transfers:
  - USA
  - CAN
  administrating_department: engineering
  data_protection_impact_assessment:
    is_required: true
    status: Complete
    link: https://example.org/analytics_system_data_protection_impact_assessment
"""

DATASET = """
dataset:
  key: foo_key
  tags:
  - foo
  - bar
  name: user
  description: <resource description>
  meta:
    last_updated: '2021-01-01'
    version: 1.0.0
  data_categories:
  - user.contact
  data_qualifier: identified
  joint_controller:
    name: Dave
    address: Museumplein 10, 1071 DJ Amsterdam, Netherlands
    email: dave@organization.com
    phone: 020 573 2911
  third_country_transfers:
  - USA
  - CAN
  collections:
  - name: user
    description: user data
    data_categories:
    - user.contact
    data_qualifier: identified
    fields:
    - name: email
      description: user email
      data_categories:
      - user.contact.email
      data_qualifier: identified
      deidentifier:
        type: replace
        value: fake@email.com
      period: P365D
    - name: name
      description: user name
      data_categories:
      - user.name
      data_qualifier: identified
      deidentifier:
        type: redact
      period: P365D
    datetime_field:
      name: created_at
"""

SQLITE = """
profiles:
  dev:
    type: sqlite
    config:
      connection:
        database: "dev.db"
        uri: true
  prd:
    type: sqlite
    config:
      connection:
        database: "prd.db"
        uri: true
"""

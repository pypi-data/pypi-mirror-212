def project_yaml() -> str:
    return """
    name: test_project
    config-version: 1
    version: 0.0.1

    default-profile: dev

    catalogue-path: ./catalogue
    adapters-path: ./adapters
    """


def sqlite_adapter_yaml():
    return """
    env_prefix: TEST_
    profiles:
      dev:
        type: sqlite
        config:
          connection:
            database: "file::memory:?cache=shared"
            uri: true"""


def organization_yaml() -> str:
    return """
    organization:
      - key: organization_foo
        name: Acme Incorporated
        description: An Organization that represents all of Acme Inc.
        security_policy: https://example.org/privacy
        controller:
          name: Dave L. Epper
          address: 1 Acme Pl. New York, NY
          email: controller@acmeinc.com
          phone: +1 555 555 5555
        data_protection_officer:
          name: Preet Ector
          address: 1 Acme Pl. New York, NY
          email: dpo@acmeinc.com
          phone: +1 555 555 5555
        representative:
          name: Ann Othername
          address: 1 Acme Pl. New York, NY
          email: representative@acmeinc.com
          phone: +1 555 555 5555
    """


def system_yaml() -> str:
    return """
    system:
      - key: system_foo
        name: User Systems System
        description: A System for all of the user-related resources.
    """


def resource_yaml() -> str:
    return """
    resource:
      - key: demo_analytics_resource
        name: Demo Analytics Resource
        description: A resource used for analyzing customer behaviour.
        resource_type: Service
        data_responsibility_title: Controller
        administrating_department: Engineering
        third_country_transfers:
        - USA
        - CAN
        joint_controller:
          name: Dave L. Epper
          address: 1 Acme Pl. New York, NY
          email: controller@acmeinc.com
          phone: +1 555 555 5555
        data_protection_impact_assessment:
          is_required: True
          progress: Complete
          link: https://example.org/analytics_system_data_protection_impact_assessment
        privacy_declarations:
          - name: Analyze customer behaviour for improvements.
            data_categories:
              - user.contact
              - user.device.cookie_id
            data_use: improve.system
            data_subjects:
              - customer
            data_qualifier: identified_data
            egress:
              - another_demo_system
            ingress:
              - yet_another_demo_system
      """


def dataset_yaml(table: str) -> str:
    return f"""
    dataset:
      - key: demo_users_dataset
        name: Demo Users Dataset
        description: Data collected about users for our analytics system.
        third_country_transfers:
        - USA
        - CAN
        joint_controller:
          name: Dave L. Epper
          address: 1 Acme Pl. New York, NY
          email: controller@acmeinc.com
          phone: +1 555 555 5555
          retention: 1 year post account deletion
        collections:
          - name: {table}
            description: User information
            data_categories:
              - user
            retention: 30 days post account deletion
            datetime_field:
                name: created_at
            fields:
              - name: name
                description: User's first name
                data_categories:
                  - user.name
                deidentifier:
                  type: redact
                period: P365D # [±]P[DD]DT[HH]H[MM]M[SS]S
              - name: email
                description: User's Email
                data_categories:
                  - user.contact.email
                deidentifier:
                  type: replace
                  value: fake@email.com
                period: P365D # [±]P[DD]DT[HH]H[MM]M[SS]S
              - name: ip
                description: User's IP address
                data_categories:
                  - user.device.ip_address
                deidentifier:
                  type: mask
                  value: "#"
                period: "280 00" # [-][DD ][HH:MM]SS[.ffffff]
    """

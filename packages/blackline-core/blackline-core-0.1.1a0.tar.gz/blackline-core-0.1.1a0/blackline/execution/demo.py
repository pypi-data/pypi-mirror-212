from datetime import datetime
from pathlib import Path
from sqlite3 import Connection, connect

from blackline.constants import DEFAULT_PROFILE, SAMPLE_DATABASE, SAMPLE_PROJECT_NAME
from blackline.project.init import InitProject


def load_users() -> list[list[object]]:
    """Returns a list of lists containing information about users.

    Returns:
        List[List[object]]: A list of lists. Each inner list contains the following fields: # noqa: E501
        1. str: User ID
        2. str: User name
        3. str: User email
        4. str: User IP address
        5. bool: True if user is active, False otherwise
        6. datetime.datetime: Date and time when user account was created
    """
    users = [
        ["00", "Bar", "bar@example.com", "555.444.3.2", True, datetime(2021, 2, 1)],
        ["01", "Biz", "biz@example.com", "555.444.3.3", True, datetime(2022, 6, 1)],
        ["02", "Baz", "baz@example.com", "555.444.3.4", False, datetime(2022, 2, 1)],
        ["03", "Cat", "cat@example.com", "555.444.3.5", True, datetime(2023, 1, 1)],
        ["04", "Dog", "dog@example.com", "555.444.3.6", False, datetime(2023, 1, 1)],
    ]
    return users


def load_shipments() -> list[list[object]]:
    """Returns a list of lists containing information about shipments.

    Returns:
        List[List[object]]: A list of lists. Each inner list contains the following fields: # noqa: E501
        1. str: Shipment ID
        2. str: User ID of the user who placed the order
        3. datetime.datetime: Date and time when the order was placed
        4. str: Street address where the shipment is to be delivered
        5. str: Postal code of the destination
        6. str: City of the destination
        7. str: Status of the shipment, either "delivered" or "returned"
    """
    shipments = [
        [
            "00",
            "01",
            datetime(2022, 6, 1),
            "Ceintuurbaan 282",
            "1072 GK",
            "Amsterdam",
            "delivered",
        ],
        [
            "01",
            "02",
            datetime(2022, 3, 1),
            "Singel 542",
            "1017 AZ",
            "Amsterdam",
            "delivered",
        ],
        [
            "02",
            "02",
            datetime(2022, 4, 15),
            "Singel 542",
            "1017 AZ",
            "Amsterdam",
            "delivered",
        ],
        [
            "03",
            "03",
            datetime(2023, 1, 5),
            "Wibautstraat 150",
            "1091 GR",
            "Amsterdam",
            "delivered",
        ],
        [
            "04",
            "03",
            datetime(2023, 1, 6),
            "Wibautstraat 150",
            "1091 GR",
            "Amsterdam",
            "returned",
        ],
        [
            "05",
            "03",
            datetime(2023, 1, 6),
            "Wibautstraat 150",
            "1091 GR",
            "Amsterdam",
            "delivered",
        ],
    ]
    return shipments


INIT_ORGANIZATION = """# See details docs at https://docs.getblackline.com/
organization:
  - key: organization_demo
"""

INIT_SYSTEM = """# See details docs at https://docs.getblackline.com/
system:
  - key: system_demo
"""

INIT_RESOURCE = """# See details docs at https://docs.getblackline.com/
resource:
  - key: resource_demo
    resource_type: Service
    privacy_declarations:
      - name: Analyze customer behaviour for improvements.
        data_categories:
          - user.contact
          - user.device.cookie_id
        data_use: improve.system
        data_subjects:
          - customer
        data_qualifier: identified_data
"""


def demo_adapter(project_root: Path, profile: str = DEFAULT_PROFILE) -> str:
    """
    Generates a demo adapter for the specified project root.

    Args:
        project_root: The root path of the project.

    Returns:
        The demo adapter in yaml format.
    """
    return f"""# See details docs at https://docs.getblackline.com/
profiles:
  {profile}:
    type: sqlite
    config:
      connection:
        database: {SAMPLE_DATABASE}
        uri: true
    """


def demo_dataset() -> str:
    """
    Generates a demo dataset.

    Returns:
        The demo dataset in yaml format.
    """
    return """
    dataset:
      - key: demo_db
        name: Demo Database
        description: Demo database for Blackline
        collections:
          - name: user
            description: User collection
            datetime_field:
              name: created_at
            fields:
              - name: name
                description: Name of user
                deidentifier:
                  type: redact
                period: P365D
              - name: email
                deidentifier:
                  type: replace
                  value: fake@email.com
                period: P365D
              - name: ip
                deidentifier:
                  type: mask
                  value: '#'
                period: 280 00
          - name: shipment
            datetime_field:
                name: order_date
            fields:
              - name: street
                deidentifier:
                  type: redact
                period: P185D
    """


class Demo:
    def __init__(
        self,
        path: Path,
        name: str = SAMPLE_PROJECT_NAME,
        overwrite: bool = False,
        default_profile: str = DEFAULT_PROFILE,
    ):
        """
        Initializes the Demo class instance with the given parameters.

        Args:
            path: Path to the directory where the project will be created.
            name: Name of the project.
            overwrite: If set to True, overwrites the existing project.
        """
        self.path = path
        self.name = name
        self.overwrite = overwrite
        self.init_project = InitProject(
            path=path,
            name=name,
            overwrite=overwrite,
            default_profile=default_profile,
            init_organization=INIT_ORGANIZATION,
            init_system=INIT_SYSTEM,
            init_resource=INIT_RESOURCE,
            init_dataset=demo_dataset(),
            init_adapter=demo_adapter(project_root=self.path, profile=default_profile),
        )
        self.project_config = self.init_project.project_config

    def create(self):
        """
        Creates a project and a database for the demo instance.
        """
        self.init_project.init_project()
        self.create_database()

    def create_database(self):
        """
        Creates user and shipment tables in the database.
        """
        conn = self.connection()
        Demo.create_user_table(conn=conn, users=load_users())
        Demo.create_shipment_table(conn=conn, shipments=load_shipments())

    def connection(self) -> Connection:
        """
        Establishes a connection with the database.

        Returns:
            Connection: A connection object.
        """
        return connect(str(Path(self.path, SAMPLE_DATABASE)))

    @staticmethod
    def create_user_table(conn: Connection, users: list[list[object]]) -> None:
        """
        Creates a user table in the database and inserts data.

        Args:
            conn (Connection): A connection object.
            users (list[list[object]]): A list of user data.

        Returns:
            None
        """
        with conn:
            cur = conn.execute(
                "CREATE TABLE IF NOT EXISTS user(id, name, email, ip, verified, created_at)"  # noqa E501
            )
            cur.executemany("INSERT INTO user VALUES(?, ?, ?, ?, ?, ?)", users)

    @staticmethod
    def create_shipment_table(conn: Connection, shipments: list[list[object]]) -> None:
        """
        Creates a shipment table in the database and inserts data.

        Args:
            conn (Connection): A connection object.
            shipments (list[list[object]]): A list of shipment data.

        Returns:
            None
        """
        with conn:
            cur = conn.execute(
                "CREATE TABLE IF NOT EXISTS shipment(id, user_id, order_date, street, postcode, city,status)"  # noqa E501
            )
            cur.executemany(
                "INSERT INTO shipment VALUES(?, ?, ?, ?, ?, ?, ?)", shipments
            )


def create_demo(
    path: Path,
    name: str = SAMPLE_PROJECT_NAME,
    overwrite: bool = False,
    default_profile: str = DEFAULT_PROFILE,
) -> Demo:
    """
    Creates an instance of Demo and runs the create() method.

    Args:
        path: Path to the directory where the project will be created.
        name: Name of the project.
        overwrite: If set to True, overwrites the existing project.

    Returns:
        Demo: A Demo class instance.
    """
    demo = Demo(
        path=path, name=name, overwrite=overwrite, default_profile=default_profile
    )
    demo.create()
    return demo

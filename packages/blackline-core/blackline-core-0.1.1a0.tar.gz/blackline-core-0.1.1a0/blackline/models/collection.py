from typing import Optional

from pydantic import BaseModel, Field


class Column(BaseModel):
    """
    Column object for a table.
    """

    name: str = Field(..., discription="The name of the column.")
    data_type: Optional[str] = Field(discription="The data type of the column.")
    nullable: bool = Field(True, discription="Whether the column is nullable.")
    unique: bool = Field(False, discription="Whether the column is unique.")
    primary_key: bool = Field(
        False, discription="Whether the column is the primary key."
    )
    foreign_key: bool = Field(False, discription="Whether the column is a foreign key.")
    check: Optional[str] = Field(discription="The check expression for the column.")
    default: Optional[str] = Field(discription="The default value for the column.")

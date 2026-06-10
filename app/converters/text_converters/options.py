"""Common option schemas for the text converter group."""
from typing import Literal
from pydantic import BaseModel, Field


class PdfOptions(BaseModel):
    page_size: Literal["a4", "letter"] = Field(
        default="a4",
        title="Page Size",
        description="Paper size for the rendered PDF document.",
    )

"""Common option schemas for the text converter group."""
from typing import Literal
from pydantic import BaseModel, Field


class PdfOptions(BaseModel):
    page_size: Literal["a4", "letter"] = Field(
        default="a4",
        title="Page Size",
        description="Paper size for the rendered PDF document.",
    )
    font_size: int = Field(
        default=11,
        title="Font Size (pt)",
        description="Base font size in points.",
        ge=6,
        le=36,
    )
    margin: float = Field(
        default=2.0,
        title="Margin (cm)",
        description="Page margin in centimeters.",
        ge=0.5,
        le=10.0,
    )

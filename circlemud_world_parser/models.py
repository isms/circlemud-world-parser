"""Shared models used across multiple parser modules."""
from pydantic import BaseModel, Field


class Flag(BaseModel):
    """A flag with a numeric value and optional descriptive note."""

    value: int = Field(..., description="Numeric flag value")
    note: str | None = Field(None, description="Human-readable flag name")


class ExtraDescription(BaseModel):
    """An extra description triggered by examining keywords."""

    keywords: list[str] = Field(..., description="Keywords that trigger this description")
    desc: str = Field(..., description="Description text")

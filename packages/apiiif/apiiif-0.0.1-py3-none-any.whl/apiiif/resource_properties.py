from pydantic import BaseModel, AnyUrl, root_validator


class LanguageString(BaseModel):
    """A language string is a dictionary with language codes as keys and
    strings as values. The language codes are ISO 2-character codes.
    Add additional languages as needed, but once more than one exists,
    logic is needed to enable all to be optional, but one must be declared."""

    @root_validator(pre=True)
    def check_language_string(cls, values):
        if len(values) == 0:
            raise ValueError('At least one language string must be provided.')
        return values

    en: list[str] | None
    fr: list[str] | None
    de: list[str] | None
    it: list[str] | None
    es: list[str] | None


class LabelValue(BaseModel):
    """Used as the value of the requiredStatement and metadata items."""
    label: LanguageString
    value: LanguageString


class Image(BaseModel):
    id: AnyUrl
    type: str = 'Image'
    width: int | None
    height: int | None


class Thumbnail(Image):
    format: str = 'image/jpeg'


class Logo(Image):
    format: str = 'image/png'


class Homepage(BaseModel):
    id: AnyUrl
    type: str = 'Text'
    label: LanguageString
    format: str = 'text/html'
    language: list[str]


class PartOf(BaseModel):
    id: AnyUrl
    type: str = 'Collection'


class Provider(BaseModel):
    id: AnyUrl
    type: str = 'Agent'
    label: LanguageString
    homepage: list[Homepage] | None
    logo: list[Logo] | None


class Choice(BaseModel):
    type: str = 'Choice'
    items: list = []


class ImageService(BaseModel):
    id: AnyUrl
    type: str = 'ImageService3'
    profile: str = 'level0'

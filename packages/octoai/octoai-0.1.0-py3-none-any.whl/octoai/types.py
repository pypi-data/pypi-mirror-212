"""Type definitions to help communicate with endpoints."""

import base64
import os
from io import BytesIO
from typing import Any, Dict, Tuple

import httpx
import soundfile
from numpy.typing import ArrayLike
from PIL import Image as PImage
from pydantic import BaseModel, Field


def file_b64encode(file_bytes: bytes) -> str:
    """Encode file as a base64 string.

    :param file_bytes: an image in byte format
    :type file_bytes: bytes
    :return: an file encoded as a base64 string.
    :rtype: str
    """
    return base64.b64encode(file_bytes).decode("ascii")


def file_b64decode(file_b64: str) -> bytes:
    """Decode base64 string into a file.

    :param file_b64: base64 image string
    :type file_b64: str
    :return: file as bytes
    :rtype: bytes
    """
    return base64.b64decode(bytes(file_b64, "ascii"))


class Text(BaseModel):
    """Text type for models that accept or return text."""

    text: str


class Image(BaseModel):
    """Image helpers for models that accept or return images.

    :param BaseModel: base model
    :type BaseModel: :class:`BaseModel`
    :raises ValueError: ``from_file`` method failed to load image.
    :raises ValueError: ``from_url`` method was unable to reach the url.
    :return: base64 encoded image
    :rtype: str
    """

    image_b64: str = Field(description="base64-encoded image file")

    @classmethod
    def from_base64(cls, b64: str):
        """Create from base64 encoded string.

        :param b64: a base64 encoded string
        :type b64: str
        :return: :class:`Image` wrapped base64 image
        :rtype: :class:`Image`
        """
        return cls(image_b64=b64)

    @classmethod
    def from_endpoint_response(cls, resp_dict: Dict[str, Any], key: str):
        """Create from endpoint response."""
        if key in resp_dict:
            return cls(image_b64=resp_dict[key]["image_b64"])
        elif "output" in resp_dict and key in resp_dict["output"]:
            return cls(image_b64=resp_dict["output"][key]["image_b64"])

        raise ValueError(f"{key} not in resp_dict")

    @classmethod
    def from_pil(cls, image_pil: PImage, format="JPEG"):
        """Create from PIL image.

        :param image_pil: image in pil format
        :type image_pil: PImage
        :param format: target output format, defaults to "JPEG"
        :type format: str, optional
        :return: :class:`Image` wrapped base64 image.
        :rtype: :class:`Image`
        """
        buffer = BytesIO()
        image_pil.save(buffer, format=format)
        return cls(image_b64=file_b64encode(buffer.getvalue()))

    @classmethod
    def from_file(cls, image_file: str):
        """Create from local file.

        :param image_file: path for image_file
        :type image_file: str
        :raises ValueError: image_file not found at provided path
        :return: :class:`Image` wrapped base64 image.
        :rtype: :class:`Image`
        """
        if not os.path.isfile(image_file):
            raise ValueError(f"File {image_file} does not exist")

        with open(image_file, "rb") as fd:
            return cls(image_b64=file_b64encode(fd.read()))

    @classmethod
    def from_url(cls, image_url: str, follow_redirects=False):
        """Create from URL.

        :param image_url: url leading to an image
        :type image_url: str
        :raises ValueError: there was an error reaching the target url
        :return: :class:`Image` wrapped base64 image.
        :rtype: :class:`Image`
        """
        resp = httpx.get(image_url, follow_redirects=follow_redirects)
        if resp.status_code != 200:
            raise ValueError(f"status {resp.status_code} ({image_url})")

        return cls(image_b64=file_b64encode(resp.content))

    def is_valid(self):
        """Check if this is a valid image.

        :return: True if valid, False if invalid
        :rtype: bool
        """
        try:
            self.to_pil().verify()
            return True
        except Exception:
            return False

    def to_pil(self) -> PImage:
        """Convert to PIL Image.

        :return: pil image
        :rtype: PImage
        """
        return PImage.open(BytesIO(file_b64decode(self.image_b64)))

    def to_file(self, file_name: str):
        """Save file to disc.

        :param file_name: file descriptor or path
        :type file_name: str
        """
        with open(file_name, "wb") as fd:
            fd.write(file_b64decode(self.image_b64))


class Audio(BaseModel):
    """Audio helpers for models that accept or return audio.

    :param BaseModel: base model
    :type BaseModel: :class:`BaseModel`
    :raises ValueError: ``from_file`` method failed to load file
    :raises ValueError: ``from_url`` method was unable to reach the url.
    :return: base64 encoded audio
    :rtype: str
    """

    audio_b64: str = Field(description="base64-encoded audio file")

    @classmethod
    def from_base64(cls, b64: str):
        """Create from base64 encoded string.

        :param b64: _description_
        :type b64: str
        :return: _description_
        :rtype: _type_
        """
        return cls(audio_b64=b64)

    @classmethod
    def from_endpoint_response(cls, resp_dict: Dict[str, Any], key: str):
        """Create from endpoint response."""
        if key in resp_dict:
            return cls(audio_b64=resp_dict[key]["audio_b64"])
        elif "output" in resp_dict and key in resp_dict["output"]:
            return cls(audio_b64=resp_dict["output"][key]["audio_b64"])

        raise ValueError(f"{key} not in resp_dict")

    @classmethod
    def from_numpy(cls, data: ArrayLike, sample_rate: int, format="WAV"):
        """Create from numpy data (frames x channels).

        :param data: frames x channels of audio
        :type data: ArrayLike
        :param sample_rate: samples per second taken to create signal
        :type sample_rate: int
        :param format: source format, defaults to "WAV"
        :type format: str, optional
        :return: :class:`Audio` wrapper around base64 audio string.
        :rtype: :class:`Audio`
        """
        buffer = BytesIO()
        soundfile.write(buffer, data=data, samplerate=sample_rate, format=format)
        return cls(audio_b64=file_b64encode(buffer.getvalue()))

    @classmethod
    def from_file(cls, audio_file: str):
        """Create from local file.

        :param audio_file: location or name of audio_file
        :type audio_file: str
        :raises ValueError: Unable to locate file at audio_file
        :return: :class:`Audio` wrapper around base64 audio string.
        :rtype: :class:`Audio`
        """
        if not os.path.isfile(audio_file):
            raise ValueError(f"File {audio_file} does not exist")

        with open(audio_file, "rb") as fd:
            return cls(audio_b64=file_b64encode(fd.read()))

    @classmethod
    def from_url(cls, audio_url: str, follow_redirects=False):
        """Create from URL.

        :param audio_url: target URL leading to audio.
        :type audio_url: str
        :raises ValueError: URL returned an HTTP status other than OK.
        :return: :class:`Audio` wrapper around base64 audio string.
        :rtype: :class:`Audio`
        """
        resp = httpx.get(audio_url, follow_redirects=follow_redirects)
        if resp.status_code != 200:
            raise ValueError(f"status {resp.status_code} ({audio_url})")

        return cls(audio_b64=file_b64encode(resp.content))

    def is_valid(self):
        """Check if this is a valid audio.

        :return: True if it's valid, false if not.
        :rtype: bool
        """
        try:
            self.to_numpy()
            return True
        except Exception:
            return False

    def to_numpy(self) -> Tuple[ArrayLike, int]:
        """Convert to numpy data.

        :return: numpy data interpretation of audio
        :rtype: Tuple[ArrayLike, int]
        """
        fd = BytesIO(file_b64decode(self.audio_b64))
        data, sample_rate = soundfile.read(fd)
        return (data, sample_rate)

    def to_file(self, file_name: str):
        """Save to disk.

        :param file_name: file descriptor or path.
        :type file_name: str
        """
        with open(file_name, "wb") as fd:
            fd.write(file_b64decode(self.audio_b64))

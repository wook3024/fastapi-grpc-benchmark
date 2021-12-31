import cv2
import base64
import numpy as np

from typing import Union
from pathlib import Path


def save_image_data(encoded_base64_data: str, save_image_path: Union[str, Path]) -> str:
    if isinstance(save_image_path, str):
        save_image_path = Path(save_image_path)
    bytes_data = base64.b64decode(encoded_base64_data)
    encoded_img = np.fromstring(bytes_data, dtype=np.uint8)
    np_array = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    save_image_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(save_image_path.as_posix(), np_array)
    image_shape = "×".join([str(value) for value in np_array.shape])
    return image_shape


def save_bytes_data(save_url: str, data: bytes):
    with open(save_url, "wb") as f:
        f.write(data)

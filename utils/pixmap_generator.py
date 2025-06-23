from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


def generate_pixmap(filepath, width, height):
    pixmap = QPixmap(filepath)

    pixmap_ratio = pixmap.width() / pixmap.height()
    container_ratio = width / height

    if container_ratio > pixmap_ratio:
        scaled_height = int(pixmap.width() / container_ratio)
        y_offset = (pixmap.height() - scaled_height) // 2
        cropped = pixmap.copy(0, y_offset, pixmap.width(), scaled_height)
    else:
        scaled_width = int(pixmap.height() * container_ratio)
        x_offset = (pixmap.width() - scaled_width) // 2
        cropped = pixmap.copy(x_offset, 0, scaled_width, pixmap.height())

    scaled_pixmap = cropped.scaled(width, height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    return scaled_pixmap

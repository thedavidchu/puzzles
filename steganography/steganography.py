import argparse
import os

import cv2


# Bit shift constants
BIT_SHIFT = 5
VISIBLE_MASK_CONST = int(BIT_SHIFT * '1' + (8 - BIT_SHIFT) * '0', 2)


def combine_visible_and_hidden(
    visible_image_path: str,
    hidden_image_path: str,
    steganograph_output_image_path: str,
):
    assert os.path.exists(visible_image_path)
    assert os.path.exists(hidden_image_path)
    
    # Open input images and resize visible to hidden size
    visible_image = cv2.imread(visible_image_path)
    hidden_image = cv2.imread(hidden_image_path)
    visible_image = cv2.resize(
        visible_image,
        hidden_image.shape[:2][::-1],
        interpolation=cv2.INTER_AREA
    )

    # Hide hidden image on the lower 3 bits
    visible_image &= VISIBLE_MASK_CONST
    hidden_image >>= BIT_SHIFT
    steganograph = visible_image + hidden_image

    # Save in lossless format
    pre, ext = os.path.splitext(steganograph_output_image_path)
    cv2.imwrite(pre + '.png', steganograph)


def extract_hidden_image(
    steganograph_image_path,
    hidden_output_image_path
):
    assert os.path.exists(steganograph_image_path)
    
    # Open steganograph and shift; save it to hidden path
    steganograph_image = cv2.imread(steganograph_image_path)
    hidden_image = (steganograph_image << BIT_SHIFT)
    cv2.imwrite(hidden_output_image_path, hidden_image)

    # Save in lossless format
    pre, ext = os.path.splitext(hidden_output_image_path)
    cv2.imwrite(pre + '.png', hidden_image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--visible-path", type=str, required=False, default=None)
    parser.add_argument("--hidden-path", type=str, required=True)
    parser.add_argument("--steganograph-path", type=str, required=True)
    args = parser.parse_args()

    if args.visible_path is None:   # Visible path is only specified for encoding
        extract_hidden_image(args.steganograph_path, args.hidden_path)
    else:
        combine_visible_and_hidden(args.visible_path, args.hidden_path, args.steganograph_path)


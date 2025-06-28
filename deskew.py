import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def calculate_horizontal_energy(img):
    # Sum each row (horizontal projection)
    row_sums = np.sum(img, axis=1)
    # High variance means text is well-aligned horizontally
    return np.var(row_sums)


def find_best_rotation(img, angle_range=(-30, 30), step=0.5):
    # Find the best rotation angle by trying different angles directly
    h, w = img.shape[:2]
    center = (w // 2, h // 2)

    max_energy = 0
    best_angle = 0

    angles = []
    energies = []

    for angle in np.arange(angle_range[0], angle_range[1] + step, step):

        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC,
                                 borderMode=cv2.BORDER_REPLICATE)

        energy = calculate_horizontal_energy(rotated)

        angles.append(angle)
        energies.append(energy)

        if energy > max_energy:
            max_energy = energy
            best_angle = angle

    plt.figure(figsize=(10, 5))
    plt.plot(angles, energies)
    plt.axvline(x=best_angle, color='r', linestyle='--')
    plt.title(f'Horizontal Energy vs. Rotation Angle (Best: {best_angle:.2f}°)')
    plt.xlabel('Angle (degrees)')
    plt.ylabel('Horizontal Energy')
    plt.grid(True)
    plt.show()

    return best_angle


def deskew_direct(img, angle_range=(-30, 30), step=0.5):
    if img.ndim == 2:
        gray = img
    elif img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        raise ValueError("Unsupported image shape.")

    angle = find_best_rotation(gray, angle_range, step)
    rotated = Image.fromarray(img)
    if angle != 0:
        rotated = rotated.rotate(angle, expand=True, fillcolor=255)

    return np.array(rotated), angle



if __name__ == "__main__":
    img = cv2.imread('Calibri\\lorem_ipsum_rotated.png', cv2.IMREAD_GRAYSCALE)

    straight, angle = deskew_direct(img, angle_range=(-30, 30), step=0.5)
    print(f"Final rotation: {angle:.2f}°")
    cv2.imwrite('rotate.png', straight)
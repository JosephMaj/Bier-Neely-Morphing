# Joseph Majesky

import cv2


start_pt = ()
end_pt = ()

Map_of_Lines = {}


def fill_map(image_array):
    for target_image in image_array:
        Map_of_Lines[hash(target_image.tostring())] = []


def select_line(event, x, y, flags, params):
    global start_pt, end_pt

    if event == cv2.EVENT_LBUTTONDOWN:
        start_pt = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        end_pt = (x, y)
        cv2.line(clone, start_pt,end_pt, (0,255,0),1)
        Map_of_Lines[hash(image_name)].append((start_pt, end_pt))
        cv2.imshow("image", clone)


img1 = cv2.imread("green.jpg")
img2 = cv2.imread("green2.png")

images = [img1, img2]

cv2.namedWindow("image")
cv2.setMouseCallback("image", select_line)



fill_map(images)

while True:
    key = None
    for image in images:
        image_name=image.tostring()
        clone=image.copy()
        while True:
            cv2.imshow("image", clone)
            key = cv2.waitKey(0) & 0xFF

            if key == ord("q"):
                break

            elif key == ord("n"):
                break

        if key == ord("q"):
            break

        elif key == ord("n"):
            pass

    if key == ord("q"):
        break


def get_images():
    return images


def get_map():
    return Map_of_Lines

import numpy as np
from PIL import ImageGrab
import cv2

SCREEN_HEIGHT = 600

def draw_lines(img, lines):
    try:
        for line in lines:
            coords = line[0]
            # modifies image live, doesn't need to return modified image
            cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 255, 255], 3) # (img, (x1, y1), (x2, y1), [r, g, b], thickness)
    except:
        pass

# region of interest
def roi(img, vertices):
    mask = np.zeros_like(img) # zero-filled tensor with same indices as passed image
    cv2.fillPoly(mask, vertices, 255) # fill the mask tensor poly with passed vertices
    masked_img = cv2.bitwise_and(img, mask) # take only masked portion of img
    return masked_img

def process_img(image):
    original_image = image
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1 = 200, threshold2 = 300) # Canny edge detection alg
    processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0) # apply blur to image to remove anti-aliasing issue

    vertices = np.array([[10, 500], [10, 300], [300, 200], [500, 200], [800, 300], [800, 500],], np.int32)
    
    processed_img = roi(processed_img, [vertices]) # apply mask for ROI to processed screen image

    lines = cv2.HoughLinesP(processed_img, rho=1, theta=np.pi/180, threshold=180, minLineLength=20, maxLineGap=15)
    # declare default slopes of lane lines, in case none are found.
    m1 = 0
    m2 = 0
    try:
    #draw_lines(processed_img, lines)
        l1, l2, m1, m2 = draw_lanes(original_image, lines)
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0, 255, 0], 20)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0, 255, 0], 20)
    except Exception as e:
        print(f"PRINTING ERROR: {str(e)}")
        pass
    try:
        for coords in lines:
            try:
                cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 0, 0], 3)
            except Exception as e:
                print(str(e))

    except Exception as e:
        pass

    return processed_img, original_image, m1, m2
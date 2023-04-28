import cv2
import math
import os



def extract_squares_form_starting_position(image_name, image_number):
    piece_list = ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"]
    for i in range(5):
        if not os.path.exists(f"images/{piece_list[i]}"):
            os.makedirs(f"images/{piece_list[i]}")
    if not os.path.exists("images/Pawn"):
        os.makedirs("images/Pawn")
    if not os.path.exists(f"images/Blank"):
        os.makedirs("images/Blank")
    img = cv2.imread(image_name)
    img_shape = img.shape
    square_side = int(img_shape[0]/8)
    crop_ratio = 0.05
    for i, piece in enumerate(piece_list):
        square_b = crop_image(img[0: square_side, i*square_side:(i+1)*square_side], square_side, crop_ratio)
        square_w = crop_image(img[7 * square_side: 8 * square_side, i*square_side:(i+1)*square_side], square_side, crop_ratio)
        cv2.imwrite(f"images/{piece}/Black_{piece}{i}{image_number}.jpg", square_b)
        cv2.imwrite(f"images/{piece}/White_{piece}{i}{image_number}.jpg", square_w)
    cv2.imwrite(f"images/Pawn/Black_Pawn{image_number}.jpg", crop_image(img[square_side: 2 * square_side, 0:square_side], square_side, crop_ratio))
    cv2.imwrite(f"images/Pawn/White_Pawn{image_number}.jpg", crop_image(img[6*square_side: 7 * square_side, 0:square_side], square_side, crop_ratio))
    cv2.imwrite(f"images/Pawn/Black_Pawn2{image_number}.jpg", crop_image(img[square_side: 2 * square_side, square_side:2*square_side], square_side, crop_ratio))
    cv2.imwrite(f"images/Pawn/White_Pawn2{image_number}.jpg", crop_image(img[6*square_side: 7 * square_side, square_side:2*square_side], square_side, crop_ratio))
    cv2.imwrite(f"images/Blank/Blank_White{image_number}.jpg", crop_image(img[2 * square_side: 3 * square_side, 0:square_side], square_side, crop_ratio))
    cv2.imwrite(f"images/Blank/Blank_Black{image_number}.jpg", crop_image(img[3 * square_side: 4 * square_side, 0:square_side], square_side, crop_ratio))


def crop_image(img, side, ratio_on_each_side):
    cropped_start = math.floor(ratio_on_each_side*side)
    cropped_finish = math.floor((1-ratio_on_each_side)*side)
    img = img[cropped_start: cropped_finish, cropped_start: cropped_finish]
    return img


#extract_squares_form_starting_position("images/chess_board2.jpg", 1)


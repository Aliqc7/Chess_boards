import cv2
import math



def extract_squares_form_starting_position(image_name, image_number):
    piece_list = ["Rook", "Knight", "Bishop", "Queen", "King"]
    img = cv2.imread(image_name)
    img_shape = img.shape
    square_side = int(img_shape[0]/8)
    cropped_start = math.floor(0.05*square_side)
    cropped_finish = math.floor(0.95*square_side)
    for i in range(len(piece_list)):
        square_b = img[0: square_side, i*square_side:(i+1)*square_side]
        square_w = img[7 * square_side: 8 * square_side, i*square_side:(i+1)*square_side]
        square_b = square_b[cropped_start: cropped_finish, cropped_start: cropped_finish]
        square_w = square_w[cropped_start: cropped_finish, cropped_start: cropped_finish]
        cv2.imwrite(f"images/{piece_list[i]}/Black_{piece_list[i]}{image_number}.jpg", square_b)
        cv2.imwrite(f"images/{piece_list[i]}/White_{piece_list[i]}{image_number}.jpg", square_w)
    cv2.imwrite(f"images/Pawn/Black_Pawn{image_number}.jpg", img[square_side: 2 * square_side, 0:square_side])
    cv2.imwrite(f"images/Pawn/White_Pawn{image_number}.jpg", img[6*square_side: 7 * square_side, 0:square_side])
    cv2.imwrite(f"images/Blank/Blank_White{image_number}.jpg", img[2 * square_side: 3 * square_side, 0:square_side])
    cv2.imwrite(f"images/Blank/Blank_Black{image_number}.jpg", img[3 * square_side: 4 * square_side, 0:square_side])


#extract_squares_form_starting_position("chess_board.png")


import cv2
import math
import os
import glob
import numpy as np

label_list = ["Blank", "Rook", "Knight", "Bishop", "Queen", "King", "Pawn"]

# def extract_squares_form_starting_position(path, image_name, image_number):
#     piece_list = ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"]
#     for i in range(5):
#         if not os.path.exists(f"{path}/{piece_list[i]}"):
#             os.makedirs(f"{path}/{piece_list[i]}")
#     if not os.path.exists(f"{path}/Pawn"):
#         os.makedirs(f"{path}/Pawn")
#     if not os.path.exists(f"{path}/Blank"):
#         os.makedirs(f"{path}/Blank")
#     img = cv2.imread(image_name)
#     img_shape = img.shape
#     square_side = int(img_shape[0]/8)
#     crop_ratio = 0.05
#     for i, piece in enumerate(piece_list):
#         square_b = crop_image(img[0: square_side, i*square_side:(i+1)*square_side], square_side, crop_ratio)
#         square_w = crop_image(img[7 * square_side: 8 * square_side, i*square_side:(i+1)*square_side], square_side, crop_ratio)
#         cv2.imwrite(f"{path}/{piece}/Black_{piece}{i}{image_number}.jpg", square_b)
#         cv2.imwrite(f"{path}/{piece}/White_{piece}{i}{image_number}.jpg", square_w)
#     cv2.imwrite(f"{path}/Pawn/Black_Pawn{image_number}.jpg", crop_image(img[square_side: 2 * square_side, 0:square_side], square_side, crop_ratio))
#     cv2.imwrite(f"{path}/Pawn/White_Pawn{image_number}.jpg", crop_image(img[6*square_side: 7 * square_side, 0:square_side], square_side, crop_ratio))
#     cv2.imwrite(f"{path}/Pawn/Black_Pawn2{image_number}.jpg", crop_image(img[square_side: 2 * square_side, square_side:2*square_side], square_side, crop_ratio))
#     cv2.imwrite(f"{path}/Pawn/White_Pawn2{image_number}.jpg", crop_image(img[6*square_side: 7 * square_side, square_side:2*square_side], square_side, crop_ratio))
#     cv2.imwrite(f"{path}/Blank/Blank_White{image_number}.jpg", crop_image(img[2 * square_side: 3 * square_side, 0:square_side], square_side, crop_ratio))
#     cv2.imwrite(f"{path}/Blank/Blank_Black{image_number}.jpg", crop_image(img[3 * square_side: 4 * square_side, 0:square_side], square_side, crop_ratio))


def crop_image(img, side, ratio_on_each_side):
    cropped_start = math.floor(ratio_on_each_side*side)
    cropped_finish = math.floor((1-ratio_on_each_side)*side)
    img = img[cropped_start: cropped_finish, cropped_start: cropped_finish]
    return img


# def construct_dataset(path, label_list):
#     y = []
#     x = np.empty([1, 100,100,3])
#     for i, label in enumerate(label_list):
#         filelist = glob.glob(f"{path}/{label}/*.jpg")
#         for file_name in filelist:
#             xx = np.array([cv2.resize(cv2.imread(file_name), (100,100))])
#             x = np.append(x, xx, axis=0)
#             y.append(i)
#     x = np.delete(x,0 ,0)
#
#     return x, y


# def read_and_resize_square(file_name):
#     xx = np.array([cv2.resize(cv2.imread(file_name), (100, 100))])
#     x = xx.reshape(1,-1)
#     return x


def create_dataset_from_board_single_image(img_path, img_size, crop_ratio):
    img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img_shape = img_gray.shape
    square_side = int(img_shape[0]/8)
    x = np.zeros(shape=(64, img_size, img_size))
    for i in range(8):
        for j in range(8):
            square = crop_image(img_gray[i*square_side: (i+1)*square_side, j * square_side:(j + 1) * square_side], square_side, crop_ratio)/255
            square = cv2.resize(square, (img_size, img_size))
            x[8*i+j] = square
    return x

def create_labels_for_starting_position(label_list):
    y = np.zeros((64,1))
    y[8:16, 0] = label_list.index("Pawn")
    y[48:56, 0] = label_list.index("Pawn")
    y[0, 0] = label_list.index("Rook")
    y[7, 0] = label_list.index("Rook")
    y[56, 0] = label_list.index("Rook")
    y[63, 0] = label_list.index("Rook")
    y[1, 0] = label_list.index("Knight")
    y[6, 0] = label_list.index("Knight")
    y[57, 0] = label_list.index("Knight")
    y[62, 0] = label_list.index("Knight")
    y[2, 0] = label_list.index("Bishop")
    y[5, 0] = label_list.index("Bishop")
    y[58, 0] = label_list.index("Bishop")
    y[61, 0] = label_list.index("Bishop")
    y[3, 0] = label_list.index("Queen")
    y[4, 0] = label_list.index("King")
    y[59, 0] = label_list.index("Queen")
    y[60, 0] = label_list.index("King")
    return y

def create_training_dataset(path, label_list, img_size, crop_ratio):
    filelist = glob.glob(f"{path}/*.*")
    n_files = len(filelist)
    x = np.zeros(shape=(64*n_files, img_size, img_size))
    y = np.zeros((64*n_files,1))
    for i, file in enumerate(filelist):
        x[i*64: (i+1)*64] = create_dataset_from_board_single_image(file, img_size, crop_ratio)
        y[i*64: (i+1)*64] = create_labels_for_starting_position(label_list)

    return x, y

#extract_squares_form_starting_position("images/chess_board2.jpg", 1)


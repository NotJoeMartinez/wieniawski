import cv2
import os
import pickle
from glob import glob
from scipy.ndimage import binary_fill_holes
from skimage.morphology import thin
import matplotlib.pyplot as plt


from .plot_utils import *
from .commonfunctions import *
from .pre_processing import *
from .connected_componentes import *
from .staff import calculate_thickness_spacing, remove_staff_lines, coordinator
from .segmenter import Segmenter
from .fit import predict

label_map = {
    0: {
        0: 'N0'
    },
    1: {
        0: 'b2',
        1: 'a2'
    },
    2: {
        0: 'g2',
        1: 'f2'
    },
    3: {
        0: 'e2',
        1: 'd2'
    },
    4: {
        0: 'c2',
        1: 'b1'
    },
    5: {
        0: 'a1',
        1: 'g1'
    },
    6: {
        0: 'f1',
        1: 'e1'
    },
    7: {
        0: 'd1',
        1: 'c1'
    }
}


def estim(c, idx, imgs_spacing, imgs_rows):
    spacing = imgs_spacing[idx]
    rows = imgs_rows[idx]
    margin = 1+(spacing/4)
    for index, line in enumerate(rows):
        if c >= line - margin and c <= line + margin:
            return index+1, 0
        elif c >= line + margin and c <= line + 3*margin:
            return index+1, 1
    return 7, 1


def get_note_name(prev, octave, duration):
    if duration in ['4', 'a_4']:
        return f'{octave[0]}{prev}{octave[1]}/4'
    elif duration in ['8', '8_b_n', '8_b_r', 'a_8']:
        return f'{octave[0]}{prev}{octave[1]}/8'
    elif duration in ['16', '16_b_n', '16_b_r', 'a_16']:
        return f'{octave[0]}{prev}{octave[1]}/16'
    elif duration in ['32', '32_b_n', '32_b_r', 'a_32']:
        return f'{octave[0]}{prev}{octave[1]}/32'
    elif duration in ['2', 'a_2']:
        return f'{octave[0]}{prev}{octave[1]}/2'
    elif duration in ['1', 'a_1']:
        return f'{octave[0]}{prev}{octave[1]}/1'
    else:
        return "c1/4"


def filter_beams(prims, prim_with_staff, bounds):
    n_bounds = []
    n_prims = []
    n_prim_with_staff = []
    for i, prim in enumerate(prims):
        if prim.shape[1] >= 2*prim.shape[0]:
            continue
        else:
            n_bounds.append(bounds[i])
            n_prims.append(prims[i])
            n_prim_with_staff.append(prim_with_staff[i])
    return n_prims, n_prim_with_staff, n_bounds


def get_chord_notation(chord_list):
    chord_res = "{"
    for chord_note in chord_list:
        chord_res += (str(chord_note) + ",")
    chord_res = chord_res[:-1]
    chord_res += "}"

    return chord_res

# I don't know what's happening either ¯\_(ツ)_/¯ 
"""
    - coord_imgs: is an array of ndarrays with True/False values
    These seem to correspond to the staff lines in the image

    coord_imgs[0]: (156, 1583)
    coord_imgs[1]: (158, 1583)
    coord_imgs[2]: (156, 1583)

    - prev: is a string that is used to keep track of the previous note
    The inner loop updates prev so it's not redefined in the outer loop
    
    - black_names: is a list of strings that correspond to the names of the notes

    - primitives: 
        images detected by the connected components algorithm
    - prim_with_staff:
        images detected by the connected components algorithm with staff lines
    


"""
 
def recognize(out_file, most_common, coord_imgs, imgs_with_staff, 
              imgs_spacing, imgs_rows, og_img, model_path=None):

    black_names = ['4', '8', '8_b_n', '8_b_r', '16', '16_b_n', '16_b_r',
                   '32', '32_b_n', '32_b_r', 'a_4', 'a_8', 'a_16', 'a_32', 'chord']



    ring_names = ['2', 'a_2']
    whole_names = ['1', 'a_1']

    disk_size = most_common / 4

    if len(coord_imgs) > 1:
        out_file.write("{\n")



    all_labels = []
    labeled_imgs = []
    for i, img in enumerate(coord_imgs):
        res = []
        prev = ''
        time_name = ''

        primitives, prim_with_staff, boundary = get_connected_components(
            img, imgs_with_staff[i])

        

        detected = cv2.cvtColor(np.array(255*imgs_with_staff[i].copy()).astype(np.uint8),cv2.COLOR_GRAY2RGB)


        for j, prim in enumerate(primitives):
            minr, minc, maxr, maxc = boundary[j]

            prim = binary_opening(prim, square(
                np.abs(most_common-imgs_spacing[i])))

            saved_img = (255*(1 - prim)).astype(np.uint8)

            labels = predict(saved_img, model_path=model_path)
            print(f"Predicted labels: {labels}")
            octave = None
            label = labels[0]

       
            cv2.rectangle(detected, (minc, minr), (maxc, maxr), (0, 0, 255), 2)
            # means we have a valid note, prev is the sharp or flat stuff
            if label in black_names:

                test_img = np.copy(prim_with_staff[j])
                test_img = binary_dilation(test_img, disk(disk_size))

                comps, comp_w_staff, bounds = get_connected_components(
                    test_img, prim_with_staff[j])

                comps, comp_w_staff, bounds = filter_beams(
                    comps, comp_w_staff, bounds)

                bounds = [np.array(bound) + disk_size-2 for bound in bounds]

                if len(bounds) > 1 and label not in ['8_b_n', '8_b_r', '16_b_n', '16_b_r', '32_b_n', '32_b_r']:
                    l_res = []
                    bounds = sorted(bounds, key=lambda b: -b[2])

                    for k in range(len(bounds)):
                        idx, p = estim(
                            boundary[j][0]+bounds[k][2], i, imgs_spacing, imgs_rows)

                        l_res.append(f'{label_map[idx][p]}/4')
                        if k+1 < len(bounds) and (bounds[k][2]-bounds[k+1][2]) > 1.5*imgs_spacing[i]:

                            idx, p = estim(
                                boundary[j][0]+bounds[k][2]-imgs_spacing[i]/2, i, imgs_spacing, imgs_rows)
                            l_res.append(f'{label_map[idx][p]}/4')

                    
                    cv2.putText(detected, str(l_res), (minc-2, minr-2), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                    res.append(sorted(l_res))
                else:
                    for bbox in bounds:
                        c = bbox[2]+boundary[j][0]
                        line_idx, p = estim(int(c), i, imgs_spacing, imgs_rows)
                        l = label_map[line_idx][p]
                        note_name = get_note_name(prev, l, label)
                        cv2.putText(detected, note_name, (minc-2, minr-2), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                        res.append(note_name)

            elif label in ring_names:
                head_img = 1-binary_fill_holes(1-prim)
                head_img = binary_closing(head_img, disk(disk_size))
                comps, comp_w_staff, bounds = get_connected_components(
                    head_img, prim_with_staff[j])
                for bbox in bounds:
                    c = bbox[2]+boundary[j][0]
                    line_idx, p = estim(int(c), i, imgs_spacing, imgs_rows)
                    l = label_map[line_idx][p]
                    note_name = get_note_name(prev, l, label)
                    cv2.putText(detected, note_name, (minc-2, minr-2), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                    res.append(note_name)

            elif label in whole_names:
                c = boundary[j][2]
                line_idx, p = estim(int(c), i, imgs_spacing, imgs_rows)
                l = label_map[line_idx][p]
                note_name = get_note_name(prev, l, label)
                cv2.putText(detected, note_name, (minc-2, minr-2), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                res.append(note_name)

            elif label in ['bar', 'bar_b', 'clef', 'clef_b', 'natural', 'natural_b', 't24', 't24_b', 't44', 't44_b'] or label in []:
                print(f"bar?: {label}")
                continue

            elif label in ['#', '#_b']:
                if prim.shape[0] == prim.shape[1]:
                    prev = '##'
                else:
                    prev = '#'

            elif label in ['cross']:
                prev = '##'

            elif label in ['flat', 'flat_b']:
                if prim.shape[1] >= 0.5*prim.shape[0]:
                    prev = '&&'
                else:
                    prev = '&'

            elif label in ['dot', 'dot_b', 'p']:
                if len(res) == 0 or (len(res) > 0 and res[-1] in ['flat', 'flat_b', 'cross', '#', '#_b', 't24', 't24_b', 't44', 't44_b']):
                    continue
                res[-1] += '.'

            elif label in ['t2', 't4']:
                time_name += label[1]

            elif label == 'chord':
                img = thin(1-prim.copy(), max_iter=20)
                head_img = binary_closing(1-img, disk(disk_size))

            if label not in ['flat', 'flat_b', 'cross', '#', '#_b']:
                prev = ''
            
            # show_images([detected], [label])

        write_predictions(out_file, res, time_name)
        
        labeled_imgs.append(detected)

    if len(coord_imgs) > 1:
        out_file.write("}")


    for i, img in enumerate(coord_imgs):
        plt.imshow(labeled_imgs[i])
        plt.title(f"Predicted labels: {res}")
        plt.show()

    # show_images(labeld_imgs, ['1', '2', '3'])
    # show_images([detected], ['Detected'])
    # cv2.imwrite('detected.png', detected)
    # plt.imshow(og_img)
    # plt.title(f"Predicted labels: {res}")
    # plt.show()


    print(f"wrote predictions to {out_file}")
    print("###########################", all_labels, "##########################")


def write_predictions(out_file, res, time_name):
    def format_elements(elements):
        formatted_elements = []
        for elem in elements:
            if type(elem) != list:
                formatted_elements.append(str(elem))
            else:
                formatted_elements.append(get_chord_notation(elem))
        return ' '.join(formatted_elements)

    if len(time_name) == 2:
        out_file.write("[ " + "\\" + "meter<\"" + str(time_name[0]) + "/" + str(time_name[1]) + "\">" + format_elements(res) + "]\n")
    elif len(time_name) == 1:
        out_file.write("[ " + "\\" + "meter<\"" + '4' + "/" + '2' + "\">" + format_elements(res) + "]\n")
    else:
        out_file.write("[ " + format_elements(res) + "]\n")

    print(f"Writing predictions: {res}")

def predict_file(input_path, output_path, model_path=None):
    import warnings
    from sklearn.exceptions import ConvergenceWarning
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    warnings.filterwarnings("ignore", category=UserWarning)

    img_name = input_path.split('/')[-1].split('.')[0]
    out_file = open(f'{output_path}/{img_name}.txt', "w")

    print(f"Processing new image {input_path}...")

    img = io.imread(input_path)
    img = gray_img(img)

    # horizontal = IsHorizontal(img)
    horizontal = True 

    original = img.copy()

    gray = img 
    bin_img = get_thresholded(gray, threshold_otsu(gray))

    segmenter = Segmenter(bin_img)
    imgs_with_staff = segmenter.regions_with_staff
    most_common = segmenter.most_common

    print("most common: ", most_common)
    print(f"type: {type(most_common)}")

    imgs_spacing = []
    imgs_rows = []
    coord_imgs = []

    for i, img in enumerate(imgs_with_staff):
        spacing, rows, no_staff_img = coordinator(img, horizontal)
        imgs_rows.append(rows)
        imgs_spacing.append(spacing)
        coord_imgs.append(no_staff_img)

    print("Recognize...")

    recognize(out_file, most_common, coord_imgs,
                imgs_with_staff, imgs_spacing, imgs_rows, 
                gray, model_path=model_path)


    out_file.close()
    print("Done...")
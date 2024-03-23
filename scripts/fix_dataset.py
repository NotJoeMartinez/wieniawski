import os
import shutil
import re
from pprint import pprint

def main():
    og_dir = 'data/mozart_dataset_original'
    training_data = os.listdir(og_dir)

    labels = [
    't2', 't24', 't24_b', 't4', 't44', 't44_b',
    '#', '#_b', 'clef', 'clef_b', 'flat', 'flat_b', 'natural', 'natural_b',
    '1', '16', '16_b_n', '16_b_r', '2', '32', '32_b_n', '32_b_r', '4', '8', '8_b_n', '8_b_r',
    'a_1', 'a_2', 'a_4', 'a_8', 'a_16', 'a_32', 'bar', 'bar_b', 'chord', 'cross', 'dot', 'dot_b', 'p'
    ]

    # remove duplicates
    labels = list(set(labels))

    label_dir_map = {}
    for lable in labels:
        prifix = f'{lable}'
        label_dir_map[lable] = []
        for dir in training_data:
            match = re.match(rf'{prifix}_\d\d\d', dir)
            if match:
                label_dir_map[lable].append(dir)


    pruned_dir = 'data/pruned'
    os.makedirs(pruned_dir, exist_ok=True)


    for label, dirs in label_dir_map.items():
        os.makedirs(f'{pruned_dir}/{label}', exist_ok=True)

        count = 1
        for dir in dirs:
            for file in os.listdir(f'{og_dir}/{dir}'):
                new_file = f'{label}_{count}.png'
                shutil.copy(f'{og_dir}/{dir}/{file}', f'{pruned_dir}/{label}/{new_file}')
                count += 1




if __name__ == "__main__":
    main()



    # alt_names = ['4_009', '4_010', '4_011', '4_012', '8_013', '8_014', '8_015', '8_016', '8_b_n_017', '8_b_n_018', '8_b_r_018', '8_b_r_019', '8_b_r_020', '8_b_r_021', '16_021', '16_022', '16_023', '16_024', '16_025', '16_b_n_025', '16_b_n_026', '16_b_n_027', '16_b_n_028', '16_b_n_029', '16_b_n_030', '16_b_r_030', '16_b_r_031', '16_b_r_032', '16_b_r_033', '16_b_r_034', '16_b_r_035', '16_b_r_036', '32_036', '32_037', '32_038', '32_b_n_038', '32_b_n_039', '32_b_n_040', '32_b_n_041', '32_b_n_042', '32_b_n_043', '32_b_r_043', '32_b_r_044', '32_b_r_045', '32_b_r_046', '32_b_r_047', '32_b_r_048', '32_b_r_049', 'a_4_066', 'a_4_067', 'a_4_068', 'a_4_069', 'a_4_070', 'a_4_071', 'a_4_072', 'a_4_073', 'a_4_074', 'a_4_075', 'a_4_076', 'a_4_077', 'a_8_077', 'a_8_078', 'a_8_079', 'a_8_080', 'a_8_081', 'a_8_082', 'a_8_083', 'a_8_084', 'a_8_085', 'a_8_086', 'a_16_086', 'a_16_087', 'a_16_088', 'a_16_089', 'a_16_090', 'a_16_091', 'a_16_092', 'a_16_093', 'a_16_094', 'a_32_094', 'a_32_095', 'a_32_096', 'a_32_097', 'chord_129', 'chord_130', 'chord_131', 'chord_132', 'chord_133']

    # label_map = {
    #     '4': ['4_009', '4_010', '4_011', '4_012'],
    #     '8': ['8_013', '8_014', '8_015', '8_016'], 
    #     '8_b_n': ['8_b_n_017', '8_b_n_018'],
    #     '8_b_r': ['8_b_r_018', '8_b_r_019', '8_b_r_020', '8_b_r_021'],
    #     '16': ['16_021', '16_022', '16_023', '16_024', '16_025'],
    #     '16_b_n': ['16_b_n_025', '16_b_n_026', '16_b_n_027', '16_b_n_028', '16_b_n_029', '16_b_n_030'],
    #     '16_b_r': ['16_b_r_030', '16_b_r_031', '16_b_r_032', '16_b_r_033', '16_b_r_034', '16_b_r_035', '16_b_r_036'],
    #     '32': ['32_036', '32_037', '32_038'],
    #     '32_b_n ': ['32_b_n_038', '32_b_n_039', '32_b_n_040', '32_b_n_041', '32_b_n_042', '32_b_n_043'],
    #     '32_b_r ': ['32_b_r_043', '32_b_r_044', '32_b_r_045', '32_b_r_046', '32_b_r_047', '32_b_r_048', '32_b_r_049'],
    #     'a_4': ['a_4_066', 'a_4_067', 'a_4_068', 'a_4_069', 'a_4_070', 'a_4_071', 'a_4_072', 'a_4_073', 'a_4_074', 'a_4_075', 'a_4_076', 'a_4_077'],
    #     'a_8': ['a_8_077', 'a_8_078', 'a_8_079', 'a_8_080', 'a_8_081', 'a_8_082', 'a_8_083', 'a_8_084', 'a_8_085', 'a_8_086'],
    #     'a_16 ': ['a_16_086', 'a_16_087', 'a_16_088', 'a_16_089', 'a_16_090', 'a_16_091', 'a_16_092', 'a_16_093', 'a_16_094'],
    #     'a_32': ['a_32_094', 'a_32_095', 'a_32_096', 'a_32_097'],
    #     'chord': ['chord_129', 'chord_130', 'chord_131', 'chord_132', 'chord_133']
    # }

    # new_dataset = 'data/pruned'
    # os.makedirs(new_dataset, exist_ok=True)

    # for dir in training_data:
    #     if dir in alt_names:
    #         continue
    #     shutil.copytree(f'data/training_data/{dir}', f'{new_dataset}/{dir}')


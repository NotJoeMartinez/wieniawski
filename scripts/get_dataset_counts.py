import os
def main():
    dataset_path = "../data/training_datasets/manual_pick"

    labels = os.listdir(dataset_path)

    label_counts = {}

    for label in labels:
        label_path = os.path.join(dataset_path, label)
        count = len(os.listdir(label_path))

        label_counts[label] = count
    
    # sort by count

    sorted_label_counts = dict(sorted(label_counts.items(), key=lambda item: item[1]))
    for label, count in sorted_label_counts.items():
        print(f"{label}, {count}")


if __name__ == "__main__":
    main()
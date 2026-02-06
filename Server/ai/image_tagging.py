import cv2

def basic_image_tags(image_path):
    """
    Very basic tagging (placeholder)
    """
    tags = []

    img = cv2.imread(image_path)
    if img is None:
        return tags

    h, w, _ = img.shape

    if h > w:
        tags.append("portrait")
    else:
        tags.append("landscape")

    return tags

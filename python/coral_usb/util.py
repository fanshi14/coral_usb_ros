import numpy as np


def get_panorama_slices(width, n_split, overlap=True):
    if overlap:
        x_offsets = np.arange(n_split) * int(width / (n_split + 1))
        x_width = int(2 * width / (n_split + 1))
        x_offsets = x_offsets.astype(np.int)
        panorama_slices = [
            slice(x_offset, x_offset + x_width) for x_offset in x_offsets]
        panorama_slices.append(
            slice(width - int(x_width / 2), int(x_width / 2)))
        return panorama_slices
    else:
        x_offsets = np.arange(n_split) * int(width / n_split)
        x_width = int(width / n_split)
        x_offsets = x_offsets.astype(np.int)
        panorama_slices = [
            slice(x_offset, x_offset + x_width) for x_offset in x_offsets]
        return panorama_slices


def get_panorama_sliced_image(panorama_img, panorama_slice):
    if panorama_slice.start > panorama_slice.stop:
        left_sliced_img = panorama_img[:, panorama_slice.start:, :]
        right_sliced_img = panorama_img[:, :panorama_slice.stop, :]
        img = np.concatenate([left_sliced_img, right_sliced_img], 1)
    else:
        img = panorama_img[:, panorama_slice, :]
    return img


def get_panorama_sliced_image_xy(panorama_img, panorama_slice_width, panorama_slice_height):
    img = panorama_img[panorama_slice_height, panorama_slice_width, :]
    return img


# copied from chainercv
def non_maximum_suppression(bbox, thresh, score=None, limit=None):
    if len(bbox) == 0:
        return np.zeros((0,), dtype=np.int32)

    if score is not None:
        order = score.argsort()[::-1]
        bbox = bbox[order]
    bbox_area = np.prod(bbox[:, 2:] - bbox[:, :2], axis=1)

    selec = np.zeros(bbox.shape[0], dtype=bool)
    for i, b in enumerate(bbox):
        tl = np.maximum(b[:2], bbox[selec, :2])
        br = np.minimum(b[2:], bbox[selec, 2:])
        area = np.prod(br - tl, axis=1) * (tl < br).all(axis=1)

        iou = area / (bbox_area[i] + bbox_area[selec] - area)
        if (iou >= thresh).any():
            continue

        selec[i] = True
        if limit is not None and np.count_nonzero(selec) >= limit:
            break

    selec = np.where(selec)[0]
    if score is not None:
        selec = order[selec]
    return selec.astype(np.int32)

"""Float placement and alpha-coverage checks using the already configured runtime.

Input RGBA is uint8 [0,255] or floating [0,1]. Coordinates are canvas corners;
do not add the contour pixel-center offset here. No downloads or package installs.
"""
import math
import logo_lab as lab
np, cv2 = lab.np, lab.cv2


def _rgba(image):
    a = np.asarray(image)
    if a.ndim != 3 or a.shape[2] != 4:
        raise ValueError('Expected HxWx4 RGBA.')
    result = a.astype(np.float32) / (255 if a.dtype == np.uint8 else 1)
    if not np.isfinite(result).all() or result.min() < 0 or result.max() > 1:
        raise ValueError('RGBA must be finite uint8 or float [0,1].')
    return result


def place_rgba(canvas, artwork, x, y):
    """Return source-over RGBA canvas with padded fractional placement.

    Premultiply before interpolation; clip only at final canvas bounds. OpenCV
    INTER_LINEAR has 1/32px coefficient precision; vector rasterization or higher
    resolution may be needed for a tighter output-space tolerance.
    """
    if not math.isfinite(x) or not math.isfinite(y):
        raise ValueError('Position must be finite.')
    dst, src = _rgba(canvas), _rgba(artwork)
    h, w = src.shape[:2]
    src = src.copy(); src[:, :, :3] *= src[:, :, 3:4]
    ix, iy = math.floor(x), math.floor(y)
    patch = cv2.warpAffine(src, np.float32([[1, 0, x-ix], [0, 1, y-iy]]),
                           (w+1, h+1), flags=cv2.INTER_LINEAR,
                           borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    dh, dw = dst.shape[:2]
    x0, y0, x1, y1 = max(ix, 0), max(iy, 0), min(ix+w+1, dw), min(iy+h+1, dh)
    if x1 > x0 and y1 > y0:
        p = patch[y0-iy:y1-iy, x0-ix:x1-ix]
        d = dst[y0:y1, x0:x1]
        alpha = p[:, :, 3:4] + d[:, :, 3:4]*(1-p[:, :, 3:4])
        rgb = p[:, :, :3] + d[:, :, :3]*d[:, :, 3:4]*(1-p[:, :, 3:4])
        dst[y0:y1, x0:x1] = np.concatenate((np.divide(rgb, alpha, out=np.zeros_like(rgb), where=alpha>0), alpha), axis=2)
    if np.asarray(canvas).dtype == np.uint8:
        return np.clip(np.rint(dst*255), 0, 255).astype(np.uint8)
    return dst


def coverage_difference(before, after, tolerance=0):
    """Compare UNCOMPRESSED alpha coverage, not encoded grayscale or IoU alone.

    Caller chooses and documents tolerance before checking; no built-in PASS.
    Keep raw data and inspect where differences occur.
    """
    def coverage(a):
        a = np.asarray(a)
        if a.ndim != 2:
            raise ValueError('Use a 2D alpha coverage array.')
        result = a.astype(np.float64)/(255 if a.dtype == np.uint8 else 1)
        if not np.isfinite(result).all() or result.min() < 0 or result.max() > 1:
            raise ValueError('Coverage must be uint8 or float [0,1].')
        return result
    a, b = coverage(before), coverage(after)
    if a.shape != b.shape or not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError('Same canvas shape and finite nonnegative tolerance required.')
    difference = np.abs(a-b)
    return {'changed_pixels': int(np.count_nonzero(difference > tolerance)),
            'max_alpha_error': float(difference.max()),
            'absolute_coverage_error': float(difference.sum()),
            'signed_area_change': float((b-a).sum()), 'tolerance': tolerance}

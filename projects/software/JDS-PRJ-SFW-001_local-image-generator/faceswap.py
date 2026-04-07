"""faceswap.py — Natural face swap between two images.

Takes a face from a source photo and blends it onto a target photo.
Uses insightface for detection/alignment + Poisson blending for seamless edges.

Usage:
  swap(source_img, target_img) → result with source face on target body
"""

import threading
import numpy as np
from PIL import Image

_analyser = None


def _bg(fn):
    threading.Thread(target=fn, daemon=True).start()


def _get_analyser():
    global _analyser
    if _analyser is None:
        from insightface.app import FaceAnalysis
        _analyser = FaceAnalysis(name="buffalo_l",
                                  providers=["CPUExecutionProvider"])
        _analyser.prepare(ctx_id=0, det_size=(640, 640))
    return _analyser


def _largest_face(faces):
    return max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) *
               (f.bbox[3] - f.bbox[1]))


def _get_face_landmarks(img_np):
    """Detect face and return 5-point landmarks + bbox."""
    app = _get_analyser()
    faces = app.get(img_np)
    if not faces:
        return None, None
    face = _largest_face(faces)
    return face.kps, face.bbox


def _align_face(src_kps, dst_kps):
    """Compute affine transform from source landmarks to dest landmarks."""
    import cv2
    src_pts = np.float32(src_kps[:3])
    dst_pts = np.float32(dst_kps[:3])
    return cv2.getAffineTransform(src_pts, dst_pts)


def _create_face_mask(shape, bbox, kps):
    """Create a soft oval mask around the face for blending."""
    import cv2
    h, w = shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)

    x1, y1, x2, y2 = [int(v) for v in bbox]
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    rw = int((x2 - x1) * 0.55)
    rh = int((y2 - y1) * 0.65)

    cv2.ellipse(mask, (cx, cy), (rw, rh), 0, 0, 360, 255, -1)
    mask = cv2.GaussianBlur(mask, (51, 51), 20)
    return mask


def swap(source, target, status=None, done=None, error=None):
    """Swap face from source image onto target image. Natural blending."""
    def _run():
        try:
            import cv2

            if status: status("Detecting faces...")
            src_np = np.array(source.convert("RGB"))
            tgt_np = np.array(target.convert("RGB"))

            src_kps, src_bbox = _get_face_landmarks(src_np)
            tgt_kps, tgt_bbox = _get_face_landmarks(tgt_np)

            if src_kps is None:
                if error: error("No face found in source image.")
                return
            if tgt_kps is None:
                if error: error("No face found in target image.")
                return

            if status: status("Aligning face...")

            # Compute transform to map source face onto target
            M = _align_face(src_kps, tgt_kps)
            h, w = tgt_np.shape[:2]

            # Warp source image to align with target face
            warped = cv2.warpAffine(src_np, M, (w, h),
                                     borderMode=cv2.BORDER_REFLECT_101)

            # Create blending mask around target face
            mask = _create_face_mask(tgt_np.shape, tgt_bbox, tgt_kps)

            if status: status("Blending...")

            # Try Poisson blending (seamless clone) for natural edges
            try:
                x1, y1, x2, y2 = [int(v) for v in tgt_bbox]
                center = ((x1 + x2) // 2, (y1 + y2) // 2)

                # Poisson needs a binary mask
                mask_bin = (mask > 128).astype(np.uint8) * 255

                result = cv2.seamlessClone(
                    warped, tgt_np, mask_bin,
                    center, cv2.NORMAL_CLONE)
            except Exception:
                # Fallback: alpha blending
                mask_3 = np.stack([mask / 255.0] * 3, axis=-1)
                result = (warped * mask_3 + tgt_np * (1 - mask_3)).astype(np.uint8)

            # Colour correction: match source face to target skin tone
            result = _colour_correct(result, tgt_np, mask)

            if status: status("Face swap complete.")
            if done: done(Image.fromarray(result))

        except ImportError:
            if error:
                error("Missing packages.\n\n"
                      "Run: pip install insightface opencv-python onnxruntime")
        except Exception as e:
            if error: error(str(e))
    _bg(_run)


def _colour_correct(result, target, mask):
    """Match the swapped face colour to the target skin tone."""
    import cv2

    mask_bool = mask > 128

    for ch in range(3):
        src_vals = result[:, :, ch][mask_bool].astype(np.float32)
        tgt_vals = target[:, :, ch][mask_bool].astype(np.float32)

        if len(src_vals) == 0:
            continue

        src_mean, src_std = src_vals.mean(), max(src_vals.std(), 1)
        tgt_mean, tgt_std = tgt_vals.mean(), max(tgt_vals.std(), 1)

        corrected = (result[:, :, ch].astype(np.float32) - src_mean)
        corrected = corrected * (tgt_std / src_std) + tgt_mean
        result[:, :, ch] = np.clip(corrected, 0, 255).astype(np.uint8)

    # Blend correction only within the mask
    mask_f = (mask / 255.0)[:, :, np.newaxis]
    blended = result * mask_f + target * (1 - mask_f)
    return blended.astype(np.uint8)


def multi_swap(source, target, status=None, done=None, error=None):
    """Swap ALL faces in target with the source face."""
    def _run():
        try:
            import cv2
            if status: status("Detecting all faces...")

            src_np = np.array(source.convert("RGB"))
            tgt_np = np.array(target.convert("RGB"))

            app = _get_analyser()
            src_faces = app.get(src_np)
            tgt_faces = app.get(tgt_np)

            if not src_faces:
                if error: error("No face in source."); return
            if not tgt_faces:
                if error: error("No faces in target."); return

            src_face = _largest_face(src_faces)
            result = tgt_np.copy()

            for i, tgt_face in enumerate(tgt_faces):
                if status: status(f"Swapping face {i+1}/{len(tgt_faces)}...")

                M = _align_face(src_face.kps, tgt_face.kps)
                h, w = result.shape[:2]
                warped = cv2.warpAffine(src_np, M, (w, h),
                                         borderMode=cv2.BORDER_REFLECT_101)
                mask = _create_face_mask(result.shape, tgt_face.bbox, tgt_face.kps)

                try:
                    x1, y1, x2, y2 = [int(v) for v in tgt_face.bbox]
                    center = ((x1 + x2) // 2, (y1 + y2) // 2)
                    mask_bin = (mask > 128).astype(np.uint8) * 255
                    result = cv2.seamlessClone(warped, result, mask_bin,
                                               center, cv2.NORMAL_CLONE)
                except Exception:
                    mask_3 = np.stack([mask / 255.0] * 3, axis=-1)
                    result = (warped * mask_3 + result * (1 - mask_3)).astype(np.uint8)

                result = _colour_correct(result, tgt_np, mask)

            if status: status(f"Swapped {len(tgt_faces)} face(s).")
            if done: done(Image.fromarray(result))

        except Exception as e:
            if error: error(str(e))
    _bg(_run)

#!/usr/bin/env python3
"""Extract transparent character sprites from the two character-sheet uploads.

The sheets are AI-generated reference boards: figures sit on a smooth grey
gradient (white / "REN" version) or on plain white (hijab / "AMIRA" version).
This script keys the background out with a per-row background model plus a
flood fill from the crop borders, then trims and exports production sprites.

Usage:  python3 tools/extract_sprites.py
"""
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
SITE = ROOT / "site"
OUT = SITE / "assets" / "characters"

WHITE_SHEET = RAW / "gpt-image-2.5-sunburst_a_BUAT_MENJADI_TAMPILA.png"
CREAM_SHEET = RAW / "gpt-image-2.5-sunburst_a_Buat_karakter_sheet_.png"


def flood_from_border(candidate: np.ndarray) -> np.ndarray:
    """Connected region of `candidate` reachable from the crop border."""
    filled = np.zeros_like(candidate)
    filled[0, :] = candidate[0, :]
    filled[-1, :] = candidate[-1, :]
    filled[:, 0] = candidate[:, 0]
    filled[:, -1] = candidate[:, -1]
    while True:
        grown = filled.copy()
        grown[1:, :] |= filled[:-1, :]
        grown[:-1, :] |= filled[1:, :]
        grown[:, 1:] |= filled[:, :-1]
        grown[:, :-1] |= filled[:, 1:]
        grown &= candidate
        if np.array_equal(grown, filled):
            return filled
        filled = grown


def fit_backdrop(img: np.ndarray) -> np.ndarray:
    """Fit the smooth studio backdrop as a 2D quadratic surface per channel.

    AI-sheet backdrops are soft gradients, so a per-row median is not accurate
    enough: bright corners leak through as halos. We first flag the obvious
    subject pixels and then least-squares fit a quadratic field to the rest,
    refining the mask once with the fitted field.
    """
    h, w, _ = img.shape
    yy, xx = np.mgrid[0:h, 0:w]
    yn, xn = yy / max(h - 1, 1) * 2 - 1, xx / max(w - 1, 1) * 2 - 1
    basis = np.stack([np.ones_like(xn), xn, yn, xn * xn, xn * yn, yn * yn], -1)
    fy = img.astype(np.float32)

    border = np.zeros((h, w), bool)
    border[:2, :] = border[-2:, :] = border[:, :2] = border[:, -2:] = True
    sample = border.copy()
    bg = np.repeat(fy[border].mean(axis=0)[None, :], h * w, 0).reshape(h, w, 3)

    for _ in range(3):
        dist = np.abs(fy - bg).max(axis=2)
        sample = dist < 14
        if sample.sum() < 500:
            sample = border
        A = basis[sample]
        coef, *_ = np.linalg.lstsq(A, fy[sample], rcond=None)
        bg = (basis.reshape(-1, 6) @ coef).reshape(h, w, 3)
    return bg


def key_flat(img: np.ndarray, lo: float = 9, hi: float = 20) -> np.ndarray:
    """Key out a plain paper-white backdrop (the cream / hijab sheet)."""
    fy = img.astype(np.float32)
    border = np.concatenate([fy[:4].reshape(-1, 3), fy[-4:].reshape(-1, 3),
                             fy[:, :4].reshape(-1, 3), fy[:, -4:].reshape(-1, 3)])
    bg = np.median(border, axis=0)

    dist = np.abs(fy - bg[None, None, :]).max(axis=2)
    sat = fy.max(axis=2) - fy.min(axis=2)
    score = np.maximum(dist, np.clip(sat - 6.0, 0, None))
    alpha = np.clip((score - lo) / (hi - lo), 0.0, 1.0)

    from scipy import ndimage
    # Close pinholes inside the garment (near-backdrop cream folds).
    solid = ndimage.binary_closing(alpha > 0.35, np.ones((7, 7)))
    alpha = np.where(solid & (alpha > 0.05), np.maximum(alpha, 0.65), alpha)

    filled = flood_from_border(alpha < 0.06)
    alpha = np.where(filled, 0.0, alpha)

    a3 = alpha[:, :, None]
    safe = np.maximum(a3, 0.10)
    rgb = np.clip((fy - bg[None, None, :] * (1.0 - a3)) / safe, 0, 255)
    rgb = np.where(a3 < 0.97, rgb, fy)
    return np.dstack([rgb, alpha * 255.0])


def keep_seed_component(rgba: np.ndarray, min_frac: float = 0.02) -> np.ndarray:
    """Keep components connected to the figure whose feet are near the bottom."""
    from scipy import ndimage

    alpha = rgba[:, :, 3]
    mask = alpha > 26
    labels, n = ndimage.label(mask)
    if n == 0:
        return rgba
    h, w = mask.shape
    # Seed = strongest alpha in the bottom third, centre half of the crop.
    band = np.zeros_like(mask)
    band[int(h * 0.55):, int(w * 0.15):int(w * 0.85)] = True
    cand = labels[band & mask]
    if not len(cand):
        return rgba
    vals, counts = np.unique(cand, return_counts=True)
    keep = {int(vals[counts.argmax()])}
    # Also keep any component that is a decent chunk of the figure (straps).
    sizes = ndimage.sum(mask, labels, range(1, n + 1))
    big = sizes.max()
    for i, sz in enumerate(sizes, start=1):
        if sz >= big * min_frac:
            keep.add(i)
    sel = ndimage.binary_dilation(np.isin(labels, list(keep)), iterations=2)
    out = rgba.copy()
    out[:, :, 3] = np.where(sel, alpha, 0.0)
    return out


def key_out(img: np.ndarray, lo: float = 15, hi: float = 46) -> np.ndarray:
    """Return an RGBA array with the smooth backdrop keyed out."""
    fy = img.astype(np.float32)
    bg = fit_backdrop(img)
    dist = np.abs(fy - bg).max(axis=2)

    # Bright surfaces against a bright backdrop still differ in *hue*, so add a
    # chroma term: the backdrop is near-neutral, the outfits are warm/cool.
    sat_img = fy.max(axis=2) - fy.min(axis=2)
    sat_bg = bg.max(axis=2) - bg.min(axis=2)
    chroma_gain = np.clip(sat_img - sat_bg - 5.0, 0, None)

    score = np.maximum(dist, chroma_gain)
    alpha = np.clip((score - lo) / (hi - lo), 0.0, 1.0)

    # Contact shadow: low-saturation darkening hugging the floor. Fade it out.
    h = alpha.shape[0]
    floor = np.clip((np.arange(h) - h * 0.80) / (h * 0.20), 0.0, 1.0)[:, None]
    shadowish = np.clip((bg.mean(axis=2) - fy.mean(axis=2) - 3.0) / 26.0, 0.0, 1.0) \
        * (1.0 - np.clip(sat_img / 12.0, 0.0, 1.0))
    alpha = alpha * (1.0 - 0.9 * floor * shadowish)

    filled = flood_from_border(alpha < 0.10)
    alpha = np.where(filled, 0.0, alpha)

    # Un-premultiply the backdrop from soft edge pixels so the fringe keeps the
    # character's colour instead of glowing grey.
    a3 = alpha[:, :, None]
    safe = np.maximum(a3, 0.10)
    unpremult = (fy - bg * (1.0 - a3)) / safe
    rgb = np.where(a3 < 0.97, np.clip(unpremult, 0, 255), fy)

    alpha = keep_main_components(alpha * 255.0)
    return np.dstack([rgb, alpha])


def keep_main_components(alpha: np.ndarray, min_frac: float = 0.05) -> np.ndarray:
    """Drop disconnected specks (sheet labels, headers, palette chips)."""
    from scipy import ndimage

    mask = alpha > 20
    labels, n = ndimage.label(mask)
    if n <= 1:
        return alpha
    sizes = ndimage.sum(mask, labels, range(1, n + 1))
    biggest = sizes.max()
    keep = {i + 1 for i, s in enumerate(sizes) if s >= biggest * min_frac}
    keep_mask = np.isin(labels, list(keep))
    halo = ndimage.binary_dilation(keep_mask, iterations=3)
    return np.where(halo, alpha, 0.0)


def trim_to_content(rgba: np.ndarray, pad: int = 6) -> np.ndarray:
    a = rgba[:, :, 3] > 12
    rows = np.where(a.any(axis=1))[0]
    cols = np.where(a.any(axis=0))[0]
    y0, y1 = max(rows[0] - pad, 0), min(rows[-1] + pad + 1, rgba.shape[0])
    x0, x1 = max(cols[0] - pad, 0), min(cols[-1] + pad + 1, rgba.shape[1])
    return rgba[y0:y1, x0:x1]


def save(rgba: np.ndarray, name: str, max_w: int = 0) -> None:
    img = Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8), "RGBA")
    if max_w and img.width > max_w:
        h = round(img.height * max_w / img.width)
        img = img.resize((max_w, h), Image.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    img.save(OUT / f"{name}.webp", quality=88, method=6)
    print(f"  {name}.webp  {img.width}x{img.height}")


def main() -> None:
    white = np.asarray(Image.open(WHITE_SHEET).convert("RGB"))
    cream = np.asarray(Image.open(CREAM_SHEET).convert("RGB"))

    OUT.mkdir(parents=True, exist_ok=True)

    # (sheet, crop box, tol_soft, tol_hard, output name, scale)
    FIGURES = [
        # (name, sheet, crop box, keyer)
        ("ren_front", white, (8, 38, 252, 792), "grad"),
        ("ren_back", white, (256, 38, 464, 792), "grad"),
        ("ren_side", white, (470, 38, 618, 792), "grad"),
        ("amira_front", cream, (2, 36, 252, 780), "flat"),
        ("amira_back", cream, (250, 36, 456, 780), "flat"),
        ("amira_side", cream, (458, 36, 640, 780), "flat"),
    ]
    print("figures:")
    for name, sheet, box, kind in FIGURES:
        crop = sheet[box[1]:box[3], box[0]:box[2]]
        rgba = key_out(crop) if kind == "grad" else keep_seed_component(key_flat(crop))
        save(trim_to_content(rgba), name)

    # Expression heads. Cell edges were measured from the sheet grids; the
    # white sheet's last cell is clipped by the panel, so it only has four.
    cells = {
        "ren": (white, "grad", 610, 752, [801, 931, 1076, 1219, 1366], 4),
        "amira": (cream, "flat", 596, 746, [800, 922, 1046, 1171, 1296, 1421], 5),
    }
    expr_by_char = {
        "ren": ["neutral", "smile", "serious", "surprised"],
        "amira": ["neutral", "smile", "serious", "surprised", "annoyed"],
    }
    print("faces:")
    for who, (sheet, kind, y0, y1, xs, count) in cells.items():
        for i in range(count):
            expr = expr_by_char[who][i]
            crop = sheet[y0:y1, xs[i] + 4:xs[i + 1] - 4]
            rgba = key_out(crop, lo=12, hi=40) if kind == "grad" else key_flat(crop)
            save(trim_to_content(rgba, pad=3), f"{who}_face_{expr}")

    # Head-detail portraits for the reaction / speech cards.
    print("portraits:")
    portraits = [
        ("ren_portrait", white, "grad", (796, 42, 1100, 336)),
        ("amira_portrait", cream, "flat", (792, 34, 1104, 340)),
    ]
    for name, sheet, kind, box in portraits:
        crop = sheet[box[1]:box[3], box[0]:box[2]]
        rgba = key_out(crop) if kind == "grad" else key_flat(crop)
        save(trim_to_content(rgba), name)

    # Logos / emblems from the sheets (silver for REN, gold for AMIRA).
    print("emblems:")
    emblems = [
        ("ren_emblem", white, "grad", (588, 884, 708, 972), 12),
        ("amira_emblem", cream, "flat", (566, 862, 745, 1000), 12),
    ]
    for name, sheet, kind, box, lo in emblems:
        crop = sheet[box[1]:box[3], box[0]:box[2]]
        rgba = key_out(crop, lo=lo, hi=lo + 28) if kind == "grad" else key_flat(crop, lo=6, hi=16)
        rgba[:, :, 3] = keep_main_components(rgba[:, :, 3], min_frac=0.06)
        save(trim_to_content(rgba), name)


def export_sheet_refs() -> None:
    """Small JPEG-free WebP copies of the two reference sheets for the viewer."""
    print("sheets:")
    refs = [("sheet_ren", WHITE_SHEET), ("sheet_amira", CREAM_SHEET)]
    out = SITE / "assets" / "sheets"
    out.mkdir(parents=True, exist_ok=True)
    for name, path in refs:
        img = Image.open(path).convert("RGB")
        img.thumbnail((1100, 1100), Image.LANCZOS)
        img.save(out / f"{name}.webp", quality=78, method=6)
        print(f"  {name}.webp  {img.width}x{img.height}")


if __name__ == "__main__":
    main()
    export_sheet_refs()

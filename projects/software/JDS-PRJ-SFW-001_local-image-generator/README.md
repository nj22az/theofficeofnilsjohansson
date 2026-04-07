# JDS Image Studio — Local Image Generator

| Field | Value |
|-------|-------|
| **Document No.** | JDS-PRJ-SFW-001 |
| **Revision** | B |
| **Date** | 2026-04-07 |
| **Status** | CURRENT |
| **Author** | N. Johansson |

---

## What Is This?

A fully local, unrestricted image generation desktop app that runs on Apple Silicon using Stable Diffusion. No cloud, no internet required after model download, no content filters. Your machine, your rules.

Double-click to launch. Close the window to shut down. Nothing stays running.

## Key Features

- **Double-click launch** — `setup.command` (one-time), then `JDS Image Studio.command` to run
- **Model Manager** — Browse, download, and switch models from inside the app
- **Optimised for realistic humans** — Recommended models curated for photorealistic faces and skin
- **Text-to-Image** — Generate images from text prompts
- **Image-to-Image** — Transform existing photos with strength control
- **No safety filters** — Full unrestricted generation (safety checker disabled)
- **Photo negative preset** — One-click negative prompt for clean realistic photos
- **Quick size presets** — 512x512, 512x768, 768x512, 768x768
- **Flat iOS-style GUI** — Clean, modern interface built with CustomTkinter
- **Apple Silicon native** — Runs on MPS (Metal Performance Shaders) backend
- **DPM++ 2M Karras scheduler** — Fast, high-quality sampling
- **Seed control** — Reproduce and copy seeds
- **Clean shutdown** — Close window to unload model and free all memory

## System Requirements

| Requirement | Minimum |
|-------------|---------|
| macOS | 12.0+ (Monterey) |
| Chip | Apple M1 / M1 Pro / M2+ |
| RAM | 16 GB |
| Python | 3.10+ |
| Disk | ~5 GB per model |

## Quick Start

### First time (one-time setup)

1. Double-click **`setup.command`** in Finder
2. Wait for dependencies to install (~2-5 min)

### Every time after

1. Double-click **`JDS Image Studio.command`** in Finder
2. The Model Manager opens automatically on first launch
3. Click **Download & Load** on "Realistic Vision v5.1" (recommended)
4. Enter a prompt and hit **Generate**

### Alternative (terminal)

```bash
cd projects/software/JDS-PRJ-SFW-001_local-image-generator/
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

## Recommended Models for Realistic Humans

| Model | Size | Best For |
|-------|------|----------|
| **Realistic Vision v5.1** | ~5 GB | Photorealistic humans, faces, skin (recommended) |
| Dreamlike Photoreal 2.0 | ~4 GB | Photorealistic with artistic flair |
| Stable Diffusion 2.1 | ~5 GB | General purpose baseline |
| Stable Diffusion 1.5 | ~4 GB | Lighter, faster, huge LoRA ecosystem |

All models are downloaded via the in-app Model Manager and cached at `~/.jds-image-studio/models/`.

## How It Works

```
Double-click → App launches → Model loads into MPS (Metal)
    → Enter prompt → Generate → Image preview → Save
Close window → Model unloaded → Memory freed → Process exits
```

No server. No background processes. Everything runs inside the app process.

## Project Structure

```
JDS-PRJ-SFW-001_local-image-generator/
    app.py                      # Main application
    requirements.txt            # Python dependencies
    setup.command               # One-time installer (double-click)
    JDS Image Studio.command    # App launcher (double-click)
    README.md                   # This file (project card)
    CHANGELOG.md                # All revisions tracked here
```

## Configuration

Settings persist at `~/.jds-image-studio/config.json`:
- Selected model
- Downloaded model list
- Default image dimensions, steps, guidance scale
- Output directory

Models cached at `~/.jds-image-studio/models/` (survives app updates).

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| B | 2026-04-07 | N. Johansson | Model Manager, double-click launch, realistic human models, DPM++ scheduler, negative presets, size presets, copy seed, clean shutdown |
| A | 2026-04-07 | N. Johansson | Initial release — txt2img, img2img, flat iOS GUI, MPS backend |

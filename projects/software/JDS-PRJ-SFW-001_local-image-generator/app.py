#!/usr/bin/env python3
"""
JDS-PRJ-SFW-001 — Local Image Generator
A flat, iOS-style local image generation app using Stable Diffusion.
Runs entirely on-device via Hugging Face Diffusers with Apple MPS backend.

Rev B — Model download manager, recommended realistic-human models, clean shutdown.
Author: N. Johansson
"""

import os
import sys
import json
import signal
import threading
import datetime
import gc
from pathlib import Path
from PIL import Image, ImageTk

import customtkinter as ctk

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
APP_NAME = "JDS Image Studio"
APP_VERSION = "2.0.0"
CONFIG_DIR = Path.home() / ".jds-image-studio"
CONFIG_FILE = CONFIG_DIR / "config.json"
MODELS_DIR = CONFIG_DIR / "models"
DEFAULT_OUTPUT_DIR = Path.home() / "Pictures" / "JDS-Image-Studio"

# Recommended models — curated for realistic humans and photos on M1 Pro 16GB
RECOMMENDED_MODELS = [
    {
        "id": "SG161222/Realistic_Vision_V5.1_noVAE",
        "name": "Realistic Vision v5.1",
        "desc": "Best for photorealistic humans and faces. Top community model.",
        "size": "~5 GB",
        "default": True,
    },
    {
        "id": "dreamlike-art/dreamlike-photoreal-2.0",
        "name": "Dreamlike Photoreal 2.0",
        "desc": "Photorealistic style with artistic flair. Great skin tones.",
        "size": "~4 GB",
        "default": False,
    },
    {
        "id": "stabilityai/stable-diffusion-2-1",
        "name": "Stable Diffusion 2.1",
        "desc": "Official Stability AI model. Good general purpose baseline.",
        "size": "~5 GB",
        "default": False,
    },
    {
        "id": "runwayml/stable-diffusion-v1-5",
        "name": "Stable Diffusion 1.5",
        "desc": "Lighter, faster. Huge community support and LoRA ecosystem.",
        "size": "~4 GB",
        "default": False,
    },
]

# Pre-built negative prompt for realistic human photography
NEGATIVE_PRESET_PHOTO = (
    "cartoon, anime, drawing, painting, illustration, sketch, 3d render, "
    "cgi, doll, plastic, deformed, ugly, blurry, bad anatomy, bad hands, "
    "extra fingers, missing fingers, extra limbs, disfigured, out of frame, "
    "watermark, text, logo, signature, low quality, jpeg artifacts"
)

# iOS-style colour palette (flat, muted)
COLORS = {
    "bg": "#F2F2F7",
    "surface": "#FFFFFF",
    "text": "#1C1C1E",
    "text_secondary": "#8E8E93",
    "accent": "#007AFF",
    "accent_hover": "#0056CC",
    "destructive": "#FF3B30",
    "success": "#34C759",
    "warning": "#FF9500",
    "separator": "#E5E5EA",
    "fill": "#E5E5EA",
    "fill_light": "#F2F2F7",
}


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def load_config():
    defaults = {
        "model_id": "",
        "output_dir": str(DEFAULT_OUTPUT_DIR),
        "default_width": 512,
        "default_height": 512,
        "default_steps": 30,
        "default_guidance": 7.0,
        "downloaded_models": [],
    }
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                saved = json.load(f)
            defaults.update(saved)
        except Exception:
            pass
    return defaults


def save_config(config):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


# ---------------------------------------------------------------------------
# Pipeline engine
# ---------------------------------------------------------------------------

_pipeline = None
_pipeline_lock = threading.Lock()
_current_model_id = None


def get_device():
    import torch
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def unload_pipeline():
    """Free the current pipeline and reclaim memory."""
    global _pipeline, _current_model_id
    with _pipeline_lock:
        if _pipeline is not None:
            del _pipeline
            _pipeline = None
            _current_model_id = None
            gc.collect()
            try:
                import torch
                if hasattr(torch, "mps") and hasattr(torch.mps, "empty_cache"):
                    torch.mps.empty_cache()
                elif torch.cuda.is_available():
                    torch.cuda.empty_cache()
            except Exception:
                pass


def download_model(model_id, on_status=None, on_progress=None,
                   on_done=None, on_error=None):
    """Download a model from HuggingFace Hub (background thread)."""

    def _download():
        try:
            if on_status:
                on_status(f"Downloading {model_id}...")

            from huggingface_hub import snapshot_download

            local_path = snapshot_download(
                model_id,
                cache_dir=str(MODELS_DIR),
                resume_download=True,
            )

            if on_status:
                on_status(f"Download complete: {model_id}")
            if on_done:
                on_done(model_id, local_path)

        except Exception as e:
            if on_error:
                on_error(str(e))

    t = threading.Thread(target=_download, daemon=True)
    t.start()


def load_pipeline(model_id, on_status=None, on_done=None, on_error=None):
    """Load a Stable Diffusion pipeline (background thread)."""

    def _load():
        global _pipeline, _current_model_id
        try:
            # Unload previous model first
            unload_pipeline()

            if on_status:
                on_status("Loading model — please wait...")

            import torch
            from diffusers import (
                StableDiffusionPipeline,
                DPMSolverMultistepScheduler,
            )

            device = get_device()
            dtype = torch.float16 if device == "cuda" else torch.float32

            if on_status:
                on_status(f"Device: {device.upper()} | Loading...")

            is_local = os.path.isdir(model_id)

            with _pipeline_lock:
                pipe = StableDiffusionPipeline.from_pretrained(
                    model_id,
                    torch_dtype=dtype,
                    cache_dir=str(MODELS_DIR) if not is_local else None,
                    local_files_only=is_local,
                )

                # Disable safety checker — unrestricted
                pipe.safety_checker = None
                pipe.feature_extractor = None

                # Use DPM++ 2M Karras scheduler — fast, high quality
                pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                    pipe.scheduler.config,
                    use_karras_sigmas=True,
                    algorithm_type="dpmsolver++",
                )

                pipe = pipe.to(device)
                pipe.enable_attention_slicing()

                _pipeline = pipe
                _current_model_id = model_id

            if on_status:
                on_status(f"Ready — {device.upper()}")
            if on_done:
                on_done()

        except Exception as e:
            if on_error:
                on_error(str(e))

    t = threading.Thread(target=_load, daemon=True)
    t.start()


def generate_image(prompt, negative_prompt="", width=512, height=512,
                   steps=30, guidance=7.0, seed=-1,
                   on_status=None, on_done=None, on_error=None):
    def _generate():
        try:
            import torch
            if _pipeline is None:
                if on_error:
                    on_error("No model loaded. Load or download a model first.")
                return

            if on_status:
                on_status("Generating...")

            actual_seed = seed
            if seed < 0:
                actual_seed = torch.randint(0, 2**32 - 1, (1,)).item()
            generator = torch.Generator(device="cpu").manual_seed(actual_seed)

            with _pipeline_lock:
                result = _pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt or None,
                    width=width,
                    height=height,
                    num_inference_steps=steps,
                    guidance_scale=guidance,
                    generator=generator,
                )

            if on_done:
                on_done(result.images[0], actual_seed)

        except Exception as e:
            if on_error:
                on_error(str(e))

    t = threading.Thread(target=_generate, daemon=True)
    t.start()


def generate_img2img(prompt, init_image, strength=0.75, negative_prompt="",
                     steps=30, guidance=7.0, seed=-1,
                     on_status=None, on_done=None, on_error=None):
    def _generate():
        try:
            import torch
            from diffusers import StableDiffusionImg2ImgPipeline

            if _pipeline is None:
                if on_error:
                    on_error("No model loaded.")
                return

            if on_status:
                on_status("Running img2img...")

            img2img_pipe = StableDiffusionImg2ImgPipeline(
                vae=_pipeline.vae,
                text_encoder=_pipeline.text_encoder,
                tokenizer=_pipeline.tokenizer,
                unet=_pipeline.unet,
                scheduler=_pipeline.scheduler,
                safety_checker=None,
                feature_extractor=None,
            )
            img2img_pipe = img2img_pipe.to(_pipeline.device)
            img2img_pipe.enable_attention_slicing()

            actual_seed = seed
            if seed < 0:
                actual_seed = torch.randint(0, 2**32 - 1, (1,)).item()
            generator = torch.Generator(device="cpu").manual_seed(actual_seed)

            init = init_image.convert("RGB")
            init = init.resize((init.width // 8 * 8, init.height // 8 * 8))

            result = img2img_pipe(
                prompt=prompt,
                image=init,
                strength=strength,
                negative_prompt=negative_prompt or None,
                num_inference_steps=steps,
                guidance_scale=guidance,
                generator=generator,
            )

            if on_done:
                on_done(result.images[0], actual_seed)

        except Exception as e:
            if on_error:
                on_error(str(e))

    t = threading.Thread(target=_generate, daemon=True)
    t.start()


# ---------------------------------------------------------------------------
# Model Download Window
# ---------------------------------------------------------------------------

class ModelManagerWindow(ctk.CTkToplevel):
    """Modal window for browsing, downloading, and selecting models."""

    def __init__(self, master, config, on_model_selected=None):
        super().__init__(master)
        self.config = config
        self.on_model_selected = on_model_selected

        self.title("Model Manager")
        self.geometry("620x560")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg"])
        self.grab_set()

        # Title
        ctk.CTkLabel(
            self, text="Model Manager",
            font=("SF Pro Display", 20, "bold"),
            text_color=COLORS["text"],
        ).pack(padx=24, pady=(20, 4), anchor="w")

        ctk.CTkLabel(
            self, text="Download and manage Stable Diffusion models.",
            font=("SF Pro Text", 13),
            text_color=COLORS["text_secondary"],
        ).pack(padx=24, pady=(0, 12), anchor="w")

        # Scrollable list of models
        scroll = ctk.CTkScrollableFrame(self, fg_color=COLORS["bg"])
        scroll.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        for model in RECOMMENDED_MODELS:
            self._build_model_card(scroll, model)

        # Separator
        ctk.CTkFrame(self, height=1, fg_color=COLORS["separator"]).pack(
            fill="x", padx=16, pady=(4, 8))

        # Custom model entry
        custom_frame = ctk.CTkFrame(self, fg_color="transparent")
        custom_frame.pack(fill="x", padx=24, pady=(0, 4))

        ctk.CTkLabel(
            custom_frame, text="Custom HuggingFace model ID:",
            font=("SF Pro Text", 12),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w")

        entry_row = ctk.CTkFrame(custom_frame, fg_color="transparent")
        entry_row.pack(fill="x", pady=(4, 0))

        self.custom_entry = ctk.CTkEntry(
            entry_row, corner_radius=10, font=("SF Pro Text", 12),
            fg_color=COLORS["fill"], border_width=0,
            placeholder_text="e.g. username/model-name",
        )
        self.custom_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        ctk.CTkButton(
            entry_row, text="Download", width=100, corner_radius=10, height=32,
            font=("SF Pro Text", 12, "bold"),
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            command=self._download_custom,
        ).pack(side="right")

        # Status
        self.dl_status = ctk.CTkLabel(
            self, text="", font=("SF Pro Text", 11),
            text_color=COLORS["text_secondary"],
        )
        self.dl_status.pack(padx=24, pady=(4, 16), anchor="w")

    def _build_model_card(self, parent, model):
        card = ctk.CTkFrame(parent, corner_radius=12, fg_color=COLORS["surface"])
        card.pack(fill="x", pady=4)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=12)
        inner.grid_columnconfigure(0, weight=1)

        # Name + badge
        name_row = ctk.CTkFrame(inner, fg_color="transparent")
        name_row.pack(fill="x")

        name = model["name"]
        if model.get("default"):
            name += "  (Recommended)"

        ctk.CTkLabel(
            name_row, text=name,
            font=("SF Pro Text", 14, "bold"),
            text_color=COLORS["text"],
        ).pack(side="left")

        ctk.CTkLabel(
            name_row, text=model["size"],
            font=("SF Pro Text", 11),
            text_color=COLORS["text_secondary"],
        ).pack(side="right")

        # Description
        ctk.CTkLabel(
            inner, text=model["desc"],
            font=("SF Pro Text", 12),
            text_color=COLORS["text_secondary"],
            wraplength=500, justify="left",
        ).pack(anchor="w", pady=(2, 6))

        # Buttons
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.pack(fill="x")

        ctk.CTkButton(
            btn_row, text="Download & Load", width=140,
            corner_radius=10, height=32,
            font=("SF Pro Text", 12, "bold"),
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            command=lambda m=model: self._download_and_load(m),
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            btn_row, text="Load (if downloaded)", width=150,
            corner_radius=10, height=32,
            font=("SF Pro Text", 12),
            fg_color=COLORS["fill"], text_color=COLORS["text"],
            hover_color=COLORS["separator"],
            command=lambda m=model: self._load_existing(m),
        ).pack(side="left")

    def _set_dl_status(self, msg):
        self.after(0, lambda: self.dl_status.configure(text=msg))

    def _download_and_load(self, model):
        self._set_dl_status(f"Downloading {model['name']}... (this may take a while)")

        def on_done(model_id, local_path):
            # Track downloaded models
            downloaded = self.config.get("downloaded_models", [])
            if model_id not in downloaded:
                downloaded.append(model_id)
                self.config["downloaded_models"] = downloaded
            self.config["model_id"] = model_id
            save_config(self.config)
            self._set_dl_status(f"Downloaded. Now loading {model['name']}...")

            if self.on_model_selected:
                self.after(0, lambda: self.on_model_selected(model_id))

        def on_error(e):
            self._set_dl_status(f"Error: {e}")

        download_model(
            model["id"],
            on_status=self._set_dl_status,
            on_done=on_done,
            on_error=on_error,
        )

    def _load_existing(self, model):
        self.config["model_id"] = model["id"]
        save_config(self.config)
        if self.on_model_selected:
            self.on_model_selected(model["id"])
        self.destroy()

    def _download_custom(self):
        model_id = self.custom_entry.get().strip()
        if not model_id:
            self._set_dl_status("Enter a model ID first.")
            return

        custom = {"id": model_id, "name": model_id}
        self._download_and_load(custom)


# ---------------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------------

class ImageStudioApp(ctk.CTk):
    """Main window — flat iOS-style design."""

    def __init__(self):
        super().__init__()

        self.config = load_config()
        self.current_image = None
        self.input_image = None
        self.last_seed = None
        self._is_generating = False

        # Window
        self.title(APP_NAME)
        self.geometry("1100x800")
        self.minsize(960, 680)
        self.configure(fg_color=COLORS["bg"])

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Clean shutdown
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main_area()

        # Auto-show model manager if no model configured
        if not self.config.get("model_id"):
            self.after(500, self._open_model_manager)

    # -----------------------------------------------------------------------
    # Sidebar
    # -----------------------------------------------------------------------
    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, width=330, corner_radius=0,
                          fg_color=COLORS["surface"])
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)

        # --- Header ---
        ctk.CTkLabel(
            sb, text=APP_NAME,
            font=("SF Pro Display", 22, "bold"),
            text_color=COLORS["text"],
        ).pack(padx=20, pady=(20, 0), anchor="w")

        ctk.CTkLabel(
            sb, text=f"v{APP_VERSION} — 100% Local",
            font=("SF Pro Text", 11),
            text_color=COLORS["text_secondary"],
        ).pack(padx=20, pady=(0, 8), anchor="w")

        ctk.CTkFrame(sb, height=1, fg_color=COLORS["separator"]).pack(
            fill="x", padx=20, pady=(0, 10))

        # --- Scrollable controls area ---
        controls = ctk.CTkScrollableFrame(sb, fg_color=COLORS["surface"])
        controls.pack(fill="both", expand=True, padx=0, pady=0)

        px = 20  # standard horizontal padding inside controls

        # Mode selector
        self.mode_var = ctk.StringVar(value="txt2img")
        ctk.CTkSegmentedButton(
            controls, values=["txt2img", "img2img"],
            variable=self.mode_var,
            command=self._on_mode_change,
            font=("SF Pro Text", 13),
        ).pack(fill="x", padx=px, pady=(4, 10))

        # Prompt
        ctk.CTkLabel(
            controls, text="Prompt",
            font=("SF Pro Text", 13, "bold"),
            text_color=COLORS["text"],
        ).pack(padx=px, pady=(0, 4), anchor="w")

        self.prompt_box = ctk.CTkTextbox(
            controls, height=80, corner_radius=10,
            font=("SF Pro Text", 13),
            fg_color=COLORS["fill"], text_color=COLORS["text"],
            border_width=0,
        )
        self.prompt_box.pack(fill="x", padx=px, pady=(0, 8))

        # Negative prompt
        neg_row = ctk.CTkFrame(controls, fg_color="transparent")
        neg_row.pack(fill="x", padx=px)

        ctk.CTkLabel(
            neg_row, text="Negative Prompt",
            font=("SF Pro Text", 13, "bold"),
            text_color=COLORS["text"],
        ).pack(side="left")

        ctk.CTkButton(
            neg_row, text="Photo preset", width=90,
            corner_radius=8, height=24,
            font=("SF Pro Text", 10),
            fg_color=COLORS["fill"], text_color=COLORS["accent"],
            hover_color=COLORS["separator"],
            command=self._fill_negative_preset,
        ).pack(side="right")

        self.neg_prompt_box = ctk.CTkTextbox(
            controls, height=50, corner_radius=10,
            font=("SF Pro Text", 13),
            fg_color=COLORS["fill"], text_color=COLORS["text"],
            border_width=0,
        )
        self.neg_prompt_box.pack(fill="x", padx=px, pady=(4, 8))

        # img2img controls (hidden by default)
        self.img2img_frame = ctk.CTkFrame(controls, fg_color="transparent")

        ctk.CTkButton(
            self.img2img_frame, text="Load Input Image",
            corner_radius=10, height=36,
            font=("SF Pro Text", 13),
            fg_color=COLORS["fill"], text_color=COLORS["text"],
            hover_color=COLORS["separator"],
            command=self._load_input_image,
        ).pack(fill="x", pady=(0, 4))

        self.strength_label = ctk.CTkLabel(
            self.img2img_frame, text="Strength: 0.75",
            font=("SF Pro Text", 12),
            text_color=COLORS["text_secondary"],
        )
        self.strength_label.pack(anchor="w")

        self.strength_slider = ctk.CTkSlider(
            self.img2img_frame, from_=0.1, to=1.0, number_of_steps=18,
            command=self._on_strength_change,
        )
        self.strength_slider.set(0.75)
        self.strength_slider.pack(fill="x", pady=(0, 8))

        # --- Settings grid ---
        ctk.CTkFrame(controls, height=1, fg_color=COLORS["separator"]).pack(
            fill="x", padx=px, pady=(4, 8))

        ctk.CTkLabel(
            controls, text="Settings",
            font=("SF Pro Text", 13, "bold"),
            text_color=COLORS["text"],
        ).pack(padx=px, pady=(0, 4), anchor="w")

        grid = ctk.CTkFrame(controls, fg_color="transparent")
        grid.pack(fill="x", padx=px, pady=(0, 8))
        grid.grid_columnconfigure((0, 1), weight=1)

        self.width_entry = self._add_setting_row(grid, 0, "Width",
                                                  str(self.config["default_width"]))
        self.height_entry = self._add_setting_row(grid, 1, "Height",
                                                   str(self.config["default_height"]))
        self.steps_entry = self._add_setting_row(grid, 2, "Steps",
                                                  str(self.config["default_steps"]))
        self.guidance_entry = self._add_setting_row(grid, 3, "CFG Scale",
                                                     str(self.config["default_guidance"]))
        self.seed_entry = self._add_setting_row(grid, 4, "Seed", "-1")

        # --- Quick size presets ---
        size_row = ctk.CTkFrame(controls, fg_color="transparent")
        size_row.pack(fill="x", padx=px, pady=(0, 8))

        for label, w, h in [("512x512", 512, 512), ("512x768", 512, 768),
                             ("768x512", 768, 512), ("768x768", 768, 768)]:
            ctk.CTkButton(
                size_row, text=label, width=68,
                corner_radius=8, height=26,
                font=("SF Pro Text", 10),
                fg_color=COLORS["fill"], text_color=COLORS["text"],
                hover_color=COLORS["separator"],
                command=lambda ww=w, hh=h: self._set_size(ww, hh),
            ).pack(side="left", padx=(0, 4))

        # --- Model section ---
        ctk.CTkFrame(controls, height=1, fg_color=COLORS["separator"]).pack(
            fill="x", padx=px, pady=(4, 8))

        model_header = ctk.CTkFrame(controls, fg_color="transparent")
        model_header.pack(fill="x", padx=px)

        ctk.CTkLabel(
            model_header, text="Model",
            font=("SF Pro Text", 13, "bold"),
            text_color=COLORS["text"],
        ).pack(side="left")

        ctk.CTkButton(
            model_header, text="Model Manager", width=110,
            corner_radius=8, height=26,
            font=("SF Pro Text", 11),
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            command=self._open_model_manager,
        ).pack(side="right")

        self.model_display = ctk.CTkLabel(
            controls,
            text=self.config.get("model_id", "No model selected") or "No model selected",
            font=("SF Pro Text", 11),
            text_color=COLORS["text_secondary"],
            wraplength=280,
        )
        self.model_display.pack(padx=px, pady=(4, 4), anchor="w")

        # Load model button
        self.load_model_btn = ctk.CTkButton(
            controls, text="Load Model",
            corner_radius=10, height=36,
            font=("SF Pro Text", 13, "bold"),
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            command=self._load_model,
        )
        self.load_model_btn.pack(fill="x", padx=px, pady=(4, 12))

        # --- Bottom of sidebar (not in scroll) ---
        # Generate button
        self.generate_btn = ctk.CTkButton(
            sb, text="Generate",
            corner_radius=12, height=48,
            font=("SF Pro Display", 17, "bold"),
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            command=self._on_generate,
        )
        self.generate_btn.pack(fill="x", padx=20, pady=(0, 8), side="bottom")

        # Status
        self.status_label = ctk.CTkLabel(
            sb, text="No model loaded — open Model Manager to get started",
            font=("SF Pro Text", 11),
            text_color=COLORS["text_secondary"],
            wraplength=280,
        )
        self.status_label.pack(padx=20, pady=(0, 8), side="bottom", anchor="w")

    def _add_setting_row(self, parent, row, label, default):
        ctk.CTkLabel(
            parent, text=label,
            font=("SF Pro Text", 12),
            text_color=COLORS["text_secondary"],
        ).grid(row=row, column=0, sticky="w", pady=2)

        entry = ctk.CTkEntry(
            parent, width=80, corner_radius=8,
            font=("SF Pro Text", 12),
            fg_color=COLORS["fill"], border_width=0,
        )
        entry.insert(0, default)
        entry.grid(row=row, column=1, sticky="e", pady=2)
        return entry

    # -----------------------------------------------------------------------
    # Main area
    # -----------------------------------------------------------------------
    def _build_main_area(self):
        main = ctk.CTkFrame(self, corner_radius=0, fg_color=COLORS["bg"])
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=1)

        # Image card
        self.image_card = ctk.CTkFrame(
            main, corner_radius=16, fg_color=COLORS["surface"])
        self.image_card.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.image_card.grid_rowconfigure(0, weight=1)
        self.image_card.grid_columnconfigure(0, weight=1)

        self.image_label = ctk.CTkLabel(
            self.image_card, text="",
            font=("SF Pro Text", 15),
            text_color=COLORS["text_secondary"],
        )
        self.image_label.configure(
            text="Open Model Manager to download a model,\nthen enter a prompt and hit Generate.")
        self.image_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Toolbar
        toolbar = ctk.CTkFrame(main, height=48, corner_radius=0,
                               fg_color=COLORS["bg"])
        toolbar.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))

        ctk.CTkButton(
            toolbar, text="Save Image", width=120,
            corner_radius=10, height=36,
            font=("SF Pro Text", 13),
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            command=self._save_image,
        ).pack(side="left")

        ctk.CTkButton(
            toolbar, text="Copy Seed", width=100,
            corner_radius=10, height=36,
            font=("SF Pro Text", 13),
            fg_color=COLORS["fill"], text_color=COLORS["text"],
            hover_color=COLORS["separator"],
            command=self._copy_seed,
        ).pack(side="left", padx=(8, 0))

        self.seed_display = ctk.CTkLabel(
            toolbar, text="",
            font=("SF Pro Text", 12),
            text_color=COLORS["text_secondary"],
        )
        self.seed_display.pack(side="right")

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------
    def _set_status(self, msg):
        self.after(0, lambda: self.status_label.configure(text=msg))

    def _on_mode_change(self, mode):
        if mode == "img2img":
            self.img2img_frame.pack(fill="x", padx=20, pady=(0, 8),
                                    after=self.neg_prompt_box)
        else:
            self.img2img_frame.pack_forget()

    def _on_strength_change(self, val):
        self.strength_label.configure(text=f"Strength: {val:.2f}")

    def _set_size(self, w, h):
        self.width_entry.delete(0, "end")
        self.width_entry.insert(0, str(w))
        self.height_entry.delete(0, "end")
        self.height_entry.insert(0, str(h))

    def _fill_negative_preset(self):
        self.neg_prompt_box.delete("1.0", "end")
        self.neg_prompt_box.insert("1.0", NEGATIVE_PRESET_PHOTO)

    def _open_model_manager(self):
        ModelManagerWindow(self, self.config, on_model_selected=self._on_model_selected)

    def _on_model_selected(self, model_id):
        self.model_display.configure(text=model_id)
        self.config["model_id"] = model_id
        save_config(self.config)
        self._load_model()

    def _load_input_image(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(
            title="Select input image",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp")])
        if path:
            self.input_image = Image.open(path)
            self._display_image(self.input_image)
            self._set_status(f"Input image: {os.path.basename(path)}")

    def _load_model(self):
        model_id = self.config.get("model_id", "").strip()
        if not model_id:
            self._set_status("No model selected — open Model Manager.")
            return

        self.generate_btn.configure(state="disabled")
        self.load_model_btn.configure(state="disabled")

        def on_done():
            self.after(0, lambda: self.generate_btn.configure(state="normal"))
            self.after(0, lambda: self.load_model_btn.configure(state="normal"))

        def on_error(e):
            self._set_status(f"Load error: {e}")
            self.after(0, lambda: self.generate_btn.configure(state="normal"))
            self.after(0, lambda: self.load_model_btn.configure(state="normal"))

        load_pipeline(model_id, on_status=self._set_status,
                      on_done=on_done, on_error=on_error)

    def _on_generate(self):
        if self._is_generating:
            return

        prompt = self.prompt_box.get("1.0", "end").strip()
        if not prompt:
            self._set_status("Enter a prompt first.")
            return

        neg = self.neg_prompt_box.get("1.0", "end").strip()

        try:
            w = int(self.width_entry.get())
            h = int(self.height_entry.get())
            steps = int(self.steps_entry.get())
            guidance = float(self.guidance_entry.get())
            seed = int(self.seed_entry.get())
        except ValueError:
            self._set_status("Check your settings — invalid number.")
            return

        w = (w // 8) * 8
        h = (h // 8) * 8

        self._is_generating = True
        self.generate_btn.configure(state="disabled", text="Generating...")

        def on_done(image, actual_seed):
            self._is_generating = False
            self.current_image = image
            self.last_seed = actual_seed
            self.after(0, lambda: self._display_image(image))
            self.after(0, lambda: self.seed_display.configure(
                text=f"Seed: {actual_seed}"))
            self._set_status("Done.")
            self.after(0, lambda: self.generate_btn.configure(
                state="normal", text="Generate"))

        def on_error(e):
            self._is_generating = False
            self._set_status(f"Error: {e}")
            self.after(0, lambda: self.generate_btn.configure(
                state="normal", text="Generate"))

        mode = self.mode_var.get()
        if mode == "img2img" and self.input_image is not None:
            generate_img2img(
                prompt=prompt, init_image=self.input_image,
                strength=self.strength_slider.get(), negative_prompt=neg,
                steps=steps, guidance=guidance, seed=seed,
                on_status=self._set_status, on_done=on_done, on_error=on_error)
        else:
            generate_image(
                prompt=prompt, negative_prompt=neg,
                width=w, height=h, steps=steps, guidance=guidance, seed=seed,
                on_status=self._set_status, on_done=on_done, on_error=on_error)

    def _display_image(self, pil_image):
        card_w = max(self.image_card.winfo_width() - 40, 400)
        card_h = max(self.image_card.winfo_height() - 40, 400)

        img = pil_image.copy()
        img.thumbnail((card_w, card_h), Image.LANCZOS)

        self._tk_image = ImageTk.PhotoImage(img)
        self.image_label.configure(image=self._tk_image, text="")

    def _save_image(self):
        if self.current_image is None:
            self._set_status("No image to save.")
            return

        from tkinter import filedialog
        output_dir = self.config.get("output_dir", str(DEFAULT_OUTPUT_DIR))
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = filedialog.asksaveasfilename(
            title="Save Image",
            initialdir=output_dir,
            initialfile=f"jds_image_{ts}.png",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All", "*.*")])
        if path:
            self.current_image.save(path)
            self._set_status(f"Saved: {os.path.basename(path)}")

    def _copy_seed(self):
        if self.last_seed is not None:
            self.clipboard_clear()
            self.clipboard_append(str(self.last_seed))
            self._set_status(f"Seed {self.last_seed} copied to clipboard.")

    def _on_close(self):
        """Clean shutdown — unload model, free memory, exit."""
        self._set_status("Shutting down...")
        unload_pipeline()
        self.destroy()
        sys.exit(0)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, lambda *_: sys.exit(0))

    app = ImageStudioApp()
    app.mainloop()


if __name__ == "__main__":
    main()

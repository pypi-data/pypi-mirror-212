import torch
from diffusers import StableDiffusionLatentUpscalePipeline

from sdkit import Context
from sdkit.utils import log


def load_model(context: Context, **kwargs):
    dtype = torch.float16 if context.half_precision else torch.float32
    upscaler = StableDiffusionLatentUpscalePipeline.from_pretrained(
        "stabilityai/sd-x2-latent-upscaler", torch_dtype=dtype
    )
    if context.vram_usage_level == "low":
        upscaler.enable_sequential_cpu_offload()
    else:
        upscaler.to(context.device)

    if context.vram_usage_level != "high":
        upscaler.enable_attention_slicing(1)

    return upscaler


def unload_model(context: Context, **kwargs):
    pass

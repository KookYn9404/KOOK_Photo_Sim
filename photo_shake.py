import random
import torch
import torch.nn.functional as F


def _to_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default


class PhotoShakeNode:
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return random.random()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "enable_shake": ("BOOLEAN", {"default": True}),
                "shake_strength": ("FLOAT", {"default": 20.0, "min": 0.01, "max": 100.0, "step": 0.01}),
                "enable_color_noise": ("BOOLEAN", {"default": True}),
                "color_noise_strength": ("FLOAT", {"default": 50.0, "min": 0.01, "max": 100.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply"
    CATEGORY = "KOOK/Photo"

    def apply(self, image, enable_shake, shake_strength, enable_color_noise, color_noise_strength):
        x = image.clone()

        if enable_shake:
            x = self._shake_image(x, _to_float(shake_strength, 1.0))

        if enable_color_noise:
            x = self._add_color_noise(x, _to_float(color_noise_strength, 1.0))

        return (x.clamp(0.0, 1.0),)

    def _shake_image(self, image, strength):
        b, h, w, c = image.shape
        device = image.device
        dtype = image.dtype

        strength = max(0.01, min(100.0, strength))
        # Convert strength into a small pixel offset range and a few blend taps.
        max_shift = max(0.15, strength * 0.03)
        taps = int(min(9, max(2, 2 + strength // 20)))

        base = image.permute(0, 3, 1, 2)
        acc = torch.zeros_like(base)

        for i in range(taps):
            if taps == 1:
                dx = dy = 0.0
            else:
                t = i / (taps - 1)
                # Random handheld wobble without rotation.
                dx = (t - 0.5) * 2.0 * max_shift + (torch.rand((b,), device=device, dtype=dtype) - 0.5) * max_shift * 0.35
                dy = (0.5 - t) * 2.0 * max_shift + (torch.rand((b,), device=device, dtype=dtype) - 0.5) * max_shift * 0.35

            theta = torch.zeros((b, 2, 3), device=device, dtype=dtype)
            theta[:, 0, 0] = 1.0
            theta[:, 1, 1] = 1.0
            theta[:, 0, 2] = dx * 2.0 / max(w, 1)
            theta[:, 1, 2] = dy * 2.0 / max(h, 1)

            grid = F.affine_grid(theta, size=(b, c, h, w), align_corners=False)
            acc += F.grid_sample(
                base,
                grid,
                mode="bilinear",
                padding_mode="reflection",
                align_corners=False,
            )

        return (acc / float(taps)).permute(0, 2, 3, 1)

    def _add_color_noise(self, image, strength):
        strength = max(0.01, min(100.0, strength))
        amp = strength / 100.0 * 0.03
        rgb_noise = torch.randn_like(image) * amp
        return image + rgb_noise


NODE_CLASS_MAPPINGS = {
    "PhotoShakeNode": PhotoShakeNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PhotoShakeNode": "KOOK_Photo_Sim",
}

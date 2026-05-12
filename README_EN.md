# KOOK_Photo_Sim

[中文](./README.md)

A ComfyUI custom node for simulating a handheld photo look.

## Features

- slight shake blur to mimic handheld shooting
- optional color noise for a more realistic photo feel
- keeps a simple `IMAGE -> IMAGE` workflow
- depends only on ComfyUI and `torch`
- optimized for cloud platforms such as RunningHub and ZhiSuan Yunfei

## Parameters

- `enable_shake`
- `shake_strength`: range `0.01 ~ 100`
- `enable_color_noise`
- `color_noise_strength`: range `0.01 ~ 100`

## Default Values

- `enable_shake`: `true`
- `shake_strength`: `20`
- `enable_color_noise`: `true`
- `color_noise_strength`: `50`

## Notes

- This version removes frontend localization and custom web extensions for better cloud compatibility.
- The node logic is pure Python image tensor processing.
- The shake effect intentionally softens fine details to mimic handheld photo blur.
- The effect naturally softens some detail, which is expected for simulated shake.

## Install

Place the whole folder in:

`custom_nodes/KOOK_Photo_Sim`

# KOOK_Photo_Sim

[English](./README_EN.md)

适用于 ComfyUI 的真实拍照模拟节点，用来给图片加入轻微手持拍摄感。

## 功能

- 轻微抖动模糊，模拟手持拍照时的细微拖影
- 可选彩色噪点，模拟真实照片颗粒感
- 保持简单的 `IMAGE -> IMAGE` 工作流
- 仅依赖 ComfyUI 与 `torch`

## 参数

- `enable_shake`
- `shake_strength`：范围 `0.01 ~ 100`
- `enable_color_noise`
- `color_noise_strength`：范围 `0.01 ~ 100`

## 默认值

- `enable_shake`: `true`
- `shake_strength`: `20`
- `enable_color_noise`: `true`
- `color_noise_strength`: `50`

## 说明

- 节点核心逻辑为纯 Python 图像张量处理，便于在不同平台部署。
- 抖动效果本质上会带来一定细节变软，这是模拟拍照抖动的正常结果。

## 安装

将整个文件夹放入：

`custom_nodes/KOOK_Photo_Sim`


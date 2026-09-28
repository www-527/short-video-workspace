# 真实 AI 链路洗车配音测试包 v1

状态：素材制作完成，等待用户上传测试  
用途：本机内部 Qwen3-ASR、视觉理解、广告作用标注、全量排序、字幕和双成片导出验收  
权利：`testOnly: true`、`publishable: false`

## 直接上传主包

主包目录：`clips/main`

请新建一个独立项目，严格按 `manifests/main-upload-order.json` 的顺序一次性上传以下 11 条：

1. `wc-main-07-interior.mp4`
2. `wc-main-01-hook.mp4`
3. `wc-main-10-offer.mp4`
4. `wc-main-04-foam.mp4`
5. `wc-main-02-problem.mp4`
6. `wc-main-11-cta.mp4`
7. `wc-main-06-wheel.mp4`
8. `wc-main-03-service.mp4`
9. `wc-main-09-transition.mp4`
10. `wc-main-05-rinse.mp4`
11. `wc-main-08-result.mp4`

主包总时长约 52.8 秒，覆盖全部九种广告作用。文件名只用于人工管理，程序和模型不应依赖文件名判断作用。

## 异常包必须分开测试

异常目录：`clips/edge`

不要把所有异常片一次上传。按 `manifests/edge-upload-order.json` 每个数组单独新建项目：

- 静音：`wc-edge-01-silent.mp4`
- 音画冲突：`wc-edge-02-av-conflict.mp4`
- 极弱音+噪声：`wc-edge-03-low-volume.mp4`
- 重复文件：`wc-edge-04-duplicate-a.mp4` 与 `wc-edge-04-duplicate-b.mp4` 一起上传
- 长口播：`wc-edge-05-long-speech.mp4`
- 损坏/不支持：`wc-edge-06-unsupported.mp4`

损坏文件故意不可解码，只用于验证上传阶段直接返回原始错误且不留下半批素材。

## 上传前检查

在 PowerShell 运行：

```powershell
& 'D:\短视频\素材\真实AI链路测试包_v1\scripts\validate-package.ps1'
```

必须看到 `status: passed`。验证会重新检查源文件和输出文件哈希、媒体合同、九类覆盖、乱序清单、重复文件一致性和损坏文件拒绝行为。

## 结果验收

上传 11 段主包后，设程序分配的真实素材 ID 集合为 `S`，必须满足：

- `finalClipOrder.length === 11`
- `new Set(finalClipOrder).size === 11`
- `new Set(finalClipOrder)` 与 `S` 完全相同
- 每段都有可读画面说明和九类之一的广告作用
- 结果总体符合“钩子/问题 → 服务/过程/细节 → 效果 → 优惠/到店引导”
- 时间线严格按 `finalClipOrder` 读取 11 段上传原片
- 字幕来自真实 ASR；无字幕和带字幕成片都能从头播放到尾

具体预期口播、关键词、来源、权利标记、媒体参数和 SHA-256 见 `manifests/assets.json`。

## 目录说明

- `clips/main`：直接用于主包上传的 11 条 MP4。
- `clips/edge`：必须分场景测试的异常文件。
- `manifests/assets.json`：18 条测试文件的数据合同。
- `probe`：17 条可解码媒体的完整 ffprobe JSON；损坏文件按预期无有效探测结果。
- `tts/wav`：IndexTTS2 原始输出，未覆盖。
- `sources/original`：本轮实际使用的 9 个 Pexels 原文件只读副本。
- `sources/license-evidence`：许可/条款复核记录、素材来源复核 PDF，以及 Coverr 排除证据。
- `reports`：覆盖盘点、QA 帧、测试状态和验证结果。
- `scripts`：TTS 生成、音视频构建、许可 PDF 生成和包校验脚本。

## 重要权利限制

内置声音的公开商业授权没有确认；部分视频含可识别人脸、车牌、车辆品牌或产品特征。所有产物只允许本机内部测试，不得上传到公开平台、用于广告投放或声称得到人物/品牌背书。

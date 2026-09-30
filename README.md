# Agent 制作工作空间

本工作区用于制作、配置、测试和维护 AI Agent 应用，并包含相关工程代码和演示。当前 Agent 是“Agent 应用工程师”，其角色定义位于 `AGENTS.md`。

完成后的 Agent 默认提供角色与提示词设计、工具集成、工作流编排、应用实现、代码审查、测试、评测与维护支持；只有用户明确要求时才处理媒体文件、渲染或外部发布。

## 文件说明

- `AGENTS.md`：当前 Agent 的角色定位、工程质量标准、Agent 应用设计规则和维护规则。
- `README.md`：Agent 制作工作区说明与所有实质性项目变更的记录。

## 使用原则

在本工作区中，先定义 Agent 的角色、职责、边界、输入输出和维护规则，再根据需要增加提示词、工具配置、测试样例或发布文件。当前 Agent 默认处理 Agent 应用的角色定义、Prompt、工具、权限、状态、工作流、接口、评测、代码和测试，并以清晰、正确、可维护和可验证为质量基准。

每次实质性修改 Agent 定义、配置、测试或发布文件后，都应维护下方日志。

## 修改日志
- 2026-09-30：补充 GitHub 完整恢复备份与跨电脑恢复脚本。原因：原仓库忽略素材、成片、数据库、模型和配置，克隆代码无法恢复当前任务。涉及：`scripts/restore-backup.mjs`、本 README；完整数据另存于私有仓库 `backup-20260930` Release 的加密分卷，解压密码单独留存，不提交到 Git。验证方式：SQLite 一致性快照、原片和成片大小核对、配置密钥解密验证、独立目录恢复演练、7-Zip 完整性检查及远端附件状态/大小核对；实际结果以 Release 说明为准。影响：不改变现有业务逻辑与原始数据；恢复脚本仅在新解压的离线副本运行，可重定位数据库、JSON 和模型配置中的工作区路径。依赖环境须在新电脑重新安装。
- 2026-09-28：按用户最终选择，将整个外层工作区整理为独立 GitHub 私有仓库，保留各内层项目的实际文件及原有本地 Git 历史。涉及：根目录 `.gitignore`、`README.md`。上传代码、文档、脚本及未被忽略的图片等资源；排除密钥、数据库、依赖、模型、缓存、QA 产物、视频音频、压缩包与可执行程序，原文件均留在本地，因此本仓库不是完整媒体备份。验证方式：文件清单与敏感信息候选检查、远程提交核对；未运行业务测试。影响：新增外层版本管理，不修改业务逻辑。
- 2026-09-28：整理现有项目并同步至原 GitHub 仓库；在 `washcut-agent-demo/.gitignore` 排除 `.runtime-logs/`，防止本地浏览器会话、登录数据和诊断缓存被提交。涉及：该忽略文件及工作区、应用 README。验证：检查待提交文件、密钥候选和文件大小，确认忽略规则并核对推送后的远程提交；本次未修改业务逻辑，未运行应用测试。影响：本地运行数据保留，上传范围为应用仓库。
- 2026-09-15：精简公网测试页桌面与手机共用文案：缩短主标题和三步流程，删除重复小标题、技术说明与页脚，上传提醒压缩为一句，保留格式/大小/数量限制、动态进度及错误恢复指引。原因：用户反馈两种布局文字过多。涉及 `washcut-agent-demo/src/client/PublicTestApp.tsx` 与两个 `README.md`。验证方式：TypeScript 检查、Vite 构建通过；生产静态页面在 1440/390/320px 下无横向溢出或页面异常，模拟会话验证选择及删除素材、按钮启用正常。影响：仅调整展示文案，不修改错误原文、上传和制作逻辑；dist 已更新，未启动公网服务或真实制作。
- 2026-09-15：优化公网测试页排版：桌面采用左侧流程说明、右侧操作区，手机保留单列；收紧标题和顶部留白，统一浅色背景、圆角及按钮，放大进度辅助文字，完成区下载按钮独立成行；修复素材列表的宽泛 li 选择器误作用到上传步骤条。原因：原单列页面主次不清、辅助文字偏小且步骤条受样式污染。涉及 `washcut-agent-demo/src/client/public-test.css` 与两个 `README.md`。验证方式：TypeScript 构建、Vite 生产构建、上传状态 5 项测试通过；生产静态页在 Chromium 模拟会话下检查 1440/768/390/320px、选择删除、上传错误、四阶段排列、完成双下载入口、新建测试及登录窄屏，无横向溢出或页面异常。影响：仅 CSS 排版调整；已生成 dist，未启动公网 Tunnel，未执行真实上传或 AI 制作；重新开启公网测试后提供新版页面。
- 2026-09-07：为公网测试本机管理面板增加“打开素材文件夹”按钮，由回环管理服务打开固定的 `washcut-agent-demo/data/auto-video/originals` 原片根目录；接口不接受前端路径且要求本机管理确认请求头，失败保留系统原始错误。原因：管理员需要从监控页直接查看按项目和素材分层保存的用户上传原片。涉及 `washcut-agent-demo/src/client/PublicAdminApp.tsx`、`public-admin.css`、`src/server/test-admin.ts`、`test-admin.test.ts` 与两个 `README.md`。验证方式：集成测试覆盖拒绝与成功路径，运行完整测试、构建、差异检查并检查桌面/390px 布局。影响：重启公网测试后生效；不向公网开放文件系统，不修改任务、素材、Key、检查点或成片。
- 2026-09-07：将公网测试本机管理面板从深绿终端风格改为高可读浅色工作台：移除网格背景、荧光绿、全局等宽字体和英文控制室文案，放大正文、状态、步骤、任务信息及控件，仅让技术 ID 和中转站原文使用等宽字体；同时补齐中文任务/步骤状态与常见连接成功说明。原因：原界面 9–11px 小字和刻意的“黑客控制台”配色影响快速阅读。涉及 `washcut-agent-demo/src/client/PublicAdminApp.tsx`、`public-admin.css` 和两个 `README.md`。验证方式：生产构建、管理面板测试、完整测试及差异检查；真实页面在 1920×1080、390×844、320×800 下无横向溢出或控制台问题。影响：只调整本机管理员界面，不改变公网暴露范围、任务、Key 操作、中转站记录或重试逻辑。
- 2026-09-07：修复公网测试本机管理面板持续出现 `HTTP 400 / invalid_identity`：管理代理调用主服务的用户身份改为符合既有 `user_` 前缀合同的 `user_admin_public_test`，测试同步校验租户、用户和管理员角色请求头。原因：初始身份值 `admin_public_test` 未通过主服务身份校验，导致管理面板每次自动刷新都失败。涉及 `washcut-agent-demo/src/server/test-admin.ts`、`test-admin.test.ts` 和两个 `README.md`。验证方式：运行管理面板定向测试、完整测试、生产构建与差异检查。影响：重启公网测试后管理面板恢复读取；公网权限、任务、素材、检查点、Key 和成片数据不变。
- 2026-09-07：为公网测试新增仅在本机显示的独立管理员数据看板：启动时额外监听 `127.0.0.1:8791` 并自动打开浏览器应用窗口，展示公网任务批量阶段、自动重试次数、原始错误和中转站完整输入/输出；提供 API Key 测试/切换，以及自动重试停止后的管理员人工断点重试，重试可把失败版本显式改绑到所选 Key。公网测试者侧移除重试能力，Cloudflare 继续只转发 `8790`，管理写操作同时要求回环地址、同源和本机确认请求头，浏览器只接收掩码 Key。原因：命令行流水不便于快速判断卡点，中转站故障修复后也需要管理员掌握密钥切换与恢复权。涉及 `washcut-agent-demo/.env.example`、`src/client/PublicAdminApp.tsx`、`public-admin.css`、`PublicTestApp.tsx`、`main.tsx`、`src/server/test-admin.ts`、`test-admin.test.ts`、`test-gateway.ts`、`test-gateway.test.ts`、`test-gateway-bootstrap.ts`、`index.ts`、共享合同、启动脚本和两个 `README.md`。验证方式：项目 `pnpm test` 107 项、`pnpm build`、PowerShell 语法检查均通过；隔离模拟 API 的浏览器实测覆盖桌面、390px、320px，无横向溢出或控制台警告/错误；未进行真实 Key 切换、模型调用或任务重试。影响：重新开启公网测试后生效；历史任务、检查点、原片、时间线和成片不变，管理员端口不会进入公网 Tunnel。
- 2026-09-04：优化公网测试页的视频上传等待反馈：将流程明确拆成“创建任务—上传传输—本机保存—启动制作”四阶段，展示已传/总数据量、已保存段数、等待时间、最近进度更新时间及 15 秒无新数据的慢网提示；补充手机锁屏/切网提醒和素材全部保存确认；启动请求未确认时保留原始错误，并把按钮改为“重新尝试启动制作”，复用已保存素材且成功后自动聚焦制作进度；同时将后端回读的 uploaded 纳入未启动状态，避免一次轮询后恢复入口消失。原因：原页面的 100% 只代表浏览器传输完成，用户无法分辨本机保存和启动等待，且“已保存 + Failed to fetch + 上传并开始制作”会让人误以为必须重新上传。涉及 src/client/PublicTestApp.tsx、public-test.css、public-upload-state.ts、public-upload-state.test.ts 与两个 README.md。验证方式：上传状态纯逻辑 5 项测试通过、pnpm test 106 项通过、pnpm build 通过、git diff --check 通过；隔离本机测试网关使用 3.2 MB 真实视频验证 100% 后本机保存等待、模拟首次启动失败、只重试启动和自动聚焦，1280px、390px、320px 页面均无横向溢出，浏览器控制台无错误或警告。影响：只改变公网测试页的状态表达和未启动任务恢复入口，不修改上传/任务合同、网关权限、AI 编排、素材、时间线或成片；已打开的测试页刷新后生效。
- 2026-09-03：修复洗车公网测试页在手机系统选择器一次只返回一个视频时无法累计多段素材的问题，并增加清晰的上传总进度：视频选择改为追加模式，手机可分多次添加、电脑仍可一次多选，重复文件会被忽略；实际传输期间显示当前第几段、总百分比、明显进度条以及已传输后等待本机保存/检测的状态。原因：原页面每次选择都会覆盖已有列表，且 Fetch 上传没有浏览器侧字节进度。涉及 `washcut-agent-demo/src/client/PublicTestApp.tsx`、`src/client/public-test.css` 与两个 `README.md`。验证方式：`pnpm test` 106 项通过、`pnpm build` 通过；隔离本机网关浏览器实测电脑一次选择 2 段、390px 手机尺寸分两次选择累计 2 段、真实 multipart 上传进度与保存等待状态正常，未启动真实 AI 任务。影响：不改变逐段上传、断点重试、权限、模型、时间线或成片；当前公网 Tunnel 不需要重启或更换网址，已打开页面刷新后生效。
- 2026-09-03：修复洗车公网测试页批量上传在 Cloudflare Quick Tunnel 上可能收到 524 后整段显示 HTML、且无法定位问题素材的体验：前端将选中的视频按单段依次上传，每段展示“等待上传 / 正在上传 / 已保存 / 上传失败”状态；失败卡片明确显示对应文件名、错误码和可展开的原始错误，524 提示可删除该未保存素材后稍后重试；素材列表补充每段可操作的“删除”按钮（已保存到本机的素材在公网页保持保护）。原因：原流程把全部素材与逐段媒体探测放在同一个公网请求中，17 段素材可超过中转站等待时间，且返回的 Cloudflare HTML 不能关联到具体文件。涉及 `washcut-agent-demo/src/client/PublicTestApp.tsx`、`src/client/public-test.css` 与两个 `README.md`。验证方式：`pnpm test` 106 项通过、`pnpm build` 通过。影响：公网任务仍逐段使用原始文件；失败文件不会被保存或进入后续编排，已保存的前序素材可继续上传剩余素材并启动制作；未重新发起真实公网上传，需重启公网测试网关和 Tunnel 后生效。
- 2026-09-02：洗车公网测试启动窗口新增本机监控流水：用匿名测试者短标识输出登录、新建、上传、开始、断点继续、下载与跨会话拒绝；任务开始后每 2.5 秒独立跟踪，只输出状态/进度/环节变化；按任务所属会话读取本机模型对话库，输出请求摘要、程序发送内容、模型回复或原始错误，命令行单段限 6,000 字符而完整记录仍留在 SQLite；启动脚本把隐藏网关和 Cloudflare 输出同时转发到当前窗口，`Ctrl+C` 仍会统一关闭；访问码、API Key、Cookie 和媒体 base64 不输出，授权/密钥形式会再次脱敏。原因：制作方需在本机命令行实时掌握外部测试人员操作、制作进度、模型往返与阻塞原因，不必对外开放管理界面。涉及 `washcut-agent-demo/src/server/test-gateway.ts`、`test-gateway-bootstrap.ts`、`test-gateway.test.ts`、`scripts/start-public-test.ps1` 和两个 `README.md`。验证方式：新增集成测试验证操作、进度、模型往返与密钥脱敏，并执行完整测试、生产构建、PowerShell 5.1 语法检查和差异检查。影响：监控仅本机可见，不向测试人员或 Cloudflare 额外公开，不改变制作并发、数据合同、素材或成片。
- 2026-09-02：洗车公网测试页新增本人任务的断点重试：`retry_waiting` 可立即重试，`needs_attention/cancelled` 走后端断点恢复并重置本轮预算，`failed` 走版本重试；测试网关继续按登录会话校验项目归属，跨会话返回 404，完成任务拒绝重试，页面防止重复点击并明确无需重新上传；同时修正窄屏宽度表达式，避免手机页面被压成竖排窄列。原因：后台已有检查点和恢复接口，但简化页面未开放安全入口，任一环节进入终止状态后测试人员无法继续。涉及 `washcut-agent-demo/src/server/test-gateway.ts`、`test-gateway.test.ts`、`src/client/PublicTestApp.tsx`、`public-test.css` 与两个 `README.md`。验证方式：集成测试覆盖状态路由映射、完成任务拒绝、跨会话隔离，完整测试、构建、桌面/手机页面操作检查和差异检查。影响：不开放管理、删除、模型密钥、日志、取消或关机能力；重试复用原片和已完成检查点，不改变历史任务、模型合同、API Key、时间线或成片格式。
- 2026-09-02：改善洗车公网测试启动交互：访问码和并发输入分别显示 `Step 1/2` 与 `Step 2/2`，第一步明确不是并发；交互输入过短访问码或越界并发时会原地重新询问，不再用红色 PowerShell 错误栈退出，显式命令行非法参数仍保持快速失败。原因：用户把 `2` 输入到了第一步访问码位置，旧提示未充分区分两个输入。涉及 `washcut-agent-demo/scripts/start-public-test.ps1` 与两个 `README.md`。验证方式：PowerShell 5.1 语法/ASCII、合法参数执行至端口保护、非法访问码快速失败及差异检查。影响：仅改进双击启动体验，不修改安全下限、并发范围、API Key、任务、素材或成片。
- 2026-09-02：洗车编排台公网测试启动器新增本机画面理解并发选择：双击开启后输入访问码及 `1–30` 路并发（回车默认 `1`），也可通过 `-VisualConcurrency` 指定；选择值经环境变量传给独立测试网关，由服务端校验后写入新任务快照，测试人员无法在公网页面调高。原因：本机管理前端的并发只随其自身创建任务发送，公网入口此前固定为 `1`，不能继承该页面状态。涉及 `washcut-agent-demo/.env.example`、`scripts/start-public-test.ps1`、`src/server/test-gateway-bootstrap.ts`、`test-gateway.ts`、`test-gateway.test.ts` 与两个 `README.md`。验证方式：集成测试覆盖并发透传与越界拒绝，PowerShell 5.1 语法/ASCII 检查、完整测试、构建和差异检查。影响：重新开启公网测试后仅新任务使用所选并发；API Key 继续使用 `tenant_demo` 当前启用连接，历史任务、素材、数据库、模型全局并发上限和成片不变。
- 2026-09-02：为洗车编排台公网测试新增根目录可双击的 `开启公网测试.cmd` 和 `关闭公网测试.cmd`；关闭脚本通过 `8790` 监听端口与进程命令行双重识别，只终止测试网关及对应 Cloudflare Quick Tunnel，保留 `8787` 主程序和全部任务文件，并补充访问码及命令行用法。原因：让临时公网测试可以明确、一键启停，同时防止关闭测试时误伤本机制作流程。涉及 `开启公网测试.cmd`、`关闭公网测试.cmd`、`washcut-agent-demo/scripts/stop-public-test.ps1` 与两个 `README.md`。验证方式：PowerShell 5.1 语法解析、ASCII 编码检查、`-WhatIf` 匹配当前测试进程、快捷文件内容和差异空白检查。影响：Quick Tunnel 仍不绑定 Cloudflare 账号且网址不固定；不修改登录隔离、模型调用、视频处理、数据库、素材或成片。
- 2026-09-02：为洗车编排台新增本机处理的外部免费测试链路：独立 `8790` 测试网关只开放访问码、任务、上传、进度和双成片下载，服务端注入隔离身份并拒绝管理 API；新增极简 `/test` 页面、公开/管理样式分包、Cloudflare Quick Tunnel 启动脚本与集成测试。原因：直接把现有 Vite 端口放入 Tunnel 会暴露浏览器端固定身份可调用的删除、模型密钥、日志和关机接口，隐藏按钮不能提供权限边界。涉及 `washcut-agent-demo/src/server/test-gateway.ts`、`test-gateway-bootstrap.ts`、`test-gateway.test.ts`、`src/client/PublicTestApp.tsx`、`public-test.css`、`AutoVideoEntry.tsx`、`main.tsx`、`scripts/start-public-test.ps1`、配置、包脚本及两个 `README.md`。验证方式：网关集成测试覆盖登录、白名单、身份、流式上传、状态、双下载和跨会话隔离；`pnpm build` 通过；Cloudflare 官方签名的 `cloudflared 2026.8.3` 建立真实 Quick Tunnel，公网测试页 200、未登录会话 401、关机接口 404；浏览器完成公网登录、桌面/390px 响应式和控制台检查。影响：视频与 AI 仍只在本机运行，不改变现有数据、模型、时间线或成片；Quick Tunnel 只用于测试，网址会变化且本机、网关和 Tunnel 必须保持在线。
- 2026-09-02：修复洗车编排台已完成版本的“已分析”数量错误显示为 `0 / N`：进度统计不再只依赖可能缺失或尚未同步的逐素材检查点；画面分析步骤已完成时以当前版本去重后的权威素材 ID 全量计数，运行中则合并已持久化素材理解结果与已完成检查点，并过滤非本版本素材。原因：旧界面仅统计 `assetCheckpoints.visualAnalysis=completed`，因此完整版本即使已有全部分析结果、步骤和成片，也可能因检查点摘要为空而显示 `0 / 17`。涉及 `washcut-agent-demo/src/shared/auto-video-progress.ts`、`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/server/auto-video.test.ts` 与两个 `README.md`。验证方式：新增完成阶段缺少检查点、运行中结果与检查点合并去重的回归测试；完整 `pnpm test`、`pnpm build`、`git diff --check` 及浏览器页面实测。影响：只修正前端进度数字的读取与展示，不修改分析结果、任务状态、模型调用、时间线、字幕、原片或成片。
- 2026-09-02：修复洗车编排台中断版本后重新编排时后台任务异常可能导致整个 API 退出的问题：Worker 现在在任务调度边界消费内部处理路径之外的 Promise rejection，保留原始 `code/message/retryable`，活动版本转为可诊断的 `needs_attention`，取消或终态版本不被覆盖；二次持久化错误也不会再次形成未处理拒绝。现场确认出错时前端 `5175` 存活、后端 `8787` 已退出，因而主页与模型对话窗口同时收到 Vite 代理的 `Internal Server Error`；恢复服务后 V1 仍为 `cancelled`，V2 从 12% 断点自动重启 Qwen 并完成至 100%，未删除或重建任何版本。原因：原 `void run().finally()` 缺少最外层 rejection 隔离，存储/恢复异常可能按 Node 策略结束 API。涉及 `washcut-agent-demo/src/server/auto-video-worker.ts`、`src/server/auto-video.test.ts` 与两个 `README.md`。验证方式：注入 `checkpoint_concurrent_update` 验证无 `unhandledRejection` 且原始错误落库；定向 51 项、完整 102 项测试和生产构建通过，现场 V2 十个步骤全部完成且 API/模型对话接口恢复 200。影响：只增强后台任务容错与诊断，不改原片、历史版本、正常模型协议、时间线、字幕或成片；故障前未留存 stderr，因此不把缺失的原始异常栈当作已取证结论。
- 2026-09-02：为洗车编排台 Qwen3-ASR 接入官方 `context` 行业热词能力：新版本默认快照升级为 `car-wash-ad-zh-v2`，由私有网关把 48 个洗车广告常见短词传入官方 `Qwen3ASRModel.transcribe(context=...)`，涵盖脚垫、门把手、中控台、出风口、龙卷风清洁枪、轮胎上蜡、洗车套餐、团购和到店等表达；旧 `car-wash-zh-v1` 保留空上下文以兼容历史恢复，未知配置明确失败且不允许浏览器传任意 Prompt。原因：原有 Speaches/Whisper 热词在 Qwen 迁移后只剩 Profile 名称，网关此前会丢弃它，真实素材已出现“脚垫”识别成“电脑”。涉及 `washcut-agent-demo/.env.example`、`qwen3-asr-gateway/app.py`、`test_app.py`、网关说明、`src/shared/auto-video-contracts.ts`、`src/server/qwen3-asr.ts`、`qwen3-asr.test.ts`、`transcription-registry.ts` 与两个 `README.md`。验证方式：Python 网关测试 8 项、TypeScript 定向测试 9 项、项目完整 `pnpm test` 101 项全部通过，`pnpm build`、Python 语法编译和差异检查通过。影响：仅新建的 v2 Qwen 转写使用热词，旧版本/v1 不变；运行中的旧网关需重启，新热词对真实识别率和可能的上下文混入尚待正/负音频 A/B 验证。
- 2026-09-02：完成洗车编排台模型短引用与 1–30 路并发优化：所有 AI 模型正文改用 `clip_001` 等批内短引用，由服务端以权威素材顺序建立稳定双向映射，严格校验返回的全集、唯一性、顺序及异常字符后再回填真实 `assetId`；结构修复保留具体错误并复用映射，Relay/Qwen/网络原始错误语义不被覆盖。画面理解选择器、请求 Schema、版本快照和 Worker 统一支持 1–30、默认 1，并新增进程级模型与画面全局上限；媒体检测、转写和渲染继续使用各自限流。原因：修复真实长 ID 可能被模型字符改写的问题，并消除原先前端 4、Schema 4、模型 20 等不一致并发上限。涉及 `washcut-agent-demo/.env.example`、`washcut-agent-demo/docs/模型短引用与1至30路并发优化_AI实施方案.md`、`src/shared/auto-video-contracts.ts`、`src/server/model-asset-reference.ts`、`src/server/auto-video-model-contracts.ts`、`src/server/auto-video-ai.ts`、`src/server/auto-video-worker.ts`、`src/server/index.ts`、`src/client/AutoVideoApp.tsx`、`src/server/auto-video.test.ts` 与两个 `README.md`。验证方式：项目 `pnpm test` 100 项通过、`pnpm build` 通过、定向差异检查无空白错误；应用内浏览器在 `127.0.0.1:5175` 验证默认 1、1–30 完整选项、选择 30 和无新增控制台问题，随后恢复为 1，未提交生成任务；30 路峰值和跨任务进程上限使用可控 Promise 自动化验证。影响：新模型协议为服务端私有 v2，内部数据库、真实 ID、时间线、字幕、原片及成片格式保持兼容；未配置全局环境变量时上限为 30，历史缺省版本仍按 1 路；本次未重新运行真实 Relay/Qwen 或持续压力测试。
- 2026-09-02：新增可直接交给后续 AI 执行的《模型短引用与 1–30 路画面理解并发优化：AI 实施方案》，将真实 `projectId/assetId` 退出模型正文、`clip_001` 映射、模型 v2 合同、全集校验、错误修复、1–30 并发、全局限流、取消恢复、禁止实现、自动化测试、浏览器验收和最终交付格式写成文件级执行清单；总实施计划中的同主题章节仅作为背景。原因：随机长 ID 容易被模型改写，且当前并发在多层分别受 4 和 20 限制，原总计划章节不足以作为独立 AI 交接入口。涉及 `washcut-agent-demo/docs/模型短引用与1至30路并发优化_AI实施方案.md`、`AI视频编排系统实施计划.md` 与两个 `README.md`。验证方式：对照当前模型协议、校验代码、前端选项、创建版本接口和 Worker 限流人工核对文档；本次仅新增实施文档，未修改业务代码，未运行测试或构建。影响：不改变当前程序、数据库、模型调用、并发行为、时间线或成片；后续 AI 应以独立文档为实施准则。
- 2026-09-01：修复洗车编排服务端口竞争与完成进度：只有实际成功监听 API 端口的进程才启动 Worker recovery，绑定失败进程记录原始错误、关闭 SQLite 并失败退出；双成片检查成功后显式完成渲染步骤，`completed` 生成统一为 100%，历史 91% 快照由专用非破坏迁移在下次启动时规范化。原因：避免重复后端并发恢复同一生成任务，并消除产物全部就绪但界面仍显示 91% 的不一致。涉及 `washcut-agent-demo/src/server/server-startup.ts`、`server-startup.test.ts`、`index.ts`、`auto-video-worker.ts`、`store.ts`、相关测试/文档及两个 `README.md`。验证方式：端口冲突和成功监听测试、活动/终态进度及保留历史快照字段的迁移测试；`pnpm test` 90 项通过，`pnpm build` 通过；V3 已恢复并核对 progress 100、十步完成、11 份转写和分析、11 段时间线及双成片状态。影响：只改变服务启动所有权和进度一致性；不修改用户原片、模型分析内容、时间线、字幕或成片文件；恢复前数据库证据备份保存在项目 `data` 目录。
- 2026-09-01：实施洗车编排台“口播优先的整批 MarketingRole 判断”：画面模型不再决定最终广告作用，同一版本全部 ASR 与客观画面证据齐备后执行一次整批角色判断，严格校验素材 ID 全集/唯一性、九类角色和非空理由，再以口播叙事为主、画面衔接为辅编排；补充受控修复、断点恢复、历史兼容、对话审计、自动化测试和真实主包回归报告。原因：解决提问、效果、优惠和到店口播被可见洗车动作误标为 `process/transition` 的真实偏差。涉及 `washcut-agent-demo/src/shared/auto-video-contracts.ts`、`src/server/auto-video-ai.ts`、`src/server/auto-video-worker.ts`、`src/server/auto-video.test.ts`、相关文档及两个 `README.md`。验证方式：`pnpm test` 87 项通过、`pnpm build` 通过；真实主包结果见项目回归报告。影响：每个新 AI 生成版本增加一次整批模型操作；V1 等历史数据不迁移，原片、字幕、时间线与渲染合同不变。
- 2026-09-01：为洗车编排台新增《口播优先的整批 MarketingRole 判断：AI 实施方案》，规定在同一版本全部 ASR 与画面分析完成后只调用一次整批角色模型，再以口播叙事为主进行全量排序；方案覆盖提示词、数据合同、素材集合校验、恢复、测试与主/异常包验收。原因：当前视觉阶段过早确定角色，使明确的 Hook、Result 和 CTA 口播被画面动作覆盖。涉及 `washcut-agent-demo/docs/口播优先整批MarketingRole判断_AI实施方案.md` 与两个 `README.md`。验证方式：对照当前程序工作流、九类角色合同和真实测试结果人工核对；本次未修改业务代码或运行数据。影响：仅新增待实施方案，不改变现有模型调用、排序、字幕、时间线或成片。
- 2026-09-01：完成洗车编排台真实主包与六类异常素材最终验收归档：主包真实 Qwen3-ASR、视觉理解、全量排序、字幕和双成片通过；静音、音画冲突、低音量、重复素材通过；长口播字幕语义分割与损坏媒体错误合同部分通过。新增项目外正式验收报告，并更新测试状态与 AI 交接文档。原因：用户已完成全部异常项目，需要以数据库、模型对话、字幕、成片和错误截图的实际证据收口。涉及 `washcut-agent-demo/docs/真实AI链路洗车配音测试素材制作_AI交接文档.md`、项目外测试包 `reports` 与两个 `README.md`。验证方式：核对 5 个异常生成版本、11 次模型对话、排序唯一性和字幕 JSON；FFmpeg 完整解码 10 个异常普通/字幕 MP4；核对损坏媒体原子拒绝截图。影响：仅更新报告和文档，不改变业务代码、SQLite、原片、模型、时间线或成片；测试素材仍为内部不可发布。
- 2026-09-01：优化洗车编排台中文烧录字幕分段：连续语句的尾段不足 3 字时，允许小幅放宽 1800ms 目标并回并孤字，或从上一条移动字词形成更均衡的两条字幕；真实长停顿和句末边界仍保持，字级与片段级时间戳路径均覆盖。原因：真实测试成片把“身表面灰尘和污渍”切出单独“渍”。涉及 `washcut-agent-demo/src/server/auto-video-captions.ts`、`auto-video.test.ts` 与两个 `README.md`。验证方式：孤字回并、14+1 字符重平衡、长停顿保护、片段时间戳回归测试，完整 `pnpm test` 与 `pnpm build`。影响：只影响后续新生成或重新生成的字幕产物与带字幕成片；现有成片、无字幕视频、ASR 原始结果、原片、时间线和编排顺序不变。
- 2026-09-01：修复洗车编排台上传素材缩略图与成片预览在项目详情刷新时闪烁的问题：前端按素材 ID 和成片实际渲染版本稳定复用仍有效的签名媒体 URL，只在资源改变或签名临近过期时换源；重复选择当前项目不再先卸载成片组件。原因：详情接口每次都会刷新 `expires/signature`，完整 URL 变化导致浏览器重新加载同一 `<video>`。涉及 `washcut-agent-demo/src/client/use-stable-media-url.ts`、`AutoVideoApp.tsx`、`components/OutputPreview.tsx`、`src/server/stable-media-url.test.ts` 与两个 `README.md`。验证方式：`pnpm test` 76 项通过、`pnpm build` 通过；内置浏览器在 `127.0.0.1:5175` 使用现有 17 段素材与 V1 成片验证刷新前后素材/成片 `src` 不变、媒体保持就绪且播放连续，字幕版/无字幕版切换正常，验证期间无新增控制台错误或警告。影响：只改变网页预览的 URL 复用行为，不修改素材、成片、下载、签名校验、时间线或编排逻辑。
- 2026-08-31：实施洗车编排台上线前中文乱码与环境配置修复：逐条恢复服务端 API/状态文案、删除项目确认文案和 Worker 中文顺序关键词；新增独立 bootstrap，在动态导入所有业务模块前加载 `.env`，并补充顺序意图与 `DATA_ROOT`、`MEDIA_SIGNING_SECRET`、`VIDEO_PART_SIZE_BYTES` 启动顺序测试。原因：乱码会影响界面、错误反馈和素材先后判断，原入口又会在 `.env` 生效前缓存目录、签名和上传限制。涉及 `washcut-agent-demo/package.json`、`src/server/bootstrap.ts`、`bootstrap.test.ts`、`index.ts`、`auto-video-worker.ts`、`auto-video.test.ts`、`src/client/AutoVideoApp.tsx` 及两个 `README.md`。验证方式：UTF-8 乱码线索复查为 0；`pnpm test` 73 项通过；`pnpm build` 通过；`git diff --check` 通过（仅有既存 LF/CRLF 提示）；在独立端口和临时数据/数据库中完成健康接口、项目创建删除、不支持文件提示、模型状态、页面、设置、删除确认框和控制台冒烟检查，随后删除临时数据。影响：`.env` 现在先于业务模块生效；未触碰现有 SQLite、原片、版本、成片、模型文件、错误合同、时间线或编排逻辑；真实 Qwen/Relay 未验证。
- 2026-08-31：补充洗车编排台真实链路交接文档的中转站不稳定处理规则，说明测试中可能反复出现无法服务、超时和流中断；要求后续 AI 保留原始错误、等待现有恢复机制、避免重复生成，并正确区分外部依赖阻塞与本地程序缺陷。涉及 `washcut-agent-demo/docs/真实AI链路洗车配音测试素材制作_AI交接文档.md` 与两个 `README.md`。验证方式：人工核对文档与程序现有错误透传、断点恢复规则的一致性；未启动或修改业务程序。影响：仅补充交接说明，不改变运行行为。
- 2026-08-31：为洗车编排台新增《真实 AI 链路洗车配音测试素材制作：AI 交接文档》，记录已有网络素材复用策略、本机 IndexTTS2 接口、九类广告作用主包、异常包、逐段口播、授权证据和真实 Qwen/视觉/排序/字幕/渲染验收流程。原因：让下一位 AI 可以直接制作合法可追溯的内部测试片并验证完整真实链路。涉及 `washcut-agent-demo/docs/真实AI链路洗车配音测试素材制作_AI交接文档.md` 与两个 `README.md`。验证方式：对照本机 TTS 脚本/API、现有素材说明和官方许可页面人工核对；本次没有下载或生成媒体，也没有修改、启动业务代码。影响：仅新增交接文档，不改变程序、用户数据、模型或视频结果。
- 2026-08-31：为洗车编排台新增《上线前中文乱码与环境配置失效修复：AI 交接文档》，记录已确认的源码乱码、正常 UTF-8 被旧 PowerShell 错误显示的辨别方法，以及 `.env` 在 ESM 业务模块导入后才加载造成目录、签名密钥和上传限制可能失效的问题；文档限定了实施范围、测试、临时数据冒烟检查、验收条件和下一位 AI 的交付格式。涉及 `washcut-agent-demo/docs/乱码与环境配置修复_AI交接文档.md` 与两个 `README.md`。验证方式：对照 UTF-8 原文、相关源码和启动配置人工核对；本次未修改或运行业务代码。影响：仅提供后续修复规格，不改变现有程序、用户数据、视频编排或渲染行为。
- 2026-08-31：修复洗车片场启动器固定检查并打开 `5173` 导致端口被其他 Vite 项目占用时串台的问题。启动器现在复用已验证身份的现有洗车前端，或从 `5173` 至 `5273` 选择可绑定端口，再让 Vite 严格监听该端口；只有页面身份和后端健康检查都通过后才打开实际地址。涉及 `启动洗车片场Demo.cmd`、`washcut-agent-demo/scripts/find-available-web-port.ps1`、`washcut-agent-demo/vite.config.ts`、`washcut-agent-demo/index.html` 与两个 `README.md`。验证方式：PowerShell 端口选择测试、CMD `--no-browser` 冲突端口启动测试、浏览器页面身份与控制台检查、项目 `pnpm build`。影响：启动器会自动避开被占用的前端端口，API 仍固定为 `8787`，不改变业务数据或视频编排流程。
- 2026-08-31：扩展 Agent 的教学交付规则，要求在每次代码修改后同步讲解实际涉及的技术栈，包括语言、框架、工具和服务的职责、协作关系、前置概念、学习顺序及可动手练习。涉及 `AGENTS.md` 与 `README.md`。验证：人工核对规则位置、技术栈讲解范围及本条日志字段。影响：后续代码修改的教学说明将包含与改动直接相关的技术栈学习内容，不改变项目运行行为。
- 2026-08-31：在 Agent 协作规则中新增“代码修改后的教学说明”要求：当用户希望从零学习时，每次代码修改完成后须解释问题、修改前后行为、设计思路、关键取舍、代码路径与实际验证，帮助用户理解和复现方法。涉及 `AGENTS.md` 与 `README.md`。验证：人工核对新增规则位置、内容完整性及本条日志字段。影响：后续代码修改的交付将包含更详细的教学式说明，不改变项目运行行为。
- 2026-08-27：修复洗车编排台上传不支持的视频文件时的乱码错误提示，将接口文案改为正常中文“仅支持可验证的 MP4、WebM 或 MOV 视频文件。”。涉及 `washcut-agent-demo/src/server/index.ts` 与项目 `README.md`。验证：项目 `pnpm build`、`pnpm test`。
- 2026-08-27：实施洗车广告视频编排优化方案：移除复制项目入口与 API，素材上传改为全量预检后事务提交，流式处理大文件与分片，Relay 增加分级响应硬上限和进度节流，生成状态轮询改用轻量 progress，保留原始错误合同，并拆分普通/字幕渲染产物状态。涉及 `washcut-agent-demo/src/server/index.ts`、`store.ts`、`video-analysis.ts`、`relay-client.ts`、`auto-video-worker.ts`、`auto-video-media.ts`、`src/shared/auto-video-contracts.ts`、`src/client/auto-video-api.ts`、`src/client/AutoVideoApp.tsx` 及项目文档。验证：项目 `pnpm test`（71 项通过）、`pnpm build`。
- 2026-08-26：洗车编排台按参考画面下方字幕调整烧录样式：字号、描边和阴影随实际成片短边缩放，字幕定位到画面高度约 72% 的下部阅读区；词级与降级分段均限制每条最多 14 个字符，旧版异常长字幕渲染时自动缩小，尽量保持单行。涉及 `washcut-agent-demo/src/shared/auto-video-caption.ts`、`washcut-agent-demo/src/remotion/captions/VideoCaptions.tsx`、`washcut-agent-demo/src/client/components/OutputPreview.tsx`、`washcut-agent-demo/src/server/auto-video-captions.ts`、`washcut-agent-demo/src/server/auto-video.test.ts`、项目与根目录 `README.md`。验证方式：字幕分段与 608×1080 画布缩放回归测试、项目 `pnpm test`、`pnpm build` 和实际帧渲染检查。影响：只改变新生成或重新生成的带字幕成片及旧版 WebVTT 降级预览，不改变无字幕 MP4、原片、时间线或编排顺序。
- 2026-08-26：洗车编排台的成片预览改为由字幕开关直接切换已渲染的带字幕/无字幕 MP4，并在换源后恢复当前时间、播放状态、音量、静音和倍速；有字幕成片的新版本不再使用会随窗口缩放的网页字幕层，缺少派生成片的旧版本保留兼容降级。涉及 `washcut-agent-demo/src/client/components/OutputPreview.tsx`、项目与根目录 `README.md`。验证方式：项目 `pnpm test`（74 项通过）、`pnpm build`，以及内置浏览器真实成片播放中双向切换、媒体 URL、播放连续性、网页字幕层和控制台检查。影响：网页预览与字幕开关对应的下载 MP4 保持一致，切换不触发重新渲染。

### 2026-08-26

- 修改内容：彻底移除洗车编排台的 Whisper/Speaches 链路：删除 Provider、兼容快照、旧接口、双模型 Registry 分支、专项测试和过时 A/B 文档，并将转写合同及测试统一为 Qwen；物理删除已核验的本地 Whisper CTranslate2 权重，只保留两个 Qwen 模型目录。
- 修改原因：仅隐藏模型卡片仍会保留大量兼容代码、测试和磁盘文件，造成代码反而增多，也让实际运行边界不清晰。
- 涉及文件：`washcut-agent-demo/src/server/speaches.ts`、`speaches.test.ts`、`transcription-provider.ts`、`transcription-registry.ts`、`transcription-registry.test.ts`、`auto-video-worker.ts`、`auto-video.test.ts`、`index.ts`、`src/client/auto-video-api.ts`、`src/shared/auto-video-contracts.ts`、编排/Qwen 文档、两个过时文档、两个 `README.md`，以及 `D:\短视频\model` 下的旧根文件和 `D:\短视频\model.bin`。
- 验证方式：运行时代码/配置/文档残留搜索为 0；`pnpm test`（71 项通过）、`pnpm build`、Python `unittest`（5 项通过）、`docker compose config --quiet`，并实测 Provider API 只返回 `qwen3-asr`；本地模型目录只剩两个 Qwen 子目录。
- 影响说明：程序只接受 Qwen3-ASR；旧 Whisper 生成快照不再恢复。当前数据库已核验使用 Qwen，原片和成片数据未改动；被物理删除的旧权重只能重新下载恢复。

- 修改内容：新增完整的“安全关闭程序”入口；确认后保留运行中成片任务检查点，卸载 Qwen 并停止本机网关，关闭本项目 Compose 服务及残留 orphan，最后关闭前后端进程树，并兼容前后端分开开窗的启动状态。
- 修改原因：直接关闭命令行不能可靠释放独立 Qwen 网关、模型显存和 Docker orphan 服务，用户需要一个明确、可恢复且只影响当前项目的统一关闭动作。
- 涉及文件：`washcut-agent-demo/qwen3-asr-gateway/app.py`、`washcut-agent-demo/src/server/qwen3-asr.ts`、`washcut-agent-demo/src/server/transcription-provider.ts`、`washcut-agent-demo/src/server/transcription-registry.ts`、`washcut-agent-demo/src/server/transcription-registry.test.ts`、`washcut-agent-demo/src/server/index.ts`、`washcut-agent-demo/src/client/api.ts`、`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/auto-video.css`、两个 `README.md`。
- 验证方式：在 `washcut-agent-demo` 运行 `pnpm test`（74 项全部通过）、`pnpm build`、`python -m py_compile qwen3-asr-gateway\app.py`、`docker compose config --quiet`；使用内置浏览器检查桌面和 390px 设置抽屉、按钮可见性、确认保护及控制台。为避免中断当前服务，未点击确认执行真实关闭。
- 影响说明：运行中的生成版本不会被改为取消，重启后沿用已有检查点恢复；本地网关有 15 秒强制退出边界，远程共享网关不会被终止；只关闭本项目 Compose 服务，不退出 Docker Desktop、不关闭其他项目。

- 修改内容：恢复自动成片任务的安全持续重试；将 `stream_timeout` 等明确瞬态 SSE 失败标为可重试，移除 3 次服务恢复的人工接管上限，并在页面明确显示任务会自动等待完成、无需重复点击。
- 修改原因：当前 `relay_failed / stream_timeout` 被误判为不可重试，且服务恢复达到 3 次后会转为“需要处理”，违背用户一次点击后等待成片完成的操作目标。
- 涉及文件：`washcut-agent-demo/src/server/relay-client.ts`、`washcut-agent-demo/src/server/auto-video-worker.ts`、`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/server/pipeline.test.ts`、`washcut-agent-demo/src/server/auto-video.test.ts`、两个 `README.md`。
- 验证方式：在 `washcut-agent-demo` 运行 `pnpm test`（73 项全部通过）和 `pnpm build`（TypeScript 与 Vite 生产构建通过）。
- 影响说明：瞬态故障先做 5/15/30 秒有界重试，之后仅按 1/5/15 分钟、封顶 15 分钟进行低成本服务探测；服务恢复后从检查点续跑。用户中断、不可重试错误和已完成素材保护边界保持不变；已有“需要处理”的历史任务需点击一次继续以进入新机制。

- 修改内容：从程序可选模型和新建版本合同中删除 Whisper large-v3，只保留 Qwen3-ASR-1.7B；移除 Compose 中的 Speaches 服务，启动器增加 Docker 引擎检测，并在服务就绪后自动加载 Qwen；失败时输出原始接口错误，设置页显示可重试提示。
- 修改原因：转写链路已统一使用 Qwen，避免继续展示不可用的 Whisper 默认卡片，并减少每次启动后的手工模型加载步骤。
- 涉及文件：`启动洗车片场Demo.cmd`、`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/auto-video-api.ts`、`washcut-agent-demo/src/shared/auto-video-contracts.ts`、`washcut-agent-demo/src/server/index.ts`、`washcut-agent-demo/src/server/transcription-registry.ts`、`washcut-agent-demo/src/server/transcription-registry.test.ts`、`washcut-agent-demo/.env`、`washcut-agent-demo/.env.example`、`washcut-agent-demo/docker-compose.yml`、两个 `README.md`。
- 验证方式：`pnpm test`（72 项通过）、`pnpm build`、`docker compose config`、Docker 未运行启动分支实测，以及桌面/375px Browser 设置页、无控制台错误和“打开设置”交互检查。
- 影响说明：新任务与界面仅暴露 Qwen；旧 Whisper 版本快照保留读取/恢复兼容，不删除用户历史数据或磁盘模型文件。Docker 可用时自动加载 Qwen；当前机器 Docker Desktop 引擎未运行，真实成功加载分支未执行，已验证失败提示分支。

- 修改内容：修复 `启动洗车片场Demo.cmd` 只检查后端健康、前端未运行时仍误报就绪的问题；启动器改为分别探测并按需启动前端、后端或两者。
- 修改原因：残留的 8787 后端会让旧启动器直接打开未监听的 5173 地址，表现为双击后页面打不开。
- 涉及文件：`启动洗车片场Demo.cmd`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：复现“后端存活、前端缺失”状态，运行启动脚本后确认两个 URL 均返回 HTTP 200，并执行项目测试与生产构建。
- 影响说明：启动器能够恢复半启动状态；不改变业务逻辑、素材、项目数据或模型配置。

### 2026-08-24

### 2026-08-25

- 修改内容：在通信测试等待期间增加可见的 SSE 接收状态、已等待秒数和三段超时预算提示。
- 修改原因：逐块读取虽然已在服务端生效，但原页面只在完整响应后更新，用户无法感知流式请求仍在工作。
- 涉及文件：`washcut-agent-demo/src/client/components/RelayProtocolTester.tsx`、`washcut-agent-demo/src/client/styles.css`。
- 验证方式：运行 `pnpm build`。
- 影响说明：仅增强通信测试等待反馈，不改变请求、取消或超时逻辑。

- 修改内容：将中转站 Responses SSE 改为逐块读取，并记录首字节、首事件、分块空闲和总时长；增加三类阶段化超时错误码与自动编排重试匹配。
- 修改原因：单一总超时和 `response.text()` 无法判断 Qwen/中转站到底是在首字节、流间隔还是完整响应阶段变慢。
- 涉及文件：`washcut-agent-demo/src/server/relay-client.ts`、`washcut-agent-demo/src/shared/model-conversations.ts`、`washcut-agent-demo/src/server/auto-video-worker.ts`、`washcut-agent-demo/src/server/pipeline.test.ts`、`washcut-agent-demo/src/client/components/ModelConversationLog.tsx`、`washcut-agent-demo/.env.example`。
- 验证方式：运行 `pnpm exec tsx --test src/server/pipeline.test.ts`、`pnpm build`。
- 影响说明：模型会话日志新增 TTFT/首事件/超时阶段字段；默认首字节 120 秒、流间空闲 30 秒、总时长 180 秒，旧 `timeoutMs` 仍可兼容使用。

- 修改内容：将“开始编排”按钮放回素材卡片内部，不再额外创建独立方框，复用现有新建版本弹窗和素材/处理中禁用条件。
- 修改原因：开始动作应与素材就绪状态保持同一视觉分组，避免在版本区之外增加新的卡片。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm build`、`pnpm test`。
- 影响说明：仅恢复空状态下的可见编排入口，不改变生成 API、版本合同或处理流程。

- 修改内容：为项目头部、素材区和编排版本区增加浅色圆角分组框，使用细水绿色边线、白色纸面和极轻阴影建立外层层次；上传虚线框与素材卡保留为内层边界。
- 修改原因：用户反馈项目说明、素材上传和素材列表之间的层次不够明显，需要用克制的圆弧边角方框做分组分隔。
- 涉及文件：`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm build`，并在内置浏览器检查桌面/390px 截图、素材展开/收起、横向溢出和控制台。
- 影响说明：仅加强页面分区视觉层次；项目、素材、版本和生成逻辑不变。

- 修改内容：把素材列表调整为缩略图主导的小型媒体条；桌面端由两列改为四列、常见手机保持两列，缩略图从 54×96 放大为 68×108；移除按钮叠放到缩略图，名称缩为两行 10px，文件大小与时长纵向排列，360px 以下自动回退单列；同时移除全局 320px 最小页面宽度，避免竖向滚动条使 320px 视口产生横向溢出。
- 修改原因：用户希望放大素材画面，同时减少每张素材右侧的空白和文件名占位。
- 涉及文件：`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/src/client/styles.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm build`，并在内置浏览器检查桌面、390px 与 320px 布局、素材展开/收起、横向溢出、截图和控制台。
- 影响说明：调整素材卡片比例和响应式列数，并允许页面在极窄视口正常收缩；素材内容、删除、展开与编排逻辑不变。

- 修改内容：进一步压缩素材列表密度；两列素材行间距从 10px 收紧为 8px，竖屏缩略图从 68×120 调整为 54×96，卡片高度、内部留白和元数据间距同步缩小，同时保留 9:16 画幅与 32px 移除按钮热区。
- 修改原因：用户希望素材排列更紧密，在不牺牲文件名辨识和移除操作可用性的前提下，减少四段默认素材占用的纵向空间。
- 涉及文件：`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm build`，并在内置浏览器检查桌面与移动端布局、素材展开/收起、横向溢出、截图和控制台。
- 影响说明：仅调整素材列表密度；素材内容、删除、展开与编排逻辑不变。

- 修改内容：将素材页改为轻量素材工作台；流程状态并入项目头部，数字项目名补全“项目”前缀，头部提供唯一“新建版本”主操作，已有素材时添加入口压缩为单行，素材使用两列竖屏缩略图列表并合并元数据，“查看全部”移入素材标题行。
- 修改原因：原页面的流程条、上传区和横向深色素材卡形成多个视觉中心，已有素材时添加入口仍过大，竖屏视频在横向容器中产生大量深色留白。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm build`，并在内置浏览器检查桌面、390px 与 320px 布局、素材展开/收起、新建版本弹窗、控制台和截图。
- 影响说明：仅调整项目信息、素材列表和版本入口的结构与视觉；上传、删除、编排、版本与成片业务逻辑不变。

- 修改内容：把素材和版本列表的“查看全部/收起”控件改为右对齐的小号透明文字按钮，移除宽按钮造型，手机端也不再铺满整行。
- 修改原因：原居中宽描边按钮占据视觉中心，与素材和成片内容争抢注意力。
- 涉及文件：`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm build`，并在内置浏览器检查桌面与移动端按钮尺寸、对齐、展开/收起状态和控制台。
- 影响说明：仅降低列表披露控件的视觉权重；素材、版本和展开状态逻辑不变。

- 修改内容：删除已上传素材区域与成片版本区域之间的横向分隔线，保留现有上下留白。
- 修改原因：用户希望去掉两个区域中间多余的线条，使页面衔接更干净。
- 涉及文件：`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm build`，并在内置浏览器检查桌面与移动端分隔区域、字幕开关和控制台。
- 影响说明：仅移除视觉分隔线；素材、版本、成片及相关交互逻辑不变。

- 修改内容：删除成片卡片的“成片已生成”标题，把版本号、状态点、“已完成”和进度移入原主标题位置，并移除已生成版本上方重复的版本摘要。
- 修改原因：用户希望版本信息直接成为成片区域标题，减少卡片上方的独立层级和重复留白。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/components/OutputPreview.tsx`、`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm build`，并在内置浏览器检查桌面与移动端标题位置、目标文案 DOM、字幕开关和控制台。
- 影响说明：仅重排已生成版本的标题信息；处理中版本仍显示版本摘要，字幕、网页预览和 MP4 下载逻辑不变。

- 修改内容：删除成片区域中“字幕开关会同时控制网页预览和下载成片”的说明文字。
- 修改原因：用户希望继续减少成片结果区的文字噪音和纵向层级。
- 涉及文件：`washcut-agent-demo/src/client/components/OutputPreview.tsx`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm build`，并在内置浏览器检查桌面与移动端成片区、目标文案 DOM 和控制台。
- 影响说明：仅删除说明文案；字幕开关、网页预览和 MP4 下载逻辑不变。

- 修改内容：将 `V7`、状态点、“已完成”和 `100%` 合并成左对齐单行版本摘要，并移除完成状态胶囊的背景和边框。
- 修改原因：版本号与右侧胶囊仍像两套独立层级，削弱了上一轮标题扁平化的效果。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm build`，并在内置浏览器检查桌面与移动端版本摘要、状态文本和控制台。
- 影响说明：仅调整版本摘要布局与状态样式；版本号、状态值、进度和生成逻辑不变。

- 修改内容：移除成片区域中“当前版本”和“输出结果”两个辅助小标题，只保留版本号、完成状态和“成片已生成”主标题。
- 修改原因：两个小标题重复解释了相邻内容，形成不必要的上下文字分层和视觉噪音。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/components/OutputPreview.tsx`、`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm build`，并在内置浏览器检查桌面与移动端成片区、关键文案 DOM 和控制台。
- 影响说明：仅精简成片区域标题层级；版本状态、播放器、字幕和下载行为不变。

- 修改内容：在洗车编排台的已上传素材区与当前版本/成片区之间增加浅灰绿色分隔线，并为桌面和移动端设置对应留白。
- 修改原因：浅色主题下两个连续的开放式内容区缺少明确边界，素材输入与成片输出容易被看成同一组内容。
- 涉及文件：`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm build`，并在内置浏览器检查桌面与移动端分区、横向溢出和控制台。
- 影响说明：仅增强主工作区的视觉分区；素材、版本、成片数据和显示顺序不变。

- 修改内容：将洗车编排台的顶栏、项目导航、主画布、任务栏和设置抽屉统一改为雾白与纯白浅色主题，保留浅水绿色状态反馈和橙色主操作，并补足浅色界面的边界、焦点与选中态。
- 修改原因：原深青色顶栏、侧栏和素材容器占据过多视觉面积，与浅色内容区割裂，页面整体显得沉重且层级相互竞争。
- 涉及文件：`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm build`，并在内置浏览器检查桌面与移动端页面、控制台以及设置抽屉交互。
- 影响说明：仅调整页面视觉主题和现有控件反馈；项目、素材、版本、上传、编排与成片生成逻辑不变。

- 修改内容：为右侧任务栏的当前阶段、任务概览和快捷定位增加 1px 浅色边框、现有中等圆角和纸面背景。
- 修改原因：移除冗余状态提示后右栏层级略显松散，需要用克制边界重新建立三个有效信息组。
- 涉及文件：`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm build`、项目仓库内的 `git diff --check`，并检查桌面与移动端页面布局。
- 影响说明：仅调整右侧只读任务栏的视觉分组；统计、快捷定位、项目数据和生成流程不变。

- 修改内容：移除项目标题旁的“可生成版本”状态标签和右侧任务栏中的“原片不会被覆盖”提示，并让窄屏任务栏按剩余三项自然排列。
- 修改原因：两处只读信息都不帮助用户完成上传、编排或查看成片，反而增加页面噪音。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm test`、`pnpm build`、项目仓库内的 `git diff --check`，并检查桌面与窄屏页面布局。
- 影响说明：仅精简界面展示；项目状态合同、原片保存机制、版本生成和素材处理逻辑不变。

- 修改内容：将下载版烧录字幕从距底部 216px 上移到 384px，与网页预览约 20% 画面高度的字幕安全区保持一致。
- 修改原因：下载版字幕此前只距 1920px 高画面底部约 11%，实际观看位置明显低于网页预览。
- 涉及文件：`washcut-agent-demo/src/remotion/captions/VideoCaptions.tsx`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm test`、`pnpm build` 和项目仓库内的 `git diff --check`，重新渲染现有 V7 并抽帧检查字幕位置。
- 影响说明：只调整带字幕 MP4 的字幕垂直位置；网页预览、开关行为、字幕内容与时间、字号、无字幕成片和片段时间线不变。

- 修改内容：让成片区的字幕开关同时控制网页预览和 MP4 下载；渲染阶段保存带字幕与无字幕两份成片，旧版本可在首次下载时补生成带字幕派生文件，并为等待与失败提供明确状态。
- 修改原因：原开关只隐藏或显示预览字幕，下载始终返回无字幕 MP4，与用户对同一字幕状态的预期不一致。
- 涉及文件：`washcut-agent-demo/src/remotion/AutoVideo.tsx`、`washcut-agent-demo/src/remotion/Root.tsx`、`washcut-agent-demo/src/remotion/captions/VideoCaptions.tsx`、`washcut-agent-demo/src/shared/auto-video-contracts.ts`、`washcut-agent-demo/src/server/auto-video-media.ts`、`washcut-agent-demo/src/server/auto-video-worker.ts`、`washcut-agent-demo/src/server/index.ts`、`washcut-agent-demo/src/client/auto-video-api.ts`、`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/components/OutputPreview.tsx`、`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm test`（63 项）、`pnpm build` 和项目仓库内的 `git diff --check`；使用现有 17 段、43.83 秒 V7 实测旧版补渲染，检查 H.264/AAC 元数据、字幕烧录帧及签名下载返回 200。内置浏览器控制运行时在本次会话不可用，因此未完成页面级自动点击和移动端截图。
- 影响说明：下载结果现在严格跟随字幕开关；新版本渲染时间与磁盘占用会增加一份字幕版 MP4，原始素材、编排顺序、无字幕成片和独立字幕文件不变。

- 修改内容：压缩“查看全部素材—当前版本—成片结果”之间的叠加间距，修正成片标题区域未撑满卡片宽度的问题，并让手机端的版本名称与完成状态保持同一行。
- 修改原因：素材区、版本标题和成片卡片各自保留的旧间距叠加后形成大块空白；成片卡片还继承了旧居中对齐，造成内部左右留白过多。
- 涉及文件：`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm test`、`pnpm build`、`git diff --check`，并在内置浏览器检查桌面和 390×844 移动端结果区间距、成片标题宽度与横向溢出。
- 影响说明：仅调整现有结果区的间距、拉伸和响应式排列；素材展开、版本状态、字幕、下载、播放与生成逻辑保持不变。

- 修改内容：将项目页顶部四步流程改为居中的紧凑状态条，步骤文案缩短为“项目 / 素材 / 编排 / 成片”；把项目状态移到项目名称旁，限制中央内容宽度，并压缩项目说明到上传区域的空白。
- 修改原因：原流程横跨整个宽屏，步骤间关联较弱；项目状态和上传操作距离对应标题过远，首屏出现大块无效留白。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm test`、`pnpm build`、`git diff --check`，并在内置浏览器检查 1550×720 宽屏和 390×844 移动端布局。
- 影响说明：仅调整现有流程文案、位置、宽度和间距；步骤状态判断、项目状态、上传、编排与成片逻辑保持不变。

- 修改内容：把新建版本弹窗中的处理方式、画面理解并发、转文字模型、LLM 模型和推理强度统一迁移到设置抽屉“编排设置”；弹窗只保留本次编排要求和创建确认，生成时读取设置中的当前值。
- 修改原因：新建版本弹窗与设置抽屉提供了两套相同配置入口，增加选择成本，也可能让用户误以为两处配置含义不同。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm test`、`pnpm build`、`git diff --check`，并在内置浏览器检查设置抽屉、精简后的新建版本弹窗和移动端布局。
- 影响说明：所有编排配置现在只有设置中的一个入口；生成 API、版本配置快照、历史版本和本地顺序合成能力保持不变。

- 修改内容：减少编排台顶部流程、项目标题、主内容分区、素材/版本/步骤列表和右侧任务概览中的装饰性边框与分隔线，改用留白和轻底色建立层级；继续保留上传拖拽区、表单控件、播放器与危险操作的必要边界。
- 修改原因：页面同时使用边框、分隔线、底色和阴影表达相同层级，形成连续的框框并增加视觉噪音。
- 涉及文件：`washcut-agent-demo/src/client/auto-video.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm test`、`pnpm build`、`git diff --check`，并在内置浏览器检查桌面/移动端布局、快捷定位交互、运行时错误覆盖层和横向溢出。
- 影响说明：仅调整现有前端视觉样式；项目、素材、版本、上传、编排和成片生成逻辑保持不变。

- 修改内容：精简编排台成片与版本区域的重复按钮，移除成片下方的“新建视频”和“重新编排”、专业诊断中的“基于此重新编排”及空状态的重复创建按钮；将“复制项目”移入设置抽屉的低频“项目操作”，并统一左侧项目创建入口名称。
- 修改原因：完成区、项目栏和版本区同时提供语义重叠的操作，造成主次不清和重复选择。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `pnpm test`、`pnpm build`、`git diff --check`，并在内置浏览器检查桌面/移动端按钮层级、设置抽屉和控制台。
- 影响说明：新项目仅从左侧项目栏创建，新版本仅从“编排版本”区创建；复制项目能力仍保留在设置中，现有项目、版本和生成数据不变。

- 修改内容：将洗车自动编排项目的素材上传上限从 20 个提高到 50 个，并统一前端提示、上传批次、项目/版本数据合同及旧数据归一化上限；新增项目剩余名额校验和 50/51 边界回归测试。
- 修改原因：支持一次任务上传更多碎片化洗车素材，同时确保页面、接口和持久化合同对上限的理解一致。
- 涉及文件：`washcut-agent-demo/src/shared/auto-video-contracts.ts`、`washcut-agent-demo/src/server/index.ts`、`washcut-agent-demo/src/server/store.ts`、`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/server/auto-video.test.ts`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行素材数量合同回归测试、完整 TypeScript 测试、生产构建和 `git diff --check`。
- 影响说明：每个自动编排项目最多可保存和编排 50 个素材；单文件 250 MB 上限及旧版通用素材接口保持不变。

- 修改内容：为编排台素材和版本列表增加渐进展开；桌面端默认显示 4 段素材和 4 个版本，手机端默认显示 2 段素材和 3 个版本，可查看全部或收起，且收起时继续显示当前选中的历史版本。
- 修改原因：项目包含大量素材时，完整网格会把当前成片和版本区域推到数千像素之后，导致页面过长、定位成本高。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/auto-video.css`。
- 验证方式：运行 `npm run build`、`npm test`、`git diff --check`，并在内置浏览器检查桌面和移动端默认数量、全部展开、再次收起、历史版本保持可见、控制台和横向溢出。
- 影响说明：仅增加按项目隔离的客户端显示状态和响应式可见数量；所有素材、版本、上传、移除、编排和生成数据保持不变。

- 修改内容：完成编排台第二轮可读性重构，建立 13/14/15/24/31px 的稳定文字层级，放大流程、项目导航、素材、版本与任务概览文字和操作热区，并将宽屏工作区扩展为项目导航、中央画布、任务概览三栏布局。
- 修改原因：主页面文案精简后，剩余信息仍存在字号偏小、层级接近和宽屏空间利用不足的问题。
- 涉及文件：`washcut-agent-demo/src/client/auto-video.css`。
- 验证方式：运行 `npm run build`、`npm test`、`git diff --check`，并在内置浏览器检查 1280×720、390×844 与 320×800 布局、控制台、横向溢出及版本快捷定位交互。
- 影响说明：仅调整现有前端排版、栏宽、间距和响应式规则；未修改 React 状态、接口、数据合同或视频生成逻辑。

- 修改内容：精简编排台主页面文案，移除当前版本的模型、分析策略、并发、推理强度、转写快照等技术参数；版本卡片不再显示模型名，素材卡片不再显示 MIME 与分辨率，逐素材处理名单改为汇总进度，并压缩流程栏和右侧任务栏文案。
- 修改原因：技术参数和重复说明占据主页面注意力，普通用户只需要看到素材、版本、状态、进度和可执行操作。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/styles.css`。
- 验证方式：运行 `npm run build`、`npm test`、`git diff --check`，并检查桌面与移动端页面文字密度、状态信息和快捷定位操作。
- 影响说明：仅精简普通工作区的显示内容；模型、推理、并发和转写设置仍保留在设置与创建版本流程中，生成合同和处理逻辑不变。

### 2026-08-21

- 修改内容：重做编排台可读性样式，恢复正文、标题、素材信息和右侧上下文的舒适字号，增加留白，并收起重复的流程辅助说明。
- 修改原因：原页面信息密度过高，文字过小，用户难以快速识别当前阶段、素材状态和下一步操作。
- 涉及文件：`washcut-agent-demo/src/client/styles.css`。
- 验证方式：运行 `npm run build`、`npm test`、`git diff --check`，并通过本地浏览器检查桌面与 390×844 移动端布局及素材上传快捷定位。
- 影响说明：仅调整前端排版、字号、间距和响应式显示，不改变业务流程、数据合同或接口行为。

- 修改内容：在编排台宽屏工作区增加右侧任务上下文栏，汇总原始片段、已检测素材、保存版本与画布信息，并提供素材上传/编排版本快捷定位和“原片不可变”约束提示；窄屏自动折叠为辅助区。
- 修改原因：现有页面在主工作区右侧留下未承载信息的空白，用户缺少对当前阶段、素材规模和下一步动作的持续上下文。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/styles.css`。
- 验证方式：运行 `npm run build`，并检查桌面/窄屏断点下新增区域不遮挡原有上传、版本和弹窗操作。
- 影响说明：仅新增现有数据的只读摘要与页面内滚动快捷入口，保留原有业务接口、素材不变量和生成流程不变。

- 修改内容：根据实际桌面截图做密度优化，放宽主工作区到更大的桌面宽度，压缩顶部栏、流程线、项目头部、上传投放区和素材卡片高度，让主要操作在更短的首屏内完成。
- 修改内容：根据实际桌面截图做密度优化，放宽主工作区到更大的桌面宽度，压缩顶部栏、流程线、项目头部、上传投放区和素材卡片高度，让主要操作在更短的首屏内完成。
- 修改原因：页面两侧留白过多，核心内容纵向堆叠偏长，影响素材浏览和上传操作的连续性。
- 涉及文件：`washcut-agent-demo/src/client/styles.css`。
- 验证方式：运行生产构建并重新加载本地页面截图，检查现有按钮和上传/版本区域仍可见。
- 影响说明：仅调整桌面容器宽度、间距、组件高度和响应式断点，不新增功能、不删除按钮、不改变业务逻辑。

### 2026-08-21

- 修改内容：按现有功能重新收敛编排台的前端层级，仅围绕项目列表、素材上传、模型高级设置、生成版本和版本详情重排视觉；把流程提示压成顶部状态线，去掉多余的卡片堆叠，保留所有已有按钮和操作入口。
- 修改原因：上一版视觉稿引入了超出当前程序功能量级的“控制室”分区，导致页面显得复杂，和实际使用路径不匹配。
- 涉及文件：`washcut-agent-demo/src/client/styles.css`。
- 验证方式：重新加载本地页面，检查真实组件结构、现有按钮数量与生产构建。
- 影响说明：仅调整现有组件的布局、表面层级、颜色和响应式呈现，不新增功能、不删除按钮、不改变业务逻辑。

### 2026-08-21

- 修改内容：重整洗车视频编排台的前端视觉层，统一为接近 Codex 的中性灰白界面、单一绿色强调色、轻量分隔线和更紧凑的导航/卡片层级；保留顶部模型设置、模型对话、新建视频、项目删除、素材上传/删除、版本管理、生成/取消/重试、字幕与导出等现有按钮与交互入口。
- 修改原因：当前页面颜色、渐变、阴影和卡片边界过多，信息层级不够清晰，用户希望整体画面更简洁。
- 涉及文件：`washcut-agent-demo/src/client/styles.css`。
- 验证方式：运行 TypeScript/Vite 生产构建，并进行本地页面截图与交互冒烟检查。
- 影响说明：仅调整客户端样式和响应式布局，不改变业务逻辑、按钮事件、接口合同或素材处理流程。

### 2026-08-21

- 修改内容：修正项目列表删除按钮被通用列表按钮样式覆盖的问题，改为右侧紧凑的 `×` 图标按钮。
- 修改原因：避免删除入口拉伸为整行红色胶囊，遮挡项目条目内容。
- 涉及文件：`washcut-agent-demo/src/client/styles.css`、`washcut-agent-demo/src/client/AutoVideoApp.tsx`。
- 验证方式：运行项目生产构建。
- 影响说明：仅调整删除入口的尺寸、定位和悬停反馈，删除行为与接口不变。

### 2026-08-21

- 修改内容：为洗车视频编排 Demo 的“我的项目”列表增加删除按钮，并补充服务端项目删除与素材/成片目录清理；删除前需确认，运行中的版本不可删除。
- 修改原因：让用户可以直接清理不再需要的项目及其原始素材、版本和成片产物。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/auto-video-api.ts`、`washcut-agent-demo/src/client/styles.css`、`washcut-agent-demo/src/server/index.ts`、`washcut-agent-demo/src/server/store.ts`。
- 验证方式：运行项目测试与生产构建。
- 影响说明：删除不可恢复；需先完成或中断运行中的版本后才能删除项目。

### 2026-08-21

- 修改内容：将 Qwen 的 Windows 提权启动改为随网关提供的 `start-qwen-gateway.ps1` 启动器。启动器负责触发 UAC、在管理员进程中直接运行网关并记录独立日志；主服务在提权失败时保留原始 PyTorch DLL 错误和提权错误。
- 修改原因：受限进程加载 `torch_python.dll` 时，原有内联 `Start-Process -Verb RunAs` 可能返回 `0xc0000142`，导致真正的 `[WinError 5]` 被覆盖，无法实现稳定的一键启动。
- 涉及文件：`washcut-agent-demo/src/server/qwen3-asr.ts`、`washcut-agent-demo/qwen3-asr-gateway/start-qwen-gateway.ps1`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：PowerShell 语法解析通过；运行 `npm test`（61 项通过）和 `npm run build`（TypeScript/Vite 构建通过）。
- 影响说明：用户点击一次 Qwen 启用按钮即可触发 UAC、启动管理员网关并继续加载模型；非 Windows 或无需提权的环境保持原有启动路径。

### 2026-08-21

- 修改内容：当 Windows 受限进程加载 `torch_python.dll` 返回 `[WinError 5]` 时，Qwen 启用流程会自动回收由主服务托管的本地网关，并通过 Windows UAC 重新启动网关后重试模型加载；普通环境仍保持原有无提权启动路径。
- 修改原因：用户点击 Qwen 启用按钮后，网关进程虽然可达，但受限进程无法加载 PyTorch DLL，模型启用失败且需要手工重新启动。
- 涉及文件：`washcut-agent-demo/src/server/qwen3-asr.ts`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：运行 `npm test`（61 项通过）和 `npm run build`（TypeScript/Vite 构建通过）；在受限环境复现 `[WinError 5]`，在正常 Windows 权限下验证同一虚拟环境可导入 `torch 2.13.0+cu126`。
- 影响说明：用户只需点击一次 Qwen 启用按钮；若 Windows 显示 UAC，需完成系统安全确认，手工启动网关和模型的路径不变。

### 2026-08-21

- 修改内容：在工作区全局 Agent 规则中加入防御性工程停止条件：默认不新增哈希、合同冻结、基线或额外门禁；只有能说明具体失败场景及现有机制缺口时才允许新增，同时保留认证、数据安全、不可逆操作和正式发布等高风险安全边界。
- 修改原因：避免低风险任务在真正执行前堆叠无必要的防御性工程，控制 Token、延迟和实现复杂度。
- 涉及文件：`AGENTS.md`、`README.md`。
- 验证方式：人工核对规则同时覆盖“默认不新增”“不得删除既有安全措施”“高风险环节继续严格处理”和新增前的两问自检；本次为文档修改，未运行代码测试。
- 影响说明：后续 Agent 任务默认优先推进可验证的业务实现；不改变现有认证、数据安全、不可逆操作、正式发布或项目已有防护行为。

### 2026-08-21

- 修改内容：在高级设置和生成版本弹窗加入推理强度选择（低/中/高）；默认低，按连接保存高级设置，并将每次生成的选择快照传给中转站请求。
- 修改原因：用户需要在速度、成本和复杂素材理解质量之间主动取舍。
- 涉及文件：`washcut-agent-demo/src/shared/auto-video-contracts.ts`、`washcut-agent-demo/src/server/relay-client.ts`、`washcut-agent-demo/src/server/index.ts`、`washcut-agent-demo/src/server/auto-video-worker.ts`、`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/styles.css`、`README.md`。
- 验证方式：运行 `npm test`（61 项通过）和 `npm run build`（TypeScript/Vite 构建通过）。
- 影响说明：新生成版本固定本次推理强度，历史版本默认兼容低强度；若上游中转站不支持所选值，仍透传原始错误。

### 2026-08-21

- 修改内容：在项目页“高级设置”增加 LLM 模型选择器和模型列表刷新入口；选择的模型作为后续智能编排默认值并按连接保存在浏览器本地，生成版本弹窗仍可单次覆盖。
- 修改原因：原先只能在生成版本弹窗中选择 LLM，项目级设置没有统一的模型选择入口。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/styles.css`、`README.md`。
- 验证方式：运行 TypeScript/Vite 生产构建，并通过本地浏览器展开高级设置检查模型选择控件和当前连接状态。
- 影响说明：仅增加客户端模型选择入口，仍通过现有中转站模型发现接口读取列表，不改变服务端连接和版本合同。

### 2026-08-21

- 修改内容：将语音转文字模型切换器同时放入项目页“高级设置”，保留生成版本弹窗中的同一入口；用户无需先打开生成弹窗即可切换 Whisper 或 Qwen。
- 修改原因：原入口只出现在智能编排弹窗中，用户难以发现；顶部“模型设置”容易被误认为是转写模型设置，实际只是连接配置。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`README.md`。
- 验证方式：运行 TypeScript/Vite 生产构建，并通过本地浏览器检查项目页高级设置中的转写模型入口。
- 影响说明：复用现有模型切换逻辑和互斥/卸载保护，不改变服务端模型生命周期合同。

### 2026-08-21

- 修改内容：收拢洗车视频编排台的用户流程：新增“新建项目—上传素材—选择编排—查看成片”四步引导；将模型与转文字配置移入高级设置；在素材上传完成后提供明确的下一步入口；修正项目创建按钮的实际语义。
- 修改原因：原界面把项目、素材、模型服务和版本操作同时暴露在首屏，创建按钮还会暗示会立即上传素材，导致首次使用时不知道下一步该做什么。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/styles.css`、`README.md`。
- 验证方式：运行 TypeScript/Vite 生产构建，并通过浏览器首屏、创建项目、素材步骤与响应式布局检查。
- 影响说明：不改变生成接口、素材合同或版本数据；仅调整入口顺序、文案和配置区域的可见性。

### 2026-08-21

- 修改内容：为中转站模型增加“本次生成版本”选择入口。创建智能编排版本时可读取当前中转站的模型列表并选择具体模型；所选模型写入版本快照并用于实际视觉理解请求，读取失败时回退到连接默认模型。
- 修改原因：中转站可能同时提供多个模型，原流程只能使用连接保存的单一默认模型，无法按任务选择。
- 涉及文件：`washcut-agent-demo/src/shared/auto-video-contracts.ts`、`washcut-agent-demo/src/server/index.ts`、`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/styles.css`、`README.md`。
- 验证方式：在 `washcut-agent-demo` 运行 `npm test`（61 项通过）和 `npm run build`（TypeScript/Vite 构建通过）。
- 影响说明：未选择模型时保持原有连接默认值；已有生成版本不变，模型选择仅影响新建版本。

### 2026-08-20

- 修改内容：为默认 Speaches/Whisper 转写增加服务端固定的洗车热词上下文，并通过 OpenAI 兼容 `transcription.prompt` 传入上游；新生成版本保存该上下文快照。
- 修改原因：提高洗车服务、施工项目、车辆部件和营销优惠术语在口播中的识别倾向，同时保证任务重试可复现。
- 涉及文件：`washcut-agent-demo/src/server/speaches.ts`、`washcut-agent-demo/src/shared/auto-video-contracts.ts`、`washcut-agent-demo/.env.example`、`washcut-agent-demo/src/server/speaches.test.ts`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：转写 multipart 参数回归测试、TypeScript 测试与生产构建。
- 影响说明：默认转写会携带洗车领域热词；热词仅由服务端配置，浏览器不能注入任意转写 Prompt。

### 2026-08-20

- 修改内容：移除洗车广告成片预览页面的 WebVTT 字幕下载按钮。
- 修改原因：字幕文件仅用于网页内按时间显示字幕，不再提供给用户下载。
- 涉及文件：`washcut-agent-demo/src/client/components/OutputPreview.tsx`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：TypeScript/Vite 生产构建。
- 影响说明：MP4 下载、字幕开关、字幕时间控制与后端 VTT 兼容产物保持不变。

### 2026-08-20

- 修改内容：将洗车广告字幕生成从优先使用段级转写改为优先使用词级时间戳分组，限制每条字幕的文字和时长；禁用预览中的浏览器原生 VTT 显示，避免与网页字幕层重复。
- 修改原因：段级时间戳导致整句口播常驻，原生轨道自动显示会与网页字幕叠加。
- 涉及文件：`washcut-agent-demo/src/server/auto-video-captions.ts`、`washcut-agent-demo/src/server/auto-video.test.ts`、`washcut-agent-demo/src/client/components/OutputPreview.tsx`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：词级字幕分组回归测试、完整 TypeScript 测试和生产构建。
- 影响说明：具有词级时间戳的新生成版本会按短句精准展示；只有段级时间戳的转写保留兼容的整段展示。

### 2026-08-20

- 修改内容：同步上移洗车广告播放器非全屏状态的网页字幕位置。
- 修改原因：此前位置规则仅限定在 `:fullscreen`，导致普通预览没有跟随用户要求的位置变化。
- 涉及文件：`washcut-agent-demo/src/client/styles.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：TypeScript/Vite 生产构建。
- 影响说明：全屏字幕位置保持现状；普通预览字幕现在也位于更高的下部安全区。

### 2026-08-20

- 修改内容：进一步上移洗车广告预览在播放器容器全屏时的字幕位置。
- 修改原因：匹配用户要求的更高下部字幕安全区。
- 涉及文件：`washcut-agent-demo/src/client/styles.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：TypeScript/Vite 生产构建。
- 影响说明：只调整全屏字幕的纵向位置。

### 2026-08-20

- 修改内容：将洗车广告预览在播放器容器全屏时的字幕上移到用户参考图所示的下部安全区。
- 修改原因：避免字幕贴近底部控制栏，并将其放在画面主体下方的稳定阅读位置。
- 涉及文件：`washcut-agent-demo/src/client/styles.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：TypeScript/Vite 生产构建。
- 影响说明：只影响全屏网页字幕的纵向位置；字体、描边、普通预览、VTT 与 MP4 不变。

### 2026-08-20

- 修改内容：将洗车广告预览从原生视频单元素全屏改为包含视频、网页字幕和控制栏的播放器容器全屏；新增轻量自定义播放、进度、时长和全屏控件。
- 修改原因：原生视频全屏会将网页字幕叠层排除在全屏外，且浏览器对原生 VTT 字幕显示行为不一致。
- 涉及文件：`washcut-agent-demo/src/client/components/OutputPreview.tsx`、`washcut-agent-demo/src/client/styles.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：TypeScript/Vite 生产构建。
- 影响说明：点击全屏或双击画面后，视频、字幕与控制栏会整体进入全屏；不改变成片 MP4、WebVTT 文件或字幕时间线。

### 2026-08-20

- 修改内容：补强洗车广告预览在浏览器原生全屏下的字幕轨道切换，兼容标准全屏、全屏外层容器与 WebKit 视频全屏事件。
- 修改原因：部分浏览器原生视频全屏不会把 `document.fullscreenElement` 设为视频元素本身，导致此前的全屏字幕显示条件未满足。
- 涉及文件：`washcut-agent-demo/src/client/components/OutputPreview.tsx`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：TypeScript/Vite 生产构建。
- 影响说明：只扩大全屏字幕可识别的事件与目标范围，不改变普通预览、字幕文件或 MP4 产物。

### 2026-08-20

- 修改内容：将洗车广告成片预览的字幕由过大的海报式比例下调为用户参考图中的轻量短视频字幕比例；同步缩小原生全屏 WebVTT 轨道的字号与描边。
- 修改原因：让字幕清晰可读但不遮挡洗车画面主体。
- 涉及文件：`washcut-agent-demo/src/client/styles.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：TypeScript/Vite 生产构建。
- 影响说明：字幕颜色、描边、全屏持续显示、WebVTT 与 MP4 产物行为保持不变。

### 2026-08-20

- 修改内容：修复洗车广告成片预览在视频原生全屏时网页字幕叠层消失的问题；常规预览字幕改为按播放器容器放大，原生全屏切换至经 `::cue` 设定白字黑描边的 WebVTT 轨道。
- 修改原因：参考画面需要显著更大的短视频字幕，且全屏模式必须持续显示字幕而不是回落为浏览器默认小号样式。
- 涉及文件：`washcut-agent-demo/src/client/components/OutputPreview.tsx`、`washcut-agent-demo/src/client/styles.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：TypeScript/Vite 生产构建，以及页面全屏事件与字幕轨道状态代码审查。
- 影响说明：普通预览与全屏字幕均为白字、黑描边效果；不改变 MP4 不烧录字幕、WebVTT 下载或字幕时间线。

### 2026-08-20

- 修改内容：将洗车广告编排网页成片预览的字幕改为短视频常见的底部居中白字黑描边样式，移除深色圆角背景卡片。
- 修改原因：匹配用户提供的参考画面，提高移动端画面上的识别度，并避免字幕卡片遮挡洗车素材。
- 涉及文件：`washcut-agent-demo/src/client/styles.css`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：TypeScript/Vite 生产构建。
- 影响说明：只改变网页预览层的字幕外观；MP4 不烧录字幕、WebVTT 独立下载和字幕时间线保持不变。

### 2026-08-20

- 修改内容：修复洗车广告编排应用联系表、单截图和精查视觉请求错误使用“验证中转站连接”系统指令的问题；改为通过 Responses API 的 `instructions` 字段发送各自的业务视觉分析指令，仍保持普通图片输入且不启用 `text.format/json_schema`。
- 修改原因：避免测试助手的泛化指令覆盖洗车素材理解约束，并让模型对话记录中显示的系统指令与实际任务一致。
- 涉及文件：`washcut-agent-demo/src/server/auto-video-ai.ts`、`washcut-agent-demo/src/server/auto-video.test.ts`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：联系表视觉请求体回归测试、完整 TypeScript 测试与生产构建。
- 影响说明：视觉模型会收到“视频素材联合理解”业务指令；其用户输入保留本次结构化内容与附件图片，原始视频/音频权限边界不变。

### 2026-08-20

- 修改内容：修复洗车广告编排应用的 Whisper/Qwen 切换仍依赖用户手工设置 TTL 的问题；Whisper 保持首次转写按需加载，切换离开时主程序通过 Speaches `/api/ps/{modelId}` 显式卸载并并行复查已加载模型列表；项目管理的 Speaches 容器兼容设置 `WHISPER__TTL=0` 与 `STT_MODEL_TTL=0`，启动脚本自动拉起该服务，新增生命周期回归测试。
- 修改原因：让用户直接在网页中完成模型切换，并兼容本机 Speaches 0.1.x 与新版配置名；避免只凭应用侧声明推断 GPU 模型已经释放。
- 涉及文件：`washcut-agent-demo/src/server/speaches.ts`、`washcut-agent-demo/src/server/speaches.test.ts`、`washcut-agent-demo/.env`、`washcut-agent-demo/.env.example`、`washcut-agent-demo/docker-compose.yml`、`启动洗车片场Demo.cmd`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：Speaches/Registry 定向测试、完整 TypeScript 测试、生产构建、Compose 配置检查和本机 Speaches 实际切换检查。
- 影响说明：用户无需手改 TTL 环境变量；卸载状态不能确认时不会加载 Qwen，HTTP 上游原始错误继续透传。Speaches 的确认粒度是“模型不在已加载列表”，不是 CUDA allocated/reserved 字节测量。

### 2026-08-20

- 修改内容：为洗车广告编排应用新增全局转文字模型切换按钮和严格互斥生命周期；Qwen 增加无副作用健康检查、显式加载/卸载、推理互斥、垃圾回收、CUDA 缓存清理及显存归零确认，Speaches 增加 `STT_MODEL_TTL=0` 部署合同检查；运行中的视频任务禁止切换，创建智能版本必须使用当前已启用模型。
- 修改原因：让用户明确选择 Whisper 或 Qwen，并防止两个转写模型同时驻留 GPU、切换过程中并发转写或卸载失败后继续加载第二个模型。
- 涉及文件：`washcut-agent-demo/src/shared/auto-video-contracts.ts`、`washcut-agent-demo/src/server/transcription-provider.ts`、`washcut-agent-demo/src/server/transcription-registry.ts`、`washcut-agent-demo/src/server/speaches.ts`、`washcut-agent-demo/src/server/qwen3-asr.ts`、`washcut-agent-demo/src/server/index.ts`、`washcut-agent-demo/src/server/store.ts`、`washcut-agent-demo/src/server/qwen3-asr.test.ts`、`washcut-agent-demo/src/server/transcription-registry.test.ts`、`washcut-agent-demo/src/client/auto-video-api.ts`、`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/styles.css`、`washcut-agent-demo/qwen3-asr-gateway/app.py`、`washcut-agent-demo/qwen3-asr-gateway/test_app.py`、`washcut-agent-demo/qwen3-asr-gateway/README.md`、`washcut-agent-demo/.env`、`washcut-agent-demo/.env.example`、`washcut-agent-demo/docker-compose.yml`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：`npm test` 56/56 通过；`npm run build` 通过；Qwen 网关 5/5 Python 测试与 Python 语法检查通过；桌面与 390×844 移动端浏览器中验证全局按钮、Whisper 启用态、ARIA 状态和无控制台错误；真实 CUDA 加载后测得 5,160,450,048 字节 allocated / 5,179,965,440 字节 reserved，卸载后两项均为 0 且 `gpuMemoryReleased=true`；5173、8787、8010、8000 无遗留监听。
- 影响说明：任何停止失败、Speaches 未声明即时释放或 Qwen 未确认显存归零的情况都会中止切换，不会启动第二个转写模型；现有版本快照和历史输出不变。React 最佳实践用于保持数据请求和按钮状态流清晰，前端验收流程促使切换器改为无项目时也可见的全局控件。

### 2026-08-20

- 修改内容：完成 Qwen ForcedAligner 修复后的真实重测、主应用 HTTP Provider 合同验证和 17 段真实洗车口播 A/B；新增逐段对照报告并更新实施计划状态。
- 修改原因：补齐此前因审批余额中断的真实对齐验证，并以同批真实素材检验 Qwen 文本、时间戳和 TypeScript 适配路径，避免仅凭单元测试声称可用。
- 涉及文件：`washcut-agent-demo/docs/qwen3-asr-real-material-ab-2026-08-20.md`、`washcut-agent-demo/docs/qwen3-asr-switchable-transcription-plan.md`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：真实 CUDA 模型加载；中文冒烟音频 ASR 与 18 项 ForcedAligner 时间戳；17/17 真实洗车片段转写成功且 17/17 时间戳合同有效；主应用 `Qwen3AsrTranscriptionProvider` 的健康检查、快照、multipart 调用和 `NormalizedTranscript` 校验；TypeScript 类型检查、54 项项目测试、2 项 Python 回归测试、Python 语法检查、生产构建；8010 与 GPU 终态检查。
- 影响说明：Qwen 本地转写链路已证明可用，真实素材中出现多处领域语句改善迹象；因缺少人工参考稿，不能计算准确率，Whisper 继续作为默认模型。测试网关已关闭，显存已释放。

### 2026-08-20

- 修改内容：根据真实 `qwen-asr 0.0.6` 返回合同修复私有网关的 ForcedAligner 结果解析；支持 `List[ForcedAlignResult]` 中的 `ForcedAlignResult.items`，同时保留旧列表形状兼容，并增加两项 Python 回归测试。
- 修改原因：真实测试中 ASR 已正确输出中文句子，但网关将官方 `ForcedAlignResult` 对象误判为无效 item 列表，导致有效对齐结果返回 `QWEN_ALIGN_INVALID_RESULT`。
- 涉及文件：`washcut-agent-demo/qwen3-asr-gateway/app.py`、`washcut-agent-demo/qwen3-asr-gateway/test_app.py`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：ASR 与 ForcedAligner 模型健康检查均为 ready；真实 ASR 成功；Python 语法检查与两项单元测试通过。修复后的真实 ForcedAligner 重测因 RootFlowAI 审批预扣余额不足而未执行。
- 影响说明：仅修正官方 SDK 结构适配，不生成估算时间戳，不改写上游错误；当前没有遗留网关监听进程。

### 2026-08-20

- 修改内容：核对并接通洗车广告智能编排应用的本机 Qwen3-ASR 部署；确认两个完整模型快照、Python 网关历史真实加载/转写记录，并为 TypeScript 主应用配置 `127.0.0.1:8010` 的 ASR 与 ForcedAligner 地址。
- 修改原因：此前网关和模型已部署，但主应用 `.env` 仍只有 Whisper 配置，导致 Qwen 在界面中始终显示未配置。
- 涉及文件：`washcut-agent-demo/.env`、`washcut-agent-demo/docs/qwen3-asr-switchable-transcription-plan.md`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：检查模型快照必需文件与网关日志；TypeScript 类型检查通过，54 项测试通过，并完成生产构建。
- 影响说明：Qwen 仅在本机网关健康且两个模型 ID 匹配时可选；Whisper 保持默认，既有版本和失败语义不变，不会静默回退。真实 ForcedAligner 端到端和洗车素材 A/B 仍待验证。

### 2026-08-19

- 修改内容：新增 `washcut-agent-demo/qwen3-asr-gateway/` 私有 Qwen3-ASR 网关适配器，按官方 `qwen-asr` API 加载 ASR 与 ForcedAligner，提供本机绑定、可选 API Key、结构化错误和真实时间戳输出。
- 修改原因：完成可切换转写计划的独立模型服务边界，不把模型权重或凭据放入 TypeScript 主应用，也不允许 Qwen 静默回退到 Whisper。
- 涉及文件：`washcut-agent-demo/qwen3-asr-gateway/app.py`、`requirements.txt`、`.env.example`、`README.md`。
- 验证方式：已进行 Python 语法检查，以及 `pnpm.cmd exec tsc --noEmit`、`pnpm.cmd test`（54 项通过）和 `pnpm.cmd build`（TypeScript/Vite 通过）。真实模型加载、GPU 执行和洗车素材 A/B 尚未执行。
- 影响说明：Qwen 仍保持禁用，直到两个独立完整 Qwen 模型快照和 Python/CUDA 运行环境就绪。


### 2026-08-19

- Change: completed the application-side implementation of switchable Whisper/Qwen3-ASR transcription for the car-wash short-video project, including private Qwen ASR + ForcedAligner gateway contracts, health status API, generation-level snapshots, real-timestamp validation, raw error propagation, provider selector UI, deployment documentation, and tests.
- Reason: provide a comparable Qwen path for Chinese car-wash voice-over, background noise, dialects, and domain terminology while keeping retry/resume behavior deterministic and preventing silent provider fallback.
- Files: `washcut-agent-demo/src/shared/auto-video-contracts.ts`, `washcut-agent-demo/src/server/{transcription-provider,speaches,qwen3-asr,transcription-registry,auto-video-worker,index}.ts`, `washcut-agent-demo/src/client/{auto-video-api,AutoVideoApp}.tsx`, `washcut-agent-demo/src/client/styles.css`, `washcut-agent-demo/.env.example`, `washcut-agent-demo/docker-compose.yml`, `washcut-agent-demo/docs/qwen3-asr-gateway.md`, `washcut-agent-demo/src/server/qwen3-asr.test.ts`, and `README.md`.
- Verification: ran `pnpm.cmd exec tsc --noEmit`, `pnpm.cmd test` (54 passed), and `pnpm.cmd build` (TypeScript/Vite passed) in `washcut-agent-demo`. A real Qwen private gateway, model loading, GPU execution, and car-wash-material E2E A/B validation were not run.
- Impact: Whisper large-v3 remains default; Qwen is unavailable if either service is unconfigured, unreachable, not ready, or reports a mismatched model; historical generations keep legacy Whisper compatibility. The complete model snapshots and the private gateway must be deployed before real Qwen transcription can be enabled.

### 2026-08-19

- 修改内容：新增 Qwen3-ASR-1.7B 可切换语音转写实施计划，定义 Whisper/Qwen 互斥按钮、生成版本级模型快照、Qwen 转写与强制对齐链路、服务边界、错误处理、测试和 A/B 评测要求。
- 修改原因：为洗车短视频口播在噪声、方言和专业词场景下评估更强中文 ASR 提供可执行且可回退的工程路径，同时避免运行中混用模型或丢失字幕时间戳。
- 涉及文件：`washcut-agent-demo/docs/qwen3-asr-switchable-transcription-plan.md`、`README.md`。
- 验证方式：人工复核计划与现有转写架构（Speaches/faster-whisper、`NormalizedTranscript`、生成版本工作器、字幕时间戳）的一致性；本次仅新增设计文档，未改动运行时代码、未部署 Qwen 服务，未运行构建或模型评测。
- 影响说明：无运行时行为变化；后续实施前须按文档完成服务部署、合同测试、真实洗车素材 A/B 评测和完整回归验证。

### 2026-08-19

- 修改内容：生成版本区改为自适应多列卡片；已完成、失败、已取消和待人工处理的版本在悬停或键盘聚焦时显示删除按钮。新增删除版本接口，清理版本数据库记录、素材检查点、关联模型对话和该版本的导出工件。
- 修改原因：避免版本数量增加后横向单列滚动难以浏览，并让已不需要的历史编排结果可被明确、可控地移除。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/auto-video-api.ts`、`washcut-agent-demo/src/client/styles.css`、`washcut-agent-demo/src/server/index.ts`、`washcut-agent-demo/src/server/store.ts`、`washcut-agent-demo/src/server/auto-video.test.ts`、`README.md`。
- 验证方式：在 `washcut-agent-demo` 运行 `pnpm test`（51 项通过）与 `pnpm build`（TypeScript 校验和 Vite 生产构建通过）；新增存储层回归测试覆盖版本删除同时清理其检查点。
- 影响说明：运行中的版本不提供删除入口且服务端拒绝删除；删除已完成版本需二次确认，确认后其处理结果、字幕、成片及记录不可恢复，原始上传素材不受影响。

### 2026-08-19

- 修改内容：为智能编排新增版本级“画面理解并发”选项，提供 1、2、3、4 路选择，默认 1 路；所选值保存到生成版本快照，基础画面理解与可选精查均按该值限流，所有项目合计仍受 4 路进程级上限保护。
- 修改原因：允许在模型中转站容量充足时缩短批量素材理解时间，同时保留串行默认值以降低限流和网关错误风险。
- 涉及文件：`washcut-agent-demo/src/shared/auto-video-contracts.ts`、`washcut-agent-demo/src/server/index.ts`、`washcut-agent-demo/src/server/auto-video-worker.ts`、`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/styles.css`、`washcut-agent-demo/src/server/auto-video.test.ts`、`README.md`。
- 验证方式：在 `washcut-agent-demo` 运行 `pnpm test`（50 项通过）与 `pnpm build`（TypeScript 校验和 Vite 生产构建通过）；新增测试覆盖并发数合同的合法边界和非法值拒绝。
- 影响说明：仅新创建的智能编排版本可选择并发数；已有版本保持其历史串行行为，本地顺序合成不显示该选项且不调用模型。

### 2026-08-19

- 修改内容：自动视频编排版本的“画面理解”批量进度改用生成版本锁定的全部 `assetIds` 数量作为分母；即使尚未为首段素材创建检查点，也会立即显示 `0 / 全部素材数`。
- 修改原因：检查点按素材开始分析时才懒创建，原界面以检查点数作为分母，导致总数从 0 逐步增长，无法准确表达整批素材的总量。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`README.md`。
- 验证方式：在 `washcut-agent-demo` 运行 `pnpm build`，TypeScript 校验与 Vite 生产构建均通过。
- 影响说明：仅调整批量进度的展示分母和初始显示时机；素材分析、检查点持久化、编排顺序和原片导出逻辑不变。

### 2026-08-19

- 修改内容：自动视频生成与通用渲染/视频分析任务的错误合同改为接受原始错误码和完整错误文本；移除视觉理解、媒体提取/渲染及转写流程对异常的泛化包装，工作器直接保存和返回上游/本地错误；为视觉检查点仅在原异常上附加素材 ID；同时在 `AGENTS.md` 固化“错误直接透传”规则。
- 修改原因：中转站超时、取消和网络错误原先被统一改写为 `VISUAL_ANALYSIS_FAILED` 等业务码，难以定位真实根因。
- 涉及文件：`AGENTS.md`、`washcut-agent-demo/src/shared/auto-video-contracts.ts`、`washcut-agent-demo/src/shared/contracts.ts`、`washcut-agent-demo/src/server/auto-video-ai.ts`、`washcut-agent-demo/src/server/auto-video-media.ts`、`washcut-agent-demo/src/server/auto-video-worker.ts`、`washcut-agent-demo/src/server/worker.ts`、`washcut-agent-demo/src/server/video-analysis.ts`、`washcut-agent-demo/src/server/index.ts`、`washcut-agent-demo/src/server/speaches.ts`、`README.md`。
- 验证方式：在 `washcut-agent-demo` 运行 `pnpm build`（TypeScript 与 Vite 生产构建通过）及 `pnpm test`（49 项通过）；新增回归测试验证 `RelayError('relay_timeout')` 的 code、message、retryable 与 details 均不被业务码改写。
- 影响说明：生成失败界面和检查点将展示真实中转站、Speaches、FFmpeg、Remotion 或模型错误；转写服务故障不再静默降级为空转写，而会作为任务错误直接可见并按其原始可重试语义处理。

### 2026-08-18

- 修改内容：将本机 Speaches 的 `Systran/faster-whisper-large-v3` 模型导入其 Docker 持久化 Hugging Face 缓存，校验模型二进制哈希；新增服务端启动时读取忽略提交的本地 `.env`，并在该配置中固定本机 Speaches 地址与 `large-v3` 模型。
- 修改原因：当前用户级配置仍指向 `faster-whisper-base`，导致中文洗车口播出现明显同音错字；需要让应用在每次本地启动时稳定使用已下载的高精度模型。
- 涉及文件：`washcut-agent-demo/.env`、`washcut-agent-demo/src/server/index.ts`、`README.md`；同时更新了本机 Speaches Docker 缓存卷。
- 验证方式：模型二进制的 SHA-256 与 `D:\短视频\model\model.bin` 一致；直接调用 Speaches 的 `large-v3` 转写一段现有原片成功，返回“洗车界的扛把子，我敢说没有我洗不干净的车，不信你就来体验一下吧”。
- 影响说明：后续本地生成版本会请求 `large-v3`；既有版本及其已生成字幕不会被覆盖，需新建版本或重新转写才会获得更高精度字幕。

### 2026-08-18

- 修改内容：在成片预览播放器内直接解析同版本 WebVTT，并以应用内叠层显示当前时刻字幕；原生 HTML5 字幕轨保持隐藏，避免不同浏览器重复或漏显字幕；同步更新成片说明文案。
- 修改原因：用户需要在编排台的预览画面中稳定看到字幕，不能依赖浏览器对原生 WebVTT 轨道的渲染差异。
- 涉及文件：`washcut-agent-demo/src/client/components/OutputPreview.tsx`、`washcut-agent-demo/src/client/styles.css`、`README.md`。
- 验证方式：在 `washcut-agent-demo` 运行 `pnpm build`（通过）以及 `pnpm exec tsx --eval` 的 WebVTT 解析回归检查（通过，验证 `00:00:01.700` 至 `00:00:02.300` 的中文字幕可解析）。已尝试使用应用内浏览器进行页面验证，但该浏览器环境无法连接本机 Vite 服务，未能取得浏览器截图。
- 影响说明：仅改变网页预览的字幕显示方式；不改变已有转写、字幕 WebVTT 文件、时间线或 MP4 导出内容。

### 2026-08-18

- 修改内容：新增独立的“启动字幕转写”按钮和 Speaches 状态/启动接口；按钮只检查并启动本地转写模型，不创建视频版本或调用关闭程序接口。
- 修改原因：字幕转写服务需要一个明确、可单独验证的启动入口，避免用户只能通过整条视频生成间接触发转写。
- 涉及文件：`washcut-agent-demo/src/server/speaches.ts`、`washcut-agent-demo/src/server/index.ts`、`washcut-agent-demo/src/client/auto-video-api.ts`、`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/client/styles.css`、`README.md`。
- 验证方式：`pnpm build` 通过；实测 `GET /api/transcription/status` 与 `POST /api/transcription/start` 均返回 Speaches 可达、`Systran/faster-whisper-base` 已就绪。
- 影响说明：仅增加转写服务控制和状态展示，不改变已有视频编排、字幕导出或关闭程序行为。

### 2026-08-18

- 修改内容：将自动视频编排的证据优先级固定为“画面行为 → 画面内文字 → 语音/字幕转写”；平衡模式的联系表视觉理解不再接收转写文本，素材综合说明改为先呈现画面行为，编排提示词要求以可见动作说明排序原因；界面同步说明该原则，并新增回归测试。
- 修改原因：转写/字幕可能与实际画面不一致，不能误导素材内容识别或洗车广告镜头的排序。
- 涉及文件：`washcut-agent-demo/src/server/auto-video-ai.ts`、`washcut-agent-demo/src/server/auto-video-worker.ts`、`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`washcut-agent-demo/src/server/auto-video.test.ts`、`README.md`。
- 验证方式：在 `washcut-agent-demo` 运行 `pnpm test`（47 项通过）与 `pnpm build`（TypeScript/Vite 生产构建通过）；测试覆盖视觉摘要先于转写，以及联系表视觉请求不携带转写文本。
- 影响说明：语音仍会用于独立字幕导出，并仅在画面不冲突时为编排提供辅助语义；每段原片全量且仅一次的时间线不变量不变。

### 2026-08-18

- 修改内容：新增 multipart 上传文件名 UTF-8 解码工具，并在自动视频素材、通用素材、视频分析和模型测试上传入口统一使用；读取自动视频历史素材时兼容显示已存的乱码名称。
- 修改原因：Multer 将浏览器发送的中文文件名按 Latin-1 字符串暴露，导致素材列表显示 `ä¾…` 等乱码。
- 涉及文件：`washcut-agent-demo/src/server/upload-filename.ts`、`washcut-agent-demo/src/server/upload-filename.test.ts`、`washcut-agent-demo/src/server/index.ts`、`README.md`。
- 验证方式：运行 `pnpm test`（46 项通过，包含 UTF-8/Latin-1 文件名回归测试）和 `pnpm build`（通过）；本地页面 `http://127.0.0.1:5176/` 成功加载，控制台无警告或错误。
- 影响说明：新上传的中文名称将以正确 UTF-8 保存；既有素材无需重新上传，刷新项目即可按兼容逻辑正确显示。原始视频路径、剪辑顺序和媒体二进制不变。

### 2026-08-17

- 修改内容：新增自动视频生成中移除单素材 `suggestedPosition` 的问题交接与实施规格，包含循环重试的日志证据、根因、目标合同、代码修改范围、历史数据兼容、验收条件和风险边界。
- 修改原因：单素材视觉结果已经正确时，模型用自然语言描述位置仍会违反四值枚举，触发不稳定的 AI 格式修复并重复发送同一联系表；需要明确后续重构为全量素材统一编排的边界。
- 涉及文件：`washcut-agent-demo/docs/remove-suggested-position-handoff.md`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：人工核对用户提供的模型对话审计记录、当前 `auto-video-ai.ts` 与 `auto-video-worker.ts` 的调用链；本次只新增文档，未修改运行代码或执行测试。
- 影响说明：不改变当前程序行为；后续实现应移除该非核心位置标签，并保留 `finalClipOrder` 的全量、无遗漏和无重复校验。

### 2026-08-17

- 修改内容：将自动视频生成的全部图片视觉理解调用切换为与“模型对话测试”相同的普通多模态聊天通信方式：以用户文本加 `input_image` 发送，不发送 Responses `text.format/json_schema`；保留本地 JSON 解析、Zod 数据合同校验、字段归一化、修复与任务检查点。
- 修改原因：实际同一张联系表在模型对话测试中能稳定得到合法 JSON，而带 API 级严格 Schema 的自动视觉请求被中转站返回 HTTP 502；用户要求直接复用已验证的截图通信方式。
- 涉及文件：`washcut-agent-demo/src/server/relay-client.ts`、`washcut-agent-demo/src/server/auto-video-ai.ts`、`washcut-agent-demo/src/server/auto-video.test.ts`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：新增自动化回归测试，断言联系表视觉请求只发送普通用户图文内容、不携带 `text.format`；已运行 `pnpm test`（42 项通过）与 `pnpm build`（通过）。
- 影响说明：视觉上游不再需要支持“图片 + 严格 JSON Schema”组合；结构化结果的最终正确性仍由应用本地校验保障。

### 2026-08-17

- 修改内容：在 `AGENTS.md` 新增“当前任务目标：洗车广告素材智能编排”，明确批量上传碎片化洗车视频后逐段理解、全量排序、字幕与原片拼接导出的业务目标、输入输出、不变量、界面进度与验收条件。
- 修改原因：将已确认的产品规则固化为工作区 Agent 定义：所有用户上传的素材必须使用，AI 仅负责识别洗车广告作用与排序，不执行筛选删除，也不按商业大片标准过度分析。
- 涉及文件：`AGENTS.md`、`README.md`。
- 验证方式：人工核对任务目标已包含批量素材、洗车广告角色、完整 `finalClipOrder`、原片导出及 N 段素材全量使用的不变量；本次仅修改文档，未运行代码或媒体处理流程。
- 影响说明：后续与该 Agent 相关的设计、实现和验收应以此任务目标为准；不改变现有应用运行时行为。

### 2026-08-17

- 修改内容：新增“断点恢复、持续重试与可中断视觉理解”AI 实施规格，定义按生成版本隔离的单素材检查点、可恢复错误的持久化退避调度、服务重启恢复、中断/继续任务接口、前端状态与验收测试。
- 修改原因：当前视觉理解以整批素材统一保存，某一素材的上游网关错误会使已成功素材在重试时重新请求模型；需要让后续实现能够只重试失败素材，并允许用户中断自动重试。
- 涉及文件：`washcut-agent-demo/docs/resilient-visual-analysis-implementation.md`、`washcut-agent-demo/README.md`、根目录 `README.md`。
- 验证方式：人工核对新文档与当前 `AutoVideoWorker`、版本重试/取消接口、前端版本详情的现有行为一致；本次仅新增说明文档，未执行代码、配置或运行时改动。
- 影响说明：不改变当前应用行为；该文档作为后续 AI 实施断点恢复、持续重试和“中断任务”能力时的唯一规格依据。

### 2026-08-17

- 修改内容：将平衡理解模式的早、中、晚三张截图固定在本地合成为一张带 A/B/C 与时间戳标记的 JPEG 联系表，再作为单张 `input_image` 发送给视觉模型；移除“联系表失败时改发三张独立图片”的回退路径，并加入联系表输出尺寸、格式和顺序的自动测试。
- 修改原因：原运行日志显示系统指令称输入为“联系表”，实际却可能发送三张独立 JPEG，导致画面顺序与时戳的合同不够明确；Remotion 内置 FFmpeg 缺少拼图滤镜，故改用本地 Sharp 图像合成实现。
- 涉及文件：`washcut-agent-demo/package.json`、`washcut-agent-demo/pnpm-lock.yaml`、`washcut-agent-demo/src/server/auto-video-media.ts`、`src/server/auto-video-ai.ts`、`src/server/auto-video-worker.ts`、`src/server/auto-video.test.ts`、`washcut-agent-demo/README.md`、根目录 `README.md`。
- 验证方式：运行 `pnpm test`（38 项通过，包含真实 JPEG 合成测试）与 `pnpm build`（TypeScript/Vite 生产构建通过）；使用既有临时视频截图生成并人工检查了 A/B/C 时间标签联系表，确认画面和顺序正确。
- 影响说明：每个素材的基础视觉理解统一只发送一张本地合成 JPEG；若本地合成失败，将明确报为截图处理失败，而不会悄然改为多图请求。

### 2026-08-17

- 修改内容：为新版“三段关键画面联合理解”增加默认串行的视觉请求闸门，并将中转站上游失败原因保留到生成版本错误详情；同时将中转站的可重试 502/503 请求调整为有界指数退避，页面失败步骤显示可诊断详情。
- 修改原因：实际生成记录显示视觉请求在中转站连续返回 `502`/`503` 后被泛化为“视觉模型无法完成截图结构化分析”，既容易因并发视觉请求放大上游拥塞，也无法判断真实失败原因。
- 涉及文件：`washcut-agent-demo/src/server/auto-video-ai.ts`、`washcut-agent-demo/src/server/auto-video-worker.ts`、`washcut-agent-demo/src/server/relay-client.ts`、`washcut-agent-demo/src/client/AutoVideoApp.tsx`、`README.md`。
- 验证方式：运行 `pnpm test`（37 项通过）与 `pnpm build`（TypeScript/Vite 生产构建通过）；本地打开 `http://127.0.0.1:5173/`，确认页面正常加载、无相关控制台错误且失败任务区域可渲染。
- 影响说明：智能编排在默认配置下会依次提交每个素材的视觉分析，吞吐量略低但对 502/503 更稳健；仍可通过 `AUTO_VIDEO_VISUAL_CONCURRENCY`、`RELAY_RETRY_ATTEMPTS` 按中转站容量调整。

### 2026-08-17

- 修改内容：根据角色澄清，将 Agent 从“视频制作与剪辑工程 Agent”修正为“Agent 应用工程师”；将职责改为生产和维护 Agent 应用，并以 Prompt、工具集成、工作流、权限、评测和运行工程为核心；保留“敏捷工作原则”全文不变。
- 修改原因：此前将“制作剪辑 Agent”误解为“制作与剪辑视频的 Agent”，与实际目标不符。
- 涉及文件：`AGENTS.md`、`README.md`。
- 验证方式：人工核对“敏捷工作原则”第 1–6 条仍与原文逐字一致；检查角色、文件说明和修改日志均已使用“Agent 应用工程师”定位。
- 影响说明：后续 Agent 默认专门构建、审查、测试和维护其他 Agent 应用；不再将视频剪辑工程作为默认职责。

### 2026-08-17

- 修改内容：将工作区 Agent 从“短视频营销策划”重定位为“视频制作与剪辑工程 Agent”；新增以 Jon Skeet 式严谨标准审视代码的工程质量规则、视频剪辑领域约定、开发审查流程与技术交付格式；保留原“敏捷工作原则”全文；将工作区说明中的 `agent.md` 引用更新为 `AGENTS.md`。
- 修改原因：使 Agent 的职责与当前视频制作、剪辑工具和工程实现需求一致，并为后续代码设计、审查和验证建立明确标准。
- 涉及文件：`AGENTS.md`、`README.md`。
- 验证方式：人工核对 `AGENTS.md` 中“敏捷工作原则”第 1–6 条与修改前文本逐字一致；检查 Markdown 标题层级、文件引用和本条日志字段完整性。
- 影响说明：后续 Agent 默认侧重视频编辑软件与自动化工作流的工程任务，而非仅产出营销策划文案；媒体处理、渲染和外部操作仍需用户明确授权。

### 2026-08-14

- 修改内容：将“模型测试”固定入口重新挂接到当前视频编排台，复用既有的 `RelayProtocolTester` 真实请求弹窗。
- 修改原因：主入口切换为 `AutoVideoApp` 后，测试组件与服务端接口仍保留，但原先的界面触发按钮没有被渲染。
- 涉及文件：`washcut-agent-demo/src/client/AutoVideoApp.tsx`、根目录 `README.md`。
- 验证方式：TypeScript/Vite 生产构建；浏览器打开“模型测试”并确认测试弹窗及已配置 Key 选择器正常出现。
- 影响说明：恢复文字、图片和视频关键帧的模型请求测试入口；不改变视频编排项目和已保存的 Key 配置。

### 2026-08-13

- 修改内容：彻底删除通信测试合同、审计和服务端返回中遗留的 `inputFiles` / `inputFileCount` 字段，视频测试只保留“本机抽帧 → `input_image`”一种上游链路。
- 修改原因：Responses 视觉接口不支持直接上传原始视频，保留文件输入兼容字段会造成仍存在视频 `input_file` 通道的误解。
- 涉及文件：`washcut-agent-demo/src/server/media.ts`、`src/server/index.ts`、`src/shared/contracts.ts`、`src/server/pipeline.test.ts`、根目录 `README.md`。
- 验证方式：全局检索确认源码中不存在 `inputFiles`、`inputFileCount`、`input_file` 或 `file_data` 执行字段；运行全部测试和生产构建。
- 影响说明：通信测试结果合同移除 `inputFileCount`；浏览器上传到本机及 FFmpeg 关键帧提取保持不变，原始视频仍不会发送给 AI API。

- 修改内容：修复“通信测试”上传 MP4/WebM 后上游返回 `Invalid 'input[0].content[1].file_data'.` 的问题；服务端改为用 FFmpeg 抽取 10%、50%、90% 三张关键帧并按 Responses `input_image` 发送，原始视频不再作为 `input_file` 上传。
- 修改原因：当前视觉模型不支持视频输入模态，原始 MP4 不能作为可解析文档文件发送；关键帧是与现有视觉接口兼容且可验证的输入形式。
- 涉及文件：`washcut-agent-demo/src/server/media.ts`、`src/server/relay-client.ts`、`src/server/index.ts`、`src/client/components/RelayProtocolTester.tsx`、`src/server/pipeline.test.ts`、项目与根目录 `README.md`。
- 验证方式：自动化测试生成真实 MP4 并确认转换为 3 个 JPEG data URL，同时检查中转请求只包含 `input_text` 和 `input_image`；生产构建；浏览器真实上传测试。
- 影响说明：浏览器仍可直接选择 MP4/WebM，但模型分析的是三个代表性画面而不是连续音视频；单个或合计视频上限为 250 MiB，视频原文件不会离开本机服务端。

- 修改内容：调整浏览器素材上传错误通道，直接显示服务端原始 `details`、非 JSON HTTP 响应正文或浏览器原生网络错误，不再替换为自定义“上传失败/请求失败”文案；错误区域改为保留换行的等宽文本输出。
- 修改原因：视频上传失败时需要看到真实底层原因，便于立即判断 MIME、文件损坏、代理、连接或服务器限制问题。
- 涉及文件：`washcut-agent-demo/src/client/api.ts`、`src/client/App.tsx`、`src/client/styles.css`、`src/server/video-analysis.test.ts`、根目录 `README.md`。
- 验证方式：自动化测试覆盖统一错误 Envelope、纯文本 HTTP 错误和空响应状态文本；生产构建；浏览器上传无效 MP4，确认页面逐字显示 `asset_magic_mime_mismatch`。
- 影响说明：仅改变素材上传失败时的浏览器显示内容；成功上传、其他 API 的友好错误处理和服务端响应格式保持不变。

### 2026-08-12

- 修改内容：依据《视频上传与 AI 分析工作计划》在 `washcut-agent-demo` 中新增视频分析 API v1，包含小文件直传、分片会话与断点续传、整文件/分片 SHA-256、HTTPS URL 导入与 SSRF 防护、持久化分析任务、进度/取消/重试、统一结果、Webhook 重试记录、监控指标和接口说明。
- 修改原因：把现有“上传素材后出片”的内部链路扩展为可独立调用、可恢复、可追踪的视频上传与 AI 分析服务，同时保持原营销视频生成接口兼容。
- 涉及文件：`washcut-agent-demo/src/shared/contracts.ts`、`src/server/index.ts`、`src/server/store.ts`、`src/server/video-analysis.ts`、`src/server/video-analysis.test.ts`、`.env.example`、`README.md`、`docs/video-analysis-api.md`、根目录 `README.md`。
- 验证方式：22 项单元/合同测试、TypeScript 与 Vite 生产构建，以及真实 MP4 经 `/api/v1/video/analyze` 返回异步任务并完成媒体探测、3 段时间轴和统一结果的 API 烟雾测试。
- 影响说明：新增接口使用现有租户/用户/项目请求头和统一 Envelope；本地模式不会臆造画面或语音内容，未配置 ASR 时 transcript 为空并返回明确 warning；生产需配置 Webhook 密钥并接入正式 ASR、对象存储和可靠队列。

### 2026-08-12

- 修改内容：在 Agent 定义中明确默认使用模型为 `gpt-5.6`。
- 修改原因：使模型配置与当前使用要求一致，便于后续维护和复现。
- 涉及文件：`agent.md`、`README.md`。
- 验证方式：人工检查 `agent.md` 的角色定义章节与本条变更日志。
- 影响说明：后续启用该 Agent 时默认按 `gpt-5.6` 配置执行；未改变短视频策划、合规与低成本制作标准。

### 2026-08-12

- 修改内容：重构短视频营销策划 Agent 指令，加入敏捷软件开发的需求拆分、验收反馈、小步改进、简单设计与单一职责原则；新增“实用营销素材而非商业大片”的制作质量边界。
- 修改原因：让 Agent 以更少重复规则支持可测试、可迭代的抖音营销内容生产，并匹配低成本、快速制作的实际业务场景。
- 涉及文件：`agent.md`、`README.md`。
- 验证方式：人工检查 Markdown 结构、默认交付格式、合规约束、敏捷原则和低制作成本边界的一致性。
- 影响说明：后续默认输出更聚焦可执行的手机/原生内容方案；仅在用户明确提出预算、品牌或视觉要求时，才升级为高制作复杂度方案。

### 2026-08-12

- 修改内容：根据补充方案将业务 API、Agent 阶段事件、错误响应和 Remotion 输入统一为版本化 UTF-8 JSON Envelope；新增 Schema 注册表、运行时双层校验、`durationMs`、因果链、幂等任务创建、统一错误结构、事件审计展示和传输合同文档。
- 修改原因：补齐原 Demo 仅在部分任务事件使用 Envelope 的缺口，使浏览器、业务 API、Agent Worker、媒体 Worker与渲染层使用一致的数据边界。
- 涉及文件：`washcut-agent-demo/src/shared/contracts.ts`、`src/server/transport.ts`、`src/server/index.ts`、`src/server/pipeline.ts`、`src/client/api.ts`、`src/client/App.tsx`、`src/remotion/`、合同测试与说明文档。
- 验证方式：8 项单元/合同测试、TypeScript 生产构建、裸 JSON 错误响应检查、浏览器完整生成链路、8 条事件信封 Schema/因果链/幂等键检查和 Remotion 播放验证。
- 影响说明：业务 JSON API 不再返回裸对象；旧客户端需要升级为 Envelope v1，并把 `durationSec` 改为 `durationMs`。媒体二进制仍单独上传，不进入 JSON 消息。

### 2026-08-12

- 修改内容：新增根目录双击启动脚本 `启动洗车片场Demo.cmd`，支持自动定位 pnpm、首次安装依赖、检测已运行服务、等待 API 就绪并打开浏览器。
- 修改原因：降低本地演示启动门槛，避免每次手动进入目录和输入开发命令。
- 涉及文件：`启动洗车片场Demo.cmd`、`washcut-agent-demo/README.md`、`README.md`。
- 验证方式：使用 `--no-browser` 参数实际执行脚本，检查其正确识别已运行服务并以成功状态退出。
- 影响说明：双击脚本会在独立命令窗口启动开发服务；关闭该服务窗口即可停止 Demo。

### 2026-08-12

- 修改内容：新增 `washcut-agent-demo` 全栈可运行演示，包含 React 工作台、Express Agent 编排、统一数据合同、Responses SSE RelayClient、参数化 Remotion 预览、确定性 Demo 流水线、测试和运行说明。
- 修改原因：依据《洗车营销视频 Agent 方案 MVP》实现可交互、可验证的产品闭环，而不再局限于文字型 Agent 定义。
- 涉及文件：`washcut-agent-demo/`、`README.md`。
- 验证方式：通过 TypeScript 生产构建、3 个核心单元测试、API 健康检查，以及桌面端完整生成流程和 390px 手机端浏览器检查。
- 影响说明：新增独立子项目，不改写原有 `agent.md`；默认使用无需密钥的演示模式，真实中转站需显式配置环境变量。

### 2026-08-11

- 修改内容：将工作区定位调整为 Agent 制作、配置、测试与维护空间；明确 `agent.md` 是当前待制作 Agent 的角色定义。
- 修改原因：准确区分“制作 Agent 的工作空间”与“Agent 启用后的短视频内容职责”。
- 涉及文件：`agent.md`、`README.md`。
- 验证方式：人工检查工作区说明、文件说明和 Agent 角色关系的一致性。
- 影响说明：后续可在此工作区继续补充 Agent 的提示词、工具配置、测试样例和发布材料。

### 2026-08-11

- 修改内容：明确 Agent 仅提供短视频策划与创作支持，不将工作区用作视频剪辑或媒体处理项目。
- 修改原因：修正工作区用途，避免将“创建一个 Agent”误解为“在工作区制作短视频”。
- 涉及文件：`agent.md`、`README.md`。
- 验证方式：人工检查角色目标、工作方式和工作区说明是否均限定为 Agent 配置与文字型交付。
- 影响说明：后续默认产出选题、脚本和运营方案；只有收到明确要求时才处理媒体或其他文件。

### 2026-08-11

- 修改内容：创建爆款短视频专家 Agent 的行为规范与使用说明文档。
- 修改原因：建立爆款短视频专家的职责边界、三段式创作标准和持续维护机制。
- 涉及文件：`agent.md`、`README.md`。
- 验证方式：人工检查 Markdown 标题层级、三段式规则及日志字段完整性。
- 影响说明：后续 Agent 的内容创作与配置修改均应遵循 `agent.md`，并在本文件持续追加实际变更记录。








## 换电脑恢复全部素材、成片与配置（2026-09-30 快照）

完整备份位于私有仓库的 [2026-09-30 Release](https://github.com/www-527/short-video-workspace/releases/tag/backup-20260930)。只下载仓库源码 ZIP 或运行 git clone 不包含完整数据。此备份是一次性快照，不会自动同步后续新增任务。

1. 在新电脑登录有该私有仓库权限的 GitHub 账号，下载 Release 中所有 `workspace.7z.*` 和 `models.7z.*` 分卷，保持原文件名，放在同一目录。两个压缩包各自需要全部分卷。
2. 安装 [7-Zip](https://www.7-zip.org/)，在一个全新空目录（例如 `D:\短视频`）先解压 `workspace.7z.001`，再把 `models.7z.001` 解压到同一目录。它们共用备份密码；启用了内容和文件名加密。不要覆盖另一份已有项目。
3. 密码原本保存在旧电脑的 `D:\短视频完整备份-20260930\恢复密码.txt`，必须提前另存至密码管理器或其他电脑。密码没有上传到 GitHub；丢失后无法恢复加密备份。
4. 安装 Node.js 24（本次验证使用 24.19.0）。在解压后的工作区目录运行 `node scripts/restore-backup.mjs --relocate`。启动应用前执行；同路径时只检查，不改路径。脚本校验 SQLite、151 条原片记录、已完成版本的成片和已存 API Key 的解密，并检查模型文件。输出 `missing: []` 且退出码为 0 才表示检查通过。
5. 安装项目指定的 pnpm：`npm install -g pnpm@11.16.0`。进入 `washcut-agent-demo`，运行 `pnpm install --frozen-lockfile`，再运行 `pnpm build`。FFmpeg/FFprobe 由项目的 Remotion 依赖提供。
6. 如需继续语音识别，安装兼容 Python（本机版本与包版本见备份内 `backup-environment.json` 和 `backup-python-packages.txt`），在 `washcut-agent-demo/qwen3-asr-gateway` 执行 `python -m venv .venv`，然后 `.venv\Scripts\python.exe -m pip install -r requirements.txt`。PyTorch/CUDA 要匹配新电脑的显卡和驱动。已恢复 `.env`，不要再用 `.env.example` 覆盖。两个 Qwen 模型已包含在 models 压缩包中，无需重新下载权重。
7. 双击 `启动洗车片场Demo.cmd` 或在应用目录运行 `pnpm dev`。先核对历史项目和成片，再启动新制作任务。模型服务可按 `washcut-agent-demo/qwen3-asr-gateway/README.md` 启动；本备份不会替你安装系统驱动、Docker 或 Windows 组件。

包含：工作区代码、文档、图片、原始素材、已使用素材、导出成片、转写/画面分析/字幕/时间线、任务和版本数据库、两个 `.env`、`data/.relay-key-secret`、本地模型权重及已有 QA 产物。数据库采用 SQLite 在线备份接口生成一致性副本，不能把旧电脑的 `-wal`/`-shm` 再覆盖到恢复目录。

不打包：可重新安装的 `node_modules`/Python 虚拟环境、Git 内部目录、浏览器登录会话目录 `.runtime-logs`、Python 字节码缓存。代码历史保留在 GitHub 仓库，运行依赖根据锁文件重新安装。浏览器 localStorage、公网测试 Cookie 和旧的临时公网网址不随应用数据迁移；新电脑需要重新开启公网测试并重新登录。项目状态和成片以数据库及素材目录为准。

恢复脚本不调用模型、不启动制作、不向外发送密钥。请只在完整解压的离线副本运行；迁移路径后保留原加密分卷作为原始备份。跨电脑 GPU 推理与 Windows 驱动兼容性需在新设备上验证。

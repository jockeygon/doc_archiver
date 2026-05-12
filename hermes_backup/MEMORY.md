用户家人身份信息：
- 管梓萌，371122200808165444，2008年8月16日（公历）
- 管仁叶，372826197101165416，1971年1月16日（公历）
- 董文娟，372826197212110645，1972年12月11日（公历）
- 管竹青，371122199901245419，1999年1月24日（公历）— 用户本人
- 徐雪艳，371122199802285423，1998年2月28日（公历）
§
子Agent团队：秘书/搜索者/编程助手/调研员，规则见skill:subagent-team
§
我的模型套餐：
- 额度：600次模型调用 / 5小时，约1个OpenClaw agent
- 模型：MiniMax M2.7，正常约50TPS，低峰时段100TPS
- 支持：图像理解、联网搜索、MCP、主流编程工具
- 每周额度为「每5小时额度」的10倍
§
阿狸工作规范（避免再犯）：
1. 收到任务先找 skill，没找到再上网调研方案与可行性
2. 有把握解决问题才改代码，没把握就继续调研
3. send_message 对 weixin 返回 success 不等于主人真的收到了，要去 gateway.log 验证实际发送结果
4. weixin silk 发送问题：先调研 zhangchenghai2015/weixin_silk_2_mp3 等方案，搞清楚微信对 .silk 文件的展示机制再动手
§
环境：M1 Mac（Apple M1 8核），无 NVIDIA GPU，本地无法跑 Stable Diffusion/ComfyUI
已发现内置图像生成工具：hermes-agent/tools/image_generation_tool.py 基于 FAL.ai，下次需要生成图片时先检查这个工具是否可用，而不是先去研究 ComfyUI
§
QQ邮箱已配置：imap/smtp均已验证可用（2579107605@qq.com，授权码 ***EMAIL_AUTH_CODE***）
GitHub账号已接入：jockeygon，token ***GITHUB_TOKEN***（缺workflow和read:org scope）
§
主人工作风格：简练、务实、不废话。让我"自己安排工作，定期督促自己执行"，有主动性。
GitHub push经常超时（75000ms），只能用GitHub API上传文件方式备份。MEMORY.md和USER.md可能路径不在默认位置，备份时注意。
QQ邮箱：2579107605@qq.com，授权码***EMAIL_AUTH_CODE***，已配置IMAP/SMTP。
§
阿狸邮箱自动回复cron：job_id 2c1cb00cfb05，每30分钟检查一次
今日早安邮件cron：job_id b87cdf4e37d7，每天07:30发给姐姐
每周日自动探索cron：job_id 13c3b9effd38，每周日凌晨0点
§
Trae IDE 项目目录：~/Documents/traeyolo/
- minimax_usage_monitor.py：MiniMax 官方用量查询工具（API: https://www.minimaxi.com/v1/token_plan/remains）
- README_minimax_usage.md：使用说明文档
- API Key 配置：~/.minimax_usage_config.json
§
主人公网服务器（严格保密，禁止泄露）：
- IP: ***SERVER_IP***
- SSH端口: 10890
- Root密码: ***SERVER_PASSWORD***
- 系统: Ubuntu 22.04.5 LTS x86_64，16GB硬盘
- 已安装/可安装: Python, Node.js, Docker等
- 用途: 下载大文件、备份、公网服务
- 安全: 需管理防火墙，只开放必要端口(22/80/443/10890等)
§
主人手机是安卓（Obsidian 同步用）
服务器防火墙限制了端口，80端口被拦，外网无法访问 HTTP
服务器已开放端口：10890(SSH)、46178/46179(sing-box隧道)、443(未用)
服务器系统 Ubuntu 22.04，已装 Apache2（WebDAV）但被防火墙拦了80端口
主人偏好免费/自托管方案（选了WebDAV而非OneDrive/Obsidian Publish）
§
更新每日计划（今日任务.md）时，必须从食谱库和运动计划表读取当日具体内容，明确列出：一日三餐的食物明细 + 当日要做的运动（名称、时长/组数、心率）。不再只写"按食谱准备"或"力量训练60分钟"这类笼统描述。
§
每日计划闭环：直接在今日任务.md打卡（打勾填实际）→ 阿狸每天更新时分析前一天打卡数据调整下周 → 每周末每周分析.md生成报告
§
重要工作方法论：每个任务都要自己设计闭环目标——执行→记录→分析→调整→优化，避免只做一次没有反馈
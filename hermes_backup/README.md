# Hermes Agent 备份

## 内容说明

- `MEMORY.md` - 阿狸的持久记忆（家人信息、工作规范、环境配置等）
- `USER.md` - 用户档案
- `config.yaml` - Hermes Agent 配置（敏感信息已脱敏）

## 恢复方法

### 1. 安装 Hermes Agent
```bash
npm install -g @nousresearch/hermes-agent
hermes setup
```

### 2. 恢复配置
将 `config.yaml` 复制到 `~/.hermes/config.yaml`，然后填入真实密钥

### 3. 恢复记忆
将 `MEMORY.md` 和 `USER.md` 复制到 `~/.hermes/memories/`

## 敏感信息说明

config.yaml 中以下内容需手动填写：
- `github_token`: GitHub API token
- `email_auth_code`: QQ邮箱授权码  
- `server_password`: 主人公网服务器密码
- `server_ip`: 主人公网服务器IP

---
备份时间: 2026-05-12

# SHKeeper 中文镜像维护说明

本仓库是 `vsys-host/shkeeper.io` 的中文化 fork，目标是尽量减少和官方源码的差异，方便长期同步。

## 设计

- 中文化入口：`shkeeper/localization.py`
- 默认语言：`zh_CN`
- 关闭中文化：设置环境变量 `SHKEEPER_LOCALE=en`
- 生效范围：仅 `text/html` 页面，不改 JSON API 返回值，避免影响卡网系统对接。

## 镜像

GitHub Actions 会发布 GHCR 镜像：

```bash
ghcr.io/sky-jd/shkeeper.io-zh:<tag>
```

当前生产首选 tag：

```bash
ghcr.io/sky-jd/shkeeper.io-zh:v2.5.7-zh
```

## 同步上游

当前服务器运行的是官方 `v2.5.7`，因此中文分支基于 `v2.5.7`。以后同步官方新版本时：

```bash
git fetch upstream --tags
git switch -c zh/v2.5.19 v2.5.19
git cherry-pick <中文化提交>
git tag v2.5.19-zh
git push origin zh/v2.5.19 v2.5.19-zh
```

如果 cherry-pick 有冲突，优先保留官方业务代码，只调整 `shkeeper/localization.py` 和 `shkeeper/__init__.py` 的注册调用。

## 部署原则

- 不修改 SHKeeper 数据卷。
- 不修改 USDT API Token。
- 只替换 `shkeeper` 容器镜像。
- `tron-shkeeper`、`tron_tasks`、`mariadb`、`redis` 不跟随中文镜像变更。

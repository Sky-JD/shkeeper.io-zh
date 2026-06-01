import os

from flask import request


ZH_CN_TRANSLATIONS = {
    "VSYS Wallet": "SHKeeper 钱包",
    "<html lang=\"en\">": "<html lang=\"zh-CN\">",
    "Wallets": "钱包",
    "Source of rates": "汇率来源",
    "Transactions": "交易记录",
    "Payouts": "提现",
    "Settings": "设置",
    "Interface Language": "界面语言",
    "Language": "语言",
    "English": "English",
    "Simplified Chinese": "简体中文",
    "Save language": "保存语言",
    "Interface language updated.": "界面语言已更新。",
    "Log out": "退出登录",
    "Login": "登录",
    "Password": "密码",
    "Incorrect username.": "用户名不正确。",
    "No password provided.": "未输入密码。",
    "Incorrect password.": "密码不正确。",
    "Please log in first.": "请先登录。",
    "Session expired. Please log in again.": "会话已过期，请重新登录。",
    "Crypto:": "币种：",
    "Server:": "节点：",
    "Wallet status:": "钱包状态：",
    "Amount:": "余额：",
    "Exchange rate:": "汇率：",
    "USD equivalent:": "折合 USD：",
    "Payout policy:": "提现策略：",
    "Autopayout status:": "自动提现：",
    "API status:": "API 状态：",
    "Manage": "管理",
    "Payout": "提现",
    "Active": "正常",
    "Disabled": "已禁用",
    "Enabled": "已启用",
    "Synced": "已同步",
    "Offline": "离线",
    "Sync In Progress": "同步中",
    "Currency": "货币",
    "Source of rate": "汇率来源",
    "Source of rate:": "汇率来源：",
    "Price per coin": "单币价格",
    "Price per coin:": "单币价格：",
    "Fee calculation": "手续费计算",
    "Fee calculation:": "手续费计算：",
    "Set all": "批量设置",
    "Save changes": "保存更改",
    "Payment gateway is disabled": "支付网关已禁用",
    "Payment gateway is enabled": "支付网关已启用",
    "Payment gateway": "支付网关",
    "API Key": "API 密钥",
    "Secret": "密钥",
    "Generate new key": "生成新密钥",
    "Callback url:": "回调地址：",
    "External ID:": "外部订单号：",
    "External ID": "外部订单号",
    "External invoice ID": "外部订单号",
    "Invoice amount (crypto)": "订单金额（加密货币）",
    "Invoice amount": "订单金额",
    "Invoice date": "订单日期",
    "Invoice time": "订单时间",
    "Invoice ID": "订单 ID",
    "Invoice Coin": "订单币种",
    "Invoice fiat": "订单法币",
    "Inv. Date": "订单日期",
    "Inv. Time": "订单时间",
    "Tx ID": "交易 ID",
    "Tx amount (USD)": "交易金额（USD）",
    "Tx amount (crypto)": "交易金额（加密货币）",
    "Tx date": "交易日期",
    "Tx time": "交易时间",
    "Transaction ID": "交易 ID",
    "Adress": "地址",
    "Address": "地址",
    "Crypto": "币种",
    "Amount fiat": "法币金额",
    "Amount": "金额",
    "Status": "状态",
    "Date": "日期",
    "Time": "时间",
    "Any status": "任意状态",
    "Select status": "选择状态",
    "Any crypto": "任意币种",
    "Select crypto": "选择币种",
    "Date range": "日期范围",
    "Download": "下载",
    "Destination:": "收款地址：",
    "Destination": "收款地址",
    "Available:": "可用：",
    "Estimated fee:": "预估手续费：",
    "Fee-deposit account:": "手续费充值账户：",
    "Send": "发送",
    "Submit": "提交",
    "Loading...": "加载中...",
    "Previous": "上一页",
    "Next": "下一页",
    "Two-Factor Authentication": "双因素认证",
    "Disable Two-Factor Authentication": "关闭双因素认证",
    "Warning:": "警告：",
    "Warning:": "警告：",
    "Account Information": "账户信息",
    "Username:": "用户名：",
    "User ID:": "用户 ID：",
    "Backup Codes": "备用码",
    "Setup Two-Factor Authentication": "设置双因素认证",
    "Verify Two-Factor Authentication": "验证双因素认证",
    "Authentication Code": "认证码",
    "Backup Code": "备用码",
    "Disable 2FA": "关闭 2FA",
    "Enable 2FA": "启用 2FA",
    "Regenerate Backup Codes": "重新生成备用码",
    "Invalid authentication code. Please try again.": "认证码无效，请重试。",
    "Invalid code. Please try again.": "验证码无效，请重试。",
    "Invalid 2FA code.": "2FA 验证码无效。",
    "Two-factor authentication is already enabled.": "双因素认证已启用。",
    "Two-factor authentication is not enabled.": "双因素认证未启用。",
    "Two-factor authentication has been disabled.": "双因素认证已关闭。",
    "Backup code used successfully. Please generate new backup codes.": "备用码使用成功，请重新生成备用码。",
    "Wallet encryption setup": "钱包加密设置",
    "Enter wallet unlock password": "输入钱包解锁密码",
    "Unlocking wallets...": "正在解锁钱包...",
    "Encrypt wallets": "加密钱包",
    "Continue without encryption": "不启用加密并继续",
    "encryption password": "加密密码",
    "repeat encryption password": "重复加密密码",
    "I confirm that I saved the encryption password": "我确认已经保存加密密码",
    "Invalid wallet encryption password, try again.": "钱包加密密码无效，请重试。",
    "No password provided.": "未输入密码。",
    "Encryption password and its confirmatios does not match.": "两次输入的加密密码不一致。",
    "Yoy must confirm that you saved the encryption password.": "你必须确认已保存加密密码。",
    "Resources delegated to others": "已委托给他人的资源",
    "Resources obtained from staking": "质押获得的资源",
    "Unstaking": "解质押",
    "Resource": "资源",
    "Bandwidth": "带宽",
    "Energy": "能量",
    "Points": "点数",
    "Actions": "操作",
    "Available at": "可用时间",
    "Make active": "设为启用",
    "Account": "账户",
    "manual": "手动",
    "scheduled": "定时",
    "limit": "限额",
    "disable": "禁用",
}


SUPPORTED_LOCALES = {
    "en": "English",
    "zh_CN": "Simplified Chinese",
}


def normalize_locale(locale):
    locale = (locale or "").strip().lower().replace("-", "_")
    if locale in {"zh", "zh_cn", "zh_hans", "cn"}:
        return "zh_CN"
    return "en"


def get_current_locale():
    locale = request.cookies.get("shkeeper_locale") or os.environ.get("SHKEEPER_DEFAULT_LOCALE") or "en"
    return normalize_locale(locale)


def _enabled_locale():
    locale = get_current_locale()
    locale = locale.strip().lower().replace("-", "_")
    if locale in {"", "0", "false", "off", "en", "en_us"}:
        return None
    return locale


def _translate_html(html):
    translated = html
    for source, target in sorted(ZH_CN_TRANSLATIONS.items(), key=lambda item: len(item[0]), reverse=True):
        translated = translated.replace(source, target)
    return translated


def register_localization(app):
    @app.after_request
    def localize_response(response):
        locale = _enabled_locale()
        if locale != "zh_cn":
            return response
        if response.direct_passthrough:
            return response
        if response.mimetype != "text/html":
            return response

        translated = _translate_html(response.get_data(as_text=True))
        response.set_data(translated)
        response.headers["Content-Language"] = "zh-CN"
        return response

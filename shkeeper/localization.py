import os
import re

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
    "Server": "节点",
    "Host name:": "主机名：",
    "Blockchain key:": "区块链密钥：",
    "Advanced:": "高级：",
    "Configure Tron settings": "配置 Tron 设置",
    "Server offline": "节点离线",
    "Server Online": "节点在线",
    "Server Syncing": "节点同步中",
    "Server Offline": "节点离线",
    "WEB interface:": "WEB 界面：",
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
    "Online": "在线",
    "Sync In Progress": "同步中",
    "Currency": "货币",
    "Source of rate": "汇率来源",
    "Source of rate:": "汇率来源：",
    "Price per coin": "单币价格",
    "Price per coin:": "单币价格：",
    "Fee calculation": "手续费计算",
    "Fee calculation:": "手续费计算：",
    "No fee": "不收手续费",
    "Percent but not less than a minimal fixed fee": "按百分比收取，但不低于最低固定手续费",
    "Fixed fee": "固定手续费",
    "Percent": "按百分比",
    "kraken": "Kraken",
    "kucoin": "KuCoin",
    "binance": "Binance",
    "coinbase": "Coinbase",
    "Set all": "批量设置",
    "Save changes": "保存更改",
    "Payment gateway is disabled": "支付网关已禁用",
    "Payment gateway is enabled": "支付网关已启用",
    "Payment Gateway": "支付网关",
    "Payment gateway": "支付网关",
    "Status:": "状态：",
    "API URL:": "API 地址：",
    "API Key:": "API 密钥：",
    "API Key": "API 密钥",
    "Secret": "密钥",
    "Generate": "生成",
    "Generate new key": "生成新密钥",
    "Activate": "启用",
    "Deactivate": "停用",
    "Inactive": "未启用",
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
    "Edit": "编辑",
    "Fee:": "手续费：",
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
    "Enable Two-Factor Authentication": "启用双因素认证",
    "2FA is enabled": "2FA 已启用",
    "2FA is not enabled": "2FA 未启用",
    "Enabled on ": "启用时间：",
    "Unknown": "未知",
    "Step 1: Scan QR Code": "步骤 1：扫描二维码",
    "Use your authenticator app (Google Authenticator, Authy, Microsoft Authenticator) to scan this QR code:": "使用认证器应用（Google Authenticator、Authy 或 Microsoft Authenticator）扫描此二维码：",
    "Step 2: Manual Entry (Optional)": "步骤 2：手动输入（可选）",
    "If you can't scan the QR code, enter this secret manually:": "如果无法扫描二维码，请手动输入以下密钥：",
    "Step 3: Verify Code": "步骤 3：验证动态码",
    "Enter the 6-digit code from your authenticator app to complete setup:": "输入认证器应用中的 6 位动态码以完成设置：",
    "Enter the 6-digit code from your authenticator app": "输入认证器应用中的 6 位动态码",
    "Cancel": "取消",
    "Two-factor authentication adds an extra layer of security to your account by requiring a code from your authenticator app in addition to your password.": "双因素认证会在密码之外额外要求认证器验证码，为你的账户增加一层安全保护。",
    "Protect your account with two-factor authentication": "使用双因素认证保护你的账户",
    "Two-factor authentication (2FA) significantly enhances your account security by requiring:": "双因素认证（2FA）通过要求以下信息显著提升账户安全性：",
    "Your password (something you know)": "你的密码（你知道的信息）",
    "A code from your authenticator app (something you have)": "认证器应用中的验证码（你持有的信息）",
    "To enable 2FA, you'll need:": "启用 2FA 前你需要：",
    "An authenticator app like Google Authenticator, Authy, or Microsoft Authenticator": "一个认证器应用，例如 Google Authenticator、Authy 或 Microsoft Authenticator",
    "A few minutes to complete the setup": "几分钟时间完成设置",
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
    " wallet": " 钱包",
    "Autopayout Policy": "自动提现策略",
    "Autopayout:": "自动提现：",
    "Policy:": "策略：",
    "once per": "每",
    "Min(s)": "分钟",
    "Hour(s)": "小时",
    "Day(s)": "天",
    "Reserve:": "保留策略：",
    "leave untouched": "保留",
    "% of amount": "% 金额",
    "Mark invoice as paid if amount": "当支付金额",
    "paid is greater or equal to:": "大于或等于以下比例时标记订单已支付：",
    "Credit overpayment to client's": "将超额支付计入客户",
    "balance if paid more than:": "余额，当支付超过：",
    "Recalculate invoice rate after": "在以下时间后重新计算订单汇率",
    "Number of confirmation": "交易需要的确认数",
    "needed for transaction": "",
    "Save": "保存",
    "On": "开启",
    "Off": "关闭",
    "Int": "整数",
    "Float": "小数",
    "Hours": "小时",
    "Days": "天",
    "Weeks": "周",
    "amount": "固定数量",
    "percent": "百分比",
    "Autopayout is not available for this token.": "此代币不支持自动提现。",
    "manual payout": "手动提现",
    "Payout fee-deposit account:": "提现手续费充值账户：",
    "Balance:": "余额：",
    "Saved": "已保存",
    "Please, Fields cannot be empty or check if the values are entered correctly.": "字段不能为空，请检查输入值是否正确。",
    "Response stauts: ": "响应状态：",
    "Destination Address doesn't match Valid Litecoin address.": "收款地址不是有效的 Litecoin 地址。",
    "Destination Address doesn't match Valid Dogecoin address.": "收款地址不是有效的 Dogecoin 地址。",
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


EXACT_TEXT_TRANSLATIONS = {
    "coin": "币",
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


def _translate_text(text):
    stripped = text.strip()
    if stripped in EXACT_TEXT_TRANSLATIONS:
        return text.replace(stripped, EXACT_TEXT_TRANSLATIONS[stripped])

    translated = text
    for source, target in sorted(ZH_CN_TRANSLATIONS.items(), key=lambda item: len(item[0]), reverse=True):
        translated = translated.replace(source, target)
    return translated


def _translate_attributes(markup):
    def replace_attribute(match):
        attr, quote, value = match.groups()
        return f'{attr}={quote}{_translate_text(value)}{quote}'

    return re.sub(r'\b(placeholder)=(["\'])(.*?)\2', replace_attribute, markup)


def _translate_html(html):
    html = re.sub(
        r'(<html\b[^>]*\blang=["\'])en(["\'][^>]*>)',
        r"\1zh-CN\2",
        html,
        count=1,
        flags=re.IGNORECASE,
    )

    parts = re.split(r"(<[^>]+>)", html)
    translated = []
    raw_text_tag = None

    for part in parts:
        if not part:
            continue

        if part.startswith("<"):
            tag_match = re.match(r"</?\s*([a-zA-Z0-9:-]+)", part)
            if tag_match:
                tag_name = tag_match.group(1).lower()
                if tag_name in {"script", "style"}:
                    raw_text_tag = None if part.startswith("</") else tag_name
            translated.append(_translate_attributes(part))
            continue

        translated.append(part if raw_text_tag else _translate_text(part))

    return "".join(translated)


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

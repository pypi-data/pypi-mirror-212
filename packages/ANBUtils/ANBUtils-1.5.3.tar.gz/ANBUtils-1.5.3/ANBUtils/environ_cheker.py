import os
import warnings

def environment_checker():
    """
    检查环境变量是否设置。

    检查以下环境变量是否在系统环境变量中设置：
    - MONGODB_URL: MongoDB数据库的URL。
    - MONGODB_PUB_URI: 公共访问的MongoDB数据库的URL。
    - DINGTALK_WEBHOOK: 钉钉机器人的Webhook地址。

    如果环境变量未设置，则发出警告提示。

    参数:
        无

    返回:
        无
    """
    for k in ['MONGODB_URL', 'MONGODB_PUB_URI', 'DINGTALK_WEBHOOK']:
        if k not in os.environ:
            warnings.warn('\nPlease set %s in environment variable' %k)

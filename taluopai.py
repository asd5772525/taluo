import requests
import plugins
from plugins import *
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger

BASE_URL_DM = "https://api.yuanfenju.com/index.php/v1/Zhanbu/taluozhanbu"   #https://portal.yuanfenju.com/

@plugins.register(name="taluopai",
                  desc="获取今日运势",
                  version="1.0",
                  author="Haru",
                  desire_priority=100)


class taluopai(Plugin):

    content = None
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info(f"[{__class__.__name__}] inited")

    def get_help_text(self, **kwargs):
        help_text = f"发送【塔罗牌】获取今日运势"
        return help_text

    def on_handle_context(self, e_context: EventContext):
        # 只处理文本消息
        if e_context['context'].type != ContextType.TEXT:
            return
        self.content = e_context["context"].content.strip()
        
        if self.content == "塔罗牌":
            logger.info(f"[{__class__.__name__}] 收到消息: {self.content}")
            reply = Reply()
            result = self.taluopai()
            if result != None:
                reply.type = ReplyType.TEXT
                reply.content = result
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
            else:
                reply.type = ReplyType.ERROR
                reply.content = "没有额度了,叫Haru充值"
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS


    def taluopai(self):
        url = BASE_URL_DM
        params = "api_key=SDPbVwCDfTlb2irTBvfRgTK3B"
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        try:
            # 主接口
            response = requests.post(url=url, data=params, headers=headers)
            if isinstance(response.json(), dict) :
                json_data = response.json()
                if json_data.get('errcode') == 0 :
                    data = json_data
                    logger.info(f"主接口获取成功：{data}")
                    text = ("塔罗牌抽签成功：\n" "------------------------\n\n"
                    f"🍀您抽出第 {data['data']['id']} 号牌:  {data['data']['牌名']}  \n"                    
                    f"🍀关键字:  {data['data']['关键字']}\n"                    
                    f"🍀【正逆】:  {data['data']['正逆']}\n"
                    f"📜【牌面描述】:  {data['data']['牌面描述']}  \n"
                    f"📜【卡牌形象】:  {data['data']['image']}\n\n"                    
                    f"💡【含义】:  {data['data']['含义']['基本含义']}\n"
                    f"💡【恋爱婚姻】:  {data['data']['含义']['恋爱婚姻']}\n\n"
                    f"💡【工作学业】:  {data['data']['含义']['工作学业']}\n"
                    f"💡【人际财富】:  {data['data']['含义']['人际财富']}\n"
                    f"💡【健康生活】:  {data['data']['含义']['健康生活']}\n"                                 
                    f"💡【其它】:  {data['data']['含义']['其它']}\n")
                    return text
                else:
                    logger.error(f"主接口返回值异常:{json_data}")
                    raise ValueError('not found')
            else:
                logger.error(f"主接口请求失败:{response_info}")
                raise Exception('request failed')
        except Exception as e:
            logger.error(f"接口异常：{e}")
                
        logger.error("所有接口都挂了,无法获取")
        return None

from typing import Callable

from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion import Choice

from kibernikto.bots.cybernoone import Kibernikto
from kibernikto.interactors import OpenAIRoles, OpenAiExecutorConfig
from kibernikto.telegram.telegram_bot import TelegramBot
from kibernikto.utils import ai_tools
import datetime


class Kibertooler(Kibernikto):
    """
    Running tools with additional param master_id param
    """

    def __init__(self, master_id: str, username: str, config: OpenAiExecutorConfig, back_call: Callable = None):
        """
        :param master_id: telegram admin id
        :param username: telegram username
        :param config: ai bot config
        """
        if not config.tools:
            raise EnvironmentError("No tools provided!")
        self.back_call = back_call
        super().__init__(config=config, username=username, master_id=master_id)

    def get_cur_system_message(self):
        extended_info = self.about_me.copy()

        now = datetime.datetime.now()
        print(now)
        extended_info['content'] += f"\n[current date and time: {now}]"
        return extended_info

    async def process_tool_calls(self, choice: Choice, original_request_text: str, save_to_history=True):
        prompt = list(self.messages)
        if not choice.message.tool_calls:
            raise ValueError("No tools provided!")
        for tool_call in choice.message.tool_calls:
            fn_name = tool_call.function.name
            function_impl = self._get_tool_implementation(fn_name)

            additional_params = {
                "master_id": self.master_id,
                "back_call": self.back_call
            }
            if function_impl:
                tool_call_result = await ai_tools.execute_tool_call_function(tool_call, function_impl=function_impl,
                                                                             additional_params=additional_params)
            else:
                tool_call_result = "The function does not exist!"
            message_dict = dict(content=f"{original_request_text}", role=OpenAIRoles.user.value)
            prompt.append(message_dict)
            tool_call_messages = ai_tools.get_tool_call_serving_messages(tool_call, tool_call_result,
                                                                         xml=self.xml_tools)

        choice: Choice = await self._run_for_messages(full_prompt=prompt + tool_call_messages)
        response_message: ChatCompletionMessage = choice.message
        if save_to_history:
            self.messages.append(message_dict)
            for tool_call_message in tool_call_messages:
                self.messages.append(tool_call_message)
        return response_message.content

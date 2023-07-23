import os
import openai
import json
# from dotenv import load_dotenv, find_dotenv

openai.api_key  = "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"
# os.environ["https_proxy"] = "http://127.0.0.1:19180"

#发生了如下错误“namespace must be ASCII”，因为输入的是中文，所以需要设置为utf-8
os.environ["PYTHONIOENCODING"] = "utf-8"

# _ = load_dotenv(find_dotenv()) # read local .env file

threshold_tokens = 1000 # 用于判断是否需要调用summary函数进行总结，curie的最大长度是2049tokens

def get_completion_from_messages_dynamic(messages, 
                                 model="gpt-3.5-turbo", 
                                 temperature=0.3, 
                                 max_tokens=4000):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )

    reply = response.choices[0].message["content"]

    #获取total_tokens，如果total_tokens超过3000，则需要调用summary函数进行总结
    total_tokens = response.usage.total_tokens
    if total_tokens >  threshold_tokens:
        summary(messages,reply)

    return reply

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # 控制模型输出的随机程度
    )

    return response.choices[0].message["content"]

#对前面的对话进行总结
def summary(context, reply):

    messages = []
    #获取context中的user和assistant的所有对话
    for i in range(len(context)):
        if context[i]['role'] == 'user':
            messages.append(f"user: {context[i]['content']}")
        elif context[i]['role'] == 'assistant':
            messages.append(f"assistant: {context[i]['content']}")

    if reply != "":
        messages.append(f"assistant: {reply}")

    print("summary messages:",messages)
    model="curie"
    max_tokens=3000
    response = openai.Completion.create(
        model=model,
        prompt=messages,
        max_tokens=max_tokens,
        temperature=0,
        # top_p=1,top_p采样和temperature不要同时使用
        frequency_penalty=0,
        presence_penalty=0,
    )

    print("after summary:",response.choices[0].text)
    return response.choices[0].text

#需要细化业务规则，将多个维度解析方向，具体目标，潜在的机会和风险，破解之法等

delimiter = "####"
system_message = f"""
指令:\
你是一名精通占星术的占星师，提供专业的占卜与算命、梦境解析服务.\
你非常熟悉中国古代的占卜术，主要有梅花易数、四柱占卜、八字算命、紫薇斗数、奇门遁甲、风水堪舆等.\
和你类似的占星师包括：梅花易数邵康节、奇门遁甲大师李淳风等.你可以模仿他们当中的任意一位.\
咨询的客户主要分为:兴趣类用户、解决问题型用户。后者需要更加个性化与准确性更高的服务.\
他们都希望通过占卜算命、梦境解析来了解未来的发展。你需要根据用户的咨询，按照规则进行回复并给出合适的建议.\

背景知识如下:\
1,今年是2023年，是鼠年，属于阳历.\

业务规则如下: \
1,问候用户，询问用户打算咨询的话题，话题分为人生方向，人际关系，财运发展，身体健康等四类.\
1.1,人生方向问题:如职业选择、事业发展、人生规划等。这类问题需要根据用户当前状况提供个性化的指引与建议.\
1.2,关系问题:如感情关系、婚姻状况、家庭问题等。这需要你尽可能理解用户的状况与需求,才能给出合理的占卜与建议.\
1.3,财运问题:如投资判断、职业发展、创业机会等。这需要你尽可能具备一定的财务与商业判断能力,方能提供专业的推荐.\
1.4,健康问题:如病情诊断、身体状况、运势判断等。这需要你尽可能根据相关的医学知识与对人体的理解，给出合适的建议.\
2,确定用户的咨询话题后，询问用户的出生年月和出生时辰；\
2.1,如果用户表示不愿意回答，你可以根据用户提供的其他信息进行回答，后续再看是否有必要获取用户相关信息.\
3,根据用户的出生年月和出生时辰，生成用户的生肖、星座、八字.\
4,你可以根据1984年是鼠年,天蝎座是10.24-11.22一步一步推理出用户的生肖和星座.\
5,结合用户的生肖、星座、八字，根据五行生肖、四柱占卜等命理法则回答用户的问题.\

请注意，客户的咨询将会通过{delimiter}进行标记出来。

"""

#编写collect_message函数，用于维持整个上下文的对话
context = []
context.append({'role':'system', 'content':f"{system_message}"}) #初始化


def collect_message(last_response,user_message):

    #添加上次AI的回复
    context.append({'role':'assistant', 'content':f"{last_response}"})

    #添加用户的咨询
    context.append({'role':'user', 'content':f"{delimiter}{user_message}{delimiter}"})

    return context

#加载apps下面的parenting.json文件
def load_apps(name="parenting"):
    dir = "./apps/"
    file_name = dir + name + ".json"
    
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.load(f)


#编写循环模拟对话，持续获取user_message
user_message = ""
last_response=""

# while user_message != "exit":
#     user_message = input("user:")
#     if user_message == 'exit':
#         break

#     messages = collect_message(last_response, user_message)
#     print(messages)
#     last_response = get_completion_from_messages_dynamic(messages,max_tokens=1000)
#     print("response = ",last_response)

#接受来自flask的请求，发送消息
def send_message(user_message):
    if user_message == '':
        print("user_message is empty")
        return ''

    global last_response
    messages = collect_message(last_response, user_message)
    last_response = get_completion_from_messages_dynamic(messages,max_tokens=1000)
    
    return last_response


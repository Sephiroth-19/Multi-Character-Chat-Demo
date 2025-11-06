from conversation import ConversationManager

cm = ConversationManager()

print('测试角色：罗宾')
reply1 = cm.ask("robin", "你好，请用两句话介绍一下自己。")
print('第一次回答：',reply1)
reply2 = cm.ask("robin", "你喜欢什么，现在在干什么，以后什么计划？")
print('第二次回答：',reply2)
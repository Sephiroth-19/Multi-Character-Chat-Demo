from characters import list_characters, get_character, get_default_character_key

print("默认角色：", get_default_character_key())
print("所有角色：", list_characters())

for key in list_characters().keys():
    c = get_character(key)
    print("\n---", c.name, "的 system prompt ---")
    print(c.system_prompt[:200] + "...")

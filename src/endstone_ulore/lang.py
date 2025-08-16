import os
import json


def load_lang_data(lang_dir: str) -> dict:
    zh_CN_file_path = os.path.join(lang_dir, 'zh_CN.json')
    en_US_file_path = os.path.join(lang_dir, 'en_US.json')

    if not os.path.exists(zh_CN_file_path):
        with open(zh_CN_file_path, 'w', encoding='utf-8') as f:
            zh_CN = {
                'item_name': '物品名称',
                'item_type': '物品类型',
                'item_enchants': '物品附魔',
                'item_lore': '物品特殊标签',

                'lore_text': '特殊标签文本',

                'button.back': '返回上一级',

                'message.type_error': '表单解析错误, 请按提示正确填写...',

                'add_lore.message.fail': '为物品添加特殊标签失败',
                'add_lore.message.fail.reason': '你的主手上没有持有任何物品...',
                'add_lore_form.title': '添加特殊标签',
                'add_lore_form.content': '请选择操作...',
                'add_lore_form.button.add_new_lore_text': '添加新特殊标签文本',

                'add_new_lore_text_form.title': '添加新特殊标签文本',
                'add_new_lore_text_form.textinput.label': '输入该物品的新特殊标签文本...',
                'add_new_lore_text_form.textinput.placeholder': '输入任意字符串但不能留空...',
                'add_new_lore_text_form.submit_button': '添加',

                'single_lore_text_form.title': '特殊标签文本',
                'single_lore_text_form.content': '请选择操作...',
                'single_lore_text_form.button.delete_lore_text': '删除该特殊标签文本',
                'single_lore_text_form.button.update_lore_text': '更新该特殊标签文本',

                'update_single_lore_text_form.title': '更新特殊标签文本',
                'update_single_lore_text_form.textinput.label': '输入该特殊标签文本的新名称...',
                'update_single_lore_text_form.textinput.placeholder': '输入任意字符串但不能留空...',
                'update_single_lore_text_form.submit_button': '更新',
            }
            json_str = json.dumps(zh_CN, indent=4, ensure_ascii=False)
            f.write(json_str)

    if not os.path.exists(en_US_file_path):
        with open(en_US_file_path, 'w', encoding='utf-8') as f:
            en_US = {
                'item_name': 'Item name',
                'item_type': 'Item type',
                'item_enchants': 'Item enchant(s)',
                'item_lore': 'Item lore',

                'lore_text': 'Lore text',

                'button.back': 'Back to previous',

                'message.type_error': 'The form is parsed incorrectly, please follow the prompts to fill in correctly...',

                'add_lore.message.fail': 'Failed to add lore text(s) for item(s)',
                'add_lore.message.fail.reason': 'your mainhand is empty...',
                'add_lore_form.title': 'Add lore',
                'add_lore_form.content': 'Please select a function...',
                'add_lore_form.button.add_new_lore_text': 'Add a new lore text',

                'add_new_lore_text_form.title': 'Add a new lore text',
                'add_new_lore_text_form.textinput.label': 'Input new lore text for this item...',
                'add_new_lore_text_form.textinput.placeholder': 'Input any string but cannot be blank...',
                'add_new_lore_text_form.submit_button': 'Add',

                'single_lore_text_form.title': 'Lore text',
                'single_lore_text_form.content': 'Please select a function...',
                'single_lore_text_form.button.delete_lore_text': 'Delete this lore text',
                'single_lore_text_form.button.update_lore_text': 'Update this lore text',

                'update_single_lore_text_form.title': 'Update lore text',
                'update_single_lore_text_form.textinput.label': 'Input new name of this lore text...',
                'update_single_lore_text_form.textinput.placeholder': 'Input any string but cannot be blank...',
                'update_single_lore_text_form.submit_button': 'Update',
            }
            json_str = json.dumps(en_US, indent=4, ensure_ascii=False)
            f.write(json_str)

    lang_data = {}

    for lang in os.listdir(lang_dir):
        lang_name = lang.strip('.json')

        lang_file_path = os.path.join(lang_dir, lang)

        with open(lang_file_path, 'r', encoding='utf-8') as f:
            lang_data[lang_name] = json.loads(f.read())

    return lang_data

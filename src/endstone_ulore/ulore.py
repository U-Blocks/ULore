import os
import json

from endstone import ColorFormat, Player, NamespacedKey
from endstone.plugin import Plugin
from endstone.form import ActionForm, ModalForm, TextInput
from endstone.inventory import ItemStack

from endstone_ulore.lang import load_lang_data

current_dir = os.getcwd()

first_dir = os.path.join(current_dir, 'plugins', 'ulore')

if not os.path.exists(first_dir):
    os.mkdir(first_dir)

lang_dir = os.path.join(first_dir, 'lang')

if not os.path.exists(lang_dir):
    os.mkdir(lang_dir)


class ulore(Plugin):
    api_version = '0.10'

    def __init__(self):
        super().__init__()

        # Load lang data
        self.lang_data = load_lang_data(lang_dir)

    def on_enable(self):
        if self.server.plugin_manager.get_plugin('ushop') is None:
            self.logger.error(
                f'{ColorFormat.RED}'
                f'Pre-plugin UShop is required...'
            )

            self.server.plugin_manager.disable_plugin(self)

            return

        self.logger.info(
            f'{ColorFormat.YELLOW}'
            f'ULore is enabled...'
        )

    # Add lore for item(s)
    def add_lore(self, player: Player):
        if player.inventory.item_in_main_hand is None:
            player.send_message(
                f'{ColorFormat.RED}'
                f'{self.get_text(player, "add_lore.message.fail")}: '
                f'{ColorFormat.WHITE}'
                f'{self.get_text(player, "add_lore.message.fail.reason")}'
            )

            return

        itemstack = player.inventory.item_in_main_hand

        item_amount = itemstack.amount

        item_type_id = itemstack.type.id

        item_type_translation_key = itemstack.type.translation_key

        item_name = self.server.language.translate(
            item_type_translation_key,
            None,
            player.locale
        )

        item_enchants = itemstack.item_meta.enchants

        item_enchants_display = '\n'

        for item_enchant_key, item_enchant_level in item_enchants.items():
            item_enchant_translation_key = self.server.enchantment_registry.get(NamespacedKey.from_string(item_enchant_key)).translation_key

            item_enchant_name = self.server.language.translate(
                item_enchant_translation_key,
                None,
                player.locale
            )

            item_enchants_display += f'{item_enchant_name} [lvl {item_enchant_level}]\n'

        if itemstack.item_meta.has_lore:
            item_lore = itemstack.item_meta.lore
        else:
            item_lore = []

        item_lore_display = '\n'

        if item_lore:
            for il in item_lore:
                item_lore_display += f'{il}\n'

        add_lore_form = ActionForm(
            title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}'
                  f'{self.get_text(player, "add_lore_form.title")}',
            content=f'{ColorFormat.GREEN}'
                    f'{self.get_text(player, "item_name")}: '
                    f'{ColorFormat.WHITE}'
                    f'{item_name}\n'
                    f'\n'
                    f'{ColorFormat.GREEN}'
                    f'{self.get_text(player, "item_type")}: '
                    f'{ColorFormat.WHITE}'
                    f'{item_type_id}\n'
                    f'\n'
                    f'{ColorFormat.GREEN}'
                    f'{self.get_text(player, "item_enchants")}: '
                    f'{ColorFormat.WHITE}'
                    f'{item_enchants_display}'
                    f'{ColorFormat.GREEN}'
                    f'{self.get_text(player, "item_lore")}: '
                    f'{ColorFormat.WHITE}'
                    f'{item_lore_display}'
                    f'\n'
                    f'{ColorFormat.GREEN}'
                    f'{self.get_text(player, "add_lore_form.content")}',
            on_close=self.server.plugin_manager.get_plugin('ushop').official_shop
        )

        add_lore_form.add_button(
            f'{ColorFormat.YELLOW}'
            f'{self.get_text(player, "add_lore_form.button.add_new_lore_text")}',
            icon='textures/ui/color_plus',
            on_click=self.add_new_lore_text(
                item_name,
                item_amount,
                item_type_id,
                item_enchants,
                item_lore
            )
        )

        il_index = 0

        for il in item_lore:
            add_lore_form.add_button(
                il,
                icon='textures/items/name_tag',
                on_click=self.single_lore_text(
                    item_amount,
                    item_type_id,
                    item_enchants,
                    item_lore,
                    il,
                    il_index
                )
            )

            il_index += 1

        player.send_form(add_lore_form)

    # Add new lore text
    def add_new_lore_text(self, item_name, item_amount, item_type_id, item_enchants, item_lore):
        def on_click(player: Player):
            textinput = TextInput(
                label=f'{ColorFormat.GREEN}'
                      f'{self.get_text(player, "item_name")}: '
                      f'{ColorFormat.WHITE}'
                      f'{item_name}\n'
                      f'\n'
                      f'{ColorFormat.GREEN}'
                      f'{self.get_text(player, "add_new_lore_text_form.textinput.label")}',
                placeholder=self.get_text(player, "add_new_lore_text_form.textinput.placeholder")
            )

            add_new_lore_form = ModalForm(
                title=f'{ColorFormat.GOLD}{ColorFormat.LIGHT_PURPLE}'
                      f'{self.get_text(player, "add_new_lore_text_form.title")}',
                controls=[textinput],
                submit_button=f'{ColorFormat.YELLOW}'
                              f'{self.get_text(player, "add_new_lore_text_form.submit_button")}',
                on_close=self.add_lore
            )

            def on_submit(p: Player, json_str: str):
                data = json.loads(json_str)

                if len(data[0]) == 0:
                    player.send_message(
                        f'{ColorFormat.RED}'
                        f'{self.get_text(player, "message.type_error")}'
                    )

                    return

                new_lore_text = data[0]

                item_lore.append(new_lore_text)

                itemstack = ItemStack(
                    type=item_type_id,
                    amount=item_amount
                )

                itemmeta_copy = itemstack.item_meta

                if item_enchants:
                    for item_enchant_key, item_enchant_level in item_enchants.items():
                        itemmeta_copy.add_enchant(
                            id=item_enchant_key,
                            level=item_enchant_level
                        )

                itemmeta_copy.lore = item_lore

                itemstack.set_item_meta(itemmeta_copy)

                player.inventory.item_in_main_hand = None

                player.inventory.item_in_main_hand = itemstack

                self.add_lore(p)

            add_new_lore_form.on_submit = on_submit

            player.send_form(add_new_lore_form)

        return on_click

    # Single lore text
    def single_lore_text(self, item_amount, item_type_id, item_enchants, item_lore, lore_text, lore_index):
        def on_click(player: Player):
            single_lore_text_form = ActionForm(
                title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}'
                      f'{self.get_text(player, "single_lore_text_form.title")}',
                content=f'{ColorFormat.GREEN}'
                        f'{self.get_text(player, "lore_text")}: '
                        f'{ColorFormat.WHITE}'
                        f'{lore_text}\n'
                        f'\n'
                        f'{ColorFormat.GREEN}'
                        f'{self.get_text(player, "single_lore_text_form.content")}',
                on_close=self.add_lore
            )

            # Delete single lore text
            single_lore_text_form.add_button(
                f'{ColorFormat.YELLOW}'
                f'{self.get_text(player, "single_lore_text_form.button.delete_lore_text")}',
                icon='textures/ui/icon_trash',
                on_click=self.delete_single_lore_text(
                    item_amount,
                    item_type_id,
                    item_enchants,
                    item_lore,
                    lore_index
                )
            )

            # Update single lore text
            single_lore_text_form.add_button(
                f'{ColorFormat.YELLOW}'
                f'{self.get_text(player, "single_lore_text_form.button.update_lore_text")}',
                icon='textures/ui/refresh',
                on_click=self.update_single_lore_text(
                    item_amount,
                    item_type_id,
                    item_enchants,
                    item_lore,
                    lore_index
                )
            )

            single_lore_text_form.add_button(
                f'{ColorFormat.YELLOW}'
                f'{self.get_text(player, "button.back")}',
                icon='textures/ui/refresh_light',
                on_click=self.add_lore
            )

            player.send_form(single_lore_text_form)

        return on_click

    # Delete single lore text
    def delete_single_lore_text(self, item_amount, item_type_id, item_enchants, item_lore, lore_index):
        def on_click(player: Player):
            item_lore.pop(lore_index)

            itemstack = ItemStack(
                type=item_type_id,
                amount=item_amount
            )

            itemmeta_copy = itemstack.item_meta

            if item_enchants:
                for item_enchant_key, item_enchant_level in item_enchants.items():
                    itemmeta_copy.add_enchant(
                        id=item_enchant_key,
                        level=item_enchant_level
                    )

            itemmeta_copy.lore = item_lore

            itemstack.set_item_meta(itemmeta_copy)

            player.inventory.item_in_main_hand = None

            player.inventory.item_in_main_hand = itemstack

            self.add_lore(player)

        return on_click

    # Update single lore text
    def update_single_lore_text(self, item_amount, item_type_id, item_enchants, item_lore, lore_index):
        def on_click(player: Player):
            textinput = TextInput(
                label=f'{ColorFormat.GREEN}'
                      f'{self.get_text(player, "update_single_lore_text_form.textinput.label")}',
                placeholder=self.get_text(player, "update_single_lore_text_form.textinput.placeholder"),
                default_value=item_lore[lore_index]
            )

            update_single_lore_text_form = ModalForm(
                title=f'{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}'
                      f'{self.get_text(player, "update_single_lore_text_form.title")}',
                controls=[textinput],
                submit_button=f'{ColorFormat.YELLOW}'
                              f'{self.get_text(player, "update_single_lore_text_form.submit_button")}',
                on_close=self.add_lore
            )

            def on_submit(p: Player, json_str: str):
                data = json.loads(json_str)

                if len(data[0]) == 0:
                    p.send_message(
                        f'{ColorFormat.RED}'
                        f'{self.get_text(p, "message.type_error")}'
                    )

                    return

                update_lore_text = data[0]

                item_lore.pop(lore_index)

                item_lore.insert(lore_index, update_lore_text)

                itemstack = ItemStack(
                    type=item_type_id,
                    amount=item_amount
                )

                itemmeta_copy = itemstack.item_meta

                if item_enchants:
                    for item_enchant_key, item_enchant_level in item_enchants.items():
                        itemmeta_copy.add_enchant(
                            id=item_enchant_key,
                            level=item_enchant_level
                        )

                itemmeta_copy.lore = item_lore

                itemstack.set_item_meta(itemmeta_copy)

                p.inventory.item_in_main_hand = None

                p.inventory.item_in_main_hand = itemstack

                self.add_lore(p)

            update_single_lore_text_form.on_submit = on_submit

            player.send_form(update_single_lore_text_form)

        return on_click

    # Get text
    def get_text(self, player: Player, text_key: str) -> str:
        player_lang = player.locale

        try:
            if self.lang_data.get(player_lang) is None:
                text_value = self.lang_data['en_US'][text_key]
            else:
                if self.lang_data[player_lang].get(text_key) is None:
                    text_value = self.lang_data['en_US'][text_key]
                else:
                    text_value = self.lang_data[player_lang][text_key]

            return text_value
        except Exception as e:
            self.logger.error(
                f'{ColorFormat.RED}'
                f'{e}'
            )

            return text_key

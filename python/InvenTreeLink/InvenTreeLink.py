import adsk.core
import traceback

import os

try:
    from .apper import apper
    from . import config
    from . import functions

    # Create our addin definition object
    my_addin = apper.FusionApp(config.app_name, config.company_name, False)
    my_addin.root_path = config.app_path

    from .commands.ShowPartCommand import ShowPartCommand
    from .commands.BOMOverviewCommand import BomOverviewPaletteShowCommand
    from .commands.SendBomCommand import SendBomCommand
    from .commands.SendBomOnlineCommand import SendBomOnlineCommand
    from .commands.SendStepCommand import SendStepCommand

    # Commands
    my_addin.add_command(
        'Show part details',
        ShowPartCommand,
        {
            'cmd_description': 'Show the InvenTree part-details for the selected part',
            'cmd_id': config.DEF_SEND_PART,
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'Commands',
            'cmd_resources': config.DEF_SEND_PART,
            'command_visible': True,
            'command_promoted': False,
        }
    )

    my_addin.add_command(
        'Upload STEP to attachments',
        SendStepCommand,
        {
            'cmd_description': 'Generates a STEP file and attaches it to a part',
            'cmd_id': config.DEF_SEND_STEP,
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'Commands',
            'cmd_resources': config.DEF_SEND_BOM,
            'command_visible': True,
            'command_promoted': False,
            'palette_id': config.ITEM_PALETTE,
        }
    )

    # Palette
    my_addin.add_command(
        'Show BOM overview',
        BomOverviewPaletteShowCommand,
        {
            'cmd_description': 'Show the BOM overview palette',
            'cmd_id': config.DEF_SHOW_PALETTE,
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': config.APP_PANEL,
            'cmd_resources': 'ShowPalette',
            'command_visible': True,
            'command_promoted': True,
            'palette_id': config.ITEM_PALETTE,
            'palette_name': 'InvenTreeLink BOM overview',
            'palette_html_file_url': os.path.join('commands', 'palette_html', 'palette.html'),
            'palette_use_new_browser': True,
            'palette_is_visible': True,
            'palette_show_close_button': True,
            'palette_is_resizable': True,
            'palette_width': 500,
            'palette_height': 600,
        }
    )

    # Commands that need the palette
    my_addin.add_command(
        'Load BOM for assembly',
        SendBomCommand,
        {
            'cmd_description': 'Load the BOM for the assembly in the current file',
            'cmd_id': config.DEF_SEND_BOM,
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': config.APP_PANEL,
            'cmd_resources': config.DEF_SEND_BOM,
            'command_visible': True,
            'command_promoted': False,
            'palette_id': config.ITEM_PALETTE,
        }
    )

    my_addin.add_command(
        'Get InvenTree Information',
        SendBomOnlineCommand,
        {
            'cmd_description': 'Fetch the InvenTree information for all BOM-parts',
            'cmd_id': config.DEF_SEND_ONLINE_STATE,
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': config.APP_PANEL,
            'cmd_resources': config.DEF_SEND_ONLINE_STATE,
            'command_visible': True,
            'command_promoted': False,
            'palette_id': config.ITEM_PALETTE,
        }
    )

    app = adsk.core.Application.cast(adsk.core.Application.get())
    ui = app.userInterface

    functions.init_sentry()
    functions.load_config()
    functions.init_Fusion360()

except:  # noqa: E722
    app = adsk.core.Application.get()
    ui = app.userInterface
    if ui:
        ui.messageBox('Initialization Failed: {}'.format(traceback.format_exc()))

debug = True


def run(context):
    my_addin.run_app()


def stop(context):
    my_addin.stop_app()

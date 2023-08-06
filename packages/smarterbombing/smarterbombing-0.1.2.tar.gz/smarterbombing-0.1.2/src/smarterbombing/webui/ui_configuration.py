"""Configuration UI"""
import gradio as gr

from smarterbombing.configuration import save_configuration

def render_configuration(configuration, configuration_path):
    """Render the configuration UI"""
    def _character_list():
        return ', '.join(configuration['characters'])

    def _add_character(character_name):
        characters = configuration['characters']
        characters.append(character_name)
        save_configuration(configuration, configuration_path)
        print(f'added character -> {character_name}')

        return _character_list()

    def _change_log_directory(new_log_directory):
        configuration['log_directory'] = new_log_directory
        save_configuration(configuration, configuration_path)
        print(f'changed log_directory -> {new_log_directory}')

    def _change_dps_rolling_window(seconds):
        configuration['dps_rolling_window_seconds'] = seconds
        save_configuration(configuration, configuration_path)

    dps_rolling_window_seconds = gr.Slider(label='Average Window (Seconds)',
                                           minimum=0.0, maximum=300,
                                           value=configuration['dps_rolling_window_seconds'])
    dps_rolling_window_seconds.change(fn=_change_dps_rolling_window,
                                      inputs=[dps_rolling_window_seconds])

    log_directory = gr.Textbox(
        value=configuration['log_directory'],
        label="EVE Online Log Directory")
    log_directory.submit(fn=_change_log_directory, inputs=[log_directory])

    add_character = gr.Textbox(
        placeholder='Character name',
        label='Add Character')

    gr.Markdown('### Characters')
    character_list = gr.Markdown(_character_list())

    add_character.submit(fn=_add_character, inputs=[add_character], outputs=[character_list])

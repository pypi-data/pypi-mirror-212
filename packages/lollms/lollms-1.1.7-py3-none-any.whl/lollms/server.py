from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from lollms import AIPersonality, MSG_TYPE
from lollms.binding import BindingConfig
import importlib
from pathlib import Path
import argparse
import logging
import shutil


# Reset
color_reset = '\u001b[0m'

# Regular colors
color_black = '\u001b[30m'
color_red = '\u001b[31m'
color_green = '\u001b[32m'
color_yellow = '\u001b[33m'
color_blue = '\u001b[34m'
color_magenta = '\u001b[35m'
color_cyan = '\u001b[36m'
color_white = '\u001b[37m'

# Bright colors
color_bright_black = '\u001b[30;1m'
color_bright_red = '\u001b[31;1m'
color_bright_green = '\u001b[32;1m'
color_bright_yellow = '\u001b[33;1m'
color_bright_blue = '\u001b[34;1m'
color_bright_magenta = '\u001b[35;1m'
color_bright_cyan = '\u001b[36;1m'
color_bright_white = '\u001b[37;1m'



class LoLLMsServer:
    def __init__(self):
        self.app = Flask("LoLLMsServer_Server")
        self.app.config['SECRET_KEY'] = 'your-secret-key'
        CORS(self.app)  # Enable CORS for all routes
        self.socketio = SocketIO(self.app)
        self.clients = {}
        self.models = []
        self.personalities = {}
        self.answer = ['']

        # Set log level to warning
        self.app.logger.setLevel(logging.WARNING)
        # Configure a custom logger for Flask-SocketIO
        self.socketio_log = logging.getLogger('socketio')
        self.socketio_log.setLevel(logging.WARNING)
        self.socketio_log.addHandler(logging.StreamHandler())

        self.initialize_routes()

    def initialize_routes(self):
        @self.socketio.on('connect')
        def handle_connect():
            client_id = request.sid
            self.clients[client_id] = {"namespace": request.namespace, "full_discussion_blocks": []}
            print(f'Client connected with session ID: {client_id}')

        @self.socketio.on('disconnect')
        def handle_disconnect():
            client_id = request.sid
            if client_id in self.clients:
                del self.clients[client_id]
            print(f'Client disconnected with session ID: {client_id}')

        @self.socketio.on('list_personalities')
        def handle_list_personalities():
            personality_names = list(self.personalities.keys())
            emit('personalities_list', {'personalities': personality_names}, room=request.sid)

        @self.socketio.on('add_personality')
        def handle_add_personality(data):
            personality_path = data['path']
            try:
                personality = AIPersonality(personality_path)
                self.personalities[personality.name] = personality
                emit('personality_added', {'name': personality.name}, room=request.sid)
            except Exception as e:
                error_message = str(e)
                emit('personality_add_failed', {'error': error_message}, room=request.sid)

        @self.socketio.on('generate_text')
        def handle_generate_text(data):
            model = self.models[0]
            client_id = request.sid
            prompt = data['prompt']
            personality: AIPersonality = self.personalities[data['personality']]
            # Placeholder code for text generation
            # Replace this with your actual text generation logic
            print(f"Text generation requested by client: {client_id}")

            self.answer[0] = ''
            full_discussion_blocks = self.clients[client_id]["full_discussion_blocks"]

            def callback(text, message_type: MSG_TYPE):
                if message_type == MSG_TYPE.MSG_TYPE_CHUNK:
                    self.answer[0] = self.answer[0] + text
                    emit('text_chunk', {'chunk': text}, room=client_id)
                return True

            if personality.processor is not None and personality.processor_cfg["process_model_input"]:
                preprocessed_prompt = personality.processor.process_model_input(prompt)
            else:
                preprocessed_prompt = prompt

            full_discussion_blocks.append(personality.user_message_prefix)
            full_discussion_blocks.append(preprocessed_prompt)
            full_discussion_blocks.append(personality.link_text)
            full_discussion_blocks.append(personality.ai_message_prefix)

            full_discussion = personality.personality_conditioning + ''.join(full_discussion_blocks)

            print(f"---------------- Input prompt -------------------")
            print(f"{color_green}{full_discussion}")
            print(f"{color_reset}--------------------------------------------")
            if personality.processor is not None and personality.processor_cfg["custom_workflow"]:
                print("processing...", end="", flush=True)
                generated_text = personality.processor.run_workflow(prompt, full_discussion, callback=callback)
            else:
                print("generating...", end="", flush=True)
                generated_text = model.generate(full_discussion, n_predict=personality.model_n_predicts,
                                                callback=callback)
            full_discussion_blocks.append(generated_text)
            print(f"{color_green}ok{color_reset}", end="", flush=True)

            # Emit the generated text to the client
            emit('text_generated', {'text': generated_text}, room=client_id)

    def build_model(self, bindings_path: Path, cfg: BindingConfig):
        binding_path = Path(bindings_path) / cfg["binding_name"]
        # first find out if there is a requirements.txt file
        install_file_name = "install.py"
        install_script_path = binding_path / install_file_name
        if install_script_path.exists():
            module_name = install_file_name[:-3]  # Remove the ".py" extension
            module_spec = importlib.util.spec_from_file_location(module_name, str(install_script_path))
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            if hasattr(module, "Install"):
                module.Install(self.config)
        # define the full absolute path to the module
        absolute_path = binding_path.resolve()
        # infer the module name from the file path
        module_name = binding_path.stem
        # use importlib to load the module from the file path
        loader = importlib.machinery.SourceFileLoader(module_name, str(absolute_path / "__init__.py"))
        binding_module = loader.load_module()
        binding_class = getattr(binding_module, binding_module.binding_name)

        model = binding_class(cfg)
        return model

    def run(self, host="localhost", port="9600"):
        parser = argparse.ArgumentParser()
        parser.add_argument('--host', '-hst', default=host, help='Host name')
        parser.add_argument('--port', '-prt', default=port, help='Port number')

        parser.add_argument('--config', '-cfg', default=None, help='Path to the configuration file')
        parser.add_argument('--bindings_path', '-bp', default=str(Path(__file__).parent / "bindings_zoo"),
                            help='The path to the Bindings folder')
        parser.add_argument('--personalities_path', '-pp',
                            default=str(Path(__file__).parent / "personalities_zoo"),
                            help='The path to the personalities folder')
        parser.add_argument('--models_path', '-mp', default=str(Path(__file__).parent / "models"),
                            help='The path to the models folder')

        parser.add_argument('--binding_name', '-b', default="llama_cpp_official",
                            help='Binding to be used by default')
        parser.add_argument('--model_name', '-m', default="Manticore-13B.ggmlv3.q4_0.bin",
                            help='Model name')
        parser.add_argument('--personality_full_name', '-p', default="personality",
                            help='Personality path relative to the personalities folder (language/category/name)')

        args = parser.parse_args()

        if args.config is None:
            original = Path(__file__).parent / "configs/config.yaml"
            local = Path(__file__).parent / "configs/local_config.yaml"
            if not local.exists():
                shutil.copy(original, local)
            cfg_path = local

        print("█       █        █       █▄  ▄█▄  ▄█")
        print("█       █        █       █ ▀▀   ▀▀ █")
        print("█       █        █       █         █")
        print("█▄▄▄▄   █▄▄▄▄▄   █▄▄▄▄   █         █")

        if cfg_path.exists():
            self.config = BindingConfig(cfg_path)
        else:
            self.config = BindingConfig()

        if args.binding_name:
            self.config.binding_name = args.binding_name

        if args.model_name:
            self.config.model_name = args.model_name

        model = self.build_model(args.bindings_path, self.config)
        self.models.append(model)

        self.personalities["default_personality"] = AIPersonality()

        for p in self.config.personalities:
            personality = AIPersonality(self.config.personalities_path/p)
            self.personalities[personality.name] = personality

        print("running...")
        self.socketio.run(self.app, host=args.host, port=args.port)

if __name__ == '__main__':
    server = AIPersonalityServer()
    server.run()

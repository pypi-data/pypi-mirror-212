from lollms import AIPersonality, lollms_path
from lollms.binding import BindingConfig, LLMBinding
import shutil
import yaml
import importlib
from pathlib import Path
import sys

class BindingBuilder:
    def build_binding(self, bindings_path: Path, cfg: BindingConfig)->LLMBinding:
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
                module.Install(cfg)
        # define the full absolute path to the module
        absolute_path = binding_path.resolve()
        # infer the module name from the file path
        module_name = binding_path.stem
        # use importlib to load the module from the file path
        loader = importlib.machinery.SourceFileLoader(module_name, str(absolute_path / "__init__.py"))
        binding_module = loader.load_module()
        binding_class = getattr(binding_module, binding_module.binding_name)
        return binding_class
    

class ModelBuilder:
    def __init__(self, binding_class:LLMBinding, config:BindingConfig):
        self.binding_class = binding_class
        self.model = None
        self.build_model(config) 

    def build_model(self, cfg: BindingConfig):
        self.model = self.binding_class(cfg)

    def get_model(self):
        return self.model


class MainMenu:
    def __init__(self, conversation):
        self.binding_infs = []
        self.conversation = conversation

    def show_menu(self, options):
        print("Menu:")
        for index, option in enumerate(options):
            print(f"{index + 1} - {option}")
        choice = input("Enter your choice: ")
        return int(choice) if choice.isdigit() else -1

    def select_binding(self):
        bindings_list = []
        for p in (lollms_path/"bindings_zoo").iterdir():
            if p.is_dir():
                with open(p/"binding_card.yaml", "r") as f:
                    card = yaml.safe_load(f)
                with open(p/"models.yaml", "r") as f:
                    models = yaml.safe_load(f)
                entry=f"{card['name']} (by {card['author']})"
                bindings_list.append(entry)
                entry={
                    "name":p.name,
                    "card":card,
                    "models":models
                }
                self.binding_infs.append(entry)

        choice = self.show_menu(bindings_list)
        if 1 <= choice <= len(self.binding_infs):
            print(f"You selected binding: {self.binding_infs[choice - 1]['name']}")
            self.conversation.config['binding_name']=self.binding_infs[choice - 1]['name']
            self.conversation.load_binding()
            self.conversation.config.save_config()
        else:
            print("Invalid choice!")

    def select_model(self):
        models_dir:Path = (lollms_path/"models"/self.conversation.config['binding_name'])
        models_dir.mkdir(parents=True, exist_ok=True)
        models_list = [m.name for m in models_dir.iterdir()] + ["Install model"]
        choice = self.show_menu(models_list)
        if 1 <= choice <= len(models_list)-1:
            print(f"You selected model: {models_list[choice - 1]}")
            self.conversation.config['model_name']=models_list[choice - 1]
            self.conversation.load_model()
            self.conversation.config.save_config()
        elif choice <= len(models_list):
            self.install_model()
        else:
            print("Invalid choice!")

    def install_model(self):
        models_list = ["Install model from internet","Install model from local file"]
        choice = self.show_menu(models_list)
        if 1 <= choice <= len(models_list)-1:
            url = input("Give a URL to the model to be downloaded :")
            self.conversation.config.download_model(url)
            self.select_model()
        elif choice <= len(models_list):
            path = Path(input("Give a path to the model to be used on your PC:"))
            if path.exists():
                self.conversation.config.reference_model(path)
            self.select_model()
        else:
            print("Invalid choice!")

    def select_personality(self):
        personality_languages = [p.stem for p in (lollms_path/"personalities_zoo").iterdir()]
        print("Select language")
        choice = self.show_menu(personality_languages)
        if 1 <= choice <= len(personality_languages):
            language = personality_languages[choice - 1]
            print(f"You selected language: {language}")
            personality_categories = [p.stem for p in lollms_path/"personalities_zoo"/language]
            print("Select category")
            choice = self.show_menu(personality_categories)
            if 1 <= choice <= len(personality_categories):
                category = personality_categories[choice - 1]
                print(f"You selected category: {category}")

                personality_names = [p.stem for p in lollms_path/"personalities_zoo"/language/category]
                print("Select personality")
                choice = self.show_menu(personality_names)
                if 1 <= choice <= len(personality_names):
                    name = personality_names[choice - 1]
                    print(f"You selected personality: {name}")
                    self.conversation.config["personalities"]=[f"{language}/{category}/{name}"]
                    self.conversation.load_personality()
                    self.conversation.config.save_config()
                else:
                    print("Invalid choice!")

            else:
                print("Invalid choice!")

        else:
            print("Invalid choice!")

    def main_menu(self):
        while True:
            print("\nMain Menu:")
            print("1 - Select Binding")
            print("2 - Select Model")
            print("3 - Select Personality")
            print("0 - Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.select_binding()
            elif choice == "2":
                self.select_model()
            elif choice == "3":
                self.select_personality()
            elif choice == "0":
                print("Exiting the program...")
                break
            else:
                print("Invalid choice! Try again.")

class Conversation:
    def __init__(self):
        # url = "https://huggingface.co/TheBloke/Manticore-13B-GGML/resolve/main/Manticore-13B.ggmlv3.q4_0.bin"
        # personality_path = "english/generic/lollms"
        # model_name = url.split("/")[-1]

        # Change configuration
        original = lollms_path / "configs/config.yaml"
        local = lollms_path / "configs/local_config.yaml"
        if not local.exists():
            shutil.copy(original, local)
        self.cfg_path = local

        self.config = BindingConfig(self.cfg_path)
        # load binding
        self.load_binding()

        # Load model
        self.load_model()
        # cfg.binding_name = llm_binding.binding_folder_name
        # cfg.model_name = model_name

        # Load personality
        self.load_personality()

        print("█          █        █       █▄ ▄█▄ ▄█       ")
        print("█     ▄▀▀▄ █        █       █ ▀   ▀ █  ▄▀▀▄ ")
        print("█     █  █ █        █       █       █  ▀▄▄  ")
        print("█▄▄▄▄ ▀▄▄▀ █▄▄▄▄▄   █▄▄▄▄   █       █  ▄▄▄▀ ")

        print("Version: 1.0")
        print("By : ParisNeo")

        print("Base commands:")
        print("└ commands:")
        print("   ├ exit: exists the console")
        print("   ├ reset: resets the context")
        print("   ├ empty prompt: forces the codel to continue generating")
        print("   ├ context_infos: current context size and space left before cropping")
        print("   └ menu: shows main menu")
        # If there is a disclaimer, show it
        if self.personality.disclaimer != "":
            print("\nDisclaimer")
            print(self.personality.disclaimer)
            print()

        if self.personality.welcome_message:
            print(self.personality.welcome_message)
        

    def load_binding(self):
        try:
            self.binding_class = BindingBuilder().build_binding(lollms_path/"bindings_zoo", self.config)
        except Exception as ex:
            print(ex)
            print(f"Couldn't find binding. Please verify your configuration file at {self.cfg_path} or use the next menu to select a valid binding")
            MainMenu(self).select_binding()

    def load_model(self):
        if not self.config.check_model_existance():
            print(f"No model found for binding {self.config['binding_name']}")
            print("Please select a valid model or install a new one from a url")
            MainMenu(self).select_model()
            # cfg.download_model(url)
        else:
            try:
                self.model = ModelBuilder(self.binding_class, self.config).get_model()
            except Exception as ex:
                print(ex)
                print(f"Couldn't load model. Please verify your configuration file at {self.cfg_path} or use the next menu to select a valid model")
                MainMenu(self).select_model()

    def load_personality(self):
        self.personality = AIPersonality(lollms_path / "personalities_zoo" / self.config["personalities"][0], self.model)

    def reset_context(self):
        if self.personality.include_welcome_message_in_disucssion:
            full_discussion = (
                self.personality.ai_message_prefix +
                self.personality.welcome_message +
                self.personality.link_text
            )
        else:
            full_discussion = (
                self.personality.personality_conditioning +
                self.personality.link_text
            )
        return full_discussion
        
    def start_conversation(self):
        full_discussion = self.reset_context()
        cond_tk = self.personality.model.tokenize(self.personality.personality_conditioning)
        n_cond_tk = len(cond_tk)
        while True:
            try:
                prompt = input("You: ")
                if prompt == "exit":
                    return
                if prompt == "menu":
                    MainMenu(self).main_menu()
                    continue
                if prompt == "reset":
                    self.reset_context()
                    print("Context reset issued")
                    continue
                if prompt == "context_infos":
                    tokens = self.personality.model.tokenize(full_discussion)
                    print(f"Current context has {len(tokens)} tokes/ {self.config.ctx_size}")
                    continue                
                              
                if prompt != '':
                    if self.personality.processor is not None:
                        preprocessed_prompt = self.personality.processor.process_model_input(prompt)
                    else:
                        preprocessed_prompt = prompt
                        
                    full_discussion += (
                        self.personality.user_message_prefix +
                        preprocessed_prompt +
                        self.personality.link_text +
                        self.personality.ai_message_prefix
                    )
                    print(f"{self.personality.name}:", end='', flush=True)
                else:
                    print(output.strip(),end="",flush=True)

                def callback(text, type=None):
                    print(text, end="", flush=True)
                    return True

                tk = self.personality.model.tokenize(full_discussion)
                n_tokens = len(tk)
                fd = self.personality.model.detokenize(tk[-min(self.config.ctx_size-n_cond_tk,n_tokens):])
                
                output = self.personality.model.generate(self.personality.personality_conditioning+fd, n_predict=self.personality.model_n_predicts, callback=callback)
                full_discussion += output.strip()
                print("\n")

                if self.personality.processor is not None:
                    if self.personality.processor.process_model_output is not None:
                        output = self.personality.processor.process_model_output(output)

            except KeyboardInterrupt:
                print("Keyboard interrupt detected.\nBye")
                break

        print("Done")
        print(f"{self.personality}")

def main():
    conversation = Conversation()
    conversation.start_conversation()
    

if __name__ == "__main__":
    main()
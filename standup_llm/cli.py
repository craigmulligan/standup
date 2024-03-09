import fire
from standup_llm.config import get_config, save_config, DEFAULT_CONFIG
from standup_llm.llm import llm_factory
from standup_llm.utils import Git
from standup_llm.prompts import prompt
import questionary


class Standup():
    """
    standup generates a standup message from your
    latest git commit messages and diffs.
    """
    def run(self, sha: str):
        f"""
        Given a git sha it'll generate a standup message from HEAD to the target sha
        grouped by author.
        """
        config = get_config()
        git = Git()
        llm = llm_factory(config)
        logs = git.logs(sha)
        full_log = "\n\n\n".join([f"""message:\n {log["commit"].message}\n\nauthor: {log["commit"].author.name}\n\ndiff:\n\n{log['diffs']}""" for log in logs])

        docs = llm.text_splitter(full_log)
        output = llm.summarize_docs(docs, prompt)
        print(output['output_text'])

    def configure(self):
        f"""
        Configures standup with your llm. 
        """
        config = get_config()
        model_type = questionary.select(
            "🤖 Select model type:",
            choices=[
                {"name": "OpenAI", "value": "openai"},
                {"name": "Local", "value": "local"},
                {"name": "Ollama", "value": "ollama"},
            ]
        ).ask()
        config["model_type"] = model_type
        if model_type == "openai":
            model_name = input("🤖 Enter your model name (default: gpt-3.5-turbo): ") or DEFAULT_CONFIG["model_name"]
            config["model_name"] = model_name

            api_key = questionary.password("🤖 Enter your API key: ").ask()
            config["api_key"] = api_key
        if model_type == "ollama":
            model_name = input("🤖 Enter your model name (default: llama2): ") or "llama2"
            config["model_name"] = model_name

            base_url = input("🤖 Enter your base url (default: http://localhost:11434)") or "http://localhost:11434"
            config["base_url"] = base_url
        else:
            model_path = input(f"🤖 Enter your model path: (default: {DEFAULT_CONFIG['model_path']}) ")
            config["model_path"] = model_path

        save_config(config)

def main():
    try:
        fire.Fire(Standup)
    except KeyboardInterrupt:
        print("\n🤖 Bye!")
    except Exception as e:
        if str(e) == "<empty message>":
            print("🤖 Please configure your API key. Use talk-codebase configure")
        else:
            raise e


if __name__ == "__main__":
    main()

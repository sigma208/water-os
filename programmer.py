import subprocess
import execjs
import rubyeval
import lupa
from lupa import LuaRuntime

class MultiLanguageProgrammer:
    def __init__(self):
        self.languages = {
            "python": {"extension": ".py", "interpreter": self.run_python},
            "javascript": {"extension": ".js", "interpreter": self.run_javascript},
            "ruby": {"extension": ".rb", "interpreter": self.run_ruby},
            "java": {"extension": ".java", "interpreter": self.run_java},
            "cpp": {"extension": ".cpp", "interpreter": self.run_cpp},
            "lua": {"extension": ".lua", "interpreter": self.run_lua},
        }

    def run_python(self, code):
        try:
            exec(code)
        except Exception as e:
            print(f"Ошибка при выполнении Python кода: {e}")

    def run_javascript(self, code):
        try:
            context = execjs.compile(code)
            context.call("eval")
        except Exception as e:
            print(f"Ошибка при выполнении JavaScript кода: {e}")

    def run_ruby(self, code):
        try:
            result = rubyeval.eval(code)
            print(result)
        except Exception as e:
            print(f"Ошибка при выполнении Ruby кода: {e}")

    def run_java(self, code):
        try:
            filename = "temp_code.java"
            with open(filename, "w") as file:
                file.write(code)
            subprocess.run(["javac", filename], check=True)
            subprocess.run(["java", "temp_code"], check=True)
        except Exception as e:
            print(f"Ошибка при выполнении Java кода: {e}")
        finally:
            import os
            os.remove(filename)
            try:
                os.remove("temp_code.class")
            except FileNotFoundError:
                pass

    def run_cpp(self, code):
        try:
            filename = "temp_code.cpp"
            with open(filename, "w") as file:
                file.write(code)
            subprocess.run(["g++", filename, "-o", "temp_code"], check=True)
            subprocess.run(["./temp_code"], check=True)
        except Exception as e:
            print(f"Ошибка при выполнении C++ кода: {e}")
        finally:
            import os
            os.remove(filename)
            try:
                os.remove("temp_code")
            except FileNotFoundError:
                pass

    def run_lua(self, code):
        try:
            lua = LuaRuntime(unpack_returned_tuples=True)
            result = lua.execute(code)
            print(result)
        except Exception as e:
            print(f"Ошибка при выполнении Lua кода: {e}")

    def list_languages(self):
        print("Доступные языки:")
        for lang in self.languages:
            print(lang)

    def run_code(self, language, code):
        if language not in self.languages:
            print(f"Язык '{language}' не поддерживается.")
            return

        interpreter = self.languages[language]["interpreter"]
        interpreter(code)

# Пример использования
programmer = MultiLanguageProgrammer()
programmer.list_languages()

# Выполнение кода на Python
programmer.run_code("python", "print('Hello, World!')")

# Выполнение кода на JavaScript
programmer.run_code("javascript", "console.log('Hello, World!')")

# Выполнение кода на Ruby
programmer.run_code("ruby", "puts 'Hello, World!'")

# Выполнение кода на Java
programmer.run_code("java", "public class temp_code { public static void main(String[] args) { System.out.println('Hello, World!'); } }")

# Выполнение кода на C++
programmer.run_code("cpp", "#include <iostream>\nint main() { std::cout << \"Hello, World!\" << std::endl; return 0; }")

# Выполнение кода на Lua
programmer.run_code("lua", "print('Hello, World!')")

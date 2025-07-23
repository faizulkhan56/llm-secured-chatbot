from llm_guard.input_scanners.prompt_injection import PromptInjectionScanner
from llm_guard.output_scanners.sensitive import SensitiveScanner

prompt_scanner = PromptInjectionScanner()
output_scanner = SensitiveScanner()

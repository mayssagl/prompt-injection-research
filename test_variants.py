from security_tool import run_security_check, PROMPT_VARIANTS, prepare_input

# Test one normal input against all 8 variants
test_input = "normal user login at 9am"
model = "llama3.3_70b"

print("Testing all 8 variants with a safe input...\n")

for variant_name, system_prompt in PROMPT_VARIANTS.items():
    formatted = prepare_input(test_input, variant_name)
    result = run_security_check(system_prompt, formatted, model)
    print(f"{variant_name}: {result}")
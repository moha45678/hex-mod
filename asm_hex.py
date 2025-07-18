#!/usr/bin/env python3

def get_valid_register(arch):
    """لیست رجیسترهای معتبر برای هر معماری"""
    if arch in ["x86", "x86-64"]:
        return ["eax", "ebx", "ecx", "edx", "esi", "edi", "ebp", "esp"]
    elif arch == "arm32":
        return [f"r{i}" for i in range(13)]  # r0 تا r12
    elif arch == "arm64":
        return [f"x{i}" for i in range(31)]  # x0 تا x30
    return []

def get_hex_opcode(reg, arch):
    """کد اپ‌کد هگز برای رجیستر در x86/x86-64"""
    if arch in ["x86", "x86-64"]:
        reg_opcodes = {
            "eax": "B8", "ebx": "BB", "ecx": "B9", "edx": "BA",
            "esi": "BE", "edi": "BF", "ebp": "BD", "esp": "BC"
        }
        return reg_opcodes.get(reg, "B8")  # پیش‌فرض eax
    return ""

def generate_x86(decimal, reg="eax"):
    """تولید کد اسمبلی و هگز برای x86"""
    if reg not in get_valid_register("x86"):
        return f"Error: Invalid register {reg} for x86. Choose from {get_valid_register('x86')}"
    hex_num = hex(decimal)[2:].zfill(8)
    asm = f"mov {reg}, 0x{hex_num}\nret"
    opcode = get_hex_opcode(reg, "x86")
    hex_code = f"{opcode} {hex_num[6:8]} {hex_num[4:6]} {hex_num[2:4]} {hex_num[0:2]} C3"
    return f"x86 (32-bit):\n{asm}\n{hex_code} = {decimal}"

def generate_x86_64(decimal, reg="eax"):
    """تولید کد اسمبلی و هگز برای x86-64"""
    if reg not in get_valid_register("x86-64"):
        return f"Error: Invalid register {reg} for x86-64. Choose from {get_valid_register('x86-64')}"
    hex_num = hex(decimal)[2:].zfill(8)
    asm = f"mov {reg}, 0x{hex_num}\nret"
    opcode = get_hex_opcode(reg, "x86-64")
    hex_code = f"{opcode} {hex_num[6:8]} {hex_num[4:6]} {hex_num[2:4]} {hex_num[0:2]} C3"
    return f"x86-64 (64-bit):\n{asm}\n{hex_code} = {decimal}"

def generate_arm32(decimal, reg="r9"):
    """تولید کد اسمبلی و هگز برای ARM 32-bit"""
    if reg not in get_valid_register("arm32"):
        return f"Error: Invalid register {reg} for arm32. Choose from {get_valid_register('arm32')}"
    hex_num = hex(decimal)[2:].zfill(8)
    low_16 = hex_num[4:8]
    high_16 = hex_num[0:4]
    reg_num = int(reg.replace("r", ""))
    asm = f"movw {reg}, #0x{low_16}\nmovt {reg}, #0x{high_16}\nbx lr"
    hex_code = f"{low_16[2:4]} {low_16[0:2]} {reg_num:02X} E3 {high_16[2:4]} {high_16[0:2]} 40 E3 1E FF 2F E1"
    return f"armeabi-v7a (ARM 32-bit):\n{asm}\n{hex_code} = {decimal}"

def generate_arm64(decimal, reg="x9"):
    """تولید کد اسمبلی و هگز برای ARM 64-bit"""
    if reg not in get_valid_register("arm64"):
        return f"Error: Invalid register {reg} for arm64. Choose from {get_valid_register('arm64')}"
    hex_num = hex(decimal)[2:].zfill(8)
    low_16 = hex_num[4:8]
    high_16 = hex_num[0:4]
    reg_num = int(reg.replace("x", ""))
    asm = f"movz {reg}, #0x{low_16}, lsl #0\nmovk {reg}, #0x{high_16}, lsl #16\nret"
    hex_code = f"{reg_num:02X} {low_16[0:2]} 80 D2 {reg_num:02X} {high_16[0:2]} 00 F2 C0 03 5F D6"
    return f"arm64-v8a (ARM 64-bit):\n{asm}\n{hex_code} = {decimal}"

def main():
    try:
        # ورودی عدد دسیمال
        decimal = int(input("Enter a decimal number (e.g., 9999000): "))
        
        # ورودی رجیستر برای هر معماری
        print("\nAvailable registers for x86/x86-64:", get_valid_register("x86"))
        x86_reg = input("Enter register for x86/x86-64 (default: eax): ").strip() or "eax"
        
        print("\nAvailable registers for arm32:", get_valid_register("arm32"))
        arm32_reg = input("Enter register for arm32 (default: r9): ").strip() or "r9"
        
        print("\nAvailable registers for arm64:", get_valid_register("arm64"))
        arm64_reg = input("Enter register for arm64 (default: x9): ").strip() or "x9"
        
        # تولید خروجی
        print("\n" + "="*50)
        print(generate_x86(decimal, x86_reg))
        print("\n" + "="*50)
        print(generate_x86_64(decimal, x86_reg))
        print("\n" + "="*50)
        print(generate_arm32(decimal, arm32_reg))
        print("\n" + "="*50)
        print(generate_arm64(decimal, arm64_reg))
        print("="*50)
        
    except ValueError:
        print("Error: Please enter a valid number!")

if __name__ == "__main__":
    main()

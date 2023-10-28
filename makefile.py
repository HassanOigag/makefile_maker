from sys import argv, exit
import os

red = "\033[31m"
green = "\033[32m"
reset = "\033[0m"

makefile = "Makefile"

def parse_line(new_files, compiler):
    file_extension = ".cpp" if compiler == "c++" else ".c"
    valid_files = [file for file in new_files if file.endswith(file_extension)]
    updated_files = []
    for valid_file in valid_files:
        if not os.path.exists(valid_file):
            colored_print(f"{valid_file} does not exist", red)
        else:
            updated_files.append(valid_file)
    return updated_files

def update_makefile(new_files):
    lines = []
    compiler = ""
    with open(makefile, 'r') as f:
        for line in f.readlines():
            if line.startswith(("CC =", "CXX =", "CXX=", "CC=")):
                compiler = line.split("=")[1].strip()
            if line.startswith("SRCS"):
                current_files_str = line.split("=")[1]
                current_files = current_files_str.split()
                updated_files = parse_line(new_files, compiler)
                for file in updated_files:
                    if file not in current_files:
                        current_files.append(file) 
                new_line = f"SRCS = {' '.join(current_files)}\n"
                lines.append(new_line)
            else:
                lines.append(line)
    return lines

def colored_print(text, color):
    print(f"{color}{text}{reset}")

def add_files(old_files):
    if not os.path.exists(makefile):
        colored_print("Makefile does not exist", red)
        exit(1)
    if not old_files:
        colored_print("please provide source files", red)
        exit(1)
    update = update_makefile(old_files)
    with open(makefile, "w") as f:
        for line in update:
            f.write(line)
    exit(0)

if __name__ == "__main__":
    usage = f"python3 {__file__} [output_file_name] [c/cpp]"
    output_file_name = "a.out"
    language = "c"
    if len(argv) == 2:
        output_file_name = argv[1]
        if (output_file_name == "help"):
            print(usage)
            exit(0)
        if (output_file_name == "add"):
            add_files(argv[2:])
    if len(argv) > 2:
        output_file_name = argv[1]
        if (output_file_name == "add"):
            add_files(argv[2:])
        language = argv[2]
    if len(output_file_name) == 0:
        output_file_name = "a.out"
    if len(language) == 0:
        language = "c"
    if language not in ["c", "cpp", "c++", "C", "C++", "CPP"]:
        colored_print(f"{language} is not supported", red)
        exit(1)
    if language in ["c", "C"]:
        compiler = "cc"
        file_extension = ".c"
    else:
        compiler = "c++"
        file_extension = ".cpp"

    additional_flag = "-std=c++98" if compiler == "c++" else ""
    if os.path.exists(makefile):
        colored_print(f"Makefile already exists", red)
        while True:
            try:
                answer = input("Do you want to overwrite it? [y/n]: ")
                if answer not in ["y", "n"]:
                    continue
                elif answer == "y":
                    break
                else:
                    colored_print(f"{makefile} was not created", red)
                    exit(0)
            except (KeyboardInterrupt, EOFError):
                exit(0)
    all_files = [f for f in os.listdir() if os.path.isfile(f) and f.endswith(file_extension)]
    srcs = " ".join(all_files)
    print("creating Makefile...")
    with open(makefile, "w") as f:
        flags = 'CFLAGS' if compiler == 'cc' else 'CXXFLAGS'
        cmpl = 'CC' if compiler == 'cc' else 'CXX'
        f.write(f"{cmpl} = {compiler}\n\n")
        f.write(f"{flags} = -Wall -Wextra -Werror {additional_flag}\n\n")
        f.write(f"NAME = {output_file_name}\n\n")
        f.write(f"SRCS = {srcs}\n\n")
        f.write(f"OBJS = $(SRCS:{file_extension}=.o)\n\n")
        f.write(f"all: $(NAME)\n\n")
        f.write(f"%.o: %{file_extension}\n")
        f.write(f"\t$({cmpl}) $({flags}) -c $< -o $@\n\n")
        f.write(f"$(NAME): $(OBJS)\n")
        f.write(f"\t$({cmpl}) $({flags}) $(OBJS) -o $(NAME)\n\n")
        f.write(f"clean:\n")
        f.write(f"\trm -f $(OBJS)\n\n")
        f.write(f"fclean: clean\n")
        f.write(f"\trm -f $(NAME)\n\n")
        f.write(f"re: fclean all\n\n")
        f.write(f"run: all\n")
        f.write(f"\t./$(NAME)\n\n")
        f.write(f".PHONY: all clean fclean re\n")
    colored_print(f"created: {makefile} successfully", green)

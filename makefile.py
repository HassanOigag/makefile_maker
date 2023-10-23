from sys import argv, exit
import os

red = "\033[31m"
green = "\033[32m"
reset = "\033[0m"

makefile = "Makefile"

def colored_print(text, color):
    print(f"{color}{text}{reset}")

if __name__ == "__main__":
    usage = f"python3 {__file__} [output_file_name] [c/cpp]"
    output_file_name = "a.out"
    language = "c"
    if len(argv) == 2:
        output_file_name = argv[1]
        if (output_file_name == "help"):
            print(usage)
            exit(0)
    if len(argv) > 2:
        output_file_name = argv[1]
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
        f.write(f"CC = {compiler}\n\n")
        f.write(f"CFLAGS = -Wall -Wextra -Werror {additional_flag}\n\n")
        f.write(f"NAME = {output_file_name}\n\n")
        f.write(f"SRCS = {srcs}\n\n")
        f.write(f"OBJS = $(SRCS:{file_extension}=.o)\n\n")
        f.write(f"all: $(NAME)\n\n")
        f.write(f"$(NAME): $(OBJS)\n")
        f.write(f"\t$(CC) $(CFLAGS) $(OBJS) -o $(NAME)\n\n")
        f.write(f"clean:\n")
        f.write(f"\trm -f $(OBJS)\n\n")
        f.write(f"fclean: clean\n")
        f.write(f"\trm -f $(NAME)\n\n")
        f.write(f"re: fclean all\n\n")
        f.write(f".PHONY: all clean fclean re\n")
    colored_print(f"created: {makefile} successfully", green)

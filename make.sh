#!/usr/bin/env bash
NAME=Makefile
OVERRIDE=0
ANSWER=""
EXEC="a.out"
COMPILER="cc"
EXSTENTION="c"
LANGUAGE=1
SRCS=$(ls *.c | tr "\n" " ")
USAGE="makefile [output_file] [c/c++]"

if [ $# -eq 1 ];then
	if [ "$1" == "help" ];then
		echo $USAGE
		exit 0
	fi
fi

if [ $# -eq 1 ];then
    EXEC=$1
fi

if [ $# -eq 2 ];then
    EXEC=$1
    LANGUAGE=2
fi

echo "creating a generic makefile..."
if [ -e $NAME ];then
    echo "$NAME already exists"
    echo "Do you want to override it? yes/no"
    read ANSWER
    while [ "$ANSWER" != "yes" ] && [ "$ANSWER" != "no" ]; do
        echo "Do you want to override it? yes/no"
        read ANSWER
    done

    if [ "$ANSWER" = "yes" ]; then
        OVERRIDE=1
    else
        OVERRIDE=0
    fi
else
    touch $NAME
    OVERRIDE=1
fi

if [ $LANGUAGE -eq 2 ]; then
    EXSTENTION="cpp"
    SRCS=$(ls *.$EXSTENTION | tr "\n" " " )
    COMPILER="c++"
fi

if (($OVERRIDE == 1)); then
    echo "CC = $COMPILER" > Makefile
else
    echo "makefile not overriden"
    exit 0
fi

echo "CFLAGS = -Wall -Werror -Wextra -std=c++98" >> $NAME
echo "NAME = $EXEC" >> $NAME
echo "SRCS = $SRCS" >> $NAME
echo "OBJS = \$(SRCS:.$EXSTENTION=.o)" >> $NAME
echo "" >> $NAME
echo "%.o: %.$EXSTENTION" >> $NAME
echo -e "\t\$(CC) \$(CFLAGS) -c \$^" >> $NAME
echo "" >> $NAME
echo "all: \$(NAME)" >> $NAME
echo "" >> $NAME
echo "\$(NAME): \$(OBJS)" >> $NAME
echo -e "\t\$(CC) \$(CFLAGS) \$^ -o \$@" >> $NAME
echo "" >> $NAME
echo "clean:" >> $NAME
echo -e "\trm -f \$(OBJS)" >> $NAME
echo "" >> $NAME
echo "fclean: clean" >> $NAME
echo -e "\trm -f \$(NAME)" >> $NAME
echo "" >> $NAME
echo "re: fclean all" >> $NAME
echo "" >> $NAME
echo ".PHONY: clean fclean all re" >> $NAME

echo "Makefile created successfully"

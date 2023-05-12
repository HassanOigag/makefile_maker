#!/bin/bash
NAME=Makefile
OVERRIDE=0
ANSWER=""
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

if (($OVERRIDE == 1)); then
    echo "CC = cc" > Makefile
else
    echo "makefile not overriden"
    exit 0
fi

echo "CFLAGS = -Wall -Werror -Wextra" >> $NAME
echo "NAME = a.out" >> $NAME
echo "SRCS = *.c" >> $NAME
echo "OBJS = \$(SRCS:.c=.o)" >> $NAME
echo "" >> $NAME
echo "%.o: %.c" >> $NAME
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
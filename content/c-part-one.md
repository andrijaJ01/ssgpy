---
title: Learn C - Part 1
subtitle: Learn basics of c and set up enviroment.
summary: Learn basics of c and set up enviroment.
slug: c-part-one
img: assets/img/0256.jpg
author: Andrija Jovnovic
date: 2020-05-15
---

# Learn C part 1 

C programming is an imperative procedural language. It was designed to compiled using a relatively straightforward compiler and it also provides the access to memory to provide language constructs to follow the machine instructions.

In this section, you will learn how to start with c programming and also I will explain this by using a simple and easy example program which prints the “Hello World”. Apart from this, you will also learn the below things:

- Basic commands of c programming.

- How to write a C program.

- A simple C program with an output.

- How to use cmake 

- How to compile and execute a C program

## C Hello world program

    #include <stdio.h>
    int main() {
    printf("Hello, World!");
    return 0;
    }

In code above we can recognize following:
    
- ```#include```: Used to "*Import*" libraries for use, like ```stdio.h``` which stands for *standard input output*.

- ```int main()```: Every program written in c starts executing from here.

- ```printf()```: Function from stdio.h library.

- ```return 0;```: statement is the **_"Exit status"_** of the program. In simple terms, the program ends with this statement.

## Compile and execute C program.

to compile C program there are few options, but here I will show one with ```cmake``` and ```ninja```.

### preparation

To continue make make for project and cd into it:

    mkdir project && cd project
    
and make following project structure:

    project
    ├── bin
    ├── build
    ├── build.sh
    ├── CMakeLists.txt
    ├── headers
    └── src

### CMakeLists.txt

In text editor open CMakeLists.txt and write following content.


    cmake_minimum_required (VERSION 3.5)

    project (HelloWorld)

    set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Werror")
    set (source_dir "${PROJECT_SOURCE_DIR}/src/")
    set (include_dir "${PROJECT_SOURCE_DIR}/headers/")
    set (CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_SOURCE_DIR}/bin/")
    set (PROJ_VERSION "0.1")

    include_directories(${include_dir})
    file (GLOB source_files "${source_dir}/*c" "${include_dir}/*h" )

    set (exec_name "main_${PROJ_VERSION}")

    add_executable  (${exec_name} ${source_files})

first we set minimum required version of cmake to 3.5, then some compiler flags so it shows all warnings and errors.

we set then directories where cmake can find source and header files as well as where to put executable and how to name it.

### build.sh

write:

    #!/bin/sh

    cmake -B './build' -G "Ninja" -DCMAKE_BUILD_TYPE=Debug 

save it and make it executable:

    sudo chmod +x build.sh
    
this is simple shell script that will just run cmake and set all required options like Build System to ```ninja``` , where to put build files and so on.

### source code

save the code we wrote above and name it as you want with ```.c``` extension, and place it in  ```./src``` directory.

in terminal, change directory to root of project where build.sh is located and run it

    ./build.sh
    
the command above will set up everything for compiling , to actually compile the code

    cd build && ninja && cd ..
    
This will cd to build folder where we set up build files in ```build.sh```

you can find executable in ```bin``` folder in root of project.

run it:

    ./bin/main_0.1
    
if everything went fine there should be ```Hello, World!``` printed in terminal.

## Some more examples

### pause before exiting

    #include <stdio.h>
    int main()
    {
    /* Our first simple C basic program */
    printf("Hello World! ");
    getch();
    return 0;
    }
    
__output__

    >Hello World
    
### accept user input

    #include <stdio.h>
    
    main()
    {
    int number;
    
    printf("Please enter an integer\n");
    scanf("%d",&number);
    
    printf("You have entered number is: %d\n", number);
    
    return 0;
    }
    
__output__

    >Enter an integer
    >50
    >Integer entered by you is 50
    
### cli arguments

first argument or argv\[0] is allways the program itself.

    #include <stdio.h>

    int main( int argc, char *argv[] ) {
            int i;

        printf( "argc:     %d\n", argc );
        printf( "argv[0]:  %s\n", argv[0] );

        if ( argc == 1 ) {
                printf( "No arguments were passed.\n" );
        } else {
                printf( "Arguments:\n" );

                for ( i = 1; i < argc; ++i ) {
                        printf( "  %d. %s\n", i, argv[i] );
                }
        }

        return 0;
    }
    
__output__

    >gcc argument.c
    >./a.out first
    argc:     2
    argv[0]:  ./a.out
    Arguments:
    1. first
    >./a.out first second third fourth fifth sixth seventh eighth ninth tenth eleventh twelfth
    argc:     13
    argv[0]:  ./a.out
    Arguments:
    1. first
    2. second
    3. third
    4. fourth
    5. fifth
    6. sixth
    7. seventh
    8. eighth
    9. ninth
    10. tenth
    11. eleventh
    12. twelfth
    > 


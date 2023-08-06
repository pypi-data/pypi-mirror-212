def parser(subparser):

    ans = subparser.add_parser(
        "setenv",
        help="Set environment variables for running easifem on your system.",
        description="""
        The [setenv] subcommand sets the environment variable \n
        for running easifem on your system. \n
        \n 
        While setting the environment you can provide following details. \n
        A) EASIFEM_INSTALL_DIR \n
        B) EASIFEM_BUILD_DIR \n
        C) EASIFEM_SOURCE_DIR \n
        \n
        EASIFEM_INSTALL_DIR: denotes the root location where EASIFEM will \n
        be installed. It is specified by \n
        --install=value. \n
        \n
        Following are the good choices for --install variable: \n
        1) ${HOME} \n
        2) ${HOME}/.local \n
        3) /opt \n
        \n
        The default value is ${HOME}.
        \n
        EASIFEM_SOURCE_DIR: specifies the location where the source code of \n
        the components of EASIFEM will be stored. \n
        It is specified by\n
        --source=value \n
        \n
        Following are the good choices for --source variable: \n
        1) ${HOME}/code/\n
        \n
        The default value is ${HOME}/code.
        \n
        EASIFEM_BUILD_DIR: specifies the location where the components of \n
        EASIFEM will be build. It is specified by\n
        --build=value \n
        \n
        Following are the good choices for --root variable: \n
        1) ${HOME}/temp \n
        \n
        The default value is ${HOME}/temp.
        \n

        Example

        easifem setenv --install ${HOME} --build ${HOME}/temp --source ${HOME}/code
        easifem setenv -r ${HOME} -b ${HOME}/temp -s ${HOME}/code
        """,
    )

    ans.add_argument(
        "-i",
        "--install",
        help="Root directory for easifem, EASIFEM_INSTALL_DIR",
        required=False,
    )

    ans.add_argument(
        "-b",
        "--build",
        help="Location where easifem will be build, EASIFEM_BUILD_DIR",
        required=False,
    )

    ans.add_argument(
        "-s",
        "--source",
        help="Location where the source-code of easifem will be stored, EASIFEM_SOURCE_DIR",
        required=False,
    )

    ans.add_argument(
        "--shell",
        help="System shell that you are using, you have following choices: [bash, zsh, fish]",
        required=False,
        choices=[
            "bash",
            "zsh",
            "fish",
        ],
    )

    ans.add_argument(
        "-q",
        "--quite",
        help="If specified lesser output will be printed",
        action="store_true",
    )

    return ans

def parser(subparser):

    ans = subparser.add_parser(
        "install",
        help="Install components of easifem.",
        description="""
        The [install] subcommand helps you installing the components of \n 
        EASIFEM, such as extpkgs, base, classes, materials, kernels, etc. \n
        \n
        In order to install a component you should specify following environment variables: \n
        A) EASIFEM_ROOT_DIR: the place where easifem is installed. \n
        B) EASIFEM_BUILD_DIR: the place where easifem is build. \n
        C) EASIFEM_SOURCE_DIR: the place where the source of easifem will be stored. \n
        \n
        You can specify them by using \n
        \n
        easifem setenv --build= --install= --source=
        \n
        For more see,\n
        easifem setenv --help \n
        \n
        """,
    )

    ans.add_argument(
        "-i",
        "--install",
        help="Location where easifem is installed, EASIFEM_INSTALL_DIR",
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
        "-q",
        "--quite",
        help="If specified lesser output will be printed",
        action="store_true",
    )

    ans.add_argument(
        "components",
        metavar="c",
        type=str,
        nargs="+",
        help="Names of components to install",
    )

    return ans

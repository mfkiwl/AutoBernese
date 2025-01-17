
!!! note "Work in progress"

    We are currently preparing the installation of Bernese GNSS Software version 5.4
    [BSW].

    This page will eventuelly explain to the users how we have set up the server
    that runs the software.

    For now, here are the settings that we have set during installation.

    The settings below are apt to change until we have established a good working solution
    for BSW and the automation program.


## Environments

BSW is installed in three different locations used for different purposes
focusing either on maintaining a durable production-ready [`prod`] installation
and more brittle environments for trying out new things with the automation
program [`dev`] and testing them [`test`], before they are made available in the
production environment.

| `[BSW_ENV]` | Description | Function                              | Updated/rebuilt                    |
| ----------- | ----------- | ------------------------------------- | ---------------------------------- |
| `prod`      | Production  | Used for actual work                  | With new BSW updates               |
| `test`      | Test        | Used for testing new features         | With new BSW updates               |
| `dev`       | Development | Wild west environment for developers. | When need a new fresh installation |

Each environment's paths are set in the following way parameterised byt the
short-names defined for the different environments:

| What                       | Value                               |
| -------------------------- | ----------------------------------- |
| Installation directory     | `/home/bsw/[BSW_ENV]/BERN54`        |
| DATAPOOL                   | `/home/bsw/[BSW_ENV]/data/DATAPOOL` |
| CAMPAIGN                   | `/home/bsw/[BSW_ENV]/CAMPAIGN54`    |
| SAVEDISK                   | `/home/bsw/[BSW_ENV]/SAVEDISK`      |
| User environment           | `$HOME/bsw/[BSW_ENV]/user`          |
| Temporary user environment | `$HOME/bsw/[BSW_ENV]/temp`          |


## Setup a user environment for Bernese GNSS Software

A user of BSW needs a user environment consisting of two user-specific
directories in the path established by the environment variables set in
`LOADGPS.setvar` script. To create a new user environment, you need to `source`
the file, run the configuration script and select the action that creates a new
user environment. This is demonstrated below.

A normal user should only need to create a user in what we have named the
production environment. (See previous section for details.)


!!! note "Deviations from the default installation"

    Between versions 5.2 and 5.4, the default names for the user environment
    directories have changed. However, we chose a different naming convention than
    the default one:

    | Directory      | 5.2         | 5.4       | 5.4 (our names) |
    | -------------- | ----------- | --------- | --------------- |
    | `basename($U)` | `GPSUSER52` | `GPSUSER` | `user`          |
    | `basename($T)` | `GPSTEMP`   | `GPSWORK` | `temp`          |


### Steps to create environment

On the server

*   Set environment variables for the current shell session

    ```sh
    source /home/bsw/prod/BERN54/LOADGPS.setvar
    ```

*   Run the BSW configuration tool.

    ```
    $EXE/configure.pm
    ```

    ``` title="Output" hl_lines="6"
    ==========================================
    CONFIGURATION OF THE BERNESE GNSS SOFTWARE
    ==========================================
    1 ... Update LOADGPS.setvar
    2 ... Install online updates
    3 ... Add a new user environment
    4 ... Compile the menu
    5 ... Compile the programs
    6 ... Install the example campaign
    7 ... Update / install Bernese license file
    8 ...   ---

    x ... Exit

    Enter option:
    ```

*   Choose option 3

    ``` title="Output" hl_lines="3"
    Enter option: 3

    Create user environment /home/<user>/bsw/user (y/n):
    ```

* Say yes `y`

    ``` title="Output" hl_lines="8"
    Create user environment /home/<user>/bsw/user (y/n): y

    Copying menu and program input files...
    Copying BPE user scripts...
    Copying examples for process control files...
    Copying BPE options for processing examples...
    Copying ICONS ...
    ### Archive of ICONS not found!

    **********************************************************************
    * User area /home/<user>/bsw/user
    * has been added/updated.
    **********************************************************************
    ```

Despite the warning above, the environment is now created by creating the above
directory as well as a temporary directory.

!!! info "Steps to delete an environment"

    If you need to delete an environment, this can be done by simply deleting the
    directory `[BSW_ENV]` corresponding to the user environment, you want to get rid
    of:

    ```
    rm -rf ~/bsw/[BSW_ENV]
    ```

### Initial directory content for a new user environment

A newly-created user environment contains to directories `temp` and `user`.
`temp` has no initial content, whereas `user` gets copies of content from source
directories under the main directory of the BErnese installation path. The `user
directory` is initialised with the following content:

| `user/*` | Initial content         |
| -------- | ----------------------- |
| `OPT`    | Copied from `$C/USER`   |
| `OUT`    | *Empty*                 |
| `PAN`    | Copied from `$C/SUPGUI` |
| `PCF`    | Copied from `$C/USER`   |
| `SCRIPT` | Copied from `$C/USER`   |
| `WORK`   | *Empty*                 |


## Campaign management

### Given: Newly-created campaign

A newly-created campaign consists of a directory with an arbitrary name and an
entry in the campaign menu `MENU_CMP.INP` panel file inside the Bernese
installation directory.

A new campaign directory has the following basic content:

```
.
├── ATM
├── BPE
├── GEN
│   ├── OBSERV_COD.SEL
│   └── SESSIONS.SES
├── GRD
├── OBS
├── ORB
├── ORX
├── OUT
├── RAW
├── SOL
└── STA
```

### Given: Possible campaign-directory paths

*   Campaigns do not have to follow the given example [`${P}/EXAMPLE`] but may
    be put in any desired directory, e.g.:

    ```
    /home/<some-user>/my-campaigns/campaign
    ```

    This means that our campaigns can and, probably, should, be ordered in sub
    directories by campaign type, e.g.:

    -   `${P}/<type-A>/2222`
    -   `${P}/<type-B>/2222`
    -   ...

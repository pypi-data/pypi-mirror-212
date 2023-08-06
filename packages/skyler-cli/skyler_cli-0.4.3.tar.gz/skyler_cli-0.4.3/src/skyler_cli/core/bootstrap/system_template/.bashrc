# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# If there is a default location, cd to it
defaultLocation='{{default_location_file_path}}'
if [ -s $defaultLocation ]; then
    if [ -d `cat $defaultLocation` ]; then
        cd `cat $defaultLocation`;
    fi
fi

g() {
    if [ -s $defaultLocation ]; then
      if [ -d `cat $defaultLocation` ];
        then
          cd $(cat /tmp/defaultTerminalLocation);
      fi;
    fi
}


if [ $(whoami) == 'root' ]; then
    PS1="\e[95m!\! \e[32m[\T] \e[91m$(whoami)\e[36m@\h \e[31m\w\e[39m\n# "
else
    PS1="\e[95m!\! \e[32m[\T] \e[36m$(whoami)@\h \e[31m\w\e[39m\n# "
fi

set -o vi
shopt -s cdspell

{{#aliases}}
alias {{key}}="{{{value}}}"
{{/aliases}}

lt() {
    ls -t $1 | head
}

if [[ -d "~/.bash_init_scripts" ]]; then
    for f in ~/.bash_setup_scripts/*; do
        source $f
    done
fi
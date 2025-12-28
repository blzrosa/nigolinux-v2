if status is-interactive
    # Commands to run in interactive sessions can go here
end

starship init fish | source

alias ls='lsd'
alias ll='lsd -l'
alias la='lsd -a'
alias lt='lsd --tree'

export EDITOR=nvim
export VISUAL=nvim

set -g fish_greeting ''

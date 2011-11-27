set autoindent smartindent et sts=4 tabstop=4 shiftwidth=4 expandtab softtabstop=4

" show the trilling spaces on red
highlight BadWhitespace ctermbg=red guibg=red
au BufRead,BufNewFile *.py,*.pyw match BadWhitespace /^\t\+/
au BufRead,BufNewFile *.py,*.pyw,*.c,*.h match BadWhitespace /\s\+$/

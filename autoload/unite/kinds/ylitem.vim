let s:save_cpo = &cpo
set cpo&vim

function! unite#kinds#ylitem#define() "{{{
  return s:kind
endfunction"}}}

let s:kind = {
      \ 'name' : 'ylitem',
      \ 'default_action' : 'paste',
      \ 'action_table': {},
      \}

" Actions "{{{
let s:kind.action_table.paste = {
      \ 'description' : 'paste word or text',
      \ }

function! s:kind.action_table.paste.func(candidate) "{{{
    let value = a:candidate.action__value

    call rpcrequest(g:yanklist_channel, "yanklist_choose", value)
    execute 'normal! p'

    " Open folds.
    normal! zv
endfunction"}}}
"}}}

let &cpo = s:save_cpo
unlet s:save_cpo



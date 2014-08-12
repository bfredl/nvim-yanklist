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
    let contents = a:candidate.action__text
    let regtype = a:candidate.action__regtype
    let old_reg = [getreg('"'), getregtype('"')]

    call setreg('"', contents, regtype)
    try
      execute 'normal! ""p'
    finally
      call setreg('"', old_reg[0], old_reg[1])
    endtry

    " Open folds.
    normal! zv
endfunction"}}}
"}}}

let &cpo = s:save_cpo
unlet s:save_cpo


